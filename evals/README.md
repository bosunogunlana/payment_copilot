# Evaluations

Synthetic datasets, offline checks and saved model experiments for the Payment
Reliability Copilot. Run commands from the project root (`payment_copilot/`).

Use your installed Python environment. For the existing workspace:

```sh
export COPILOT_PYTHON="$PWD/../.venv/bin/python"
```

For a project-local environment, use `$PWD/.venv/bin/python` instead. Setup and
dependency limitations are in the [Week 1 guide](../docs/WEEK-01-LOCAL-GUIDE.md)
and [Week 2 guide](../docs/WEEK-02-LOCAL-GUIDE.md).

## Week 1 — Payment diagnosis

Week 1 includes a deterministic diagnosis baseline, an independent LLM diagnosis
adapter, a 30-case labelled dataset and a paired Luna/Sol comparison. The
baseline is a reference for behavior validation; it does not run inside the LLM
adapter. Both paths return validated diagnosis data without executing payments.

Run offline checks and zero-request plans:

```sh
"$COPILOT_PYTHON" -m evals.diagnose_fixture --case-id case-001
"$COPILOT_PYTHON" -m evals.smoke_diagnosis
"$COPILOT_PYTHON" -m evals.compare_diagnosis
```

The reviewed comparison 02 used the revised prompt, identical 30-case inputs,
interleaved model requests and a 2048-output-token limit for both configurations.

| Metric | Luna | Sol |
| --- | --- | --- |
| Label matches | 30/30 | 30/30 |
| Schema-valid | 30/30 | 30/30 |
| Unsafe unknown outcomes | 0 | 0 |
| Mean latency | 1.85 s | 2.27 s |
| Estimated total cost | $0.00361 | $0.06313 |

Decision: retain Luna for this bounded slice. Sol cost about 17.5 times more
without an observed quality gain. These are historical estimates for 30 requests
per model, not current pricing or invoice totals. Confidence remains uncalibrated;
causal explanations require grounding review. One synthetic run does not establish
statistical significance or production reliability.

Evidence:

- [Dataset and labeling policy](datasets/README.md)
- [Week 1 summary](reports/week1-summary.md)
- [Comparison 02](reports/week1-comparison-02.json) and [review](reports/week1-comparison-02-review.md)
- [Configuration and recorded rates](configs/week1.json)

The original comparison and review remain available as experiment history.
Reports include per-case outcomes, skipped cases, category/tag summaries, usage,
latency and provenance. Compare paired attempted cases; unmatched budget-stop
results are coverage information, not a fair model comparison.

## Week 2 — Tool selection and recovery

Week 2 measures first-tool selection over 40 frozen synthetic questions and
exercises application recovery separately with scripted failures. The collector
uses ToolModel and OpenAIToolClient for one model turn per question. It does not
execute tools or evaluate final answers. Expected labels are hidden from the model.

| Metric | Reviewed result |
| --- | --- |
| Correct first tool | 38/40 (95%) |
| Correct first tool and arguments | 38/40 |
| Valid normalized responses | 40/40 |
| Skipped cases | 0 |
| Mean latency | 0.968 s |
| Input / output tokens | 13,047 / 1,155 |
| Offline recovery scenarios | 17/17 pass |

Both selection misses concern provider status. One requests the correct tool
second, which still misses the first-selection criterion. The $2 reserved for the
complete run is local allocation accounting, not actual model cost.

Preview collection and reproduce saved selection/recovery evidence offline:

```sh
"$COPILOT_PYTHON" -m evals.collect_tool_selection
"$COPILOT_PYTHON" -m evals.score_tool_selection \
  --predictions evals/reports/week2-selection-predictions-02.jsonl \
  --run-kind model --model gpt-6-luna \
  --prompt-file evals/prompts/tool_selection_v1.txt \
  --output /tmp/week2-selection-local.json
"$COPILOT_PYTHON" -m evals.recovery_evidence \
  --output /tmp/week2-recovery-local.json
```

Choose a new recovery output path if it exists. The scorer writes its output path;
use a scratch path to preserve reviewed reports. `--run-kind model` identifies the
saved predictions' declared provenance; scoring itself makes no requests.

Evidence:

- [Selection dataset](datasets/tool_selection.jsonl) and [frozen prompt](prompts/tool_selection_v1.txt)
- [Complete predictions](reports/week2-selection-predictions-02.jsonl), [manifest](reports/week2-selection-predictions-02.jsonl.run.json) and [scores](reports/week2-selection-results-02.json)
- [Selection and recovery report](reports/week2-error-recovery.md)
- [Recovery traces](reports/week2-recovery-traces-02.json)
- [Lifecycle learning note](../docs/learning-notes/week2.md)
- [Local handoff and source verification](../docs/WEEK-02-LOCAL-GUIDE.md)

The first selection run attempted one case and skipped 39 because its per-request
reservation equaled its total budget. It remains saved as budget-control evidence;
run 02 is the complete quality evaluation. Recovery uses the actual gateway, loop,
retry executor and fake effect store, with scripted inputs and a fake clock.

Recovery is currently exercised separately from ToolLoop. Timeouts are cooperative,
idempotency is serial and in-memory, and full live reasoning-model continuation
is not verified. Phase 5 evaluation is complete; Phase 6 packaging verification
is tracked separately. These results do not establish production readiness.

## New live experiments

Offline commands above need no API key or spending allowance. New paid runs need
OPENAI_API_KEY in the shell, a deliberate experiment allocation and conservative
per-request limits. Refresh prices before choosing reservations or estimating cost.

- Diagnosis smoke: `evals.smoke_diagnosis --live --max-output-tokens 512 --acknowledge-spend`.
- Diagnosis comparison: `evals.compare_diagnosis --live --budget-usd ... --reserve-usd ... --output NEW_PATH`.
- Tool selection: `evals.collect_tool_selection --live --acknowledge-spend --budget-usd ... --reserve-usd ... --output NEW_PATH`.

Invoke these modules with your chosen Python's `-m` option. Use `--help` for model,
timeout and output-token options supported by each runner. No automatic resume or
replay of paid requests is performed. Keep existing artifacts and use new output
paths for new runs.

Comparison and collection reserve funds before each request and never reclaim
unused reservations. Missing usage is unknown spend, not zero cost; it stops
subsequent requests. Reservations are local accounting, not a provider billing
cap. A prior smoke allowance does not automatically authorize a new experiment.
