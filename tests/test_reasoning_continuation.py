"""Reasoning replay across real application layers with SDK calls mocked out."""

import json
import unittest
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import Mock

from openai.types.responses import (
    ResponseFunctionToolCall, ResponseOutputMessage, ResponseReasoningItem,
)

from app.clients.openai_tool_client import OpenAIToolClient
from app.llm.tool_loop import ToolLoop
from app.llm.tool_model import ToolModel
from app.tools.contracts import TrustedContext
from app.tools.gateway import ToolGateway


def reasoning(number):
    return ResponseReasoningItem(id=f"rs_{number}", summary=[], type="reasoning",
                                 encrypted_content=f"synthetic-ciphertext-{number}")


def function(number, name="get_payment"):
    return ResponseFunctionToolCall(id=f"fc_{number}", call_id=f"call-{number}",
                                    type="function_call", name=name,
                                    arguments='{"payment_id":"pay-shared"}')


def final():
    return ResponseOutputMessage(id="msg_final", role="assistant", status="completed",
                                 type="message", content=[{
                                     "type": "output_text", "text": "Evidence received.",
                                     "annotations": [],
                                 }])


def response(items, status="completed"):
    return SimpleNamespace(status=status, output=items,
                           usage=SimpleNamespace(input_tokens=20, output_tokens=10))


def serialized(items):
    return [item.model_dump(mode="json", exclude_none=True) for item in items]


