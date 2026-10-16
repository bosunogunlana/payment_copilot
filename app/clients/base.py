"""Shared OpenAI SDK dependency and construction defaults.

The caller owns the SDK client lifecycle. Adapters may share the same injected
client; they neither construct nor close it implicitly.
"""

from enum import StrEnum

from openai import OpenAI


class Models(StrEnum):
    CHEAP = "gpt-6-luna"
    DEFAULT = "gpt-6-luna"
    STRONG = "gpt-6.1-sol"


def create_openai_client(*, api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, timeout=20.0, max_retries=0)


class OpenAIClientBase:
    """Hold the injected SDK client without owning its lifecycle."""

    def __init__(self, *, client: OpenAI) -> None:
        self.client = client
