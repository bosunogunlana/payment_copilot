# Week 4 Build / Ship Tracker — Evaluation-driven development

[All weeks](BUILD-SHIP-INDEX.md) · [Week 4 plan](WEEK-04-BUILD-SHIP.md) · [Previous week](WEEK-03-BUILD-SHIP-TRACKER.md) · [Next week](WEEK-05-BUILD-SHIP-TRACKER.md)

Check boxes only when reviewed artifacts, tests, traces, metrics or notes support them. New phases start unchecked; this is a planning baseline, not a claim about browser progress or existing code. The browser tracker remains the authority for curriculum completion.

## Current status

- Overall status: Not started
- Current phase: Phase 1
- Last evidence update: —
- Main blocker: Not assessed
- Next action: Read the Week 4 prerequisites and plan; define one coherent Phase 1 batch.

Status values: `Not started` · `In progress` · `Blocked` · `Done`

## Phase overview

| Phase | Focus | Status | Evidence |
| --- | --- | --- | --- |
| 1 | [Golden dataset and score contract](#phase-1) | Not started | — |
| 2 | [Immutable prompt registry](#phase-2) | Not started | — |
| 3 | [Reusable evaluation runner](#phase-3) | Not started | — |
| 4 | [Before/after and variance](#phase-4) | Not started | — |
| 5 | [Promotion and rollback rehearsal](#phase-5) | Not started | — |
| 6 | [Local ship and learning handoff](#phase-6) | Not started | — |

## Phase checklist

<a id="phase-1"></a>

### Phase 1 — Golden dataset and score contract

- [ ] Curate at least 75 unique cases from previous weeks.
- [ ] Version inputs and define an error taxonomy.
- [ ] Specify accuracy, schema compliance, tool correctness and unsupported-claim graders.
- [ ] Define latency, usage and estimated-cost counting including failed attempts.

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

### Phase 2 — Immutable prompt registry

- [ ] Create file-based prompt versions with name, version, created_at, model, template, status, eval_dataset, eval_score and notes.
- [ ] Keep published templates immutable; put changing release status and evidence in a manifest.
- [ ] Pin runtime registry versions.
- [ ] Prepare payment_diagnosis versions and incident_investigator/v1.yaml without building the future investigator.

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

### Phase 3 — Reusable evaluation runner

- [ ] Extend the existing runner rather than creating a second eval system.
- [ ] Record prompt_version, model, dataset_version and timestamp on every run.
- [ ] Report category scores, accuracy, unsupported_claim_rate, tool_correctness, cost and latency.
- [ ] Exercise invalid output and evaluator failures with deterministic fixtures.

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

### Phase 4 — Before/after and variance

- [ ] Freeze dataset and settings and compare two prompt versions.
- [ ] Run repeated model trials within a declared spending allowance.
- [ ] Retain a regression even when aggregate accuracy improves.
- [ ] Classify failures and distinguish reproducible inputs from stochastic outputs.

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

### Phase 5 — Promotion and rollback rehearsal

- [ ] Restore the prior version and rerun the golden set.
- [ ] Verify template identity rather than only a version label.
- [ ] Save before/after results and promotion or rejection rationale.
- [ ] Record known stochastic variation and the cost/latency tradeoff in prompt-regression.md.

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
| `evals/runner.py` | 3 | Not started | — |
| `evals/datasets/golden_set.jsonl` | 1 | Not started | — |
| `evals/reports/week4.md` | 5 | Not started | — |
| `evals/error_taxonomy.yml` | 1 | Not started | — |
| `prompts/payment_diagnosis/` | 2 | Not started | — |
| `prompts/incident_investigator/v1.yaml` | 2 | Not started | — |
| `evals/reports/prompt-regression.md` | 5 | Not started | — |

## Failure and experiment coverage

Curriculum failure pass: Run at least one prompt change you expect to help that makes an eval worse. Keep the before/after report and classify why.

Use the plan’s phase checks and expanded curriculum contract to enumerate individual cases. Add one row per failure/experiment; separate represented inputs from executed and reviewed results.

| Case / experiment | Dataset or fixture ID | Test / eval command | Expected outcome | Observed outcome / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Plausible prompt improvement regresses a metric | — | — | Define from phase acceptance checks | — | Not started |
| Repeated runs produce quality variation | — | — | Define from phase acceptance checks | — | Not started |
| Exact prior-template rollback | — | — | Define from phase acceptance checks | — | Not started |
| Malformed output / broken evaluator | — | — | Define from phase acceptance checks | — | Not started |

## Curriculum exit criteria evidence

These retain the curriculum’s exact exit checks. Link each checked item to phase evidence; thresholds require actual measurements with denominators, not intended targets.

- [ ] Golden set contains at least 75 cases
- [ ] Eval execution is reproducible
- [ ] Scores are broken down by category
- [ ] Model and prompt metadata are stored
- [ ] A before/after comparison exists
- [ ] You can distinguish a better score from a lucky sample
- [ ] Every eval run identifies prompt, model and dataset versions
- [ ] A previous prompt version can be restored exactly
- [ ] Accuracy, unsupported claims, tool correctness, cost and latency regressions are visible
- [ ] Prompt changes have recorded release and rollback decisions

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
