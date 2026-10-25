"""Collect first tool-selection turns; dry-run by default, no tool execution."""

import argparse
import hashlib
import json
import math
import os
import sys
from collections.abc import Callable
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal
from importlib.metadata import version
from pathlib import Path

from app.clients.base import Models, create_openai_client
from app.clients.openai_tool_client import OpenAIToolClient
from app.llm.tool_model import ToolModel
from app.tools.contracts import TOOL_ARGUMENT_MODELS
from evals.score_tool_selection import DEFAULT_DATASET, read_jsonl

ROOT = Path(__file__).resolve().parent
DEFAULT_PROMPT = ROOT / "prompts/tool_selection_v1.txt"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tools_for_model() -> list[dict[str, object]]:
    return [
        {"name": name, "parameters": model.model_json_schema()}
        for name, model in TOOL_ARGUMENT_MODELS.items()
    ]


def validate_cases(cases: list[dict]) -> None:
    if len(cases) != 40:
        raise ValueError("Phase 5 requires exactly 40 frozen cases")
    ids = [case.get("case_id") for case in cases]
    if any(not isinstance(value, str) or not value.strip() for value in ids):
        raise ValueError("Every case needs a nonblank case ID")
    if len(set(ids)) != len(ids):
        raise ValueError("Case IDs must be unique")
    for case in cases:
        question = case.get("question")
        if (
            not isinstance(question, str)
            or not question.strip()
            or len(question) > 5000
        ):
            raise ValueError("Questions must contain 1–5000 characters")


