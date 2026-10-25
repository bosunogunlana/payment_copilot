# Week 2 — Tool selection and recovery

Status: Phase 5 complete; selection, offline recovery evidence and learner lifecycle note reviewed.

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

Executed 2026-10-17 against existing application boundaries. All 17 scripted
scenarios pass. The full suite passes 165 tests. No model/provider requests,
real sleeps or external effects are used in this evidence run.

Artifact: [week2-recovery-traces-02.json](week2-recovery-traces-02.json).
Refreshed offline on 2026-10-18 after runner-source changes; 17/17 cases pass.
The original run 01 is retained as historical evidence.
Includes per-attempt typed errors, retryability, allotted budgets, timings,
backoff, authorization/read counts, loop traces, receipts and source/fixture hashes.

```sh
../.venv/bin/python -m evals.recovery_evidence \
  --output evals/reports/week2-recovery-traces-01.json
../.venv/bin/python -m unittest discover -s tests -q
```

Existing outputs are protected; choose a new suffix when rerunning.

| Scenario | Final error | Retryable | Attempts / steps | Stop | Checks |
| --- | --- | --- | --- | --- | --- |
| unknown_tool | UNKNOWN_TOOL | false | 1 | nonretryable | Pass |
| invalid_arguments | INVALID_ARGUMENTS | false | 1 | nonretryable | Pass |
| unauthorized | UNAUTHORIZED | false | 1 | nonretryable | Pass |
| payment_not_found | PAYMENT_NOT_FOUND | false | 1 | nonretryable | Pass |
| invalid_provider | INVALID_PROVIDER | false | 1 | nonretryable | Pass |
| malformed_response | MALFORMED_RESPONSE | false | 1 | nonretryable | Pass |
| empty_object | EMPTY_RESPONSE | false | 1 | nonretryable | Pass |
| empty_list_success | — | — | 1 | success | Pass |
| timeout_recovery | — | — | 2 | success | Pass |
| server_error_recovery | — | — | 2 | success | Pass |
| attempt_exhaustion | TIMEOUT | true | 3 | max_attempts | Pass |
| deadline | TIMEOUT | true | 2 | deadline | Pass |
| authorization_revoked | UNAUTHORIZED | false | 2 | nonretryable | Pass |
| late_success | — | — | 1 | success | Pass |
| replayed_call_id | — | — | 1 | repeated_call | Pass |
| fresh_read | — | — | 2 | completed | Pass |
| commit_then_timeout | — | — | 2 | success | Pass |

Recovered timeout and 500 cases retain their retryable failures in the first
attempt even though the final result succeeds. Deadline budgets shrink from
1.0s to 0.25s. Revocation runs authorization twice but reads once. Replayed call
IDs stop after one read; fresh IDs perform two authorized reads. Fake effect
replay takes two attempts, creates one effect and returns the original receipt;
changed payload raises a nonretryable conflict.

Recovery uses a fake clock, while nested gateway/loop timings use perf_counter.
Timeouts remain cooperative; deduplication remains serial and in-memory.
These observations do not establish live-provider or full multi-turn model behavior.

## Lifecycle drawing from memory

Reviewed 2026-10-18: [Week 2 learning note](../../docs/learning-notes/week2.md) contains the lifecycle diagram and explanation of model/tool limits, correlated results, provider authentication, application authorization with trusted identity, and the separate bounded-recovery path.

## Engineering note

First-tool routing meets the required 90% threshold on this small synthetic
sample. Provider status remains the weakest distinction; preserve the misses
before changing descriptions or instructions and version any follow-up experiment.
One run does not measure repeatability. Retry deadlines are cooperative; known
success survives time overruns. Idempotency evidence covers serial in-memory fake
effects, without durable/concurrent or live-provider guarantees.
