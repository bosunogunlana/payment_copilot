# Week 1 Build / Ship Tracker

Use this file to track evidence for the phased build. Check a box only when the artifact, test, trace, or note exists. The browser curriculum tracker remains the source of truth for course progress; this file is a working companion for the implementation slice.

## Current status

- Overall status: In progress
- Current phase: Phase 2
- Last evidence update: 2026-10-01
- Main blocker: Decline classification ignores the new reason_code field; defensive fallback confidence is 0.5 rather than below 0.5. Dataset serialization evidence remains incomplete.
- Next action: Align defensive fallback confidence with the existing uncertain outcomes; then test structured AUTH_DECLINED reason-code mapping and generic-decline uncertainty.

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
Status: Done
Files or links: app/models/diagnosis.py; tests/test_diagnosis.py; evals/datasets/week1.jsonl
What this proves: Typed payment and diagnosis boundaries; explicit missing-identifier and invalid-enum rejection; all 11 tests pass via `../.venv/bin/python -m unittest discover -s tests -v`. All five unique synthetic JSONL cases parse as Payment and their expected labels match the enums.
Open question: None for the Phase 1 exit gate. Next phase: deterministic baseline; review cause inference against event evidence.
```

### Phase 2 — Deterministic baseline

- [x] Diagnose a successful payment.
- [x] Diagnose a pending/provider-timeout payment.
- [x] Diagnose a failed/declined payment.
- [x] Fail closed when events are missing.
- [x] Fail closed when evidence conflicts.
- [ ] Reuse the same `Diagnosis` schema.

Evidence / notes:

```text
Status: In progress
Files or links: app/models/diagnosis.py; tests/test_diagnosis.py
What this proves: All 14 unittest cases pass via `../.venv/bin/python -m unittest discover -s tests -v`. Unknown payment with payment.created now returns unknown/escalation, no likely cause, and confidence 0.2. Defensive fallback now preserves unknown status. Timeout and decline explanations are present; formatting and cls construction remain sound.
Open question: Defensive fallback confidence is 0.5 (not below 0.5), decline confidence is 0.1 without documented semantics, and reason_code is accepted but ignored by classification. Dataset-driven schema serialization evidence still needed. Phase 2 remains In progress.
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
| `app/models/diagnosis.py` | 1–2 | In progress | Phase 1 contract verified; Phase 2 baseline still under review |
| `app/llm/diagnose.py` | 3 | Not started | — |
| `evals/datasets/week1.jsonl` | 1, 2, 4 | In progress | Five unique labelled synthetic inputs parse; expected enums validated |
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
| 2026-10-01 | Phase 1 | Review | Exit gate verified; Phase 1 Done | 11 tests passed; five unique labelled fixtures validated | Phase 2: pending-without-timeout negative case |
| 2026-10-01 | Phase 2 | Review | Pending evidence guard verified | All 12 tests pass; failed-without-decline defect reproduced | Add failed-payment negative test; keep Phase 2 open |
| 2026-10-01 | Phase 2 | Review | Failed-payment evidence guard verified; Python formatting reviewed | All 13 tests pass; explicit decline behavior preserved | Define confidence semantics; align unknown/fallback outcomes |
| 2026-10-01 | Phase 2 | Review | Unknown-state uncertainty verified | All 14 tests pass; unknown confidence 0.2 and cause None | Align fallback confidence; test structured decline reason codes |

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
