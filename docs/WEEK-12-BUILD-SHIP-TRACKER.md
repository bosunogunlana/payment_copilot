# Week 12 Build / Ship Tracker — MCP + Go

[All weeks](BUILD-SHIP-INDEX.md) · [Week 12 plan](WEEK-12-BUILD-SHIP.md) · [Previous week](WEEK-11-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-13-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 12 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [MCP and adapter contract](#phase-1) | Not started | — |
| 2 | [Go simulator server](#phase-2) | Not started | — |
| 3 | [Authorization and bounded execution](#phase-3) | Not started | — |
| 4 | [Client contract rehearsal](#phase-4) | Not started | — |
| 5 | [Clean-run handoff](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — MCP and adapter contract

- [ ] Define payment://{id} and incident://{id} resource shapes.
- [ ] Define get_payment, get_payment_events, search_incidents and get_provider_status tools.
- [ ] Document conceptual simulator/Paqet adapter interface.
- [ ] Define trusted identity, argument validation and stable error outcomes.

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

### Phase 2 — Go simulator server

- [ ] Build mcp/paqet-mcp/server.go with simulator adapters.
- [ ] Expose payment and incident resources and the four tools.
- [ ] Reject malformed requests and unknown IDs.
- [ ] Keep transport and domain adapter responsibilities separate.

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

### Phase 3 — Authorization and bounded execution

- [ ] Authorize tenant/resource/tool access in application code.
- [ ] Enforce tool timeouts and stable client-visible errors.
- [ ] Test forged or cross-tenant requests.
- [ ] Keep destructive operations simulated and require explicit argument-bound human approval for the destructive test path.

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

### Phase 4 — Client contract rehearsal

- [ ] Exercise resources and tools through an MCP client.
- [ ] Store malformed-request, unknown-ID, unauthorized and timeout cases in contract.jsonl.
- [ ] Include a denied or approval-gated simulated destructive request.
- [ ] Run Go request-validation tests and MCP contract checks.

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

### Phase 5 — Clean-run handoff

- [ ] Document build, run, client setup and tests in the server README.
- [ ] Run the contract suite from a clean source checkout.
- [ ] Explain MCP resources versus tools and stable errors.
- [ ] Record the future Paqet adapter seam without requiring a real integration or remote HTTP transport.

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
| `mcp/paqet-mcp/` | 2 | Not started | — |
| `mcp/paqet-mcp/server.go` | 2 | Not started | — |
| `mcp/paqet-mcp/README.md` | 5 | Not started | — |
| `evals/mcp/contract.jsonl` | 4 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Test malformed requests, unknown IDs, authorization boundaries, tool timeouts, and a destructive action that requires explicit human approval.

Use the plan’s phase checks to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Malformed request / unknown ID | — | — | Define from phase acceptance checks | — | Not started |
| Cross-tenant or unauthorized resource/tool call | — | — | Define from phase acceptance checks | — | Not started |
| Tool timeout and stable client error | — | — | Define from phase acceptance checks | — | Not started |
| Unapproved simulated destructive request | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] Server exposes resources and tools
- [ ] Go tests cover request validation
- [ ] Client receives stable errors
- [ ] Simulator and Paqet adapters share a conceptual interface
- [ ] Destructive operations require approval
- [ ] MCP contract tests pass from a clean run

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
