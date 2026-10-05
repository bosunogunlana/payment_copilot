# Week 1 report summary

Comparison 02 evaluated Luna and Sol on the same 30 labelled synthetic payment
cases using the revised diagnosis prompt. Figures below are rounded from the
[saved comparison](week1-comparison-02.json); see the
[review](week1-comparison-02-review.md) for evidence and limitations.

| Metric | Luna | Sol |
| --- | --- | --- |
| Label matches | 30/30 | 30/30 |
| Schema-valid | 30/30 | 30/30 |
| Unsafe unknown outcomes | 0 | 0 |
| Mean latency | 1.85 s | 2.27 s |
| Estimated cost | $0.00361 | $0.06313 |

Cost is the estimated total for each model's 30 requests, not per request or
an invoice total. Latency is the mean adapter duration. No cases were skipped.

Decision: keep Luna for this bounded slice. Both models met the evaluated
acceptance rules; Sol cost about 17.5 times more without an observed quality
gain. This is one run per model on synthetic cases, not proof of production
reliability or calibrated confidence.
