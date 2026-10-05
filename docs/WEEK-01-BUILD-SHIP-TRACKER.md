# Week 1 Build / Ship Tracker

Use this file to track evidence for the phased build. Check a box only when the artifact, test, trace, or note exists. The browser curriculum tracker remains the source of truth for course progress; this file is a working companion for the implementation slice.

## Current status

- Overall status: In progress
- Current phase: Phase 5
- Last evidence update: 2026-10-05
- Main blocker: Comparison exposes prompt/dataset policy misalignment for missing events and unsupported decline codes; baseline method docstring describes the wrong path.
- Next action: Correct baseline/adapter documentation and make prompt rule precedence and supported-code scope explicit; preserve report 01 and review changes before another allocated run.

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
- [x] Confirm credentials are outside source control.

Evidence / notes:

```text
Status: Done
Files or links: app/llm/diagnose.py; app/llm/openai_transport.py; tests/test_llm_diagnose.py; tests/test_openai_transport.py; evals/smoke_diagnosis.py
What this proves: Assistant executed `../.venv/bin/python -m unittest discover -s tests -v`: all 37 tests pass in 0.021s, including the stdout regression. Transport strict-schema construction, refusal/incomplete handling, SDK failure mapping, timeout, and disabled retries are verified offline. User-provided live command `python -m evals.smoke_diagnosis --live --max-output-tokens 512 --acknowledge-spend` returned a validated succeeded/successful_payment/no_action diagnosis with confidence 0.99 and error null. Live evidence is user-provided, not independently rerun; it covers one synthetic case only.
Credential/budget evidence: User confirms OPENAI_API_KEY is in the shell environment and declares a $5 total smoke-test allowance. This records user-attested credential placement, not a historical secret scan. Output token limits and spending acknowledgement do not enforce a hard dollar cap; actual cumulative spend is not measured here.
Open question: None for the bounded Phase 3 exit gate. Next phase: Phase 4 failure dataset. No additional paid request was made for this verification.
```

### Phase 4 — Failure dataset

- [x] Expand `evals/datasets/week1.jsonl` to at least 30 cases.
- [x] Include missing-event cases.
- [x] Include conflicting-signal cases.
- [x] Include plausible-but-wrong-cause cases.
- [x] Include insufficient-evidence and escalation cases.
- [x] Give every case a stable ID and machine-checkable expected outcome.
- [x] Confirm that all data is synthetic.

Evidence / notes:

```text
Status: Done
Dataset count: 30
Case IDs reviewed: case-001 through case-030 reviewed against bounded Week 1 evidence policy
What this proves: All 39 tests pass. Dataset tests validate unique IDs and payloads, typed inputs and enum labels, synthetic markers, rationales, and required failure coverage. Existing fixture checks validate baseline label agreement and Diagnosis JSON round-trips across all 30 cases. Original five inputs/labels are preserved. Provenance and bounded label semantics are documented in evals/datasets/README.md. No model calls were made.
Reproducibility evidence: All 39 tests pass in the workspace (0.013s) and an isolated git HEAD archive plus the three candidate Phase 4 files (0.014s), with PYTHONPATH removed. This verifies candidate source portability using the existing dependency environment; it is not a fresh dependency installation. Dataset/test/README changes remain outside HEAD until committed.
Review: No blocking label or Python defect found. Labels comprise 4 success, 4 timeout, 3 authorization failure, and 19 unknown cases. Required tags cover 5 missing, 5 conflicting, 8 misleading-cause, 13 insufficient-evidence, and 5 repeated-event cases; counts overlap. Phase 5 must report category/tag breakdowns rather than aggregate accuracy alone. Matching labels does not prove likely_cause is grounded; unknown cause/confidence checks and cause-grounding review remain necessary.
Open question: None for the bounded Phase 4 gate. Next phase: Phase 5 comparison. No paid model calls were made.
```

### Phase 5 — Comparison and measurement

- [x] Name configuration A.
- [x] Name configuration B.
- [x] Run both against the same cases.
- [x] Record schema validity.
- [x] Record correctness or acceptable-label match.
- [x] Record confidence.
- [x] Record latency.
- [x] Record tokens when available.
- [x] Record estimated cost.
- [x] Group failures by category.
- [x] Record the spending limit and skipped cases.

Evidence / notes:

```text
Status: In progress
Report location: evals/reports/week1-comparison-01.json; evals/reports/week1-comparison-01-review.md
Decision: Provisional Luna for cost/latency; neither satisfies all current acceptance rules. Align prompt/dataset policy before drawing a capability conclusion.
What this proves: All 49 tests pass in 0.020s. Existing live report reviewed: both models attempt 30 cases, no skips/errors, 100% schema validity; Luna matches 27 labels, Sol 28. Both have two unsafe expected-unknown outcomes. Estimated costs $0.003422/$0.058462; mean latency 1.798s/4.829s. Report records $3 allocation and $0.05 reservations; dataset hash matches. Cause-grounding review is saved separately so original results remain intact. No new paid requests were made during review.
Open question: Fix prompt ambiguity (missing events override success; only AUTH_DECLINED supported for failed diagnoses) and misplaced baseline docstring. Phase 5 remains open pending policy alignment review. Historical measurements are preserved; further paid runs require an allocated budget.
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
| `app/llm/diagnose.py` | 3 | Done | 37 tests pass; live synthetic success and user-attested credential/budget setup recorded |
| `evals/datasets/week1.jsonl` | 1, 2, 4 | Done | 30 synthetic cases reviewed; 39 tests pass in workspace and isolated candidate snapshot |
| `docs/learning-notes/week1.md` | 6 | Not started | — |

## Failure coverage matrix

| Failure case | Represented in dataset | Test/eval run | Result or note |
| --- | --- | --- | --- |
| Missing events | [x] | [x] | 5 dataset cases; baseline checks pass |
| Conflicting signals | [x] | [x] | 5 dataset cases; baseline checks pass |
| Plausible but wrong cause | [x] | [x] | 8 dataset cases; baseline checks pass; LLM performance unmeasured |
| Refusal | [ ] | [ ] | — |
| Incomplete response | [ ] | [ ] | — |
| Malformed structured output | [ ] | [ ] | — |
| Insufficient evidence | [x] | [x] | 13 explicitly tagged cases; baseline escalation checks pass |

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
| 2026-10-02 | Phase 3 | Closeout | Phase 3 exit gate supported; Phase 3 Done | User confirms shell-environment key and $5 total smoke-test allowance; passing tests and live result already recorded | Phase 4: expand labelled synthetic dataset to at least 30 cases |

## Definition of done

Phase 5 review (2026-10-05): original 46 tests pass; expanded 49-method suite has one missing-usage contract failure. Assistant-owned harness preflight/checkpoint gaps fixed and tested. Phase 5 remains open pending usage normalization, comparison allocation, actual report, and cause-grounding review.

Phase 4 review (2026-10-02): 30 synthetic cases reviewed; all 39 tests pass in the workspace and isolated candidate snapshot. Phase 4 Done; next phase is Phase 5. No model comparison or paid call was performed.

The Week 1 build/ship segment is complete when all of these are true:

- [ ] The four curriculum deliverables exist.
- [ ] The test command passes from a clean run.
- [x] At least 30 labelled synthetic scenarios are stored.
- [ ] The diagnosis path handles success, uncertainty, and failure explicitly.
- [ ] Two model configurations have been compared on the same cases.
- [ ] Validity, confidence, latency, tokens, and cost are recorded.
- [ ] The learning note explains what failed and what the measurements changed.
- [ ] No production integration or real-money action is implied by the result.
