"""Phase 4: deterministic recovery; no wall-clock sleeps or external effects."""

import unittest
from copy import deepcopy
from unittest.mock import Mock

from app.tools.contracts import ToolResult, ToolTrace, TrustedContext
from app.tools.errors import ToolError, ToolReadError
from app.tools.gateway import ToolGateway
from app.tools.recovery import RetryExecutor, RetryPolicy
from simulator.idempotency import FakeEffectStore


class FakeClock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        assert seconds >= 0
        self.sleeps.append(seconds)
        self.now += seconds


def outcome(error=None, data=None):
    return ToolResult(
        data={"synthetic": True} if error is None and data is None else data,
        error=error,
        trace=ToolTrace(
            organization_id="org-a",
            request_id="recovery-001",
            tool_name="get_payment",
            payment_id="pay-shared",
            outcome="succeeded" if error is None else "failed",
            error_code=error.code if error else None,
            attempt=1,
            duration_ms=0,
        ),
    )


def failure(code="TIMEOUT", retryable=True):
    return outcome(
        ToolError(code=code, retryable=retryable, message="Synthetic evidence failure.")
    )


class ToolRecoveryTest(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()

    def executor(self, **changes):
        values = dict(
            max_attempts=3,
            attempt_timeout_s=1.0,
            total_timeout_s=5.0,
            initial_backoff_s=0.25,
            max_backoff_s=0.5,
        )
        values.update(changes)
        return RetryExecutor(
            policy=RetryPolicy(**values), clock=self.clock, sleep=self.clock.sleep
        )

    def test_success_has_one_attempt_and_no_sleep(self):
        operation = Mock(return_value=outcome())
        report = self.executor().run(operation=operation)
        self.assertEqual(report.stop_reason, "success")
        self.assertIsNone(report.result.error)
        self.assertEqual(len(report.attempts), 1)
        operation.assert_called_once_with(timeout_s=1.0)
        self.assertEqual(self.clock.sleeps, [])

    def test_timeout_and_server_error_recover_with_observable_backoff(self):
        operation = Mock(side_effect=[failure(), failure("SERVER_ERROR"), outcome()])
        report = self.executor().run(operation=operation)
        self.assertEqual(report.stop_reason, "success")
        self.assertEqual([a.attempt for a in report.attempts], [1, 2, 3])
        self.assertEqual([a.backoff_s for a in report.attempts], [0.25, 0.5, 0])
        self.assertEqual(self.clock.sleeps, [0.25, 0.5])
        self.assertEqual(report.attempts[0].result.error.code, "TIMEOUT")
        self.assertEqual(report.attempts[1].result.error.code, "SERVER_ERROR")
        self.assertEqual(report.result.trace.attempt, 3)
        for attempt in report.attempts:
            self.assertGreaterEqual(attempt.duration_ms, 0)
            self.assertGreater(attempt.timeout_s, 0)
        report.model_dump_json()

    def test_attempt_limit_preserves_last_failure_without_final_sleep(self):
        operation = Mock(side_effect=[failure()] * 3)
        report = self.executor().run(operation=operation)
        self.assertEqual(report.stop_reason, "max_attempts")
        self.assertEqual(operation.call_count, 3)
        self.assertEqual(report.result.error.code, "TIMEOUT")
        self.assertEqual(self.clock.sleeps, [0.25, 0.5])
        self.assertEqual(report.attempts[-1].backoff_s, 0)

    def test_nonretryable_errors_never_retry(self):
        for code in (
            "INVALID_ARGUMENTS",
            "UNAUTHORIZED",
            "PAYMENT_NOT_FOUND",
            "MALFORMED_RESPONSE",
            "INVALID_PROVIDER",
            "UNKNOWN_TOOL",
        ):
            with self.subTest(code=code):
                operation = Mock(return_value=failure(code, retryable=False))
                report = self.executor().run(operation=operation)
                self.assertEqual(report.stop_reason, "nonretryable")
                operation.assert_called_once()
                self.assertEqual(self.clock.sleeps, [])

    def test_retryable_code_also_requires_true_retryable_flag(self):
        operation = Mock(return_value=failure("TIMEOUT", retryable=False))
        report = self.executor().run(operation=operation)
        self.assertEqual(report.stop_reason, "nonretryable")
        operation.assert_called_once()

    def test_deadline_shrinks_attempt_budget_and_prevents_another_attempt(self):
        budgets = []

        def operation(*, timeout_s):
            budgets.append(timeout_s)
            self.clock.now += timeout_s
            return failure()

        report = self.executor(total_timeout_s=1.5).run(operation=operation)
        self.assertEqual(report.stop_reason, "deadline")
        self.assertEqual(budgets, [1.0, 0.25])
        self.assertEqual(self.clock.sleeps, [0.25])
        self.assertAlmostEqual(self.clock.now, 1.5)
        self.assertEqual(report.result.error.code, "TIMEOUT")

    def test_backoff_that_cannot_leave_attempt_time_stops_without_sleep(self):
        def operation(*, timeout_s):
            self.clock.now += 0.9
            return failure()

        report = self.executor(total_timeout_s=1.0).run(operation=operation)
        self.assertEqual(report.stop_reason, "deadline")
        self.assertEqual(len(report.attempts), 1)
        self.assertEqual(self.clock.sleeps, [])

    def test_backoff_is_exponential_and_capped(self):
        operation = Mock(return_value=failure())
        self.executor(max_attempts=5).run(operation=operation)
        self.assertEqual(self.clock.sleeps, [0.25, 0.5, 0.5, 0.5])

    def test_late_success_is_preserved_without_retry_even_after_total_deadline(self):
        for total_timeout in (5.0, 0.5):
            with self.subTest(total_timeout=total_timeout):
                self.clock = FakeClock()
                successful_result = outcome()

                def complete_late(*, timeout_s):
                    self.clock.now += timeout_s + 0.1
                    return successful_result

                operation = Mock(side_effect=complete_late)
                report = self.executor(total_timeout_s=total_timeout).run(
                    operation=operation
                )
                self.assertEqual(report.stop_reason, "success")
                self.assertEqual(report.result.data, successful_result.data)
                self.assertIsNone(report.result.error)
                self.assertEqual(report.result.trace.outcome, "succeeded")
                self.assertEqual(len(report.attempts), 1)
                self.assertGreater(
                    report.attempts[0].duration_ms, report.attempts[0].timeout_s * 1000
                )
                self.assertEqual(report.attempts[0].backoff_s, 0)
                self.assertEqual(self.clock.sleeps, [])
                operation.assert_called_once()

    def test_unexpected_defect_propagates_without_retry(self):
        operation = Mock(side_effect=RuntimeError("Synthetic internal defect"))
        with self.assertRaises(RuntimeError):
            self.executor().run(operation=operation)
        operation.assert_called_once()

    def test_recovery_state_resets_for_each_run(self):
        executor = self.executor()
        for _ in range(2):
            report = executor.run(operation=Mock(return_value=outcome()))
            self.assertEqual([a.attempt for a in report.attempts], [1])

    def test_every_retry_runs_gateway_authorization_again(self):
        context = TrustedContext(organization_id="org-a", request_id="r")
        reader = Mock(
            side_effect=[
                ToolReadError(
                    ToolError(
                        code="TIMEOUT", retryable=True, message="Synthetic timeout."
                    )
                ),
                {"synthetic": True},
            ]
        )
        authorize = Mock(return_value=True)
        gateway = ToolGateway(authorize=authorize, reader=reader)

        def operation(*, timeout_s):
            # Real adapters must apply this budget to their underlying I/O.
            return gateway.execute(
                tool_name="get_payment",
                arguments={"payment_id": "pay-shared"},
                context=context,
            )

        report = self.executor().run(operation=operation)
        self.assertEqual(report.stop_reason, "success")
        self.assertEqual(authorize.call_count, 2)
        self.assertEqual(reader.call_count, 2)

    def test_revoked_authorization_stops_recovery_before_another_read(self):
        context = TrustedContext(organization_id="org-a", request_id="r")
        reader = Mock(
            side_effect=ToolReadError(
                ToolError(code="TIMEOUT", retryable=True, message="Synthetic timeout.")
            )
        )
        gateway = ToolGateway(authorize=Mock(side_effect=[True, False]), reader=reader)

        def operation(*, timeout_s):
            return gateway.execute(
                tool_name="get_payment",
                arguments={"payment_id": "pay-shared"},
                context=context,
            )

        report = self.executor().run(operation=operation)
        self.assertEqual(report.stop_reason, "nonretryable")
        self.assertEqual(report.result.error.code, "UNAUTHORIZED")
        reader.assert_called_once()

    def test_invalid_policy_is_rejected(self):
        cases = [{"max_attempts": v} for v in (0, -1, True, 1.5)]
        for field in ("attempt_timeout_s", "total_timeout_s"):
            cases.extend({field: v} for v in (0, -1, float("inf"), float("nan"), True))
        for field in ("initial_backoff_s", "max_backoff_s"):
            cases.extend({field: v} for v in (-1, float("inf"), float("nan"), True))
        for changes in cases:
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    self.executor(**changes)


class FakeEffectReplayTest(unittest.TestCase):
    def setUp(self):
        self.store = FakeEffectStore()
        self.payload = {"amount_minor": 100, "currency": "USD"}

    def apply(self, org="org-a", key="operation-001", payload=None):
        return self.store.apply(
            organization_id=org,
            operation_key=key,
            payload=self.payload if payload is None else payload,
        )

    def test_commit_then_timeout_retries_same_operation_without_duplicate_effect(self):
        clock = FakeClock()
        calls = []
        receipt = None

        def operation(*, timeout_s):
            nonlocal receipt
            calls.append(("org-a", "operation-001"))
            receipt = self.apply()
            if len(calls) == 1:
                clock.now += timeout_s
                return failure()
            return outcome(data=receipt)

        executor = RetryExecutor(policy=RetryPolicy(), clock=clock, sleep=clock.sleep)
        report = executor.run(operation=operation)
        self.assertEqual(report.stop_reason, "success")
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], calls[1])
        self.assertEqual(self.store.effect_count, 1)
        self.assertEqual(report.result.data, receipt)
        self.assertEqual(self.apply(), receipt)
        self.assertEqual(self.store.effect_count, 1)

    def test_same_key_with_changed_payload_is_a_nonretryable_conflict(self):
        self.apply()
        with self.assertRaises(ToolReadError) as raised:
            self.apply(payload={"amount_minor": 999, "currency": "USD"})
        self.assertEqual(raised.exception.error.code, "IDEMPOTENCY_CONFLICT")
        self.assertIs(raised.exception.error.retryable, False)
        self.assertEqual(self.store.effect_count, 1)

    def test_operation_keys_are_scoped_by_organization(self):
        self.apply()
        self.apply(org="org-b")
        self.assertEqual(self.store.effect_count, 2)

    def test_mutable_inputs_and_receipts_cannot_corrupt_deduplication(self):
        original_payload = deepcopy(self.payload)
        receipt = self.apply()
        expected_receipt = deepcopy(receipt)
        self.payload["amount_minor"] = 999
        receipt["tampered"] = True
        self.assertEqual(self.apply(payload=original_payload), expected_receipt)
        self.assertEqual(self.store.effect_count, 1)


