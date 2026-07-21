#!/usr/bin/env python3
"""Independent bootstrap verifier for the Project FAR validation authority.

This verifier intentionally uses only the Python standard library and does not
import the validation engine it protects.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "validation" / "manifest.json"
LOCK = ROOT / "validation_bootstrap" / "bootstrap-lock.json"


def fail(message: str) -> int:
    print(f"FAR-VAL-BOOT-001: {message}", file=sys.stderr)
    return 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_object(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return payload


def main() -> int:
    try:
        manifest = load_object(MANIFEST)
        lock = load_object(LOCK)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
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

    assurance_path = lock.get("assurance_lock")
    if not isinstance(assurance_path, str) or not assurance_path:
        return fail("assurance lock path is missing")
    try:
        assurance = load_object(ROOT / assurance_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return fail(f"cannot load assurance lock: {exc}")
    if assurance.get("schema_version") != "1.0":
        return fail("unsupported assurance lock schema")

    files = assurance.get("files")
    if not isinstance(files, dict) or not files:
        return fail("assurance file lock must be nonempty")
    for raw_path, expected in sorted(files.items()):
        if not isinstance(raw_path, str) or not isinstance(expected, str) or len(expected) != 64:
            return fail(f"malformed assurance hash entry: {raw_path!r}")
        path = ROOT / raw_path
        if not path.is_file():
            return fail(f"assurance file missing: {raw_path}")
        actual = sha256(path)
        if actual != expected:
            return fail(f"assurance file hash mismatch: {raw_path}: {actual} != {expected}")

    workflow = assurance.get("workflow")
    if not isinstance(workflow, dict):
        return fail("assurance workflow contract missing")
    workflow_path = workflow.get("path")
    fragments = workflow.get("required_fragments")
    if not isinstance(workflow_path, str) or not isinstance(fragments, list):
        return fail("assurance workflow contract malformed")
    try:
        workflow_text = (ROOT / workflow_path).read_text(encoding="utf-8")
    except OSError as exc:
        return fail(f"cannot read assurance workflow: {exc}")
    for fragment in fragments:
        if not isinstance(fragment, str) or fragment not in workflow_text:
            return fail(f"assurance workflow missing required fragment: {fragment!r}")

    evidence = assurance.get("required_evidence")
    if not isinstance(evidence, list) or set(evidence) != {
        "independent-oracle", "test-weakening", "formal-model", "lean-proof", "mutation-campaign",
    }:
        return fail("required assurance evidence set changed")
    for evidence_id in evidence:
        marker = f"--required-evidence {evidence_id}"
        if marker not in workflow_text:
            return fail(f"merge certificate does not require assurance evidence: {evidence_id}")

    runtime_policy_path = assurance.get("runtime_policy")
    try:
        runtime_policy = load_object(ROOT / str(runtime_policy_path))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return fail(f"cannot load runtime policy: {exc}")
    if runtime_policy.get("network_policy") != "deny":
        return fail("runtime network policy was weakened")
    if runtime_policy.get("skip_checks"):
        return fail("runtime trace exemptions are not allowed in the frozen assurance package")

    print(
        f"Project FAR bootstrap verified: {len(checks)} checks, "
        f"{len(locked_protected)} protected checks, {len(files)} assurance files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
