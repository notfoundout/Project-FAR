#!/usr/bin/env python3
"""Verify the immutable CRE-002 preregistration package byte-for-byte."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"
MANIFEST = PACKAGE / "package-manifest.json"
LOCK = PACKAGE / "checksum-lock.json"
EXECUTION_LOCK = PACKAGE / "execution-lock.json"
SOURCE_COMMIT = "003f0fda30f0919d13edb1e5f1b3b3d2e0fd1d04"
EXPECTED_IMMUTABLE_PATHS = {
    "README.md",
    "preregistration.md",
    "scenario/scenario-v1.0.md",
    "scenario/scenario-v1.0.json",
    "ambiguity-policies.json",
    "decision-rules.json",
}


def snapshot() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    paths = {item["path"] for item in manifest["files"]}
    if paths != EXPECTED_IMMUTABLE_PATHS:
        raise ValueError(f"immutable CRE-002 file set drifted: {sorted(paths)}")
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
        "source_commit": SOURCE_COMMIT,
        "execution_state_at_lock": False,
        "files": files,
        "excluded_mutable_controls": [
            {
                "path": "execution-lock.json",
                "initial_locked_sha256": "014a8cd67391270f28dec983a619bde281bc64473ec0eff397f5d86c507648f3",
                "initial_locked_byte_count": 722,
                "reason": "This reviewed administrative control must change to authorize execution and is not part of the immutable scientific preregistration content.",
            }
        ],
    }


def validate_execution_control() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    control = json.loads(EXECUTION_LOCK.read_text(encoding="utf-8"))
    if manifest["execution_permitted"] != control["execution_permitted"]:
        raise ValueError("manifest and execution control disagree")
    if control["execution_permitted"]:
        evidence = control.get("authorization_evidence", {})
        required = {
            "preregistration_merge_commit",
            "checksum_lock_merge_commit",
            "checksum_lock_id",
            "repository_health_before_unlock",
            "pre_unlock_result_artifacts_present",
        }
        if not required.issubset(evidence):
            raise ValueError("execution authorization evidence is incomplete")
        if evidence["repository_health_before_unlock"] != "passed":
            raise ValueError("execution authorization lacks passing repository health")
        if evidence["pre_unlock_result_artifacts_present"] is not False:
            raise ValueError("execution was not prospectively clean before unlock")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", type=Path)
    args = parser.parse_args()
    try:
        actual = snapshot()
        validate_execution_control()
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"CRE-002 lock validation failed: {exc}", file=sys.stderr)
        return 1
    if args.emit:
        args.emit.write_text(json.dumps(actual, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(args.emit)
        return 0
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
    print("CRE-002 checksum lock and execution control verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
