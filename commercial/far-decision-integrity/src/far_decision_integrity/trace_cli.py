from __future__ import annotations

import argparse
import json
from pathlib import Path

from .trace_ingest import TraceIngestionError, ingest_trace, load_trace, package_payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-trace-ingest")
    parser.add_argument("trace")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        package = ingest_trace(load_trace(args.trace))
    except TraceIngestionError as exc:
        print(json.dumps({"status": "invalid-trace", "error": str(exc)}, sort_keys=True))
        return 40
    payload = package_payload(package)
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "normalized", "decision_id": package.decision_id, "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
