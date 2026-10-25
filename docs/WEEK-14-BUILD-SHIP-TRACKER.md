# Week 14 Build / Ship Tracker — AI observability

[All weeks](BUILD-SHIP-INDEX.md) · [Week 14 plan](WEEK-14-BUILD-SHIP.md) · [Previous week](WEEK-13-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-15-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 14 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Timing and trace contract](#phase-1) | Not started | — |
| 2 | [Instrumentation and dashboard](#phase-2) | Not started | — |
| 3 | [Guarded semantic cache experiment](#phase-3) | Not started | — |
| 4 | [Freshness and permission attacks](#phase-4) | Not started | — |
| 5 | [Cache-off/on measurement](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Timing and trace contract

- [ ] Specify request → agent → model/tool/retrieval → response spans and correlation IDs.
- [ ] Define TTFT, total/model/tool/retrieval latency, throughput and timing boundaries.
- [ ] Distinguish provider timing, client timing, chunks and tokens.
- [ ] Use N/A for unavailable observations and specify conditional inter-token-gap measurements.

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

### Phase 2 — Instrumentation and dashboard

- [ ] Instrument the existing runtime with OpenTelemetry, Prometheus and Grafana.
- [ ] Track tokens, cost, steps, completion, escalation, eval score, model and prompt version.
- [ ] Display p50/p95 latency, tool errors and retrieval latency.
- [ ] Provide AI operations and streaming-latency dashboards, marking unimplemented streaming metrics N/A.

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

### Phase 3 — Guarded semantic cache experiment

- [ ] Implement query embedding → authorized nearest cached query → threshold/equivalence/freshness checks → hit or agent miss.
- [ ] Scope by organization, permissions, payment ID, state/version, knowledge version and prompt/model configuration.
- [ ] Use expiry, invalidation and current-state revalidation; TTL alone cannot establish equivalence.
- [ ] Never cache mutations as executable actions.

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

### Phase 4 — Freshness and permission attacks

- [ ] Test equivalent delayed/stuck queries in the same payment state.
- [ ] Change state, payment, tenant, permissions, runbook and prompt version.
- [ ] Assert changed state/access cannot reuse an old answer.
- [ ] Inject a provider error and drill from the dashboard to the exact tool/model span.

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

### Phase 5 — Cache-off/on measurement

- [ ] Compare cold and warm cache-off/on runs.
- [ ] Report hit rate, latency improvement, cost reduction and incorrect stale hits.
- [ ] Include embedding, state-validation and miss-path costs.
- [ ] Save semantic-cache.md and week14.md; leave runtime cache optional until correctness and benefit are demonstrated.

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
| `observability/tracing/` | 2 | Not started | — |
| `observability/metrics/` | 2 | Not started | — |
| `observability/dashboards/ai-operations.json` | 2 | Not started | — |
| `docs/learning-notes/week14.md` | 6 | Not started | — |
| `app/cache/semantic_cache.py` | 3 | Not started | — |
| `evals/reports/semantic-cache.md` | 5 | Not started | — |
| `observability/dashboards/streaming-latency.json` | 2 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Create a dashboard drill-down from a slow request to the exact tool/model span. Inject a provider error and verify it is visible without reading application logs.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Same-state delayed/stuck query equivalence | — | — | Define from phase acceptance checks | — | Not started |
| Payment state or payment ID changed | — | — | Define from phase acceptance checks | — | Not started |
| Tenant changed or permission revoked | — | — | Define from phase acceptance checks | — | Not started |
| Runbook or prompt version changed | — | — | Define from phase acceptance checks | — | Not started |
| Provider error and slow-request drill-down | — | — | Define from phase acceptance checks | — | Not started |
| Cold/warm cache-off versus cache-on | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

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
