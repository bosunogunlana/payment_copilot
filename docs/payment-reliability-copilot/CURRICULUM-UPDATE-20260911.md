# Additive curriculum update — 11 September 2026

## Scope and preservation

The source of truth is the existing 16-week syllabus in this project, including the earlier study guidance. No course replacement, extra weeks, new runtime framework, deployment or live Paqet integration. The learner continues building one simulator-first Payment Reliability Copilot behind Domain Interfaces with SimulatorAdapter primary and PaqetAdapter when ready.

All original goals, resources, assignment text, experiments, deliverables, exit criteria and positional checkpoint keys are retained. `curriculum-updates.js` appends requirements after `study.js` enriches the original data. Contradictory study guidance is narrowly overridden: hybrid retrieval/reranking is now required, and Week 16 implements a bounded flywheel/fallback slice before the feature freeze. Supplemental references are labelled Required, Recommended or Optional.

The existing storage key, schema, notes and backup format are unchanged. New deliverable/exit checks start unchecked; older checks are not transferred to new requirements. Required-reading additions enter the denominator; recommended/optional reading checks remain saved but do not gate completion. A fully completed old course therefore reopens only the 11 updated weeks, preserving the other 5 completed weeks.

## Required additions by week

| Week | Integrated extension | Evidence the learner produces |
| --- | --- | --- |
| 2 | Typed tool errors; timeout/500/malformed/empty/invalid/unauthorized/repeat/duplicate recovery | Error contract and recovery/idempotency trace report |
| 4 | Prompt Registry; release/rollback; model/prompt/dataset versioned evals | Registry files and same-dataset regression comparison |
| 6 | BM25 + dense search, merging, trusted filters and reranker interface | Four-way retrieval comparison on payment codes and paraphrases |
| 7 | Cross-encoder reranking, graded relevance and NDCG | 50-candidate/top-5 pass with Recall@5, MRR, NDCG, latency and cost |
| 9 | Context Assembler, token budget, authority and freshness | Overflow cases, inspectable failed-call context and six context metrics |
| 10 | Evidence-based trajectory quality, not lucky answers | Six trajectory metrics and a trajectory grader |
| 11 | LangGraph vs Temporal-style durable execution concepts | Engineering note on seven durability concepts; no new engine |
| 13 | Cheap/normal/strong Model Router; escalation; CI regression/security gates | Router-vs-strongest report and positive/negative CI gate tests |
| 14 | AI latency/streaming signals; state-aware Semantic Cache experiment | Cache-off/on cost/latency/hit/stale-hit report and dashboard |
| 15 | Application-controlled tool least privilege | Seven attack categories and replay-resistant simulated mutations |
| 16 | Curated observations-to-evals flywheel; fallback hierarchy | Reviewed synthetic cases and preferred/fallback/human rehearsal |

## Coherence and workload

Use roughly 2 hours of focused reading, 4–5 implementation, 1–2 failure testing/evals and 1 hour of notes. Reuse one corpus, one growing dataset, one router and one trace store. Compare retrieval on a small set in Week 6 before the fuller Week 7 evaluation. Route with simple rules in Week 13; reuse that router for Week 16 fallback. The Semantic Cache experiment is required, but enabling it in the eventual runtime is conditional on demonstrated safety and benefit. Temporal is conceptual only; local model serving, training/fine-tuning, multi-agent consensus, voice/computer-use/A2A and GPU engineering stay optional further study with no checkpoints.

The app prominently states: “Build the important abstraction yourself once. Measure where it fails. Then adopt the framework.” An expandable architecture view shows the interfaces/adapters, router, runtime, Context Assembler, tools, retrieval branches, reranker, optional guarded cache, telemetry, eval system and release gates. Each week displays reading outcomes and an engineering-note prompt; updated weeks add implementation, experiment, metric and reference-shape sections inside the existing layout.

## Reading sources

New references were checked against primary sources; use equivalent appropriate implementations rather than treating libraries as requirements:

- [BM25 reference](https://github.com/dorianbrown/rank_bm25) and [retrieve/rerank concepts](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)
- [NDCG](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html)
- [Retries/backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Durable workflow concepts](https://docs.temporal.io/workflow-execution)
- [CI exit codes](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/set-exit-codes)
- [Semantic cache concepts](https://redis.io/docs/latest/develop/ai/redisvl/concepts/extensions/)
- [Tool least privilege / excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## Verification

19 Node regression tests cover the original behavior plus a frozen pre-update content comparison, every legacy checkpoint’s position, old completed-course migration, note/backup preservation, appended progress arithmetic, Required/Recommended/Optional behavior, all-week rendering and technical requirement coverage. JavaScript syntax checks pass. No localStorage mutation is performed by these tests: they use isolated in-memory storage.

The installed Desktop project passes all 19 tests and syntax checks for all four JavaScript files. Live-browser checks visited all 11 updated weeks and confirmed their extension sections and metrics, then checked an unchanged week for hidden extensions. The Week 9 context-budget example was inspected at 390px width with no horizontal page overflow. The browser console reported no errors. Browser checks did not change any completion checks or notes; the native backup file-picker flow was not retested.

The project remains a standalone folder, not a Git repository. The implementation skill’s Git workflow is inapplicable, so direct scoped edits and verification are used. New UI controls reuse the design-system skill’s existing tokens and class namespace. No Git commit, push, hosting change or course implementation service is included.
