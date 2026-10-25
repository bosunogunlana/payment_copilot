# Week 16 Build / Ship Plan — Ship the Payment Reliability Copilot

[All weeks](BUILD-SHIP-INDEX.md) · [Week 16 tracker](WEEK-16-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-15-BUILD-SHIP.md)

## Scope and ship target

Ship the capstone: a natural-language operations interface with payment investigation, RAG over runbooks, semantic incident search, tool calling, multi-step investigations, MCP tools, citations, human approval, evals, tracing, cost tracking, authorization, and resilience. The core finish is a reproducible simulator-backed demo. Treat a live production rollout as a separate operational milestone.

**Learning goal:** Bring the system together into a credible, explainable, observable capstone you can demo and defend.

**Before you start:** Bring forward the same simulator, eval runner and evidence from previous weeks.

**Keep the build focused:** Reuse the router, trace store and eval runner. Demonstrate a small curated review queue with simulator events, then freeze and record the existing final demo. A reproducible simulator demo remains the core learning finish; real production release requires separate validation.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 16. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Capstone integration and release manifest](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Curated data-to-eval flywheel](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Preferred/fallback/human hierarchy](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Failure and recovery rehearsal](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Portfolio freeze and explanation](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Capstone integration and release manifest

### Goal

Bring existing capabilities together around one reproducible simulator demo.

### Expected outcome and completion checklist

- [ ] Verify natural-language investigation, RAG, incident search, tool calling, bounded agents, MCP, citations and approval paths.
- [ ] Pin domain adapters, context/retrieval/router/cache policy, prompt/model/dataset versions and traces.
- [ ] Carry forward eval, authorization, resilience and cost controls.
- [ ] Inventory open gaps and keep live production release separate.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for capstone integration and release manifest, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-16-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Curated data-to-eval flywheel

### Goal

Turn observations into reviewed evaluation evidence without automatic training.

### Expected outcome and completion checklist

- [ ] Document thumbs down, human corrections, agent failures, tool failures, low confidence and production incidents as candidate sources.
- [ ] Redact, deduplicate, retain provenance and require human label review.
- [ ] Protect held-out evaluation and document authorization/consent/retention before real-data use.
- [ ] Convert synthetic thumbs-down, correction and tool failure into reviewed versioned cases and rerun evals.

### Primary files

- `docs/data-eval-flywheel.md`
- `evals/candidates/reviewed-examples.jsonl`

### Walkthrough needed

Explain the contract and data flow for curated data-to-eval flywheel, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-16-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Preferred/fallback/human hierarchy

### Goal

Fail safely when the preferred model is unavailable or unaffordable.

### Expected outcome and completion checklist

- [ ] Reuse Week 13 router and typed errors for preferred → fallback → human escalation.
- [ ] Define failure/capacity/budget criteria, maximum attempts, cost and latency bounds.
- [ ] Check tool/schema compatibility and preserve tenant/tool/approval policies across models.
- [ ] Document fallback quality/cost consequences and evidence-backed escalation reasons.

### Primary files

- `docs/fallback-architecture.md`

### Walkthrough needed

Explain the contract and data flow for preferred/fallback/human hierarchy, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-16-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Failure and recovery rehearsal

### Goal

Show eventual safe escalation and no duplicate effects.

### Expected outcome and completion checklist

- [ ] Inject preferred-model failure, capacity rejection and exhausted budget.
- [ ] Make fallback fail or lack evidence and verify bounded human escalation.
- [ ] Rehearse happy path, insufficient evidence, provider outage, injection, cross-tenant request, duplicate side effect and process restart.
- [ ] Keep traces, final eval report and fallback-rehearsal.md including failures and tradeoffs.

### Primary files

- `evals/reports/final.md`
- `evals/reports/fallback-rehearsal.md`

### Walkthrough needed

Explain the contract and data flow for failure and recovery rehearsal, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-16-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Portfolio freeze and explanation

### Goal

Record the existing final demo and defend the engineering choices.

### Expected outcome and completion checklist

- [ ] Write architecture.md showing adapters, context, retrieval, routing, cache, traces and release gates.
- [ ] Write case-study.md explaining why AI fits and what changes at 100× scale.
- [ ] Freeze and record a 2–4 minute payment-copilot-demo.mp4.
- [ ] Document one observation unsuitable as a label, one prohibited fallback and evidence required for the next release.

### Primary files

- `docs/architecture.md`
- `demo/payment-copilot-demo.mp4`
- `docs/case-study.md`

### Walkthrough needed

Explain the contract and data flow for portfolio freeze and explanation, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-16-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-16-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Keep the portfolio release and final rehearsal. Design a Data Flywheel: interactions → success/failure/human correction signals → review pipeline → labelled eval cases → versioned dataset → prompt/model changes → gated release. Capture thumbs down, human corrections, agent failures, tool failures, low-confidence cases and production incidents as candidates, not automatically trusted labels.
- Demonstrate the review flow with simulator observations. Redact sensitive data, check authorization/consent and retention before any real production use, deduplicate cases, require human label review, retain provenance and keep held-out evaluation uncontaminated. Do not automatically train or fine-tune models from production data.
- Add a bounded preferred model → fallback model → human escalation hierarchy. Document failure/capacity/budget criteria, tool/schema compatibility, quality and cost implications, maximum attempts and safe failure behavior. Use the Week 13 router and typed errors; prohibit a cheaper fallback from weakening tenant, tool or approval rules. Provide evidence and a reason when escalating instead of fabricating an answer.

## Curriculum contract — experiments and comparisons

- Turn a synthetic thumbs-down, human correction and tool failure into reviewed labelled cases and rerun the eval suite. Inject preferred-model failure, capacity rejection and exhausted budget, then make the fallback fail or lack evidence. Verify eventual human escalation, bounded spend/latency and no duplicate side effects.

## Required failure and evaluation pass

Run a final rehearsal with a happy path, insufficient evidence, provider outage, prompt injection, cross-tenant request, duplicate side effect, and process restart. Keep the trace and the eval report.

## Curriculum deliverables

- [ ] `docs/architecture.md`
- [ ] `evals/reports/final.md`
- [ ] `demo/payment-copilot-demo.mp4`
- [ ] `docs/case-study.md`
- [ ] `docs/data-eval-flywheel.md`
- [ ] `evals/candidates/reviewed-examples.jsonl`
- [ ] `docs/fallback-architecture.md`
- [ ] `evals/reports/fallback-rehearsal.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] All core capabilities have a working path
- [ ] Final eval report includes failures and trade-offs
- [ ] Architecture document explains boundaries
- [ ] A 2–4 minute demo is recorded
- [ ] Case study explains why AI is appropriate
- [ ] You can explain what changes at 100× scale
- [ ] All six observation sources have a documented candidate-to-reviewed-eval path
- [ ] Data review includes privacy, provenance, deduplication and held-out-set protection
- [ ] No production feedback automatically trains a model or bypasses label review
- [ ] Preferred/fallback/human hierarchy passes failure, capacity and budget rehearsals
- [ ] Fallback quality, cost, compatibility and safe-failure behavior are documented
- [ ] Final architecture shows domain adapters, context, retrieval, routing, cache policy, traces and release gates

## Engineering note

Explain one observation that should not become a label, one unsafe fallback you prohibit, and the evidence required for the next release.

## Optional depth — does not gate this week

Deploy a private demo or add the Paqet adapter only when its API and authorization contract are ready.
