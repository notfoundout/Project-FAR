"""Fail-closed checks for POST-W6-AUDIT-HARDENING-001."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

AUDIT_TARGET_COMMIT = "03cda5007ff4ac8ca3ce90585b8c872f091965cf"
AUDIT_TARGET_TREE = "90d299b6c4df4824fe512e63f1cead49c90f9b41"
W6_RESULTS = ROOT / "research/results/pca-w6-empirical-audit-utility/results.json"
W6_EXECUTION = ROOT / "docs/research/pca-w6-empirical-audit-utility/02-execution-and-results.md"
HARDENING_RECORD = ROOT / "governance/post-w6-audit-hardening-v1.0.json"
INCIDENT_LEDGER = ROOT / "governance/post-w6-execution-incidents-v1.0.json"
AUDIT_DOC = ROOT / "docs/audits/post-w6-audit-hardening-v1.0.md"
MANIFEST = ROOT / "governance/post-w6-audit-hardening-manifest-v1.0.json"

EXPECTED_W6_RESULTS_SHA256 = "6b4784bb012445149f684651e195112c922cdd107a3d891b51ae203a7ce3b3bb"
EXPECTED_W6_EXECUTION_SHA256 = "6fc2266117f5aa9f14e8d7cfcce782892dfac3d0a7acc93f96e0da76fad21db8"
EXPECTED_INCIDENT_IDS = tuple(f"W6-INC-{index:03d}" for index in range(1, 8))
EXPECTED_FINDINGS = {
    "PW6-AUDIT-001": ("MODERATE", "REPAIR_WITH_SIDECAR_LEDGER"),
    "PW6-AUDIT-002": ("HIGH", "BLOCKED_EXTERNAL_CONFIGURATION"),
}
EXPECTED_HARDENING_ARTIFACTS = (
    "docs/audits/post-w6-audit-hardening-v1.0.md",
    "docs/planning/next-actions.md",
    "governance/post-w6-audit-hardening-v1.0.json",
    "governance/post-w6-execution-incidents-v1.0.json",
    "tests/test_post_w6_audit_hardening.py",
    "tools/check_post_w6_audit_hardening.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_manifest() -> list[str]:
    errors: list[str] = []
    if not MANIFEST.is_file():
        return ["missing hardening manifest"]
    manifest = load_json(MANIFEST)
    if manifest.get("schema_version") != "1.0":
        errors.append("hardening manifest schema_version mismatch")
    if manifest.get("record_id") != "POST-W6-AUDIT-HARDENING-001":
        errors.append("hardening manifest record id mismatch")
    if manifest.get("status") != "REPAIR_IN_PROGRESS":
        errors.append("hardening manifest must remain REPAIR_IN_PROGRESS while control-plane protection is open")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return errors + ["hardening manifest artifacts must be a list"]
    observed_paths: list[str] = []
    for item in artifacts:
        if not isinstance(item, dict) or set(item) != {"path", "git_blob_sha1"}:
            errors.append("hardening manifest artifact entries must contain only path and git_blob_sha1")
            continue
        rel = str(item["path"])
        observed_paths.append(rel)
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"hardening manifest artifact missing: {rel}")
            continue
        actual = git_blob_sha1(path)
        if item["git_blob_sha1"] != actual:
            errors.append(
                f"hardening manifest blob mismatch: {rel}: expected={item['git_blob_sha1']} actual={actual}"
            )
    if tuple(observed_paths) != EXPECTED_HARDENING_ARTIFACTS:
        errors.append(
            "hardening manifest artifact set/order mismatch: "
            f"expected={EXPECTED_HARDENING_ARTIFACTS!r} actual={tuple(observed_paths)!r}"
        )
    return errors


def check() -> list[str]:
    errors: list[str] = []

    for path in (W6_RESULTS, W6_EXECUTION, HARDENING_RECORD, INCIDENT_LEDGER, AUDIT_DOC, MANIFEST):
        if not path.is_file():
            errors.append(f"missing required hardening artifact: {path.relative_to(ROOT)}")
    if errors:
        return errors

    if sha256(W6_RESULTS) != EXPECTED_W6_RESULTS_SHA256:
        errors.append("frozen W6 results.json changed during post-W6 hardening")
    if sha256(W6_EXECUTION) != EXPECTED_W6_EXECUTION_SHA256:
        errors.append("audited W6 execution record changed during post-W6 hardening")

    hardening = load_json(HARDENING_RECORD)
    if hardening.get("schema_version") != "1.0":
        errors.append("hardening record schema_version mismatch")
    if hardening.get("record_id") != "POST-W6-AUDIT-HARDENING-001":
        errors.append("hardening record id mismatch")
    if hardening.get("status") != "REPAIR_IN_PROGRESS":
        errors.append("hardening record must remain REPAIR_IN_PROGRESS while control-plane protection is open")
    target = hardening.get("audit_target", {})
    if target.get("main_commit") != AUDIT_TARGET_COMMIT or target.get("main_tree") != AUDIT_TARGET_TREE:
        errors.append("hardening audit target drift")
    if target.get("w6_results_sha256") != EXPECTED_W6_RESULTS_SHA256:
        errors.append("hardening record W6 result hash mismatch")
    if target.get("w6_execution_sha256") != EXPECTED_W6_EXECUTION_SHA256:
        errors.append("hardening record W6 execution hash mismatch")

    findings = hardening.get("findings")
    if not isinstance(findings, list) or len(findings) != 2:
        errors.append("hardening record must contain exactly two accepted findings")
    else:
        observed = {}
        for finding in findings:
            if not isinstance(finding, dict):
                errors.append("hardening finding must be an object")
                continue
            finding_id = finding.get("id")
            if finding_id in observed:
                errors.append(f"duplicate hardening finding: {finding_id}")
            observed[finding_id] = (finding.get("severity"), finding.get("disposition"))
            if finding.get("theory_impact") != "NONE":
                errors.append(f"finding {finding_id} must not claim theory impact")
            if finding.get("w6_scientific_result_impact") != "NONE":
                errors.append(f"finding {finding_id} must not claim W6 scientific-result impact")
        if observed != EXPECTED_FINDINGS:
            errors.append(f"hardening finding projection mismatch: {observed!r}")

    repairs = hardening.get("repairs", {})
    incident_repair = repairs.get("machine_readable_execution_incidents", {})
    if incident_repair.get("status") != "IMPLEMENTED_ON_REPAIR_BRANCH":
        errors.append("machine-readable incident repair is not marked implemented on the repair branch")
    control_plane = repairs.get("control_plane_branch_protection", {})
    if control_plane.get("status") != "BLOCKED_EXTERNAL_CONFIGURATION":
        errors.append("branch-protection repair must remain an explicit external-configuration blocker")
    required_state = control_plane.get("required_state", {})
    required_true = (
        "protected",
        "require_pull_request_before_merge",
        "require_status_checks",
        "require_branches_up_to_date",
        "restrict_force_pushes",
        "restrict_deletions",
        "include_administrators_or_equivalent_bypass_restriction",
    )
    for field in required_true:
        if required_state.get(field) is not True:
            errors.append(f"branch-protection required state missing true field: {field}")
    completion = str(control_plane.get("completion_condition", ""))
    if "GitHub control-plane read" not in completion or "Repository files or CI" not in completion:
        errors.append("branch-protection completion condition must reject repository-local substitutes")

    ledger = load_json(INCIDENT_LEDGER)
    if ledger.get("schema_version") != "1.0":
        errors.append("incident ledger schema_version mismatch")
    if ledger.get("record_id") != "PCA-W6-EXECUTION-INCIDENTS-1.0":
        errors.append("incident ledger record id mismatch")
    if ledger.get("source_execution_sha256") != EXPECTED_W6_EXECUTION_SHA256:
        errors.append("incident ledger source execution hash mismatch")
    if ledger.get("frozen_result_sha256") != EXPECTED_W6_RESULTS_SHA256:
        errors.append("incident ledger frozen result hash mismatch")
    if ledger.get("scientific_deviations") != []:
        errors.append("incident ledger must preserve zero scientific deviations")
    incidents = ledger.get("execution_incidents")
    if not isinstance(incidents, list):
        errors.append("execution_incidents must be a list")
    else:
        incident_ids = tuple(item.get("id") for item in incidents if isinstance(item, dict))
        if incident_ids != EXPECTED_INCIDENT_IDS:
            errors.append(f"execution incident projection mismatch: {incident_ids!r}")
        for item in incidents:
            if not isinstance(item, dict):
                errors.append("execution incident must be an object")
                continue
            if item.get("changed_scientific_condition") is not False:
                errors.append(f"incident {item.get('id')} must remain classified as non-scientific")
            if not item.get("observation") or not item.get("resolution"):
                errors.append(f"incident {item.get('id')} lacks observation or resolution")

    audit_text = AUDIT_DOC.read_text(encoding="utf-8")
    required_phrases = (
        "REPOSITORY REPAIR IMPLEMENTED, CONTROL-PLANE ENFORCEMENT OPEN",
        "preserve the frozen W6 result byte-for-byte",
        "Repository-local CI and validators",
        "not equivalent to branch protection",
        "does not imply a W7",
    )
    for phrase in required_phrases:
        if phrase not in audit_text:
            errors.append(f"audit document missing required boundary: {phrase}")

    errors.extend(check_manifest())
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("POST-W6-AUDIT-HARDENING: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("POST-W6-AUDIT-HARDENING: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
