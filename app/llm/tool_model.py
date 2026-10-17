import math
import time
from collections.abc import Callable
from typing import TypedDict

from app.clients.base import Models
from app.clients.contracts import ProviderClient, ToolRequest


class ToolCall(TypedDict):
    call_id: str
    name: str
    arguments_json: str


class ToolTurn(TypedDict):
    tool_calls: list[ToolCall]


class TextTurn(TypedDict):
    tool_calls: list[ToolCall]
    final_text: str


type ModelTurn = ToolTurn | TextTurn


class ToolModel:
    TOOL_DESCRIPTIONS = {
        "get_payment": "Read the internal payment record, amount, currency and status.",
        "get_payment_events": "Read payment lifecycle events, timestamps and reason codes.",
        "get_ledger_entries": "Read accounting entries posted for a payment.",
        "get_provider_status": "Read a provider's reported payment status.",
    }

    def __init__(
        self,
        *,
        client: ProviderClient,
        model: str = Models.DEFAULT,
        instructions: str,
        request_timeout_s: float,
        max_output_tokens: int,
        observe: Callable[[dict[str, object]], None],
    ) -> None:
        if (
            type(request_timeout_s) is not float
            or request_timeout_s <= 0
            or not math.isfinite(request_timeout_s)
        ):
            raise ValueError("invalid request_timeout_s")

        if type(max_output_tokens) is not int or max_output_tokens <= 0:
            raise ValueError("invalid max_output_tokens")

        self.client = client
        self.model = model
        self.instructions = instructions
        self.request_timeout_s = request_timeout_s
        self.max_output_tokens = max_output_tokens
        self.observe = observe

    def __call__(
        self, *, messages: list[dict[str, object]], tools: list[dict[str, object]]
    ) -> ModelTurn | None:
        payload = self._build_request(messages=messages, tools=tools)
        started_at = time.perf_counter()

        try:
            response = self.client.request(payload=payload)
        except (TimeoutError, ConnectionError):
            self.observe(
                {
                    "status": "transport_error",
                    "outcome": "transport_error",
                    "duration_ms": (time.perf_counter() - started_at) * 1000,
                    "usage": None,
                }
            )
            return None

        turn = self._normalize_response(response=response)
        status = response.get("status") if isinstance(response, dict) else None
        usage = response.get("usage") if isinstance(response, dict) else None
        if turn is not None:
            outcome = "valid_response"
        elif isinstance(response, dict) and response.get("refusal") is not None:
            outcome = "refusal"
        elif status is not None and status != "completed":
            outcome = "noncompleted_response"
        else:
            outcome = "invalid_response"

        self.observe(
            {
                "status": status,
                "outcome": outcome,
                "duration_ms": (time.perf_counter() - started_at) * 1000,
                "usage": usage,
            }
        )
        return turn

    def _build_request(
        self, *, messages: list[dict[str, object]], tools: list[dict[str, object]]
    ) -> ToolRequest:
        described_tools: list[dict[str, object]] = []
        for tool in tools:
            name = tool["name"]
            if not isinstance(name, str):
                raise ValueError("Tool name must be a string")
            described_tools.append({
                **tool,
                "description": self.TOOL_DESCRIPTIONS[name],
            })

        return {
            "model": self.model,
            "instructions": self.instructions,
            "timeout_s": self.request_timeout_s,
            "max_output_tokens": self.max_output_tokens,
            "messages": messages,
            "tools": described_tools,
        }

    @staticmethod
    def _normalize_response(response: object) -> ModelTurn | None:
        # Reject refusal/incomplete responses before extracting calls.
        # Preserve call IDs, tool names, and argument JSON unchanged.
        # Return None when no valid normalized turn is available.
        if not isinstance(response, dict):
            return None

        if response.get("status") != "completed":
            return None

        if response.get("refusal") is not None:
            return None

        tool_calls = response.get("tool_calls")
        if not isinstance(tool_calls, list):
            return None

        parsed_tool_calls: list[ToolCall] = []
        for tool_call in tool_calls:
            if not isinstance(tool_call, dict):
                return None

            call_id = tool_call.get("id")
            name = tool_call.get("name")
            arguments = tool_call.get("arguments")

            if not isinstance(call_id, str) or not call_id.strip():
                return None
            if not isinstance(name, str) or not name.strip():
                return None
            if not isinstance(arguments, str):
                return None

            parsed_tool_calls.append(
                ToolCall(
                    call_id=call_id,
                    name=name,
                    arguments_json=arguments,
                )
            )

        if parsed_tool_calls:
            return ToolTurn(tool_calls=parsed_tool_calls)

        text = response.get("output_text")
        if isinstance(text, str) and text.strip():
            return TextTurn(tool_calls=[], final_text=text)

        return None
