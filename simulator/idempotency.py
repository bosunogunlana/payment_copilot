"""Serial, in-memory idempotency demonstration; performs no external actions."""

import json
from copy import deepcopy

from app.tools.errors import ToolError, ToolReadError


class FakeEffectStore:
    """Keep one synthetic receipt per organization-scoped operation key.

    State lasts for this instance only. This is not durable or thread-safe.
    """

    def __init__(self) -> None:
        self._effects: dict[
            tuple[str, str], tuple[str, dict[str, object]]
        ] = {}

    @property
    def effect_count(self) -> int:
        return len(self._effects)

    def apply(
        self,
        *,
        organization_id: str,
        operation_key: str,
        payload: dict[str, object],
    ) -> dict[str, object]:
        for name, value in (
            ("organization_id", organization_id),
            ("operation_key", operation_key),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonblank string")
        if not isinstance(payload, dict):
            raise ValueError("payload must be a JSON object")

        snapshot = deepcopy(payload)
        fingerprint = json.dumps(
            snapshot, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
        key = (organization_id, operation_key)
        previous = self._effects.get(key)

        if previous is not None:
            previous_fingerprint, receipt = previous
            if fingerprint != previous_fingerprint:
                raise ToolReadError(
                    ToolError(
                        code="IDEMPOTENCY_CONFLICT",
                        retryable=False,
                        message="Operation key was already used with a different payload.",
                    )
                )
            return deepcopy(receipt)

        receipt: dict[str, object] = {
            "receipt_id": f"fake-effect-{self.effect_count + 1}",
            "organization_id": organization_id,
            "operation_key": operation_key,
            "payload": snapshot,
        }
        self._effects[key] = (fingerprint, receipt)
        return deepcopy(receipt)
