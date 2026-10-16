"""Learner-owned ToolModel acceptance using a synthetic provider contract.

No SDK or network dependency. See WEEK-02-EVALUATION-CONTRACT.md for the
request/response seam. Tests intentionally fail while ToolModel is a Protocol.
"""

import json
import unittest
from copy import deepcopy
from unittest.mock import Mock

from app.llm.tool_model import ToolModel
from app.tools.contracts import TOOL_ARGUMENT_MODELS


def response(*, calls=None, text=None, status="completed", refusal=None):
    return {
        "status": status,
        "tool_calls": [] if calls is None else calls,
        "output_text": text,
        "refusal": refusal,
        "usage": {"input_tokens": 12, "output_tokens": 8},
    }


def provider_call(*, call_id="call-001", name="get_payment", arguments=None):
    return {
        "id": call_id,
        "name": name,
        "arguments": '{"payment_id":"pay-shared"}' if arguments is None else arguments,
    }


class ToolModelTest(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.client.request.return_value = response(calls=[provider_call()])
        self.observations = []
        self.messages = [{"role": "user", "content": "Fetch payment pay-shared"}]
        self.tools = [
            {"name": name, "parameters": model.model_json_schema()}
            for name, model in TOOL_ARGUMENT_MODELS.items()
        ]

    def adapter(self):
        return ToolModel(
            client=self.client,
            model="synthetic-model",
            instructions="Use the supplied read-only tools for payment evidence.",
            request_timeout_s=2.0,
            max_output_tokens=512,
            observe=self.observations.append,
        )

    def invoke(self):
        return self.adapter()(messages=self.messages, tools=self.tools)

    def test_makes_one_request_with_application_configuration(self):
        self.invoke()
        self.client.request.assert_called_once()
        payload = self.client.request.call_args.kwargs["payload"]
        self.assertEqual(payload["model"], "synthetic-model")
        self.assertEqual(payload["instructions"],
                         "Use the supplied read-only tools for payment evidence.")
        self.assertEqual(payload["timeout_s"], 2.0)
        self.assertEqual(payload["max_output_tokens"], 512)
        self.assertEqual(payload["messages"][0], self.messages[0])
        self.assertEqual({t["name"] for t in payload["tools"]}, set(TOOL_ARGUMENT_MODELS))
        for tool in payload["tools"]:
            self.assertTrue(tool["description"].strip())
            self.assertEqual(tool["parameters"], TOOL_ARGUMENT_MODELS[
                tool["name"]
            ].model_json_schema())

    def test_normalizes_multiple_tool_calls_preserving_order_and_arguments(self):
        calls = [provider_call(), provider_call(
            call_id="call-002", name="get_payment_events",
            arguments=' { "payment_id" : "pay-shared" } ',
        )]
        self.client.request.return_value = response(calls=calls)
        self.assertEqual(self.invoke(), {"tool_calls": [
            {"call_id": c["id"], "name": c["name"], "arguments_json": c["arguments"]}
            for c in calls
        ]})

    def test_normalizes_text_only_completion(self):
        self.client.request.return_value = response(text="Payment evidence is available.")
        self.assertEqual(self.invoke(), {
            "tool_calls": [], "final_text": "Payment evidence is available.",
        })

    def test_preserves_malformed_argument_json_for_gateway_validation(self):
        self.client.request.return_value = response(calls=[provider_call(arguments="{broken")])
        turn = self.invoke()
        self.assertEqual(turn["tool_calls"][0]["arguments_json"], "{broken")

    def test_preserves_unknown_tool_name_for_gateway_rejection(self):
        self.client.request.return_value = response(calls=[provider_call(name="unknown_tool")])
        self.assertEqual(self.invoke()["tool_calls"][0]["name"], "unknown_tool")

    def test_refusal_and_incomplete_responses_discard_calls_and_text(self):
        for changes in ({"refusal": "Cannot comply"}, {"status": "incomplete"}):
            with self.subTest(changes=changes):
                self.client.request.return_value = response(
                    calls=[provider_call()], text="Partial answer", **changes
                )
                self.assertIsNone(self.invoke())

    def test_invalid_or_empty_response_never_becomes_an_executable_turn(self):
        for raw in (None, {}, response(), response(text="   "),
                    response(calls=[{"name": "get_payment"}])):
            with self.subTest(response=raw):
                self.client.request.return_value = raw
                self.assertIsNone(self.invoke())

    def test_tool_result_remains_correlated_with_requested_call(self):
        content = json.dumps({"data": {"synthetic": True}, "error": None})
        self.messages.extend([
            {"role": "assistant", "tool_calls": [{
                "call_id": "call-001", "name": "get_payment",
                "arguments_json": '{"payment_id":"pay-shared"}',
            }]},
            {"role": "tool", "call_id": "call-001", "content": content},
        ])
        self.invoke()
        messages = self.client.request.call_args.kwargs["payload"]["messages"]
        self.assertEqual(messages[1]["tool_calls"][0]["call_id"], "call-001")
        self.assertEqual(messages[2]["call_id"], "call-001")
        self.assertEqual(messages[2]["content"], content)

    def test_does_not_mutate_input_messages_schemas_or_response(self):
        before = deepcopy((self.messages, self.tools, self.client.request.return_value))
        self.invoke()
        self.assertEqual((self.messages, self.tools, self.client.request.return_value), before)

    def test_observes_usage_latency_and_outcome_outside_model_turn(self):
        turn = self.invoke()
        self.assertEqual(len(self.observations), 1)
        metadata = self.observations[0]
        self.assertEqual(metadata["status"], "completed")
        self.assertEqual(metadata["usage"], {"input_tokens": 12, "output_tokens": 8})
        self.assertGreaterEqual(metadata["duration_ms"], 0)
        self.assertNotIn("usage", turn)
        self.assertNotIn("duration_ms", turn)

    def test_expected_transport_failure_is_observed_without_retry(self):
        for error in (TimeoutError("Synthetic timeout"), ConnectionError("Synthetic failure")):
            with self.subTest(error=error):
                self.client.request.reset_mock()
                self.observations.clear()
                self.client.request.side_effect = error
                self.assertIsNone(self.invoke())
                self.client.request.assert_called_once()
                self.assertEqual(len(self.observations), 1)
                self.assertEqual(self.observations[0]["status"], "transport_error")

    def test_unexpected_programming_error_propagates(self):
        self.client.request.side_effect = RuntimeError("Synthetic internal defect")
        with self.assertRaisesRegex(RuntimeError, "Synthetic internal defect"):
            self.invoke()
        self.client.request.assert_called_once()
