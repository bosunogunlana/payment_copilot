"""OpenAI tool-call adapter"""

from copy import deepcopy
from typing import cast

from openai import APIError, APITimeoutError
from openai.types.responses import FunctionToolParam, ResponseInputParam

from app.clients.base import OpenAIClientBase
from app.clients.contracts import ToolRequest


class OpenAIToolClient(OpenAIClientBase):
    """Translate tool-model envelopes into OpenAI requests and back.

    Uses the injected SDK client without owning its lifecycle. Expected SDK
    failures become built-in transport errors; tool execution stays with the gateway.
    """

    def request(self, *, payload: ToolRequest) -> object:
        translated_message = self._translate_messages(payload["messages"])
        translated_tools = self._translate_tools(payload["tools"])

        try:
            response = self.client.responses.create(
                model=payload["model"],
                tools=translated_tools,
                input=cast(ResponseInputParam, translated_message),
                instructions=payload["instructions"],
                timeout=payload["timeout_s"],
                max_output_tokens=payload["max_output_tokens"],
                include=["reasoning.encrypted_content"],
                store=False,
            )
        except APITimeoutError as exc:
            raise TimeoutError("Model request timed out.") from exc
        except APIError as exc:
            raise ConnectionError("Model request failed") from exc

        usage = getattr(response, "usage", None)
        usage_json = {}
        if usage is not None:
            usage_json["input_tokens"] = usage.input_tokens
            usage_json["output_tokens"] = usage.output_tokens
        else:
            usage_json = None

        if response.status != "completed":
            return {
                "status": response.status,
                "tool_calls": [],
                "output_text": None,
                "refusal": None,
                "usage": usage_json,
            }

        tool_calls = []
        text_parts: list[str] = []
        for item in response.output:
            if item.type not in {"function_call", "message"}:
                continue

            if item.type == "message":
                for content in item.content:
                    if content.type == "refusal":
                        return {
                            "status": "completed",
                            "refusal": content.refusal,
                            "output_text": None,
                            "usage": usage_json,
                            "tool_calls": [],
                        }

                    if content.type == "output_text":
                        text_parts.append(content.text)

            if item.type == "function_call":
                tool_calls.append(
                    {
                        "arguments": item.arguments,
                        "id": item.call_id,
                        "name": item.name,
                    }
                )

        output_items = [
            item.model_dump(mode="json", exclude_none=True) for item in response.output
        ]

        return {
            "status": "completed",
            "tool_calls": tool_calls,
            "output_text": "".join(text_parts) or None,
            "refusal": None,
            "usage": usage_json,
            "provider_state": {
                "provider": "openai.provider",
                "output_items": output_items,
            },
        }

    @staticmethod
    def _translate_messages(
        messages: list[dict[str, object]],
    ) -> list[dict[str, object]]:
        translated: list[dict[str, object]] = []

        for message in messages:
            role = message.get("role")
            calls = message.get("tool_calls")
            state = message.get("provider_state")
            if role == "assistant" and state is not None:
                if not isinstance(state, dict):
                    raise ValueError("Continuation state must be an object")

                if state["provider"] != "openai.provider":
                    raise ValueError("Unsupported continuation provider")

                translated.extend(deepcopy(state["output_items"]))
                continue

            if role == "assistant" and calls:
                if not isinstance(calls, list):
                    raise ValueError("tool_calls must be a list")

                for call in calls:
                    if not isinstance(call, dict):
                        raise ValueError("Each tool call must be a dict")

                    translated.append(
                        {
                            "type": "function_call",
                            "call_id": call["call_id"],
                            "name": call["name"],
                            "arguments": call["arguments_json"],
                        }
                    )
            elif role == "tool":
                translated.append(
                    {
                        "type": "function_call_output",
                        "call_id": message["call_id"],
                        "output": message["content"],
                    }
                )
            elif role in {"user", "assistant"}:
                translated.append(
                    {
                        "role": role,
                        "content": message["content"],
                    }
                )
            else:
                raise ValueError(f"Unsupported message role: {role!r}")

        return translated

    @staticmethod
    def _translate_tools(
        tools: list[dict[str, object]],
    ) -> list[FunctionToolParam]:

        translated_tools: list[FunctionToolParam] = []
        for tool in tools:
            name = tool.get("name")
            description = tool.get("description")
            parameters = tool.get("parameters")

            if not isinstance(name, str):
                raise ValueError("Tool name must be a string")
            if not isinstance(description, str):
                raise ValueError("Tool description must be a string")
            if not isinstance(parameters, dict):
                raise ValueError("Tool parameters must be an object")

            translated_tools.append(
                FunctionToolParam(
                    type="function",
                    name=name,
                    description=description,
                    parameters=parameters,
                    strict=False,
                )
            )

        return translated_tools
