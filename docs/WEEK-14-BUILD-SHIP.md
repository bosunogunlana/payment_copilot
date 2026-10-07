# Week 14 Build / Ship Plan — AI observability

[All weeks](BUILD-SHIP-INDEX.md) · [Week 14 tracker](WEEK-14-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-13-BUILD-SHIP.md) · [Next week](WEEK-15-BUILD-SHIP.md)

## Scope and ship target

Instrument request → agent trace → model call → tool call → retrieval → response. Build an AI Operations Dashboard with latency, tokens, cost, tool errors, retrieval latency, steps, completion %, escalation %, eval score, model, and prompt version.

**Learning goal:** Make every model call, tool call, retrieval, and escalation visible enough to operate in production.

**Before you start:** Reuse cost/latency records from Week 1 and trajectories from Week 9.

**Keep the build focused:** Instrument one end-to-end path with OpenTelemetry and one dashboard. Include all listed signals; keep high-cardinality payment IDs out of metric labels and redact sensitive span data. Extend one existing dashboard and one read-only investigation path. Use the existing simulator clock and state versions for invalidation tests.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 14. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Timing and trace contract](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Instrumentation and dashboard](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Guarded semantic cache experiment](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Freshness and permission attacks](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Cache-off/on measurement](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Timing and trace contract

### Goal

Define metrics before instrumenting the existing request path.

### Expected outcome and completion checklist

- [ ] Specify request → agent → model/tool/retrieval → response spans and correlation IDs.
- [ ] Define TTFT, total/model/tool/retrieval latency, throughput and timing boundaries.
- [ ] Distinguish provider timing, client timing, chunks and tokens.
- [ ] Use N/A for unavailable observations and specify conditional inter-token-gap measurements.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for timing and trace contract, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-14-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Instrumentation and dashboard

### Goal

Make a slow or failed request diagnosable without reading application logs.

### Expected outcome and completion checklist

- [ ] Instrument the existing runtime with OpenTelemetry, Prometheus and Grafana.
- [ ] Track tokens, cost, steps, completion, escalation, eval score, model and prompt version.
- [ ] Display p50/p95 latency, tool errors and retrieval latency.
- [ ] Provide AI operations and streaming-latency dashboards, marking unimplemented streaming metrics N/A.

### Primary files

- `observability/tracing/`
- `observability/metrics/`
- `observability/dashboards/ai-operations.json`
- `observability/dashboards/streaming-latency.json`

### Walkthrough needed

Explain the contract and data flow for instrumentation and dashboard, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-14-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Guarded semantic cache experiment

### Goal

Reuse equivalent authorized evidence only in the same valid state.

### Expected outcome and completion checklist

- [ ] Implement query embedding → authorized nearest cached query → threshold/equivalence/freshness checks → hit or agent miss.
- [ ] Scope by organization, permissions, payment ID, state/version, knowledge version and prompt/model configuration.
- [ ] Use expiry, invalidation and current-state revalidation; TTL alone cannot establish equivalence.
- [ ] Never cache mutations as executable actions.

### Primary files

- `app/cache/semantic_cache.py`

### Walkthrough needed

Explain the contract and data flow for guarded semantic cache experiment, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-14-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Freshness and permission attacks

### Goal

Make semantically similar unsafe reuse miss or invalidate.

### Expected outcome and completion checklist

- [ ] Test equivalent delayed/stuck queries in the same payment state.
- [ ] Change state, payment, tenant, permissions, runbook and prompt version.
- [ ] Assert changed state/access cannot reuse an old answer.
- [ ] Inject a provider error and drill from the dashboard to the exact tool/model span.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for freshness and permission attacks, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-14-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Cache-off/on measurement

### Goal

Include the costs of validation and misses in the cache decision.

### Expected outcome and completion checklist

- [ ] Compare cold and warm cache-off/on runs.
- [ ] Report hit rate, latency improvement, cost reduction and incorrect stale hits.
- [ ] Include embedding, state-validation and miss-path costs.
- [ ] Save semantic-cache.md and week14.md; leave runtime cache optional until correctness and benefit are demonstrated.

### Primary files

- `evals/reports/semantic-cache.md`

### Walkthrough needed

Explain the contract and data flow for cache-off/on measurement, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-14-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

- `docs/learning-notes/week14.md`

### Walkthrough needed

Explain the contract and data flow for local ship and learning handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-14-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Keep OpenTelemetry, Prometheus and Grafana. Add TTFT, total latency, model latency, tool latency, retrieval latency and tokens/second where observable. If streaming is implemented, measure inter-token gaps where practical; distinguish chunks from tokens, client-observed vs provider timing, and mark unavailable metrics N/A rather than zero.
- Build a small Semantic Cache experiment: query embedding → nearest authorized cached query → threshold plus equivalence/freshness checks → hit or agent on miss. Scope by organization, permissions, payment ID, payment state/version, knowledge version and prompt/model configuration. Use expiry and invalidation, and revalidate relevant current state before reuse. Never cache a mutation as an executable action or use TTL alone to establish response equivalence.
- Measure hit rate, latency improvement, cost reduction and incorrect stale hits including embedding, state-validation and miss-path costs. Keep the cache optional in the final runtime until correctness and benefit are demonstrated; the experiment itself is required.

## Curriculum contract — experiments and comparisons

- Compare “Why is payment 123 delayed?” and “What’s causing payment 123 to be stuck?” in the same state. Then change payment state, use another payment/tenant, revoke permission, change the runbook or bump the prompt version. These must miss or invalidate even when semantic similarity is high. Compare cache-off vs cache-on using cold and warm runs.

## Curriculum contract — metrics to record

- TTFT / time to first token · total_latency · model_latency · tool_latency · retrieval_latency · tokens_per_second · inter_token_gap (if streaming) · cache_hit_rate · latency_improvement · cost_reduction · incorrect_stale_hits

## Required failure and evaluation pass

Create a dashboard drill-down from a slow request to the exact tool/model span. Inject a provider error and verify it is visible without reading application logs.

## Curriculum deliverables

- [ ] `observability/tracing/`
- [ ] `observability/metrics/`
- [ ] `observability/dashboards/ai-operations.json`
- [ ] `docs/learning-notes/week14.md`
- [ ] `app/cache/semantic_cache.py`
- [ ] `evals/reports/semantic-cache.md`
- [ ] `observability/dashboards/streaming-latency.json`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

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

## Engineering note

Explain which computation is safe to reuse, why similarity is insufficient, and whether to enable the cache in the capstone.

## Optional depth — does not gate this week

Production alert routing and a hosted tracing vendor are optional.
