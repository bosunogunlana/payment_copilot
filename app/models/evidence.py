from datetime import datetime

from pydantic import BaseModel, Field

from app.models.diagnosis import Payment, PaymentEvent, PaymentStatus


class LedgerEntry(BaseModel):
    entry_id: str = Field(min_length=1)
    organization_id: str = Field(min_length=1)
    payment_id: str = Field(min_length=1)
    amount_minor: int = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")
    posted_at: datetime


class ProviderStatus(BaseModel):
    provider_id: str = Field(min_length=1)
    organization_id: str = Field(min_length=1)
    payment_id: str = Field(min_length=1)
    status: PaymentStatus


type ToolEvidence = Payment | list[PaymentEvent] | list[LedgerEntry] | ProviderStatus
