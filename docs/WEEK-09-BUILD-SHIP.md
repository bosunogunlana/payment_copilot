# Week 9 Build / Ship Plan — Build an agent yourself

[All weeks](BUILD-SHIP-INDEX.md) · [Week 9 tracker](WEEK-09-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-08-BUILD-SHIP.md) · [Next week](WEEK-10-BUILD-SHIP.md)

## Scope and ship target

Implement a bounded agent loop for “Why is payment pay_123 still processing?” Store observable trajectories: requested tool, arguments, result, timing, and final answer. Do not depend on private chain-of-thought.

**Learning goal:** Understand an agent without framework magic: state, decisions, validated actions, observations, and termination.

**Before you start:** Reuse the Week 2 loop; do not start another tool framework.

**Keep the build focused:** Add explicit state, max steps, total deadline, retry budget and observable trajectories. Compare with a fixed deterministic investigation workflow. Add one assembler to the existing bounded loop. Use synthetic long observations for overflow tests instead of building a general memory service.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 09. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [State and termination contract](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Manual agent execution](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Context assembler and authority](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Overflow and freshness failures](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Bounded baseline evaluation](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: State and termination contract

### Goal

Extend the Week 2 loop into a bounded investigation.

### Expected outcome and completion checklist

- [ ] Define explicit agent state and observable trajectory fields.
- [ ] Set MAX_STEPS, total timeout and retry budgets.
- [ ] Define answer, insufficient-evidence and human-escalation termination conditions.
- [ ] Create a fixed deterministic investigation workflow for comparison.

### Primary files

- `app/agents/state.py`

### Walkthrough needed

Explain the contract and data flow for state and termination contract, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-09-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Manual agent execution

### Goal

Investigate pay_123 using validated application-owned tools.

### Expected outcome and completion checklist

- [ ] Implement the bounded loop for why pay_123 is still processing.
- [ ] Validate and authorize every tool call.
- [ ] Store requested tool, arguments, result, timing and final answer.
- [ ] Convert timeout, incorrect/conflicting data and repeated calls into typed observations.

### Primary files

- `app/agents/loop.py`

### Walkthrough needed

Explain the contract and data flow for manual agent execution, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-09-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Context assembler and authority

### Goal

Own the exact model input within a measured budget.

### Expected outcome and completion checklist

- [ ] Implement assemble_context with request, instructions, state, conversation, tool results, documents and max_tokens.
- [ ] Use model tokenizer or a conservative measured estimate and reserve output/tool-schema headroom.
- [ ] Define drop/summarize/never-remove rules preserving safety, task and authoritative evidence.
- [ ] Retain source IDs, versions, timestamps and summary provenance; treat source text as untrusted.

### Primary files

- `app/agents/context_assembler.py`

### Walkthrough needed

Explain the contract and data flow for context assembler and authority, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-09-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Overflow and freshness failures

### Goal

Fail safely when context or evidence cannot support an answer.

### Expected outcome and completion checklist

- [ ] Exceed context with old conversation, huge tool outputs and redundant documents.
- [ ] Expire stale observations and refresh retrieval on payment/document version changes.
- [ ] Assert essential evidence and authorization cannot be removed to fit.
- [ ] Save a redacted exact input snapshot with model/prompt/policy versions and replay a failed call without private chain-of-thought.

### Primary files

- `evals/agent/context_overflow.jsonl`

### Walkthrough needed

Explain the contract and data flow for overflow and freshness failures, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-09-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Bounded baseline evaluation

### Goal

Compare trajectories and context behavior against a fixed workflow.

### Expected outcome and completion checklist

- [ ] Measure ≥80% completion on baseline investigations and zero unbounded loops.
- [ ] Test repeated calls, infinite-loop attempts, timeouts and no-answer cases.
- [ ] Record context_tokens, retrieved_tokens, tool_result_tokens, conversation_tokens, tokens_dropped and tokens_summarized with counting conventions.
- [ ] Save context-budget.md and week9.md explaining compression failures and freshness policy.

### Primary files

- `evals/agent/baseline.jsonl`
- `evals/reports/context-budget.md`

### Walkthrough needed

Explain the contract and data flow for bounded baseline evaluation, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-09-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

- `docs/learning-notes/week9.md`

### Walkthrough needed

Explain the contract and data flow for local ship and learning handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-09-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Build assemble_context(user_request, system_instructions, agent_state, conversation, tool_results, retrieved_documents, max_tokens). Use the selected model’s tokenizer or a conservative measured estimate. Reserve room for output and tool schemas within the model limit; the example budget is input context, not a model recommendation.
- Define what is dropped, summarized and never removed: preserve safety/authorization boundaries, the current task and authoritative evidence needed for a safe answer. Treat tool/document text as untrusted data, not instructions. Include source IDs, versions and observation timestamps. Summaries retain provenance and must not become more authoritative than their sources.
- Expire stale observations, repeat retrieval when payment state or document versions change, and fail safely or escalate if essential context cannot fit. Store a redacted inspectable snapshot of exactly the assembled synthetic input, plus model, prompt and policy versions; protect any real diagnostic snapshots with access and retention controls.

## Curriculum contract — experiments and comparisons

- Deliberately exceed the context budget with old conversation, huge tool results and redundant documents. Assert selection rules, output headroom, stale-observation handling and retained authoritative sources. Replay a failed call from its context snapshot; never request private chain-of-thought.

## Curriculum contract — metrics to record

- context_tokens · retrieved_tokens · tool_result_tokens · conversation_tokens · tokens_dropped · tokens_summarized

## Required failure and evaluation pass

Force an infinite loop, repeated tool call, timeout, incorrect tool data, conflicting tools, and no-answer scenario. Make each failure a typed observation.

## Curriculum deliverables

- [ ] `app/agents/loop.py`
- [ ] `app/agents/state.py`
- [ ] `evals/agent/baseline.jsonl`
- [ ] `docs/learning-notes/week9.md`
- [ ] `app/agents/context_assembler.py`
- [ ] `evals/agent/context_overflow.jsonl`
- [ ] `evals/reports/context-budget.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

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

## Engineering note

Explain authority and freshness rules, one compression failure, and what you refuse to remove even when the context is full.

## Optional depth — does not gate this week

Planning strategies are optional until the bounded baseline passes.
