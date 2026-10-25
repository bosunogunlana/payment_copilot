# Week 1 Build / Ship Plan

## Scope

Build and locally ship Payment Diagnosis Service v0. The service accepts a payment and its event history, then returns a typed diagnosis containing:

- status
- category
- likely cause
- recommended action
- confidence

This plan expands the Week 1 implementation assignment into small phases. It preserves the curriculum boundary: use synthetic payment data, keep the simulator as the source of truth, and do not build tools, agents, retrieval, production deployment, or live payment actions yet.

Use [WEEK-01-BUILD-SHIP-TRACKER.md](WEEK-01-BUILD-SHIP-TRACKER.md) as the working checklist.

## Week 1 ship target

At the end of the week, I should be able to run one local command that diagnoses a payment fixture, validates the result against the application model, and records enough evidence to compare two model configurations.

The shipped slice is local and reproducible. “Ship” means another person can clone the project, install the dependencies, run the tests and evaluation command, inspect the saved scenarios, and understand the known failure modes. It does not mean production deployment or real-money integration.

## Working rules

- Keep core implementation work learner-owned under `app/`.
- Keep tests, fixtures, evaluation data, and review scaffolding separate from the core implementation.
- Treat model output as untrusted input, even when structured output validation succeeds.
- Use only synthetic payments and event histories.
- Keep API keys outside the repository and set a spending limit before model comparisons.
- Reuse the existing `Payment`, `PaymentEvent`, and `Diagnosis` boundary rather than creating a second domain model.
- Do not add a framework until a measured failure gives it a job.

---

## Phase 1: Establish the diagnosis contract

### Goal

Make the input and output boundaries explicit and executable before connecting a model.

### Expected outcome

I should have:

- A typed `Payment` input with a payment status and event history.
- A typed `Diagnosis` output with bounded enum values and a confidence value from `0` to `1`.
- Validation for invalid amounts, currencies, missing identifiers, and invalid confidence values.
- A small set of representative synthetic payment fixtures.
- A passing test command from the project root.

### Primary files

- `app/models/diagnosis.py`
- `tests/`
- `evals/datasets/week1.jsonl` — start with the first five cases only

### Walkthrough needed

Help me decide:

- Which fields belong in the domain model versus the prompt payload.
- Which values should be enums and which should remain explanatory text.
- How to represent missing, stale, and conflicting events.
- Why confidence is an application field that still needs calibration, not proof of correctness.

### Completion checklist

- [ ] A valid payment with events can be parsed.
- [ ] An invalid payment is rejected at the model boundary.
- [ ] A diagnosis with invalid enum values or confidence is rejected.
- [ ] At least five labelled synthetic cases exist.
- [ ] The test command passes from a clean run.

### Do not do yet

Do not add an LLM client, prompt comparison, retries, tools, or an HTTP service in this phase.

---

## Phase 2: Build a deterministic baseline

### Goal

Create a small baseline that makes the domain behavior understandable before model behavior is introduced.

### Expected outcome

I should be able to pass a typed payment to a deterministic diagnosis path and receive a typed result for the obvious cases:

- successful payment
- pending provider timeout
- failed or declined payment
- missing event history
- conflicting evidence

The baseline should fail closed when the evidence is insufficient or contradictory.

### Primary files

- `app/models/diagnosis.py`
- `tests/`
- `evals/datasets/week1.jsonl`

### Walkthrough needed

Help me reason about:

- The difference between payment status and diagnosis category.
- Why a conflicting ledger/provider history should not be forced into a confident answer.
- Which facts are deterministic and should not be delegated to an LLM.
- How to keep the baseline useful for later comparison without treating it as production logic.

### Completion checklist

- [ ] The five starter cases have expected outputs.
- [ ] Missing evidence produces an explicit unknown or escalation outcome.
- [ ] Conflicting events fail closed.
- [ ] Tests cover both successful and unsafe-to-decide paths.
- [ ] The baseline output serializes through the same `Diagnosis` schema used later.

### Exit gate

Do not connect the model until the baseline tests explain what a correct, incomplete, and conflicting diagnosis looks like.

---

## Phase 3: Add the LLM diagnosis adapter

### Goal

Connect the model behind a narrow adapter that accepts the existing domain input and returns validated structured output.

### Expected outcome

I should have one callable diagnosis path that:

- Accepts a payment and its event history.
- Uses an explicit system instruction and a bounded input payload.
- Requests the `Diagnosis` shape rather than free-form prose.
- Validates the response with the application model.
- Handles refusal, incomplete output, malformed output, and API errors explicitly.
- Does not silently convert an uncertain or unavailable response into a confident diagnosis.

### Primary files

- `app/llm/diagnose.py`
- `app/models/diagnosis.py`
- `tests/`

### Walkthrough needed

Help me understand:

- What belongs in the system instruction, user payload, and output schema.
- How structured output differs from factual correctness.
- How to distinguish a provider/API failure from a valid low-confidence diagnosis.
- How to keep secrets and spending controls out of source control.
- Which model settings are part of the experiment record.

### Completion checklist

