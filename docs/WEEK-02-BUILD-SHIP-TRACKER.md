# Week 2 Build / Ship Tracker — Function calling & tool design

[All weeks](BUILD-SHIP-INDEX.md) · [Week 2 plan](WEEK-02-BUILD-SHIP.md) · [Previous week](WEEK-01-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-03-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: In progress
- Current phase: Phase 1
- Last evidence update: 2026-10-07
- Main blocker: Rejection messages are empty; validated payment IDs are absent from success/denial traces.
- Next action: Populate safe rejection messages and validated trace payment IDs; rerun the full acceptance suite.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Tool contracts and identity](#phase-1) | In progress | Initial 64 tests pass; expanded 66-method suite exposes two contract gaps |
| 2 | [Fixture-backed execution](#phase-2) | Not started | — |
| 3 | [Manual tool lifecycle](#phase-3) | Not started | — |
| 4 | [Bounded recovery and replay](#phase-4) | Not started | — |
| 5 | [Tool selection and recovery evaluation](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Tool contracts and identity

- [x] Define schemas for get_payment, get_payment_events, get_ledger_entries and get_provider_status.
- [x] Carry trusted organization identity separately from model arguments.
- [ ] Define ToolError(code, retryable, message) and safe trace fields.
- [x] Reject malformed arguments and denied authorization before fixture access.

Evidence / notes:

```text
Status: In progress
Files or links: app/tools/contracts.py; app/tools/errors.py; app/tools/gateway.py; tests/test_tool_contracts.py
Command / review procedure: `../.venv/bin/python -m unittest discover -s tests -q`
Dataset / prompt / model / policy versions (where relevant): Phase 1 mocks only; no fixtures or model calls
Observed result / metrics: Existing 64 tests pass (0.407s). Expanded 66-method suite fails 11 subtests across two new methods: three blank rejection messages and eight missing validated payment IDs in success/denial traces.
What this proves: Four strict argument schemas, trusted identity separation, validation-before-authorization, deny-before-reader, literal-True decisions, bounded trace fields and exclusive results pass existing checks.
Limitations / unverified behavior: Real fixture tenant isolation is Phase 2; no live model requests. Core files remain learner-owned and untracked at review time.
Open question / blocker: Populate explicit safe messages and validated payment IDs. Error enum/string values are inconsistent but current emitted codes pass existing checks.
Next action: Fix both gaps in one batch and rerun review.
```

<a id="phase-2"></a>

### Phase 2 — Fixture-backed execution

- [ ] Implement the four tools using synthetic simulator fixtures.
- [ ] Cover unknown payment IDs, invalid providers and payment-not-found.
- [ ] Distinguish malformed and empty responses from successful evidence.
- [ ] Test Org A cannot read Org B fixtures through any tool.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-3"></a>

### Phase 3 — Manual tool lifecycle

- [ ] Implement the manual tool loop without an agent framework.
- [ ] Validate tool name and arguments and authorize every execution.
- [ ] Record requested tool, arguments, result and timing in the trace.
- [ ] Enforce maximum tool steps and distinguish fresh reads from stale repeated invocations.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-4"></a>

### Phase 4 — Bounded recovery and replay

- [ ] Set per-attempt timeout, total deadline, maximum attempts and backoff.
- [ ] Test timeout and 500 retryability; never automatically retry invalid arguments or denied access.
- [ ] Use a stable operation key for one fake local side effect.
- [ ] Simulate commit followed by timeout and prove retry cannot duplicate the effect.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-5"></a>

### Phase 5 — Tool selection and recovery evaluation

- [ ] Store 40 labelled first-tool-selection scenarios and measure ≥90% correctness.
- [ ] Assert typed error code, retryability, attempts and trace for all failure categories.
- [ ] Record repeated invocation and duplicate side-effect outcomes.
- [ ] Save week2-error-recovery.md and draw the tool-calling lifecycle from memory.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-6"></a>

### Phase 6 — Local ship and learning handoff

- [ ] Document setup and exact offline/test/eval commands from the project root.
- [ ] Verify the slice from a clean source checkout and record dependency/environment limitations.
- [ ] Complete the deliverable inventory and curriculum exit-criteria evidence below.
- [ ] Write the engineering note with a deliberate failure, measured tradeoff, limitations and next smallest action.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

## Deliverable inventory

Paths below are relative to the project root; they are target artifacts, not claims that files already exist.

| Curriculum deliverable | Primary phase | Status | Evidence |
| --- | --- | --- | --- |
| `app/tools/` | 2 | Not started | — |
| `app/llm/tool_loop.py` | 3 | Not started | — |
| `simulator/fixtures/` | 2 | Not started | — |
| `evals/datasets/tool_selection.jsonl` | 5 | Not started | — |
| `app/tools/errors.py` | 1 | Not started | — |
| `evals/reports/week2-error-recovery.md` | 5 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Make tools return unknown IDs, invalid providers, malformed arguments, timeouts, 500s, empty responses, and payment-not-found. Add an explicit maximum tool-step count.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Unknown ID / invalid provider | — | — | Define from phase acceptance checks | — | Not started |
| Malformed arguments / denied authorization | — | — | Define from phase acceptance checks | — | Not started |
| Timeout / 500 / malformed response / empty response | — | — | Define from phase acceptance checks | — | Not started |
| Stale repeated call versus intentional fresh read | — | — | Define from phase acceptance checks | — | Not started |
| Fake side effect commits before timeout and retry | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] ≥90% correct first tool selection across 40 scenarios
- [ ] Invalid tool arguments are rejected before execution
- [ ] Authorization is performed by the application
- [ ] A maximum tool-step count exists
- [ ] Timeouts cannot create infinite retries
- [ ] Draw the full tool-calling lifecycle from memory
- [ ] Retryable and non-retryable failures produce typed ToolError results
- [ ] Retries have explicit attempt and total-time limits
- [ ] Duplicate side effects are prevented with an idempotent operation key
- [ ] Tool errors and recovery attempts are observable in the execution trace

| Criterion or metric | Supporting phase / evidence | Result / denominator | Remaining gap |
| --- | --- | --- | --- |
| Add a row for each verified criterion | — | — | — |

## Session log

Append verified work without rewriting earlier evidence.

| Date | Phase | Timebox | Completed / reviewed | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| 2026-10-07 | Phase 1 | Review | Validation and authorization gate verified; error/trace gaps reproduced | 64 passing original tests; 66 expanded methods with 11 failing subtests | Add safe messages and validated trace IDs |

## Definition of done

- [ ] All six phase checklists and exit gates have reviewed evidence.
- [ ] Every curriculum deliverable is present and its purpose verified.
- [ ] Every curriculum exit criterion above is supported by evidence.
- [ ] Required failure cases and experiments have saved results, including misses and limitations.
- [ ] Setup, commands and environment assumptions are documented and verified from clean source.
- [ ] The engineering note explains the primitive, deliberate failure, measurements and tradeoff.
- [ ] The next smallest action and remaining gaps are recorded.
- [ ] Supported browser checkpoints are identified; no browser completion or production readiness is inferred.
