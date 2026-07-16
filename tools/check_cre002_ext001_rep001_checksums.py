#!/usr/bin/env python3
"""Verify the frozen CRE-002-EXT-001-REP-001 scientific package byte-for-byte."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001"
LOCK = PACKAGE / "checksum-lock.json"
FILES = [
    "README.md",
    "preregistration.md",
    "isolation-protocol.json",
    "decision-rules.json",
    "output-schema.json",
]


def snapshot() -> dict:
    records = []
    for relative in FILES:
        path = PACKAGE / relative
        payload = path.read_bytes()
        records.append({
            "path": relative,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_count": len(payload),
        })
    return {
        "artifact_id": "CRE-002-EXT-001-REP-001-CHECKSUM-LOCK-1.0",
        "algorithm": "SHA-256",
        "status": "locked",
        "immutable_scientific_files": records,
    }


def main() -> int:
    actual = snapshot()
    if not LOCK.exists():
        print("CRE-002-EXT-001-REP-001 CHECKSUM SNAPSHOT")
        print(json.dumps(actual, indent=2, sort_keys=True))
        return 1
    recorded = json.loads(LOCK.read_text(encoding="utf-8"))
    if recorded != actual:
        print("CRE-002-EXT-001-REP-001 CHECKSUM MISMATCH")
        print(json.dumps(actual, indent=2, sort_keys=True))
        return 1
    print("CRE-002-EXT-001-REP-001 checksum lock verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
