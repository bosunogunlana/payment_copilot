# Week 3 Build / Ship Plan — Practical machine-learning foundations

[All weeks](BUILD-SHIP-INDEX.md) · [Week 3 tracker](WEEK-03-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-02-BUILD-SHIP.md) · [Next week](WEEK-04-BUILD-SHIP.md)

## Scope and ship target

Generate roughly 1,000 payment-support messages across seven labels. Compare TF-IDF + logistic regression against an LLM structured classifier using train, validation, and test splits.

**Learning goal:** Build enough classical ML intuition to know when a deterministic or statistical model is the better tool.

**Before you start:** Reuse payment categories; learn only classification, splits and metrics from the crash course.

**Keep the build focused:** Generate 1,000 messages from varied templates. Split by template family before fitting TF-IDF to avoid leakage. Compare both classifiers on the same held-out subset within your budget.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 03. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Label and split contract](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Synthetic dataset and leakage checks](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Classical baseline](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Structured LLM classifier](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Error analysis and recommendation](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Label and split contract

### Goal

Define a fair seven-label comparison before generating data.

### Expected outcome and completion checklist

- [ ] Define seven payment-support labels and costly false-positive outcomes.
- [ ] Design varied synthetic template families and stable row IDs.
- [ ] Specify train, validation and test splits grouped by template family.
- [ ] Freeze the split manifest before fitting features or prompts.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for label and split contract, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-03-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Synthetic dataset and leakage checks

### Goal

Create roughly 1,000 messages without train/test template overlap.

### Expected outcome and completion checklist

- [ ] Generate roughly 1,000 labelled synthetic messages into payment_issues.csv.
- [ ] Validate counts, labels and template-family provenance.
- [ ] Assert related templates never span train and test.
- [ ] Reserve one common held-out subset for both classifiers within the model budget.

### Primary files

- `data/payment_issues.csv`

### Walkthrough needed

Explain the contract and data flow for synthetic dataset and leakage checks, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-03-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Classical baseline

### Goal

Learn features and a statistical classifier only from training data.

### Expected outcome and completion checklist

- [ ] Fit TF-IDF on the training split only.
- [ ] Train logistic regression and tune using validation data.
- [ ] Evaluate frozen predictions on held-out test messages.
- [ ] Record inference cost and latency separately from training work.

### Primary files

- `experiments/classical_classifier.py`

### Walkthrough needed

Explain the contract and data flow for classical baseline, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-03-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Structured LLM classifier

### Goal

Compare the model against the same label and split contract.

### Expected outcome and completion checklist

- [ ] Request and validate the seven-label structured output.
- [ ] Handle refusals, invalid outputs and unavailable responses explicitly.
- [ ] Freeze prompt and settings before held-out evaluation.
- [ ] Set a spending allowance and use the same held-out subset as the classical baseline.

### Primary files

- `experiments/llm_classifier.py`

### Walkthrough needed

Explain the contract and data flow for structured llm classifier, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-03-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Error analysis and recommendation

### Goal

Choose a classifier using class-level errors and operational consequences.

### Expected outcome and completion checklist

- [ ] Report confusion matrices, accuracy, precision, recall and F1 for both classifiers.
- [ ] Inspect the class where false positives are most costly.
- [ ] Explain training versus inference, overfitting and split roles.
- [ ] Write classifier-comparison.md with a deployment recommendation and a task where a $0 deterministic classifier wins.

### Primary files

- `docs/learning-notes/classifier-comparison.md`

### Walkthrough needed

Explain the contract and data flow for error analysis and recommendation, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-03-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-03-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Required failure and evaluation pass

Inspect the confusion matrix. Find the class where a false positive is most costly, then decide whether accuracy or recall should lead your deployment recommendation.

## Curriculum deliverables

- [ ] `experiments/classical_classifier.py`
- [ ] `experiments/llm_classifier.py`
- [ ] `data/payment_issues.csv`
- [ ] `docs/learning-notes/classifier-comparison.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] Explain training vs inference
- [ ] Explain train, validation, and test data
- [ ] Explain overfitting
- [ ] Explain precision vs recall and when F1 helps
- [ ] Name a task where a $0 deterministic classifier wins
- [ ] Write a deployment recommendation

## Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

## Optional depth — does not gate this week

Explore cross-validation after one clean train/validation/test comparison. Synthetic scores are not production evidence.
