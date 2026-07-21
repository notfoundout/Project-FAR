#!/usr/bin/env python3
"""Small independent bootstrap verifier for the unified validation manifest."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "validation" / "manifest.json"
LOCK = ROOT / "validation_bootstrap" / "bootstrap-lock.json"


def fail(message: str) -> int:
    print(f"FAR-VAL-BOOT-001: {message}", file=sys.stderr)
    return 1


def main() -> int:
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"cannot load bootstrap inputs: {exc}")

    if manifest.get("schema_version") != "1.0" or lock.get("schema_version") != "1.0":
        return fail("unsupported schema version")
    raw_checks = manifest.get("checks")
    profiles = manifest.get("profiles")
    if not isinstance(raw_checks, list) or not isinstance(profiles, dict):
        return fail("manifest checks/profiles malformed")
    checks = {item.get("id"): item for item in raw_checks if isinstance(item, dict)}
    if None in checks or len(checks) != len(raw_checks):
        return fail("missing or duplicate check IDs")

    manifest_protected = set(manifest.get("protected_checks", []))
    locked_protected = set(lock.get("protected_checks", []))
    if manifest_protected != locked_protected:
        return fail(
            f"protected check set changed: expected={sorted(locked_protected)} "
            f"actual={sorted(manifest_protected)}"
        )
    for check_id in sorted(locked_protected):
        check = checks.get(check_id)
        if not check:
            return fail(f"protected check missing: {check_id}")
        if check.get("protected") is not True:
            return fail(f"protected check flag removed: {check_id}")
        if check.get("severity") != "critical":
            return fail(f"protected check severity weakened: {check_id}")
        for profile in lock.get("required_profiles", []):
            if check_id not in profiles.get(profile, []):
                return fail(f"protected check {check_id} missing from {profile}")

    for profile, check_ids in profiles.items():
        if not isinstance(check_ids, list):
            return fail(f"profile {profile} must be a list")
        unknown = sorted(set(check_ids) - set(checks))
        if unknown:
            return fail(f"profile {profile} references unknown checks: {unknown}")

    print(
        f"Project FAR bootstrap verified: {len(checks)} checks, "
        f"{len(locked_protected)} protected checks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
