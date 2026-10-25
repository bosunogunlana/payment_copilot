from collections.abc import Callable
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

from app.tools.contracts import ToolResult


class AttemptTrace(BaseModel):
    attempt: int = Field(ge=1)
    timeout_s: float = Field(gt=0, allow_inf_nan=False)
    duration_ms: float = Field(ge=0, allow_inf_nan=False)
    backoff_s: float = Field(ge=0, allow_inf_nan=False)
    result: ToolResult


class RetryPolicy(BaseModel):
    model_config = ConfigDict(frozen=True)

    max_attempts: int = Field(default=3, strict=True, ge=1)
    attempt_timeout_s: float = Field(
        default=1.0, strict=True, gt=0, allow_inf_nan=False
    )
    total_timeout_s: float = Field(default=5.0, strict=True, gt=0, allow_inf_nan=False)
    initial_backoff_s: float = Field(
        default=0.25, strict=True, ge=0, allow_inf_nan=False
    )
    max_backoff_s: float = Field(default=0.5, ge=0, strict=True, allow_inf_nan=False)


type StopReasons = Literal["success", "nonretryable", "max_attempts", "deadline"]


class RecoveryResult(BaseModel):
    result: ToolResult
    attempts: list[AttemptTrace]
    stop_reason: StopReasons


class Operation(Protocol):
    def __call__(self, *, timeout_s: float) -> ToolResult: ...


class RetryExecutor:
    def __init__(
        self,
        policy: RetryPolicy,
        clock: Callable[[], float],
        sleep: Callable[[float], None],
    ) -> None:
        self.policy = policy
        self.clock = clock
        self.sleep = sleep

    def run(self, operation: Operation) -> RecoveryResult:
        deadline = self.clock() + self.policy.total_timeout_s
        attempts: list[AttemptTrace] = []
        backoff = min(self.policy.initial_backoff_s, self.policy.max_backoff_s)

        def finish(reason: StopReasons) -> RecoveryResult:
            return RecoveryResult(
                result=attempts[-1].result, attempts=attempts, stop_reason=reason
            )

        for attempt_number in range(1, self.policy.max_attempts + 1):
            remaining_time = deadline - self.clock()

            if remaining_time <= 0:
                if not attempts:
                    raise TimeoutError("Deadline expired before the first attempt")
                return finish("deadline")

            timeout_s = min(self.policy.attempt_timeout_s, remaining_time)
            started_at = self.clock()

            result = operation(timeout_s=timeout_s).model_copy(deep=True)

            elapsed_s = self.clock() - started_at
            duration_ms = elapsed_s * 1000

            result.trace.attempt = attempt_number
            result.trace.duration_ms = duration_ms

            attempt_trace = AttemptTrace(
                attempt=attempt_number,
                timeout_s=timeout_s,
                duration_ms=duration_ms,
                backoff_s=0,
                result=result,
            )
            attempts.append(attempt_trace)

            if result.error is None:
                return finish("success")

            remaining_time = deadline - self.clock()
            if remaining_time <= 0:
                return finish("deadline")

            error = result.error
            if not error.retryable:
                return finish("nonretryable")

            if attempt_number == self.policy.max_attempts:
                return finish("max_attempts")

            if backoff >= remaining_time:
                return finish("deadline")

            attempt_trace.backoff_s = backoff
            self.sleep(backoff)

            backoff = min(backoff * 2, self.policy.max_backoff_s)

        raise AssertionError("Validated attempt limit must allow at least one attempt.")
