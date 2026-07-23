from __future__ import annotations

import argparse
import json
from pathlib import Path

from .distributed import DISTRIBUTED_SCHEMA_VERSION, DistributedRuntimeError

INVALID_INPUT_EXIT = 40


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="far-distributed-runtime")
    parser.add_argument("config", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = json.loads(args.config.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise DistributedRuntimeError("configuration must be a JSON object")
        required = ("postgres_dsn_secret", "object_store", "coordination")
        missing = [name for name in required if not payload.get(name)]
        if missing:
            raise DistributedRuntimeError("missing configuration fields: " + ", ".join(missing))
        result = {
            "schema_version": DISTRIBUTED_SCHEMA_VERSION,
            "status": "valid",
            "metadata_backend": "postgresql",
            "object_backend": payload["object_store"].get("type"),
            "coordination_backend": payload["coordination"].get("type"),
        }
    except (OSError, json.JSONDecodeError, DistributedRuntimeError, AttributeError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, sort_keys=True))
        return INVALID_INPUT_EXIT
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
