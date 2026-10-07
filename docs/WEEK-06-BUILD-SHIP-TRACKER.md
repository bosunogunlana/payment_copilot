# Week 6 Build / Ship Tracker — Build RAG manually

[All weeks](BUILD-SHIP-INDEX.md) · [Week 6 plan](WEEK-06-BUILD-SHIP.md) · [Previous week](WEEK-05-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-07-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 6 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Chunk and source contract](#phase-1) | Not started | — |
| 2 | [Manual cited-answer pipeline](#phase-2) | Not started | — |
| 3 | [Authorized hybrid retrieval](#phase-3) | Not started | — |
| 4 | [Minimal reranker and four-way comparison](#phase-4) | Not started | — |
| 5 | [Chunk/top-k failure experiments](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Chunk and source contract

- [ ] Define stable document/chunk IDs, source versions and authorized metadata.
- [ ] Implement chunking with selectable 250, 500 and 1,000 sizes.
- [ ] Define cited answer, evidence and source as separate outputs.
- [ ] Freeze a small shared query set for all retrieval experiments.

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

### Phase 2 — Manual cited-answer pipeline

- [ ] Build query preprocessing → embedding → retrieval → context selection → prompt → LLM.
- [ ] Attach source identifiers to every answer.
- [ ] Handle missing or contradictory evidence without unsupported claims.
- [ ] Separate answer, evidence and source in a minimal existing interface or local presentation.

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

### Phase 3 — Authorized hybrid retrieval

- [ ] Add BM25 alongside dense retrieval and trace both branches.
- [ ] Apply trusted organization/access/version filters before reranker or model exposure.
- [ ] Merge rankings and deduplicate stable chunk IDs using a documented rule such as rank fusion.
- [ ] Test overlapping candidates, missing metadata and an out-of-tenant exact match.

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

### Phase 4 — Minimal reranker and four-way comparison

- [ ] Implement a reusable reranker interface with an appropriate minimal implementation.
- [ ] Compare BM25, Dense, Hybrid and Hybrid + reranker on identical queries.
- [ ] Include TX_ALREADY_EXISTS and paraphrased blockchain-confirmation symptoms.
- [ ] Save per-stage evidence and four-way quality, latency and cost observations.

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

### Phase 5 — Chunk/top-k failure experiments

- [ ] Compare chunk sizes 250/500/1,000 while holding top-k fixed.
- [ ] Compare top-k 3/5/10 while holding chunk size fixed.
- [ ] Reuse retrieval outputs where possible and avoid an exhaustive cross-product.
- [ ] Save rag_chunking.md and explain retrieval, source, context and generation failures separately.

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
| `app/retrieval/chunker.py` | 1 | Not started | — |
| `app/retrieval/retriever.py` | 2 | Not started | — |
| `app/rag/pipeline.py` | 2 | Not started | — |
| `experiments/rag_chunking.md` | 5 | Not started | — |
| `app/retrieval/hybrid.py` | 3 | Not started | — |
| `app/retrieval/reranker.py` | 4 | Not started | — |
| `experiments/retrieval-four-way.md` | 4 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Compare chunk sizes 250 / 500 / 1,000 and top-k 3 / 5 / 10. Keep the output and record whether the failure came from query understanding, retrieval, source quality, context, or generation.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Out-of-tenant exact-code match | — | — | Define from phase acceptance checks | — | Not started |
| Missing metadata / duplicate candidates | — | — | Define from phase acceptance checks | — | Not started |
| Contradictory source documents | — | — | Define from phase acceptance checks | — | Not started |
| Chunk sizes 250/500/1,000 | — | — | Define from phase acceptance checks | — | Not started |
| Top-k 3/5/10 | — | — | Define from phase acceptance checks | — | Not started |
| BM25 / Dense / Hybrid / Hybrid + reranker | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] Trace a wrong answer to a pipeline stage
- [ ] Answer, evidence, and source are separate in the UI
- [ ] At least three chunk sizes are compared
- [ ] At least three top-k values are compared
- [ ] Every answer carries source identifiers
- [ ] You can explain why more context can reduce quality
- [ ] BM25, dense retrieval, merging, filtering and reranking can be inspected independently
- [ ] BM25 / Dense / Hybrid / Hybrid + reranker are compared on identical payment queries
- [ ] Unauthorized candidates never enter the reranker or model context

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
