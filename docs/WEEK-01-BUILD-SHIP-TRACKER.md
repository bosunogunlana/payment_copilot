# Week 1 Build / Ship Tracker

Use this file to track evidence for the phased build. Check a box only when the artifact, test, trace, or note exists. The browser curriculum tracker remains the source of truth for course progress; this file is a working companion for the implementation slice.

## Current status

- Overall status: In progress
- Current phase: Phase 3
- Last evidence update: 2026-10-02
- Main blocker: No test blocker remains; credential placement and the smoke-run spending allowance remain unverified.
- Next action: Record credential placement and the spending allowance before closing Phase 3; live success and all 37 passing tests are recorded.

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
- [x] Reuse the same `Diagnosis` schema.

Evidence / notes:

```text
Status: Done
Files or links: app/models/diagnosis.py; tests/test_diagnosis.py; evals/datasets/week1.jsonl; docs/decisions/week1-baseline-conventions.md
What this proves: All 17 unittest cases pass via `../.venv/bin/python -m unittest discover -s tests -v`. Recognized outcomes have explanations and confidence above 0.5; tested uncertain outcomes have confidence below 0.5 and escalate. Structured decline codes are bound to the decline event. Persistent fixture coverage matches all five expected outcomes and verifies Diagnosis JSON round-trips. Baseline confidence semantics and limitations are documented.
Open question: None for the bounded Phase 2 exit gate. Nonblocking style: wrap the decline_reason_codes comprehension, remove its redundant event-type membership check, and remove trailing whitespace. Next phase: Phase 3 LLM adapter.
```

### Phase 3 — LLM adapter

- [x] Add the narrow diagnosis adapter.
- [x] Send a bounded payment and event payload.
- [x] Request structured output.
- [x] Validate successful output with the application model.
- [x] Handle refusal and incomplete output.
- [x] Handle malformed output and API failure.
- [x] Exercise the adapter with a stubbed response.
- [ ] Confirm credentials are outside source control.

Evidence / notes:

```text
Status: In progress
Files or links: app/llm/diagnose.py; app/llm/openai_transport.py; tests/test_llm_diagnose.py; tests/test_openai_transport.py; evals/smoke_diagnosis.py
What this proves: Assistant executed `../.venv/bin/python -m unittest discover -s tests -v`: all 37 tests pass in 0.021s, including the stdout regression. Transport strict-schema construction, refusal/incomplete handling, SDK failure mapping, timeout, and disabled retries are verified offline. User-provided live command `python -m evals.smoke_diagnosis --live --max-output-tokens 512 --acknowledge-spend` returned a validated succeeded/successful_payment/no_action diagnosis with confidence 0.99 and error null. Live evidence is user-provided, not independently rerun; it covers one synthetic case only.
Open question: Credential placement and smoke-run spending allowance remain unverified. Output token limits and spending acknowledgement are not a hard dollar cap. No additional paid request was made for this verification.
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
| `app/models/diagnosis.py` | 1–2 | Done | Phase 1–2 bounded gates verified; 17 baseline tests pass |
| `app/llm/diagnose.py` | 3 | In progress | Offline boundary verified with 28 passing tests; provider wiring remains |
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
| 2026-10-01 | Phase 2 | Review | Structured decline guard and fixture schema reuse verified | 16 tests pass; all five fixture labels and JSON round-trips pass | Finish confidence documentation, success explanation, and regression coverage in one batch |
| 2026-10-01 | Phase 2 | Review | Phase 2 exit gate verified; conventions documented | 17 tests pass, persistent five-fixture comparisons and JSON round-trips | Phase 3: adapter contract and stubbed responses |
| 2026-10-02 | Phase 3 | Review | Offline adapter reviewed; boundary regressions added | Original 25 tests pass; expanded 27 methods produce 3 failures and 3 errors | Fix envelope guards, result exclusivity, and error serialization in one batch |
| 2026-10-02 | Phase 3 | Review | Offline boundary fixes verified; invalid-limit regression added | All 28 tests pass; Ruff unavailable in project venv | Finish Phase 3 provider transport and controlled smoke-run setup |
| 2026-10-02 | Phase 3 | Review | Provider transport and smoke runner reviewed | Original 36 tests pass; new stdout regression fails; dry-run makes zero requests | Remove debug prints and record controlled smoke evidence |
| 2026-10-02 | Phase 3 | Verification | Stdout regression resolved; supplied live smoke result recorded | Assistant-run suite: 37 tests pass in 0.021s; user live result: validated successful diagnosis, error null | Verify credential placement and spending allowance |

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
