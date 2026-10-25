"""Offline Phase 5 evidence: real boundaries, scripted failures, no API calls."""

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from app.llm.tool_loop import ToolLoop
from app.tools.contracts import ToolResult, ToolTrace, TrustedContext
from app.tools.errors import ToolError, ToolReadError
from app.tools.fixture_reader import FixtureReader
from app.tools.gateway import ToolGateway
from app.tools.recovery import RetryExecutor, RetryPolicy
from simulator.idempotency import FakeEffectStore

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "simulator/fixtures/week2_tools.json"


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def gateway_case(
    case_id: str,
    *,
    expected_code: str | None,
    expected_attempts: int,
    expected_stop: str,
    expected_reads: int,
    tool_name: str = "get_payment",
    arguments: dict | None = None,
    failures: tuple[str, ...] = (),
    decisions: tuple[bool, ...] = (True,),
    mutation: str | None = None,
    total_timeout_s: float = 5.0,
    late_success: bool = False,
) -> dict:
    clock = FakeClock()
    reader = FixtureReader(FIXTURE)
    record = next(
        r
        for r in reader.data["records"]
        if r["organization_id"] == "org-a" and r["payment_id"] == "pay-shared"
    )
    if mutation == "empty":
        record["payment"] = None
    elif mutation == "malformed":
        record["payment"] = {"payment_id": "pay-shared"}
    elif mutation == "empty_list":
        record["events"] = []
    counts = {"authorize": 0, "read": 0}
    budget = 0.0

    def authorize(**kwargs):
        index = counts["authorize"]
        counts["authorize"] += 1
        return decisions[min(index, len(decisions) - 1)]

    def read(**kwargs):
        index = counts["read"]
        counts["read"] += 1
        if index < len(failures):
            clock.now += budget
            raise ToolReadError(
                ToolError(
                    code=failures[index],
                    retryable=True,
                    message="Synthetic transient reader failure.",
                )
            )
        result = reader(**kwargs)
        if late_success:
            clock.now += budget + 0.1
        return result

    gateway = ToolGateway(authorize=authorize, reader=read)
    context = TrustedContext(organization_id="org-a", request_id=case_id)

    def operation(*, timeout_s):
        nonlocal budget
        budget = timeout_s
        return gateway.execute(
            tool_name=tool_name,
            arguments={"payment_id": "pay-shared"} if arguments is None else arguments,
            context=context,
        )

    result = RetryExecutor(
        policy=RetryPolicy(total_timeout_s=total_timeout_s),
        clock=clock,
        sleep=clock.sleep,
    ).run(operation)
    error = result.result.error
    code = error.code if error else None
    checks = {
        "error_code": code == expected_code,
        "attempts": len(result.attempts) == expected_attempts,
        "stop_reason": result.stop_reason == expected_stop,
        "reader_calls": counts["read"] == expected_reads,
        "retryability": (error.retryable if error else None)
        == (expected_code in {"TIMEOUT", "SERVER_ERROR"} if expected_code else None),
        "trace_codes": all(
            a.result.trace.error_code
            == (a.result.error.code if a.result.error else None)
            for a in result.attempts
        ),
        "trace_attempts": [a.result.trace.attempt for a in result.attempts]
        == list(range(1, expected_attempts + 1)),
        "authorization_per_valid_attempt": counts["authorize"]
        == (
            0
            if expected_code in {"UNKNOWN_TOOL", "INVALID_ARGUMENTS"}
            else expected_attempts
        ),
    }
    if late_success:
        checks["overrun_observed"] = (
            result.attempts[0].duration_ms > result.attempts[0].timeout_s * 1000
        )
    if mutation == "empty_list":
        checks["empty_list_success"] = result.result.data == []
    return {
        "case_id": case_id,
        "checks": checks,
        "passed": all(checks.values()),
        "counts": counts,
        "sleeps": clock.sleeps,
        "recovery": result.model_dump(mode="json"),
    }


