"""Manual live walkthrough wiring, verified without API calls."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

from openai.types.responses import ResponseFunctionToolCall
from test_reasoning_continuation import final, reasoning, response

from scripts.week2_multi_turn import SEQUENCE, main, run_walkthrough


class MultiTurnScriptTest(unittest.TestCase):
    def test_dry_run_constructs_no_client(self):
        with patch("scripts.week2_multi_turn.create_openai_client") as factory:
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main([]), 0)
            factory.assert_not_called()

    def test_four_tool_rounds_preserve_reasoning_and_results_before_final_answer(self):
        sdk = Mock()
        outputs = []
        for number, name in enumerate(SEQUENCE, 1):
            arguments = '{"payment_id":"pay-shared"}'
            if name == "get_provider_status":
                arguments = '{"payment_id":"pay-shared","provider_id":"simulator"}'
            outputs.append(response([reasoning(number), ResponseFunctionToolCall(
                type="function_call", id=f"fc_{number}", call_id=f"call-{number}",
                name=name, arguments=arguments)]))
        sdk.responses.create.side_effect = outputs + [response([final()])]
        with redirect_stdout(io.StringIO()):
            report = run_walkthrough(sdk=sdk, model_name="synthetic-model",
                                     timeout_s=2.0, max_output_tokens=512)
        self.assertTrue(report["multi_turn_verified"])
        self.assertEqual(report["result"]["model_turns"], 5)
        self.assertEqual(report["result"]["steps"], 4)
        last_input = sdk.responses.create.call_args_list[-1].kwargs["input"]
        self.assertEqual([item["type"] for item in last_input[1:]],
                         ["reasoning", "function_call", "function_call_output"] * 4)
        self.assertEqual([item["call_id"] for item in last_input if item.get("type") == "function_call_output"],
                         [f"call-{i}" for i in range(1, 5)])

    def test_early_text_answer_does_not_claim_multi_turn_success(self):
        sdk = Mock()
        sdk.responses.create.return_value = response([final()])
        with redirect_stdout(io.StringIO()):
            report = run_walkthrough(sdk=sdk, model_name="synthetic-model",
                                     timeout_s=2.0, max_output_tokens=512)
        self.assertFalse(report["multi_turn_verified"])
        self.assertEqual(report["result"]["steps"], 0)
        sdk.responses.create.assert_called_once()
