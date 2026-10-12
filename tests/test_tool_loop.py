"""Week 2 Phase 3 acceptance: manual loop with a scripted, offline model.

Learner-owned implementation: app.llm.tool_loop.ToolLoop.
See docs/WEEK-02-TOOL-LOOP-CONTRACT.md for the normalized model interface.
"""

import json
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import Mock

from app.llm.tool_loop import ToolLoop
from app.tools.contracts import TOOL_ARGUMENT_MODELS, TrustedContext
from app.tools.fixture_reader import FixtureReader
from app.tools.gateway import ToolGateway

FIXTURE = Path(__file__).resolve().parents[1] / "simulator/fixtures/week2_tools.json"


def call(call_id="c-1", name="get_payment", arguments=None):
    return {
        "call_id": call_id,
        "name": name,
        "arguments_json": json.dumps(
            {"payment_id": "pay-shared"} if arguments is None else arguments
        ),
    }


def calls(*items):
    return {"tool_calls": list(items), "final_text": None}


def final(text="Evidence reviewed."):
    return {"tool_calls": [], "final_text": text}


class ScriptedModel:
    """Capture immutable request snapshots and return predetermined turns."""

    def __init__(self, *turns):
        self.turns = list(turns)
        self.requests = []

    def __call__(self, *, messages, tools):
        self.requests.append(deepcopy({"messages": messages, "tools": tools}))
        if not self.turns:
            raise AssertionError("Unexpected model call after scripted turns")
        return deepcopy(self.turns.pop(0))


