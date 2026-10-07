# Week 10 Build / Ship Tracker — Incident investigation agent

[All weeks](BUILD-SHIP-INDEX.md) · [Week 10 plan](WEEK-10-BUILD-SHIP.md) · [Previous week](WEEK-09-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-11-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 10 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Incident evidence and labels](#phase-1) | Not started | — |
| 2 | [Operational investigation tools](#phase-2) | Not started | — |
| 3 | [Investigator integration](#phase-3) | Not started | — |
| 4 | [Trajectory grading](#phase-4) | Not started | — |
| 5 | [Answer and trajectory evaluation](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Incident evidence and labels

- [ ] Create at least 30 seeded time-series incident variants in the existing simulator.
- [ ] Label root causes, required evidence and acceptable alternative tool orders.
- [ ] Define the last-30-minutes USDC withdrawal success-rate question.
- [ ] Reuse Week 9 state, budgets and trace store.

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

### Phase 2 — Operational investigation tools

- [ ] Implement query_metrics, search_logs, find_incidents and list_failed_payments.
- [ ] Reuse get_provider_status and search_runbooks.
- [ ] Enforce trusted scope and typed tool errors.
- [ ] Test timing windows and conflicting operational observations.

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

### Phase 3 — Investigator integration

- [ ] Connect tools to the existing bounded investigator.
- [ ] Record evidence sources supporting root-cause claims.
- [ ] Escalate insufficient evidence rather than guessing.
- [ ] Keep observable trajectories and per-investigation tokens, cost and latency.

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

### Phase 4 — Trajectory grading

- [ ] Grade first tool, sufficient evidence, irrelevant tools, repeats, stopping and budgets.
- [ ] Allow scenario-specific alternative tool orders rather than one rigid script.
- [ ] Report correct_tool_selection, unnecessary_tool_calls, duplicate_tool_calls, steps_to_resolution, tool_error_recovery and trajectory_success.
- [ ] Document denominators and mark error recovery N/A when no tool error occurred.

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

### Phase 5 — Answer and trajectory evaluation

- [ ] Compare missing-evidence correctness, efficient evidence-backed diagnosis, over-budget work, unnecessary repeat and recovered timeout.
- [ ] Evaluate the same 30 scenarios, without creating another dataset.
- [ ] Measure ≥80% correct root cause, ≥90% no unsupported claims and zero infinite loops.
- [ ] Save trajectory-quality.md with average tool calls and quality/cost/latency tradeoffs.

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
| `simulator/scenarios/` | 1 | Not started | — |
| `app/agents/investigator.py` | 3 | Not started | — |
| `evals/agent/scenarios.jsonl` | 1 | Not started | — |
| `evals/graders/trajectory.py` | 4 | Not started | — |
| `evals/reports/trajectory-quality.md` | 5 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Evaluate both final diagnosis and trajectory: relevant evidence inspected, unnecessary calls, premature stopping, root-cause confidence, and unsupported claims.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Correct guessed diagnosis without evidence | — | — | Define from phase acceptance checks | — | Not started |
| Efficient supported diagnosis | — | — | Define from phase acceptance checks | — | Not started |
| Over-budget investigation | — | — | Define from phase acceptance checks | — | Not started |
| Unnecessary repeat | — | — | Define from phase acceptance checks | — | Not started |
| Recovered timeout | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] At least 30 incident scenarios exist
- [ ] ≥80% correct root cause
- [ ] ≥90% no unsupported root-cause claims
- [ ] Zero infinite loops
- [ ] Average tool calls are tracked
- [ ] Tokens, cost, and latency per investigation are tracked
- [ ] Trajectory grading checks first tool, evidence coverage, repeats, stopping and budgets
- [ ] All six trajectory metrics are reported alongside final-answer quality
- [ ] An unsupported lucky diagnosis cannot pass trajectory_success

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
