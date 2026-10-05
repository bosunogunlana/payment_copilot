"""Two-configuration evaluation scaffolding. Defaults to a zero-request plan."""

import argparse
import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from time import perf_counter

from app.llm.diagnose import DiagnosisAdapter
from app.models.diagnosis import Diagnosis, Payment


ROOT = Path(__file__).resolve().parent


def estimated_cost(usage, config):
    if not isinstance(usage, dict):
        return None
    counts = [usage.get("input_tokens"), usage.get("output_tokens")]
    if any(type(count) is not int or count < 0 for count in counts):
        return None
    # Uncached input estimate; cache discounts/writes and account premiums excluded.
    return (
        counts[0] * config["input_usd_per_million"]
        + counts[1] * config["output_usd_per_million"]
    ) / 1_000_000


def score(case, result):
    diagnosis = result.diagnosis
    if diagnosis is None:
        return {"schema_valid": False, "label_match": False, "uncertainty_safe": None}
    actual = diagnosis.model_dump(mode="json")
    uncertainty_safe = None
    if case["expected"]["category"] == "unknown":
        uncertainty_safe = (
            diagnosis.likely_cause is None
            and diagnosis.confidence < 0.5
            and actual["recommended_action"] == "escalate_to_human"
        )
    return {
        "schema_valid": True,
        "label_match": all(actual[key] == value for key, value in case["expected"].items()),
        "uncertainty_safe": uncertainty_safe,
    }


def summarize(rows):
    groups = {}
    for row in rows:
        keys = ["all", "category:" + row["expected_category"]]
        keys += ["tag:" + tag for tag in row["failure_tags"]]
        for key in keys:
            group = groups.setdefault(row["configuration"] + "/" + key, {
                "total": 0, "attempted": 0, "skipped": 0,
                "schema_valid": 0, "label_match": 0, "errors": {},
                "unsafe_unknown": 0,
            })
            group["total"] += 1
            if "skip_reason" in row:
                group["skipped"] += 1
                continue
            group["attempted"] += 1
            for metric in ("schema_valid", "label_match"):
                group[metric] += int(row[metric])
            group["unsafe_unknown"] += int(row["uncertainty_safe"] is False)
            if row["error"]:
                group["errors"][row["error"]] = group["errors"].get(row["error"], 0) + 1
    for group in groups.values():
        count = group["attempted"]
        group["label_match_rate"] = group["label_match"] / count if count else None
        group["schema_valid_rate"] = group["schema_valid"] / count if count else None
    return groups


def validate_run(cases, configs, *, budget_usd, reserve_usd):
    if not all(math.isfinite(x) and x > 0 for x in (budget_usd, reserve_usd)):
        raise ValueError("Budget and per-request reservation must be finite and positive.")
    if len(configs) != 2 or len({c["name"] for c in configs}) != 2:
        raise ValueError("Exactly two uniquely named configurations are required.")
    for config in configs:
        if not isinstance(config["model"], str) or not config["model"].strip():
            raise ValueError("Each configuration must name a model.")
        if type(config["max_output_tokens"]) is not int or config["max_output_tokens"] <= 0:
            raise ValueError("Output token limits must be positive integers.")
        for field in ("input_usd_per_million", "output_usd_per_million"):
            if not math.isfinite(config[field]) or config[field] < 0:
                raise ValueError("Token rates must be finite and nonnegative.")
    payments = [Payment.model_validate(case["payment"]) for case in cases]
    if len({case["case_id"] for case in cases}) != len(cases):
        raise ValueError("Dataset case IDs must be unique.")
    for case in cases:
        Diagnosis.model_validate({**case["expected"], "confidence": 0.2})
        if not isinstance(case["failure_tags"], list) or not all(isinstance(tag, str) for tag in case["failure_tags"]):
            raise ValueError("Failure tags must be a list of strings.")
    return payments


