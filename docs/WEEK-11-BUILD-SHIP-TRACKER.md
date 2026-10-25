# Week 11 Build / Ship Tracker — LangGraph & durable workflows

[All weeks](BUILD-SHIP-INDEX.md) · [Week 11 plan](WEEK-11-BUILD-SHIP.md) · [Previous week](WEEK-10-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-12-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 11 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Graph state and baseline contract](#phase-1) | Not started | — |
| 2 | [LangGraph implementation](#phase-2) | Not started | — |
| 3 | [Approval and side-effect isolation](#phase-3) | Not started | — |
| 4 | [Crash/restart rehearsal](#phase-4) | Not started | — |
| 5 | [Durability comparison](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Graph state and baseline contract

- [ ] Freeze Week 10 scenarios and manual-loop results.
- [ ] Define persisted graph state and trusted identity boundaries.
- [ ] Map understand_request → gather_payment_state → gather_operational_state → retrieve_knowledge → analyze → confidence_gate.
- [ ] Define answer versus human_review outcomes and proposed simulated create_incident.

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

### Phase 2 — LangGraph implementation

- [ ] Implement the graph with existing investigator tools and context assembler.
- [ ] Persist checkpoints through an explicit checkpoint adapter.
- [ ] Preserve authorization, time/step/retry budgets and source evidence.
- [ ] Compare output and trajectory behavior against the unchanged manual baseline.

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

### Phase 3 — Approval and side-effect isolation

- [ ] Bind simulated create_incident approval to actor, tenant, exact arguments, operation ID and expiry.
- [ ] Persist pending approval and resume only after application validation.
- [ ] Use application idempotency for the fake side effect.
- [ ] Reject replayed, altered, expired or unauthorized approvals.

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

### Phase 4 — Crash/restart rehearsal

- [ ] Kill and resume before a model call.
- [ ] Kill and resume after a recorded model/tool result.
- [ ] Crash after the fake side effect but before acknowledgment.
- [ ] Prove persisted state, resumed approval and no duplicate side effects with recovery.jsonl.

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

### Phase 5 — Durability comparison

- [ ] Compare stored checkpoints with history-based replay and recorded activity results.
- [ ] Cover checkpointing, replay, idempotency, side-effect isolation, resume, determinism and persistence semantics.
- [ ] Identify model calls, wall-clock reads and mutations as nondeterministic boundaries.
- [ ] Write langgraph.md and langgraph-vs-durable-workflows.md without installing Temporal or building another engine.

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
| `app/agents/graph.py` | 2 | Not started | — |
| `app/agents/checkpoints.py` | 2 | Not started | — |
| `evals/agent/recovery.jsonl` | 4 | Not started | — |
| `docs/decisions/langgraph.md` | 6 | Not started | — |
| `docs/learning-notes/langgraph-vs-durable-workflows.md` | 5 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Kill the process halfway through an investigation, restart it, and resume from checkpoint. Attempt to replay a side effect and prove it is not duplicated.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Crash before model call | — | — | Define from phase acceptance checks | — | Not started |
| Crash after recorded result | — | — | Define from phase acceptance checks | — | Not started |
| Crash after fake side effect before acknowledgment | — | — | Define from phase acceptance checks | — | Not started |
| Altered / expired / replayed approval | — | — | Define from phase acceptance checks | — | Not started |
| Paused approval survives restart | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] Workflow survives a process restart
- [ ] State is persisted
- [ ] Duplicate side effects are prevented
- [ ] Approval pauses and resumes correctly
- [ ] You can explain the value over the Week 9 loop
- [ ] Recovery behavior is covered by an eval
- [ ] The engineering note compares all seven durability concepts using the existing workflow
- [ ] Nondeterministic model calls and external side effects have explicit isolation/idempotency boundaries
- [ ] Explain why checkpointing alone does not guarantee exactly-once side effects

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