- [ ] The adapter has one clear input/output boundary.
- [ ] Successful responses validate against `Diagnosis`.
- [ ] Refusals and incomplete responses have an explicit application outcome.
- [ ] Malformed structured output is observable and does not become a false success.
- [ ] The adapter can be exercised with a stubbed response without making a live API call.
- [ ] One live or sandboxed smoke run is possible only when credentials and budget controls are intentionally configured.

### Do not do yet

Do not build a general agent loop, tool calling, retrieval, provider integration, or automatic retries beyond what is needed to make one bounded diagnosis request safe to evaluate.

---

## Phase 4: Expand the dataset and break the diagnosis

### Goal

Turn the happy-path demo into a small labelled evaluation set that exposes where the diagnosis fails.

### Expected outcome

I should have at least 30 labelled scenarios in `evals/datasets/week1.jsonl`, including:

- successful payments
- pending payments
- provider timeouts
- declines and authorization failures
- missing event history
- conflicting ledger and provider signals
- duplicate or repeated-looking events
- plausible but wrong causes
- insufficient evidence that should trigger human escalation

Each case should have enough metadata to evaluate the result without relying on prose inspection alone. At minimum, record an input, expected label or acceptable labels, and a short rationale.

### Walkthrough needed

Help me design:

- A stable JSONL case shape.
- Labels that test behavior without overfitting to one wording.
- Cases where the correct result is uncertainty or escalation.
- A separation between synthetic-data coverage and evidence of real-world performance.

### Completion checklist

- [ ] The dataset contains at least 30 cases.
- [ ] Every case has a stable case ID.
- [ ] Missing, conflicting, and plausible-but-wrong cases are represented.
- [ ] Expected outcomes are machine-checkable where possible.
- [ ] No real customer, account, credential, or payment data is included.
- [ ] The dataset can be loaded from a clean checkout.

### Exit gate

Do not compare models until the dataset can show both correct answers and safe refusals. A larger happy-path dataset is not a substitute for failure coverage.

---

## Phase 5: Compare configurations and measure the trade-offs

### Goal

Compare two model configurations using the same cases and record evidence instead of relying on intuition.

### Expected outcome

I should have a repeatable comparison that records, per configuration and preferably per case:

- schema validity
- label or diagnosis correctness
- confidence
- latency
- input and output tokens when available
- estimated cost
- refusal or incomplete-response rate
- notable failure category

Use the same dataset and acceptance rules for both configurations. Keep the comparison small enough to fit the Week 1 budget.

### Walkthrough needed

Help me explain:

- Temperature and sampling conceptually.
- Context-window constraints and payload growth.
- Why a valid schema does not guarantee a correct cause.
- Why cost and latency need to be measured rather than guessed.
- Which result would justify keeping the simpler or cheaper configuration.

### Completion checklist

- [ ] Two configurations are named and recorded.
- [ ] Both configurations run against the same labelled cases.
- [ ] Validity, confidence, latency, tokens, and cost are recorded.
- [ ] Failures are grouped by category rather than only counted.
- [ ] A third model is not added until the two-configuration comparison works.
- [ ] The spending limit and any skipped cases are documented.

### Exit gate

The comparison is complete only when it supports a decision such as “keep configuration A for this slice because…” or “neither configuration is reliable for this failure class because…”.

---

## Phase 6: Package and ship the local learning artifact

### Goal

Make the Week 1 slice reproducible, reviewable, and explainable.

### Expected outcome

I should have:

- A working diagnosis command or documented runner.
- A passing test command.
- A versioned 30-case dataset.
- A comparison result for two configurations.
- A learning note that records the primitive, deliberate failure, evidence, and trade-off.
- A clear list of limitations and the next smallest extension.

### Primary files

- `app/llm/diagnose.py`
- `app/models/diagnosis.py`
- `evals/datasets/week1.jsonl`
- `docs/learning-notes/week1.md`
- `WEEK-01-BUILD-SHIP-TRACKER.md`

### Learning note outline

The note should answer:

1. What primitive did I build manually?
2. What does the input and output contract guarantee?
3. What deliberate failure did I add?
4. What did the measurements show?
5. Where did the model produce a valid-looking but wrong result?
6. What would I change next, and why is that outside Week 1 scope?

### Final ship checklist

- [ ] A clean checkout can run the tests.
- [ ] A clean checkout can load the dataset.
- [ ] A single documented command runs the diagnosis path.
- [ ] Successful responses satisfy the schema.
- [ ] Refusals and incomplete responses are handled explicitly.
- [ ] At least 30 labelled scenarios are stored.
- [ ] Temperature and sampling can be explained conceptually.
- [ ] Context-window constraints can be explained.
- [ ] Structured output limitations can be explained.
- [ ] Cost and latency are measured.
- [ ] `docs/learning-notes/week1.md` contains the evidence and trade-off.

### Out of scope for the Week 1 ship

- Production deployment.
- Real payment or customer data.
- Live money movement, refunds, or provider credentials.
- Function calling and tool execution.
- Retrieval or RAG.
- Multi-step agents.
- Paqet integration.
- Framework adoption driven only by preference.

