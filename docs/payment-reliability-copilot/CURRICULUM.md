# AI Engineering Curriculum — Payment Reliability Copilot

**Consolidated learner-facing syllabus · 16 weeks · 8–10 hours per week**

This document is the consolidated snapshot of the existing curriculum and its additive September 2026 updates. It is generated from the seeded course data in `study.js` and `curriculum-updates.js`; the browser app remains the interactive source for completion state.

## Purpose and learner profile

Build and explain a production-minded **Payment Reliability Copilot** through one continuous, simulator-first project. The course assumes strong experience with Ruby on Rails, backend and distributed systems, payments and ledgers, PostgreSQL, Redis, Docker, Kubernetes, Go, Prometheus/Grafana, observability, and incident response. The learning target is AI engineering in real systems—not generic chatbot tutorials or machine-learning research.

## Non-negotiable architecture

Paqet is still under development, so it must never block the course. The simulator is the primary controlled environment; Paqet becomes an adapter when its APIs and authorization contract are ready.
```text
Payment Copilot → Domain Interfaces
                   ├─ SimulatorAdapter (primary controlled environment)
                   └─ PaqetAdapter (when ready; never a course blocker)

User → API / Auth Layer → Model Router → Agent Runtime
                                          ├─ Context Assembler
                                          └─ Least-privilege Tools → Domain Interfaces
                  Retrieval Pipeline ←─────┘
                   ├─ BM25 / lexical
                   └─ Dense search
                         ↓ merge + authorized metadata filtering
                      Reranker → top-K evidence → Agent
                         ↓
          Optional Semantic Cache (state / identity / freshness policy)
                         ↓
                       Output

Cache lookup/reuse is guarded before an agent run; valid results may
be stored afterward. It never bypasses authorization or state checks.

Every stage emits model, prompt version, tool trajectory, retrieval
trace, token counts, context size, latency, cost, cache behavior,
errors and final outcome (use N/A when a field does not apply).
                         ↓
Evaluation System → regression tests + hard security gates
                         ↓
                   release decision
```

## Curriculum philosophy

```text
Problem
  ↓
Primitive
  ↓
Implement it manually
  ↓
Break it deliberately
  ↓
Evaluate it
  ↓
Understand tradeoffs
  ↓
Adopt abstraction/framework
```
> **Build the important abstraction yourself once. Measure where it fails. Then adopt the framework.**
Examples: manual tool loop → agent framework; manual cosine similarity → pgvector; dense retrieval → hybrid retrieval; manual agent state → LangGraph; raw tool integration → MCP. Every new concept must solve a failure encountered in the same project.

## Weekly operating rhythm

Plan approximately:
- **Learn / read — about 2 hours:** read the focus sections, not entire courses.
- **Build — 4–5 hours:** extend the same project, fixtures, interfaces, corpus, router, and trace store.
- **Break and evaluate — 1–2 hours:** run the failure pass and experiments; save evidence.
- **Reflect — about 1 hour:** check deliverables, explain exit criteria, and write the engineering note.
These are bounded learning budgets, not promises that every linked course must be completed cover-to-cover.

## How progress works in the app

- Each week contains Goal, Learning resources, Reading outcomes, Implementation assignment, Failure pass, Deliverables, Exit criteria, Engineering notes, and Progress.
- Required resources and all assignment/deliverable/exit checks contribute to core progress. Recommended and Optional readings are tracked separately and do not gate completion.
- New checks are appended. Existing checkpoint IDs, completion state, active week, notes, and backup format remain intact. A previously complete week can reopen only for newly added requirements.
- Notes are week-specific and autosaved in browser storage. Export before changing browser/origin or clearing data; restore replaces the current browser state rather than merging it.
- Use **Continue learning** to jump to the actual next unfinished required checkpoint.

## Four-month roadmap

| Month | Weeks | Arc |
| --- | --- | --- |
| 01 | 01—04 | LLMs as software |
| 02 | 05—08 | Grounding & RAG |
| 03 | 09—12 | Agentic systems |
| 04 | 13—16 | Production AI |

| Week | Focus |
| --- | --- |
| 01 | Models, prompting & structured output — Treat the LLM as an unreliable software component with measurable behavior—not as a chatbot. |
| 02 | Function calling & tool design — Understand the core mechanism behind agents: the model requests work, your application validates and executes it. |
| 03 | Practical machine-learning foundations — Build enough classical ML intuition to know when a deterministic or statistical model is the better tool. |
| 04 | Evaluation-driven development — Make evals part of development so a prompt change can be judged objectively. |
| 05 | Embeddings & semantic retrieval — Understand vector retrieval from first principles before reaching for a vector database. |
| 06 | Build RAG manually — Trace every stage from a question to a cited answer before adding a framework. |
| 07 | Retrieval evaluation — Evaluate the retrieval layer separately from generation so “bad answer” has a diagnosable cause. |
| 08 | Production RAG & multi-tenancy — Turn “chat with documents” into a trustworthy knowledge subsystem with identity, freshness, and deletion semantics. |
| 09 | Build an agent yourself — Understand an agent without framework magic: state, decisions, validated actions, observations, and termination. |
| 10 | Incident investigation agent — Move from a single payment diagnosis to a system-level production investigation with metrics, logs, history, and provider state. |
| 11 | LangGraph & durable workflows — Learn the framework after understanding the primitive it abstracts: stateful, long-running, resumable workflows. |
| 12 | MCP + Go — Turn payment-domain capabilities into reusable AI infrastructure and connect your Go learning to a real boundary. |
| 13 | Serious evals — Expand from a demo-sized golden set to an evaluation system that measures the whole agent environment. |
| 14 | AI observability — Make every model call, tool call, retrieval, and escalation visible enough to operate in production. |
| 15 | AI security & reliability — Attack the system before an operator—or a malicious prompt—does it for you. |
| 16 | Ship the Payment Reliability Copilot — Bring the system together into a credible, explainable, observable capstone you can demo and defend. |

# Detailed 16-week syllabus

## Week 01 — Models, prompting & structured output

**Month 1: LLMs as software**

**Goal:** Treat the LLM as an unreliable software component with measurable behavior—not as a chatbot.

**Before you start:** Python functions, JSON, a virtual environment and one passing test. Use synthetic data and keep API keys outside source control.

