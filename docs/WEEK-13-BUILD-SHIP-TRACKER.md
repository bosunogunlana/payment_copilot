# Week 13 Build / Ship Tracker — Serious evals

[All weeks](BUILD-SHIP-INDEX.md) · [Week 13 plan](WEEK-13-BUILD-SHIP.md) · [Previous week](WEEK-12-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-14-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 13 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Versioned evaluation strategy](#phase-1) | Not started | — |
| 2 | [Graders and disagreement review](#phase-2) | Not started | — |
| 3 | [Rule-based model router](#phase-3) | Not started | — |
| 4 | [Router versus strongest experiment](#phase-4) | Not started | — |
| 5 | [CI regression and restore gates](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Versioned evaluation strategy

- [ ] Version 300–500 cases with 300+ required and 500 stretch.
- [ ] Cover investigation, retrieval, tool selection, insufficient information, ambiguity, outages, permission boundaries, injection and hallucination.
- [ ] Separate development and final held-out tasks.
- [ ] Define deterministic, human, LLM-judge and pairwise grading roles.

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

### Phase 2 — Graders and disagreement review

- [ ] Compare at least two grading methods.
- [ ] Review manual samples and document judge disagreement.
- [ ] Define denominators, missing-metric behavior and repeated-run policy.
- [ ] Extend existing runner and prompt registry rather than starting a new system.

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

### Phase 3 — Rule-based model router

- [ ] Implement cheap/normal/strong rules using task, context, complexity, tool needs, confidence, tenant budget and latency SLO.
- [ ] Calibrate confidence on held-out outcomes or combine it with evidence checks.
- [ ] Log routing reasons and bound attempts, total spend and latency.
- [ ] Escalate cheap → stronger on insufficient evidence without exceeding tenant budget.

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

### Phase 4 — Router versus strongest experiment

- [ ] Compare routing with always using the strongest model.
- [ ] Exercise simple, complex, large-context, tool-required and budget-exhausted cases.
- [ ] Include failed and escalated attempts in quality/cost/latency/escalation totals.
- [ ] Save model-routing.md under a declared live-comparison budget; keep deterministic stubs separate.

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

### Phase 5 — CI regression and restore gates

- [ ] Configure regression-thresholds.yaml and ci/eval-gates.yml.
- [ ] Document percentage-point versus relative change; example gates are accuracy drop >3 points, unsupported claims >5%, cross-tenant >0 and executed schemas <100%.
- [ ] Inject prompt regressions and security/schema failures; demonstrate a passing non-regressing run.
- [ ] Fail closed on missing metrics or broken evaluators and restore the prior prompt/model configuration.

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
| `evals/datasets/v1/` | 1 | Not started | — |
| `evals/graders/` | 2 | Not started | — |
| `evals/reports/week13.md` | 6 | Not started | — |
| `docs/evaluation-strategy.md` | 1 | Not started | — |
| `app/llm/router.py` | 3 | Not started | — |
| `evals/reports/model-routing.md` | 4 | Not started | — |
| `evals/regression-thresholds.yaml` | 5 | Not started | — |
| `ci/eval-gates.yml` | 5 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Compare deterministic assertions, human scoring, LLM-as-judge, and pairwise comparison. Sample cases manually and document judge disagreement.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Prompt quality regression | — | — | Define from phase acceptance checks | — | Not started |
| Cross-tenant violation / invalid executed schema | — | — | Define from phase acceptance checks | — | Not started |
| Missing metric / evaluator failure | — | — | Define from phase acceptance checks | — | Not started |
| Simple / complex / large-context / tool-required routes | — | — | Define from phase acceptance checks | — | Not started |
| Tenant budget exhausted | — | — | Define from phase acceptance checks | — | Not started |
| Router versus always-strongest on held-out tasks | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

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
