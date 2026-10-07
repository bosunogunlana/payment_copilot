# Week 7 Build / Ship Plan — Retrieval evaluation

[All weeks](BUILD-SHIP-INDEX.md) · [Week 7 tracker](WEEK-07-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-06-BUILD-SHIP.md) · [Next week](WEEK-08-BUILD-SHIP.md)

## Scope and ship target

Create 50 retrieval-specific test cases with relevant document IDs and required facts. Calculate Precision@K, Recall@K, MRR, correctness, faithfulness, citation correctness, and completeness.

**Learning goal:** Evaluate the retrieval layer separately from generation so “bad answer” has a diagnosable cause.

**Before you start:** Freeze the Week 6 baseline and document IDs.

**Keep the build focused:** Label 50 queries. Separate answerable retrieval cases from unanswerable refusal cases. Learning targets: Recall@5 ≥0.85, citation precision ≥0.90, unsupported answers ≤0.10. Record denominators and misses, not just a score. Extend Week 6 code and the existing 50 queries. Use a subset for candidate-budget sweeps, then one full comparison.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 07. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Frozen relevance judgments](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Retrieval and answer graders](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Cross-encoder candidate pipeline](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Controlled four-way measurement](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Miss analysis and targeted fix](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Frozen relevance judgments

### Goal

Make ranking scores meaningful before tuning retrieval.

### Expected outcome and completion checklist

- [ ] Extend the existing dataset to 50 retrieval-specific queries.
- [ ] Label relevant document IDs, required facts and graded relevance 0/1/2.
- [ ] Define binary relevance thresholds and zero-relevance handling.
- [ ] Separate unanswerable refusal cases from answerable retrieval denominators.

### Primary files

- `evals/retrieval/graded_relevance.jsonl`

### Walkthrough needed

Explain the contract and data flow for frozen relevance judgments, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-07-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Retrieval and answer graders

### Goal

Measure retrieval independently of generated answers.

### Expected outcome and completion checklist

- [ ] Calculate Precision@K, Recall@K, MRR and NDCG@5.
- [ ] Work a toy graded-relevance NDCG example before using a helper.
- [ ] Grade correctness, faithfulness, citation correctness and completeness separately.
- [ ] Test conflicting, outdated and vocabulary-overlap documents.

### Primary files

- `evals/retrieval/`
- `evals/rag/`

### Walkthrough needed

Explain the contract and data flow for retrieval and answer graders, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-07-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Cross-encoder candidate pipeline

### Goal

Rerank authorized candidates while preserving candidate-recall limits.

### Expected outcome and completion checklist

- [ ] Reuse Week 6 reranker and cross-encode query/document pairs.
- [ ] Retrieve up to 50 distinct authorized candidates and return top 5.
- [ ] Expand the synthetic corpus with distractors if needed for a full 50-candidate pass.
- [ ] Show a relevant document absent from candidates cannot be rescued by reranking.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for cross-encoder candidate pipeline, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-07-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Controlled four-way measurement

### Goal

Compare relevance gains against total latency and cost.

### Expected outcome and completion checklist

- [ ] Sweep candidate budgets 5/20/50 on a small diagnostic subset.
- [ ] Run BM25, Dense, Hybrid and Hybrid + rerank on the same 50 held-out queries.
- [ ] Hold corpus, filters and generation settings fixed.
- [ ] Report Recall@5, MRR, NDCG@5, Precision@K and generation metrics with retrieval-plus-reranking latency and compute/API cost.

### Primary files

- `evals/reports/reranking-comparison.md`

### Walkthrough needed

Explain the contract and data flow for controlled four-way measurement, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-07-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Miss analysis and targeted fix

### Goal

Use learning targets to choose one evidence-based improvement.

### Expected outcome and completion checklist

- [ ] Report denominators and misses against Recall@5 ≥0.85, citation precision ≥0.90 and unsupported answers ≤0.10.
- [ ] Separate candidate-recall, ranking and generation errors.
- [ ] If a target is missed, analyze it and rerun one targeted fix.
- [ ] Save week7.md and reranking-comparison.md with the measured bi-encoder/cross-encoder tradeoff.

### Primary files

- `evals/reports/week7.md`

### Walkthrough needed

Explain the contract and data flow for miss analysis and targeted fix, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-07-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-07-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Extend the 50-case retrieval dataset with graded relevance labels (for example 0 irrelevant, 1 useful, 2 directly answers). Document the binary threshold used for Recall/Precision/MRR. Retrieve up to 50 distinct authorized candidates cheaply, cross-encode query/document pairs, then return the top 5. Expand the synthetic corpus with distractors if needed to exercise a full 50-candidate pass.
- Keep the same held-out queries, corpus, filters and generation settings for all four retrieval variants. Report Recall@5, MRR and NDCG@5 alongside latency and cost; also retain Precision@K and the existing generation metrics. Define zero-relevance handling and report unanswerable cases separately. Any suitable cross-encoder implementation is acceptable; no local model serving stack is required.

## Curriculum contract — experiments and comparisons

- Run BM25, Dense, Hybrid and Hybrid + rerank. Compare 5/20/50 candidate budgets on a small diagnostic subset, include total retrieval plus reranking latency, and record the reranker’s compute/API cost. Show a case where reranking cannot rescue a document missing from the candidate set.

## Required failure and evaluation pass

Add unanswerable questions, conflicting documents, outdated documents, and irrelevant documents that share vocabulary. Report retrieval failure separately from generation failure.

## Curriculum deliverables

- [ ] `evals/retrieval/`
- [ ] `evals/rag/`
- [ ] `evals/reports/week7.md`
- [ ] `evals/retrieval/graded_relevance.jsonl`
- [ ] `evals/reports/reranking-comparison.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] Dataset contains 50 retrieval cases
- [ ] Recall@5 is measured
- [ ] Citation precision is measured
- [ ] Unanswerable questions are represented
- [ ] Retrieval and generation failures are separate
- [ ] Your report includes an error taxonomy and next action
- [ ] NDCG@5 is calculated with documented graded relevance and zero-relevance handling
- [ ] A cross-encoder reranks up to 50 candidates into a top-5 result
- [ ] All four retrieval variants have Recall@5, MRR, NDCG, latency and cost comparisons
- [ ] Explain the measured bi-encoder vs cross-encoder tradeoff

## Engineering note

Record whether the reranker improves relevance enough to justify its extra work; separate candidate-recall limits from ranking errors.

## Optional depth — does not gate this week

If a target is missed, write a failure analysis and rerun one targeted fix. These are learning targets, not production certification.
