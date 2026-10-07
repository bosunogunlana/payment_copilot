# Build / Ship Learning Map

Start here to choose a week, then open its plan for scope and its tracker for session evidence. These documents break the build/ship segment into phases; use the [curriculum](payment-reliability-copilot/CURRICULUM.md) for readings and the [browser tracker instructions](payment-reliability-copilot/README.md) for course progress.

## How to use each week

1. Read the week’s prerequisites and ship target. Bring forward the named simulator, corpus, interfaces and evidence.
2. Open the tracker and choose the first phase without verified completion evidence. Work on one coherent batch within it.
3. Build your implementation; use the [learning assistant prompt](LEARNING-ASSISTANT-PROMPT.md) for guidance, tests, fixtures and review.
4. Break the slice, record actual results and review the exit gate before moving on.
5. Append the evidence and next action to the tracker. Finish with local reproducibility and an engineering note.

Plan = what to build and where to stop. Tracker = what the evidence supports. Browser tracker = Required readings and curriculum completion. Markdown edits do not update browser storage. Weeks 2–16 begin with unchecked planning baselines; no current learning progress is inferred.

## Weekly navigation

### Month 1 — LLMs as software

| Week | Build / ship plan | Evidence tracker |
| --- | --- | --- |
| 01 — Models, prompting & structured output | [Plan](WEEK-01-BUILD-SHIP.md) | [Tracker](WEEK-01-BUILD-SHIP-TRACKER.md) |
| 02 — Function calling & tool design | [Plan](WEEK-02-BUILD-SHIP.md) | [Tracker](WEEK-02-BUILD-SHIP-TRACKER.md) |
| 03 — Practical machine-learning foundations | [Plan](WEEK-03-BUILD-SHIP.md) | [Tracker](WEEK-03-BUILD-SHIP-TRACKER.md) |
| 04 — Evaluation-driven development | [Plan](WEEK-04-BUILD-SHIP.md) | [Tracker](WEEK-04-BUILD-SHIP-TRACKER.md) |

### Month 2 — Grounding & RAG

| Week | Build / ship plan | Evidence tracker |
| --- | --- | --- |
| 05 — Embeddings & semantic retrieval | [Plan](WEEK-05-BUILD-SHIP.md) | [Tracker](WEEK-05-BUILD-SHIP-TRACKER.md) |
| 06 — Build RAG manually | [Plan](WEEK-06-BUILD-SHIP.md) | [Tracker](WEEK-06-BUILD-SHIP-TRACKER.md) |
| 07 — Retrieval evaluation | [Plan](WEEK-07-BUILD-SHIP.md) | [Tracker](WEEK-07-BUILD-SHIP-TRACKER.md) |
| 08 — Production RAG & multi-tenancy | [Plan](WEEK-08-BUILD-SHIP.md) | [Tracker](WEEK-08-BUILD-SHIP-TRACKER.md) |

### Month 3 — Agentic systems

| Week | Build / ship plan | Evidence tracker |
| --- | --- | --- |
| 09 — Build an agent yourself | [Plan](WEEK-09-BUILD-SHIP.md) | [Tracker](WEEK-09-BUILD-SHIP-TRACKER.md) |
| 10 — Incident investigation agent | [Plan](WEEK-10-BUILD-SHIP.md) | [Tracker](WEEK-10-BUILD-SHIP-TRACKER.md) |
| 11 — LangGraph & durable workflows | [Plan](WEEK-11-BUILD-SHIP.md) | [Tracker](WEEK-11-BUILD-SHIP-TRACKER.md) |
| 12 — MCP + Go | [Plan](WEEK-12-BUILD-SHIP.md) | [Tracker](WEEK-12-BUILD-SHIP-TRACKER.md) |

### Month 4 — Production AI

| Week | Build / ship plan | Evidence tracker |
| --- | --- | --- |
| 13 — Serious evals | [Plan](WEEK-13-BUILD-SHIP.md) | [Tracker](WEEK-13-BUILD-SHIP-TRACKER.md) |
| 14 — AI observability | [Plan](WEEK-14-BUILD-SHIP.md) | [Tracker](WEEK-14-BUILD-SHIP-TRACKER.md) |
| 15 — AI security & reliability | [Plan](WEEK-15-BUILD-SHIP.md) | [Tracker](WEEK-15-BUILD-SHIP-TRACKER.md) |
| 16 — Ship the Payment Reliability Copilot | [Plan](WEEK-16-BUILD-SHIP.md) | [Tracker](WEEK-16-BUILD-SHIP-TRACKER.md) |

## Learning rhythm and boundaries

Budget 8–10 hours per week: about 2 reading, 4–5 building, 1–2 deliberate failure/evaluation and 1 documenting. Phase counts do not add hours. Keep required evidence visible when work runs long; optional depth stays optional.

Reuse one evolving project. Manual tool loops, cosine search, RAG and agent state come before their framework abstractions. Keep payment data synthetic and actions simulated. Live model comparisons need a spending allowance; a dry run or stub test does not prove live model quality. The capstone finish is a reproducible simulator demo, with any live production rollout handled separately.

All assignment paths in weekly documents resolve from the project root. The zero-padded filenames preserve the learning assistant’s `WEEK-{NN}` lookup. [Week 1 local guide](WEEK-01-LOCAL-GUIDE.md) remains available for its shipped diagnosis commands.