class ReasoningContinuationTest(unittest.TestCase):
    def setUp(self):
        self.sdk = Mock()
        self.observations = []
        self.model = ToolModel(client=OpenAIToolClient(client=self.sdk),
                               instructions="Read synthetic evidence.", request_timeout_s=2.0,
                               max_output_tokens=512, observe=self.observations.append)
        self.reader = Mock(return_value=[])
        self.authorize = Mock(return_value=True)
        self.loop = ToolLoop(model=self.model, gateway=ToolGateway(
            authorize=self.authorize, reader=self.reader))
        self.context = TrustedContext(organization_id="org-a", request_id="reasoning-test")

    def test_two_turn_loop_replays_reasoning_call_then_correlated_result_once(self):
        items = [reasoning(1), function(1)]
        self.sdk.responses.create.side_effect = [response(items), response([final()])]
        result = self.loop.run("Inspect pay-shared", self.context)
        self.assertEqual(result.status, "completed")
        self.assertEqual((result.steps, result.model_turns), (1, 2))
        second = self.sdk.responses.create.call_args_list[1].kwargs
        self.assertEqual(second["input"][1:3], serialized(items))
        self.assertEqual(second["input"][3]["type"], "function_call_output")
        self.assertEqual(second["input"][3]["call_id"], "call-1")
        self.assertEqual(json.loads(second["input"][3]["output"])["data"], [])
        self.assertEqual(len(second["input"]), 4)
        self.reader.assert_called_once()
        for invocation in self.sdk.responses.create.call_args_list:
            self.assertIs(invocation.kwargs["store"], False)
            self.assertIn("reasoning.encrypted_content", invocation.kwargs["include"])

    def test_multiple_calls_and_consecutive_tool_turns_preserve_entire_history(self):
        first = [reasoning(1), function(1), function(2, "get_payment_events")]
        second = [reasoning(2), function(3, "get_ledger_entries")]
        self.sdk.responses.create.side_effect = [response(first), response(second), response([final()])]
        result = self.loop.run("Inspect pay-shared", self.context)
        self.assertEqual(result.status, "completed")
        self.assertEqual((result.steps, result.model_turns), (3, 3))
        inputs = self.sdk.responses.create.call_args_list[2].kwargs["input"]
        self.assertEqual(inputs[1:4], serialized(first))
        self.assertEqual([item["call_id"] for item in inputs[4:6]], ["call-1", "call-2"])
        self.assertTrue(all(item["type"] == "function_call_output" for item in inputs[4:6]))
        self.assertEqual(inputs[6:8], serialized(second))
        self.assertEqual(inputs[8]["call_id"], "call-3")
        self.assertEqual(len(inputs), 9)
        self.assertEqual(self.authorize.call_count, 3)

    def test_reusing_loop_and_client_does_not_leak_state_between_runs(self):
        self.sdk.responses.create.side_effect = [response([reasoning(1), function(1)]),
                                                response([final()])] * 2
        for question in ("First request", "Independent request"):
            self.assertEqual(self.loop.run(question, self.context).status, "completed")
        inputs = self.sdk.responses.create.call_args_list[2].kwargs["input"]
        self.assertEqual(inputs, [{"role": "user", "content": "Independent request"}])

    def test_malformed_provider_state_rejects_turn_before_gateway_execution(self):
        valid_call = {"id": "call-1", "name": "get_payment", "arguments": "{}"}
        states = [[], {}, {"provider": 1, "output_items": []},
                  {"provider": "", "output_items": []},
                  {"provider": "   ", "output_items": []},
                  {"provider": "openai.provider", "output_items": "invalid"},
                  {"provider": "openai.provider", "output_items": [1]},
                  {"provider": "openai.provider"}]
        for state in states:
            with self.subTest(state=state):
                client = Mock()
                client.request.return_value = {"status": "completed", "refusal": None,
                    "tool_calls": [valid_call], "output_text": None, "usage": None,
                    "provider_state": state}
                model = ToolModel(client=client, instructions="Read evidence.",
                                  request_timeout_s=2.0, max_output_tokens=512,
                                  observe=self.observations.append)
                self.assertIsNone(model(messages=[{"role": "user", "content": "Inspect"}], tools=[]))
                gateway = Mock()
                result = ToolLoop(model=model, gateway=gateway).run("Inspect", self.context)
                self.assertEqual(result.status, "invalid_model_response")
                gateway.execute.assert_not_called()
                self.assertEqual(self.observations[-1]["outcome"], "invalid_response")

    def test_provider_state_is_copied_and_translation_does_not_mutate_it(self):
        items = serialized([reasoning(1), function(1)])
        state = {"provider": "openai.provider", "output_items": items}
        message = {"role": "assistant", "tool_calls": [], "provider_state": state}
        before = deepcopy(message)
        translated = OpenAIToolClient._translate_messages([message])
        self.assertEqual(message, before)
        translated[0]["encrypted_content"] = "changed"
        self.assertEqual(message, before)

    def test_foreign_provider_state_is_rejected_before_sdk_request(self):
        payload = self.model._build_request(messages=[{
            "role": "assistant", "tool_calls": [],
            "provider_state": {"provider": "other-provider", "output_items": []},
        }], tools=[])
        with self.assertRaises(ValueError):
            OpenAIToolClient(client=self.sdk).request(payload=payload)
        self.sdk.responses.create.assert_not_called()

    def test_refusal_or_incomplete_output_does_not_execute_or_continue(self):
        refusal = ResponseOutputMessage(id="msg_refused", role="assistant", status="completed",
            type="message", content=[{"type": "refusal", "refusal": "Cannot comply"}])
        for raw in (response([reasoning(1), function(1)], status="incomplete"),
                    response([reasoning(1), function(1), refusal])):
            with self.subTest(status=raw.status):
                self.sdk.responses.create.reset_mock()
                self.sdk.responses.create.side_effect = None
                self.sdk.responses.create.return_value = raw
                result = self.loop.run("Inspect", self.context)
                self.assertEqual(result.status, "invalid_model_response")
                self.reader.assert_not_called()
                self.sdk.responses.create.assert_called_once()

    def test_replayed_call_id_still_stops_before_a_second_execution(self):
        self.sdk.responses.create.side_effect = [response([reasoning(1), function(1)]),
                                                response([reasoning(2), function(1)])]
        result = self.loop.run("Inspect", self.context)
        self.assertEqual(result.status, "repeated_call")
        self.reader.assert_called_once()