def loop_case(*, fresh: bool) -> dict:
    case_id = "fresh_read" if fresh else "replayed_call_id"
    counts = {"authorize": 0, "read": 0}
    fixture_reader = FixtureReader(FIXTURE)

    def authorize(**kwargs):
        counts["authorize"] += 1
        return True

    def reader(**kwargs):
        counts["read"] += 1
        return fixture_reader(**kwargs)

    def turn(call_id):
        return {
            "tool_calls": [
                {
                    "call_id": call_id,
                    "name": "get_payment",
                    "arguments_json": '{"payment_id":"pay-shared"}',
                }
            ]
        }

    turns = iter(
        [
            turn("call-001"),
            turn("call-002" if fresh else "call-001"),
            {"tool_calls": [], "final_text": "Synthetic evidence collected."},
        ]
    )
    result = ToolLoop(
        model=lambda **kwargs: next(turns),
        gateway=ToolGateway(authorize=authorize, reader=reader),
    ).run(
        "Read synthetic payment evidence.",
        TrustedContext(organization_id="org-a", request_id=case_id),
    )
    checks = {
        "status": result.status == ("completed" if fresh else "repeated_call"),
        "steps": result.steps == (2 if fresh else 1),
        "reader_calls": counts["read"] == (2 if fresh else 1),
        "authorization_calls": counts["authorize"] == counts["read"],
        "repetition": [t.repetition for t in result.trace]
        == (["first_read", "fresh_read"] if fresh else ["first_read"]),
    }
    return {
        "case_id": case_id,
        "checks": checks,
        "passed": all(checks.values()),
        "counts": counts,
        "loop": result.model_dump(mode="json"),
    }


def effect_case() -> dict:
    store = FakeEffectStore()
    clock = FakeClock()
    context = TrustedContext(organization_id="org-a", request_id="effect-replay")
    calls = 0
    first_receipt = None
    payload = {"amount_minor": 100, "currency": "USD"}

    def operation(*, timeout_s):
        nonlocal calls, first_receipt
        calls += 1
        receipt = store.apply(
            organization_id=context.organization_id,
            operation_key="operation-001",
            payload=payload,
        )
        error = None
        if calls == 1:
            first_receipt = receipt
            clock.now += timeout_s
            error = ToolError(
                code="TIMEOUT",
                retryable=True,
                message="Synthetic receipt lost after commit.",
            )
        return ToolResult(
            data=None if error else receipt,
            error=error,
            trace=ToolTrace(
                organization_id=context.organization_id,
                request_id=context.request_id,
                tool_name="fake_local_effect",
                payment_id=None,
                outcome="failed" if error else "succeeded",
                error_code="TIMEOUT" if error else None,
                attempt=1,
                duration_ms=0,
            ),
        )

    result = RetryExecutor(policy=RetryPolicy(), clock=clock, sleep=clock.sleep).run(
        operation
    )
    # This trusted local operation is never exposed in the model tool registry.
    conflict = None
    try:
        store.apply(
            organization_id="org-a",
            operation_key="operation-001",
            payload={"amount_minor": 999, "currency": "USD"},
        )
    except ToolReadError as exc:
        conflict = exc.error
    checks = {
        "two_attempts": len(result.attempts) == calls == 2,
        "one_effect": store.effect_count == 1,
        "original_receipt": result.result.data == first_receipt,
        "success": result.stop_reason == "success",
        "first_timeout": result.attempts[0].result.error.code == "TIMEOUT",
        "conflict_nonretryable": conflict is not None
        and conflict.code == "IDEMPOTENCY_CONFLICT"
        and not conflict.retryable,
    }
    return {
        "case_id": "commit_then_timeout",
        "checks": checks,
        "passed": all(checks.values()),
        "effect_count": store.effect_count,
        "original_receipt": first_receipt,
        "conflict": conflict.model_dump() if conflict else None,
        "sleeps": clock.sleeps,
        "recovery": result.model_dump(mode="json"),
    }


