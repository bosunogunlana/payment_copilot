# Week 1 comparison review

Reviewed locally on 2026-10-05. Source: `week1-comparison-01.json`.
No API requests were made during review. Dataset hash matches the current file.

| Metric | A-luna | B-sol |
| --- | --- | --- |
| Attempted / skipped | 30 / 0 | 30 / 0 |
| Schema-valid | 30 / 30 | 30 / 30 |
| Expected-label match | 27 / 30 | 28 / 30 |
| Unsafe expected-unknown outcomes | 2 | 2 |
| Mean adapter latency | 1.798 s | 4.829 s |
| Estimated uncached text cost | $0.003422 | $0.058462 |
| Input / output tokens | 21871 / 2469 | 21871 / 1472 |
| Refusal / incomplete / API failure | 0 / 0 / 0 | 0 / 0 / 0 |

The run records a $3 allocation and $0.05 per-request reservations. Reserved
capacity is not actual spend; cost estimates exclude the documented billing
adjustments. No usage is missing and no cases were skipped.

## Findings

- case-003: Luna preserved payment status pending while returning unknown,
  null cause, low confidence, and human escalation. This is an exact-label
  mismatch but the uncertainty behavior is safe under the evaluator's check.
- case-012: Both models diagnosed success despite an empty event history.
  The baseline/dataset requires escalation. The prompt's success rule allows
  success without conflicting evidence and does not explicitly make missing
  events override recorded success. Clarify rule precedence before attributing
  this disagreement entirely to model capability.
- case-022: Both models interpreted INSUFFICIENT_FUNDS on the decline event.
  Their causes are grounded in the supplied reason code. The bounded dataset
  expects unknown because this code is outside the prototype's implemented
  policy, but the prompt does not declare an exhaustive supported-code list
  and the output enum permits insufficient_funds. This is a policy alignment
  defect, not evidence that the models invented a funding cause.

The other recognized explanations reviewed here refer to recorded status,
ledger posting, timeout, or same-event AUTH_DECLINED without inventing customer
actions. Expected-unknown cases that passed uncertainty checks have null cause
and low confidence. This is a manual review of one run, not calibrated quality.

## Decision

Retain Luna as the provisional economical option for the next experiment:
Sol costs about 17 times more and has about 2.7 times the mean latency for one
additional exact-label match. Neither meets all current acceptance rules.
Align the prompt with the documented missing-event and supported-code policy,
keep this report unchanged, and evaluate a new version under an explicitly
allocated budget. One run over 30 policy-derived synthetic cases cannot establish
a stable model ranking or production readiness.
