"""Diagnose a synthetic fixture with the deterministic baseline; no API calls."""

import argparse
import json
from pathlib import Path

from app.models.diagnosis import Diagnosis, Payment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", default="case-001")
    parser.add_argument("--output", type=Path, help="Save JSON to a new file.")
    args = parser.parse_args()
    dataset = Path(__file__).resolve().parent / "datasets" / "week1.jsonl"
    cases = [
        json.loads(line)
        for line in dataset.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    matches = [case for case in cases if case["case_id"] == args.case_id]
    if len(matches) != 1:
        parser.error("--case-id must identify exactly one dataset case")
    case = matches[0]
    if case.get("synthetic") is not True:
        parser.error("only explicitly synthetic fixtures are supported")
    payment = Payment.model_validate(case["payment"])
    diagnosis = Diagnosis.model_validate_json(
        Diagnosis.diagnose(payment).model_dump_json()
    )
    output = diagnosis.model_dump_json() + "\n"
    if args.output is not None:
        try:
            with args.output.open("x", encoding="utf-8") as saved:
                saved.write(output)
        except OSError as exc:
            parser.error(f"cannot save result: {exc}")
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
