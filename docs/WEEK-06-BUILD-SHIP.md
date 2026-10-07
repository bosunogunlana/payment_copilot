# Week 6 Build / Ship Plan — Build RAG manually

[All weeks](BUILD-SHIP-INDEX.md) · [Week 6 tracker](WEEK-06-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-05-BUILD-SHIP.md) · [Next week](WEEK-07-BUILD-SHIP.md)

## Scope and ship target

Build Payment Knowledge Assistant as a manual pipeline: query preprocessing → embedding → retrieval → context selection → prompt construction → LLM → answer + citations.

**Learning goal:** Trace every stage from a question to a cited answer before adding a framework.

**Before you start:** Use Week 5 corpus and search interface.

**Keep the build focused:** Build one cited-answer pipeline. Change chunk size while holding top-k fixed, then change top-k with chunk size fixed. Reuse query results to control cost. Use the existing small corpus and query set for the first four-way comparison. Week 7 expands measurement; skip search infrastructure tuning.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 06. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Chunk and source contract](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Manual cited-answer pipeline](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Authorized hybrid retrieval](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Minimal reranker and four-way comparison](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Chunk/top-k failure experiments](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Chunk and source contract

### Goal

Reuse the corpus with inspectable citation and access boundaries.

### Expected outcome and completion checklist

- [ ] Define stable document/chunk IDs, source versions and authorized metadata.
- [ ] Implement chunking with selectable 250, 500 and 1,000 sizes.
- [ ] Define cited answer, evidence and source as separate outputs.
- [ ] Freeze a small shared query set for all retrieval experiments.

### Primary files

- `app/retrieval/chunker.py`

### Walkthrough needed

Explain the contract and data flow for chunk and source contract, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-06-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Manual cited-answer pipeline

### Goal

Trace a question through retrieval and generation without a framework.

### Expected outcome and completion checklist

- [ ] Build query preprocessing → embedding → retrieval → context selection → prompt → LLM.
- [ ] Attach source identifiers to every answer.
- [ ] Handle missing or contradictory evidence without unsupported claims.
- [ ] Separate answer, evidence and source in a minimal existing interface or local presentation.

### Primary files

- `app/retrieval/retriever.py`
- `app/rag/pipeline.py`

### Walkthrough needed

Explain the contract and data flow for manual cited-answer pipeline, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-06-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Authorized hybrid retrieval

### Goal

Combine exact-code and semantic evidence without mixing raw scores.

### Expected outcome and completion checklist

- [ ] Add BM25 alongside dense retrieval and trace both branches.
- [ ] Apply trusted organization/access/version filters before reranker or model exposure.
- [ ] Merge rankings and deduplicate stable chunk IDs using a documented rule such as rank fusion.
- [ ] Test overlapping candidates, missing metadata and an out-of-tenant exact match.

### Primary files

- `app/retrieval/hybrid.py`

### Walkthrough needed

Explain the contract and data flow for authorized hybrid retrieval, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-06-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Minimal reranker and four-way comparison

### Goal

Measure the added ranking stage on the same payment queries.

### Expected outcome and completion checklist

- [ ] Implement a reusable reranker interface with an appropriate minimal implementation.
- [ ] Compare BM25, Dense, Hybrid and Hybrid + reranker on identical queries.
- [ ] Include TX_ALREADY_EXISTS and paraphrased blockchain-confirmation symptoms.
- [ ] Save per-stage evidence and four-way quality, latency and cost observations.

### Primary files

- `app/retrieval/reranker.py`
- `experiments/retrieval-four-way.md`

### Walkthrough needed

Explain the contract and data flow for minimal reranker and four-way comparison, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-06-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Chunk/top-k failure experiments

### Goal

Identify the stage responsible for wrong answers.

### Expected outcome and completion checklist

- [ ] Compare chunk sizes 250/500/1,000 while holding top-k fixed.
- [ ] Compare top-k 3/5/10 while holding chunk size fixed.
- [ ] Reuse retrieval outputs where possible and avoid an exhaustive cross-product.
- [ ] Save rag_chunking.md and explain retrieval, source, context and generation failures separately.

### Primary files

- `experiments/rag_chunking.md`

### Walkthrough needed

Explain the contract and data flow for chunk/top-k failure experiments, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-06-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-06-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Keep the manual cited-answer pipeline. Add a BM25 branch beside dense search. Trace each independently before merging. Apply the same trusted organization/access/version metadata filters to both branches before candidates reach a reranker or model. Deduplicate by stable document/chunk ID and merge rankings (for example reciprocal-rank fusion); do not blindly add incomparable raw scores.
- Add a reranker interface and run a minimal appropriate reranking implementation. Compare BM25 only, Dense only, Hybrid and Hybrid + reranker on identical queries. Reuse that reranker in Week 7 for the cross-encoder experiment; do not require a new search service or specific model/library.

## Curriculum contract — experiments and comparisons

- Compare exact-code queries such as TX_ALREADY_EXISTS with “payment was sent but blockchain confirmation never completed.” Include overlapping candidates, missing metadata, contradictory documents and an out-of-tenant exact match. Keep the chunk-size/top-k experiments already assigned; vary one factor at a time rather than running every combination.

## Required failure and evaluation pass

Compare chunk sizes 250 / 500 / 1,000 and top-k 3 / 5 / 10. Keep the output and record whether the failure came from query understanding, retrieval, source quality, context, or generation.

## Curriculum deliverables

- [ ] `app/retrieval/chunker.py`
- [ ] `app/retrieval/retriever.py`
- [ ] `app/rag/pipeline.py`
- [ ] `experiments/rag_chunking.md`
- [ ] `app/retrieval/hybrid.py`
- [ ] `app/retrieval/reranker.py`
- [ ] `experiments/retrieval-four-way.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] Trace a wrong answer to a pipeline stage
- [ ] Answer, evidence, and source are separate in the UI
- [ ] At least three chunk sizes are compared
- [ ] At least three top-k values are compared
- [ ] Every answer carries source identifiers
- [ ] You can explain why more context can reduce quality
- [ ] BM25, dense retrieval, merging, filtering and reranking can be inspected independently
- [ ] BM25 / Dense / Hybrid / Hybrid + reranker are compared on identical payment queries
- [ ] Unauthorized candidates never enter the reranker or model context

## Engineering note

Explain which queries each approach wins, why rank fusion was chosen, and where reranking earns its latency.

## Optional depth — does not gate this week

The full RAG course, new search services and advanced query rewriting remain optional. Hybrid retrieval and the reranker experiment are required.
