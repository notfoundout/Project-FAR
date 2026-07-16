#!/usr/bin/env python3
"""Validate the frozen CRE-002 preregistration and its reviewed execution state."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"
SCIENTIFIC_FILES = ["README.md", "preregistration.md", "scenario/scenario-v1.0.md", "scenario/scenario-v1.0.json", "ambiguity-policies.json", "decision-rules.json"]
ADMIN_FILES = ["execution-lock.json", "package-manifest.json", "checksum-lock.json"]
NONCLAIMS = ["universal sufficiency", "primitive-only sufficiency", "necessity", "minimality", "independence", "superiority", "FAR proof", "universal structure of reasoning"]


def load(rel: str):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    for rel in SCIENTIFIC_FILES + ADMIN_FILES:
        if not (BASE / rel).is_file():
            errors.append(f"missing {rel}")
    if errors:
        print("CRE-002 PREREGISTRATION CHECK FAILED")
        print("\n".join(errors))
        return 1
    scenario, policies, decisions = load("scenario/scenario-v1.0.json"), load("ambiguity-policies.json"), load("decision-rules.json")
    lock, manifest = load("execution-lock.json"), load("package-manifest.json")
    permitted = lock.get("execution_permitted")
    if permitted not in {False, True}:
        errors.append("execution control must contain a boolean execution_permitted value")
    if manifest.get("execution_permitted") is not permitted:
        errors.append("manifest execution state differs from execution control")
    results_present = (BASE / "execution/cre002-comparison.json").is_file()
    if manifest.get("official_results_present") is not results_present:
        errors.append("manifest official-results state differs from committed execution evidence")
    if permitted is True:
        audit_path = BASE / "execution-unlock-audit.json"
        if not audit_path.is_file():
            errors.append("authorized execution requires execution-unlock-audit.json")
        else:
            audit = load("execution-unlock-audit.json")
            if audit.get("authorization_status") != "authorized":
                errors.append("execution unlock audit is not authorized")
            if audit.get("preregistration_merge_commit") != "a2c46a72b0fe145fd4835973d799531222f1edd8":
                errors.append("unlock audit lacks the registered preregistration merge commit")
            if audit.get("checksum_lock_merge_commit") != "f1d086480ae39c91d05a1381f4c3915e682ce439":
                errors.append("unlock audit lacks the registered checksum-lock merge commit")
        valid_statuses = {"execution-authorized", "execution-completed"}
        if manifest.get("status") not in valid_statuses:
            errors.append("authorized manifest has an invalid status")
        if results_present and manifest.get("status") != "execution-completed":
            errors.append("committed results require execution-completed manifest status")
    elif manifest.get("status") not in {"preregistered-under-review", "preregistered-checksum-locked"}:
        errors.append("locked manifest has an invalid preregistration status")
    if len(scenario.get("transitions", [])) < 9:
        errors.append("scenario transition set is incomplete")
    if len(policies.get("policies", [])) < 8:
        errors.append("ambiguity policy set is incomplete")
    if set(decisions.get("candidate_outcomes", [])) != {"complete", "partial", "unsupported", "error"}:
        errors.append("candidate outcome set differs from preregistration")
    manifest_paths = {entry.get("path") for entry in manifest.get("files", [])}
    for rel in SCIENTIFIC_FILES:
        if rel not in manifest_paths:
            errors.append(f"manifest omits immutable scientific file {rel}")
    if "execution-lock.json" in manifest_paths:
        errors.append("mutable execution control must not be listed as an immutable scientific file")
    controls = {entry.get("path") for entry in manifest.get("mutable_administrative_controls", [])}
    if "execution-lock.json" not in controls:
        errors.append("manifest omits execution-lock.json from mutable administrative controls")
    combined = "\n".join((BASE / rel).read_text(encoding="utf-8") for rel in ["README.md", "preregistration.md"])
    for claim in NONCLAIMS:
        if claim not in combined:
            errors.append(f"missing nonclaim: {claim}")
    if errors:
        print("CRE-002 PREREGISTRATION CHECK FAILED")
        print("\n".join(errors))
        return 1
    print("CRE-002 PREREGISTRATION CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
