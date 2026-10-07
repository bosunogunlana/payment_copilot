# Week 8 Build / Ship Plan — Production RAG & multi-tenancy

[All weeks](BUILD-SHIP-INDEX.md) · [Week 8 tracker](WEEK-08-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-07-BUILD-SHIP.md) · [Next week](WEEK-09-BUILD-SHIP.md)

## Scope and ship target

Add organization_id, document_version, source_type, effective_date, access_level, provider, and network to every chunk. Implement tenant-aware search, re-indexing, deletion, retries, version replacement, and deduplication.

**Learning goal:** Turn “chat with documents” into a trustworthy knowledge subsystem with identity, freshness, and deletion semantics.

**Before you start:** Use the authorization boundary from Week 2 and the Week 7 eval runner.

**Keep the build focused:** Finish tenant filtering, deletion and version replacement first, then retry/deduplication. A failed isolation test is a stop gate, not an acceptable averaged score.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 08. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Tenant and document lifecycle contract](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Tenant-aware search](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Deletion and version replacement](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Ingestion recovery and deduplication](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Grounded operator rehearsal](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Tenant and document lifecycle contract

### Goal

Specify who can retrieve each chunk and which version is current.

### Expected outcome and completion checklist

- [ ] Add organization_id, document_version, source_type, effective_date, access_level, provider and network to every chunk.
- [ ] Derive tenant/access scope from trusted identity.
- [ ] Create similar Org A and Org B documents.
- [ ] Define replacement, deletion and deduplication semantics.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for tenant and document lifecycle contract, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-08-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Tenant-aware search

### Goal

Enforce scope before evidence reaches ranking or generation.

### Expected outcome and completion checklist

- [ ] Implement retrieval filters and database row-level-security boundaries.
- [ ] Test direct search and generated answers for cross-tenant attempts.
- [ ] Assert unauthorized chunks never reach reranker or context.
- [ ] Stop progression on any isolation failure instead of averaging it into quality scores.

### Primary files

- `app/retrieval/filters.py`

### Walkthrough needed

Explain the contract and data flow for tenant-aware search, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-08-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Deletion and version replacement

### Goal

Remove stale evidence from every search path.

### Expected outcome and completion checklist

- [ ] Implement deletion and re-indexing.
- [ ] Replace updated document versions without retaining stale searchable chunks.
- [ ] Test retrieval after deletion and version replacement.
- [ ] Verify generated claims retain current source IDs and versions.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for deletion and version replacement, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-08-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Ingestion recovery and deduplication

### Goal

Recover ingestion failures without creating duplicate evidence.

### Expected outcome and completion checklist

- [ ] Add bounded retries to the synchronous ingestion contract.
- [ ] Deduplicate repeated ingestion using stable identity.
- [ ] Inject ingestion failures and make them observable.
- [ ] Test retry after partial ingestion and preserve current-version consistency.

### Primary files

- `app/ingestion/`

### Walkthrough needed

Explain the contract and data flow for ingestion recovery and deduplication, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-08-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Grounded operator rehearsal

### Goal

Demonstrate the v0.2 knowledge boundary with adversarial tenant fixtures.

### Expected outcome and completion checklist

- [ ] Run tenant_retrieval.jsonl through the existing eval runner.
- [ ] Verify zero cross-tenant retrieval, deleted-document absence and stale-version exclusion.
- [ ] Demonstrate one source-grounded operator answer.
- [ ] Write rag-architecture.md with identity, freshness, deletion and failure boundaries.

### Primary files

- `evals/security/tenant_retrieval.jsonl`

### Walkthrough needed

Explain the contract and data flow for grounded operator rehearsal, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-08-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

- `docs/rag-architecture.md`

### Walkthrough needed

Explain the contract and data flow for local ship and learning handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-08-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Required failure and evaluation pass

Create Org A and Org B with deliberately similar documents. Attempt cross-tenant leakage, stale-version retrieval, duplicate ingestion, and retrieval after deletion.

## Curriculum deliverables

- [ ] `app/ingestion/`
- [ ] `app/retrieval/filters.py`
- [ ] `evals/security/tenant_retrieval.jsonl`
- [ ] `docs/rag-architecture.md`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] Zero cross-tenant retrieval in tests
- [ ] Deleted documents disappear from search
- [ ] Updated documents replace stale versions
- [ ] Generated claims identify their source
- [ ] Ingestion failures are observable
- [ ] Paqet Copilot v0.2 can ground an operator answer

## Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

## Optional depth — does not gate this week

A background ingestion worker can follow the synchronous contract tests.
