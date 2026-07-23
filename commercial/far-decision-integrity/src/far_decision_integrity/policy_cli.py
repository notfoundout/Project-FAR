from __future__ import annotations

import argparse
import json
from pathlib import Path

from .policy_impact import ImpactDecision, RefundPolicy, compare_policies
from .refund import RefundRequest

EXIT_CODES = {ImpactDecision.PASS: 0, ImpactDecision.REVIEW: 31, ImpactDecision.BLOCKED: 30}


def _load(path: str) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-policy-impact")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        baseline = RefundPolicy(**_load(args.baseline))
        candidate = RefundPolicy(**_load(args.candidate))
        raw_cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
        if not isinstance(raw_cases, list):
            raise ValueError("cases must contain a JSON array")
        cases = [RefundRequest(**item) for item in raw_cases]
        report = compare_policies(baseline, candidate, cases)
        payload = report.to_dict()
        Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(payload, sort_keys=True))
        return EXIT_CODES[report.decision]
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"decision": "invalid-input", "error": str(exc)}, sort_keys=True))
        return 40


if __name__ == "__main__":
    raise SystemExit(main())
