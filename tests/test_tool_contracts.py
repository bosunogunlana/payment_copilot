"""Week 2 Phase 1 acceptance contract; no fixtures or model calls.

The learner implements app.tools. Imports intentionally fail until it exists.
"""

import unittest
from unittest.mock import Mock

from pydantic import ValidationError

from app.tools.contracts import (
    TOOL_ARGUMENT_MODELS,
    ToolResult,
    ToolTrace,
    TrustedContext,
)
from app.tools.errors import ToolError
from app.tools.gateway import ToolGateway

TOOL_NAMES = (
    "get_payment",
    "get_payment_events",
    "get_ledger_entries",
    "get_provider_status",
)


def valid_arguments(tool_name):
    arguments = {"payment_id": "pay-synthetic-001"}
    if tool_name == "get_provider_status":
        arguments["provider_id"] = "simulator"
    return arguments


class ToolContractsTest(unittest.TestCase):
    def setUp(self):
        self.context = TrustedContext(
            organization_id="org-a", request_id="request-synthetic-001"
        )

    def test_registry_contains_exactly_four_tools_without_identity_arguments(self):
        self.assertEqual(set(TOOL_ARGUMENT_MODELS), set(TOOL_NAMES))
        for name, model in TOOL_ARGUMENT_MODELS.items():
            with self.subTest(tool=name):
                schema = model.model_json_schema()
                self.assertIs(schema["additionalProperties"], False)
                self.assertNotIn("organization_id", schema["properties"])
                self.assertNotIn("request_id", schema["properties"])
                required = {"payment_id"}
                if name == "get_provider_status":
                    required.add("provider_id")
                self.assertEqual(set(schema["required"]), required)
                parsed = model.model_validate(valid_arguments(name))
                self.assertEqual(parsed.payment_id, "pay-synthetic-001")

    def test_arguments_reject_missing_blank_wrong_type_and_extra_fields(self):
        for name, model in TOOL_ARGUMENT_MODELS.items():
            good = valid_arguments(name)
            invalid = [
                {},
                {**good, "payment_id": ""},
                {**good, "payment_id": "   "},
                {**good, "payment_id": 123},
                {**good, "payment_id": None},
                {**good, "organization_id": "org-b"},
                {**good, "request_id": "spoofed"},
                {**good, "extra": True},
            ]
            if name == "get_provider_status":
                invalid.extend(
                    [
                        {"payment_id": "pay-synthetic-001"},
                        {**good, "provider_id": "   "},
                        {**good, "provider_id": 123},
                    ]
                )
            for arguments in invalid:
                with self.subTest(tool=name, arguments=arguments):
                    with self.assertRaises(ValidationError):
                        model.model_validate(arguments)

    def test_trusted_context_rejects_missing_or_blank_identity(self):
        for values in (
            {},
            {"organization_id": "", "request_id": "r"},
            {"organization_id": "org-a", "request_id": " "},
        ):
            with self.subTest(values=values):
                with self.assertRaises(ValidationError):
                    TrustedContext(**values)

    def test_error_and_trace_round_trip_with_bounded_timing(self):
        error = ToolError(
            code="UNAUTHORIZED", retryable=False, message="Access denied."
        )
        trace = ToolTrace(
            request_id=self.context.request_id,
            organization_id=self.context.organization_id,
            tool_name="get_payment",
            payment_id="pay-synthetic-001",
            outcome="rejected",
            error_code=error.code,
            attempt=1,
            duration_ms=0.0,
        )
        self.assertEqual(ToolError.model_validate_json(error.model_dump_json()), error)
        self.assertEqual(ToolTrace.model_validate_json(trace.model_dump_json()), trace)
        for changes in ({"duration_ms": -1}, {"attempt": 0}, {"outcome": "oops"}):
            with self.subTest(changes=changes):
                with self.assertRaises(ValidationError):
                    ToolTrace(**{**trace.model_dump(), **changes})

    def test_result_requires_exactly_one_data_or_error(self):
        trace = ToolTrace(
            request_id="r",
            organization_id="org-a",
            tool_name="get_payment",
            payment_id=None,
            outcome="rejected",
            error_code="INVALID_ARGUMENTS",
            attempt=1,
            duration_ms=0,
        )
        error = ToolError(
            code="INVALID_ARGUMENTS", retryable=False, message="Invalid arguments."
        )
        for data, failure in ((None, None), ({}, error)):
            with self.subTest(data=data, error=failure):
                with self.assertRaises(ValidationError):
                    ToolResult(data=data, error=failure, trace=trace)
        self.assertIsNotNone(ToolResult(data=[], error=None, trace=trace).data)
        self.assertIsNotNone(ToolResult(data=None, error=error, trace=trace).error)


