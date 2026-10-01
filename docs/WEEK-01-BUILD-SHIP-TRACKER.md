# Week 1 Build / Ship Tracker

Use this file to track evidence for the phased build. Check a box only when the artifact, test, trace, or note exists. The browser curriculum tracker remains the source of truth for course progress; this file is a working companion for the implementation slice.

## Current status

- Overall status: In progress
- Current phase: Phase 1
- Last evidence update: 2026-10-01
- Main blocker: Phase 1 boundary coverage still needs explicit missing-identifier and invalid-diagnosis-enum tests.
- Next action: Add those two boundary cases, then re-run the model-boundary tests.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase checklist

### Phase 1 — Diagnosis contract

- [x] Define the typed payment input.
- [x] Define the typed diagnosis output.
- [x] Add validation tests for invalid input and output.
- [x] Create the first five synthetic cases.
- [x] Record the passing test command.

Evidence / notes:

```text
Status: In progress
Files or links: app/models/diagnosis.py; tests/test_diagnosis.py; evals/datasets/week1.jsonl
What this proves: The typed payment/diagnosis boundary, validation cases, five starter scenarios, and a passing `python -m unittest discover -s tests -v` run with 9 tests.
Open question: Add explicit tests for missing identifiers and invalid diagnosis enum values before advancing to Phase 2.
```

### Phase 2 — Deterministic baseline

- [ ] Diagnose a successful payment.
- [ ] Diagnose a pending/provider-timeout payment.
- [ ] Diagnose a failed/declined payment.
- [ ] Fail closed when events are missing.
- [ ] Fail closed when evidence conflicts.
- [ ] Reuse the same `Diagnosis` schema.

Evidence / notes:

```text
Status:
Files or links:
What this proves:
Open question:
```

### Phase 3 — LLM adapter

- [ ] Add the narrow diagnosis adapter.
- [ ] Send a bounded payment and event payload.
- [ ] Request structured output.
- [ ] Validate successful output with the application model.
- [ ] Handle refusal and incomplete output.
- [ ] Handle malformed output and API failure.
- [ ] Exercise the adapter with a stubbed response.
- [ ] Confirm credentials are outside source control.

Evidence / notes:

```text
Status:
Files or links:
What this proves:
Open question:
```

### Phase 4 — Failure dataset

- [ ] Expand `evals/datasets/week1.jsonl` to at least 30 cases.
- [ ] Include missing-event cases.
- [ ] Include conflicting-signal cases.
- [ ] Include plausible-but-wrong-cause cases.
- [ ] Include insufficient-evidence and escalation cases.
- [ ] Give every case a stable ID and machine-checkable expected outcome.
- [ ] Confirm that all data is synthetic.

Evidence / notes:

```text
Status:
Dataset count:
Case IDs reviewed:
What this proves:
Open question:
```

### Phase 5 — Comparison and measurement

- [ ] Name configuration A.
- [ ] Name configuration B.
- [ ] Run both against the same cases.
- [ ] Record schema validity.
- [ ] Record correctness or acceptable-label match.
- [ ] Record confidence.
- [ ] Record latency.
- [ ] Record tokens when available.
- [ ] Record estimated cost.
- [ ] Group failures by category.
- [ ] Record the spending limit and skipped cases.

Evidence / notes:

```text
Status:
Report location:
Decision:
What this proves:
Open question:
```

### Phase 6 — Local ship

- [ ] Document the one-command diagnosis path.
- [ ] Run the tests from a clean checkout.
- [ ] Load the dataset from a clean checkout.
- [ ] Write `docs/learning-notes/week1.md`.
- [ ] Explain the primitive and its boundary.
- [ ] Explain one deliberate failure.
- [ ] Include measurements and a trade-off.
- [ ] Record limitations and the next smallest action.

Evidence / notes:

```text
Status:
Commands:
Files or links:
What this proves:
Open question:
```

## Deliverable inventory

| Deliverable | Phase | Status | Evidence |
| --- | --- | --- | --- |
| `app/models/diagnosis.py` | 1–2 | Not started | — |
| `app/llm/diagnose.py` | 3 | Not started | — |
| `evals/datasets/week1.jsonl` | 1, 2, 4 | Not started | — |
| `docs/learning-notes/week1.md` | 6 | Not started | — |

## Failure coverage matrix

| Failure case | Represented in dataset | Test/eval run | Result or note |
| --- | --- | --- | --- |
| Missing events | [ ] | [ ] | — |
| Conflicting signals | [ ] | [ ] | — |
| Plausible but wrong cause | [ ] | [ ] | — |
| Refusal | [ ] | [ ] | — |
| Incomplete response | [ ] | [ ] | — |
| Malformed structured output | [ ] | [ ] | — |
| Insufficient evidence | [ ] | [ ] | — |

## Session log

| Date | Phase | Timebox | Completed | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| 2026-10-01 | Phase 1 | — | Test command passes | 9 unittest cases passed | Add missing-identifier and invalid-enum boundary tests |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## Definition of done

The Week 1 build/ship segment is complete when all of these are true:

- [ ] The four curriculum deliverables exist.
- [ ] The test command passes from a clean run.
- [ ] At least 30 labelled synthetic scenarios are stored.
- [ ] The diagnosis path handles success, uncertainty, and failure explicitly.
- [ ] Two model configurations have been compared on the same cases.
- [ ] Validity, confidence, latency, tokens, and cost are recorded.
- [ ] The learning note explains what failed and what the measurements changed.
- [ ] No production integration or real-money action is implied by the result.
