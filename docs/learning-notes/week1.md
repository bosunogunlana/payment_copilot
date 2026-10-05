# Week 1 learning note

## Primitive and boundary

### Implemented

- `app.models.diagnosis.Diagnosis` -> `Diagnosis.diagnose`  - A deterministic baseline and independent reference for supported behaviour. No LLM call.
- `app.llm.diagnose.DiagnosisAdapter` - An LLM based diagnosis adaptor with a bounded input, strict structured output and application validation and LLM response handling
  - The manually built primitive is a bounded diagnosis adapter: typed payment input → explicit instruction and strict output schema → one transport request → application validation → exactly one diagnosis or error.
- Eval Dataset for testing LLM behaviour across different models

## Evaluation 

Ran 2 rounds of review with the evaluation dataset and observed the first round produced a wrong result because of unbounded system prompt which allows the LLM
to assume a result outside of scope. Adjusted the prompt and that gave an accurate resume: The most useful failure was schema-valid but incorrect output. Initially, both models diagnosed success without event evidence and interpreted an unsupported decline code. I tightened the instruction to make missing events override recorded status and supported patterns exhaustive.

The contract guarantees accepted field types, enum values, confidence bounds, and explicit refusal/incomplete/malformed/API-failure outcomes. It does not
guarantee factual correctness or calibrated confidence. A schema-valid cause still needs evidence. Missing or conflicting evidence should yield unknown,
null cause, confidence below 0.5, and human escalation.

### Deliberate failure and correction

Report 01 exposed valid-looking policy violations: both models accepted a recorded success despite empty event history in case-012 and interpreted an
unsupported insufficient-funds code in case-022. Luna also retained pending status for case-003 where the expected diagnosis status was unknown.

I revised the instruction to make empty event history an explicit override and the recognized evidence patterns exhaustive. Report 02 then matched every
expected label. This shows the value of explicit policy and negative examples; it does not prove general reliability beyond these cases.

### Measurements

Both configurations used the same 30 synthetic cases. The revised run recorded:

| Metric | Luna | Sol |
| --- | --- | --- |
| Label matches | 30/30 | 30/30 |
| Schema-valid | 30/30 | 30/30 |
| Unsafe unknown outcomes | 0 | 0 |
| Mean latency | 1.85 s | 2.27 s |
| Estimated cost | $0.00361 | $0.06313 |

Costs cover all 30 requests per configuration, not one request. The raw report preserves per-case confidence, tokens, latency, errors, and estimated cost.

### Decision

Keep Luna for this evaluated Week 1 slice: observed quality was equal while its estimated cost was about 17.5 times lower. Single-run latency and quality are not stable
population estimates. Prices are the experiment's recorded estimates, not a current pricing quotation.

Evidence: [original run review](../../evals/reports/week1-comparison-01-review.md), [revised run review](../../evals/reports/week1-comparison-02-review.md), and [raw revised report](../../evals/reports/week1-comparison-02.json).

## AI concepts

- Model produces a bag of choices - tokens
- Sampling selects the next token from the model's probability distribution.
- Temperature changes that distribution before selection: lower values favor already likely tokens; higher values spread probability more broadly.
- The context window bounds tokens across instructions, input, schema, and output.
- The adapter's event and UTF-8 byte limits bound payload growth but are not exact token budgets. Oversized input is rejected rather than silently removing
  evidence. Structured output constrains shape; evidence policy and evaluation are still needed to constrain meaning.

## Limitations and next action

All payments are synthetic. There is no provider integration, real-money action, production authorization proof, confidence calibration, or repeated-run
variance study.
Manual cause review complements label checks because a correct label can still carry an unsupported explanation.

The next extension belongs to Week 2: bounded read-only tool access to synthetic payment evidence, with typed errors and observable failure behavior. Keep tools
and agent orchestration outside this Week 1 slice.