def collect(
    cases: list[dict],
    *,
    model: Callable,
    observations: list[dict],
    budget_usd: Decimal,
    reserve_usd: Decimal,
    emit: Callable[[dict], None],
) -> dict:
    """Reserve before each request; persist every case, including skipped ones.

    Reservations are never reclaimed. Missing usage or a transport failure stops
    further requests because actual spend is unknown. Reservations are local
    accounting, not a provider billing cap; callers must choose them conservatively.
    """
    validate_cases(cases)
    if any(not value.is_finite() or value <= 0 for value in (budget_usd, reserve_usd)):
        raise ValueError("Budget and reservation must be finite and positive")
    reserved = Decimal(0)
    attempted = 0
    stop_reason = None
    tools = tools_for_model()
    for case in cases:
        row = {"case_id": case["case_id"], "turn": None}
        if stop_reason is None and reserved + reserve_usd > budget_usd:
            stop_reason = "budget"
        if stop_reason is not None:
            row["skip_reason"] = stop_reason
            emit(row)
            continue
        reserved += reserve_usd
        attempted += 1
        observations.clear()
        turn = model(
            messages=[{"role": "user", "content": case["question"]}],
            tools=deepcopy(tools),
        )
        if len(observations) != 1:
            raise RuntimeError(
                "Each model invocation must emit exactly one observation"
            )
        metadata = deepcopy(observations[0])
        row.update(turn=turn, metadata=metadata, reserved_usd=str(reserve_usd))
        usage = metadata.get("usage")
        valid_usage = isinstance(usage, dict) and all(
            type(usage.get(key)) is int and usage[key] >= 0
            for key in ("input_tokens", "output_tokens")
        )
        if metadata.get("outcome") == "transport_error":
            stop_reason = "transport_error"
        elif not valid_usage:
            stop_reason = "missing_usage"
        emit(row)
    return {
        "total": len(cases),
        "attempted": attempted,
        "skipped": len(cases) - attempted,
        "reserved_usd": str(reserved),
        "stop_reason": stop_reason,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--prompt-file", type=Path, default=DEFAULT_PROMPT)
    parser.add_argument("--model", default=Models.DEFAULT.value)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--budget-usd", type=Decimal)
    parser.add_argument("--reserve-usd", type=Decimal)
    parser.add_argument("--timeout-s", type=float, default=20.0)
    parser.add_argument("--max-output-tokens", type=int, default=512)
    parser.add_argument("--acknowledge-spend", action="store_true")
    args = parser.parse_args(argv)
    dataset_bytes = args.dataset.read_bytes()
    cases = read_jsonl(args.dataset)
    try:
        validate_cases(cases)
    except ValueError as exc:
        parser.error(str(exc))
    prompt = args.prompt_file.read_text()
    if not prompt.strip() or not args.model.strip():
        parser.error("Prompt and model must be nonblank")
    if (
        not math.isfinite(args.timeout_s)
        or args.timeout_s <= 0
        or args.max_output_tokens <= 0
    ):
        parser.error("Timeout and output limit must be finite and positive")
    tools = tools_for_model()
    manifest = {
        "run_kind": "model" if args.live else "dry-run",
        "model": args.model,
        "dataset_sha256": digest(dataset_bytes),
        "prompt_sha256": digest(args.prompt_file.read_bytes()),
        "instructions": prompt,
        "tools": tools,
        "tool_descriptions": ToolModel.TOOL_DESCRIPTIONS,
        "schema_sha256": digest(json.dumps(tools, sort_keys=True).encode()),
        "timeout_s": args.timeout_s,
        "max_output_tokens": args.max_output_tokens,
        "strict": False,
        "store": False,
        "openai_version": version("openai"),
        "started_at": datetime.now(UTC).isoformat(),
        "code_sha256": {
            str(path.relative_to(ROOT.parent)): digest(path.read_bytes())
            for path in (
                Path(__file__),
                ROOT.parent / "app/llm/tool_model.py",
                ROOT.parent / "app/clients/openai_tool_client.py",
                ROOT.parent / "app/clients/base.py",
            )
        },
    }
    if not args.live:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "cases": len(cases),
                    "requests": 0,
                    "model": args.model,
                    "dataset_sha256": manifest["dataset_sha256"],
                }
            )
        )
        return 0
    if not args.acknowledge_spend or args.output is None:
        parser.error("--live requires --acknowledge-spend and --output")
    if any(
        value is None or not value.is_finite() or value <= 0
        for value in (args.budget_usd, args.reserve_usd)
    ):
        parser.error("--live requires positive finite --budget-usd and --reserve-usd")
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key.strip():
        parser.error("Configure OPENAI_API_KEY outside source control")
    manifest_path = args.output.with_name(args.output.name + ".run.json")
    if args.output.exists() or manifest_path.exists():
        parser.error("Output or manifest exists; choose a new path")
    manifest.update(
        budget_usd=str(args.budget_usd),
        reserve_usd=str(args.reserve_usd),
        status="running",
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents accidental replacement of previous evidence.
    with manifest_path.open("x") as stream:
        json.dump(manifest, stream, indent=2)
    observations: list[dict] = []
    try:
        with (
            args.output.open("x") as output,
            create_openai_client(api_key=api_key) as sdk,
        ):
            model = ToolModel(
                client=OpenAIToolClient(client=sdk),
                model=args.model,
                instructions=prompt,
                request_timeout_s=args.timeout_s,
                max_output_tokens=args.max_output_tokens,
                observe=observations.append,
            )

            def emit(row: dict) -> None:
                output.write(json.dumps(row) + "\n")
                output.flush()
                print(
                    f"{row['case_id']}: {row.get('skip_reason', row.get('metadata', {}).get('outcome'))}",
                    file=sys.stderr,
                )

            summary = collect(
                cases,
                model=model,
                observations=observations,
                budget_usd=args.budget_usd,
                reserve_usd=args.reserve_usd,
                emit=emit,
            )
        manifest.update(
            summary,
            status="completed",
            predictions_sha256=digest(args.output.read_bytes()),
        )
    except Exception as exc:
        # Keep partial evidence and mark the run; do not disguise programming defects.
        manifest.update(status="aborted", error_type=type(exc).__name__)
        raise
    finally:
        manifest["finished_at"] = datetime.now(UTC).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(summary))
    return 0 if summary["skipped"] == 0 and summary["stop_reason"] is None else 1


if __name__ == "__main__":
    raise SystemExit(main())