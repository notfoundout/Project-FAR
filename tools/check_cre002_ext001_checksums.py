#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001"
LOCK = PACKAGE / "checksum-lock.json"
IMMUTABLE_FILES = [
    "README.md",
    "preregistration.md",
    "scenario/scenario-v1.0.json",
    "ambiguity-policies.json",
    "decision-rules.json",
    "output-schema.json",
]


def snapshot() -> dict:
    files = []
    for relative in IMMUTABLE_FILES:
        path = PACKAGE / relative
        data = path.read_bytes()
        files.append({
            "path": relative,
            "sha256": hashlib.sha256(data).hexdigest(),
            "byte_count": len(data),
        })
    return {
        "lock_id": "CRE-002-EXT-001-CHECKSUM-LOCK-1.0",
        "algorithm": "SHA-256",
        "package_id": "CRE-002-EXT-001-PACKAGE-1.0",
        "immutable_scientific_files": files,
        "execution_permitted": False,
        "compiler_implementation_permitted": False,
        "official_results_present": False,
    }


def main() -> int:
    actual = snapshot()
    if not LOCK.exists():
        print("CRE-002-EXT-001 CHECKSUM SNAPSHOT")
        print(json.dumps(actual, indent=2, sort_keys=True))
        print("checksum-lock.json is missing", file=sys.stderr)
        return 1

    expected = json.loads(LOCK.read_text(encoding="utf-8"))
    if expected != actual:
        print("CRE-002-EXT-001 checksum lock mismatch", file=sys.stderr)
        print("EXPECTED")
        print(json.dumps(expected, indent=2, sort_keys=True))
        print("ACTUAL")
        print(json.dumps(actual, indent=2, sort_keys=True))
        return 1

    print("CRE-002-EXT-001 checksum lock verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
