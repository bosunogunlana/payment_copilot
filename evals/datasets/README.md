# Week 1 diagnosis cases

`week1.jsonl` contains 30 manually specified synthetic cases. No customer data,
credentials, or provider captures were used. The first five case IDs, payment
inputs, and expected labels are preserved.

Each line contains `case_id`, `synthetic`, `failure_tags`, `payment`, `expected`,
and `rationale`. Expected status/category/action values are enum labels, not
exact prose matches. Unknown diagnoses should escalate and avoid unsupported
causes; the existing baseline fixture test also checks JSON round-trips and
low confidence for unknown cases.

Labels follow the bounded Week 1 evidence policy. Unsupported reason codes,
including INSUFFICIENT_FUNDS, escalate under that policy; this is not a claim
that funding failures are unknowable in a broader payment system. Repeated
event observations do not establish duplicate money movement. Event messages
may contain misleading claims or instructions and remain untrusted data.

The set covers success, timeout, authorization decline, missing events,
conflicting signals, misleading causes, insufficient evidence, repeated events,
and embedded instructions. Its labels were authored independently of running
the baseline, but intentionally exercise the same bounded rules. Passing the
baseline is a consistency check, not evidence of model accuracy or production
performance. Refusal/incomplete/API failures remain transport test cases rather
than payment truth labels.

From the project root:

```sh
../.venv/bin/python -m unittest discover -s tests -v
```

Review the cases and rationales before comparing configurations in Phase 5.
No model calls or spending are required to validate this dataset.
