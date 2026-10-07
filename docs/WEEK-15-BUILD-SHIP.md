# Week 15 Build / Ship Plan — AI security & reliability

[All weeks](BUILD-SHIP-INDEX.md) · [Week 15 tracker](WEEK-15-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-14-BUILD-SHIP.md) · [Next week](WEEK-16-BUILD-SHIP.md)

## Scope and ship target

Audit and strengthen the security controls built in earlier weeks: authentication, RBAC, tenant isolation, tool permissions, validation, rate limits, PII filtering, injection defenses, timeouts, circuit breakers, max steps and argument-bound human approval. Keep actions simulator-only.

**Learning goal:** Attack the system before an operator—or a malicious prompt—does it for you.

**Before you start:** Revisit the boundaries introduced in Weeks 2, 8, 9 and 11.

**Keep the build focused:** Audit and strengthen existing controls rather than adding security for the first time. Use synthetic adversarial inputs; test authorization, tenant isolation, approval replay and retry exhaustion. Extend the existing security suite and simulated actions. No real refunds, status changes, key rotation or new identity provider.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 15. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [Existing-control audit](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Application-owned tool allowlists](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Approval and untrusted-input boundaries](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Seven-category red team](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Reliability and privacy regression](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: Existing-control audit

### Goal

Strengthen the accumulated boundaries using a concrete threat model.

### Expected outcome and completion checklist

- [ ] Audit authentication, RBAC, tenant isolation, validation, rate limits and PII filtering.
- [ ] Audit timeouts, circuit breakers, max steps and existing approvals.
- [ ] Map each threat to an application control and regression case.
- [ ] Use synthetic attacks and simulated actions throughout.

### Primary files

- `app/security/`

### Walkthrough needed

Explain the contract and data flow for existing-control audit, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-15-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Application-owned tool allowlists

### Goal

Restrict model visibility and independently authorize execution.

### Expected outcome and completion checklist

- [ ] Build context-specific allowlists from trusted identity and permissions.
- [ ] Expose only get_payment, query_metrics, search_logs and search_runbooks to ReadOnlyInvestigator.
- [ ] Keep refund_payment, change_payment_status and rotate_key absent from its context.
- [ ] Reject forged direct calls independently of whether the tool was visible.

### Primary files

- `app/policy/`
- `app/policy/tool_allowlists.py`

### Walkthrough needed

Explain the contract and data flow for application-owned tool allowlists, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-15-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Approval and untrusted-input boundaries

### Goal

Prevent injected instructions and replay from changing authority.

### Expected outcome and completion checklist

- [ ] Treat retrieved text and tool outputs as untrusted data.
- [ ] Bind simulated mutation approval to actor, tenant, exact arguments, operation ID and expiration.
- [ ] Reject altered arguments, expired approvals and replayed mutations.
- [ ] Prove the model cannot grant itself privileges or relax application policy.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for approval and untrusted-input boundaries, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-15-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Seven-category red team

### Goal

Capture the exact control stopping each adversarial attempt.

### Expected outcome and completion checklist

- [ ] Test indirect runbook/tool-response injection and argument manipulation.
- [ ] Test cross-tenant retrieval and cross-tenant tool calls.
- [ ] Test privilege escalation, destructive requests and replayed mutating calls.
- [ ] Assert forbidden tools are absent from context and forged execution is denied.

### Primary files

- `evals/security/least-privilege.jsonl`

### Walkthrough needed

Explain the contract and data flow for seven-category red team, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-15-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Reliability and privacy regression

### Goal

Verify controls under exhausted budgets and hostile inputs.

### Expected outcome and completion checklist

- [ ] Attack show every customer payments and refund all failed payments.
- [ ] Exercise a tool that never succeeds, retry exhaustion, timeout and circuit breaker.
- [ ] Verify PII is filtered from model context and logs.
- [ ] Save adversarial.jsonl, least-privilege.jsonl and security-model.md with results for every attack category.

### Primary files

- `evals/security/adversarial.jsonl`

### Walkthrough needed

Explain the contract and data flow for reliability and privacy regression, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-15-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

- `docs/security-model.md`

### Walkthrough needed

Explain the contract and data flow for local ship and learning handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-15-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Curriculum contract — added implementation requirements

- Keep all existing security controls and red-team exercises. Build context-specific tool allowlists. ReadOnlyInvestigator sees get_payment, query_metrics, search_logs and search_runbooks; refund_payment, change_payment_status and rotate_key are not visible. Application code selects exposed tools using trusted identity and permissions, then authorizes every call again at execution time. Hiding a tool is defense in depth, not the authorization check.
- Treat retrieved text and tool outputs as untrusted. Bind any simulated mutation approval to the actor, tenant, exact arguments, operation ID and expiration. Prevent replay and do not let an LLM grant itself privilege or relax a boundary.

## Curriculum contract — experiments and comparisons

- Test indirect prompt injection in a runbook/tool response, tool argument manipulation, cross-tenant retrieval, cross-tenant tool calls, privilege escalation, a destructive action request and a replayed mutating call. Assert both that forbidden tools are absent from context and that forged direct calls are rejected.

## Required failure and evaluation pass

Attack with “show every customer’s payments,” “run create_refund for all failed payments,” a malicious runbook, a cross-org request, and a tool that never succeeds. Capture the failure and control that stopped it.

## Curriculum deliverables

- [ ] `app/security/`
- [ ] `app/policy/`
- [ ] `evals/security/adversarial.jsonl`
- [ ] `docs/security-model.md`
- [ ] `app/policy/tool_allowlists.py`
- [ ] `evals/security/least-privilege.jsonl`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

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

## Engineering note

Explain why a prompt saying “do not refund” is not a security control, and distinguish hidden tools from authorized execution.

## Optional depth — does not gate this week

Provider-specific policies are extensions. No live refunds, transfers or production credentials are needed.
