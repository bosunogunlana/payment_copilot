"""Week 2 Phase 2 contracts: typed evidence and tenant-scoped fixture access."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from app.models.diagnosis import Payment, PaymentEvent
from app.models.evidence import LedgerEntry, ProviderStatus
from app.tools.contracts import TOOL_ARGUMENT_MODELS, TrustedContext
from app.tools.errors import ToolError, ToolReadError
from app.tools.fixture_reader import FixtureReader
from app.tools.gateway import ToolGateway

TOOLS = tuple(TOOL_ARGUMENT_MODELS)
FIXTURE = Path(__file__).resolve().parents[1] / "simulator/fixtures/week2_tools.json"


class FixtureToolsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "fixtures.json"
        self.document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.context = TrustedContext(organization_id="org-a", request_id="r-001")

    def reader(self):
        self.path.write_text(json.dumps(self.document), encoding="utf-8")
        return FixtureReader(path=self.path)

    def arguments(self, tool, payment_id="pay-shared", provider="simulator"):
        values = {"payment_id": payment_id}
        if tool == "get_provider_status":
            values["provider_id"] = provider
        return TOOL_ARGUMENT_MODELS[tool].model_validate(values)

    def read(self, reader, tool, org="org-a", payment_id="pay-shared"):
        return reader(
            tool_name=tool,
            organization_id=org,
            arguments=self.arguments(tool, payment_id),
        )

    def read_error(self, reader, tool, org="org-a", payment_id="pay-shared"):
        with self.assertRaises(ToolReadError) as raised:
            self.read(reader, tool, org=org, payment_id=payment_id)
        return raised.exception.error

    def assert_error(self, value, code):
        self.assertIsInstance(value, ToolError)
        self.assertEqual(value.code, code)
        self.assertIs(value.retryable, False)
        self.assertTrue(value.message.strip())

    def test_all_four_tools_return_typed_deterministic_evidence(self):
        reader = self.reader()
        expected_types = {
            "get_payment": Payment,
            "get_payment_events": PaymentEvent,
            "get_ledger_entries": LedgerEntry,
            "get_provider_status": ProviderStatus,
        }
        for tool in TOOLS:
            with self.subTest(tool=tool):
                first = self.read(reader, tool)
                self.assertEqual(first, self.read(reader, tool))
                if tool in ("get_payment_events", "get_ledger_entries"):
                    self.assertIsInstance(first, list)
                    self.assertTrue(first)
                    for item in first:
                        self.assertIsInstance(item, expected_types[tool])
                else:
                    self.assertIsInstance(first, expected_types[tool])

    def test_same_id_in_two_organizations_returns_only_scoped_evidence(self):
        reader = self.reader()
        for tool in TOOLS:
            with self.subTest(tool=tool):
                a = self.read(reader, tool)
                b = self.read(reader, tool, org="org-b")
                if tool == "get_payment":
                    self.assertEqual(
                        (a.organization_id, a.amount_minor), ("org-a", 1100)
                    )
                    self.assertEqual(
                        (b.organization_id, b.amount_minor), ("org-b", 9900)
                    )
                elif tool == "get_ledger_entries":
                    self.assertEqual(a[0].organization_id, "org-a")
                    self.assertEqual(b[0].organization_id, "org-b")
                elif tool == "get_provider_status":
                    self.assertEqual(a.organization_id, "org-a")
                    self.assertEqual(b.organization_id, "org-b")
                else:
                    self.assertNotEqual(a, b)
                    expected = self.document["records"][0]["events"]
                    self.assertEqual(
                        [event.model_dump(mode="json") for event in a],
                        [
                            PaymentEvent.model_validate(e).model_dump(mode="json")
                            for e in expected
                        ],
                    )

    def test_cross_tenant_id_and_nonexistent_id_have_same_not_found_outcome(self):
        reader = self.reader()
        for tool in TOOLS:
            with self.subTest(tool=tool):
                cross = self.read_error(reader, tool, payment_id="pay-b-only")
                missing = self.read_error(reader, tool, payment_id="does-not-exist")
                self.assert_error(cross, "PAYMENT_NOT_FOUND")
                self.assertEqual(cross, missing)

    def test_gateway_preserves_typed_success_and_reader_failure(self):
        gateway = ToolGateway(authorize=Mock(return_value=True), reader=self.reader())
        for tool in TOOLS:
            for payment_id in ("pay-shared", "does-not-exist"):
                with self.subTest(tool=tool, payment_id=payment_id):
                    result = gateway.execute(
                        tool_name=tool,
                        arguments=self.arguments(tool, payment_id).model_dump(),
                        context=self.context,
                    )
                    self.assertEqual(result.trace.payment_id, payment_id)
                    if payment_id == "pay-shared":
                        self.assertIsNone(result.error)
                        self.assertEqual(result.trace.outcome, "succeeded")
                    else:
                        self.assertIsNone(result.data)
                        self.assert_error(result.error, "PAYMENT_NOT_FOUND")
                        self.assertEqual(result.trace.outcome, "failed")
                        self.assertEqual(result.trace.error_code, "PAYMENT_NOT_FOUND")
                    json.loads(result.model_dump_json())

    def test_unknown_provider_is_a_nonretryable_error(self):
        reader = self.reader()
        with self.assertRaises(ToolReadError) as raised:
            reader(
                tool_name="get_provider_status",
                organization_id="org-a",
                arguments=self.arguments(
                    "get_provider_status", provider="other-provider"
                ),
            )
        self.assert_error(raised.exception.error, "INVALID_PROVIDER")

    def test_empty_collections_are_valid_evidence(self):
        record = self.document["records"][0]
        record["events"] = []
        record["ledger_entries"] = []
        reader = self.reader()
        for tool in ("get_payment_events", "get_ledger_entries"):
            with self.subTest(tool=tool):
                self.assertEqual(self.read(reader, tool), [])

    def test_absent_single_response_is_distinct_from_not_found(self):
        for tool, field in (
            ("get_payment", "payment"),
            ("get_provider_status", "provider_status"),
        ):
            with self.subTest(tool=tool):
                original = self.document["records"][0][field]
                self.document["records"][0][field] = None
                self.assert_error(
                    self.read_error(self.reader(), tool), "EMPTY_RESPONSE"
                )
                self.document["records"][0][field] = original

    def test_malformed_tool_payload_returns_safe_error(self):
        fields = {
            "get_payment": "payment",
            "get_payment_events": "events",
            "get_ledger_entries": "ledger_entries",
            "get_provider_status": "provider_status",
        }
        secret = "synthetic-secret-never-log"
        for tool, field in fields.items():
            with self.subTest(tool=tool):
                original = self.document["records"][0][field]
                self.document["records"][0][field] = {"secret": secret}
                result = self.read_error(self.reader(), tool)
                self.assert_error(result, "MALFORMED_RESPONSE")
                self.assertNotIn(secret, result.model_dump_json())
                self.document["records"][0][field] = original

    def test_embedded_identity_mismatch_is_not_returned_as_evidence(self):
        for tool, field in (
            ("get_payment", "payment"),
            ("get_provider_status", "provider_status"),
        ):
            with self.subTest(tool=tool):
                payload = self.document["records"][0][field]
                payload["organization_id"] = "org-b"
                self.assert_error(
                    self.read_error(self.reader(), tool), "MALFORMED_RESPONSE"
                )
                payload["organization_id"] = "org-a"
        self.document["records"][0]["ledger_entries"][0]["payment_id"] = "other-payment"
        self.assert_error(
            self.read_error(self.reader(), "get_ledger_entries"), "MALFORMED_RESPONSE"
        )

    def test_gateway_catches_expected_read_failure_and_preserves_error(self):
        error = ToolError(
            code="MALFORMED_RESPONSE",
            retryable=False,
            message="Invalid evidence response.",
        )
        reader = Mock(side_effect=ToolReadError(error))
        gateway = ToolGateway(authorize=Mock(return_value=True), reader=reader)
        result = gateway.execute(
            tool_name="get_payment",
            arguments={"payment_id": "pay-shared"},
            context=self.context,
        )
        self.assertIsNone(result.data)
        self.assertEqual(result.error, error)
        self.assertEqual(result.trace.outcome, "failed")
        self.assertEqual(result.trace.error_code, error.code)
        self.assertEqual(result.trace.attempt, 1)
        self.assertEqual(result.trace.payment_id, "pay-shared")
        self.assertGreaterEqual(result.trace.duration_ms, 0)
        reader.assert_called_once()

    def test_gateway_does_not_mask_unexpected_reader_defects(self):
        defect = RuntimeError("Synthetic internal defect")
        gateway = ToolGateway(
            authorize=Mock(return_value=True), reader=Mock(side_effect=defect)
        )
        with self.assertRaises(RuntimeError) as raised:
            gateway.execute(
                tool_name="get_payment",
                arguments={"payment_id": "pay-shared"},
                context=self.context,
            )
        self.assertIs(raised.exception, defect)

    def test_read_exception_carries_safe_error_message(self):
        error = ToolError(code="PAYMENT_NOT_FOUND", message="Payment not found.")
        failure = ToolReadError(error)
        self.assertIs(failure.error, error)
        self.assertEqual(str(failure), error.message)
