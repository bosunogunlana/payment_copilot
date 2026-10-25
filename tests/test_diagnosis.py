import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from app.models.diagnosis import (
    Diagnosis,
    DiagnosisCategory,
    Payment,
    PaymentEvent,
    PaymentStatus,
    RecommendedAction,
)


def event(
    event_id: str, event_type: str, *, reason_code: str | None = None
) -> PaymentEvent:
    return PaymentEvent(
        event_id=event_id,
        event_type=event_type,
        occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        source="simulator",
        reason_code=reason_code,
    )


def payment(status: PaymentStatus, events: list[PaymentEvent]) -> Payment:
    return Payment(
        payment_id="pay_test",
        organization_id="org_demo",
        amount_minor=1250,
        currency="USD",
        status=status,
        events=events,
    )


class DiagnosisModelTest(unittest.TestCase):
    def test_successful_payment_is_diagnosed(self):
        result = Diagnosis.diagnose(
            payment(PaymentStatus.SUCCEEDED, [event("evt_posted", "ledger.posted")])
        )

        self.assertEqual(result.status, PaymentStatus.SUCCEEDED)
        self.assertEqual(result.category, DiagnosisCategory.SUCCESSFUL_PAYMENT)
        self.assertEqual(result.recommended_action, RecommendedAction.NO_ACTION)
        self.assertIsInstance(result.likely_cause, str)
        self.assertTrue(result.likely_cause.strip())
        self.assertGreater(result.confidence, 0.5)

    def test_pending_provider_timeout_is_diagnosed_as_reconciliation_work(self):
        result = Diagnosis.diagnose(
            payment(PaymentStatus.PENDING, [event("evt_timeout", "provider.timeout")])
        )

        self.assertEqual(result.status, PaymentStatus.PENDING)
        self.assertEqual(result.category, DiagnosisCategory.PROVIDER_TIMEOUT)
        self.assertEqual(result.recommended_action, RecommendedAction.WAIT_AND_RECONCILE)
        self.assertEqual(
            result.likely_cause, "The provider did not return a terminal result."
        )
        self.assertGreater(result.confidence, 0.5)

    def test_pending_payment_without_timeout_evidence_fails_closed(self):
        result = Diagnosis.diagnose(
            payment(PaymentStatus.PENDING, [event("evt_created", "payment.created")])
        )

        self.assertEqual(result.status, PaymentStatus.UNKNOWN)
        self.assertEqual(result.category, DiagnosisCategory.UNKNOWN)
        self.assertEqual(result.recommended_action, RecommendedAction.ESCALATE_TO_HUMAN)
        self.assertLess(result.confidence, 0.5)

    def test_unknown_payment_with_events_has_low_confidence_and_escalates(self):
        result = Diagnosis.diagnose(
            payment(PaymentStatus.UNKNOWN, [event("evt_created", "payment.created")])
        )

        self.assertEqual(result.status, PaymentStatus.UNKNOWN)
        self.assertEqual(result.category, DiagnosisCategory.UNKNOWN)
        self.assertEqual(result.recommended_action, RecommendedAction.ESCALATE_TO_HUMAN)
        self.assertIsNone(result.likely_cause)
        self.assertLess(result.confidence, 0.5)

    def test_failed_provider_decline_is_diagnosed_as_authorization_failure(self):
        result = Diagnosis.diagnose(
            payment(
                PaymentStatus.FAILED,
                [event("evt_declined", "provider.declined", reason_code="AUTH_DECLINED")],
            )
        )

        self.assertEqual(result.status, PaymentStatus.FAILED)
        self.assertEqual(result.category, DiagnosisCategory.AUTHORIZATION_FAILURE)
        self.assertEqual(result.recommended_action, RecommendedAction.ESCALATE_TO_PROVIDER)
        self.assertEqual(result.likely_cause, "The provider rejected payment authorization.")
        self.assertGreater(result.confidence, 0.5)

    def test_decline_without_authorization_reason_code_fails_closed(self):
        for reason_code in (None, "", "INSUFFICIENT_FUNDS", "UNRECOGNIZED"):
            with self.subTest(reason_code=reason_code):
                declined = event(
                    "evt_declined", "provider.declined", reason_code=reason_code
                )
                declined.message = "A prior attempt mentioned AUTH_DECLINED."
                result = Diagnosis.diagnose(payment(PaymentStatus.FAILED, [declined]))

                self.assertEqual(result.status, PaymentStatus.UNKNOWN)
                self.assertEqual(result.category, DiagnosisCategory.UNKNOWN)
                self.assertEqual(
                    result.recommended_action, RecommendedAction.ESCALATE_TO_HUMAN
                )
                self.assertIsNone(result.likely_cause)
                self.assertLess(result.confidence, 0.5)

    def test_authorization_code_on_another_event_does_not_explain_decline(self):
        result = Diagnosis.diagnose(
            payment(
                PaymentStatus.FAILED,
                [
                    event("evt_created", "payment.created", reason_code="AUTH_DECLINED"),
                    event("evt_declined", "provider.declined"),
                ],
            )
        )

        self.assertEqual(result.status, PaymentStatus.UNKNOWN)
        self.assertEqual(result.category, DiagnosisCategory.UNKNOWN)
        self.assertEqual(result.recommended_action, RecommendedAction.ESCALATE_TO_HUMAN)
        self.assertIsNone(result.likely_cause)
        self.assertLess(result.confidence, 0.5)

    def test_failed_payment_without_decline_evidence_fails_closed(self):
        result = Diagnosis.diagnose(
            payment(PaymentStatus.FAILED, [event("evt_created", "payment.created")])
        )

        self.assertEqual(result.status, PaymentStatus.UNKNOWN)
        self.assertEqual(result.category, DiagnosisCategory.UNKNOWN)
        self.assertEqual(result.recommended_action, RecommendedAction.ESCALATE_TO_HUMAN)
        self.assertLess(result.confidence, 0.5)

    def test_conflicting_events_fail_closed_even_when_payment_status_succeeded(self):
        result = Diagnosis.diagnose(
            payment(
                PaymentStatus.SUCCEEDED,
                [
                    event("evt_declined", "provider.declined"),
                    event("evt_posted", "ledger.posted"),
                ],
            )
        )

        self.assertEqual(result.status, PaymentStatus.UNKNOWN)
        self.assertEqual(result.category, DiagnosisCategory.UNKNOWN)
        self.assertEqual(result.recommended_action, RecommendedAction.ESCALATE_TO_HUMAN)
        self.assertLess(result.confidence, 0.5)

    def test_pending_payment_without_events_fails_closed_as_unknown(self):
        result = Diagnosis.diagnose(payment(PaymentStatus.PENDING, []))

        self.assertEqual(result.status, PaymentStatus.UNKNOWN)
        self.assertEqual(result.category, DiagnosisCategory.UNKNOWN)
        self.assertEqual(result.recommended_action, RecommendedAction.ESCALATE_TO_HUMAN)
        self.assertLess(result.confidence, 0.5)

    def test_starter_fixtures_match_expected_labels_and_round_trip_as_diagnosis(self):
        dataset_path = (
            Path(__file__).resolve().parents[1] / "evals" / "datasets" / "week1.jsonl"
        )
        cases = [
            json.loads(line)
            for line in dataset_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertGreaterEqual(len(cases), 5)
        self.assertEqual(len({case["case_id"] for case in cases}), len(cases))

        for case in cases:
            with self.subTest(case_id=case["case_id"]):
                result = Diagnosis.diagnose(Payment.model_validate(case["payment"]))
                self.assertIsInstance(result, Diagnosis)
                restored = Diagnosis.model_validate_json(result.model_dump_json())
                self.assertEqual(restored, result)
                actual = restored.model_dump(mode="json")
                for field, expected in case["expected"].items():
                    self.assertEqual(actual[field], expected, field)
                if result.category == DiagnosisCategory.UNKNOWN:
                    self.assertIsNone(result.likely_cause)
                    self.assertEqual(
                        result.recommended_action, RecommendedAction.ESCALATE_TO_HUMAN
                    )
                    self.assertLess(result.confidence, 0.5)

    def test_valid_payment_contains_typed_events(self):
        payment = Payment(
            payment_id="pay_001",
            organization_id="org_demo",
            amount_minor=1250,
            currency="USD",
            status=PaymentStatus.SUCCEEDED,
            events=[event("evt_001", "ledger.posted")],
        )

        self.assertEqual(payment.events[0].event_type, "ledger.posted")
        self.assertEqual(payment.status, PaymentStatus.SUCCEEDED)

    def test_negative_amount_is_rejected(self):
        with self.assertRaises(ValidationError):
            Payment(
                payment_id="pay_invalid",
                organization_id="org_demo",
                amount_minor=-1,
                currency="USD",
                status=PaymentStatus.FAILED,
                events=[],
            )

    def test_missing_payment_identifiers_are_rejected(self):
        valid_input = payment(PaymentStatus.PENDING, []).model_dump()

        for field in ("payment_id", "organization_id"):
            with self.subTest(field=field):
                invalid_input = valid_input.copy()
                del invalid_input[field]

                with self.assertRaises(ValidationError) as raised:
                    Payment.model_validate(invalid_input)

                errors = raised.exception.errors()
                self.assertEqual(len(errors), 1)
                self.assertEqual(errors[0]["loc"], (field,))
                self.assertEqual(errors[0]["type"], "missing")

    def test_invalid_diagnosis_enum_values_are_rejected(self):
        valid_output = {
            "status": "unknown",
            "category": "unknown",
            "recommended_action": "escalate_to_human",
            "likely_cause": "insufficient evidence",
            "confidence": 0.2,
        }
        Diagnosis.model_validate(valid_output)

        for field in ("status", "category", "recommended_action"):
            with self.subTest(field=field):
                invalid_output = {**valid_output, field: "unsupported_value"}

                with self.assertRaises(ValidationError) as raised:
                    Diagnosis.model_validate(invalid_output)

                errors = raised.exception.errors()
                self.assertEqual(len(errors), 1)
                self.assertEqual(errors[0]["loc"], (field,))
                self.assertEqual(errors[0]["type"], "enum")

    def test_confidence_must_be_between_zero_and_one(self):
        with self.assertRaises(ValidationError):
            Diagnosis(
                status=PaymentStatus.UNKNOWN,
                category=DiagnosisCategory.UNKNOWN,
                likely_cause="insufficient evidence",
                recommended_action=RecommendedAction.ESCALATE_TO_HUMAN,
                confidence=1.1,
            )

    def test_currency_must_be_an_iso_style_three_letter_code(self):
        with self.assertRaises(ValidationError):
            Payment(
                payment_id="pay_invalid_currency",
                organization_id="org_demo",
                amount_minor=100,
                currency="X",
                status=PaymentStatus.PENDING,
                events=[],
            )


if __name__ == "__main__":
    unittest.main()
