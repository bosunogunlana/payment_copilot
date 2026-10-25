# Week 2 local handoff — Function calling and tool design

Run commands from the project root (`payment_copilot/`). This slice provides four
read-only fixture tools, a manual tool loop, a two-layer OpenAI tool adapter,
bounded standalone recovery and an in-memory fake-effect replay demonstration.

## Setup

The verified interpreter is Python 3.13.2 with openai 3.5.0 and pydantic 2.13.4.
The code uses Python 3.12+ type aliases; use the verified 3.13 environment here.

For a new checkout:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export COPILOT_PYTHON="$PWD/.venv/bin/python"
```

For this workspace's existing environment instead:

```sh
export COPILOT_PYTHON="$PWD/../.venv/bin/python"
```

Direct dependencies are pinned, transitive dependencies are not locked. The
verification below reuses the existing environment; a fresh dependency install
has not been verified. No credentials are required for the offline commands.

## Reproduce offline

```sh
"$COPILOT_PYTHON" -m unittest discover -s tests -q
"$COPILOT_PYTHON" -m evals.collect_tool_selection
"$COPILOT_PYTHON" -m evals.recovery_evidence \
  --output /tmp/week2-recovery-local.json
"$COPILOT_PYTHON" -m evals.score_tool_selection \
  --predictions evals/reports/week2-selection-predictions-02.jsonl \
  --run-kind model --model gpt-6-luna \
  --prompt-file evals/prompts/tool_selection_v1.txt \
  --output /tmp/week2-selection-local.json
```

Recovery output is exclusive: choose another filename if it already exists.
The scorer works offline against saved predictions; declaring run-kind model
identifies the saved run and does not make a model request. It writes its output
path, so use a scratch path to preserve saved evidence.

Expected working-source results: 165 tests pass; collector reports 40 cases and
zero requests; recovery passes 17/17 scenarios; saved first selections score
38/40 (95%), with 38 correct tool-and-argument pairs. Routine reruns do not require
another paid experiment or identical gateway microsecond timings.

## Evidence and boundaries

| Artifact | Purpose |
| --- | --- |
| [Learning note](learning-notes/week2.md) | Learner lifecycle diagram and explanation |
| [Selection/recovery report](../evals/reports/week2-error-recovery.md) | Observed metrics, misses, failure table and limitations |
| [Selection predictions](../evals/reports/week2-selection-predictions-02.jsonl) | Complete 40-case run |
| [Run manifest](../evals/reports/week2-selection-predictions-02.jsonl.run.json) | Prompt, schemas, model, code hashes, token counts and reservations |
| [Recovery traces](../evals/reports/week2-recovery-traces-02.json) | 17 scripted outcomes, attempts, authorization counts and fake receipts |
| [Source-copy verification](../evals/reports/week2-local-verification.json) | Committed HEAD versus working source checks |
| [Evaluation contract](WEEK-02-EVALUATION-CONTRACT.md) | Interfaces, live-run flags and experiment accounting |

Model requests are untrusted. The gateway validates arguments and invokes the
application authorization function with TrustedContext before fixture access.
Tool call IDs correlate results; replayed IDs stop while new IDs may intentionally
read fresh evidence. Recovery traces use a fake clock for budgets and real
perf_counter timings inside gateway/loop code.

ToolLoop currently invokes the gateway directly; RetryExecutor is demonstrated
separately through the same gateway boundary. Full live reasoning-model
continuation is not yet verified because the loop does not retain all provider
continuation items. Final loop text is not a structured DiagnosisResult, and
automatic evidence-to-diagnosis assembly is not implemented.

## Deliberate failure and measured tradeoff

The selection run met the 90% gate at 38/40. Both misses concern provider status;
one requests the right tool second. Schema-valid calls can seek the wrong evidence,
so first-selection accuracy is separate from successful parsing and final text.
The dataset consists of explicit synthetic requests and does not establish broad
incident-diagnosis quality or repeatability. Preserve these misses before changing
the prompt; version any follow-up dataset or experiment.

The fake replay commits an effect before returning TIMEOUT, then retries the same
organization-scoped operation key. Two attempts produce one effect and the original
receipt. This illustrates deduplication after an ambiguous result, without claiming
durable, concurrent or cross-process exactly-once behavior.

Deadlines stop additional work, but cannot forcibly cancel arbitrary blocking
Python. A known successful result is preserved even after an allotted timeout.
Authorization is rechecked on retries. These choices preserve known outcomes and
access boundaries while keeping the simulator deterministic.

The complete selection run records mean latency 0.968s and 13,047 input / 1,155
output tokens. Its $2 reserved allocation is local accounting, not measured cost.
No new paid requests were made during handoff verification.


