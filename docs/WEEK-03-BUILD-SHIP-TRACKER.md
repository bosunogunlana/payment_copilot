# Week 3 Build / Ship Tracker — Practical machine-learning foundations

[All weeks](BUILD-SHIP-INDEX.md) · [Week 3 plan](WEEK-03-BUILD-SHIP.md) · [Previous week](WEEK-02-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-04-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 3 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Label and split contract](#phase-1) | Not started | — |
| 2 | [Synthetic dataset and leakage checks](#phase-2) | Not started | — |
| 3 | [Classical baseline](#phase-3) | Not started | — |
| 4 | [Structured LLM classifier](#phase-4) | Not started | — |
| 5 | [Error analysis and recommendation](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Label and split contract

- [ ] Define seven payment-support labels and costly false-positive outcomes.
- [ ] Design varied synthetic template families and stable row IDs.
- [ ] Specify train, validation and test splits grouped by template family.
- [ ] Freeze the split manifest before fitting features or prompts.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-2"></a>

### Phase 2 — Synthetic dataset and leakage checks

- [ ] Generate roughly 1,000 labelled synthetic messages into payment_issues.csv.
- [ ] Validate counts, labels and template-family provenance.
- [ ] Assert related templates never span train and test.
- [ ] Reserve one common held-out subset for both classifiers within the model budget.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-3"></a>

### Phase 3 — Classical baseline

- [ ] Fit TF-IDF on the training split only.
- [ ] Train logistic regression and tune using validation data.
- [ ] Evaluate frozen predictions on held-out test messages.
- [ ] Record inference cost and latency separately from training work.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-4"></a>

### Phase 4 — Structured LLM classifier

- [ ] Request and validate the seven-label structured output.
- [ ] Handle refusals, invalid outputs and unavailable responses explicitly.
- [ ] Freeze prompt and settings before held-out evaluation.
- [ ] Set a spending allowance and use the same held-out subset as the classical baseline.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-5"></a>

### Phase 5 — Error analysis and recommendation

- [ ] Report confusion matrices, accuracy, precision, recall and F1 for both classifiers.
- [ ] Inspect the class where false positives are most costly.
- [ ] Explain training versus inference, overfitting and split roles.
- [ ] Write classifier-comparison.md with a deployment recommendation and a task where a $0 deterministic classifier wins.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

<a id="phase-6"></a>

### Phase 6 — Local ship and learning handoff

- [ ] Document setup and exact offline/test/eval commands from the project root.
- [ ] Verify the slice from a clean source checkout and record dependency/environment limitations.
- [ ] Complete the deliverable inventory and curriculum exit-criteria evidence below.
- [ ] Write the engineering note with a deliberate failure, measured tradeoff, limitations and next smallest action.

Evidence / notes:

```text
Status: Not started
Files or links:
Command / review procedure:
Dataset / prompt / model / policy versions (where relevant):
Observed result / metrics:
What this proves:
Limitations / unverified behavior:
Open question / blocker:
Next action:
```

## Deliverable inventory

Paths below are relative to the project root; they are target artifacts, not claims that files already exist.

| Curriculum deliverable | Primary phase | Status | Evidence |
| --- | --- | --- | --- |
| `experiments/classical_classifier.py` | 3 | Not started | — |
| `experiments/llm_classifier.py` | 4 | Not started | — |
| `data/payment_issues.csv` | 2 | Not started | — |
| `docs/learning-notes/classifier-comparison.md` | 5 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Inspect the confusion matrix. Find the class where a false positive is most costly, then decide whether accuracy or recall should lead your deployment recommendation.

Use the plan’s phase checks to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Template-family train/test leakage | — | — | Define from phase acceptance checks | — | Not started |
| Invalid or refused LLM classification | — | — | Define from phase acceptance checks | — | Not started |
| Costly false positive by class | — | — | Define from phase acceptance checks | — | Not started |
| Overfitting versus held-out performance | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] Explain training vs inference
- [ ] Explain train, validation, and test data
- [ ] Explain overfitting
- [ ] Explain precision vs recall and when F1 helps
- [ ] Name a task where a $0 deterministic classifier wins
- [ ] Write a deployment recommendation

| Criterion or metric | Supporting phase / evidence | Result / denominator | Remaining gap |
| --- | --- | --- | --- |
| Add a row for each verified criterion | — | — | — |

## Session log

Append verified work without rewriting earlier evidence.

| Date | Phase | Timebox | Completed / reviewed | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | — |

## Definition of done

- [ ] All six phase checklists and exit gates have reviewed evidence.
- [ ] Every curriculum deliverable is present and its purpose verified.
- [ ] Every curriculum exit criterion above is supported by evidence.
- [ ] Required failure cases and experiments have saved results, including misses and limitations.
- [ ] Setup, commands and environment assumptions are documented and verified from clean source.
- [ ] The engineering note explains the primitive, deliberate failure, measurements and tradeoff.
- [ ] The next smallest action and remaining gaps are recorded.
- [ ] Supported browser checkpoints are identified; no browser completion or production readiness is inferred.
