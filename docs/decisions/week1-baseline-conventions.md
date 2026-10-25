# Week 1 deterministic baseline conventions

Verified on 2026-10-01 against `app/models/diagnosis.py` and 17 passing unittest cases.

## Confidence

Confidence describes how strongly the available synthetic evidence supports the returned diagnosis. It does not measure certainty that escalation is appropriate.

These scores are hand-assigned baseline heuristics, not calibrated probabilities or evidence of real-provider reliability. A score of 0.8 does not mean 80 percent accuracy, and 1.0 does not establish real-world certainty. Later evaluations must measure correctness separately.

| Outcome | Current score | Convention |
| --- | --- | --- |
| Recorded success | 1.0 | Recognized outcome, above 0.5 |
| Pending with a timeout event | 1.0 | Recognized outcome, above 0.5 |
| Failed with structured AUTH_DECLINED on a decline event | 0.8 | Recognized cause, above 0.5 |
| Ledger posting conflicts with a provider decline | 0.4 | Uncertain outcome, below 0.5 |
| Missing events, unknown state, unsupported pending/failed cause, defensive fallback | 0.2 | Uncertain outcome, below 0.5 |

The current baseline does not use exactly 0.5. The difference between uncertain scores 0.2 and 0.4 is an implementation convention without measured significance. Tests enforce the recognized-versus-uncertain boundary without requiring exact score constants.

## Evidence and explanations

- Missing evidence and the supported conflict pair are checked before ordinary state mappings.
- Success uses the recorded payment state. Its explanation mentions ledger posting only when a `ledger.posted` event exists.
- Pending state alone does not prove a timeout. A `provider.timeout` event is required.
- Failed state alone does not prove an authorization failure. The same event must have type `provider.declined` and structured `reason_code` equal to `AUTH_DECLINED`.
- Event messages are untrusted descriptive text. A code mentioned in prose, or attached to another event type, cannot establish an authorization cause.
- Unsupported, missing, and conflicting causes produce unknown status/category, `likely_cause=None`, and human escalation. Returning unknown diagnosis status does not mutate the input payment's recorded status.
- Explanations are controlled application text derived from the recognized evidence; they are not copied from arbitrary event messages.

## Verification and limits

From the project root, run:

```bash
../.venv/bin/python -m unittest discover -s tests -v
```

The persistent fixture test loads the five labelled JSONL scenarios, checks expected labels, serializes each result to JSON, and validates it back through `Diagnosis`.

This baseline implements the bounded Week 1 simulator cases. It does not resolve all possible conflicts, event ordering, freshness, or multiple-attempt histories. It does not perform payment actions or establish production readiness.
