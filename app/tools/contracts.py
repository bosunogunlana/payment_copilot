from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.tools.errors import ToolError

MODEL_CONFIG = ConfigDict(
    extra="forbid",
    strict=True,
    str_strip_whitespace=True
)

class BaseToolArgument(BaseModel):
    payment_id: str = Field(min_length=1)
    
    model_config = MODEL_CONFIG

class GetPaymentArgument(BaseToolArgument):
    pass

class GetPaymentEventsArgument(BaseToolArgument):
    pass

class GetLedgerEntriesArgument(BaseToolArgument):
    pass

class GetProviderStatusArgument(BaseToolArgument):
    provider_id: str = Field(min_length=1)


TOOL_ARGUMENT_MODELS = {
    "get_payment": GetPaymentArgument,
    "get_payment_events": GetPaymentEventsArgument,
    "get_ledger_entries": GetLedgerEntriesArgument,
    "get_provider_status": GetProviderStatusArgument   
}

class TrustedContext(BaseModel):
    organization_id: str = Field(min_length=1)
    request_id: str = Field(min_length=1)

    model_config = MODEL_CONFIG

class ToolTraceOutcome(StrEnum):
    SUCCEEDED = "succeeded"
    REJECTED = "rejected"

class ToolTrace(BaseModel):
    organization_id: str = Field(min_length=1)
    request_id: str = Field(min_length=1)
    tool_name: str = Field(min_length=1)
    payment_id: str | None = None
    outcome: ToolTraceOutcome
    error_code: str | None = None
    attempt: int = Field(ge=1)
    duration_ms: float = Field(ge=0, allow_inf_nan=False)
    

class ToolResult(BaseModel):
    data: object | None
    error: ToolError | None
    trace: ToolTrace

    @model_validator(mode="after")
    def validate_exclusive_outcome(self) -> Self:
        if (self.data is None) == (self.error is None):
            raise ValueError("Exactly one of data or error must be populated")
        return self