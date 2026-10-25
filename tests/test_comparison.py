import copy
import unittest
from unittest.mock import Mock

from app.models.diagnosis import PaymentStatus
from evals.compare_diagnosis import compare, estimated_cost
from test_diagnosis import payment
from test_llm_diagnose import VALID_OUTPUT, completed


CONFIGS = [
    {"name": name, "model": "test-model", "input_usd_per_million": 2,
     "output_usd_per_million": 10, "max_output_tokens": 512}
    for name in ("A", "B")
]
CASE = {
    "case_id": "test-case", "failure_tags": ["timeout"],
    "payment": payment(PaymentStatus.PENDING, []).model_dump(mode="json"),
    "expected": {key: VALID_OUTPUT[key] for key in ("status", "category", "recommended_action")},
}


class ComparisonTest(unittest.TestCase):
    def test_all_payments_are_validated_before_transport_construction(self):
        invalid = copy.deepcopy(CASE)
        invalid["case_id"] = "invalid"
        invalid["payment"]["amount_minor"] = -1
        factory = Mock()
        with self.assertRaises(ValueError):
            compare([CASE, invalid], CONFIGS, factory, budget_usd=1, reserve_usd=0.01)
        factory.assert_not_called()

    def test_checkpoint_preserves_first_result_when_next_call_crashes(self):
        transport = Mock(side_effect=[
            {**completed(), "usage": {"input_tokens": 1, "output_tokens": 1}},
            RuntimeError("synthetic programming defect"),
        ])
        checkpoint = Mock()
        with self.assertRaises(RuntimeError):
            compare([CASE], CONFIGS, lambda _: transport, budget_usd=1,
                    reserve_usd=0.01, checkpoint=checkpoint)
        checkpoint.assert_called_once()
        self.assertEqual(checkpoint.call_args.args[0][0]["configuration"], "A")

    def test_cost_uses_usage_and_missing_usage_is_not_free(self):
        self.assertAlmostEqual(estimated_cost({"input_tokens": 1000, "output_tokens": 100}, CONFIGS[0]), 0.003)
        for usage in (None, {}, {"input_tokens": -1, "output_tokens": 1}):
            self.assertIsNone(estimated_cost(usage, CONFIGS[0]))

    def test_same_cases_are_scored_for_both_configurations(self):
        response = {**completed(), "usage": {"input_tokens": 1000, "output_tokens": 100}}
        report = compare([CASE], CONFIGS, lambda _: Mock(return_value=response), budget_usd=1, reserve_usd=0.01)
        self.assertEqual(len(report["rows"]), 2)
        for row in report["rows"]:
            self.assertTrue(row["schema_valid"])
            self.assertTrue(row["label_match"])
            self.assertGreaterEqual(row["latency_ms"], 0)
        self.assertEqual(report["summary"]["A/tag:timeout"]["label_match_rate"], 1)

    def test_schema_valid_wrong_label_does_not_pass(self):
        response = {**completed({**VALID_OUTPUT, "category": "network_error"}),
                    "usage": {"input_tokens": 1, "output_tokens": 1}}
        report = compare([CASE], CONFIGS, lambda _: Mock(return_value=response), budget_usd=1, reserve_usd=0.01)
        self.assertTrue(report["rows"][0]["schema_valid"])
        self.assertFalse(report["rows"][0]["label_match"])

    def test_budget_exhaustion_skips_without_calling_transport(self):
        transport = Mock()
        report = compare([CASE], CONFIGS, lambda _: transport, budget_usd=0.001, reserve_usd=0.01)
        transport.assert_not_called()
        self.assertTrue(all(row["skip_reason"] == "budget_reservation_exhausted" for row in report["rows"]))

    def test_missing_usage_stops_after_one_attempt(self):
        transport = Mock(return_value=completed())
        report = compare([CASE], CONFIGS, lambda _: transport, budget_usd=1, reserve_usd=0.01)
        transport.assert_called_once()
        self.assertIsNone(report["rows"][0]["estimated_cost_usd"])
        self.assertEqual(report["rows"][1]["skip_reason"], "usage_unavailable")

    def test_unknown_with_invented_cause_is_unsafe_despite_matching_labels(self):
        case = copy.deepcopy(CASE)
        unknown = {"status": "unknown", "category": "unknown", "recommended_action": "escalate_to_human"}
        case["expected"] = unknown
        response = {**completed({**unknown, "confidence": 0.2, "likely_cause": "Invented cause"}),
                    "usage": {"input_tokens": 1, "output_tokens": 1}}
        report = compare([case], CONFIGS, lambda _: Mock(return_value=response), budget_usd=1, reserve_usd=0.01)
        self.assertTrue(report["rows"][0]["label_match"])
        self.assertFalse(report["rows"][0]["uncertainty_safe"])
