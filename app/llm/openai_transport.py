from copy import deepcopy
from enum import StrEnum
from typing import Any

from openai import APIError, APITimeoutError, OpenAI


class Models(StrEnum):
    CHEAP = "gpt-6-luna"
    DEFAULT = "gpt-6-luna"
    STRONG = "gpt-6.1-sol"


def create_openai_client(*, api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, timeout=20.0, max_retries=0)


class OpenAITransport:
    def __init__(
        self, *, client, model: str = Models.DEFAULT, max_output_tokens: int
    ) -> None:
        if max_output_tokens <= 0:
            raise ValueError("max_output_token must be positive.")

        self.max_output_tokens = max_output_tokens
        self.client = client
        self.model = model

    def __call__(self, payload: dict[str, Any]) -> object:
        schema = deepcopy(payload["output_schema"])
        schema["additionalProperties"] = False
        schema["required"] = list(schema["properties"])
        schema["properties"]["likely_cause"].pop("default", None)

        text_format = {
            "format": {
                "type": "json_schema",
                "name": "payment_diagnosis",
                "strict": True,
                "schema": schema,
            }
        }

        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=payload["system_instruction"],
                input=payload["input_json"],
                max_output_tokens=self.max_output_tokens,
                text=text_format,
                store=False,
            )
        except APITimeoutError as exc:
            raise TimeoutError("Diagnosis request timed out.") from exc
        except APIError as exc:
            raise ConnectionError("Diagnosis request failed") from exc

        if response.status == "incomplete":
            return {"status": "incomplete", "refusal": None, "output_json": None}

        if response.status != "completed":
            raise ConnectionError("Diagnosis response did not complete")

        text_parts: list[str] = []

        for item in response.output:
            if item.type != "message":
                continue

            for content in item.content:
                if content.type == "refusal":
                    return {
                        "status": "completed",
                        "refusal": content.refusal,
                        "output_json": None,
                    }

                if content.type == "output_text":
                    text_parts.append(content.text)

        return {
            "status": "completed",
            "refusal": None,
            "output_json": "".join(text_parts) or None,
        }
