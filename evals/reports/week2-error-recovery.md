# Week 2 — Tool selection and recovery

Status: Selection gate verified; recovery trace artifacts and learner lifecycle drawing remain open.

## Selection experiment

Reviewed 2026-10-16. Model requested: gpt-6-luna. Dataset version 1 contains
40 synthetic direct evidence requests, ten per tool. This is a routing evaluation,
not a diagnosis-quality or full multi-turn provider evaluation.

| Metric | Complete run 02 |
| --- | --- |
| Attempted / total | 40 / 40 |
| Correct first tool | 38 / 40 (95%) |
| Correct first tool and arguments | 38 / 40 |
| Valid normalized turns | 40 / 40 |
| Skipped / transport failures | 0 / 0 |
| Mean request + normalization latency | 0.968 s |
| Input / output tokens | 13,047 / 1,155 |
| Local reserved allocation | $2.00 (40 × $0.05) |
| Actual dollar cost | Not calculated; reservations are not charges |

Artifacts: week2-selection-predictions-02.jsonl, its .run.json manifest, and
week2-selection-results-02.json. Dataset, prompt and prediction hashes match the
manifest; all four recorded code hashes match current source. SDK version 3.5.0;
20s request timeout, 512 output-token cap, strict=False. Run timestamps:
2026-10-16T08:33:18.328263+00:00 to 2026-10-16T08:33:57.097875+00:00.
Requested alias is recorded; resolved provider model version is not retained.

Scoring command:

```sh
../.venv/bin/python -m evals.score_tool_selection \
  --predictions evals/reports/week2-selection-predictions-02.jsonl \
  --run-kind model --model gpt-6-luna \
  --prompt-file evals/prompts/tool_selection_v1.txt \
  --output evals/reports/week2-selection-results-02.json
```

### Misses

- tool-038: “Which status does provider simulator assign to payment pay-shared?”
  Expected get_provider_status; selected get_payment_events.
- tool-039: “Look up payment pay-shared at provider simulator.” Expected
  get_provider_status; requested get_payment first and get_provider_status second.
  The correct second call does not satisfy first-tool selection.

Per-tool first-selection results: get_payment 10/10, get_payment_events 10/10,
get_ledger_entries 10/10, get_provider_status 8/10. The two first calls have
valid arguments for their selected tools but do not match the expected tool and
arguments. A schema-valid request can still seek the wrong evidence.

The initial run reserved $5 per request against a $5 allocation, so it attempted
one case (correct) and skipped 39. It is a budget-control observation, not a full
quality evaluation. Preserve its original predictions and manifest separately.
No additional model requests were made during review.

## Recovery evidence

Review command: ../.venv/bin/python -m unittest discover -s tests -q.
Observed 160 passing tests on 2026-10-16, including deterministic gateway,
recovery, repeated-call and fake replay assertions. Saved representative recovery
traces and per-failure outcome table remain pending; selection predictions do not
execute tools or prove recovery behavior.

## Lifecycle drawing from memory

Learner drawing and explanation: pending.

## Engineering note

First-tool routing meets the required 90% threshold on this small synthetic
sample. Provider status remains the weakest distinction; preserve the misses
before changing descriptions or instructions and version any follow-up experiment.
One run does not measure repeatability. Retry deadlines are cooperative; known
success survives time overruns. Idempotency evidence covers serial in-memory fake
effects, without durable/concurrent or live-provider guarantees.
