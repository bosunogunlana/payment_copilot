# Week 8 Build / Ship Tracker — Production RAG & multi-tenancy

[All weeks](BUILD-SHIP-INDEX.md) · [Week 8 plan](WEEK-08-BUILD-SHIP.md) · [Previous week](WEEK-07-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-09-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 8 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Tenant and document lifecycle contract](#phase-1) | Not started | — |
| 2 | [Tenant-aware search](#phase-2) | Not started | — |
| 3 | [Deletion and version replacement](#phase-3) | Not started | — |
| 4 | [Ingestion recovery and deduplication](#phase-4) | Not started | — |
| 5 | [Grounded operator rehearsal](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Tenant and document lifecycle contract

- [ ] Add organization_id, document_version, source_type, effective_date, access_level, provider and network to every chunk.
- [ ] Derive tenant/access scope from trusted identity.
- [ ] Create similar Org A and Org B documents.
- [ ] Define replacement, deletion and deduplication semantics.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-2"></a>

### Phase 2 — Tenant-aware search

- [ ] Implement retrieval filters and database row-level-security boundaries.
- [ ] Test direct search and generated answers for cross-tenant attempts.
- [ ] Assert unauthorized chunks never reach reranker or context.
- [ ] Stop progression on any isolation failure instead of averaging it into quality scores.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-3"></a>

### Phase 3 — Deletion and version replacement

- [ ] Implement deletion and re-indexing.
- [ ] Replace updated document versions without retaining stale searchable chunks.
- [ ] Test retrieval after deletion and version replacement.
- [ ] Verify generated claims retain current source IDs and versions.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-4"></a>

### Phase 4 — Ingestion recovery and deduplication

- [ ] Add bounded retries to the synchronous ingestion contract.
- [ ] Deduplicate repeated ingestion using stable identity.
- [ ] Inject ingestion failures and make them observable.
- [ ] Test retry after partial ingestion and preserve current-version consistency.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-5"></a>

### Phase 5 — Grounded operator rehearsal

- [ ] Run tenant_retrieval.jsonl through the existing eval runner.
- [ ] Verify zero cross-tenant retrieval, deleted-document absence and stale-version exclusion.
- [ ] Demonstrate one source-grounded operator answer.
- [ ] Write rag-architecture.md with identity, freshness, deletion and failure boundaries.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-6"></a>

### Phase 6 — Local ship and learning handoff

- [ ] Document setup and exact offline/test/eval commands from the project root.
- [ ] Verify the slice from a clean source checkout and record dependency/environment limitations.
- [ ] Complete the deliverable inventory and curriculum exit-criteria evidence below.
- [ ] Write the engineering note with a deliberate failure, measured tradeoff, limitations and next smallest action.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

## Deliverable inventory

Paths below are relative to the project root; they are target artifacts, not claims that files already exist.

| Curriculum deliverable | Primary phase | Status | Evidence |
| --- | --- | --- | --- |
| `app/ingestion/` | 4 | Not started | — |
| `app/retrieval/filters.py` | 2 | Not started | — |
| `evals/security/tenant_retrieval.jsonl` | 5 | Not started | — |
| `docs/rag-architecture.md` | 6 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Create Org A and Org B with deliberately similar documents. Attempt cross-tenant leakage, stale-version retrieval, duplicate ingestion, and retrieval after deletion.

Use the plan’s phase checks to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Cross-tenant similar-document leakage | — | — | Define from phase acceptance checks | — | Not started |
| Retrieval after deletion | — | — | Define from phase acceptance checks | — | Not started |
| Stale version after replacement | — | — | Define from phase acceptance checks | — | Not started |
| Repeated ingestion / partial failure and retry | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] Zero cross-tenant retrieval in tests
- [ ] Deleted documents disappear from search
- [ ] Updated documents replace stale versions
- [ ] Generated claims identify their source
- [ ] Ingestion failures are observable
- [ ] Paqet Copilot v0.2 can ground an operator answer

| Criterion or metric | Supporting phase / evidence | Result / denominator | Remaining gap |
| --- | --- | --- | --- |
| Add a row for each verified criterion | — | — | — |

## Session log

Append verified work without rewriting earlier evidence.

| Date | Phase | Timebox | Completed / reviewed | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | — |

## Definition of done

- [ ] All six phase checklists and exit gates have reviewed evidence.
- [ ] Every curriculum deliverable is present and its purpose verified.
- [ ] Every curriculum exit criterion above is supported by evidence.
- [ ] Required failure cases and experiments have saved results, including misses and limitations.
- [ ] Setup, commands and environment assumptions are documented and verified from clean source.
- [ ] The engineering note explains the primitive, deliberate failure, measurements and tradeoff.
- [ ] The next smallest action and remaining gaps are recorded.
- [ ] Supported browser checkpoints are identified; no browser completion or production readiness is inferred.
