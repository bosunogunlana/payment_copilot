# Week 2 Phase 5 — Selection and recovery evaluation

## Batch and ownership

Freeze selection cases, collect normalized first model turns, score first-tool
selection, and save recovery evidence. Reuse the existing loop, registry, gateway
and executor. The assistant owns dataset, scoring and acceptance scaffolding;
the learner owns the model adapter and application integration.

Target timebox: 60–90 minutes, excluding model experiment troubleshooting.
Do not change expected labels after seeing results; record ambiguous labels and
version the dataset before a new run. Version 1 has 40 synthetic cases, ten per
tool, all using existing org-a/pay-shared fixtures and provider simulator.
This small explicit-request dataset measures routing, not general incident diagnosis.

## Learner batch: normalized model adapter

Suggested core file: `app/llm/tool_model.py`.
Implement `ToolModel.__call__(*, messages, tools) -> object`, matching `LoopModel`.
Inject the transport/client and model configuration. Keep model I/O separate from
`ToolLoop`; the loop still validates and executes. Supply concise tool descriptions
that distinguish internal payment state, event history, ledger postings and
provider-side status. Save the actual instruction text as the prompt artifact.

Data flow:

1. Evaluator reads a case and passes only its question plus the frozen instructions
   and tool schemas to the model. Never expose expected_tool/expected_arguments.
2. Adapter translates normalized messages/tools into the provider request format.
3. Adapter normalizes tool calls to call_id, name and arguments_json; text-only
   replies normalize to an empty tool_calls list plus final_text.
4. Collector saves the FIRST turn with the case ID. Selection measurement does not
   require executing a payment read or asking for a final answer.
5. Separately exercise the existing gateway and recovery executor with deterministic
   failures, then retain outcomes and traces in the report.

Do not put org identity or operation keys under model control. Context is for
application execution, separate from model arguments. Refusal, incomplete output
and missing responses must remain misses; do not manufacture a valid tool call.
Use the existing client's error-handling conventions and bounded request timeout.

Prediction JSONL shape (one row per attempted case):

```json
{"case_id":"tool-001","turn":{"tool_calls":[{"call_id":"call-001","name":"get_payment","arguments_json":"{\"payment_id\":\"pay-shared\"}"}]}}
```

Save normalized response artifacts for every attempted case, including failed
turns as null with an optional error field. The scorer ignores metadata fields.
Freeze model ID, prompt, dataset and tool schema versions. Save usage, latency
and experiment configuration separately; the offline scorer cannot verify
prediction provenance or calculate model spend. A scripted run tests plumbing
and must be labelled scripted, even if every expected answer matches.

## Scoring and commands

From the project root:

```sh
../.venv/bin/python -m unittest discover -s tests -p test_tool_selection_eval.py -v
../.venv/bin/python -m unittest discover -s tests -p test_tool_recovery.py -v
../.venv/bin/python -m unittest discover -s tests -p test_fixture_tools.py -v
../.venv/bin/python -m unittest discover -s tests -p test_tool_loop.py -v
../.venv/bin/python -m unittest discover -s tests -q
```

After collecting genuine model predictions and saving the actual prompt:

```sh
../.venv/bin/python -m evals.score_tool_selection \
  --predictions evals/reports/week2-selection-predictions.jsonl \
  --run-kind model --model MODEL_ID \
  --prompt-file PATH_TO_ACTUAL_PROMPT \
  --output evals/reports/week2-selection-results.json
```

This command performs no requests. Missing, invalid, unknown-tool and text-only
turns count against the full 40-case denominator. First call alone determines
first selection. Argument validity/exact agreement is reported separately.
36/40 meets the 90% selection threshold. Unknown/duplicate prediction IDs are
input errors rather than silently overwriting results. Hashes identify dataset,
prompt and saved predictions. Only a genuine model run can establish quality;
`--run-kind model` is a provenance declaration, not independent proof.

