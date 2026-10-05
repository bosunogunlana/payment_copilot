# Week 1 comparison 02 review

Reviewed on 2026-10-05 from the existing live report. No paid requests were made
during review. Prompt hashes and dataset hash match the current source files.

| Metric | A-luna | B-sol |
| --- | --- | --- |
| Attempted / skipped | 30 / 0 | 30 / 0 |
| Schema-valid | 30 / 30 | 30 / 30 |
| Expected-label match | 30 / 30 | 30 / 30 |
| Unsafe expected-unknown outcomes | 0 | 0 |
| Mean adapter latency | 1.846 s | 2.271 s |
| Estimated uncached text cost | $0.003606 | $0.063132 |
| Refusal / incomplete / API failures | 0 / 0 / 0 | 0 / 0 / 0 |

Both configurations have complete input/output token records. The run declares
a $3 reservation allocation and $0.05 per request. Reservations are planned
capacity, not actual spend; estimated costs retain the documented exclusions.

Manual review: all recognized causes describe recorded success, ledger posting,
provider timeout, or same-event AUTH_DECLINED evidence. No fabricated customer
action or unsupported ledger claim was found. Expected-unknown outcomes have
null causes, low confidence, and human escalation. Repeated events and embedded
instructions did not produce unsafe outcomes in this run.

Report 01 remains preserved. Report 02 uses a revised prompt with explicit
missing-event precedence and exhaustive supported-code scope. Earlier mismatches
are resolved, but one run per version cannot isolate stochastic variation from
the effect of instruction changes or establish calibrated confidence.

Decision: keep Luna for this bounded Week 1 slice. Both models satisfy the
current acceptance cases; Sol costs about 17.5 times as much and has about
23% greater mean latency in this run without an observed quality gain.
This conclusion is limited to 30 synthetic, policy-derived cases and one pass
per model. It does not establish production performance or eliminate tail risks.

All 49 offline tests pass. Phase 5's comparison and decision gate is supported.
Next is Phase 6: reproducible local packaging and the learning note.
