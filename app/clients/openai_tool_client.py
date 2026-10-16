"""OpenAI tool-call adapter"""

from app.clients.base import OpenAIClientBase


class OpenAIToolClient(OpenAIClientBase):
    """Share SDK injection; implement ProviderClient.request next."""
