"""OpenAI tool-call adapter"""

from typing import TypedDict

from openai import APIError, APITimeoutError

from app.clients.base import OpenAIClientBase


class Payload(TypedDict):
    model: str
    instructions: str
    timeout_s: float
    max_output_tokens: int
    messages: list[dict[str, object]]
    tools: list[dict[str, object]]


class OpenAIToolClient(OpenAIClientBase):
    """Share SDK injection; implement ProviderClient.request next."""

    def request(self, *, payload: Payload) -> object:
        translated_message = self._translate_messages(payload.get("messages"))
        translated_tools = self._translate_tools(payload.get("tools"))

        try:
            response = self.client.responses.create(
                model=payload.get("model"),
                tools=translated_tools,
                input=translated_message,
                instructions=payload.get("instructions"),
                timeout=payload.get("timeout_s"),
                max_output_tokens=payload.get("max_output_tokens"),
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

        return {
            "status": "completed",
            "tool_calls": tool_calls,
            "output_text": "".join(text_parts) or None,
            "refusal": None,
            "usage": usage_json,
        }

    @staticmethod
    def _translate_messages(
        messages: list[dict[str, object]],
    ) -> list[dict[str, object]]:
        translated: list[dict[str, object]] = []

        for message in messages:
            role = message.get("role")
            calls = message.get("tool_calls")
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
    ) -> list[dict[str, object]]:
        # Add descriptions and translate schemas into provider format.

        translated_tools = []
        for tool in tools:
            name = tool.get("name")
            description = tool.get("description")
            parameters = tool.get("parameters")

            translated_tools.append(
                {
                    "type": "function",
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                    "strict": False,
                }
            )

        return translated_tools
