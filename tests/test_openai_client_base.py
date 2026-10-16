"""Provider adapters share injection without sharing application behavior."""

import unittest
from unittest.mock import Mock

from app.clients.base import OpenAIClientBase
from app.clients.openai_tool_client import OpenAIToolClient
from app.clients.openai_transport import OpenAITransport


class OpenAIClientBaseTest(unittest.TestCase):
    def test_adapters_can_share_one_sdk_client_without_owning_its_lifecycle(self):
        sdk = Mock()
        diagnosis = OpenAITransport(client=sdk, max_output_tokens=512)
        tools = OpenAIToolClient(client=sdk)
        for adapter in (diagnosis, tools):
            with self.subTest(adapter=type(adapter).__name__):
                self.assertIsInstance(adapter, OpenAIClientBase)
                self.assertIs(adapter.client, sdk)
        sdk.close.assert_not_called()

    def test_independent_clients_are_not_replaced_by_global_shared_state(self):
        first, second = Mock(), Mock()
        self.assertIs(OpenAIToolClient(client=first).client, first)
        self.assertIs(OpenAIToolClient(client=second).client, second)
