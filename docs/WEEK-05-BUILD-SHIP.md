# Week 5 Build / Ship Plan — Embeddings & semantic retrieval

[All weeks](BUILD-SHIP-INDEX.md) · [Week 5 tracker](WEEK-05-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-04-BUILD-SHIP.md) · [Next week](WEEK-06-BUILD-SHIP.md)

## Scope and ship target

Create a 20-document payment knowledge corpus. Implement embed_document, embed_query, cosine_similarity, and search_similar_documents first with Python arrays, then migrate behind the same interface to PostgreSQL + pgvector.

**Learning goal:** Understand vector retrieval from first principles before reaching for a vector database.

**Before you start:** Reuse the fixture domain. You need basic arrays and SQL, not a vector-database course.

**Keep the build focused:** Write 20 short synthetic documents. Get array-based cosine search working, then use pgvector exact search through the same interface.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 05. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Corpus and retrieval interface](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Array-based cosine search](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Neighbour inspection](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [pgvector exact-search migration](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Reproducible indexing and evaluation](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Corpus and retrieval interface

### Goal

Keep document identity stable across array and database search.

### Expected outcome and completion checklist

- [ ] Create 20 short synthetic payment knowledge documents.
- [ ] Define document IDs, query inputs and ranked search outputs.
- [ ] Specify embed_document, embed_query, cosine_similarity and search_similar_documents.
- [ ] Record embedding model, dimensions and document version.

### Primary files

- `knowledge/`

### Walkthrough needed

Explain the contract and data flow for corpus and retrieval interface, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-05-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Array-based cosine search

### Goal

Understand similarity before using a vector database.

### Expected outcome and completion checklist

- [ ] Implement document and query embedding through a narrow adapter.
- [ ] Calculate cosine similarity with Python arrays.
- [ ] Handle empty input, incompatible dimensions and zero vectors explicitly.
- [ ] Return stable ranked document IDs and scores.

### Primary files

- `app/retrieval/embeddings.py`

### Walkthrough needed

Explain the contract and data flow for array-based cosine search, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-05-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Neighbour inspection

### Goal

Expose semantic false friends on payment queries.

### Expected outcome and completion checklist

- [ ] Probe delayed withdrawals, broadcast-but-processing transactions and missing callbacks.
- [ ] Inspect nearest neighbours manually.
- [ ] Compare semantic matches with keyword matches.
- [ ] Record one similar document that is operationally irrelevant.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for neighbour inspection, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-05-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: pgvector exact-search migration

### Goal

Replace storage while preserving the retrieval contract.

### Expected outcome and completion checklist

- [ ] Index the same document embeddings in PostgreSQL with pgvector.
- [ ] Implement exact search behind the existing interface.
- [ ] Compare array and database results on identical queries.
- [ ] Document exact versus approximate search without HNSW tuning.

### Primary files

- `app/retrieval/vector_store.py`

### Walkthrough needed

Explain the contract and data flow for pgvector exact-search migration, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-05-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Reproducible indexing and evaluation

### Goal

Make the small corpus and retrieval result inspectable.

### Expected outcome and completion checklist

- [ ] Provide scripts/index_documents.py for repeatable indexing.
- [ ] Record corpus and embedding versions plus query results.
- [ ] Explain embeddings as representations rather than knowledge.
- [ ] Save failures and the measured storage/interface tradeoff for Week 6.

### Primary files

- `scripts/index_documents.py`

### Walkthrough needed

Explain the contract and data flow for reproducible indexing and evaluation, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-05-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-05-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Required failure and evaluation pass

Probe queries for delayed withdrawals, broadcast-but-processing transactions, and missing callbacks. Inspect nearest neighbours manually and write down false friends.

## Curriculum deliverables

- [ ] `app/retrieval/embeddings.py`
- [ ] `app/retrieval/vector_store.py`
- [ ] `knowledge/`
- [ ] `scripts/index_documents.py`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] Explain what an embedding represents
- [ ] Implement cosine similarity
- [ ] Explain semantic vs keyword search
- [ ] Explain exact vs approximate nearest-neighbour search
- [ ] Explain why embeddings are not knowledge
- [ ] Name a case where similarity is not relevance

## Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

## Optional depth — does not gate this week

Benchmark approximate indexes later; a 20-document corpus does not need HNSW tuning.
