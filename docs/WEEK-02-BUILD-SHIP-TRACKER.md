# Week 2 Build / Ship Tracker — Function calling & tool design

[All weeks](BUILD-SHIP-INDEX.md) · [Week 2 plan](WEEK-02-BUILD-SHIP.md) · [Previous week](WEEK-01-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-03-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: In progress
- Current phase: Phase 6
- Last evidence update: 2026-10-18
- Main blocker: Working-source checks pass; committed HEAD lacks the recovery runner and learning note. Fresh dependency installation remains unverified.
- Next action: Commit intended Week 2 recovery and handoff artifacts, then verify the complete committed source.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Tool contracts and identity](#phase-1) | Done | All 66 tests pass; messages, trace IDs and keyword callable contracts verified |
| 2 | [Fixture-backed execution](#phase-2) | Done | All 78 tests pass, including 12 Phase 2 methods |
| 3 | [Manual tool lifecycle](#phase-3) | Done | All 96 tests pass, including 18 offline loop methods |
| 4 | [Bounded recovery and replay](#phase-4) | Done | 114 tests pass, including 18 recovery/replay methods |
| 5 | [Tool selection and recovery evaluation](#phase-5) | Done | Selection 38/40; recovery 17/17; 165 tests pass; lifecycle note reviewed |
| 6 | [Local ship and learning handoff](#phase-6) | In progress | Working source: 165 tests and recovery 17/17; committed HEAD: 160 tests, incomplete artifacts |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Tool contracts and identity

- [x] Define schemas for get_payment, get_payment_events, get_ledger_entries and get_provider_status.
- [x] Carry trusted organization identity separately from model arguments.
- [x] Define ToolError(code, retryable, message) and safe trace fields.
- [x] Reject malformed arguments and denied authorization before fixture access.

Evidence / notes:

```text
Status: Done
Files or links: app/tools/contracts.py; app/tools/errors.py; app/tools/gateway.py; tests/test_tool_contracts.py
Command / review procedure: `../.venv/bin/python -m unittest discover -s tests -q`
Dataset / prompt / model / policy versions (where relevant): Phase 1 mocks only; no fixtures or model calls
Observed result / metrics: 2026-10-09 full suite: all 66 tests pass in 0.510s. Earlier message/trace failures are resolved; Authorize/Reader protocols match keyword invocation signatures.
What this proves: Four strict argument schemas, trusted identity separation, validation-before-authorization, deny-before-reader, literal-True decisions, bounded trace fields and exclusive results pass existing checks.
Limitations / unverified behavior: Real fixture tenant isolation is Phase 2; no live model requests. Core files remain learner-owned and untracked at review time.
Open question / blocker: None for Phase 1. Nonblocking: align the unused lowercase error enum with emitted uppercase codes, require a nonblank ToolError message, complete annotations/keyword-only signatures and normalize formatting.
Next action: Phase 2 fixture-backed execution. No fixture implementation, tenant-data test, recovery or live-model quality is established by this phase.
```

<a id="phase-2"></a>

### Phase 2 — Fixture-backed execution

- [x] Implement the four tools using synthetic simulator fixtures.
- [x] Cover unknown payment IDs, invalid providers and payment-not-found.
- [x] Distinguish malformed and empty responses from successful evidence.
- [x] Test Org A cannot read Org B fixtures through any tool.

Evidence / notes:

```text
Status: Done
Files or links: app/tools/fixture_reader.py; app/models/evidence.py; app/tools/errors.py; app/tools/gateway.py; simulator/fixtures/week2_tools.json; simulator/fixtures/README.md; tests/test_fixture_tools.py
Command / review procedure: `../.venv/bin/python -m unittest discover -s tests -q`
Dataset / prompt / model / policy versions (where relevant): synthetic week2_tools.json version 1; offline mocks; no model calls
Observed result / metrics: All 78 tests pass in 0.434s; 12 Phase 2 test methods cover typed/deterministic outputs, tenant collisions, cross-tenant/nonexistent IDs, invalid providers, empty collections, absent responses, malformed payloads, embedded identity mismatches and exception propagation.
What this proves: All four fixture readers use scoped organization/payment lookup. Expected failures raise ToolReadError; gateway preserves the original error, emits failed traces with payment ID/error code and does not mask unexpected reader defects. Earlier failed-trace regression resolved.
Limitations / unverified behavior: Synthetic local evidence only; no real provider, model selection or recovery proof. Source/dependency reproducibility remains Phase 6. New core/fixture/test files remain untracked at review time. File-loading errors surface at construction.
Open question / blocker: None for this phase. Nonblocking: align Reader protocol argument type with BaseToolArgument, narrow evidence return types, move success-result construction outside reader try, remove unused data_key_name metadata and normalize model formatting.
Next action: Phase 3 manual tool lifecycle; no framework adoption.
```

<a id="phase-3"></a>

### Phase 3 — Manual tool lifecycle

- [x] Implement the manual tool loop without an agent framework.
- [x] Validate tool name and arguments and authorize every execution.
- [x] Record requested tool, arguments, result and timing in the trace.
- [x] Enforce maximum tool steps and distinguish fresh reads from stale repeated invocations.

Evidence / notes:

```text
Status: Done
Files or links: app/llm/tool_loop.py; tests/test_tool_loop.py; docs/WEEK-02-TOOL-LOOP-CONTRACT.md
Command / review procedure: `../.venv/bin/python -m unittest discover -s tests -q`
Dataset / prompt / model / policy versions (where relevant): scripted offline model; Phase 2 synthetic fixture version 1; normalized application-owned model-turn format
Observed result / metrics: All 96 tests pass in 0.419s, including 18 loop methods.
What this proves: Final-only and multi-call lifecycles; registry-derived schemas; batch validation before execution; gateway validation/authorization; call/result correlation; safe argument traces; typed reader errors; independent call/turn limits; replay rejection; reauthorized fresh reads and run-local state. Unexpected defects propagate.
Limitations / unverified behavior: No SDK wire adapter, paid requests, model tool-selection accuracy or retry/deadline proof. Fresh-read classification describes new call identity, not actual evidence freshness. Core, contract and test files are untracked at review time.
Open question / blocker: None for this bounded phase. Nonblocking: rename raw_argunents, annotate run return/model callable/gateway dependencies, constrain repetition values and simplify nested control flow without changing behavior.
Next action: Phase 4 bounded recovery and fake local side-effect replay; retain passing Phase 1–3 contracts.
```

<a id="phase-4"></a>

### Phase 4 — Bounded recovery and replay

- [x] Set per-attempt timeout, total deadline, maximum attempts and backoff.
- [x] Test timeout and 500 retryability; never automatically retry invalid arguments or denied access.
- [x] Use a stable operation key for one fake local side effect.
- [x] Simulate commit followed by timeout and prove retry cannot duplicate the effect.

Evidence / notes:

```text
Status: Done
Files or links: app/tools/recovery.py; simulator/idempotency.py; tests/test_tool_recovery.py; docs/WEEK-02-RECOVERY-CONTRACT.md
Command / review procedure: ../.venv/bin/python -m unittest discover -s tests -q; source review; git diff --check
Dataset / prompt / model / policy versions (where relevant): Synthetic fake clock and local effects; default policy 3 attempts, 1s attempt, 5s total, 0.25s initial / 0.5s capped backoff; no model calls
Observed result / metrics: 114 tests pass, including 18 recovery/replay methods; commit-then-timeout produces two attempts and one effect
What this proves: Bounded retries, shrinking budgets, capped backoff, retry allowlist, authorization rechecks, preserved late success, scoped idempotency and immutable attempt snapshots
Limitations / unverified behavior: Cooperative timeouts cannot interrupt blocking code; effect store is serial and in-memory, without durable or concurrent guarantees; no live provider evidence
Open question / blocker: None blocking; optional callable/return annotations and type-alias naming cleanup remain
Next action: Phase 5 frozen selection dataset and recovery report
```

<a id="phase-5"></a>

### Phase 5 — Tool selection and recovery evaluation

- [x] Store 40 labelled first-tool-selection scenarios and measure ≥90% correctness.
- [x] Assert typed error code, retryability, attempts and trace for all failure categories.
- [x] Record repeated invocation and duplicate side-effect outcomes.
- [x] Save week2-error-recovery.md and draw the tool-calling lifecycle from memory.

Evidence / notes:

```text
Status: Done
Files or links: docs/learning-notes/week2.md; evals/reports/week2-recovery-traces-02.json; evals/datasets/tool_selection.jsonl; evals/reports/week2-selection-predictions-02.jsonl; companion .run.json; week2-selection-results-02.json; week2-error-recovery.md
Command / review procedure: Offline scorer over saved run 02; SHA-256 checks; ../.venv/bin/python -m unittest discover -s tests -q
Dataset / prompt / model / policy versions (where relevant): Dataset v1; tool_selection_v1.txt; requested gpt-6-luna; SDK 3.5.0; timeout 20s, output cap 512
Observed result / metrics: 38/40 first-tool and argument matches (95%); 40 valid turns; 0 skipped; mean 0.968s; 13,047 input and 1,155 output tokens; 165 tests pass
What this proves: First-selection gate met; 17/17 observed failure/replay scenarios; lifecycle diagram and trusted-boundary explanation reviewed
Limitations / unverified behavior: Provider status 8/10; no tool execution in selection collection; reserved $2 is not actual cost; no full live continuation or repeatability claim
Open question / blocker: None for this phase; recovery runner refreshed offline on 2026-10-18 to match current source
Next action: Phase 6 clean-source reproducibility and local handoff
```

<a id="phase-6"></a>

### Phase 6 — Local ship and learning handoff

- [x] Document setup and exact offline/test/eval commands from the project root.
- [ ] Verify the slice from a clean source checkout and record dependency/environment limitations.
- [x] Complete the deliverable inventory and curriculum exit-criteria evidence below.
- [x] Write the engineering note with a deliberate failure, measured tradeoff, limitations and next smallest action.

Evidence / notes:

```text
Status: In progress
Files or links: docs/WEEK-02-LOCAL-GUIDE.md; README.md; evals/reports/week2-local-verification.json
Command / review procedure: Fresh temporary source exports of committed HEAD and nonignored working source; existing Python 3.13 virtualenv; offline unit tests, collector dry-run and recovery runner
Dataset / prompt / model / policy versions (where relevant): No model requests; frozen Week 2 fixtures and default recovery policy; exact source hashes in verification artifact
Observed result / metrics: HEAD: 160 tests and zero-request dry-run pass, but recovery runner/note absent. Working source: 165 tests pass, zero requests, recovery 17/17.
What this proves: Source-independent execution with existing dependencies; setup and exact commands documented; inventory and exit evidence reviewed; measured tradeoff and limitations documented
Limitations / unverified behavior: Fresh pip installation and transitive resolution not verified; complete Week 2 working artifacts are not yet all committed; browser progress separate
Open question / blocker: Commit intended working artifacts before verifying a complete committed handoff
Next action: User-owned scoped packaging commit, then clean committed-source verification
```

## Deliverable inventory

Paths below are relative to the project root; they are target artifacts, not claims that files already exist.

| Curriculum deliverable | Primary phase | Status | Evidence |
| --- | --- | --- | --- |
| `app/tools/` | 2 | Done | Four typed tools and exception-based gateway integration; 78 tests pass |
| `app/llm/tool_loop.py` | 3 | Done | 18 offline lifecycle methods pass in 96-test suite |
| `simulator/fixtures/` | 2 | Done | Synthetic version 1 fixture and scoped collision/failure tests |
| `evals/datasets/tool_selection.jsonl` | 5 | Done | Frozen 40 cases; live run 02 scores 38/40 |
| `app/tools/errors.py` | 1 | Done | Phase 1 error and trace regressions pass in 66-test suite |
| `evals/reports/week2-error-recovery.md` | 5 | Done | Selection metrics, misses, 17 recovery scenarios and reviewed lifecycle note |

## Failure and experiment coverage

Curriculum failure pass: Make tools return unknown IDs, invalid providers, malformed arguments, timeouts, 500s, empty responses, and payment-not-found. Add an explicit maximum tool-step count.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Unknown ID / invalid provider | payment_not_found; invalid_provider | evals.recovery_evidence | Typed and bounded outcomes | Typed nonretryable errors; one read each; traces-02.json | Done |
| Malformed arguments / denied authorization | invalid_arguments; unauthorized | evals.recovery_evidence | Typed and bounded outcomes | Rejected before reader; zero reads; traces-02.json | Done |
| Timeout / 500 / malformed response / empty response | timeout_recovery; server_error_recovery; malformed_response; empty_object | evals.recovery_evidence | Typed and bounded outcomes | Transient recovery; malformed/empty failures do not retry; traces-02.json | Done |
| Stale repeated call versus intentional fresh read | replayed_call_id; fresh_read | evals.recovery_evidence | Typed and bounded outcomes | One read for replay; two authorized reads for fresh call IDs; traces-02.json | Done |
| Fake side effect commits before timeout and retry | FakeEffectReplayTest | unittest discover -s tests -p test_tool_recovery.py -v | Retry same scoped key without duplication | Two attempts; one effect; original receipt | Done |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [x] ≥90% correct first tool selection across 40 scenarios
- [x] Invalid tool arguments are rejected before execution
- [x] Authorization is performed by the application
- [x] A maximum tool-step count exists
- [x] Timeouts cannot create infinite retries
- [x] Draw the full tool-calling lifecycle from memory
- [x] Retryable and non-retryable failures produce typed ToolError results
- [x] Retries have explicit attempt and total-time limits
- [x] Duplicate side effects are prevented with an idempotent operation key
- [x] Tool errors and recovery attempts are observable in the execution trace

| Criterion or metric | Supporting phase / evidence | Result / denominator | Remaining gap |
| --- | --- | --- | --- |
| First selection | selection-results-02.json | 38/40 (95%) | Small synthetic sample; two provider-status misses |
| Validation, authorization and tool limits | Phase 1–3 tests; recovery traces 02 | Rejections before reads; bounded loop | No live multi-turn claim |
| Typed failures, retry limits and traces | recovery traces 02; 165 passing tests | 17/17 scenarios | Cooperative timeouts |
| Idempotency | commit_then_timeout trace | Two attempts; one effect; original receipt | Serial in-memory only |
| Lifecycle explanation | docs/learning-notes/week2.md | Diagram and explanation reviewed 2026-10-18 | Browser state unchanged |

## Session log

Append verified work without rewriting earlier evidence.

| Date | Phase | Timebox | Completed / reviewed | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| 2026-10-07 | Phase 1 | Review | Validation and authorization gate verified; error/trace gaps reproduced | 64 passing original tests; 66 expanded methods with 11 failing subtests | Add safe messages and validated trace IDs |

| 2026-10-09 | Phase 1 | Review | Phase 1 gate verified; Phase 1 Done | All 66 tests pass; safe rejection messages, validated trace IDs and keyword callable protocols | Phase 2 fixture-backed tools and tenant isolation |

| 2026-10-09 | Phase 2 | Review | Phase 2 gate verified; Phase 2 Done | 78 passing tests including 12 Phase 2 methods; reader failure traces corrected | Phase 3 manual lifecycle |

| 2026-10-12 | Phase 3 | Review | Phase 3 gate verified; Phase 3 Done | 96 passing tests including 18 loop methods; no model calls | Phase 4 bounded recovery and replay |

| 2026-10-14 | Phase 4 | Review | Phase 4 gate verified; Phase 4 Done | 114 tests pass; late success preserved; scoped replay deduplication; cooperative timeout limitations documented | Phase 5 selection and recovery evaluation |

| 2026-10-16 | Phase 5 | Run review | Selection gate verified; phase remains In progress | Complete run 02: 38/40 (95%), hashes verified; 160 tests pass | Save recovery traces and learner lifecycle drawing |

| 2026-10-18 | Phase 5 | Review | Phase 5 Done; lifecycle note corrected and reviewed | Selection 38/40; refreshed offline recovery 17/17; 165 tests pass | Phase 6 local reproducibility and handoff |

| 2026-10-18 | Phase 6 | Build / verification | Local guide and engineering handoff prepared; source-copy checks executed | Working source 165 tests and 17/17 recovery; HEAD 160 tests and missing latest artifacts | Commit intended artifacts and reverify committed source |

## Definition of done

- [ ] All six phase checklists and exit gates have reviewed evidence.
- [ ] Every curriculum deliverable is present and its purpose verified.
- [ ] Every curriculum exit criterion above is supported by evidence.
- [ ] Required failure cases and experiments have saved results, including misses and limitations.
- [ ] Setup, commands and environment assumptions are documented and verified from clean source.
- [ ] The engineering note explains the primitive, deliberate failure, measurements and tradeoff.
- [ ] The next smallest action and remaining gaps are recorded.
- [ ] Supported browser checkpoints are identified; no browser completion or production readiness is inferred.