**Keep the build focused:** One command that diagnoses a fixture and saves a typed result. Start with 5 cases, then reach 30; set a spending limit before model comparisons.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenAI Developer Quickstart](https://developers.openai.com/api/docs/quickstart)** — Responses API + Python SDK
- [ ] **Required — [Prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering)** — Instruction hierarchy, context, examples
- [ ] **Required — [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)** — JSON-schema constrained generation
- [ ] **Optional — [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)** — Application-side validation

### Reading outcomes

- Explain and apply: Responses API + Python SDK.
- Explain and apply: Instruction hierarchy, context, examples.
- Explain and apply: JSON-schema constrained generation.

### Implementation assignment

Build Payment Diagnosis Service v0. Accept a payment and its event history, then return a typed diagnosis: status, category, likely cause, recommended action, and confidence. Compare two model configurations.

### Failure and evaluation pass

Create 30 labelled scenarios. Deliberately include missing events, conflicting signals, and plausible-but-wrong causes. Record validity, confidence, latency, tokens, and cost.

### Deliverables

- [ ] `app/llm/diagnose.py`
- [ ] `app/models/diagnosis.py`
- [ ] `evals/datasets/week1.jsonl`
- [ ] `docs/learning-notes/week1.md`

### Exit criteria / completion checklist

- [ ] Successful responses satisfy the schema; refusals and incomplete responses are handled explicitly
- [ ] At least 30 labelled scenarios are stored
- [ ] Explain temperature and sampling conceptually
- [ ] Explain context-window constraints
- [ ] Explain why structured output does not guarantee factual correctness
- [ ] Measured cost and latency instead of guessing

### Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

### Optional depth

Try a third model only after the two-configuration comparison works.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 02 — Function calling & tool design

**Month 1: LLMs as software**

**Goal:** Understand the core mechanism behind agents: the model requests work, your application validates and executes it.

**Before you start:** Reuse Week 1 diagnosis models and fixtures.

**Keep the build focused:** Implement the four read-only tools with explicit organization identity. Reject unauthorized calls before execution; add timeouts and bounded retries now. Reuse the existing failure fixtures. Spend the failure-testing block on typed outcomes and one fake side-effect replay, not on new tool integrations.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [Function calling guide](https://developers.openai.com/api/docs/guides/function-calling)** — Tool definitions, calls, and results
- [ ] **Optional — [JSON Schema](https://json-schema.org/learn/getting-started-step-by-step)** — Validate tool arguments at the boundary
- [ ] **Optional — [OpenAI API reference](https://platform.openai.com/docs/api-reference/responses)** — Inspect the response/tool-call shape
- [ ] **Recommended — [Timeouts, retries and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)** — Read the retry and idempotency sections; map them to your four tools

### Reading outcomes

- Classify retryable vs non-retryable failures and distinguish retries from unsafe duplicate side effects.

### Implementation assignment

Create four deterministic fixture-backed tools: get_payment, get_payment_events, get_ledger_entries, and get_provider_status. Implement the orchestration loop yourself—no agent framework.

### Updated focus — Make failures part of the tool contract, not arbitrary exception strings.

#### Added implementation requirements

- Keep the four fixture-backed tools and manual loop. Return a typed ToolError(code: str, retryable: bool, message: str) on failure, with a safe message and structured trace fields. Define per-attempt timeout, total deadline, maximum attempts and backoff. Do not retry invalid arguments or denied authorization automatically.
- Detect repeated invocations, but distinguish intentional fresh reads from repeated stale calls. Use a stable operation/idempotency key where execution has side effects; demonstrate deduplication with a fake local side effect, never a live payment operation.

#### Experiments and comparisons

- Test tool timeout, 500 error, malformed response, empty response, invalid arguments, unauthorized request, repeated tool invocation and duplicate side-effect attempts. Assert the error code, retryability, attempt count and resulting trace for each. Simulate a timeout after the fake side effect committed, then retry the same operation.

#### Working example / reference shape

```text
class ToolError:
    code: str
    retryable: bool
    message: str

# Example result, not an exception dump
{"code": "PROVIDER_TIMEOUT", "retryable": true, "message": "Provider did not respond"}
```

### Failure and evaluation pass

Make tools return unknown IDs, invalid providers, malformed arguments, timeouts, 500s, empty responses, and payment-not-found. Add an explicit maximum tool-step count.

### Deliverables

- [ ] `app/tools/`
- [ ] `app/llm/tool_loop.py`
- [ ] `simulator/fixtures/`
- [ ] `evals/datasets/tool_selection.jsonl`
- [ ] `app/tools/errors.py`
- [ ] `evals/reports/week2-error-recovery.md`

### Exit criteria / completion checklist

- [ ] ≥90% correct first tool selection across 40 scenarios
- [ ] Invalid tool arguments are rejected before execution
- [ ] Authorization is performed by the application
- [ ] A maximum tool-step count exists
- [ ] Timeouts cannot create infinite retries
- [ ] Draw the full tool-calling lifecycle from memory
- [ ] Retryable and non-retryable failures produce typed ToolError results
- [ ] Retries have explicit attempt and total-time limits
- [ ] Duplicate side effects are prevented with an idempotent operation key
- [ ] Tool errors and recovery attempts are observable in the execution trace

### Engineering note

Explain which failures may be retried, what deduplication guarantees, and what happens after an ambiguous timeout.

### Optional depth

Add async tool execution only if the serial loop is understood.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 03 — Practical machine-learning foundations

**Month 1: LLMs as software**

**Goal:** Build enough classical ML intuition to know when a deterministic or statistical model is the better tool.

**Before you start:** Reuse payment categories; learn only classification, splits and metrics from the crash course.

**Keep the build focused:** Generate 1,000 messages from varied templates. Split by template family before fitting TF-IDF to avoid leakage. Compare both classifiers on the same held-out subset within your budget.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course/)** — Classification, generalization, overfitting
- [ ] **Required — [Classification metrics](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall)** — Precision, recall, F1
- [ ] **Optional — [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)** — Metric definitions + reporting
- [ ] **Optional — [Grouped train/test splits](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)** — Keep related templates out of both training and testing

### Reading outcomes

- Explain and apply: Classification, generalization, overfitting.
- Explain and apply: Precision, recall, F1.

### Implementation assignment

Generate roughly 1,000 payment-support messages across seven labels. Compare TF-IDF + logistic regression against an LLM structured classifier using train, validation, and test splits.

### Failure and evaluation pass

Inspect the confusion matrix. Find the class where a false positive is most costly, then decide whether accuracy or recall should lead your deployment recommendation.

### Deliverables

- [ ] `experiments/classical_classifier.py`
- [ ] `experiments/llm_classifier.py`
- [ ] `data/payment_issues.csv`
- [ ] `docs/learning-notes/classifier-comparison.md`

### Exit criteria / completion checklist

- [ ] Explain training vs inference
- [ ] Explain train, validation, and test data
- [ ] Explain overfitting
- [ ] Explain precision vs recall and when F1 helps
- [ ] Name a task where a $0 deterministic classifier wins
- [ ] Write a deployment recommendation

### Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

### Optional depth

Explore cross-validation after one clean train/validation/test comparison. Synthetic scores are not production evidence.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 04 — Evaluation-driven development

**Month 1: LLMs as software**

**Goal:** Make evals part of development so a prompt change can be judged objectively.

**Before you start:** Combine earlier scenarios instead of starting another dataset.

**Keep the build focused:** Curate 75 unique cases, version the inputs and prompts, and run one before/after change. Record variation across repeated model runs; reproducible inputs do not imply identical outputs. Extend the existing runner and before/after report rather than building a second eval system. Use YAML files plus a release manifest.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenAI Evals guide](https://developers.openai.com/api/docs/guides/evals)** — Datasets, graders, and repeatable runs
- [ ] **Required — [How evals drive AI development](https://openai.com/index/evals-drive-next-chapter-of-ai/)** — Specify → Measure → Improve
- [ ] **Optional — [OpenAI evaluation best practices](https://platform.openai.com/docs/guides/evals)** — Error analysis and representative examples

### Reading outcomes

- Explain immutable prompt versions, promotion status and rollback; separate prompt, model and dataset versions.

### Implementation assignment

Build a reusable eval runner that reports accuracy, schema compliance, tool correctness, unsupported claims, latency, token usage, and estimated cost. Create an error taxonomy.

### Updated focus — Treat prompt versions and evaluation evidence as release artifacts.

#### Added implementation requirements

- Add a file-based Prompt Registry. Store name, version, created_at, model, template, status, eval_dataset, eval_score and notes in each version or associated metadata. Keep published templates immutable; status and eval evidence may live in a separate release manifest. Pin the registry version when running the application.
- Every eval run records prompt_version, model, dataset_version, timestamp, accuracy, unsupported_claim_rate, tool_correctness, cost and latency. Change a prompt, rerun the same golden dataset and produce a before/after regression report. Restore the previous version and rerun it before promoting the change. No registry service is needed.

#### Experiments and comparisons

- Compare two prompt versions on the same frozen dataset and settings. Preserve a change that regresses one metric even if accuracy improves; explain whether the cost/latency tradeoff is worth promotion. Verify rollback resolves the exact prior template.

#### Working example / reference shape

```text
prompts/
  payment_diagnosis/
    v1.yaml
    v2.yaml
    v3.yaml
  incident_investigator/
    v1.yaml

# Illustrative comparison format only — replace with measured results
Prompt v6 → v7
Accuracy             88% → 91%
Unsupported claims    4% → 2%
Average cost        $0.008 → $0.011
Latency              1.2s → 1.5s
```

### Failure and evaluation pass

Run at least one prompt change you expect to help that makes an eval worse. Keep the before/after report and classify why.

### Deliverables

- [ ] `evals/runner.py`
- [ ] `evals/datasets/golden_set.jsonl`
- [ ] `evals/reports/week4.md`
- [ ] `evals/error_taxonomy.yml`
- [ ] `prompts/payment_diagnosis/`
- [ ] `prompts/incident_investigator/v1.yaml`
- [ ] `evals/reports/prompt-regression.md`

### Exit criteria / completion checklist

- [ ] Golden set contains at least 75 cases
- [ ] Eval execution is reproducible
- [ ] Scores are broken down by category
- [ ] Model and prompt metadata are stored
- [ ] A before/after comparison exists
- [ ] You can distinguish a better score from a lucky sample
- [ ] Every eval run identifies prompt, model and dataset versions
- [ ] A previous prompt version can be restored exactly
- [ ] Accuracy, unsupported claims, tool correctness, cost and latency regressions are visible
- [ ] Prompt changes have recorded release and rollback decisions

### Engineering note

Explain how prompt releases resemble application releases, what remains nondeterministic, and why a better accuracy score alone is insufficient.

### Optional depth

Add a hosted eval service after the local runner is useful.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 05 — Embeddings & semantic retrieval

**Month 2: Grounding & RAG**

**Goal:** Understand vector retrieval from first principles before reaching for a vector database.

**Before you start:** Reuse the fixture domain. You need basic arrays and SQL, not a vector-database course.

**Keep the build focused:** Write 20 short synthetic documents. Get array-based cosine search working, then use pgvector exact search through the same interface.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenAI embeddings guide](https://developers.openai.com/api/docs/guides/embeddings)** — Embedding inputs, dimensions, and search
- [ ] **Required — [pgvector documentation](https://github.com/pgvector/pgvector)** — Exact search, HNSW, and IVFFlat
- [ ] **Optional — [NumPy dot product](https://numpy.org/doc/stable/reference/generated/numpy.dot.html)** — Build similarity with plain arrays

### Reading outcomes

- Explain and apply: Embedding inputs, dimensions, and search.
- Explain and apply: Exact search, HNSW, and IVFFlat.

### Implementation assignment

Create a 20-document payment knowledge corpus. Implement embed_document, embed_query, cosine_similarity, and search_similar_documents first with Python arrays, then migrate behind the same interface to PostgreSQL + pgvector.

### Failure and evaluation pass

Probe queries for delayed withdrawals, broadcast-but-processing transactions, and missing callbacks. Inspect nearest neighbours manually and write down false friends.

### Deliverables

- [ ] `app/retrieval/embeddings.py`
- [ ] `app/retrieval/vector_store.py`
- [ ] `knowledge/`
- [ ] `scripts/index_documents.py`

### Exit criteria / completion checklist

- [ ] Explain what an embedding represents
- [ ] Implement cosine similarity
- [ ] Explain semantic vs keyword search
- [ ] Explain exact vs approximate nearest-neighbour search
- [ ] Explain why embeddings are not knowledge
- [ ] Name a case where similarity is not relevance

### Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

### Optional depth

Benchmark approximate indexes later; a 20-document corpus does not need HNSW tuning.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 06 — Build RAG manually

**Month 2: Grounding & RAG**

**Goal:** Trace every stage from a question to a cited answer before adding a framework.

**Before you start:** Use Week 5 corpus and search interface.

**Keep the build focused:** Build one cited-answer pipeline. Change chunk size while holding top-k fixed, then change top-k with chunk size fixed. Reuse query results to control cost. Use the existing small corpus and query set for the first four-way comparison. Week 7 expands measurement; skip search infrastructure tuning.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenAI retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)** — Search, ranking, and grounded answers
- [ ] **Optional — [Retrieval-augmented generation course](https://www.deeplearning.ai/courses/retrieval-augmented-generation)** — Optional reinforcement for gaps
- [ ] **Optional — [OpenAI citations pattern](https://platform.openai.com/docs/guides/retrieval)** — Return evidence with the answer
- [ ] **Required — [BM25 reference implementation](https://github.com/dorianbrown/rank_bm25)** — Inspect tokenization and BM25Okapi scoring; work through one small example manually
- [ ] **Recommended — [Retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)** — Read the two-stage pipeline and bi-encoder/cross-encoder distinction; library choice is flexible

### Reading outcomes

- Explain BM25/lexical retrieval, dense embeddings, candidate merging, metadata filtering and reranking as separate stages.
- Explain why exact error codes and paraphrased symptoms need different retrieval signals.

### Implementation assignment

Build Payment Knowledge Assistant as a manual pipeline: query preprocessing → embedding → retrieval → context selection → prompt construction → LLM → answer + citations.

### Updated focus — Recover both exact payment identifiers and semantically related operational evidence.

#### Added implementation requirements

- Keep the manual cited-answer pipeline. Add a BM25 branch beside dense search. Trace each independently before merging. Apply the same trusted organization/access/version metadata filters to both branches before candidates reach a reranker or model. Deduplicate by stable document/chunk ID and merge rankings (for example reciprocal-rank fusion); do not blindly add incomparable raw scores.
- Add a reranker interface and run a minimal appropriate reranking implementation. Compare BM25 only, Dense only, Hybrid and Hybrid + reranker on identical queries. Reuse that reranker in Week 7 for the cross-encoder experiment; do not require a new search service or specific model/library.

#### Experiments and comparisons

- Compare exact-code queries such as TX_ALREADY_EXISTS with “payment was sent but blockchain confirmation never completed.” Include overlapping candidates, missing metadata, contradictory documents and an out-of-tenant exact match. Keep the chunk-size/top-k experiments already assigned; vary one factor at a time rather than running every combination.

#### Working example / reference shape

```text
Query → authorized metadata scope
          ├─ BM25 / lexical ──┐
          └─ Dense search ────┤
                       Merge + deduplicate
                              ↓
                           Reranker
                              ↓
                           Top-K docs
                              ↓
                         LLM + citations
```

### Failure and evaluation pass

Compare chunk sizes 250 / 500 / 1,000 and top-k 3 / 5 / 10. Keep the output and record whether the failure came from query understanding, retrieval, source quality, context, or generation.

### Deliverables

- [ ] `app/retrieval/chunker.py`
- [ ] `app/retrieval/retriever.py`
- [ ] `app/rag/pipeline.py`
- [ ] `experiments/rag_chunking.md`
- [ ] `app/retrieval/hybrid.py`
- [ ] `app/retrieval/reranker.py`
- [ ] `experiments/retrieval-four-way.md`

### Exit criteria / completion checklist

- [ ] Trace a wrong answer to a pipeline stage
- [ ] Answer, evidence, and source are separate in the UI
- [ ] At least three chunk sizes are compared
- [ ] At least three top-k values are compared
- [ ] Every answer carries source identifiers
- [ ] You can explain why more context can reduce quality
- [ ] BM25, dense retrieval, merging, filtering and reranking can be inspected independently
- [ ] BM25 / Dense / Hybrid / Hybrid + reranker are compared on identical payment queries
- [ ] Unauthorized candidates never enter the reranker or model context

### Engineering note

Explain which queries each approach wins, why rank fusion was chosen, and where reranking earns its latency.

### Optional depth

The full RAG course, new search services and advanced query rewriting remain optional. Hybrid retrieval and the reranker experiment are required.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 07 — Retrieval evaluation

**Month 2: Grounding & RAG**

**Goal:** Evaluate the retrieval layer separately from generation so “bad answer” has a diagnosable cause.

**Before you start:** Freeze the Week 6 baseline and document IDs.

**Keep the build focused:** Label 50 queries. Separate answerable retrieval cases from unanswerable refusal cases. Learning targets: Recall@5 ≥0.85, citation precision ≥0.90, unsupported answers ≤0.10. Record denominators and misses, not just a score. Extend Week 6 code and the existing 50 queries. Use a subset for candidate-budget sweeps, then one full comparison.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [Information retrieval metrics](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics)** — Precision, recall, and ranking metrics
- [ ] **Required — [OpenAI Evals guide](https://developers.openai.com/api/docs/guides/evals)** — Golden cases and graders
- [ ] **Optional — [Ragas documentation](https://docs.ragas.io/en/stable/)** — Optional reference for RAG evaluation concepts
- [ ] **Required — [NDCG score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html)** — Read graded relevance, ideal ordering and ties; calculate a toy example before using a helper
- [ ] **Recommended — [Cross-encoder retrieval and reranking](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)** — Revisit only the cross-encoder section from Week 6

### Reading outcomes

- Calculate NDCG from graded relevance judgments while retaining Precision@K, Recall@K and MRR.
- Explain why jointly scoring a query-document pair usually costs more than comparing precomputed bi-encoder embeddings; measure rather than assume an accuracy gain.

### Implementation assignment

Create 50 retrieval-specific test cases with relevant document IDs and required facts. Calculate Precision@K, Recall@K, MRR, correctness, faithfulness, citation correctness, and completeness.

### Updated focus — Measure graded relevance and the quality/latency cost of a cross-encoder.

#### Added implementation requirements

- Extend the 50-case retrieval dataset with graded relevance labels (for example 0 irrelevant, 1 useful, 2 directly answers). Document the binary threshold used for Recall/Precision/MRR. Retrieve up to 50 distinct authorized candidates cheaply, cross-encode query/document pairs, then return the top 5. Expand the synthetic corpus with distractors if needed to exercise a full 50-candidate pass.
- Keep the same held-out queries, corpus, filters and generation settings for all four retrieval variants. Report Recall@5, MRR and NDCG@5 alongside latency and cost; also retain Precision@K and the existing generation metrics. Define zero-relevance handling and report unanswerable cases separately. Any suitable cross-encoder implementation is acceptable; no local model serving stack is required.

#### Experiments and comparisons

- Run BM25, Dense, Hybrid and Hybrid + rerank. Compare 5/20/50 candidate budgets on a small diagnostic subset, include total retrieval plus reranking latency, and record the reranker’s compute/API cost. Show a case where reranking cannot rescue a document missing from the candidate set.

#### Working example / reference shape

```text
Larger corpus → cheap retrieval → 50 candidates
                         → cross-encoder → top 5

Variant          Recall@5  MRR  NDCG@5  latency  cost
BM25             [measure each column]
Dense            [measure each column]
Hybrid           [measure each column]
Hybrid + rerank  [measure each column]
```

### Failure and evaluation pass

Add unanswerable questions, conflicting documents, outdated documents, and irrelevant documents that share vocabulary. Report retrieval failure separately from generation failure.

### Deliverables

- [ ] `evals/retrieval/`
- [ ] `evals/rag/`
- [ ] `evals/reports/week7.md`
- [ ] `evals/retrieval/graded_relevance.jsonl`
- [ ] `evals/reports/reranking-comparison.md`

### Exit criteria / completion checklist

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

### Engineering note

Record whether the reranker improves relevance enough to justify its extra work; separate candidate-recall limits from ranking errors.

### Optional depth

If a target is missed, write a failure analysis and rerun one targeted fix. These are learning targets, not production certification.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 08 — Production RAG & multi-tenancy

**Month 2: Grounding & RAG**

**Goal:** Turn “chat with documents” into a trustworthy knowledge subsystem with identity, freshness, and deletion semantics.

**Before you start:** Use the authorization boundary from Week 2 and the Week 7 eval runner.

**Keep the build focused:** Finish tenant filtering, deletion and version replacement first, then retry/deduplication. A failed isolation test is a stop gate, not an acceptable averaged score.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [PostgreSQL row-level security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)** — Database-enforced tenant boundaries
- [ ] **Required — [pgvector metadata filtering](https://github.com/pgvector/pgvector)** — Filter vectors with application metadata
- [ ] **Optional — [OpenAI retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)** — Grounding and source attribution

### Reading outcomes

- Explain and apply: Database-enforced tenant boundaries.
- Explain and apply: Filter vectors with application metadata.

### Implementation assignment

Add organization_id, document_version, source_type, effective_date, access_level, provider, and network to every chunk. Implement tenant-aware search, re-indexing, deletion, retries, version replacement, and deduplication.

### Failure and evaluation pass

Create Org A and Org B with deliberately similar documents. Attempt cross-tenant leakage, stale-version retrieval, duplicate ingestion, and retrieval after deletion.

### Deliverables

- [ ] `app/ingestion/`
- [ ] `app/retrieval/filters.py`
- [ ] `evals/security/tenant_retrieval.jsonl`
- [ ] `docs/rag-architecture.md`

### Exit criteria / completion checklist

- [ ] Zero cross-tenant retrieval in tests
- [ ] Deleted documents disappear from search
- [ ] Updated documents replace stale versions
- [ ] Generated claims identify their source
- [ ] Ingestion failures are observable
- [ ] Paqet Copilot v0.2 can ground an operator answer

### Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

### Optional depth

A background ingestion worker can follow the synchronous contract tests.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 09 — Build an agent yourself

**Month 3: Agentic systems**

**Goal:** Understand an agent without framework magic: state, decisions, validated actions, observations, and termination.

**Before you start:** Reuse the Week 2 loop; do not start another tool framework.

**Keep the build focused:** Add explicit state, max steps, total deadline, retry budget and observable trajectories. Compare with a fixed deterministic investigation workflow. Add one assembler to the existing bounded loop. Use synthetic long observations for overflow tests instead of building a general memory service.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)** — Tools as application-owned actions
- [ ] **Required — [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)** — Reasoning settings and response design
- [ ] **Optional — [ReAct paper](https://arxiv.org/abs/2210.03629)** — Reasoning + acting as an observable loop

### Reading outcomes

- Explain context selection, token budgets, authority, freshness and why more context does not mean better context.

### Implementation assignment

Implement a bounded agent loop for “Why is payment pay_123 still processing?” Store observable trajectories: requested tool, arguments, result, timing, and final answer. Do not depend on private chain-of-thought.

### Updated focus — Own what enters model context instead of accumulating an unlimited transcript.

#### Added implementation requirements

- Build assemble_context(user_request, system_instructions, agent_state, conversation, tool_results, retrieved_documents, max_tokens). Use the selected model’s tokenizer or a conservative measured estimate. Reserve room for output and tool schemas within the model limit; the example budget is input context, not a model recommendation.
- Define what is dropped, summarized and never removed: preserve safety/authorization boundaries, the current task and authoritative evidence needed for a safe answer. Treat tool/document text as untrusted data, not instructions. Include source IDs, versions and observation timestamps. Summaries retain provenance and must not become more authoritative than their sources.
- Expire stale observations, repeat retrieval when payment state or document versions change, and fail safely or escalate if essential context cannot fit. Store a redacted inspectable snapshot of exactly the assembled synthetic input, plus model, prompt and policy versions; protect any real diagnostic snapshots with access and retention controls.

#### Experiments and comparisons

- Deliberately exceed the context budget with old conversation, huge tool results and redundant documents. Assert selection rules, output headroom, stale-observation handling and retained authoritative sources. Replay a failed call from its context snapshot; never request private chain-of-thought.

#### Metrics to record

- context_tokens · retrieved_tokens · tool_result_tokens · conversation_tokens · tokens_dropped · tokens_summarized

#### Working example / reference shape

```text
Example input budget (tokens)
System instructions      1,500
User request               500
Agent state              1,500
Tool observations        4,000
Retrieved knowledge      4,000
Conversation             1,000
Maximum                 12,500

Reserve output/tool-schema headroom separately.
Track removed source tokens and summary input/output tokens.
```

### Failure and evaluation pass

Force an infinite loop, repeated tool call, timeout, incorrect tool data, conflicting tools, and no-answer scenario. Make each failure a typed observation.

### Deliverables

- [ ] `app/agents/loop.py`
- [ ] `app/agents/state.py`
- [ ] `evals/agent/baseline.jsonl`
- [ ] `docs/learning-notes/week9.md`
- [ ] `app/agents/context_assembler.py`
- [ ] `evals/agent/context_overflow.jsonl`
- [ ] `evals/reports/context-budget.md`

### Exit criteria / completion checklist

- [ ] MAX_STEPS is enforced
- [ ] A timeout budget exists
- [ ] A retry budget exists
- [ ] Tool calls are validated
- [ ] Termination conditions are explicit
- [ ] Agent completes ≥80% of baseline investigations
- [ ] Context Assembler enforces a documented token budget with output headroom
- [ ] Overflow tests prove drop/summarize/never-remove rules and safe failure
- [ ] Stale observations trigger documented refresh or retrieval decisions
- [ ] All six context metrics are recorded with clear counting conventions
- [ ] Explain more context != better context and inspect the exact context of a failed call

### Engineering note

Explain authority and freshness rules, one compression failure, and what you refuse to remove even when the context is full.

### Optional depth

Planning strategies are optional until the bounded baseline passes.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 10 — Incident investigation agent

**Month 3: Agentic systems**

**Goal:** Move from a single payment diagnosis to a system-level production investigation with metrics, logs, history, and provider state.

**Before you start:** Use Week 9 agent and the same simulator interfaces.

**Keep the build focused:** Use seeded metrics/log fixtures, not a new telemetry platform. Build 30 incident variants with known causes and evaluate both the evidence trail and final diagnosis. Add trajectory labels to existing incidents; do not create another 30 scenarios or new observability infrastructure.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/observability-primer/)** — Signals, traces, and context
- [ ] **Optional — [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/)** — Counters, gauges, histograms
- [ ] **Optional — [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)** — Expose only useful investigation tools

### Reading outcomes

- Define an acceptable investigation trajectory, including alternative valid tool orders and evidence requirements.

### Implementation assignment

Generate time-series simulator conditions and build an investigator with query_metrics, search_logs, find_incidents, list_failed_payments, get_provider_status, and search_runbooks. Answer why USDC withdrawal success rate dropped in the last 30 minutes.

### Updated focus — Judge the evidence-gathering process, not just a lucky final diagnosis.

#### Added implementation requirements

- Keep final-answer evaluation. Add trajectory assertions for correct first tool, sufficient evidence, irrelevant tools, unnecessary repeats, premature stopping, tool-call budgets and efficient diagnosis. Define acceptable evidence sets and alternative tool orders per scenario rather than grading one rigid script.
- Record correct_tool_selection, unnecessary_tool_calls, duplicate_tool_calls, steps_to_resolution, tool_error_recovery and trajectory_success. Report their denominators; use N/A for error recovery when no error occurred. A guessed correct answer without required evidence fails trajectory_success.

#### Experiments and comparisons

- Compare a correct diagnosis with missing evidence, an evidence-supported efficient diagnosis, an over-budget investigation, an unnecessary repeat and a recovered timeout. Grade these against the same 30 incident scenarios and retain both answer and trajectory scores.

#### Metrics to record

- correct_tool_selection · unnecessary_tool_calls · duplicate_tool_calls · steps_to_resolution · tool_error_recovery · trajectory_success

### Failure and evaluation pass

Evaluate both final diagnosis and trajectory: relevant evidence inspected, unnecessary calls, premature stopping, root-cause confidence, and unsupported claims.

### Deliverables

- [ ] `simulator/scenarios/`
- [ ] `app/agents/investigator.py`
- [ ] `evals/agent/scenarios.jsonl`
- [ ] `evals/graders/trajectory.py`
- [ ] `evals/reports/trajectory-quality.md`

### Exit criteria / completion checklist

- [ ] At least 30 incident scenarios exist
- [ ] ≥80% correct root cause
- [ ] ≥90% no unsupported root-cause claims
- [ ] Zero infinite loops
- [ ] Average tool calls are tracked
- [ ] Tokens, cost, and latency per investigation are tracked
- [ ] Trajectory grading checks first tool, evidence coverage, repeats, stopping and budgets
- [ ] All six trajectory metrics are reported alongside final-answer quality
- [ ] An unsupported lucky diagnosis cannot pass trajectory_success

### Engineering note

Compare two successful-looking answers whose trajectories differ. Explain acceptable extra calls and the cost of stopping too soon.

### Optional depth

Add more providers only after the existing scenarios are covered.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 11 — LangGraph & durable workflows

**Month 3: Agentic systems**

**Goal:** Learn the framework after understanding the primitive it abstracts: stateful, long-running, resumable workflows.

**Before you start:** Keep the Week 10 baseline unchanged for comparison.

**Keep the build focused:** Persist one investigation graph. Demonstrate restart and approval with a simulated create_incident action; bind approval to exact arguments and prevent replay. Use the engineering-note hour for the comparison and reuse the existing failure rehearsal. No second workflow implementation.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)** — Graph state and durable execution
- [ ] **Required — [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)** — Checkpoints and resumability
- [ ] **Required — [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)** — Human-in-the-loop pause and resume
- [ ] **Recommended — [Temporal Workflow Execution overview](https://docs.temporal.io/workflow-execution)** — Read state/replay concepts and activity boundaries; conceptual comparison only

### Reading outcomes

- Compare checkpointing, workflow state, replay, idempotency, side-effect isolation, resume-after-failure and deterministic execution concepts.

### Implementation assignment

Refactor the investigator into a graph: understand_request → gather_payment_state → gather_operational_state → retrieve_knowledge → analyze → confidence_gate → answer or human_review. Add a proposed create_incident action.

### Updated focus — Relate LangGraph persistence to durable workflow systems without building another engine.

#### Added implementation requirements

- Keep LangGraph and the existing restart/approval tests. Write “LangGraph persistence vs durable workflow engines.” Compare a stored graph checkpoint with history-based replay, deterministic workflow orchestration and recorded activity results. Model calls, wall-clock reads and external mutations are nondeterministic boundaries to isolate; neither framework removes the need for application idempotency. Do not install Temporal or build a workflow engine.

#### Experiments and comparisons

- Annotate the existing crash/restart test at three points: before a model call, after a recorded result, and after a fake side effect but before its acknowledgment. Explain what may run again in your LangGraph setup and how a Temporal-style workflow would manage that boundary.

### Failure and evaluation pass

Kill the process halfway through an investigation, restart it, and resume from checkpoint. Attempt to replay a side effect and prove it is not duplicated.

### Deliverables

- [ ] `app/agents/graph.py`
- [ ] `app/agents/checkpoints.py`
- [ ] `evals/agent/recovery.jsonl`
- [ ] `docs/decisions/langgraph.md`
- [ ] `docs/learning-notes/langgraph-vs-durable-workflows.md`

### Exit criteria / completion checklist

- [ ] Workflow survives a process restart
- [ ] State is persisted
- [ ] Duplicate side effects are prevented
- [ ] Approval pauses and resumes correctly
- [ ] You can explain the value over the Week 9 loop
- [ ] Recovery behavior is covered by an eval
- [ ] The engineering note compares all seven durability concepts using the existing workflow
- [ ] Nondeterministic model calls and external side effects have explicit isolation/idempotency boundaries
- [ ] Explain why checkpointing alone does not guarantee exactly-once side effects

### Engineering note

LangGraph persistence vs durable workflow engines: what is saved, what replays, what can repeat, and which guarantees belong to your application.

### Optional depth

Parallel graph branches are optional. Approval is not a replacement for application authorization.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 12 — MCP + Go

**Month 3: Agentic systems**

**Goal:** Turn payment-domain capabilities into reusable AI infrastructure and connect your Go learning to a real boundary.

**Before you start:** Know Go structs, interfaces, errors and tests; use the official Go SDK example as your starting point.

**Keep the build focused:** Build a local stdio MCP server backed by fixtures, with the listed resources and read-only tools. Pin SDK/protocol versions together and test through a real client.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [MCP architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)** — Hosts, clients, servers, and transports
- [ ] **Required — [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)** — Discoverable, callable tools
- [ ] **Required — [MCP resources specification](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)** — Read-only payment and incident resources
- [ ] **Optional — [Official MCP Go SDK](https://github.com/modelcontextprotocol/go-sdk)** — Start from the minimal server example; pin the version

### Reading outcomes

- Explain and apply: Hosts, clients, servers, and transports.
- Explain and apply: Discoverable, callable tools.
- Explain and apply: Read-only payment and incident resources.

### Implementation assignment

Build a small Paqet MCP server in Go. Expose payment://{id}, incident://{id}, and tools for get_payment, get_payment_events, search_incidents, and get_provider_status. Use simulator adapters until Paqet is ready.

### Failure and evaluation pass

Test malformed requests, unknown IDs, authorization boundaries, tool timeouts, and a destructive action that requires explicit human approval.

### Deliverables

- [ ] `mcp/paqet-mcp/`
- [ ] `mcp/paqet-mcp/server.go`
- [ ] `mcp/paqet-mcp/README.md`
- [ ] `evals/mcp/contract.jsonl`

### Exit criteria / completion checklist

- [ ] Server exposes resources and tools
- [ ] Go tests cover request validation
- [ ] Client receives stable errors
- [ ] Simulator and Paqet adapters share a conceptual interface
- [ ] Destructive operations require approval
- [ ] MCP contract tests pass from a clean run

### Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

### Optional depth

Remote HTTP transport and real Paqet integration are extensions. Keep all destructive actions simulated.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 13 — Serious evals

**Month 4: Production AI**

**Goal:** Expand from a demo-sized golden set to an evaluation system that measures the whole agent environment.

**Before you start:** Pool and deduplicate Weeks 1–12 cases before generating more.

**Keep the build focused:** Reach 300 versioned cases cumulatively, not 300 new manually written cases. Cover each failure category and reserve a held-out set. Calibrate a judge against a human-reviewed sample. Build a small rule-based router and wire the existing runner to CI. Reuse the cumulative 300-case suite; a learned router and 500 cases remain extensions.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenAI Evals guide](https://developers.openai.com/api/docs/guides/evals)** — Deterministic graders and datasets
- [ ] **Optional — [OpenAI evals best practices](https://platform.openai.com/docs/guides/evals)** — Human review and LLM-as-judge
- [ ] **Optional — [OpenAI model evaluation guide](https://platform.openai.com/docs/guides/evals)** — Pairwise comparison + regression gates
- [ ] **Recommended — [CI failure exit codes](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/set-exit-codes)** — Make the local eval command fail the pipeline; use an equivalent existing CI system if present

### Reading outcomes

- Explain model routing vs failover, calibrated escalation, and soft quality thresholds vs hard security invariants.

### Implementation assignment

Expand to 300–500 cases across payment investigation, retrieval, tool selection, insufficient information, ambiguous requests, outages, permission boundaries, prompt injection, and hallucination.

### Updated focus — Spend model capacity deliberately and gate releases with measured regressions.

#### Added implementation requirements

- Add a Model Router with cheap, normal and strong routes. Consider task type, context size, estimated complexity, tool requirements, confidence, tenant budget and latency SLO. Start with explicit rules and log routing reasons; confidence must be calibrated on held-out outcomes or combined with evidence checks, not trusted as a raw self-reported number.
- Compare routing against always using the strongest model on the same held-out tasks. Include a cheap → stronger escalation when evidence/confidence is insufficient. Bound attempts, total cost and latency; do not escalate beyond tenant budget. Measure aggregate quality, cost, latency and escalation rate, including failed and escalated attempts.
- Add configurable CI eval gates to the Week 4 runner and prompt registry. Example policy: fail when root-cause accuracy drops more than 3 percentage points from the pinned baseline, unsupported_claim_rate exceeds 5%, cross-tenant violations exceed 0, or executed tool schema validity is below 100%. Clarify percentage points vs relative change; define repeated-run policy for stochastic quality metrics. Missing metrics or a broken evaluator must fail closed. Security invariants are hard gates, never averaged away.

#### Experiments and comparisons

- Exercise simple, complex, large-context, tool-required and budget-exhausted tasks. Inject a prompt regression and cross-tenant/schema violations to prove CI fails. Show a non-regressing run passes, and keep the router-vs-strongest report. Stub deterministic CI failures when API credentials are unavailable; run live quality comparisons separately under a budget.

#### Metrics to record

- quality · cost · latency · escalation_rate

#### Working example / reference shape

```text
Task → classify type/difficulty/context/tool needs
          ├─ cheap ── low confidence → stronger
          ├─ normal
          └─ strong
Budget or safety limit reached → human escalation

Eval comparison → quality thresholds + hard security gates
                → release / reject
```

### Failure and evaluation pass

Compare deterministic assertions, human scoring, LLM-as-judge, and pairwise comparison. Sample cases manually and document judge disagreement.

### Deliverables

- [ ] `evals/datasets/v1/`
- [ ] `evals/graders/`
- [ ] `evals/reports/week13.md`
- [ ] `docs/evaluation-strategy.md`
- [ ] `app/llm/router.py`
- [ ] `evals/reports/model-routing.md`
- [ ] `evals/regression-thresholds.yaml`
- [ ] `ci/eval-gates.yml`

### Exit criteria / completion checklist

- [ ] 300+ cases are versioned
- [ ] Coverage includes safety and permissions
- [ ] At least two grading methods are compared
- [ ] Manual samples are reviewed
- [ ] Regression thresholds are defined
- [ ] A model/prompt change can be accepted or rejected by evidence
- [ ] Cheap / normal / strong routing and bounded escalation are implemented
- [ ] Router vs always-strongest comparison includes quality, cost, latency and escalation rate
- [ ] A deliberate quality regression fails CI at a configured threshold
- [ ] Cross-tenant violations and invalid executed tool schemas fail hard security gates
- [ ] Missing evaluation evidence blocks release and previous prompt/model configuration can be restored

### Engineering note

Explain routing rules, calibration, SLO/budget tradeoffs and the difference between model escalation and outage fallback.

### Optional depth

500 cases and a second judge are stretch work. Never tune prompts against the final held-out set.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 14 — AI observability

**Month 4: Production AI**

**Goal:** Make every model call, tool call, retrieval, and escalation visible enough to operate in production.

**Before you start:** Reuse cost/latency records from Week 1 and trajectories from Week 9.

**Keep the build focused:** Instrument one end-to-end path with OpenTelemetry and one dashboard. Include all listed signals; keep high-cardinality payment IDs out of metric labels and redact sensitive span data. Extend one existing dashboard and one read-only investigation path. Use the existing simulator clock and state versions for invalidation tests.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)** — Traces, metrics, and logs
- [ ] **Required — [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)** — Instrument the application
- [ ] **Optional — [Prometheus overview](https://prometheus.io/docs/introduction/overview/)** — Scrape and query metrics
- [ ] **Recommended — [Redis semantic cache concepts](https://redis.io/docs/latest/develop/ai/redisvl/concepts/extensions/)** — Read Semantic Cache and filtering; implement the experiment with existing storage before adopting a helper

### Reading outcomes

- Distinguish TTFT (time to first token), total/model/tool/retrieval latency, throughput and inter-token timing.
- Explain semantic similarity != response equivalence and why payment state must constrain cache reuse.

### Implementation assignment

Instrument request → agent trace → model call → tool call → retrieval → response. Build an AI Operations Dashboard with latency, tokens, cost, tool errors, retrieval latency, steps, completion %, escalation %, eval score, model, and prompt version.

### Updated focus — Measure AI latency and test semantic reuse without serving stale payment answers.

#### Added implementation requirements

- Keep OpenTelemetry, Prometheus and Grafana. Add TTFT, total latency, model latency, tool latency, retrieval latency and tokens/second where observable. If streaming is implemented, measure inter-token gaps where practical; distinguish chunks from tokens, client-observed vs provider timing, and mark unavailable metrics N/A rather than zero.
- Build a small Semantic Cache experiment: query embedding → nearest authorized cached query → threshold plus equivalence/freshness checks → hit or agent on miss. Scope by organization, permissions, payment ID, payment state/version, knowledge version and prompt/model configuration. Use expiry and invalidation, and revalidate relevant current state before reuse. Never cache a mutation as an executable action or use TTL alone to establish response equivalence.
- Measure hit rate, latency improvement, cost reduction and incorrect stale hits including embedding, state-validation and miss-path costs. Keep the cache optional in the final runtime until correctness and benefit are demonstrated; the experiment itself is required.

#### Experiments and comparisons

- Compare “Why is payment 123 delayed?” and “What’s causing payment 123 to be stuck?” in the same state. Then change payment state, use another payment/tenant, revoke permission, change the runbook or bump the prompt version. These must miss or invalidate even when semantic similarity is high. Compare cache-off vs cache-on using cold and warm runs.

#### Metrics to record

- TTFT / time to first token · total_latency · model_latency · tool_latency · retrieval_latency · tokens_per_second · inter_token_gap (if streaming) · cache_hit_rate · latency_improvement · cost_reduction · incorrect_stale_hits

### Failure and evaluation pass

Create a dashboard drill-down from a slow request to the exact tool/model span. Inject a provider error and verify it is visible without reading application logs.

### Deliverables

- [ ] `observability/tracing/`
- [ ] `observability/metrics/`
- [ ] `observability/dashboards/ai-operations.json`
- [ ] `docs/learning-notes/week14.md`
- [ ] `app/cache/semantic_cache.py`
- [ ] `evals/reports/semantic-cache.md`
- [ ] `observability/dashboards/streaming-latency.json`

### Exit criteria / completion checklist

- [ ] p50/p95 latency is visible
- [ ] Input and output tokens are tracked
- [ ] Cost per request is calculated
- [ ] Tool errors and agent steps are visible
- [ ] Human escalation rate is visible
- [ ] A slow request can be traced end to end
- [ ] AI-specific latency and throughput metrics have explicit timing boundaries and N/A rules
- [ ] Semantic Cache uses identity, permissions, state/freshness and invalidation checks
- [ ] Cache-on/off comparison reports hit rate, latency benefit, cost savings and stale hits
- [ ] Changed state or access cannot reuse a semantically similar cached answer
- [ ] Streaming inter-token behavior is measured if streaming is implemented

### Engineering note

Explain which computation is safe to reuse, why similarity is insufficient, and whether to enable the cache in the capstone.

### Optional depth

Production alert routing and a hosted tracing vendor are optional.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 15 — AI security & reliability

**Month 4: Production AI**

**Goal:** Attack the system before an operator—or a malicious prompt—does it for you.

**Before you start:** Revisit the boundaries introduced in Weeks 2, 8, 9 and 11.

**Keep the build focused:** Audit and strengthen existing controls rather than adding security for the first time. Use synthetic adversarial inputs; test authorization, tenant isolation, approval replay and retry exhaustion. Extend the existing security suite and simulated actions. No real refunds, status changes, key rotation or new identity provider.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OWASP Top 10 for LLM applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** — Prompt injection, data leakage, and unsafe tools
- [ ] **Optional — [OpenAI safety best practices](https://platform.openai.com/docs/guides/safety-best-practices)** — Input/output controls and abuse prevention
- [ ] **Required — [MCP security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)** — Authorization and transport boundaries
- [ ] **Recommended — [OWASP: Excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** — Read excessive functionality and permissions; apply minimum tool exposure to the investigator

### Reading outcomes

- Explain tool visibility vs execution authorization, indirect prompt injection and replay-resistant approvals.

### Implementation assignment

Audit and strengthen the security controls built in earlier weeks: authentication, RBAC, tenant isolation, tool permissions, validation, rate limits, PII filtering, injection defenses, timeouts, circuit breakers, max steps and argument-bound human approval. Keep actions simulator-only.

### Updated focus — Make least privilege an application-enforced tool boundary.

#### Added implementation requirements

- Keep all existing security controls and red-team exercises. Build context-specific tool allowlists. ReadOnlyInvestigator sees get_payment, query_metrics, search_logs and search_runbooks; refund_payment, change_payment_status and rotate_key are not visible. Application code selects exposed tools using trusted identity and permissions, then authorizes every call again at execution time. Hiding a tool is defense in depth, not the authorization check.
- Treat retrieved text and tool outputs as untrusted. Bind any simulated mutation approval to the actor, tenant, exact arguments, operation ID and expiration. Prevent replay and do not let an LLM grant itself privilege or relax a boundary.

#### Experiments and comparisons

- Test indirect prompt injection in a runbook/tool response, tool argument manipulation, cross-tenant retrieval, cross-tenant tool calls, privilege escalation, a destructive action request and a replayed mutating call. Assert both that forbidden tools are absent from context and that forged direct calls are rejected.

#### Working example / reference shape

```text
ReadOnlyInvestigator
Allowed: get_payment, query_metrics, search_logs, search_runbooks
Not visible: refund_payment, change_payment_status, rotate_key

Trusted identity → application allowlist → model tool request
                 → application authorization → bounded execution
```

### Failure and evaluation pass

Attack with “show every customer’s payments,” “run create_refund for all failed payments,” a malicious runbook, a cross-org request, and a tool that never succeeds. Capture the failure and control that stopped it.

### Deliverables

- [ ] `app/security/`
- [ ] `app/policy/`
- [ ] `evals/security/adversarial.jsonl`
- [ ] `docs/security-model.md`
- [ ] `app/policy/tool_allowlists.py`
- [ ] `evals/security/least-privilege.jsonl`

### Exit criteria / completion checklist

- [ ] Authorization never depends on the LLM
- [ ] Tenant isolation is tested
- [ ] Destructive tools require approval
- [ ] Prompt injection cases are represented
- [ ] Timeouts and circuit breakers work
- [ ] PII is filtered from logs and model context
- [ ] Tool exposure is restricted by application-owned least-privilege allowlists
- [ ] Forged or manipulated calls are denied independently of model behavior
- [ ] All seven stronger-security attack categories have passing tests
- [ ] Replayed mutations cannot reuse approval or duplicate a side effect

### Engineering note

Explain why a prompt saying “do not refund” is not a security control, and distinguish hidden tools from authorized execution.

### Optional depth

Provider-specific policies are extensions. No live refunds, transfers or production credentials are needed.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

## Week 16 — Ship the Payment Reliability Copilot

**Month 4: Production AI**

**Goal:** Bring the system together into a credible, explainable, observable capstone you can demo and defend.

**Before you start:** Bring forward the same simulator, eval runner and evidence from previous weeks.

**Keep the build focused:** Reuse the router, trace store and eval runner. Demonstrate a small curated review queue with simulator events, then freeze and record the existing final demo. A reproducible simulator demo remains the core learning finish; real production release requires separate validation.

### Learning resources

Check each resource as you use it. Required readings contribute to core progress; Recommended and Optional readings are tracked for depth but do not gate completion.

- [ ] **Required — [OpenAI production best practices](https://platform.openai.com/docs/guides/production-best-practices)** — Reliability, security, and deployment
- [ ] **Required — [FastAPI deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/)** — Serve the application safely
- [ ] **Optional — [OpenTelemetry getting started](https://opentelemetry.io/docs/getting-started/)** — Verify production instrumentation

### Reading outcomes

- Explain curated observation-to-eval flow without automatic training, and the quality/cost consequences of fallback.

### Implementation assignment

Ship the capstone: a natural-language operations interface with payment investigation, RAG over runbooks, semantic incident search, tool calling, multi-step investigations, MCP tools, citations, human approval, evals, tracing, cost tracking, authorization, and resilience. The core finish is a reproducible simulator-backed demo. Treat a live production rollout as a separate operational milestone.

### Updated focus — Close the evaluation loop and fail safely when the preferred model is unavailable.

#### Added implementation requirements

- Keep the portfolio release and final rehearsal. Design a Data Flywheel: interactions → success/failure/human correction signals → review pipeline → labelled eval cases → versioned dataset → prompt/model changes → gated release. Capture thumbs down, human corrections, agent failures, tool failures, low-confidence cases and production incidents as candidates, not automatically trusted labels.
- Demonstrate the review flow with simulator observations. Redact sensitive data, check authorization/consent and retention before any real production use, deduplicate cases, require human label review, retain provenance and keep held-out evaluation uncontaminated. Do not automatically train or fine-tune models from production data.
- Add a bounded preferred model → fallback model → human escalation hierarchy. Document failure/capacity/budget criteria, tool/schema compatibility, quality and cost implications, maximum attempts and safe failure behavior. Use the Week 13 router and typed errors; prohibit a cheaper fallback from weakening tenant, tool or approval rules. Provide evidence and a reason when escalating instead of fabricating an answer.

#### Experiments and comparisons

- Turn a synthetic thumbs-down, human correction and tool failure into reviewed labelled cases and rerun the eval suite. Inject preferred-model failure, capacity rejection and exhausted budget, then make the fallback fail or lack evidence. Verify eventual human escalation, bounded spend/latency and no duplicate side effects.

#### Working example / reference shape

```text
Observation + correction → reviewed candidate → labelled eval case
 → versioned dataset → prompt/model change → CI gates → release

Preferred model
  ↓ failure / capacity / budget policy
Fallback model
  ↓ cannot safely answer or budget exhausted
Human escalation (with evidence and reason)
```

### Failure and evaluation pass

Run a final rehearsal with a happy path, insufficient evidence, provider outage, prompt injection, cross-tenant request, duplicate side effect, and process restart. Keep the trace and the eval report.

### Deliverables

- [ ] `docs/architecture.md`
- [ ] `evals/reports/final.md`
- [ ] `demo/payment-copilot-demo.mp4`
- [ ] `docs/case-study.md`
- [ ] `docs/data-eval-flywheel.md`
- [ ] `evals/candidates/reviewed-examples.jsonl`
- [ ] `docs/fallback-architecture.md`
- [ ] `evals/reports/fallback-rehearsal.md`

### Exit criteria / completion checklist

- [ ] All core capabilities have a working path
- [ ] Final eval report includes failures and trade-offs
- [ ] Architecture document explains boundaries
- [ ] A 2–4 minute demo is recorded
- [ ] Case study explains why AI is appropriate
- [ ] You can explain what changes at 100× scale
- [ ] All six observation sources have a documented candidate-to-reviewed-eval path
- [ ] Data review includes privacy, provenance, deduplication and held-out-set protection
- [ ] No production feedback automatically trains a model or bypasses label review
- [ ] Preferred/fallback/human hierarchy passes failure, capacity and budget rehearsals
- [ ] Fallback quality, cost, compatibility and safe-failure behavior are documented
- [ ] Final architecture shows domain adapters, context, retrieval, routing, cache policy, traces and release gates

### Engineering note

Explain one observation that should not become a label, one unsafe fallback you prohibit, and the evidence required for the next release.

### Optional depth

Deploy a private demo or add the Paqet adapter only when its API and authorization contract are ready.

### Progress

The app calculates this week from Required readings, the assignment, deliverables, and exit criteria. Recommended and Optional reading checks are saved separately. The current checked state lives in browser storage and is not embedded in this document.

# Graduation outcomes

At the end of the 16 weeks, the learner should be able to build and explain:
- model API applications
- structured outputs
- tool calling
- tool error handling
- classical ML vs LLM tradeoffs
- evaluation-driven development
- prompt versioning
- embeddings
- lexical retrieval
- dense retrieval
- hybrid retrieval
- reranking
- retrieval evaluation
- production multi-tenant RAG
- context engineering
- token budgeting
- agents from first principles
- agent trajectory evaluation
- durable agent workflows
- MCP servers
- model routing
- evaluation CI gates
- AI observability
- semantic caching
- prompt-injection defenses
- tool least privilege
- human-in-the-loop controls
- cost/latency optimization
- fallback architecture
- production data/eval flywheels

# Further study — explicitly deferred

These topics are optional and add no required checkpoints to the 16-week course:
- multi-agent consensus systems
- voice agents
- computer-use agents
- local model inference
- LoRA/fine-tuning
- A2A protocols
- GPU/CUDA engineering
- training transformers
- building a workflow engine
- complex autonomous coding agents
The goal remains production AI engineering, not comprehensive machine-learning research.

# Capstone finish

The final learning finish is a reproducible simulator-backed Payment Reliability Copilot demo. It should combine payment investigation, RAG over runbooks, semantic incident search, typed tool calling and recovery, bounded multi-step investigations, MCP tools, citations, human approval, prompt/model versioned evals, tracing, cost tracking, authorization, least privilege, resilience, routing, guarded cache policy, and release gates. A live production rollout or Paqet integration is a separate operational and security milestone, not a course prerequisite.

# Document provenance

This consolidated document preserves the original 16-week seeded syllabus and appends the Week 2, 4, 6, 7, 9, 10, 11, 13, 14, 15, and 16 updates. The interactive tracker remains authoritative for current completion state; this file is the shareable reading and planning view.

