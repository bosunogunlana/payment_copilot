import json
import time
from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel, Field, ValidationError

from app.tools.contracts import TOOL_ARGUMENT_MODELS, ToolResult, TrustedContext
from app.tools.gateway import ToolGateway


class LoopStatus(StrEnum):
    COMPLETED = "completed"
    TOOL_LIMIT = "tool_limit"
    MODEL_LIMIT = "model_limit"
    REPEATED_CALL = "repeated_call"
    INVALID_MODEL_RESPONSE = "invalid_model_response"


class ToolRepetition(StrEnum):
    FIRST_READ = "first_read"
    FRESH_READ = "fresh_read"


class LoopTrace(BaseModel):
    call_id: str
    tool_name: str
    arguments: dict[str, object] | None
    repetition: ToolRepetition
    duration_ms: float = Field(ge=0, allow_inf_nan=False)
    result: ToolResult


class LoopResult(BaseModel):
    status: LoopStatus
    final_text: str | None
    steps: int = Field(ge=0)
    model_turns: int = Field(ge=0)
    trace: list[LoopTrace]


class LoopModel(Protocol):
    def __call__(
        self, *, messages: list[dict[str, object]], tools: list[dict[str, object]]
    ) -> object: ...


class ToolLoop:
    def __init__(
        self,
        model: LoopModel,
        gateway: ToolGateway,
        max_tool_steps: int = 8,
        max_model_turns: int = 8,
    ) -> None:
        if type(max_tool_steps) is not int or max_tool_steps <= 0:
            raise ValueError("Invalid max_tool_steps")

        if type(max_model_turns) is not int or max_model_turns <= 0:
            raise ValueError("Invalid max_model_turns")

        self.model = model
        self.gateway = gateway
        self.max_tool_steps = max_tool_steps
        self.max_model_turns = max_model_turns

    def run(self, question: str, context: TrustedContext) -> LoopResult:
        messages: list[dict[str, object]] = [{"role": "user", "content": question}]
        tools: list[dict[str, object]] = [
            {"name": name, "parameters": model.model_json_schema()}
            for name, model in TOOL_ARGUMENT_MODELS.items()
        ]
        traces: list[LoopTrace] = []
        steps = 0
        model_turns = 0

        def stop(status: LoopStatus) -> LoopResult:
            return LoopResult(
                status=status,
                final_text=None,
                steps=steps,
                model_turns=model_turns,
                trace=traces,
            )

        seen_call_ids: set[str] = set()
        seen_reads: set[tuple[str, str]] = set()

        while model_turns < self.max_model_turns:
            turn = self.model(messages=messages, tools=tools)
            model_turns += 1

            parsed_turn = self.parse_turn(turn)
            if parsed_turn is None:
                return stop(LoopStatus.INVALID_MODEL_RESPONSE)

            tool_calls, final_text = parsed_turn

            if final_text is not None:
                return LoopResult(
                    status=LoopStatus.COMPLETED,
                    final_text=final_text,
                    steps=steps,
                    model_turns=model_turns,
                    trace=traces,
                )

            messages.append({"role": "assistant", "tool_calls": tool_calls})

            for item in tool_calls:
                if steps >= self.max_tool_steps:
                    return stop(LoopStatus.TOOL_LIMIT)

                call_id = item["call_id"]
                tool_name = item["name"]

                if call_id in seen_call_ids:
                    return stop(LoopStatus.REPEATED_CALL)

                seen_call_ids.add(call_id)
                started_at = time.perf_counter()

                try:
                    raw_arguments = json.loads(item["arguments_json"])
                except json.JSONDecodeError:
                    raw_arguments = None

                result = self.gateway.execute(
                    tool_name=tool_name,
                    arguments=raw_arguments,
                    context=context,
                )

                steps += 1
                safe_arguments = self.validated_argument(
                    tool_name=tool_name, raw_arguments=raw_arguments
                )

                repetition = ToolRepetition.FIRST_READ

                if safe_arguments is not None:
                    read_key = (
                        tool_name,
                        json.dumps(
                            safe_arguments,
                            sort_keys=True,
                            separators=(",", ":"),
                        ),
                    )

                    if read_key in seen_reads:
                        repetition = ToolRepetition.FRESH_READ

                    seen_reads.add(read_key)

                traces.append(
                    LoopTrace(
                        call_id=call_id,
                        tool_name=tool_name,
                        arguments=safe_arguments,
                        repetition=repetition,
                        duration_ms=(time.perf_counter() - started_at) * 1000,
                        result=result,
                    )
                )

                messages.append(
                    {
                        "role": "tool",
                        "call_id": call_id,
                        "content": result.model_dump_json(),
                    }
                )

        return stop(LoopStatus.MODEL_LIMIT)

    @staticmethod
    def parse_turn(turn: object) -> tuple[list[dict[str, str]], str | None] | None:
        if not isinstance(turn, dict):
            return None

        calls = turn.get("tool_calls")
        text = turn.get("final_text")

        if not isinstance(calls, list):
            return None

        if not calls:
            if isinstance(text, str) and text.strip():
                return [], text
            return None

        if text is not None:
            return None

        validated_calls: list[dict[str, str]] = []
        batch_ids: set[str] = set()

        for item in calls:
            if not isinstance(item, dict):
                return None

            call_id = item.get("call_id")
            tool_name = item.get("name")
            arguments_json = item.get("arguments_json")

            if (
                not isinstance(call_id, str)
                or not call_id.strip()
                or not isinstance(tool_name, str)
                or not tool_name.strip()
                or not isinstance(arguments_json, str)
            ):
                return None

            if call_id in batch_ids:
                return None

            batch_ids.add(call_id)
            validated_calls.append(
                {"call_id": call_id, "name": tool_name, "arguments_json": arguments_json}
            )

        return validated_calls, None

    @staticmethod
    def validated_argument(
        tool_name: str,
        raw_arguments: object,
    ) -> dict[str, object] | None:
        argument_model = TOOL_ARGUMENT_MODELS.get(tool_name)

        if argument_model is None:
            return None

        try:
            parsed_argument = argument_model.model_validate(raw_arguments)
        except ValidationError:
            return None

        return parsed_argument.model_dump(mode="json")
