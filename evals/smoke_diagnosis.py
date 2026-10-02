"""One synthetic smoke request; dry-run unless --live is explicitly supplied."""

import argparse
import json
import os
from pathlib import Path

from app.models.diagnosis import Payment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL"),
        help="Override OPENAI_MODEL or the transport's default model.",
    )
    parser.add_argument("--max-output-tokens", type=int)
    parser.add_argument(
        "--acknowledge-spend", action="store_true",
        help="Confirm you reviewed model pricing and set a personal smoke-run allowance.",
    )
    args = parser.parse_args()
    dataset = Path(__file__).resolve().parent / "datasets" / "week1.jsonl"
    case = json.loads(next(line for line in dataset.read_text().splitlines() if line.strip()))
    payment = Payment.model_validate(case["payment"])

    if not args.live:
        print(json.dumps({"mode": "dry-run", "case_id": case["case_id"], "requests": 0}))
        return 0
    if not args.max_output_tokens or args.max_output_tokens < 1:
        parser.error("--live requires a positive --max-output-tokens")
    if not args.acknowledge_spend:
        parser.error("--live requires --acknowledge-spend")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or not api_key.strip():
        parser.error("OPENAI_API_KEY must be configured outside source control")

    from app.llm.diagnose import DiagnosisAdapter
    from app.llm.openai_transport import Models, OpenAITransport, create_openai_client

    with create_openai_client(api_key=api_key) as client:
        transport = OpenAITransport(
            client=client,
            model=args.model or Models.DEFAULT,
            max_output_tokens=args.max_output_tokens,
        )
        result = DiagnosisAdapter(transport=transport).diagnose(payment)
    print(result.model_dump_json())
    return 0 if result.error is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
