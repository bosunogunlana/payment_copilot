"""Offline acceptance contract; learner implements app.llm.diagnose.

Transport is callable(request: dict) -> dict. Response envelope:
{status: completed|incomplete, refusal: str|None, output_json: str|None}.
Adapter failures return DiagnosisResult, never a fabricated Diagnosis.
"""

import json
import unittest
from unittest.mock import Mock

from pydantic import ValidationError

from app.llm.diagnose import DiagnosisAdapter, DiagnosisError, DiagnosisResult
from app.models.diagnosis import Diagnosis, PaymentStatus
from test_diagnosis import event, payment

VALID_OUTPUT = {
    "status": "pending",
    "category": "provider_timeout",
    "recommended_action": "wait_and_reconcile",
    "likely_cause": "The provider did not return a terminal result.",
    "confidence": 0.7,
}


def completed(output=VALID_OUTPUT):
    return {
        "status": "completed",
        "refusal": None,
        "output_json": json.dumps(output),
    }


class DiagnosisAdapterTest(unittest.TestCase):
    def setUp(self):
        self.payment = payment(
            PaymentStatus.PENDING, [event("evt_timeout", "provider.timeout")]
        )

    def run_adapter(self, response):
        transport = Mock(return_value=response)
        result = DiagnosisAdapter(transport=transport).diagnose(self.payment)
        self.assertIsInstance(result, DiagnosisResult)
        transport.assert_called_once()
        return result

    def assert_failure(self, result, error):
        self.assertIsNone(result.diagnosis)
        self.assertEqual(result.error, error)

    def test_success_validates_application_model_and_requests_schema(self):
        transport = Mock(return_value=completed())
        result = DiagnosisAdapter(transport=transport).diagnose(self.payment)
        self.assertIsInstance(result, DiagnosisResult)
        self.assertEqual(result.diagnosis, Diagnosis.model_validate(VALID_OUTPUT))
        self.assertIsNone(result.error)
        transport.assert_called_once()
        request = transport.call_args.args[0]
        self.assertEqual(json.loads(request["input_json"]), self.payment.model_dump(mode="json"))
        self.assertEqual(request["output_schema"], Diagnosis.model_json_schema())
        self.assertTrue(request["system_instruction"].strip())
        self.assertEqual(self.payment.events[0].event_id, "evt_timeout")

    def test_refusal_takes_precedence_over_valid_looking_output(self):
        response = {**completed(), "refusal": "Cannot diagnose this input."}
        self.assert_failure(self.run_adapter(response), DiagnosisError.REFUSAL)

    def test_incomplete_takes_precedence_over_valid_looking_output(self):
        response = {**completed(), "status": "incomplete"}
        self.assert_failure(self.run_adapter(response), DiagnosisError.INCOMPLETE)

    def test_malformed_envelopes_json_and_schema_are_explicit_failures(self):
        responses = [
            None,
            [],
            "unexpected response",
            42,
            {},
            {**completed(), "status": "unexpected"},
            {**completed(), "output_json": None},
            {**completed(), "output_json": "not json"},
            completed([]),
            completed({**VALID_OUTPUT, "confidence": 1.1}),
            completed({**VALID_OUTPUT, "category": "invented"}),
        ]
        for response in responses:
            with self.subTest(response=response):
                self.assert_failure(self.run_adapter(response), DiagnosisError.MALFORMED_OUTPUT)

    def test_transport_failures_are_explicit_and_not_retried(self):
        for exception in (TimeoutError("timeout"), ConnectionError("unavailable")):
            with self.subTest(exception=type(exception).__name__):
                transport = Mock(side_effect=exception)
                result = DiagnosisAdapter(transport=transport).diagnose(self.payment)
                self.assert_failure(result, DiagnosisError.API_FAILURE)
                transport.assert_called_once()

    def test_event_limit_rejects_without_silently_dropping_evidence(self):
        transport = Mock(return_value=completed())
        adapter = DiagnosisAdapter(transport=transport, max_events=2)
        self.payment.events = [event(f"evt_{i}", "payment.created") for i in range(3)]
        self.assert_failure(adapter.diagnose(self.payment), DiagnosisError.INPUT_TOO_LARGE)
        transport.assert_not_called()
        self.assertEqual(len(self.payment.events), 3)

    def test_payload_limit_counts_utf8_bytes_and_allows_exact_boundary(self):
        self.payment.events[0].message = "é" * 50
        transport = Mock(return_value=completed())
        result = DiagnosisAdapter(transport=transport).diagnose(self.payment)
        self.assertIsNone(result.error)
        payload = transport.call_args.args[0]["input_json"]
        size = len(payload.encode("utf-8"))
        transport.reset_mock()
        exact = DiagnosisAdapter(transport=transport, max_payload_bytes=size)
        self.assertIsNone(exact.diagnose(self.payment).error)
        transport.reset_mock()
        too_small = DiagnosisAdapter(transport=transport, max_payload_bytes=size - 1)
        self.assert_failure(too_small.diagnose(self.payment), DiagnosisError.INPUT_TOO_LARGE)
        transport.assert_not_called()

    def test_valid_unknown_is_a_diagnosis_not_a_transport_error(self):
        unknown = {
            "status": "unknown",
            "category": "unknown",
            "recommended_action": "escalate_to_human",
            "likely_cause": None,
            "confidence": 0.2,
        }
        result = self.run_adapter(completed(unknown))
        self.assertEqual(result.diagnosis, Diagnosis.model_validate(unknown))
        self.assertIsNone(result.error)

    def test_result_requires_exactly_one_diagnosis_or_error(self):
        for values in (
            {"diagnosis": None, "error": None},
            {
                "diagnosis": Diagnosis.model_validate(VALID_OUTPUT),
                "error": DiagnosisError.API_FAILURE,
            },
        ):
            with self.subTest(values=values):
                with self.assertRaises(ValidationError):
                    DiagnosisResult(**values)

    def test_malformed_output_error_serializes_with_correct_name(self):
        result = self.run_adapter({})
        self.assertEqual(result.model_dump(mode="json")["error"], "malformed_output")

    def test_invalid_limits_are_rejected_before_transport_use(self):
        transport = Mock()
        for limits in (
            {"max_events": -1},
            {"max_payload_bytes": 0},
            {"max_payload_bytes": -1},
        ):
            with self.subTest(limits=limits):
                with self.assertRaises(ValueError):
                    DiagnosisAdapter(transport=transport, **limits)
        transport.assert_not_called()