def compare(cases, configs, transport_factory, *, budget_usd, reserve_usd, checkpoint=None, progress=None):
    payments = validate_run(cases, configs, budget_usd=budget_usd, reserve_usd=reserve_usd)
    prompt_hash = hashlib.sha256(DiagnosisAdapter.SYSTEM_INSTRUCTION.encode()).hexdigest()
    rows = []
    reserved = 0.0
    stop_reason = None
    total = len(cases) * len(configs)
    transports = {config["name"]: transport_factory(config) for config in configs}
    # Interleave configurations so a budget stop preserves paired coverage when possible.
    for case, payment in zip(cases, payments):
        for config in configs:
            prefix = f"[{len(rows) + 1}/{total}] {case['case_id']} {config['name']}"
            row = {
                "case_id": case["case_id"], "configuration": config["name"],
                "expected_category": case["expected"]["category"],
                "failure_tags": case["failure_tags"], "prompt_sha256": prompt_hash,
            }
            if stop_reason or reserved + reserve_usd > budget_usd + 1e-12:
                row["skip_reason"] = stop_reason or "budget_reservation_exhausted"
                rows.append(row)
                if checkpoint:
                    checkpoint(rows, reserved)
                if progress:
                    progress(f"{prefix} skipped: {row['skip_reason']}")
                continue
            reserved += reserve_usd
            observed = {}

            def capture(request):
                response = transports[config["name"]](request)
                if isinstance(response, dict):
                    observed.update(response)
                return response

            if progress:
                progress(f"{prefix} requesting {config['model']}...")
            start = perf_counter()
            result = DiagnosisAdapter(transport=capture).diagnose(payment)
            row.update(score(case, result))
            row.update(
                latency_ms=(perf_counter() - start) * 1000,
                result=result.model_dump(mode="json"),
                confidence=result.diagnosis.confidence if result.diagnosis else None,
                error=result.error.value if result.error else None,
                usage=observed.get("usage"),
                estimated_cost_usd=estimated_cost(observed.get("usage"), config),
            )
            row["cause_grounding"] = "manual_review_required" if result.diagnosis else "unavailable"
            rows.append(row)
            if checkpoint:
                checkpoint(rows, reserved)
            if progress:
                outcome = row["error"] or ("label match" if row["label_match"] else "label mismatch")
                if row["uncertainty_safe"] is False:
                    outcome += "; unsafe uncertainty"
                cost = row["estimated_cost_usd"]
                cost_text = f"${cost:.6f}" if cost is not None else "unavailable"
                progress(
                    f"{prefix} completed: {outcome}; {row['latency_ms'] / 1000:.2f}s; "
                    f"estimated cost {cost_text}; reserved ${reserved:.2f}/${budget_usd:.2f}"
                )
            if row["estimated_cost_usd"] is None:
                stop_reason = "usage_unavailable"
            elif row["estimated_cost_usd"] > reserve_usd:
                stop_reason = "cost_exceeded_reservation"
    return {
        "configurations": configs, "budget_usd": budget_usd,
        "reservation_per_request_usd": reserve_usd, "reserved_usd": reserved,
        "rows": rows, "summary": summarize(rows),
        "decision": "pending_actual_comparison_and_cause_review",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--budget-usd", type=float)
    parser.add_argument("--reserve-usd", type=float)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/week1-comparison.json")
    args = parser.parse_args()
    configs = json.loads((ROOT / "configs/week1.json").read_text())
    raw_dataset = (ROOT / "datasets/week1.jsonl").read_bytes()
    cases = [json.loads(line) for line in raw_dataset.decode().splitlines()]
    if not args.live:
        print(json.dumps({"mode": "dry-run", "requests": 0, "planned_requests": len(cases) * 2, "configurations": configs}))
        return
    if not all(x is not None and math.isfinite(x) and x > 0 for x in (args.budget_usd, args.reserve_usd)):
        parser.error("--live requires positive finite --budget-usd and --reserve-usd")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or not api_key.strip():
        parser.error("Set OPENAI_API_KEY outside source control")
    if args.output.exists():
        parser.error("Output already exists; choose a new report path")
    from app.llm.openai_transport import OpenAITransport, create_openai_client

    # Validate the full candidate run without constructing a live transport.
    validate_run(cases, configs, budget_usd=args.budget_usd, reserve_usd=args.reserve_usd)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "mode": "live", "run_status": "in_progress", "configurations": configs,
        "dataset_sha256": hashlib.sha256(raw_dataset).hexdigest(),
        "prompt_sha256": hashlib.sha256(DiagnosisAdapter.SYSTEM_INSTRUCTION.encode()).hexdigest(),
        "sdk_version": version("openai"), "budget_usd": args.budget_usd,
        "reservation_per_request_usd": args.reserve_usd,
        "cause_review": "pending", "rows": [],
    }
    # Exclusive creation prevents replacing an existing experiment.
    with args.output.open("x", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    def save_checkpoint(rows, reserved):
        partial = {**metadata, "rows": rows, "reserved_usd": reserved, "summary": summarize(rows)}
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(json.dumps(partial, indent=2) + "\n", encoding="utf-8")
        temporary.replace(args.output)

    def print_progress(message):
        print(message, file=sys.stderr, flush=True)

    print_progress(f"Starting comparison: {len(cases)} cases × {len(configs)} configurations")
    with create_openai_client(api_key=api_key) as client:
        report = compare(cases, configs, lambda config: OpenAITransport(
            client=client, model=config["model"], max_output_tokens=config["max_output_tokens"]
        ), budget_usd=args.budget_usd, reserve_usd=args.reserve_usd,
            checkpoint=save_checkpoint, progress=print_progress)
    report.update(
        mode="live", run_status="completed", dataset_sha256=hashlib.sha256(raw_dataset).hexdigest(),
        completed_at=datetime.now(timezone.utc).isoformat(), sdk_version=version("openai"),
        cause_review="pending", pricing_basis="Standard uncached text estimate; see evals/README.md",
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    attempted = sum("skip_reason" not in row for row in report["rows"])
    print_progress(f"Comparison finished: {attempted} attempted, {len(report['rows']) - attempted} skipped; report saved")
    print(str(args.output))


if __name__ == "__main__":
    main()