class ToolLoopTest(unittest.TestCase):
    def setUp(self):
        self.context = TrustedContext(organization_id="org-a", request_id="loop-001")
        self.authorize = Mock(return_value=True)
        self.reader = Mock(wraps=FixtureReader(path=FIXTURE))
        self.gateway = ToolGateway(authorize=self.authorize, reader=self.reader)

    def loop(self, model, **limits):
        return ToolLoop(model=model, gateway=self.gateway, **limits)

    def run_loop(self, model, **limits):
        return self.loop(model, **limits).run(
            question="Investigate this synthetic payment.", context=self.context
        )

    def assert_stopped(self, result, status):
        self.assertEqual(result.status, status)
        self.assertIsNone(result.final_text)

    def test_final_answer_without_tool_calls(self):
        model = ScriptedModel(final("No read requested."))
        result = self.run_loop(model)
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.final_text, "No read requested.")
        self.assertEqual(result.steps, 0)
        self.assertEqual(result.model_turns, 1)
        self.assertEqual(result.trace, [])
        self.reader.assert_not_called()

    def test_tool_result_returns_to_model_with_call_id_and_typed_evidence(self):
        model = ScriptedModel(calls(call()), final())
        result = self.run_loop(model)
        self.assertEqual(result.status, "completed")
        self.assertEqual((result.steps, result.model_turns), (1, 2))
        messages = model.requests[1]["messages"]
        tool_messages = [m for m in messages if m["role"] == "tool"]
        self.assertEqual(len(tool_messages), 1)
        self.assertEqual(tool_messages[0]["call_id"], "c-1")
        payload = json.loads(tool_messages[0]["content"])
        self.assertEqual(payload["data"]["organization_id"], "org-a")
        self.assertEqual(payload["data"]["amount_minor"], 1100)
        self.assertIsNone(payload["error"])
        self.assertTrue(
            any(m["role"] == "assistant" and m.get("tool_calls") for m in messages)
        )
        step = result.trace[0]
        self.assertEqual(step.call_id, "c-1")
        self.assertEqual(step.tool_name, "get_payment")
        self.assertEqual(step.arguments, {"payment_id": "pay-shared"})
        self.assertEqual(step.repetition, "first_read")
        self.assertGreaterEqual(step.duration_ms, 0)
        self.assertEqual(step.result.trace.organization_id, "org-a")
        self.assertEqual(step.result.trace.outcome, "succeeded")
        json.loads(result.model_dump_json())

    def test_tools_are_derived_from_the_existing_registry(self):
        model = ScriptedModel(final())
        self.run_loop(model)
        tools = model.requests[0]["tools"]
        self.assertEqual({tool["name"] for tool in tools}, set(TOOL_ARGUMENT_MODELS))
        for tool in tools:
            self.assertEqual(
                tool["parameters"],
                TOOL_ARGUMENT_MODELS[tool["name"]].model_json_schema(),
            )
            self.assertNotIn("organization_id", tool["parameters"]["properties"])

    def test_multiple_calls_are_serialized_and_correlated(self):
        model = ScriptedModel(
            calls(call("c-payment"), call("c-events", "get_payment_events")), final()
        )
        result = self.run_loop(model)
        self.assertEqual(result.steps, 2)
        tool_messages = [
            m for m in model.requests[1]["messages"] if m["role"] == "tool"
        ]
        self.assertEqual(
            [m["call_id"] for m in tool_messages], ["c-payment", "c-events"]
        )
        self.assertEqual([s.call_id for s in result.trace], ["c-payment", "c-events"])
        self.assertEqual(self.authorize.call_count, 2)
        self.assertEqual(self.reader.call_count, 2)

    def test_invalid_json_and_invalid_shapes_are_reported_without_reading(self):
        malformed = call()
        malformed["arguments_json"] = "{broken"
        for item in (malformed, call(arguments=[]), call(arguments={})):
            with self.subTest(item=item):
                model = ScriptedModel(calls(item), final())
                result = self.run_loop(model)
                self.assertEqual(result.trace[0].result.error.code, "INVALID_ARGUMENTS")
                self.assertIsNone(result.trace[0].arguments)
                payload = json.loads(model.requests[1]["messages"][-1]["content"])
                self.assertEqual(payload["error"]["code"], "INVALID_ARGUMENTS")
                self.authorize.assert_not_called()
                self.reader.assert_not_called()

    def test_unknown_tool_is_rejected_by_gateway(self):
        model = ScriptedModel(calls(call(name="refund_payment")), final())
        result = self.run_loop(model)
        self.assertEqual(result.trace[0].result.error.code, "UNKNOWN_TOOL")
        self.reader.assert_not_called()
        self.authorize.assert_not_called()

    def test_authorization_and_trusted_identity_are_preserved(self):
        self.authorize.return_value = False
        model = ScriptedModel(calls(call()), final())
        result = self.run_loop(model)
        self.assertEqual(result.trace[0].result.error.code, "UNAUTHORIZED")
        self.authorize.assert_called_once_with(
            context=self.context, tool_name="get_payment", payment_id="pay-shared"
        )
        self.reader.assert_not_called()

    def test_untrusted_extra_arguments_are_not_copied_to_trace_or_tool_output(self):
        secret = "synthetic-private-value"
        model = ScriptedModel(
            calls(
                call(
                    arguments={
                        "payment_id": "pay-shared",
                        "organization_id": "org-b",
                        "secret": secret,
                    }
                )
            ),
            final(),
        )
        result = self.run_loop(model)
        self.assertEqual(result.trace[0].result.error.code, "INVALID_ARGUMENTS")
        self.assertNotIn(secret, result.model_dump_json())
        tool_message = model.requests[1]["messages"][-1]
        self.assertNotIn(secret, tool_message["content"])
        self.reader.assert_not_called()

    def test_reader_error_returns_to_model_without_becoming_a_success(self):
        model = ScriptedModel(calls(call(arguments={"payment_id": "missing"})), final())
        result = self.run_loop(model)
        self.assertEqual(result.trace[0].result.error.code, "PAYMENT_NOT_FOUND")
        self.assertEqual(result.trace[0].result.trace.outcome, "failed")
        payload = json.loads(model.requests[1]["messages"][-1]["content"])
        self.assertIsNone(payload["data"])

    def test_tool_limit_bounds_a_batch_before_extra_execution(self):
        model = ScriptedModel(calls(call("c1"), call("c2"), call("c3")))
        result = self.run_loop(model, max_tool_steps=2)
        self.assert_stopped(result, "tool_limit")
        self.assertEqual(result.steps, 2)
        self.assertEqual(self.reader.call_count, 2)
        self.assertEqual(len(model.requests), 1)

    def test_invalid_calls_also_consume_the_tool_budget(self):
        model = ScriptedModel(calls(call("c1", arguments={}), call("c2", arguments={})))
        result = self.run_loop(model, max_tool_steps=1)
        self.assert_stopped(result, "tool_limit")
        self.assertEqual(result.steps, 1)
        self.reader.assert_not_called()

    def test_model_turn_limit_stops_before_an_additional_request(self):
        model = ScriptedModel(calls(call("c1")))
        result = self.run_loop(model, max_model_turns=1)
        self.assert_stopped(result, "model_limit")
        self.assertEqual(result.model_turns, 1)
        self.assertEqual(len(model.requests), 1)

    def test_replayed_call_id_stops_without_another_read(self):
        model = ScriptedModel(calls(call("same")), calls(call("same")))
        result = self.run_loop(model)
        self.assert_stopped(result, "repeated_call")
        self.assertEqual(result.steps, 1)
        self.reader.assert_called_once()
        self.authorize.assert_called_once()

    def test_new_call_id_with_same_arguments_is_an_authorized_fresh_read(self):
        model = ScriptedModel(calls(call("first")), calls(call("fresh")), final())
        result = self.run_loop(model)
        self.assertEqual(result.status, "completed")
        self.assertEqual(
            [s.repetition for s in result.trace], ["first_read", "fresh_read"]
        )
        self.assertEqual(self.reader.call_count, 2)
        self.assertEqual(self.authorize.call_count, 2)

    def test_replay_tracking_is_scoped_to_each_run(self):
        model = ScriptedModel(calls(call("c1")), final(), calls(call("c1")), final())
        loop = self.loop(model)
        for _ in range(2):
            result = loop.run(question="Read evidence.", context=self.context)
            self.assertEqual(result.status, "completed")
            self.assertEqual(result.trace[0].repetition, "first_read")
        self.assertEqual(self.reader.call_count, 2)

    def test_malformed_model_turn_stops_before_execution(self):
        invalid = [
            None,
            {},
            {"tool_calls": [], "final_text": None},
            {"tool_calls": [call()], "final_text": "Both modes"},
            calls({"name": "get_payment", "arguments_json": "{}"}),
            calls({**call(), "arguments_json": {}}),
            calls(call("duplicate"), call("duplicate")),
        ]
        for turn in invalid:
            with self.subTest(turn=turn):
                result = self.run_loop(ScriptedModel(turn))
                self.assert_stopped(result, "invalid_model_response")
                self.assertEqual(result.steps, 0)
                self.reader.assert_not_called()

    def test_limits_must_be_positive_integers(self):
        for field in ("max_tool_steps", "max_model_turns"):
            for invalid in (0, -1, True, 1.5):
                with self.subTest(field=field, invalid=invalid):
                    with self.assertRaises(ValueError):
                        self.loop(ScriptedModel(final()), **{field: invalid})

    def test_unexpected_model_and_reader_defects_propagate(self):
        with self.assertRaises(RuntimeError):
            self.run_loop(Mock(side_effect=RuntimeError("Synthetic model defect")))
        self.reader.side_effect = RuntimeError("Synthetic reader defect")
        with self.assertRaises(RuntimeError):
            self.run_loop(ScriptedModel(calls(call()), final()))
