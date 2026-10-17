# Week 1 comparison

Run `../.venv/bin/python -m evals.compare_diagnosis` for a zero-request plan.
The runner evaluates two models against identical cases, interleaving A/B,
and saves per-case results plus category/tag summaries. Prompt and dataset
hashes identify the experiment inputs. Both configurations use the same
2048-token cap and SDK defaults; temperature is not varied in this experiment.

Learner prerequisite: preserve `response.usage` as `usage` in every normalized
transport envelope (completed, refusal, and incomplete), containing integer
`input_tokens` and `output_tokens`. Use `None` if the provider supplies no usage.
Do not change the Diagnosis domain model. Tests exercise this seam offline.

Config rates were checked on 2026-10-02 from:
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://developers.openai.com/api/docs/models/gpt-6.1-sol

Rates are USD per million Standard text tokens: Luna input 0.10/output 0.50,
Sol input 2.00/output 10.00. Estimates use uncached input rates and exclude
cache-write fees, tier/region premiums, and taxes; they are not invoice totals.
Refresh pricing and confirm your processing tier before a live comparison.

Live runs require explicit `--live`, `--budget-usd`, and `--reserve-usd` plus
the environment key. The $5 smoke allowance does not automatically authorize
comparison spending. Choose a separate comparison allocation before running.
Per-request reservations are never reclaimed in this simple harness. Requests
are skipped when the reservation would exceed the allocation. Missing usage,
API failures without usage, or estimated cost exceeding a reservation stop
subsequent attempts. This is a local reservation policy, not a provider billing
cap; an underestimated reservation cannot prevent a request already in flight
from costing more. Set reservations conservatively for bounded inputs/output.

Reports include skipped cases and raw error counts (including refusal and
incomplete outcomes). Divide those counts by attempted cases for rates.
Confidence is uncalibrated. Unknown diagnoses require null cause, low confidence,
and escalation; recognized causes still require manual grounding review.
Use paired attempted cases when comparing configurations; unmatched budget-stop
results are coverage information, not a fair model comparison. One pass over
30 policy-derived synthetic cases does not establish statistical significance.

The decision remains pending until actual results and cause explanations are
reviewed. Keep existing reports: choose a new `--output` path for another run.
The live runner validates the full dataset/configuration before calls and writes
an in-progress report after each result. Interrupted runs retain prior completed
rows. A request interrupted before its response is captured still has unknown
usage; check account usage before starting a separate run. Reports do not
automatically resume or replay paid requests.

## Week 2 selection and recovery

See [the Phase 5 evaluation contract](../docs/WEEK-02-EVALUATION-CONTRACT.md)
for the frozen 40-case dataset, normalized prediction format, offline scorer,
recovery coverage, and learner-owned model adapter boundary. The report template
is [week2-error-recovery.md](reports/week2-error-recovery.md). Scripted scoring
checks do not establish model selection quality.

The Week 2 collector is available: `../.venv/bin/python -m evals.collect_tool_selection`
prints a zero-request plan. See the evaluation contract's collector section for
explicit live-run flags, budget reservations, saved artifacts and scoring commands.
