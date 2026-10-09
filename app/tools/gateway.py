import time
from typing import Protocol

from pydantic import ValidationError

from app.tools.contracts import (
    TOOL_ARGUMENT_MODELS,
    ToolResult,
    ToolTrace,
    ToolTraceOutcome,
    TrustedContext,
)
from app.tools.errors import ToolError


class Authorize(Protocol):
    def __call__(
        self, *, context: TrustedContext, tool_name: str, payment_id: str
    ) -> bool: ...


class Reader(Protocol):
    def __call__(
        self, *, tool_name: str, organization_id: str, arguments: object
    ) -> object: ...


class ToolGateway:
    def __init__(self, authorize: Authorize, reader: Reader) -> None:
        self.authorize = authorize
        self.reader = reader

    def execute(
        self, tool_name: str, arguments: object, context: TrustedContext
    ) -> ToolResult:
        started_at = time.perf_counter()
        argument_model = TOOL_ARGUMENT_MODELS.get(tool_name)
        if argument_model is None:
            duration = time.perf_counter() - started_at
            return self.build_error_report(
                context=context,
                tool_name=tool_name,
                payment_id=None,
                outcome=ToolTraceOutcome.REJECTED,
                error_code="UNKNOWN_TOOL",
                duration=duration,
            )

        try:
            parsed_argument = argument_model.model_validate(arguments)
        except ValidationError:
            duration = time.perf_counter() - started_at
            return self.build_error_report(
                context=context,
                tool_name=tool_name,
                payment_id=None,
                outcome=ToolTraceOutcome.REJECTED,
                error_code="INVALID_ARGUMENTS",
                duration=duration,
            )

        if (
            self.authorize(
                context=context,
                tool_name=tool_name,
                payment_id=parsed_argument.payment_id,
            )
            is not True
        ):
            duration = time.perf_counter() - started_at
            return self.build_error_report(
                context=context,
                tool_name=tool_name,
                payment_id=parsed_argument.payment_id,
                outcome=ToolTraceOutcome.REJECTED,
                error_code="UNAUTHORIZED",
                duration=duration,
            )

        data = self.reader(
            tool_name=tool_name,
            organization_id=context.organization_id,
            arguments=parsed_argument,
        )
        return ToolResult(
            data=data,
            error=None,
            trace=ToolTrace(
                organization_id=context.organization_id,
                request_id=context.request_id,
                payment_id=parsed_argument.payment_id,
                tool_name=tool_name,
                outcome=ToolTraceOutcome.SUCCEEDED,
                attempt=1,
                duration_ms=(time.perf_counter() - started_at) * 1000,
            ),
        )

    def build_error_report(
        self,
        *,
        context: TrustedContext,
        tool_name: str,
        payment_id: str | None,
        outcome: ToolTraceOutcome,
        error_code: str,
        duration: float,
    ) -> ToolResult:
        return ToolResult(
            data=None,
            error=ToolError(
                code=error_code, message=ToolError.error_code_to_message(error_code)
            ),
            trace=ToolTrace(
                organization_id=context.organization_id,
                request_id=context.request_id,
                payment_id=payment_id,
                tool_name=tool_name,
                outcome=outcome,
                error_code=error_code,
                attempt=1,
                duration_ms=duration * 1000,
            ),
        )
