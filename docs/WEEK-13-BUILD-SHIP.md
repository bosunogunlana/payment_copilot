# Week 13 Build / Ship Plan — Serious evals

[All weeks](BUILD-SHIP-INDEX.md) · [Week 13 tracker](WEEK-13-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-12-BUILD-SHIP.md) · [Next week](WEEK-14-BUILD-SHIP.md)

## Scope and ship target

Expand to 300–500 cases across payment investigation, retrieval, tool selection, insufficient information, ambiguous requests, outages, permission boundaries, prompt injection, and hallucination.

**Learning goal:** Expand from a demo-sized golden set to an evaluation system that measures the whole agent environment.

**Before you start:** Pool and deduplicate Weeks 1–12 cases before generating more.

**Keep the build focused:** Reach 300 versioned cases cumulatively, not 300 new manually written cases. Cover each failure category and reserve a held-out set. Calibrate a judge against a human-reviewed sample. Build a small rule-based router and wire the existing runner to CI. Reuse the cumulative 300-case suite; a learned router and 500 cases remain extensions.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 13. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Versioned evaluation strategy](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Graders and disagreement review](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Rule-based model router](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Router versus strongest experiment](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [CI regression and restore gates](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Versioned evaluation strategy

### Goal

Scale the existing runner without contaminating held-out evidence.

### Expected outcome and completion checklist

- [ ] Version 300–500 cases with 300+ required and 500 stretch.
- [ ] Cover investigation, retrieval, tool selection, insufficient information, ambiguity, outages, permission boundaries, injection and hallucination.
- [ ] Separate development and final held-out tasks.
- [ ] Define deterministic, human, LLM-judge and pairwise grading roles.

### Primary files

- `evals/datasets/v1/`
- `docs/evaluation-strategy.md`

### Walkthrough needed

Explain the contract and data flow for versioned evaluation strategy, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-13-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Graders and disagreement review

### Goal

Find evaluator failure before using scores as release authority.

### Expected outcome and completion checklist

- [ ] Compare at least two grading methods.
- [ ] Review manual samples and document judge disagreement.
- [ ] Define denominators, missing-metric behavior and repeated-run policy.
- [ ] Extend existing runner and prompt registry rather than starting a new system.

### Primary files

- `evals/graders/`

### Walkthrough needed

Explain the contract and data flow for graders and disagreement review, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-13-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Rule-based model router

### Goal

Choose capacity under trusted budgets and evidence checks.

### Expected outcome and completion checklist

- [ ] Implement cheap/normal/strong rules using task, context, complexity, tool needs, confidence, tenant budget and latency SLO.
- [ ] Calibrate confidence on held-out outcomes or combine it with evidence checks.
- [ ] Log routing reasons and bound attempts, total spend and latency.
- [ ] Escalate cheap → stronger on insufficient evidence without exceeding tenant budget.

### Primary files

- `app/llm/router.py`

### Walkthrough needed

Explain the contract and data flow for rule-based model router, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-13-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Router versus strongest experiment

### Goal

Measure all attempts on identical held-out tasks.

### Expected outcome and completion checklist

- [ ] Compare routing with always using the strongest model.
- [ ] Exercise simple, complex, large-context, tool-required and budget-exhausted cases.
- [ ] Include failed and escalated attempts in quality/cost/latency/escalation totals.
- [ ] Save model-routing.md under a declared live-comparison budget; keep deterministic stubs separate.

### Primary files

- `evals/reports/model-routing.md`

### Walkthrough needed

Explain the contract and data flow for router versus strongest experiment, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-13-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: CI regression and restore gates

### Goal

Prove release acceptance rejects broken or unsafe evidence.

### Expected outcome and completion checklist

- [ ] Configure regression-thresholds.yaml and ci/eval-gates.yml.
- [ ] Document percentage-point versus relative change; example gates are accuracy drop >3 points, unsupported claims >5%, cross-tenant >0 and executed schemas <100%.
- [ ] Inject prompt regressions and security/schema failures; demonstrate a passing non-regressing run.
- [ ] Fail closed on missing metrics or broken evaluators and restore the prior prompt/model configuration.

### Primary files

- `evals/regression-thresholds.yaml`
- `ci/eval-gates.yml`

### Walkthrough needed

Explain the contract and data flow for ci regression and restore gates, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-13-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

- `evals/reports/week13.md`

### Walkthrough needed

Explain the contract and data flow for local ship and learning handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-13-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Add a Model Router with cheap, normal and strong routes. Consider task type, context size, estimated complexity, tool requirements, confidence, tenant budget and latency SLO. Start with explicit rules and log routing reasons; confidence must be calibrated on held-out outcomes or combined with evidence checks, not trusted as a raw self-reported number.
- Compare routing against always using the strongest model on the same held-out tasks. Include a cheap → stronger escalation when evidence/confidence is insufficient. Bound attempts, total cost and latency; do not escalate beyond tenant budget. Measure aggregate quality, cost, latency and escalation rate, including failed and escalated attempts.
- Add configurable CI eval gates to the Week 4 runner and prompt registry. Example policy: fail when root-cause accuracy drops more than 3 percentage points from the pinned baseline, unsupported_claim_rate exceeds 5%, cross-tenant violations exceed 0, or executed tool schema validity is below 100%. Clarify percentage points vs relative change; define repeated-run policy for stochastic quality metrics. Missing metrics or a broken evaluator must fail closed. Security invariants are hard gates, never averaged away.

## Curriculum contract — experiments and comparisons

- Exercise simple, complex, large-context, tool-required and budget-exhausted tasks. Inject a prompt regression and cross-tenant/schema violations to prove CI fails. Show a non-regressing run passes, and keep the router-vs-strongest report. Stub deterministic CI failures when API credentials are unavailable; run live quality comparisons separately under a budget.

## Curriculum contract — metrics to record

- quality · cost · latency · escalation_rate

## Required failure and evaluation pass

Compare deterministic assertions, human scoring, LLM-as-judge, and pairwise comparison. Sample cases manually and document judge disagreement.

## Curriculum deliverables

- [ ] `evals/datasets/v1/`
- [ ] `evals/graders/`
- [ ] `evals/reports/week13.md`
- [ ] `docs/evaluation-strategy.md`
- [ ] `app/llm/router.py`
- [ ] `evals/reports/model-routing.md`
- [ ] `evals/regression-thresholds.yaml`
- [ ] `ci/eval-gates.yml`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] 300+ cases are versioned
- [ ] Coverage includes safety and permissions
- [ ] At least two grading methods are compared
- [ ] Manual samples are reviewed
- [ ] Regression thresholds are defined
- [ ] A model/prompt change can be accepted or rejected by evidence
- [ ] Cheap / normal / strong routing and bounded escalation are implemented
- [ ] Router vs always-strongest comparison includes quality, cost, latency and escalation rate
- [ ] A deliberate quality regression fails CI at a configured threshold
- [ ] Cross-tenant violations and invalid executed tool schemas fail hard security gates
- [ ] Missing evaluation evidence blocks release and previous prompt/model configuration can be restored

## Engineering note

Explain routing rules, calibration, SLO/budget tradeoffs and the difference between model escalation and outage fallback.

## Optional depth — does not gate this week

500 cases and a second judge are stretch work. Never tune prompts against the final held-out set.