class ToolGatewayTest(unittest.TestCase):
    def setUp(self):
        self.context = TrustedContext(
            organization_id="org-a", request_id="request-synthetic-001"
        )
        self.authorize = Mock(return_value=True)
        self.reader = Mock(return_value={"synthetic": True})
        self.gateway = ToolGateway(authorize=self.authorize, reader=self.reader)

    def assert_rejected(self, result, code):
        self.assertIsNone(result.data)
        self.assertEqual(result.error.code, code)
        self.assertIs(result.error.retryable, False)
        self.assertEqual(result.trace.error_code, code)
        self.assertEqual(result.trace.outcome, "rejected")
        self.assertEqual(result.trace.attempt, 1)
        self.assertGreaterEqual(result.trace.duration_ms, 0)
        self.assertEqual(result.trace.organization_id, "org-a")
        self.assertEqual(result.trace.request_id, self.context.request_id)
        self.reader.assert_not_called()

    def test_unknown_tool_never_reaches_authorization_or_reader(self):
        result = self.gateway.execute(
            tool_name="refund_payment", arguments={}, context=self.context
        )
        self.assert_rejected(result, "UNKNOWN_TOOL")
        self.authorize.assert_not_called()

    def test_each_rejection_has_a_nonblank_safe_message(self):
        cases = [
            ("refund_payment", {}, True),
            ("get_payment", {}, True),
            ("get_payment", valid_arguments("get_payment"), False),
        ]
        for name, arguments, allowed in cases:
            with self.subTest(tool=name, arguments=arguments, allowed=allowed):
                self.authorize.return_value = allowed
                result = self.gateway.execute(
                    tool_name=name, arguments=arguments, context=self.context
                )
                self.assertTrue(result.error.message.strip())
                self.reader.assert_not_called()

    def test_trace_identifies_validated_payment_on_success_and_denial(self):
        for allowed in (True, False):
            for name in TOOL_NAMES:
                with self.subTest(tool=name, allowed=allowed):
                    self.authorize.return_value = allowed
                    result = self.gateway.execute(
                        tool_name=name, arguments=valid_arguments(name),
                        context=self.context,
                    )
                    self.assertEqual(result.trace.payment_id, "pay-synthetic-001")

    def test_invalid_arguments_cannot_reach_authorization_or_reader(self):
        for name in TOOL_NAMES:
            for arguments in (
                {},
                [],
                None,
                "raw text",
                {"payment_id": " "},
                {**valid_arguments(name), "organization_id": "org-b"},
            ):
                with self.subTest(tool=name, arguments=arguments):
                    self.authorize.reset_mock()
                    self.reader.reset_mock()
                    result = self.gateway.execute(
                        tool_name=name, arguments=arguments, context=self.context
                    )
                    self.assert_rejected(result, "INVALID_ARGUMENTS")
                    self.authorize.assert_not_called()

    def test_denied_access_blocks_every_tool(self):
        self.authorize.return_value = False
        for name in TOOL_NAMES:
            with self.subTest(tool=name):
                self.authorize.reset_mock()
                result = self.gateway.execute(
                    tool_name=name,
                    arguments=valid_arguments(name),
                    context=self.context,
                )
                self.assert_rejected(result, "UNAUTHORIZED")
                self.authorize.assert_called_once_with(
                    context=self.context,
                    tool_name=name,
                    payment_id="pay-synthetic-001",
                )

    def test_only_literal_true_authorizes_execution(self):
        for decision in (None, 1, "yes", {"allowed": True}):
            with self.subTest(decision=decision):
                self.authorize.return_value = decision
                result = self.gateway.execute(
                    tool_name="get_payment",
                    arguments=valid_arguments("get_payment"),
                    context=self.context,
                )
                self.assert_rejected(result, "UNAUTHORIZED")

    def test_authorization_happens_before_reader_and_uses_trusted_identity(self):
        order = []
        self.authorize.side_effect = lambda **kwargs: order.append("authorize") or True
        self.reader.side_effect = lambda **kwargs: order.append("read") or []
        for name in TOOL_NAMES:
            with self.subTest(tool=name):
                order.clear()
                self.reader.reset_mock()
                result = self.gateway.execute(
                    tool_name=name,
                    arguments=valid_arguments(name),
                    context=self.context,
                )
                self.assertEqual(order, ["authorize", "read"])
                self.assertIsNone(result.error)
                self.assertEqual(result.data, [])
                self.assertEqual(result.trace.outcome, "succeeded")
                self.assertIsNone(result.trace.error_code)
                self.reader.assert_called_once_with(
                    tool_name=name,
                    organization_id="org-a",
                    arguments=TOOL_ARGUMENT_MODELS[name].model_validate(
                        valid_arguments(name)
                    ),
                )

    def test_rejection_does_not_echo_untrusted_values_or_secrets(self):
        secret = "sk-synthetic-do-not-log"
        result = self.gateway.execute(
            tool_name="get_payment",
            arguments={"payment_id": "p", "secret": secret},
            context=self.context,
        )
        self.assert_rejected(result, "INVALID_ARGUMENTS")
        serialized = result.model_dump_json()
        self.assertNotIn(secret, serialized)
        self.assertNotIn("input_value", serialized)
        self.assertNotIn("secret", serialized)
