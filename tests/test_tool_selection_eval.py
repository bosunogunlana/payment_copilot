"""Offline evaluator acceptance; scripted answers are not model-quality evidence."""

import json
import unittest
from collections import Counter

from app.tools.contracts import TOOL_ARGUMENT_MODELS, TrustedContext
from evals.score_tool_selection import DEFAULT_DATASET, read_jsonl, score


def prediction(case, *, name=None, arguments=None):
    return {"case_id": case["case_id"], "turn": {"tool_calls": [{
        "call_id": case["case_id"], "name": name or case["expected_tool"],
        "arguments_json": json.dumps(
            case["expected_arguments"] if arguments is None else arguments
        ),
    }]}}


class ToolSelectionEvalTest(unittest.TestCase):
    def setUp(self):
        self.cases = read_jsonl(DEFAULT_DATASET)

    def test_frozen_dataset_has_40_unique_synthetic_cases_and_valid_labels(self):
        self.assertEqual(len(self.cases), 40)
        self.assertEqual(len({c["case_id"] for c in self.cases}), 40)
        self.assertEqual(Counter(c["expected_tool"] for c in self.cases),
                         {name: 10 for name in TOOL_ARGUMENT_MODELS})
        for case in self.cases:
            with self.subTest(case=case["case_id"]):
                self.assertIs(case["synthetic"], True)
                self.assertEqual(case["dataset_version"], 1)
                self.assertTrue(case["question"].strip())
                TrustedContext.model_validate(case["context"])
                TOOL_ARGUMENT_MODELS[case["expected_tool"]].model_validate(
                    case["expected_arguments"]
                )

    def test_missing_predictions_count_against_full_denominator(self):
        report = score(self.cases, [prediction(c) for c in self.cases[:36]])
        self.assertEqual((report["correct"], report["total"]), (36, 40))
        self.assertTrue(report["threshold_met"])
        self.assertEqual(sum(r["missing_prediction"] for r in report["results"]), 4)
        self.assertFalse(score(self.cases, [prediction(c) for c in self.cases[:35]])[
            "threshold_met"
        ])

    def test_wrong_tool_invalid_turn_and_no_call_are_misses(self):
        for turn in (
            None, {"tool_calls": [], "final_text": "No tool needed"},
            {"tool_calls": [{"call_id": "x", "name": "unknown", "arguments_json": "{}"}]},
            {"tool_calls": "invalid"},
        ):
            with self.subTest(turn=turn):
                report = score(self.cases, [{"case_id": self.cases[0]["case_id"], "turn": turn}])
                self.assertEqual(report["correct"], 0)

    def test_tool_selection_and_argument_correctness_are_separate(self):
        for arguments in ({}, {"payment_id": "wrong"},
                          {"payment_id": "pay-shared", "organization_id": "org-b"}):
            with self.subTest(arguments=arguments):
                report = score(self.cases, [prediction(self.cases[0], arguments=arguments)])
                self.assertEqual(report["correct"], 1)
                self.assertEqual(report["arguments_correct"], 0)

    def test_duplicate_and_unknown_prediction_ids_are_rejected(self):
        row = prediction(self.cases[0])
        for rows in ([row, row], [{**row, "case_id": "unknown"}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                score(self.cases, rows)

    def test_first_call_alone_determines_selection(self):
        row = prediction(self.cases[0], name="get_ledger_entries")
        correct = prediction(self.cases[0])["turn"]["tool_calls"][0]
        row["turn"]["tool_calls"].append({**correct, "call_id": "second"})
        self.assertEqual(score(self.cases, [row])["correct"], 0)
