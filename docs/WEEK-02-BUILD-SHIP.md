# Week 2 Build / Ship Plan — Function calling & tool design

[All weeks](BUILD-SHIP-INDEX.md) · [Week 2 tracker](WEEK-02-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-01-BUILD-SHIP.md) · [Next week](WEEK-03-BUILD-SHIP.md)

## Scope and ship target

Create four deterministic fixture-backed tools: get_payment, get_payment_events, get_ledger_entries, and get_provider_status. Implement the orchestration loop yourself—no agent framework.

**Learning goal:** Understand the core mechanism behind agents: the model requests work, your application validates and executes it.

**Before you start:** Reuse Week 1 diagnosis models and fixtures.

**Keep the build focused:** Implement the four read-only tools with explicit organization identity. Reject unauthorized calls before execution; add timeouts and bounded retries now. Reuse the existing failure fixtures. Spend the failure-testing block on typed outcomes and one fake side-effect replay, not on new tool integrations.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 02. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Tool contracts and identity](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Fixture-backed execution](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Manual tool lifecycle](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Bounded recovery and replay](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Tool selection and recovery evaluation](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Tool contracts and identity

### Goal

Make the four read-only tool boundaries executable before model orchestration.

### Expected outcome and completion checklist

- [ ] Define schemas for get_payment, get_payment_events, get_ledger_entries and get_provider_status.
- [ ] Carry trusted organization identity separately from model arguments.
- [ ] Define ToolError(code, retryable, message) and safe trace fields.
- [ ] Reject malformed arguments and denied authorization before fixture access.

### Primary files

- `app/tools/errors.py`

### Walkthrough needed

Explain the contract and data flow for tool contracts and identity, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-02-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Fixture-backed execution

### Goal

Return deterministic payment evidence through the same validated interface.

### Expected outcome and completion checklist

- [ ] Implement the four tools using synthetic simulator fixtures.
- [ ] Cover unknown payment IDs, invalid providers and payment-not-found.
- [ ] Distinguish malformed and empty responses from successful evidence.
- [ ] Test Org A cannot read Org B fixtures through any tool.

### Primary files

- `app/tools/`
- `simulator/fixtures/`

### Walkthrough needed

Explain the contract and data flow for fixture-backed execution, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-02-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Manual tool lifecycle

### Goal

Connect model requests to application-owned validation, execution and results.

### Expected outcome and completion checklist

- [ ] Implement the manual tool loop without an agent framework.
- [ ] Validate tool name and arguments and authorize every execution.
- [ ] Record requested tool, arguments, result and timing in the trace.
- [ ] Enforce maximum tool steps and distinguish fresh reads from stale repeated invocations.

### Primary files

- `app/llm/tool_loop.py`

### Walkthrough needed

Explain the contract and data flow for manual tool lifecycle, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-02-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Bounded recovery and replay

### Goal

Recover from transient failures without repeating a fake side effect.

### Expected outcome and completion checklist

- [ ] Set per-attempt timeout, total deadline, maximum attempts and backoff.
- [ ] Test timeout and 500 retryability; never automatically retry invalid arguments or denied access.
- [ ] Use a stable operation key for one fake local side effect.
- [ ] Simulate commit followed by timeout and prove retry cannot duplicate the effect.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for bounded recovery and replay, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-02-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Tool selection and recovery evaluation

### Goal

Measure selection quality and recovery behavior on frozen scenarios.

### Expected outcome and completion checklist

- [ ] Store 40 labelled first-tool-selection scenarios and measure ≥90% correctness.
- [ ] Assert typed error code, retryability, attempts and trace for all failure categories.
- [ ] Record repeated invocation and duplicate side-effect outcomes.
- [ ] Save week2-error-recovery.md and draw the tool-calling lifecycle from memory.

### Primary files

- `evals/datasets/tool_selection.jsonl`
- `evals/reports/week2-error-recovery.md`

### Walkthrough needed

Explain the contract and data flow for tool selection and recovery evaluation, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-02-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for local ship and learning handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-02-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Keep the four fixture-backed tools and manual loop. Return a typed ToolError(code: str, retryable: bool, message: str) on failure, with a safe message and structured trace fields. Define per-attempt timeout, total deadline, maximum attempts and backoff. Do not retry invalid arguments or denied authorization automatically.
- Detect repeated invocations, but distinguish intentional fresh reads from repeated stale calls. Use a stable operation/idempotency key where execution has side effects; demonstrate deduplication with a fake local side effect, never a live payment operation.

## Curriculum contract — experiments and comparisons

- Test tool timeout, 500 error, malformed response, empty response, invalid arguments, unauthorized request, repeated tool invocation and duplicate side-effect attempts. Assert the error code, retryability, attempt count and resulting trace for each. Simulate a timeout after the fake side effect committed, then retry the same operation.

## Required failure and evaluation pass

Make tools return unknown IDs, invalid providers, malformed arguments, timeouts, 500s, empty responses, and payment-not-found. Add an explicit maximum tool-step count.

## Curriculum deliverables

- [ ] `app/tools/`
- [ ] `app/llm/tool_loop.py`
- [ ] `simulator/fixtures/`
- [ ] `evals/datasets/tool_selection.jsonl`
- [ ] `app/tools/errors.py`
- [ ] `evals/reports/week2-error-recovery.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

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

## Engineering note

Explain which failures may be retried, what deduplication guarantees, and what happens after an ambiguous timeout.

## Optional depth — does not gate this week

Add async tool execution only if the serial loop is understood.
