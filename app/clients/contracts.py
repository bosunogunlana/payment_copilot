"""Provider-neutral request contract shared by tool models and clients."""

from typing import Protocol, TypedDict


class ToolRequest(TypedDict):
    model: str
    instructions: str
    timeout_s: float
    max_output_tokens: int
    messages: list[dict[str, object]]
    tools: list[dict[str, object]]


class ProviderClient(Protocol):
    def request(self, *, payload: ToolRequest) -> object: ...

class ProviderState(TypedDict):
    provider: str
    output_items: list[dict[str, object]]