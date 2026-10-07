# Week 9 Build / Ship Tracker — Build an agent yourself

[All weeks](BUILD-SHIP-INDEX.md) · [Week 9 plan](WEEK-09-BUILD-SHIP.md) · [Previous week](WEEK-08-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-10-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 9 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [State and termination contract](#phase-1) | Not started | — |
| 2 | [Manual agent execution](#phase-2) | Not started | — |
| 3 | [Context assembler and authority](#phase-3) | Not started | — |
| 4 | [Overflow and freshness failures](#phase-4) | Not started | — |
| 5 | [Bounded baseline evaluation](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — State and termination contract

- [ ] Define explicit agent state and observable trajectory fields.
- [ ] Set MAX_STEPS, total timeout and retry budgets.
- [ ] Define answer, insufficient-evidence and human-escalation termination conditions.
- [ ] Create a fixed deterministic investigation workflow for comparison.

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

<a id="phase-2"></a>

### Phase 2 — Manual agent execution

- [ ] Implement the bounded loop for why pay_123 is still processing.
- [ ] Validate and authorize every tool call.
- [ ] Store requested tool, arguments, result, timing and final answer.
- [ ] Convert timeout, incorrect/conflicting data and repeated calls into typed observations.

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

### Phase 3 — Context assembler and authority

- [ ] Implement assemble_context with request, instructions, state, conversation, tool results, documents and max_tokens.
- [ ] Use model tokenizer or a conservative measured estimate and reserve output/tool-schema headroom.
- [ ] Define drop/summarize/never-remove rules preserving safety, task and authoritative evidence.
- [ ] Retain source IDs, versions, timestamps and summary provenance; treat source text as untrusted.

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

### Phase 4 — Overflow and freshness failures

- [ ] Exceed context with old conversation, huge tool outputs and redundant documents.
- [ ] Expire stale observations and refresh retrieval on payment/document version changes.
- [ ] Assert essential evidence and authorization cannot be removed to fit.
- [ ] Save a redacted exact input snapshot with model/prompt/policy versions and replay a failed call without private chain-of-thought.

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

### Phase 5 — Bounded baseline evaluation

- [ ] Measure ≥80% completion on baseline investigations and zero unbounded loops.
- [ ] Test repeated calls, infinite-loop attempts, timeouts and no-answer cases.
- [ ] Record context_tokens, retrieved_tokens, tool_result_tokens, conversation_tokens, tokens_dropped and tokens_summarized with counting conventions.
- [ ] Save context-budget.md and week9.md explaining compression failures and freshness policy.

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
| `app/agents/loop.py` | 2 | Not started | — |
| `app/agents/state.py` | 1 | Not started | — |
| `evals/agent/baseline.jsonl` | 5 | Not started | — |
| `docs/learning-notes/week9.md` | 6 | Not started | — |
| `app/agents/context_assembler.py` | 3 | Not started | — |
| `evals/agent/context_overflow.jsonl` | 4 | Not started | — |
| `evals/reports/context-budget.md` | 5 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Force an infinite loop, repeated tool call, timeout, incorrect tool data, conflicting tools, and no-answer scenario. Make each failure a typed observation.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Infinite-loop attempt / repeated call | — | — | Define from phase acceptance checks | — | Not started |
| Timeout / retry exhaustion | — | — | Define from phase acceptance checks | — | Not started |
| Incorrect or conflicting tools / no answer | — | — | Define from phase acceptance checks | — | Not started |
| Old conversation / huge tools / redundant documents overflow | — | — | Define from phase acceptance checks | — | Not started |
| Stale payment state or document version | — | — | Define from phase acceptance checks | — | Not started |
| Essential context cannot fit / failed-call snapshot replay | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] MAX_STEPS is enforced
- [ ] A timeout budget exists
- [ ] A retry budget exists
- [ ] Tool calls are validated
- [ ] Termination conditions are explicit
- [ ] Agent completes ≥80% of baseline investigations
- [ ] Context Assembler enforces a documented token budget with output headroom
- [ ] Overflow tests prove drop/summarize/never-remove rules and safe failure
- [ ] Stale observations trigger documented refresh or retrieval decisions
- [ ] All six context metrics are recorded with clear counting conventions
- [ ] Explain more context != better context and inspect the exact context of a failed call

| Criterion or metric | Supporting phase / evidence | Result / denominator | Remaining gap |
| --- | --- | --- | --- |
| Add a row for each verified criterion | — | — | — |

## Session log

Append verified work without rewriting earlier evidence.

| Date | Phase | Timebox | Completed / reviewed | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | — |

## Definition of done

- [ ] All six phase checklists and exit gates have reviewed evidence.
- [ ] Every curriculum deliverable is present and its purpose verified.
- [ ] Every curriculum exit criterion above is supported by evidence.
- [ ] Required failure cases and experiments have saved results, including misses and limitations.
- [ ] Setup, commands and environment assumptions are documented and verified from clean source.
- [ ] The engineering note explains the primitive, deliberate failure, measurements and tradeoff.
- [ ] The next smallest action and remaining gaps are recorded.
- [ ] Supported browser checkpoints are identified; no browser completion or production readiness is inferred.
