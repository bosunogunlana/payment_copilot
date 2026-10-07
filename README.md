# Payment Reliability Copilot

A simulator-first AI engineering project for investigating payment failures.
The project develops typed diagnosis, evidence retrieval, tool execution,
evaluation, and reliability controls through a 16-week curriculum. Features are
introduced incrementally; weekly documents describe their implementation status
and supporting evidence.

Payment data and actions remain synthetic or simulated. Paqet integration is a
future adapter boundary.

## Local setup

Run commands from the project root (`payment_copilot/`). The current environment
has been verified with Python 3.13:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

`requirements.txt` pins direct dependencies; transitive dependencies are not
locked. Keep API credentials in your shell environment, outside source control.
Live model calls require an explicit spending allowance; see the relevant weekly
guide before running them.

## Project layout

- `app/` — core application models and adapters.
- `tests/` — contract, behavior, and failure checks.
- `evals/` — synthetic datasets, evaluation runners, and reports.
- `docs/` — weekly guides, build plans, evidence trackers, and learning notes.
- `docs/payment-reliability-copilot/` — curriculum and browser progress tracker.

## Guides and progress

Start with the [curriculum](docs/payment-reliability-copilot/CURRICULUM.md) for the
learning sequence and the [course tracker instructions](docs/payment-reliability-copilot/README.md)
for browser-based progress. Weekly build trackers record implementation evidence
separately from curriculum completion. Open the [build/ship learning map](docs/BUILD-SHIP-INDEX.md)
for phased plans and evidence trackers for all 16 weeks.

| Week | Guide | Build plan | Evidence tracker |
| --- | --- | --- | --- |
| 01 — Models, prompting, and structured output | [Local diagnosis and evaluation](docs/WEEK-01-LOCAL-GUIDE.md) | [Plan](docs/WEEK-01-BUILD-SHIP.md) | [Tracker](docs/WEEK-01-BUILD-SHIP-TRACKER.md) |

Week-specific commands, model settings, results, and learning notes belong in
the corresponding guide. The [learning assistant instructions](docs/LEARNING-ASSISTANT-PROMPT.md)
define the learner-owned implementation and review workflow.
