from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evidence import write_evidence_bundle
from .regression import RegressionDecision, compare_corpus, load_suite, report_payload

EXIT_CODES = {
    RegressionDecision.PASS: 0,
    RegressionDecision.BLOCKED: 30,
    RegressionDecision.REVIEW: 31,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-reasoning-regression")
    parser.add_argument("suite")
    parser.add_argument("--output-directory", required=True)
    args = parser.parse_args(argv)
    try:
        suite_id, baseline, candidate = load_suite(args.suite)
        report = compare_corpus(suite_id, baseline, candidate)
        payload = report_payload(report)
        report_path, manifest_path = write_evidence_bundle(
            args.output_directory,
            report_name="regression-report.json",
            report_payload=payload,
            source_files={"regression-suite": args.suite},
        )
    except ValueError as exc:
        print(json.dumps({"decision": "invalid-input", "error": str(exc)}, sort_keys=True))
        return 40
    print(
        json.dumps(
            {
                **payload,
                "report_path": str(report_path),
                "manifest_path": str(manifest_path),
            },
            sort_keys=True,
        )
    )
    return EXIT_CODES[report.decision]


if __name__ == "__main__":
    raise SystemExit(main())
