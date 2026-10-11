import json
from pathlib import Path
from typing import NoReturn

from pydantic import ValidationError

from app.models.diagnosis import Payment, PaymentEvent
from app.models.evidence import LedgerEntry, ProviderStatus, ToolEvidence
from app.tools.contracts import BaseToolArgument, GetProviderStatusArgument
from app.tools.errors import ToolError, ToolReadError


class FixtureReader:
    def __init__(self, path: Path) -> None:
        self.data = json.loads(path.read_text(encoding="utf-8"))

    def __call__(
        self, *, tool_name: str, organization_id: str, arguments: BaseToolArgument
    ) -> ToolEvidence:
        records = [
            record
            for record in self.data["records"]
            if record["organization_id"] == organization_id
            and record["payment_id"] == arguments.payment_id
        ]

        if not records:
            raise ToolReadError(
                ToolError(code="PAYMENT_NOT_FOUND", message="Payment not found")
            )

        if len(records) != 1:
            self._malformed_response()

        record = records[0]

        if tool_name == "get_provider_status":
            if not isinstance(arguments, GetProviderStatusArgument):
                self._malformed_response()

            if arguments.provider_id != "simulator":
                raise ToolReadError(
                    ToolError(code="INVALID_PROVIDER", message="Unsupported provider")
                )

        try:
            if tool_name == "get_payment":
                payload = record["payment"]
                if payload is None:
                    self._empty_response()

                payment = Payment.model_validate(payload)
                if not self._matches_identity(
                    payment, organization_id, arguments.payment_id
                ):
                    self._malformed_response()

                return payment

            if tool_name == "get_payment_events":
                payload = record["events"]
                if not isinstance(payload, list):
                    self._malformed_response()

                events = [PaymentEvent.model_validate(event) for event in payload]
                return events

            if tool_name == "get_ledger_entries":
                payload = record["ledger_entries"]
                if not isinstance(payload, list):
                    self._malformed_response()

                entries = [LedgerEntry.model_validate(entry) for entry in payload]
                if any(
                    not self._matches_identity(
                        entry, organization_id, arguments.payment_id
                    )
                    for entry in entries
                ):
                    self._malformed_response()

                return entries

            if tool_name == "get_provider_status":
                if not isinstance(arguments, GetProviderStatusArgument):
                    self._malformed_response()

                payload = record["provider_status"]
                if payload is None:
                    self._empty_response()

                status = ProviderStatus.model_validate(payload)
                if (
                    not self._matches_identity(
                        status, organization_id, arguments.payment_id
                    )
                    or status.provider_id != arguments.provider_id
                ):
                    self._malformed_response()

                return status
        except (KeyError, ValidationError):
            raise ToolReadError(
                ToolError(
                    code="MALFORMED_RESPONSE", message="Invalid evidence response"
                )
            ) from None

        raise ToolReadError(ToolError(code="UNKNOWN_TOOL", message="Unknown tool."))

    @staticmethod
    def _matches_identity(
        value: Payment | LedgerEntry | ProviderStatus,
        organization_id: str,
        payment_id: str,
    ) -> bool:
        return (
            value.organization_id == organization_id and value.payment_id == payment_id
        )

    @staticmethod
    def _malformed_response() -> NoReturn:
        raise ToolReadError(
            ToolError(code="MALFORMED_RESPONSE", message="Invalid evidence response")
        )

    @staticmethod
    def _empty_response() -> NoReturn:
        raise ToolReadError(
            ToolError(code="EMPTY_RESPONSE", message="Evidence response is absent")
        )
