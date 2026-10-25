# Week 1 — Local diagnosis guide

Week 1 is a local, synthetic payment-diagnosis learning artifact. It includes a
deterministic reference, an independent LLM adapter, and a labelled evaluation
dataset. It does not execute payment actions or establish production readiness.

Run these commands from the project root (`payment_copilot/`). Python 3.13 was used for the recorded
results. Create a project-local environment; the original development environment
in the parent directory is not required:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

`requirements.txt` pins the two direct dependencies to the report versions. It
does not lock transitive dependencies. Dependency installation requires access to
a package index containing these versions.

Diagnose a fixture offline and save the validated `Diagnosis` JSON:

```sh
.venv/bin/python -m evals.diagnose_fixture --case-id case-001 --output diagnosis.json
```

The output file must be new; an existing file is never overwritten. Use
`--case-id case-003` to inspect safe uncertainty, or omit `--output` for stdout
only. This command runs the deterministic baseline, independently of the LLM.

Check the dataset and inspect the API execution plans without spending:

```sh
.venv/bin/python -m unittest discover -s tests -p test_week1_dataset.py -v
.venv/bin/python -m evals.smoke_diagnosis
.venv/bin/python -m evals.compare_diagnosis
```

For a deliberately paid LLM diagnosis, configure `OPENAI_API_KEY` in the shell,
review pricing and your remaining allowance, then use:

```sh
.venv/bin/python -m evals.smoke_diagnosis --live --max-output-tokens 512 --acknowledge-spend
```

The model argument is optional. Selection follows `--model`, `OPENAI_MODEL`, then
the transport default. Output limits and acknowledgement are not a hard dollar
cap. Do not place keys in source files. The smoke command prints a typed
`DiagnosisResult`, containing exactly one diagnosis or error.

See [evaluation instructions](../evals/README.md), the
[dataset policy](../evals/datasets/README.md), the
[Week 1 results](../evals/reports/week1-summary.md), and the
[learning-note draft](./learning-notes/week1.md).