class GatewayRetryClassificationTest(unittest.TestCase):
    def test_gateway_classifies_reader_errors_without_mutating_original(self):
        codes = (
            "TIMEOUT",
            "SERVER_ERROR",
            "INVALID_ARGUMENTS",
            "UNAUTHORIZED",
            "PAYMENT_NOT_FOUND",
            "MALFORMED_RESPONSE",
            "INVALID_PROVIDER",
            "UNKNOWN_TOOL",
            "EMPTY_RESPONSE",
            "IDEMPOTENCY_CONFLICT",
            "UNRECOGNIZED_ERROR",
        )
        context = TrustedContext(organization_id="org-a", request_id="classification")
        for code in codes:
            for requested_retryable in (True, False):
                with self.subTest(code=code, retryable=requested_retryable):
                    original = ToolError(
                        code=code,
                        retryable=requested_retryable,
                        message="Synthetic reader failure.",
                    )
                    reader = Mock(side_effect=ToolReadError(original))
                    gateway = ToolGateway(
                        authorize=Mock(return_value=True), reader=reader
                    )
                    result = gateway.execute(
                        tool_name="get_payment",
                        arguments={"payment_id": "pay-shared"},
                        context=context,
                    )
                    self.assertIs(
                        result.error.retryable,
                        requested_retryable and code in {"TIMEOUT", "SERVER_ERROR"},
                    )
                    self.assertEqual(result.error.code, code)
                    self.assertEqual(result.error.message, original.message)
                    self.assertEqual(result.trace.error_code, code)
                    self.assertEqual(result.trace.outcome, "failed")
                    self.assertIs(original.retryable, requested_retryable)
                    reader.assert_called_once()
