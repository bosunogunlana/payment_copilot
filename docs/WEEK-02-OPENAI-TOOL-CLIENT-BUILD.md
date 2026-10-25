# Phase 5 batch — OpenAI tool client

Goal: implement the provider layer needed to collect real first-tool selections.
Timebox: 60–90 minutes. Core remains learner-owned. Acceptance scaffolding:
`tests/test_openai_tool_client.py`; no API requests are made by these tests.

## Files and structure

- `app/clients/openai_tool_client.py`: concrete OpenAIToolClient, inheriting SDK
  injection from OpenAIClientBase. No extra constructor is required.
- `app/llm/tool_model.py`: existing application envelope and normalized-turn
  policy. Remove its unused translation stubs; translation lives below.
- `tests/test_openai_tool_client.py`: eleven mocked-SDK methods, including
  composition with ToolModel and original argument preservation.

Implement this structure, with complete annotations as you narrow SDK inputs:

```python
class OpenAIToolClient(OpenAIClientBase):
    def request(self, *, payload: dict[str, object]) -> object: ...

    @staticmethod
    def _translate_messages(
        messages: list[dict[str, object]],
    ) -> list[dict[str, object]]: ...

    @staticmethod
    def _translate_tools(
        tools: list[dict[str, object]],
    ) -> list[dict[str, object]]: ...

    @staticmethod
    def _extract_response(response: object) -> dict[str, object]: ...
```

The helper names are guidance; tests exercise the public request boundary.

## Input and output contract

Input keys: model (str), instructions (str), timeout_s (positive finite number),
max_output_tokens (positive int), messages (normalized conversation list),
tools (name, description, parameters). These are trusted application inputs;
invalid configuration may fail explicitly before sending a request. Type narrowing
or typed payload definitions are preferable to scattering unchecked casts.

Output always has status, tool_calls, output_text, refusal and usage. Example:

```json
{"status":"completed","tool_calls":[{"id":"call-001","name":"get_payment","arguments":"{broken"}],"output_text":null,"refusal":null,"usage":{"input_tokens":12,"output_tokens":8}}
```

The intermediate id field contains the SDK function item's call_id, NOT item.id.
Keep unknown tool names and malformed JSON strings unchanged. The gateway retains
execution authority; this wrapper neither parses tool arguments nor executes tools.

## Algorithm and mapping

1. Translate messages and tools before the SDK try block. Preserve input objects.
2. Invoke self.client.responses.create exactly once with model, instructions,
   input=translated messages, tools=translated definitions, timeout=timeout_s,
   max_output_tokens and store=False.
3. Catch APITimeoutError as TimeoutError, then other APIError as ConnectionError,
   preserving the cause. Do not add a retry loop; factory disables SDK retries.
4. Extract the returned status and usage outside that try. Missing usage -> None.
5. Noncompleted status: return the envelope with no calls or text, retaining
   status and usage. Completed status: inspect output items for refusals first;
   any refusal discards all calls/text regardless of item order.
6. Otherwise collect every function_call in order and concatenate output_text
   content from message items. Empty text -> None. Do not lose usage on refusal.

| Normalized input | SDK input |
| --- | --- |
| user role/content | user role/content |
| assistant tool_calls | one function_call item per call, with call_id/name/arguments |
| tool call_id/content | function_call_output with call_id/output |
| ordinary assistant text | assistant role/content |
| tool name/description/parameters | type=function plus those fields and strict=False |

Strict False is explicit to preserve existing argument schemas. Enabling strict
mode later requires a deliberate schema conversion, separate from this batch.

Official provider reference:
https://developers.openai.com/api/docs/guides/function-calling

## Acceptance and commands

Tests cover exact SDK request arguments, correlation IDs, multiple calls, text,
missing usage, refusal order, incomplete/failed responses, exception mapping,
unexpected defects, immutability and composition with ToolModel.

```sh
../.venv/bin/python -m unittest discover -s tests -p test_openai_tool_client.py -v
../.venv/bin/python -m unittest discover -s tests -p test_tool_model.py -v
../.venv/bin/python -m unittest discover -s tests -q
```

The new provider tests are expected to fail until request is implemented.

## Stop boundary

First-turn selection collection is the immediate objective. Basic normalized
message translation is covered; full live reasoning-model continuation is not:
provider reasoning items are not retained by the current loop contract. Do not
claim complete multi-turn provider support or hide conversation state in a shared
client. Define explicit conversation-scoped continuation before that integration.

This batch makes no paid calls. Live collection still needs an experiment budget,
request/output bounds and saved provenance. Preserve the 40-case dataset and
scorer. Diagnosis evidence assembly and Phase 6 packaging stay outside this batch.
