"""Dataset integrity and coverage checks; no model calls."""

import json
import unittest
from pathlib import Path

from app.models.diagnosis import (
    DiagnosisCategory,
    Payment,
    PaymentStatus,
    RecommendedAction,
)


class Week1DatasetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "evals/datasets/week1.jsonl"
        cls.cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def test_cases_are_unique_synthetic_and_have_typed_labels_and_rationale(self):
        self.assertGreaterEqual(len(self.cases), 30)
        ids = [case["case_id"] for case in self.cases]
        self.assertEqual(len(set(ids)), len(ids))
        payloads = [json.dumps(case["payment"], sort_keys=True) for case in self.cases]
        self.assertEqual(len(set(payloads)), len(payloads))
        for case in self.cases:
            with self.subTest(case_id=case["case_id"]):
                self.assertRegex(case["case_id"], r"^case-\d{3}$")
                self.assertIs(case["synthetic"], True)
                self.assertTrue(case["rationale"].strip())
                parsed = Payment.model_validate(case["payment"])
                self.assertTrue(all("simulator" in event.source or event.source == "ledger" for event in parsed.events))
                expected = case["expected"]
                self.assertEqual(set(expected), {"status", "category", "recommended_action"})
                PaymentStatus(expected["status"])
                DiagnosisCategory(expected["category"])
                RecommendedAction(expected["recommended_action"])

    def test_failure_coverage_includes_supported_and_escalation_outcomes(self):
        tags = {tag for case in self.cases for tag in case["failure_tags"]}
        self.assertTrue({
            "timeout", "missing_events", "conflicting_signals",
            "plausible_wrong_cause", "insufficient_evidence", "duplicate_events",
        }.issubset(tags))
        categories = {case["expected"]["category"] for case in self.cases}
        self.assertTrue({
            "successful_payment", "provider_timeout", "authorization_failure", "unknown",
        }.issubset(categories))
        for case in self.cases:
            if {"missing_events", "conflicting_signals", "insufficient_evidence"}.intersection(case["failure_tags"]):
                with self.subTest(case_id=case["case_id"]):
                    self.assertEqual(case["expected"]["category"], "unknown")
                    self.assertEqual(case["expected"]["recommended_action"], "escalate_to_human")
