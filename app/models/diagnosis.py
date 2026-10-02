from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class PaymentStatus(StrEnum):
    SUCCEEDED = "succeeded"
    PENDING = "pending"
    FAILED = "failed"
    UNKNOWN = "unknown"


class PaymentEvent(BaseModel):
    event_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    status: str | None = None
    occurred_at: datetime
    source: str = Field(min_length=1)
    message: str | None = None
    reason_code: str | None = None


class Payment(BaseModel):
    payment_id: str = Field(min_length=1)
    organization_id: str = Field(min_length=1)
    amount_minor: int = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")
    status: PaymentStatus
    events: list[PaymentEvent]


class DiagnosisCategory(StrEnum):
    SUCCESSFUL_PAYMENT = "successful_payment"
    PROVIDER_TIMEOUT = "provider_timeout"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    AUTHORIZATION_FAILURE = "authorization_failure"
    DUPLICATE_PAYMENT = "duplicate_payment"
    NETWORK_ERROR = "network_error"
    REFUND = "refund"
    UNKNOWN = "unknown"


class RecommendedAction(StrEnum):
    NO_ACTION = "no_action"
    WAIT_AND_RECONCILE = "wait_and_reconcile"
    RETRY_WITH_IDEMPOTENCY = "retry_with_idempotency"
    ASK_CUSTOMER_TO_UPDATE_FUNDING = "ask_customer_to_update_funding"
    ESCALATE_TO_PROVIDER = "escalate_to_provider"
    INVESTIGATE_LEDGER = "investigate_ledger"
    ESCALATE_TO_HUMAN = "escalate_to_human"


class Diagnosis(BaseModel):
    status: PaymentStatus
    category: DiagnosisCategory
    recommended_action: RecommendedAction
    likely_cause: str | None = None
    confidence: float = Field(ge=0, le=1)

    @classmethod
    def diagnose(cls, payment: Payment) -> "Diagnosis":
        if not payment.events:
            return cls(
                status=PaymentStatus.UNKNOWN,
                category=DiagnosisCategory.UNKNOWN,
                recommended_action=RecommendedAction.ESCALATE_TO_HUMAN,
                confidence=0.2,
            )

        event_types = {event.event_type for event in payment.events}

        if "ledger.posted" in event_types and "provider.declined" in event_types:
            return cls(
                status=PaymentStatus.UNKNOWN,
                category=DiagnosisCategory.UNKNOWN,
                recommended_action=RecommendedAction.ESCALATE_TO_HUMAN,
                confidence=0.4,
            )

        if payment.status == PaymentStatus.SUCCEEDED:
            return cls(
                status=PaymentStatus.SUCCEEDED,
                category=DiagnosisCategory.SUCCESSFUL_PAYMENT,
                recommended_action=RecommendedAction.NO_ACTION,
                likely_cause=(
                    "The payment completed and its ledger entry was posted."
                    if "ledger.posted" in event_types
                    else "The payment is recorded as completed"
                ),
                confidence=1.0,
            )

        if payment.status == PaymentStatus.UNKNOWN:
            return cls(
                status=PaymentStatus.UNKNOWN,
                category=DiagnosisCategory.UNKNOWN,
                recommended_action=RecommendedAction.ESCALATE_TO_HUMAN,
                confidence=0.2,
            )

        if payment.status == PaymentStatus.PENDING:
            if "provider.timeout" in event_types:
                return cls(
                    status=PaymentStatus.PENDING,
                    category=DiagnosisCategory.PROVIDER_TIMEOUT,
                    recommended_action=RecommendedAction.WAIT_AND_RECONCILE,
                    likely_cause="The provider did not return a terminal result.",
                    confidence=1.0,
                )

            return cls(
                status=PaymentStatus.UNKNOWN,
                category=DiagnosisCategory.UNKNOWN,
                recommended_action=RecommendedAction.ESCALATE_TO_HUMAN,
                confidence=0.2,
            )

        if payment.status == PaymentStatus.FAILED:
            decline_reason_codes = {
                event.reason_code
                for event in payment.events
                if event.event_type == "provider.declined"
            }  # noqa: E501
            if (
                "provider.declined" in event_types
                and "AUTH_DECLINED" in decline_reason_codes
            ):
                return cls(
                    status=PaymentStatus.FAILED,
                    category=DiagnosisCategory.AUTHORIZATION_FAILURE,
                    recommended_action=RecommendedAction.ESCALATE_TO_PROVIDER,
                    likely_cause="The provider rejected payment authorization.",
                    confidence=0.8,
                )
            return cls(
                status=PaymentStatus.UNKNOWN,
                category=DiagnosisCategory.UNKNOWN,
                recommended_action=RecommendedAction.ESCALATE_TO_HUMAN,
                confidence=0.2,
            )

        return cls(
            status=PaymentStatus.UNKNOWN,
            category=DiagnosisCategory.UNKNOWN,
            recommended_action=RecommendedAction.ESCALATE_TO_HUMAN,
            confidence=0.2,
        )
