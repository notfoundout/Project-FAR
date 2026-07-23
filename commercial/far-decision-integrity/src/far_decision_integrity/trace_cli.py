from __future__ import annotations

import argparse
import json
from pathlib import Path

from .trace_ingest import TraceIngestionError, ingest_trace, load_trace, package_payload

INVALID_TRACE_EXIT = 40
OUTPUT_ERROR_EXIT = 41


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-trace-ingest")
    parser.add_argument("trace")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        package = ingest_trace(load_trace(args.trace))
    except TraceIngestionError as exc:
        print(json.dumps({"status": "invalid-trace", "error": str(exc)}, sort_keys=True))
        return INVALID_TRACE_EXIT

    payload = package_payload(package)
    try:
        Path(args.output).write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        print(
            json.dumps(
                {"status": "output-error", "error": str(exc), "output": str(args.output)},
                sort_keys=True,
            )
        )
        return OUTPUT_ERROR_EXIT

    print(
        json.dumps(
            {
                "status": "normalized",
                "decision_id": package.decision_id,
                "output": str(args.output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
