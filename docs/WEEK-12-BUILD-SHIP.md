# Week 12 Build / Ship Plan — MCP + Go

[All weeks](BUILD-SHIP-INDEX.md) · [Week 12 tracker](WEEK-12-BUILD-SHIP-TRACKER.md) · [Previous week](WEEK-11-BUILD-SHIP.md) · [Next week](WEEK-13-BUILD-SHIP.md)

## Scope and ship target

Build a small Paqet MCP server in Go. Expose payment://{id}, incident://{id}, and tools for get_payment, get_payment_events, search_incidents, and get_provider_status. Use simulator adapters until Paqet is ready.

**Learning goal:** Turn payment-domain capabilities into reusable AI infrastructure and connect your Go learning to a real boundary.

**Before you start:** Know Go structs, interfaces, errors and tests; use the official Go SDK example as your starting point.

**Keep the build focused:** Build a local stdio MCP server backed by fixtures, with the listed resources and read-only tools. Pin SDK/protocol versions together and test through a real client.

Source: [Curriculum](payment-reliability-copilot/CURRICULUM.md), Week 12. This guide sequences the build/ship assignment; Required readings remain in the curriculum.

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
| 1 | [MCP and adapter contract](#phase-1) | Phase checklist, acceptance run and evidence note |
| 2 | [Go simulator server](#phase-2) | Phase checklist, acceptance run and evidence note |
| 3 | [Authorization and bounded execution](#phase-3) | Phase checklist, acceptance run and evidence note |
| 4 | [Client contract rehearsal](#phase-4) | Phase checklist, acceptance run and evidence note |
| 5 | [Clean-run handoff](#phase-5) | Phase checklist, acceptance run and evidence note |
| 6 | [Local ship and learning handoff](#phase-6) | Phase checklist, acceptance run and evidence note |

<a id="phase-1"></a>

## Phase 1: MCP and adapter contract

### Goal

Expose the same domain boundary through a small Go server.

### Expected outcome and completion checklist

- [ ] Define payment://{id} and incident://{id} resource shapes.
- [ ] Define get_payment, get_payment_events, search_incidents and get_provider_status tools.
- [ ] Document conceptual simulator/Paqet adapter interface.
- [ ] Define trusted identity, argument validation and stable error outcomes.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for mcp and adapter contract, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 1 of the tracker](WEEK-12-BUILD-SHIP-TRACKER.md#phase-1). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-2"></a>

## Phase 2: Go simulator server

### Goal

Implement protocol primitives against existing synthetic evidence.

### Expected outcome and completion checklist

- [ ] Build mcp/paqet-mcp/server.go with simulator adapters.
- [ ] Expose payment and incident resources and the four tools.
- [ ] Reject malformed requests and unknown IDs.
- [ ] Keep transport and domain adapter responsibilities separate.

### Primary files

- `mcp/paqet-mcp/`
- `mcp/paqet-mcp/server.go`

### Walkthrough needed

Explain the contract and data flow for go simulator server, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 2 of the tracker](WEEK-12-BUILD-SHIP-TRACKER.md#phase-2). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-3"></a>

## Phase 3: Authorization and bounded execution

### Goal

Protect the protocol boundary independently of client/model behavior.

### Expected outcome and completion checklist

- [ ] Authorize tenant/resource/tool access in application code.
- [ ] Enforce tool timeouts and stable client-visible errors.
- [ ] Test forged or cross-tenant requests.
- [ ] Keep destructive operations simulated and require explicit argument-bound human approval for the destructive test path.

### Primary files

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for authorization and bounded execution, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 3 of the tracker](WEEK-12-BUILD-SHIP-TRACKER.md#phase-3). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-4"></a>

## Phase 4: Client contract rehearsal

### Goal

Verify real protocol behavior rather than only local function calls.

### Expected outcome and completion checklist

- [ ] Exercise resources and tools through an MCP client.
- [ ] Store malformed-request, unknown-ID, unauthorized and timeout cases in contract.jsonl.
- [ ] Include a denied or approval-gated simulated destructive request.
- [ ] Run Go request-validation tests and MCP contract checks.

### Primary files

- `evals/mcp/contract.jsonl`

### Walkthrough needed

Explain the contract and data flow for client contract rehearsal, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 4 of the tracker](WEEK-12-BUILD-SHIP-TRACKER.md#phase-4). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Stay within this phase; advance when its checklist is supported by evidence. Retain earlier passing contracts and leave optional depth until the required slice works.

<a id="phase-5"></a>

## Phase 5: Clean-run handoff

### Goal

Make the Go boundary reproducible and explainable.

### Expected outcome and completion checklist

- [ ] Document build, run, client setup and tests in the server README.
- [ ] Run the contract suite from a clean source checkout.
- [ ] Explain MCP resources versus tools and stable errors.
- [ ] Record the future Paqet adapter seam without requiring a real integration or remote HTTP transport.

### Primary files

- `mcp/paqet-mcp/README.md`

### Walkthrough needed

Explain the contract and data flow for clean-run handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 5 of the tracker](WEEK-12-BUILD-SHIP-TRACKER.md#phase-5). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

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

Use the preceding phases’ artifacts and their acceptance tests; avoid creating a parallel implementation.

### Walkthrough needed

Explain the contract and data flow for local ship and learning handoff, which existing boundary to extend, and why each failure or measurement belongs in this phase. Use interfaces and pseudocode; keep implementation learner-owned.

### Acceptance evidence and exit gate

Record the exact command or review procedure, input/dataset/configuration versions, observed result and limitations in [Phase 6 of the tracker](WEEK-12-BUILD-SHIP-TRACKER.md#phase-6). Each checklist item needs an artifact or assertion that demonstrates it. A file existing or a plausible model answer alone is insufficient.

### Stop boundary

Finish the local reproducibility and learning evidence. Identify supported browser checkpoints without changing browser progress automatically.

## Required failure and evaluation pass

Test malformed requests, unknown IDs, authorization boundaries, tool timeouts, and a destructive action that requires explicit human approval.

## Curriculum deliverables

- [ ] `mcp/paqet-mcp/`
- [ ] `mcp/paqet-mcp/server.go`
- [ ] `mcp/paqet-mcp/README.md`
- [ ] `evals/mcp/contract.jsonl`

## Definition of done

Complete all six phase gates, all curriculum deliverables and every exit criterion below with evidence. Save exact reproduction commands, measured failures and limitations. This completes the implementation slice; Required readings and browser course completion are separate.

- [ ] Server exposes resources and tools
- [ ] Go tests cover request validation
- [ ] Client receives stable errors
- [ ] Simulator and Paqet adapters share a conceptual interface
- [ ] Destructive operations require approval
- [ ] MCP contract tests pass from a clean run

## Engineering note

Explain the primitive, a deliberate failure, your evidence and the tradeoff you would revisit.

## Optional depth — does not gate this week

Remote HTTP transport and real Paqet integration are extensions. Keep all destructive actions simulated.
