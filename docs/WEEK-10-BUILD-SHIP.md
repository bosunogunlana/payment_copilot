# Week 10 Build / Ship Plan — Incident investigation agent

[All weeks](BUILD-SHIP-INDEX.md) · [Week 10 tracker](WEEK-10-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-09-BUILD-SHIP.md) · [Next week](WEEK-11-BUILD-SHIP.md)

## Scope and ship target

Generate time-series simulator conditions and build an investigator with query_metrics, search_logs, find_incidents, list_failed_payments, get_provider_status, and search_runbooks. Answer why USDC withdrawal success rate dropped in the last 30 minutes.

**Learning goal:** Move from a single payment diagnosis to a system-level production investigation with metrics, logs, history, and provider state.

**Before you start:** Use Week 9 agent and the same simulator interfaces.

**Keep the build focused:** Use seeded metrics/log fixtures, not a new telemetry platform. Build 30 incident variants with known causes and evaluate both the evidence trail and final diagnosis. Add trajectory labels to existing incidents; do not create another 30 scenarios or new observability infrastructure.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 10. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Incident evidence and labels](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Operational investigation tools](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Investigator integration](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Trajectory grading](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Answer and trajectory evaluation](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Incident evidence and labels

### Goal

Define known causes and acceptable evidence sets for 30 incidents.

### Expected outcome and completion checklist

- [ ] Create at least 30 seeded time-series incident variants in the existing simulator.
- [ ] Label root causes, required evidence and acceptable alternative tool orders.
- [ ] Define the last-30-minutes USDC withdrawal success-rate question.
- [ ] Reuse Week 9 state, budgets and trace store.

### Primary files

- `simulator/scenarios/`
- `evals/agent/scenarios.jsonl`

### Walkthrough needed

Explain the contract and data flow for incident evidence and labels, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-10-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Operational investigation tools

### Goal

Expose bounded fixture-backed system evidence.

### Expected outcome and completion checklist

- [ ] Implement query_metrics, search_logs, find_incidents and list_failed_payments.
- [ ] Reuse get_provider_status and search_runbooks.
- [ ] Enforce trusted scope and typed tool errors.
- [ ] Test timing windows and conflicting operational observations.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for operational investigation tools, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-10-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Investigator integration

### Goal

Produce a system diagnosis grounded in the gathered evidence.

### Expected outcome and completion checklist

- [ ] Connect tools to the existing bounded investigator.
- [ ] Record evidence sources supporting root-cause claims.
- [ ] Escalate insufficient evidence rather than guessing.
- [ ] Keep observable trajectories and per-investigation tokens, cost and latency.

### Primary files

- `app/agents/investigator.py`

### Walkthrough needed

Explain the contract and data flow for investigator integration, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-10-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Trajectory grading

### Goal

Score evidence gathering independently of the final answer.

### Expected outcome and completion checklist

- [ ] Grade first tool, sufficient evidence, irrelevant tools, repeats, stopping and budgets.
- [ ] Allow scenario-specific alternative tool orders rather than one rigid script.
- [ ] Report correct_tool_selection, unnecessary_tool_calls, duplicate_tool_calls, steps_to_resolution, tool_error_recovery and trajectory_success.
- [ ] Document denominators and mark error recovery N/A when no tool error occurred.

### Primary files

- `evals/graders/trajectory.py`

### Walkthrough needed

Explain the contract and data flow for trajectory grading, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-10-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Answer and trajectory evaluation

### Goal

Demonstrate why a lucky correct answer can fail.

### Expected outcome and completion checklist

- [ ] Compare missing-evidence correctness, efficient evidence-backed diagnosis, over-budget work, unnecessary repeat and recovered timeout.
- [ ] Evaluate the same 30 scenarios, without creating another dataset.
- [ ] Measure ≥80% correct root cause, ≥90% no unsupported claims and zero infinite loops.
- [ ] Save trajectory-quality.md with average tool calls and quality/cost/latency tradeoffs.

### Primary files

- `evals/reports/trajectory-quality.md`

### Walkthrough needed

Explain the contract and data flow for answer and trajectory evaluation, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-10-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-10-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Keep final-answer evaluation. Add trajectory assertions for correct first tool, sufficient evidence, irrelevant tools, unnecessary repeats, premature stopping, tool-call budgets and efficient diagnosis. Define acceptable evidence sets and alternative tool orders per scenario rather than grading one rigid script.
- Record correct_tool_selection, unnecessary_tool_calls, duplicate_tool_calls, steps_to_resolution, tool_error_recovery and trajectory_success. Report their denominators; use N/A for error recovery when no error occurred. A guessed correct answer without required evidence fails trajectory_success.

## Curriculum contract — experiments and comparisons

- Compare a correct diagnosis with missing evidence, an evidence-supported efficient diagnosis, an over-budget investigation, an unnecessary repeat and a recovered timeout. Grade these against the same 30 incident scenarios and retain both answer and trajectory scores.

## Curriculum contract — metrics to record

- correct_tool_selection · unnecessary_tool_calls · duplicate_tool_calls · steps_to_resolution · tool_error_recovery · trajectory_success

## Required failure and evaluation pass

Evaluate both final diagnosis and trajectory: relevant evidence inspected, unnecessary calls, premature stopping, root-cause confidence, and unsupported claims.

## Curriculum deliverables

- [ ] `simulator/scenarios/`
- [ ] `app/agents/investigator.py`
- [ ] `evals/agent/scenarios.jsonl`
- [ ] `evals/graders/trajectory.py`
- [ ] `evals/reports/trajectory-quality.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] At least 30 incident scenarios exist
- [ ] ≥80% correct root cause
- [ ] ≥90% no unsupported root-cause claims
- [ ] Zero infinite loops
- [ ] Average tool calls are tracked
- [ ] Tokens, cost, and latency per investigation are tracked
- [ ] Trajectory grading checks first tool, evidence coverage, repeats, stopping and budgets
- [ ] All six trajectory metrics are reported alongside final-answer quality
- [ ] An unsupported lucky diagnosis cannot pass trajectory_success

## Engineering note

Compare two successful-looking answers whose trajectories differ. Explain acceptable extra calls and the cost of stopping too soon.

## Optional depth — does not gate this week

Add more providers only after the existing scenarios are covered.
