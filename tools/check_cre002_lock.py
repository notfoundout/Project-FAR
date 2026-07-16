#!/usr/bin/env python3
"""Verify the frozen CRE-002 preregistration package byte-for-byte."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"
MANIFEST = PACKAGE / "package-manifest.json"
LOCK = PACKAGE / "checksum-lock.json"


def snapshot() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = []
    for item in manifest["files"]:
        relative = item["path"]
        path = PACKAGE / relative
        payload = path.read_bytes()
        files.append({
            "path": relative,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_count": len(payload),
        })
    return {
        "lock_id": "CRE-002-CHECKSUM-LOCK-1.0",
        "algorithm": "SHA-256",
        "package_id": manifest["package_id"],
        "source_commit": "a2c46a72b0fe145fd4835973d799531222f1edd8",
        "execution_permitted": False,
        "files": files,
    }


def main() -> int:
    actual = snapshot()
    if not LOCK.exists():
        print("CRE-002 CHECKSUM SNAPSHOT")
        print(json.dumps(actual, indent=2, sort_keys=True))
        print("CRE-002 checksum lock missing", file=sys.stderr)
        return 1
    recorded = json.loads(LOCK.read_text(encoding="utf-8"))
    if recorded != actual:
        print("CRE-002 CHECKSUM SNAPSHOT")
        print(json.dumps(actual, indent=2, sort_keys=True))
        print("CRE-002 checksum lock mismatch", file=sys.stderr)
        return 1
    print("CRE-002 checksum lock verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
