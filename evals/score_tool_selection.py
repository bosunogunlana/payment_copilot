"""Score saved normalized first turns offline; never makes model requests."""

import argparse
import hashlib
import json
from pathlib import Path

from pydantic import ValidationError

from app.llm.tool_loop import ToolLoop
from app.tools.contracts import TOOL_ARGUMENT_MODELS

DEFAULT_DATASET = Path(__file__).resolve().parent / "datasets/tool_selection.jsonl"


def read_jsonl(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if any(not isinstance(row, dict) for row in rows):
        raise ValueError("JSONL rows must be objects")
    return rows


def score(cases: list[dict], predictions: list[dict]) -> dict:
    ids = [case["case_id"] for case in cases]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Dataset must have unique case IDs and at least one case")
    by_id = {}
    for prediction in predictions:
        case_id = prediction.get("case_id")
        if case_id not in ids or case_id in by_id:
            raise ValueError("Unknown or duplicate prediction case ID")
        by_id[case_id] = prediction
    results = []
    for case in cases:
        prediction = by_id.get(case["case_id"])
        parsed = ToolLoop.parse_turn(prediction.get("turn")) if prediction else None
        first = parsed[0][0] if parsed and parsed[0] else None
        selected = first["name"] if first else None
        arguments = None
        if first and selected in TOOL_ARGUMENT_MODELS:
            try:
                arguments = (
                    TOOL_ARGUMENT_MODELS[selected]
                    .model_validate(json.loads(first["arguments_json"]))
                    .model_dump(mode="json")
                )
            except (ValueError, ValidationError):
                pass
        results.append(
            {
                "case_id": case["case_id"],
                "expected_tool": case["expected_tool"],
                "selected_tool": selected,
                "tool_correct": selected == case["expected_tool"],
                "arguments_correct": (
                    selected == case["expected_tool"]
                    and arguments == case["expected_arguments"]
                ),
                "missing_prediction": prediction is None,
            }
        )
    correct = sum(row["tool_correct"] for row in results)
    return {
        "total": len(cases),
        "predictions": len(predictions),
        "correct": correct,
        "accuracy": correct / len(cases),
        "threshold_met": correct * 10 >= len(cases) * 9,
        "arguments_correct": sum(row["arguments_correct"] for row in results),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--run-kind", choices=("model", "scripted"), required=True)
    parser.add_argument("--model", required=True, help="Model ID or scripted stub name")
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = score(read_jsonl(args.dataset), read_jsonl(args.predictions))
    report.update(
        {
            "run_kind": args.run_kind,
            "model": args.model,
            "dataset_sha256": hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
            "prompt_sha256": hashlib.sha256(args.prompt_file.read_bytes()).hexdigest(),
            "predictions_sha256": hashlib.sha256(
                args.predictions.read_bytes()
            ).hexdigest(),
            "quality_gate_met": args.run_kind == "model" and report["threshold_met"],
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}))
    return 0 if report["threshold_met"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