No paid requests are authorized by this build. Set a Phase 5 experiment allowance
and request/output bounds before collecting live predictions; the previous smoke
allowance does not cover this experiment.

## Recovery acceptance evidence

Reuse the existing assertions; do not create an alternative retry implementation.
Save exact commands and observed results in week2-error-recovery.md.

| Failure / behavior | Existing acceptance boundary | Evidence to retain |
| --- | --- | --- |
| Malformed arguments, unknown tool, denied access | test_tool_contracts.py | Fixed code, false retryability, rejected trace, no reader call |
| Payment not found, invalid provider, malformed/empty evidence | test_fixture_tools.py | Typed error, failed trace; empty lists remain valid success |
| Timeout, synthetic 500, exhaustion, shrinking budgets | test_tool_recovery.py | Final code/flag, stop reason, attempts, allotted timeout, duration, backoff |
| Revocation during retry | test_tool_recovery.py | Second authorization denied; no second read |
| Known late success | test_tool_recovery.py | Success despite overrun; one attempt, no sleep |
| Reader error classification | GatewayRetryClassificationTest | Safe code allowlist and explicit false preserved |
| Replayed call ID versus fresh read | test_tool_loop.py | Replayed ID stops; new ID executes and reauthorizes |
| Commit followed by lost receipt/timeout | FakeEffectReplayTest | Two attempts, one scoped effect, original receipt |
| Changed payload / other organization / mutated receipts | FakeEffectReplayTest | Conflict, independent namespace, snapshot integrity |

## Exit gate and stop boundary

Save at least 36/40 genuine first selections, every miss, argument results and
provenance; reviewed failure outcomes and traces; and a lifecycle drawing from
memory. Include request -> model call -> validation -> authorization -> execution
-> typed result -> correlated model message -> stop, with bounded recovery inside
execution. The assistant does not supply the learner's from-memory drawing.

Record cooperative timeout and serial in-memory deduplication limitations. Keep
Phase 1–4 passing. Do not advance to Phase 6 or mark browser checkpoints from
scaffolding alone.

## Adapter acceptance seam

`tests/test_tool_model.py` now targets a concrete `ToolModel`, replacing the
placeholder Protocol in `app/llm/tool_model.py`. `LoopModel` already defines the
consumer protocol. The proposed constructor takes client, model, instructions,
request_timeout_s, max_output_tokens and observe, all by keyword.

These tests use a synthetic `client.request(payload=...)` seam, not a claim about
an SDK wire format. Payload keys are model, instructions, timeout_s,
max_output_tokens, messages and tools. Messages preserve the existing normalized
conversation and call IDs; tools retain name/parameters and gain a nonblank
description. A provider-specific client wrapper translates this envelope into
its SDK format. Do not mistake this test seam for a live API contract.

The fake client returns a dictionary with status, tool_calls, output_text,
refusal and usage. Tool-call fields are id, name and arguments (the original JSON
string). The adapter emits call_id, name and arguments_json. Completed calls take
precedence over incidental text. Refusal or a noncompleted status discards both.
Malformed envelopes return None; malformed argument JSON and unknown names remain
intact for the existing gateway to reject.

The observation callback receives status, duration_ms and usage on a completed
request. Expected TimeoutError/ConnectionError yields None and one observation
with status transport_error; no internal retry. Unexpected programming errors
propagate. Provider-specific expected exceptions must be translated by the client
wrapper. Inputs and provider responses must not be mutated.

Run the new learner-owned acceptance slice:

```sh
../.venv/bin/python -m unittest discover -s tests -p test_tool_model.py -v
```

## Provider package

Provider code lives in `app/clients/`: `base.py` contains OpenAIClientBase,
Models and create_openai_client; `openai_transport.py` implements diagnosis
transport; `openai_tool_client.py` holds the tool-client skeleton. Both adapters
inherit SDK injection from the base. The caller owns and closes the SDK client;
passing the same instance shares it, while separate instances remain independent.
ToolModel and ToolLoop stay under `app/llm/`. The tool wrapper's request method
and provider translation remain to be implemented.

