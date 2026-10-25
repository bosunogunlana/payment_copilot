# Week 11 Build / Ship Plan — LangGraph & durable workflows

[All weeks](BUILD-SHIP-INDEX.md) · [Week 11 tracker](WEEK-11-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-10-BUILD-SHIP.md) · [Next week](WEEK-12-BUILD-SHIP.md)

## Scope and ship target

Refactor the investigator into a graph: understand_request → gather_payment_state → gather_operational_state → retrieve_knowledge → analyze → confidence_gate → answer or human_review. Add a proposed create_incident action.

**Learning goal:** Learn the framework after understanding the primitive it abstracts: stateful, long-running, resumable workflows.

**Before you start:** Keep the Week 10 baseline unchanged for comparison.

**Keep the build focused:** Persist one investigation graph. Demonstrate restart and approval with a simulated create_incident action; bind approval to exact arguments and prevent replay. Use the engineering-note hour for the comparison and reuse the existing failure rehearsal. No second workflow implementation.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 11. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

## Working rules

- Keep implementation learner-owned, including core work outside `app/` such as Go, experiments and ingestion. The assistant supplies guidance, acceptance tests, fixtures and evaluation scaffolding.
- Extend prior simulator, corpus, interfaces and runners; use synthetic data and simulated side effects.
- Treat model output, retrieved text and tool results as untrusted. Preserve trusted identity and authorization boundaries.
- Set an explicit spending allowance before live model experiments; offline/stub runs do not establish model quality.
- “Ship” means a reproducible local slice with evidence and limitations. Production or real-money integration is a separate milestone.
- Check a phase only after reviewing its artifacts and acceptance evidence. Browser curriculum progress remains separate.

## Weekly rhythm and phase map

Aim for 8–10 hours: about 2 learning, 4–5 building, 1–2 breaking/evaluating and 1 documenting. Phases are dependency gates, not six separate full sessions; combine related work within the active phase. If required evidence needs more time, record the blocker rather than dropping requirements.

| Phase | Objective | Evidence to review |
| --- | --- | --- |
| 1 | [Graph state and baseline contract](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [LangGraph implementation](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Approval and side-effect isolation](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Crash/restart rehearsal](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Durability comparison](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Graph state and baseline contract

### Goal

Preserve the manual investigator as the comparison baseline.

### Expected outcome and completion checklist

- [ ] Freeze Week 10 scenarios and manual-loop results.
- [ ] Define persisted graph state and trusted identity boundaries.
- [ ] Map understand_request → gather_payment_state → gather_operational_state → retrieve_knowledge → analyze → confidence_gate.
- [ ] Define answer versus human_review outcomes and proposed simulated create_incident.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for graph state and baseline contract, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-11-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: LangGraph implementation

### Goal

Use the framework for the stateful primitive already understood.

### Expected outcome and completion checklist

- [ ] Implement the graph with existing investigator tools and context assembler.
- [ ] Persist checkpoints through an explicit checkpoint adapter.
- [ ] Preserve authorization, time/step/retry budgets and source evidence.
- [ ] Compare output and trajectory behavior against the unchanged manual baseline.

### Primary files

- `app/agents/graph.py`
- `app/agents/checkpoints.py`

### Walkthrough needed

Explain the contract and data flow for langgraph implementation, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-11-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Approval and side-effect isolation

### Goal

Pause and resume a proposed action without granting new authority.

### Expected outcome and completion checklist

- [ ] Bind simulated create_incident approval to actor, tenant, exact arguments, operation ID and expiry.
- [ ] Persist pending approval and resume only after application validation.
- [ ] Use application idempotency for the fake side effect.
- [ ] Reject replayed, altered, expired or unauthorized approvals.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for approval and side-effect isolation, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-11-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Crash/restart rehearsal

### Goal

Identify exactly what can execute again after interruption.

### Expected outcome and completion checklist

- [ ] Kill and resume before a model call.
- [ ] Kill and resume after a recorded model/tool result.
- [ ] Crash after the fake side effect but before acknowledgment.
- [ ] Prove persisted state, resumed approval and no duplicate side effects with recovery.jsonl.

### Primary files

- `evals/agent/recovery.jsonl`

### Walkthrough needed

Explain the contract and data flow for crash/restart rehearsal, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-11-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Durability comparison

### Goal

Explain framework guarantees using the actual restart evidence.

### Expected outcome and completion checklist

- [ ] Compare stored checkpoints with history-based replay and recorded activity results.
- [ ] Cover checkpointing, replay, idempotency, side-effect isolation, resume, determinism and persistence semantics.
- [ ] Identify model calls, wall-clock reads and mutations as nondeterministic boundaries.
- [ ] Write langgraph.md and langgraph-vs-durable-workflows.md without installing Temporal or building another engine.

### Primary files

- `docs/learning-notes/langgraph-vs-durable-workflows.md`

### Walkthrough needed

Explain the contract and data flow for durability comparison, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-11-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-6"></a>

## Phase 6: Local ship and learning handoff

### Goal

Package the week’s evidence so another learner can reproduce the slice.

### Expected outcome and completion checklist

- [ ] Document setup and exact offline/test/eval commands from the project root.
- [ ] Verify the slice from a clean source checkout and record dependency/environment limitations.
- [ ] Complete the deliverable inventory and curriculum exit-criteria evidence below.
- [ ] Write the engineering note with a deliberate failure, measured tradeoff, limitations and next smallest action.

### Primary files

- `docs/decisions/langgraph.md`

### Walkthrough needed

Explain the contract and data flow for local ship and learning handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-11-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Keep LangGraph and the existing restart/approval tests. Write “LangGraph persistence vs durable workflow engines.” Compare a stored graph checkpoint with history-based replay, deterministic workflow orchestration and recorded activity results. Model calls, wall-clock reads and external mutations are nondeterministic boundaries to isolate; neither framework removes the need for application idempotency. Do not install Temporal or build a workflow engine.

## Curriculum contract — experiments and comparisons

- Annotate the existing crash/restart test at three points: before a model call, after a recorded result, and after a fake side effect but before its acknowledgment. Explain what may run again in your LangGraph setup and how a Temporal-style workflow would manage that boundary.

## Required failure and evaluation pass

Kill the process halfway through an investigation, restart it, and resume from checkpoint. Attempt to replay a side effect and prove it is not duplicated.

## Curriculum deliverables

- [ ] `app/agents/graph.py`
- [ ] `app/agents/checkpoints.py`
- [ ] `evals/agent/recovery.jsonl`
- [ ] `docs/decisions/langgraph.md`
- [ ] `docs/learning-notes/langgraph-vs-durable-workflows.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] Workflow survives a process restart
- [ ] State is persisted
- [ ] Duplicate side effects are prevented
- [ ] Approval pauses and resumes correctly
- [ ] You can explain the value over the Week 9 loop
- [ ] Recovery behavior is covered by an eval
- [ ] The engineering note compares all seven durability concepts using the existing workflow
- [ ] Nondeterministic model calls and external side effects have explicit isolation/idempotency boundaries
- [ ] Explain why checkpointing alone does not guarantee exactly-once side effects

## Engineering note

LangGraph persistence vs durable workflow engines: what is saved, what replays, what can repeat, and which guarantees belong to your application.

## Optional depth — does not gate this week

Parallel graph branches are optional. Approval is not a replacement for application authorization.
