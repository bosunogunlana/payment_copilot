"""Collector tests use stubs only; no API keys, network or quality claims."""

import io
import json
import os
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from openai.types.responses import ResponseFunctionToolCall
from unittest.mock import Mock, patch

from evals.collect_tool_selection import collect, main
from evals.score_tool_selection import DEFAULT_DATASET, read_jsonl, score


class CollectToolSelectionTest(unittest.TestCase):
    def setUp(self):
        self.cases = read_jsonl(DEFAULT_DATASET)
        self.observations = []
        self.rows = []

        def respond(**kwargs):
            self.observations.append({"status": "completed", "outcome": "valid_response",
                                      "duration_ms": 1.0,
                                      "usage": {"input_tokens": 12, "output_tokens": 8}})
            return {"tool_calls": [{"call_id": "first-call", "name": "get_payment",
                                    "arguments_json": '{"payment_id":"pay-shared"}'}]}
        self.model = Mock(side_effect=respond)

    def run_collection(self, **changes):
        options = dict(model=self.model, observations=self.observations,
                       budget_usd=Decimal("1"), reserve_usd=Decimal("0.025"),
                       emit=self.rows.append)
        options.update(changes)
        return collect(self.cases, **options)

    def test_collects_one_turn_per_case_without_exposing_labels_or_context(self):
        summary = self.run_collection()
        self.assertEqual(summary["attempted"], 40)
        self.assertEqual(self.model.call_count, 40)
        self.assertEqual(len(self.rows), 40)
        for case, call in zip(self.cases, self.model.call_args_list):
            self.assertEqual(set(call.kwargs), {"messages", "tools"})
            self.assertEqual(call.kwargs["messages"], [{"role": "user", "content": case["question"]}])
        self.assertEqual(score(self.cases, self.rows)["total"], 40)
        self.assertEqual(self.rows[0]["metadata"]["usage"]["input_tokens"], 12)

    def test_reserves_before_request_and_records_skipped_cases(self):
        summary = self.run_collection(budget_usd=Decimal("0.05"))
        self.assertEqual(summary["attempted"], 2)
        self.assertEqual(summary["reserved_usd"], "0.050")
        self.assertEqual(self.model.call_count, 2)
        self.assertEqual(len(self.rows), 40)
        self.assertEqual(self.rows[2]["skip_reason"], "budget")
        self.assertIsNone(self.rows[2]["turn"])

    def test_insufficient_first_reservation_makes_no_request(self):
        summary = self.run_collection(budget_usd=Decimal("0.001"))
        self.model.assert_not_called()
        self.assertEqual(summary["attempted"], 0)
        self.assertEqual(len(self.rows), 40)

    def test_missing_usage_and_transport_errors_stop_future_requests(self):
        for metadata, expected in (
            ({"outcome": "invalid_response", "usage": None}, "missing_usage"),
            ({"outcome": "transport_error", "usage": None}, "transport_error"),
            ({"outcome": "valid_response", "usage": {"input_tokens": True, "output_tokens": 8}}, "missing_usage"),
        ):
            with self.subTest(expected=expected):
                self.rows.clear()
                def respond(**kwargs):
                    self.observations.append(metadata)
                    return None
                model = Mock(side_effect=respond)
                summary = self.run_collection(model=model)
                model.assert_called_once()
                self.assertEqual(summary["stop_reason"], expected)
                self.assertEqual(self.rows[1]["skip_reason"], expected)
                self.assertIsNone(self.rows[0]["turn"])

    def test_programming_defects_propagate_after_preserving_emitted_rows(self):
        original = self.model.side_effect
        calls = 0
        def respond(**kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("Synthetic defect")
            return original(**kwargs)
        self.model.side_effect = respond
        with self.assertRaisesRegex(RuntimeError, "Synthetic defect"):
            self.run_collection()
        self.assertEqual(len(self.rows), 1)

    def test_invalid_budget_or_dataset_fails_before_request(self):
        for budget in (Decimal("0"), Decimal("NaN"), Decimal("Infinity")):
            with self.subTest(budget=budget), self.assertRaises(ValueError):
                self.run_collection(budget_usd=budget)
        self.cases[-1]["case_id"] = self.cases[0]["case_id"]
        with self.assertRaises(ValueError):
            self.run_collection()
        self.model.assert_not_called()

    def test_observations_are_snapshots_and_reset_between_cases(self):
        self.run_collection()
        self.observations[0]["usage"]["input_tokens"] = 999
        self.assertEqual(self.rows[0]["metadata"]["usage"]["input_tokens"], 12)
        self.assertEqual(len(self.observations), 1)

    def test_dry_run_never_constructs_sdk_or_writes_outputs(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "predictions.jsonl"
            with patch("evals.collect_tool_selection.create_openai_client") as factory:
                with patch.dict(os.environ, {}, clear=True), redirect_stdout(io.StringIO()) as stream:
                    self.assertEqual(main(["--output", str(output)]), 0)
                factory.assert_not_called()
            self.assertEqual(json.loads(stream.getvalue())["requests"], 0)
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_mocked_live_wiring_persists_predictions_manifest_and_usage(self):
        sdk = Mock()
        sdk.responses.create.return_value = SimpleNamespace(
            status="completed", usage=SimpleNamespace(input_tokens=12, output_tokens=8),
            output=[ResponseFunctionToolCall(type="function_call", call_id="call-001",
                                    name="get_payment", arguments='{"payment_id":"pay-shared"}')],
        )
        with TemporaryDirectory() as directory:
            output = Path(directory) / "predictions.jsonl"
            with patch("evals.collect_tool_selection.create_openai_client") as factory:
                factory.return_value.__enter__.return_value = sdk
                with patch.dict(os.environ, {"OPENAI_API_KEY": "synthetic-secret"}):
                    with redirect_stdout(io.StringIO()), patch("sys.stderr", io.StringIO()):
                        result = main(["--live", "--acknowledge-spend", "--output", str(output),
                                       "--budget-usd", "1", "--reserve-usd", "0.025"])
                self.assertEqual(result, 0)
            rows = read_jsonl(output)
            manifest = json.loads(output.with_name(output.name + ".run.json").read_text())
            self.assertEqual(len(rows), 40)
            self.assertEqual(sdk.responses.create.call_count, 40)
            self.assertEqual(manifest["status"], "completed")
            self.assertEqual(manifest["attempted"], 40)
            self.assertEqual(len(manifest["predictions_sha256"]), 64)
            self.assertEqual(rows[0]["metadata"]["usage"]["input_tokens"], 12)
            self.assertNotIn("synthetic-secret", output.read_text() + json.dumps(manifest))

    def test_live_requires_explicit_spend_configuration_before_client_construction(self):
        with patch("evals.collect_tool_selection.create_openai_client") as factory:
            with redirect_stdout(io.StringIO()), patch("sys.stderr", io.StringIO()):
                with self.assertRaises(SystemExit):
                    main(["--live"])
            factory.assert_not_called()
