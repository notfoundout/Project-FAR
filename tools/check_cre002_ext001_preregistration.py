#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001"
REQUIRED = ["README.md", "preregistration.md", "scenario/scenario-v1.0.json", "ambiguity-policies.json", "decision-rules.json", "output-schema.json", "package-manifest.json", "execution-lock.json"]
NONCLAIMS = {"universal sufficiency", "primitive-only sufficiency", "necessity", "minimality", "independence", "superiority", "FAR proof", "universal structure of reasoning", "retrospective validation of CRE-002"}


def load(name: str):
    return json.loads((PKG / name).read_text())


def run_check(command: list[str], error: str, errors: list[str]) -> None:
    cp = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if cp.returncode != 0:
        errors.append(error)


def main() -> int:
    errors: list[str] = []
    for name in REQUIRED:
        if not (PKG / name).is_file():
            errors.append(f"missing {name}")
    if errors:
        print("CRE-002-EXT-001 PREREGISTRATION FAILED\n" + "\n".join(errors))
        return 1

    manifest, lock = load("package-manifest.json"), load("execution-lock.json")
    scenario, rules = load("scenario/scenario-v1.0.json"), load("decision-rules.json")
    policies, output = load("ambiguity-policies.json"), load("output-schema.json")

    if manifest.get("package_id") != "CRE-002-EXT-001-PACKAGE-1.0": errors.append("wrong package id")
    if manifest.get("checksum_state") != "locked": errors.append("checksum state must be locked")
    run_check([sys.executable, "tools/check_cre002_ext001_checksums.py"], "checksum verification failed", errors)

    if manifest.get("execution_permitted") is not True or lock.get("execution_permitted") is not True: errors.append("execution must remain authorized")
    if manifest.get("compiler_implementation_permitted") is not True or lock.get("compiler_implementation_permitted") is not True: errors.append("compiler implementation must remain authorized")

    results_present = manifest.get("official_results_present") is True or lock.get("official_results_present") is True
    if manifest.get("official_results_present") != lock.get("official_results_present"):
        errors.append("official result state is inconsistent")
    if results_present:
        if manifest.get("status") != "execution-complete" or lock.get("status") != "execution-complete": errors.append("completed result requires execution-complete status")
        for name in ["execution/cre002-ext001-comparison.json", "execution/execution-report.md", "execution/reference-behavior.json"]:
            if not (PKG / name).is_file(): errors.append(f"missing official result artifact {name}")
        run_check([sys.executable, "tools/cre002_ext001_execute.py", "--check"], "official execution artifacts are not deterministic", errors)
    elif manifest.get("status") != "execution-authorized" or lock.get("status") != "execution-authorized":
        errors.append("pre-result authorized state is inconsistent")

    audit_path = PKG / "execution-unlock-audit.json"
    if not audit_path.is_file(): errors.append("missing execution unlock audit")
    else:
        audit = load("execution-unlock-audit.json")
        if audit.get("authorization_status") != "authorized": errors.append("unlock audit is not authorized")
        if audit.get("immutable_package_lock_verified") is not True: errors.append("unlock audit omits checksum verification")
        if not NONCLAIMS.issubset(set(audit.get("nonclaims_preserved", []))): errors.append("unlock audit omits nonclaims")

    if scenario.get("scenario_id") != "CRE-002-EXT-001-SCENARIO-1.0": errors.append("wrong scenario id")
    if scenario.get("semantic_authority") != "VOCABULARY-SEMANTICS-BASELINE-1.1": errors.append("wrong semantic authority")
    if len(scenario.get("transitions", [])) != 9: errors.append("expected nine transition schemas")
    if len(policies.get("policies", [])) != 9: errors.append("expected nine ambiguity policies")
    if set(rules.get("candidate_outcomes", [])) != {"complete", "partial", "unsupported", "error"}: errors.append("candidate outcomes mismatch")
    if not NONCLAIMS.issubset(set(rules.get("global_nonclaims", []))): errors.append("decision rules omit nonclaims")
    if output.get("schema_id") != "CRE-002-EXT-001-OUTPUT-SCHEMA-1.0": errors.append("wrong output schema")
    if manifest.get("preserved_prior_result") != "CRE-002-COMPARISON-1.0": errors.append("prior CRE-002 result not preserved")

    if errors:
        print("CRE-002-EXT-001 PREREGISTRATION FAILED\n" + "\n".join(errors))
        return 1
    print("CRE-002-EXT-001 PREREGISTRATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
