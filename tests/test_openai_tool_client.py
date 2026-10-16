"""Mocked-SDK acceptance for the learner-owned tool provider wrapper."""

import unittest
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import Mock

from openai import APIError, APITimeoutError

from app.clients.openai_tool_client import OpenAIToolClient
from app.llm.tool_model import ToolModel


def call(*, call_id="call-001", name="get_payment", arguments="{broken"):
    return SimpleNamespace(
        type="function_call",
        id="fc-distinct-item-id",
        call_id=call_id,
        name=name,
        arguments=arguments,
    )


def response(*, status="completed", output=None, usage=True):
    return SimpleNamespace(
        status=status,
        output=[call()] if output is None else output,
        usage=SimpleNamespace(input_tokens=12, output_tokens=8) if usage else None,
    )


class OpenAIToolClientTest(unittest.TestCase):
    def setUp(self):
        self.sdk = Mock()
        self.sdk.responses.create.return_value = response()
        self.client = OpenAIToolClient(client=self.sdk)
        self.payload = {
            "model": "synthetic-model",
            "instructions": "Read payment evidence.",
            "timeout_s": 2.0,
            "max_output_tokens": 512,
            "messages": [{"role": "user", "content": "Fetch pay-shared"}],
            "tools": [
                {
                    "name": "get_payment",
                    "description": "Read payment record.",
                    "parameters": {
                        "type": "object",
                        "properties": {"payment_id": {"type": "string"}},
                        "required": ["payment_id"],
                        "additionalProperties": False,
                    },
                }
            ],
        }

    def test_translates_request_and_makes_exactly_one_sdk_call(self):
        self.client.request(payload=self.payload)
        self.sdk.responses.create.assert_called_once_with(
            model="synthetic-model",
            instructions="Read payment evidence.",
            input=self.payload["messages"],
            tools=[{"type": "function", **self.payload["tools"][0], "strict": False}],
            timeout=2.0,
            max_output_tokens=512,
            store=False,
        )

    def test_extracts_call_id_not_item_id_and_preserves_argument_json(self):
        result = self.client.request(payload=self.payload)
        self.assertEqual(
            result,
            {
                "status": "completed",
                "tool_calls": [
                    {"id": "call-001", "name": "get_payment", "arguments": "{broken"}
                ],
                "output_text": None,
                "refusal": None,
                "usage": {"input_tokens": 12, "output_tokens": 8},
            },
        )

    def test_extracts_multiple_calls_in_order(self):
        self.sdk.responses.create.return_value = response(
            output=[
                call(),
                call(call_id="call-002", name="get_payment_events", arguments="{}"),
            ]
        )
        result = self.client.request(payload=self.payload)
        self.assertEqual(
            [c["id"] for c in result["tool_calls"]], ["call-001", "call-002"]
        )

    def test_translates_call_and_correlated_result_messages(self):
        self.payload["messages"] += [
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "call_id": "call-001",
                        "name": "get_payment",
                        "arguments_json": "{}",
                    }
                ],
            },
            {"role": "tool", "call_id": "call-001", "content": '{"data":{}}'},
        ]
        self.client.request(payload=self.payload)
        inputs = self.sdk.responses.create.call_args.kwargs["input"]
        self.assertEqual(
            inputs,
            [
                self.payload["messages"][0],
                {
                    "type": "function_call",
                    "call_id": "call-001",
                    "name": "get_payment",
                    "arguments": "{}",
                },
                {
                    "type": "function_call_output",
                    "call_id": "call-001",
                    "output": '{"data":{}}',
                },
            ],
        )

    def test_extracts_output_text_and_handles_missing_usage(self):
        self.sdk.responses.create.return_value = response(
            usage=False,
            output=[
                SimpleNamespace(
                    type="message",
                    content=[
                        SimpleNamespace(type="output_text", text="Payment "),
                        SimpleNamespace(type="output_text", text="evidence."),
                    ],
                ),
            ],
        )
        result = self.client.request(payload=self.payload)
        self.assertEqual(result["output_text"], "Payment evidence.")
        self.assertEqual(result["tool_calls"], [])
        self.assertIsNone(result["usage"])

    def test_refusal_discards_calls_and_text_regardless_of_output_order(self):
        refusal = SimpleNamespace(
            type="message",
            content=[
                SimpleNamespace(type="output_text", text="Discard this"),
                SimpleNamespace(type="refusal", refusal="Cannot comply"),
            ],
        )
        for output in ([call(), refusal], [refusal, call()]):
            with self.subTest(output=output):
                self.sdk.responses.create.return_value = response(output=output)
                result = self.client.request(payload=self.payload)
                self.assertEqual(result["refusal"], "Cannot comply")
                self.assertEqual(result["tool_calls"], [])
                self.assertIsNone(result["output_text"])

    def test_noncompleted_responses_discard_partial_calls_and_text(self):
        for status in ("incomplete", "failed"):
            with self.subTest(status=status):
                self.sdk.responses.create.return_value = response(status=status)
                result = self.client.request(payload=self.payload)
                self.assertEqual(result["status"], status)
                self.assertEqual(result["tool_calls"], [])
                self.assertIsNone(result["output_text"])

    def test_expected_sdk_errors_translate_without_retry(self):
        request = Mock()
        for error, expected in (
            (APITimeoutError(request=request), TimeoutError),
            (APIError("Synthetic failure", request, body=None), ConnectionError),
        ):
            with self.subTest(error=error):
                self.sdk.responses.create.reset_mock()
                self.sdk.responses.create.side_effect = error
                with self.assertRaises(expected) as raised:
                    self.client.request(payload=self.payload)
                self.assertIs(raised.exception.__cause__, error)
                self.sdk.responses.create.assert_called_once()

    def test_unexpected_sdk_defect_propagates(self):
        self.sdk.responses.create.side_effect = RuntimeError("Synthetic defect")
        with self.assertRaisesRegex(RuntimeError, "Synthetic defect"):
            self.client.request(payload=self.payload)

    def test_payload_and_provider_response_are_not_mutated(self):
        before = deepcopy(self.payload)
        raw = self.sdk.responses.create.return_value
        original_arguments = raw.output[0].arguments
        self.client.request(payload=self.payload)
        self.assertEqual(self.payload, before)
        self.assertEqual(raw.output[0].arguments, original_arguments)

    def test_composes_with_tool_model_without_network_or_tool_execution(self):
        observations = []
        model = ToolModel(
            client=self.client,
            model="synthetic-model",
            instructions="Read payment evidence.",
            request_timeout_s=2.0,
            max_output_tokens=512,
            observe=observations.append,
        )
        turn = model(messages=self.payload["messages"], tools=self.payload["tools"])
        self.assertEqual(
            turn,
            {
                "tool_calls": [
                    {
                        "call_id": "call-001",
                        "name": "get_payment",
                        "arguments_json": "{broken",
                    }
                ]
            },
        )
        self.assertEqual(len(observations), 1)
        self.sdk.responses.create.assert_called_once()
