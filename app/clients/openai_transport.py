"""OpenAI structured-output transport for the payment diagnosis adapter."""

from copy import deepcopy
from typing import Any

from openai import APIError, APITimeoutError, OpenAI

from app.clients.base import Models, OpenAIClientBase


class OpenAITransport(OpenAIClientBase):
    """Send diagnosis requests and normalize provider responses.

    DiagnosisAdapter supplies the prompt, payment input and diagnosis schema.
    This transport prepares the schema and extracts output text; parsing and
    validating the resulting diagnosis remain the adapter's responsibility.

    The injected SDK client controls network timeouts and SDK retries. This
    class adds no retry loop and does not close the client. It handles diagnosis
    structured output; tool-call conversations use OpenAIToolClient instead.
    """

    def __init__(
        self, *, client: OpenAI, model: str = Models.DEFAULT, max_output_tokens: int
    ) -> None:
        """Configure the injected client, model and positive output-token limit.

        Raises:
            ValueError: If max_output_tokens is nonpositive.
        """
        if max_output_tokens <= 0:
            raise ValueError("max_output_token must be positive.")

        self.max_output_tokens = max_output_tokens
        super().__init__(client=client)
        self.model = model

    def __call__(self, payload: dict[str, Any]) -> object:
        """Make one SDK request and return the normalized diagnosis envelope.

        Args:
            payload: Application-owned mapping containing system_instruction,
                input_json and output_schema. The schema must describe the
                diagnosis object, including its likely_cause property. A deep
                copy is adapted for strict output without mutating the input:
                all properties are required, extra properties are forbidden,
                and likely_cause loses its default while retaining nullability.

        Returns:
            A mapping with status, refusal, output_json and usage. output_json
            contains concatenated text, not a parsed JSON object, or None when
            absent. Refusals and incomplete responses discard output text.
            usage contains input_tokens/output_tokens, or None if unavailable.

        Raises:
            TimeoutError: The SDK request timed out.
            ConnectionError: The SDK raised another APIError, or the returned
                status was neither completed nor incomplete.

        Invalid payloads and unexpected programming errors propagate. Response
        extraction runs outside the API exception handler so internal defects
        are not classified as request failures.
        """
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

        usage = getattr(response, "usage", None)
        usage_json = {"input_tokens": None, "output_tokens": None}
        if usage is not None:
            usage_json["input_tokens"] = usage.input_tokens
            usage_json["output_tokens"] = usage.output_tokens
        else:
            usage_json = None

        if response.status == "incomplete":
            return {
                "status": "incomplete",
                "refusal": None,
                "output_json": None,
                "usage": usage_json,
            }

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
                        "usage": usage_json,
                    }

                if content.type == "output_text":
                    text_parts.append(content.text)
        return {
            "status": "completed",
            "refusal": None,
            "output_json": "".join(text_parts) or None,
            "usage": usage_json,
        }
