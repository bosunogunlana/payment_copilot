# Week 5 Build / Ship Tracker — Embeddings & semantic retrieval

[All weeks](BUILD-SHIP-INDEX.md) · [Week 5 plan](WEEK-05-BUILD-SHIP.md) · [Previous week](WEEK-04-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-06-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 5 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Corpus and retrieval interface](#phase-1) | Not started | — |
| 2 | [Array-based cosine search](#phase-2) | Not started | — |
| 3 | [Neighbour inspection](#phase-3) | Not started | — |
| 4 | [pgvector exact-search migration](#phase-4) | Not started | — |
| 5 | [Reproducible indexing and evaluation](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Corpus and retrieval interface

- [ ] Create 20 short synthetic payment knowledge documents.
- [ ] Define document IDs, query inputs and ranked search outputs.
- [ ] Specify embed_document, embed_query, cosine_similarity and search_similar_documents.
- [ ] Record embedding model, dimensions and document version.

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

### Phase 2 — Array-based cosine search

- [ ] Implement document and query embedding through a narrow adapter.
- [ ] Calculate cosine similarity with Python arrays.
- [ ] Handle empty input, incompatible dimensions and zero vectors explicitly.
- [ ] Return stable ranked document IDs and scores.

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

### Phase 3 — Neighbour inspection

- [ ] Probe delayed withdrawals, broadcast-but-processing transactions and missing callbacks.
- [ ] Inspect nearest neighbours manually.
- [ ] Compare semantic matches with keyword matches.
- [ ] Record one similar document that is operationally irrelevant.

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

### Phase 4 — pgvector exact-search migration

- [ ] Index the same document embeddings in PostgreSQL with pgvector.
- [ ] Implement exact search behind the existing interface.
- [ ] Compare array and database results on identical queries.
- [ ] Document exact versus approximate search without HNSW tuning.

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

### Phase 5 — Reproducible indexing and evaluation

- [ ] Provide scripts/index_documents.py for repeatable indexing.
- [ ] Record corpus and embedding versions plus query results.
- [ ] Explain embeddings as representations rather than knowledge.
- [ ] Save failures and the measured storage/interface tradeoff for Week 6.

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
| `app/retrieval/embeddings.py` | 2 | Not started | — |
| `app/retrieval/vector_store.py` | 4 | Not started | — |
| `knowledge/` | 1 | Not started | — |
| `scripts/index_documents.py` | 5 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Probe queries for delayed withdrawals, broadcast-but-processing transactions, and missing callbacks. Inspect nearest neighbours manually and write down false friends.

Use the plan’s phase checks to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Zero vector / mismatched dimensions | — | — | Define from phase acceptance checks | — | Not started |
| Similar document is irrelevant | — | — | Define from phase acceptance checks | — | Not started |
| Missing callback / delayed withdrawal / broadcast but processing | — | — | Define from phase acceptance checks | — | Not started |
| Array versus pgvector exact-search parity | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] Explain what an embedding represents
- [ ] Implement cosine similarity
- [ ] Explain semantic vs keyword search
- [ ] Explain exact vs approximate nearest-neighbour search
- [ ] Explain why embeddings are not knowledge
- [ ] Name a case where similarity is not relevance

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
