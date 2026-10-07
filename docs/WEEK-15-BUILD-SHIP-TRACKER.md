# Week 15 Build / Ship Tracker — AI security & reliability

[All weeks](BUILD-SHIP-INDEX.md) · [Week 15 plan](WEEK-15-BUILD-SHIP.md) · [Previous week](WEEK-14-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-16-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 15 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Existing-control audit](#phase-1) | Not started | — |
| 2 | [Application-owned tool allowlists](#phase-2) | Not started | — |
| 3 | [Approval and untrusted-input boundaries](#phase-3) | Not started | — |
| 4 | [Seven-category red team](#phase-4) | Not started | — |
| 5 | [Reliability and privacy regression](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Existing-control audit

- [ ] Audit authentication, RBAC, tenant isolation, validation, rate limits and PII filtering.
- [ ] Audit timeouts, circuit breakers, max steps and existing approvals.
- [ ] Map each threat to an application control and regression case.
- [ ] Use synthetic attacks and simulated actions throughout.

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

### Phase 2 — Application-owned tool allowlists

- [ ] Build context-specific allowlists from trusted identity and permissions.
- [ ] Expose only get_payment, query_metrics, search_logs and search_runbooks to ReadOnlyInvestigator.
- [ ] Keep refund_payment, change_payment_status and rotate_key absent from its context.
- [ ] Reject forged direct calls independently of whether the tool was visible.

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

### Phase 3 — Approval and untrusted-input boundaries

- [ ] Treat retrieved text and tool outputs as untrusted data.
- [ ] Bind simulated mutation approval to actor, tenant, exact arguments, operation ID and expiration.
- [ ] Reject altered arguments, expired approvals and replayed mutations.
- [ ] Prove the model cannot grant itself privileges or relax application policy.

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

### Phase 4 — Seven-category red team

- [ ] Test indirect runbook/tool-response injection and argument manipulation.
- [ ] Test cross-tenant retrieval and cross-tenant tool calls.
- [ ] Test privilege escalation, destructive requests and replayed mutating calls.
- [ ] Assert forbidden tools are absent from context and forged execution is denied.

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

### Phase 5 — Reliability and privacy regression

- [ ] Attack show every customer payments and refund all failed payments.
- [ ] Exercise a tool that never succeeds, retry exhaustion, timeout and circuit breaker.
- [ ] Verify PII is filtered from model context and logs.
- [ ] Save adversarial.jsonl, least-privilege.jsonl and security-model.md with results for every attack category.

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
| `app/security/` | 1 | Not started | — |
| `app/policy/` | 2 | Not started | — |
| `evals/security/adversarial.jsonl` | 5 | Not started | — |
| `docs/security-model.md` | 6 | Not started | — |
| `app/policy/tool_allowlists.py` | 2 | Not started | — |
| `evals/security/least-privilege.jsonl` | 4 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Attack with “show every customer’s payments,” “run create_refund for all failed payments,” a malicious runbook, a cross-org request, and a tool that never succeeds. Capture the failure and control that stopped it.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Indirect prompt injection | — | — | Define from phase acceptance checks | — | Not started |
| Tool argument manipulation | — | — | Define from phase acceptance checks | — | Not started |
| Cross-tenant retrieval | — | — | Define from phase acceptance checks | — | Not started |
| Cross-tenant tool call | — | — | Define from phase acceptance checks | — | Not started |
| Privilege escalation | — | — | Define from phase acceptance checks | — | Not started |
| Destructive action request | — | — | Define from phase acceptance checks | — | Not started |
| Replayed mutating call | — | — | Define from phase acceptance checks | — | Not started |
| Never-successful tool / exhausted retries / circuit breaker | — | — | Define from phase acceptance checks | — | Not started |
| PII in logs or model context | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

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