Provider implementation batch: [OpenAI tool-client build brief](WEEK-02-OPENAI-TOOL-CLIENT-BUILD.md), including mocked-SDK acceptance tests and exact field mappings.

## Shared request typing and observations

`app/clients/contracts.py` defines the provider-neutral ToolRequest TypedDict and
ProviderClient protocol. ToolModel builds this request and OpenAIToolClient
accepts it; required fields use explicit indexing. Tool descriptions must exist
for every configured tool before a provider request is sent.

Observation status retains the provider status; outcome distinguishes
valid_response, invalid_response, refusal, noncompleted_response and
transport_error. Malformed completed envelopes therefore retain their provider
status without counting as valid normalized turns. Every handled result emits
one observation; available usage remains attached even when normalization fails.

## Collector usage (Phase 5)

`evals/collect_tool_selection.py` now owns case iteration, first-turn collection,
per-case metadata, progress on stderr, and a run manifest. `ToolModel` makes one
request per case; no ToolLoop or gateway is invoked. Model inputs contain only
questions, frozen instructions and tool definitions, never labels or context.
The prompt is `evals/prompts/tool_selection_v1.txt`.

Zero-request plan, safe without credentials:

```sh
../.venv/bin/python -m evals.collect_tool_selection
../.venv/bin/python -m unittest discover -s tests -p test_collect_tool_selection.py -v
```

After explicitly allocating Phase 5 spend, select conservative per-request
reservations against the chosen model's current pricing and these bounded inputs.
Set PHASE5_BUDGET_USD and PHASE5_RESERVE_USD to that allocation/reservation first.
The following is a command template, not authorization to execute paid requests:

```sh
../.venv/bin/python -m evals.collect_tool_selection --live \
  --acknowledge-spend --model gpt-6-luna \
  --budget-usd "$PHASE5_BUDGET_USD" --reserve-usd "$PHASE5_RESERVE_USD" \
  --timeout-s 20 --max-output-tokens 512 \
  --output evals/reports/week2-selection-predictions.jsonl
```

Requests reserve budget before execution; reservations are never reclaimed.
Missing/invalid usage or a transport error preserves the attempted row and stops
further requests. Remaining cases are written as skipped with null turns, so
scoring keeps the full denominator. Refusal/incomplete/invalid turns with valid
usage remain misses while collection continues. Unexpected defects abort loudly;
previous rows are flushed and the run manifest records aborted status. A short
budget can deliberately produce a partial experiment, not a full quality claim.

This is conservative local reservation accounting, not a provider billing cap.
The collector does not calculate actual dollar cost or validate reservations
against pricing. Token counts are saved; calculate estimates using verified rates
in the report. A request may incur a charge even when its usage is unavailable.

Existing output or manifest paths are rejected. Predictions stream to JSONL;
the companion `.jsonl.run.json` includes model, instructions, schemas, tool
descriptions, dataset/prompt/schema/code hashes, SDK version, limits, reservations,
summary, UTC timestamps and the completed predictions hash. Record the actual
provider model/version if it differs from the requested alias; current metadata
identifies the requested model only. Mocked collector tests are scaffolding
verification, never model quality evidence.

Score the saved results offline:

```sh
../.venv/bin/python -m evals.score_tool_selection \
  --predictions evals/reports/week2-selection-predictions.jsonl \
  --run-kind model --model gpt-6-luna \
  --prompt-file evals/prompts/tool_selection_v1.txt \
  --output evals/reports/week2-selection-results.json
```

Use the same model/prompt recorded in the manifest. Keep the run manifest beside
the scorer report; the scorer's run-kind flag is a declaration, not independent
provenance verification. Finish recovery evidence and the learner's lifecycle
drawing before requesting phase closeout.
