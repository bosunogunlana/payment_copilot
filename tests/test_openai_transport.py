"""Offline provider contract: no credentials or network calls required."""

import copy
import io
import json
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import Mock, patch

from openai import APIError, APITimeoutError

from app.llm.diagnose import DiagnosisAdapter, DiagnosisError
from app.llm.openai_transport import OpenAITransport, create_openai_client
from app.models.diagnosis import Diagnosis, PaymentStatus
from test_diagnosis import event, payment
from test_llm_diagnose import VALID_OUTPUT


def response(*, status="completed", content=None):
    if content is None:
        content = [SimpleNamespace(type="output_text", text=json.dumps(VALID_OUTPUT))]
    return SimpleNamespace(
        status=status,
        output=[SimpleNamespace(type="message", content=content)],
    )


class OpenAITransportTest(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.client.responses.create.return_value = response()
        self.transport = OpenAITransport(
            client=self.client, model="test-model", max_output_tokens=512
        )
        self.schema = Diagnosis.model_json_schema()
        self.request = {
            "system_instruction": "Use only supplied synthetic evidence.",
            "input_json": '{"payment_id":"pay_test"}',
            "output_schema": self.schema,
        }

    def test_request_uses_strict_schema_and_keeps_instructions_separate(self):
        original = copy.deepcopy(self.schema)
        result = self.transport(self.request)
        self.client.responses.create.assert_called_once()
        kwargs = self.client.responses.create.call_args.kwargs
        self.assertEqual(kwargs["model"], "test-model")
        self.assertEqual(kwargs["instructions"], self.request["system_instruction"])
        self.assertEqual(kwargs["input"], self.request["input_json"])
        self.assertEqual(kwargs["max_output_tokens"], 512)
        self.assertIs(kwargs["store"], False)
        fmt = kwargs["text"]["format"]
        self.assertEqual(fmt["type"], "json_schema")
        self.assertIs(fmt["strict"], True)
        self.assertTrue(fmt["name"])
        schema = fmt["schema"]
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(set(schema["required"]), set(schema["properties"]))
        cause = schema["properties"]["likely_cause"]
        self.assertNotIn("default", cause)
        self.assertIn({"type": "null"}, cause["anyOf"])
        self.assertEqual(self.schema, original, "Do not mutate the application schema")
        self.assertEqual(result["status"], "completed")
        self.assertIsNone(result["refusal"])
        self.assertEqual(json.loads(result["output_json"]), VALID_OUTPUT)

    def test_refusal_is_extracted_even_when_text_is_present(self):
        self.client.responses.create.return_value = response(content=[
            SimpleNamespace(type="output_text", text=json.dumps(VALID_OUTPUT)),
            SimpleNamespace(type="refusal", refusal="Cannot diagnose."),
        ])
        result = self.transport(self.request)
        self.assertEqual(result["refusal"], "Cannot diagnose.")
        self.assertIsNone(result["output_json"])

    def test_incomplete_response_discards_partial_text(self):
        self.client.responses.create.return_value = response(status="incomplete")
        result = self.transport(self.request)
        self.assertEqual(result["status"], "incomplete")
        self.assertIsNone(result["output_json"])

    def test_empty_completed_output_remains_malformed_to_adapter(self):
        self.client.responses.create.return_value = response(content=[])
        adapter = DiagnosisAdapter(transport=self.transport)
        result = adapter.diagnose(payment(PaymentStatus.PENDING, []))
        self.assertEqual(result.error, DiagnosisError.MALFORMED_OUTPUT)

    def test_sdk_errors_reach_adapter_as_api_failures_without_retry(self):
        for error in (
            APIError("provider failure", request=Mock(), body=None),
            APITimeoutError(request=Mock()),
        ):
            with self.subTest(error=type(error).__name__):
                self.client.reset_mock()
                self.client.responses.create.side_effect = error
                adapter = DiagnosisAdapter(transport=self.transport)
                result = adapter.diagnose(payment(PaymentStatus.PENDING, []))
                self.assertEqual(result.error, DiagnosisError.API_FAILURE)
                self.client.responses.create.assert_called_once()

    def test_transport_composes_with_existing_adapter(self):
        result = DiagnosisAdapter(transport=self.transport).diagnose(
            payment(PaymentStatus.PENDING, [event("evt_timeout", "provider.timeout")])
        )
        self.assertIsNone(result.error)
        self.assertEqual(result.diagnosis, Diagnosis.model_validate(VALID_OUTPUT))

    def test_client_factory_disables_retries_and_sets_timeout(self):
        with patch("app.llm.openai_transport.OpenAI") as constructor:
            create_openai_client(api_key="synthetic-test-key")
        constructor.assert_called_once_with(
            api_key="synthetic-test-key", timeout=20.0, max_retries=0
        )

    def test_invalid_output_limit_is_rejected(self):
        for limit in (0, -1):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                OpenAITransport(client=self.client, model="test-model", max_output_tokens=limit)

    def test_api_failure_does_not_write_provider_details_to_stdout(self):
        self.client.responses.create.side_effect = APIError(
            "synthetic provider diagnostic", request=Mock(), body=None
        )
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            result = DiagnosisAdapter(transport=self.transport).diagnose(
                payment(PaymentStatus.PENDING, [])
            )
        self.assertEqual(result.error, DiagnosisError.API_FAILURE)
        self.assertEqual(stdout.getvalue(), "")
