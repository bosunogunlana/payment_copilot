# Week 16 Build / Ship Tracker — Ship the Payment Reliability Copilot

[All weeks](BUILD-SHIP-INDEX.md) · [Week 16 plan](WEEK-16-BUILD-SHIP.md) · [Previous week](WEEK-15-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 16 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Capstone integration and release manifest](#phase-1) | Not started | — |
| 2 | [Curated data-to-eval flywheel](#phase-2) | Not started | — |
| 3 | [Preferred/fallback/human hierarchy](#phase-3) | Not started | — |
| 4 | [Failure and recovery rehearsal](#phase-4) | Not started | — |
| 5 | [Portfolio freeze and explanation](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Capstone integration and release manifest

- [ ] Verify natural-language investigation, RAG, incident search, tool calling, bounded agents, MCP, citations and approval paths.
- [ ] Pin domain adapters, context/retrieval/router/cache policy, prompt/model/dataset versions and traces.
- [ ] Carry forward eval, authorization, resilience and cost controls.
- [ ] Inventory open gaps and keep live production release separate.

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

### Phase 2 — Curated data-to-eval flywheel

- [ ] Document thumbs down, human corrections, agent failures, tool failures, low confidence and production incidents as candidate sources.
- [ ] Redact, deduplicate, retain provenance and require human label review.
- [ ] Protect held-out evaluation and document authorization/consent/retention before real-data use.
- [ ] Convert synthetic thumbs-down, correction and tool failure into reviewed versioned cases and rerun evals.

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

### Phase 3 — Preferred/fallback/human hierarchy

- [ ] Reuse Week 13 router and typed errors for preferred → fallback → human escalation.
- [ ] Define failure/capacity/budget criteria, maximum attempts, cost and latency bounds.
- [ ] Check tool/schema compatibility and preserve tenant/tool/approval policies across models.
- [ ] Document fallback quality/cost consequences and evidence-backed escalation reasons.

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

### Phase 4 — Failure and recovery rehearsal

- [ ] Inject preferred-model failure, capacity rejection and exhausted budget.
- [ ] Make fallback fail or lack evidence and verify bounded human escalation.
- [ ] Rehearse happy path, insufficient evidence, provider outage, injection, cross-tenant request, duplicate side effect and process restart.
- [ ] Keep traces, final eval report and fallback-rehearsal.md including failures and tradeoffs.

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

### Phase 5 — Portfolio freeze and explanation

- [ ] Write architecture.md showing adapters, context, retrieval, routing, cache, traces and release gates.
- [ ] Write case-study.md explaining why AI fits and what changes at 100× scale.
- [ ] Freeze and record a 2–4 minute payment-copilot-demo.mp4.
- [ ] Document one observation unsuitable as a label, one prohibited fallback and evidence required for the next release.

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
| `docs/architecture.md` | 5 | Not started | — |
| `evals/reports/final.md` | 4 | Not started | — |
| `demo/payment-copilot-demo.mp4` | 5 | Not started | — |
| `docs/case-study.md` | 5 | Not started | — |
| `docs/data-eval-flywheel.md` | 2 | Not started | — |
| `evals/candidates/reviewed-examples.jsonl` | 2 | Not started | — |
| `docs/fallback-architecture.md` | 3 | Not started | — |
| `evals/reports/fallback-rehearsal.md` | 4 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Run a final rehearsal with a happy path, insufficient evidence, provider outage, prompt injection, cross-tenant request, duplicate side effect, and process restart. Keep the trace and the eval report.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Synthetic thumbs-down / correction / tool-failure review | — | — | Define from phase acceptance checks | — | Not started |
| Preferred model failure / capacity rejection / exhausted budget | — | — | Define from phase acceptance checks | — | Not started |
| Fallback failure or insufficient evidence | — | — | Define from phase acceptance checks | — | Not started |
| Happy path / insufficient evidence / provider outage | — | — | Define from phase acceptance checks | — | Not started |
| Prompt injection / cross-tenant request | — | — | Define from phase acceptance checks | — | Not started |
| Duplicate side effect / process restart | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

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
