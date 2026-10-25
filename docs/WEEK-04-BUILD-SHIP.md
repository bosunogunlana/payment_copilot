# Week 4 Build / Ship Plan — Evaluation-driven development

[All weeks](BUILD-SHIP-INDEX.md) · [Week 4 tracker](WEEK-04-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-03-BUILD-SHIP.md) · [Next week](WEEK-05-BUILD-SHIP.md)

## Scope and ship target

Build a reusable eval runner that reports accuracy, schema compliance, tool correctness, unsupported claims, latency, token usage, and estimated cost. Create an error taxonomy.

**Learning goal:** Make evals part of development so a prompt change can be judged objectively.

**Before you start:** Combine earlier scenarios instead of starting another dataset.

**Keep the build focused:** Curate 75 unique cases, version the inputs and prompts, and run one before/after change. Record variation across repeated model runs; reproducible inputs do not imply identical outputs. Extend the existing runner and before/after report rather than building a second eval system. Use YAML files plus a release manifest.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 04. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Golden dataset and score contract](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Immutable prompt registry](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Reusable evaluation runner](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Before/after and variance](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Promotion and rollback rehearsal](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Golden dataset and score contract

### Goal

Extend the existing runner around a frozen, representative dataset.

### Expected outcome and completion checklist

- [ ] Curate at least 75 unique cases from previous weeks.
- [ ] Version inputs and define an error taxonomy.
- [ ] Specify accuracy, schema compliance, tool correctness and unsupported-claim graders.
- [ ] Define latency, usage and estimated-cost counting including failed attempts.

### Primary files

- `evals/datasets/golden_set.jsonl`
- `evals/error_taxonomy.yml`

### Walkthrough needed

Explain the contract and data flow for golden dataset and score contract, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-04-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Immutable prompt registry

### Goal

Make template identity and rollback exact.

### Expected outcome and completion checklist

- [ ] Create file-based prompt versions with name, version, created_at, model, template, status, eval_dataset, eval_score and notes.
- [ ] Keep published templates immutable; put changing release status and evidence in a manifest.
- [ ] Pin runtime registry versions.
- [ ] Prepare payment_diagnosis versions and incident_investigator/v1.yaml without building the future investigator.

### Primary files

- `prompts/payment_diagnosis/`
- `prompts/incident_investigator/v1.yaml`

### Walkthrough needed

Explain the contract and data flow for immutable prompt registry, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-04-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Reusable evaluation runner

### Goal

Produce traceable per-case and aggregate evidence.

### Expected outcome and completion checklist

- [ ] Extend the existing runner rather than creating a second eval system.
- [ ] Record prompt_version, model, dataset_version and timestamp on every run.
- [ ] Report category scores, accuracy, unsupported_claim_rate, tool_correctness, cost and latency.
- [ ] Exercise invalid output and evaluator failures with deterministic fixtures.

### Primary files

- `evals/runner.py`

### Walkthrough needed

Explain the contract and data flow for reusable evaluation runner, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-04-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Before/after and variance

### Goal

Test a plausible improvement that regresses at least one metric.

### Expected outcome and completion checklist

- [ ] Freeze dataset and settings and compare two prompt versions.
- [ ] Run repeated model trials within a declared spending allowance.
- [ ] Retain a regression even when aggregate accuracy improves.
- [ ] Classify failures and distinguish reproducible inputs from stochastic outputs.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for before/after and variance, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-04-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Promotion and rollback rehearsal

### Goal

Prove a release decision can restore the exact previous prompt.

### Expected outcome and completion checklist

- [ ] Restore the prior version and rerun the golden set.
- [ ] Verify template identity rather than only a version label.
- [ ] Save before/after results and promotion or rejection rationale.
- [ ] Record known stochastic variation and the cost/latency tradeoff in prompt-regression.md.

### Primary files

- `evals/reports/week4.md`
- `evals/reports/prompt-regression.md`

### Walkthrough needed

Explain the contract and data flow for promotion and rollback rehearsal, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-04-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-04-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Add a file-based Prompt Registry. Store name, version, created_at, model, template, status, eval_dataset, eval_score and notes in each version or associated metadata. Keep published templates immutable; status and eval evidence may live in a separate release manifest. Pin the registry version when running the application.
- Every eval run records prompt_version, model, dataset_version, timestamp, accuracy, unsupported_claim_rate, tool_correctness, cost and latency. Change a prompt, rerun the same golden dataset and produce a before/after regression report. Restore the previous version and rerun it before promoting the change. No registry service is needed.

## Curriculum contract — experiments and comparisons

- Compare two prompt versions on the same frozen dataset and settings. Preserve a change that regresses one metric even if accuracy improves; explain whether the cost/latency tradeoff is worth promotion. Verify rollback resolves the exact prior template.

## Required failure and evaluation pass

Run at least one prompt change you expect to help that makes an eval worse. Keep the before/after report and classify why.

## Curriculum deliverables

- [ ] `evals/runner.py`
- [ ] `evals/datasets/golden_set.jsonl`
- [ ] `evals/reports/week4.md`
- [ ] `evals/error_taxonomy.yml`
- [ ] `prompts/payment_diagnosis/`
- [ ] `prompts/incident_investigator/v1.yaml`
- [ ] `evals/reports/prompt-regression.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] Golden set contains at least 75 cases
- [ ] Eval execution is reproducible
- [ ] Scores are broken down by category
- [ ] Model and prompt metadata are stored
- [ ] A before/after comparison exists
- [ ] You can distinguish a better score from a lucky sample
- [ ] Every eval run identifies prompt, model and dataset versions
- [ ] A previous prompt version can be restored exactly
- [ ] Accuracy, unsupported claims, tool correctness, cost and latency regressions are visible
- [ ] Prompt changes have recorded release and rollback decisions

## Engineering note

Explain how prompt releases resemble application releases, what remains nondeterministic, and why a better accuracy score alone is insufficient.

## Optional depth — does not gate this week

Add a hosted eval service after the local runner is useful.