def build_report() -> dict:
    cases = [
        gateway_case(
            "unknown_tool",
            tool_name="unknown",
            expected_code="UNKNOWN_TOOL",
            expected_attempts=1,
            expected_stop="nonretryable",
            expected_reads=0,
        ),
        gateway_case(
            "invalid_arguments",
            arguments={},
            expected_code="INVALID_ARGUMENTS",
            expected_attempts=1,
            expected_stop="nonretryable",
            expected_reads=0,
        ),
        gateway_case(
            "unauthorized",
            decisions=(False,),
            expected_code="UNAUTHORIZED",
            expected_attempts=1,
            expected_stop="nonretryable",
            expected_reads=0,
        ),
        gateway_case(
            "payment_not_found",
            arguments={"payment_id": "missing"},
            expected_code="PAYMENT_NOT_FOUND",
            expected_attempts=1,
            expected_stop="nonretryable",
            expected_reads=1,
        ),
        gateway_case(
            "invalid_provider",
            tool_name="get_provider_status",
            arguments={"payment_id": "pay-shared", "provider_id": "invalid"},
            expected_code="INVALID_PROVIDER",
            expected_attempts=1,
            expected_stop="nonretryable",
            expected_reads=1,
        ),
        gateway_case(
            "malformed_response",
            mutation="malformed",
            expected_code="MALFORMED_RESPONSE",
            expected_attempts=1,
            expected_stop="nonretryable",
            expected_reads=1,
        ),
        gateway_case(
            "empty_object",
            mutation="empty",
            expected_code="EMPTY_RESPONSE",
            expected_attempts=1,
            expected_stop="nonretryable",
            expected_reads=1,
        ),
        gateway_case(
            "empty_list_success",
            mutation="empty_list",
            tool_name="get_payment_events",
            expected_code=None,
            expected_attempts=1,
            expected_stop="success",
            expected_reads=1,
        ),
        gateway_case(
            "timeout_recovery",
            failures=("TIMEOUT",),
            expected_code=None,
            expected_attempts=2,
            expected_stop="success",
            expected_reads=2,
        ),
        gateway_case(
            "server_error_recovery",
            failures=("SERVER_ERROR",),
            expected_code=None,
            expected_attempts=2,
            expected_stop="success",
            expected_reads=2,
        ),
        gateway_case(
            "attempt_exhaustion",
            failures=("TIMEOUT",) * 3,
            expected_code="TIMEOUT",
            expected_attempts=3,
            expected_stop="max_attempts",
            expected_reads=3,
        ),
        gateway_case(
            "deadline",
            failures=("TIMEOUT",) * 3,
            total_timeout_s=1.5,
            expected_code="TIMEOUT",
            expected_attempts=2,
            expected_stop="deadline",
            expected_reads=2,
        ),
        gateway_case(
            "authorization_revoked",
            failures=("TIMEOUT",),
            decisions=(True, False),
            expected_code="UNAUTHORIZED",
            expected_attempts=2,
            expected_stop="nonretryable",
            expected_reads=1,
        ),
        gateway_case(
            "late_success",
            late_success=True,
            total_timeout_s=0.5,
            expected_code=None,
            expected_attempts=1,
            expected_stop="success",
            expected_reads=1,
        ),
        loop_case(fresh=False),
        loop_case(fresh=True),
        effect_case(),
    ]
    paths = [
        FIXTURE,
        Path(__file__),
        ROOT / "app/tools/gateway.py",
        ROOT / "app/tools/recovery.py",
        ROOT / "app/llm/tool_loop.py",
        ROOT / "app/tools/fixture_reader.py",
        ROOT / "simulator/idempotency.py",
    ]
    return {
        "mode": "offline-scripted",
        "generated_at": datetime.now(UTC).isoformat(),
        "policy": RetryPolicy().model_dump(),
        "cases": cases,
        "passed": sum(case["passed"] for case in cases),
        "total": len(cases),
        "sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths
        },
        "limitations": [
            "No provider requests; scripted cases are not model quality evidence.",
            "Fake clock controls recovery budgets; gateway and loop timings use real perf_counter.",
            "Timeouts are cooperative; effects are serial and in-memory.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error("Output exists; choose a new path")
    report = build_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "total": report["total"],
                "mode": report["mode"],
            }
        )
    )
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
