# Week 7 Build / Ship Tracker — Retrieval evaluation

[All weeks](BUILD-SHIP-INDEX.md) · [Week 7 plan](WEEK-07-BUILD-SHIP.md) · [Previous week](WEEK-06-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-08-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 7 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Frozen relevance judgments](#phase-1) | Not started | — |
| 2 | [Retrieval and answer graders](#phase-2) | Not started | — |
| 3 | [Cross-encoder candidate pipeline](#phase-3) | Not started | — |
| 4 | [Controlled four-way measurement](#phase-4) | Not started | — |
| 5 | [Miss analysis and targeted fix](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Frozen relevance judgments

- [ ] Extend the existing dataset to 50 retrieval-specific queries.
- [ ] Label relevant document IDs, required facts and graded relevance 0/1/2.
- [ ] Define binary relevance thresholds and zero-relevance handling.
- [ ] Separate unanswerable refusal cases from answerable retrieval denominators.

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

### Phase 2 — Retrieval and answer graders

- [ ] Calculate Precision@K, Recall@K, MRR and NDCG@5.
- [ ] Work a toy graded-relevance NDCG example before using a helper.
- [ ] Grade correctness, faithfulness, citation correctness and completeness separately.
- [ ] Test conflicting, outdated and vocabulary-overlap documents.

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

### Phase 3 — Cross-encoder candidate pipeline

- [ ] Reuse Week 6 reranker and cross-encode query/document pairs.
- [ ] Retrieve up to 50 distinct authorized candidates and return top 5.
- [ ] Expand the synthetic corpus with distractors if needed for a full 50-candidate pass.
- [ ] Show a relevant document absent from candidates cannot be rescued by reranking.

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

### Phase 4 — Controlled four-way measurement

- [ ] Sweep candidate budgets 5/20/50 on a small diagnostic subset.
- [ ] Run BM25, Dense, Hybrid and Hybrid + rerank on the same 50 held-out queries.
- [ ] Hold corpus, filters and generation settings fixed.
- [ ] Report Recall@5, MRR, NDCG@5, Precision@K and generation metrics with retrieval-plus-reranking latency and compute/API cost.

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

### Phase 5 — Miss analysis and targeted fix

- [ ] Report denominators and misses against Recall@5 ≥0.85, citation precision ≥0.90 and unsupported answers ≤0.10.
- [ ] Separate candidate-recall, ranking and generation errors.
- [ ] If a target is missed, analyze it and rerun one targeted fix.
- [ ] Save week7.md and reranking-comparison.md with the measured bi-encoder/cross-encoder tradeoff.

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
| `evals/retrieval/` | 2 | Not started | — |
| `evals/rag/` | 2 | Not started | — |
| `evals/reports/week7.md` | 5 | Not started | — |
| `evals/retrieval/graded_relevance.jsonl` | 1 | Not started | — |
| `evals/reports/reranking-comparison.md` | 4 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Add unanswerable questions, conflicting documents, outdated documents, and irrelevant documents that share vocabulary. Report retrieval failure separately from generation failure.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Unanswerable query / zero relevant documents | — | — | Define from phase acceptance checks | — | Not started |
| Conflicting or outdated documents | — | — | Define from phase acceptance checks | — | Not started |
| Irrelevant vocabulary overlap | — | — | Define from phase acceptance checks | — | Not started |
| Relevant document missing from candidates | — | — | Define from phase acceptance checks | — | Not started |
| Candidate budgets 5/20/50 | — | — | Define from phase acceptance checks | — | Not started |
| Four retrieval variants on identical queries | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

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
