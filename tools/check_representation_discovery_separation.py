#!/usr/bin/env python3
"""Enforce separation between finite representation results and universal-structure discovery."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATHS = {
    "standard": ROOT / "docs/governance/representation-discovery-separation-standard-v1.0.md",
    "baseline_doc": ROOT / "docs/research/generic-relational-baseline-v1.0.md",
    "baseline": ROOT / "theory/evaluation/generic-relational-baseline-v1.0.json",
    "scope_doc": ROOT / "docs/research/reasoning-and-contrast-scope-v1.0.md",
    "scope": ROOT / "theory/evaluation/reasoning-and-contrast-scope-v1.0.json",
    "us_doc": ROOT / "docs/research/universal-structure-discovery-target-v1.0.md",
    "us_target": ROOT / "theory/evaluation/universal-structure-discovery-target-v1.0.json",
    "w35_doc": ROOT / "docs/research/w3-5-specificity-and-discovery-gate-v1.0.md",
    "w35": ROOT / "theory/evaluation/w3-5-specificity-and-discovery-gate.json",
    "candidates": ROOT / "theory/evaluation/universal-structure-candidate-registry.json",
    "gates": ROOT / "theory/evaluation/research-gates.json",
    "claims": ROOT / "theory/evaluation/central-claim-registry.json",
    "target": ROOT / "theory/evaluation/thm-target-001.json",
    "central": ROOT / "docs/governance/central-research-program.md",
    "proof_roadmap": ROOT / "docs/planning/deduction-first-proof-roadmap.md",
    "neutral_roadmap": ROOT / "docs/planning/architecture-neutral-research-roadmap.md",
    "readme": ROOT / "README.md",
    "makefile": ROOT / "Makefile",
    "task_generator": ROOT / "tools/generate_next_tasks.py",
    "status_generator": ROOT / "tools/project_status_report.py",
    "dashboard_generator": ROOT / "tools/update_readme_dashboard.py",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    for name, path in PATHS.items():
        require(path.is_file(), f"missing {name}: {path.relative_to(ROOT)}", errors)
    if errors:
        print("Representation-discovery separation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    baseline = load(PATHS["baseline"])
    scope = load(PATHS["scope"])
    us_target = load(PATHS["us_target"])
    w35 = load(PATHS["w35"])
    candidates = load(PATHS["candidates"])
    gates = load(PATHS["gates"])
    claims = load(PATHS["claims"])
    target = load(PATHS["target"])

    require(baseline.get("baseline_id") == "GREL-001", "generic baseline id must be GREL-001", errors)
    require(baseline.get("status") == "frozen_prospective", "generic baseline must be frozen prospectively", errors)
    require(baseline.get("reasoning_specific_primitives") == [], "generic baseline must contain no reasoning-specific primitives", errors)
    require(baseline.get("current_result") == "unresolved", "generic baseline result must remain unresolved before execution", errors)

    admission = scope.get("admission_rules", {})
    for key in (
        "positive_independent_of_fara",
        "positive_independent_of_candidate",
        "contrast_independent_of_fara_failure",
        "contrast_independent_of_candidate_absence",
    ):
        require(admission.get(key) is True, f"RCS-001 admission rule {key} must be true", errors)
    require(scope.get("execution_status") == "not_started", "RCS-001 execution must not be reported complete", errors)

    require(us_target.get("target_id") == "THM-US-TARGET-001", "universal target id mismatch", errors)
    require(us_target.get("status") == "frozen_prospective", "universal target must be frozen prospectively", errors)
    require(us_target.get("representation_track_implication") == "none", "representation track must have no automatic universal implication", errors)
    theorem_ids = {item.get("id") for item in us_target.get("theorem_families", [])}
    required_theorems = {
        "THM-US-EXIST-001",
        "THM-US-INV-001[K]",
        "THM-US-DISC-001[K]",
        "THM-US-NEC-001[K]",
        "THM-US-RED-001[K]",
        "THM-US-MIN-001",
        "THM-US-EQUIV-001",
        "THM-US-NO-001",
    }
    require(required_theorems <= theorem_ids, "universal target is missing theorem families", errors)

    require(w35.get("gate_id") == "W3.5-SDG-001", "W3.5 gate id mismatch", errors)
    require(w35.get("position") == "after_W3_before_W5", "W3.5 must be after W3 and before W5", errors)
    require(w35.get("W4_parallel_execution_allowed") is True, "W4 must remain allowed in parallel", errors)
    require(w35.get("W5_blocked_until_resolved") is True, "W5 must be blocked until W3.5 resolves", errors)
    require(w35.get("w5_authorized") is False, "W5 must not be authorized on freeze", errors)

    require(candidates.get("registry_id") == "US-CANDIDATES-001", "candidate registry id mismatch", errors)
    candidate_items = candidates.get("candidates", [])
    require(len(candidate_items) >= 10, "candidate registry must contain a broad initial hypothesis set", errors)
    require(all(item.get("current_classification") == "unresolved" for item in candidate_items), "candidate invariants may not be prejudged", errors)

    gates_by_name = {item.get("name"): item for item in gates.get("gates", [])}
    expected_gate_status = {
        "representation-discovery-separation": "satisfied",
        "generic-baseline-frozen": "satisfied",
        "universal-structure-target-frozen": "satisfied",
        "reasoning-contrast-scope-frozen": "satisfied",
        "baseline-factorization-resolved": "not_satisfied",
        "fara-specificity-resolved": "not_satisfied",
        "reasoning-contrast-execution": "not_satisfied",
        "universal-structure-result": "not_satisfied",
    }
    for name, status in expected_gate_status.items():
        require(name in gates_by_name, f"missing research gate {name}", errors)
        if name in gates_by_name:
            require(gates_by_name[name].get("status") == status, f"research gate {name} must be {status}", errors)

    policy = gates.get("claim_policy", {})
    for key in (
        "representation_does_not_imply_universal_structure",
        "common_schema_does_not_imply_reasoning_specificity",
        "finite_core_does_not_imply_general_universality",
        "w5_requires_w3_5_resolution",
        "dashboard_tracks_may_not_be_aggregated",
    ):
        require(policy.get(key) is True, f"claim_policy.{key} must be true", errors)

    require(target.get("program_track") == "REP", "THM-TARGET-001 must be classified as REP", errors)
    require(target.get("universal_structure_target") == "THM-US-TARGET-001", "THM-TARGET-001 must point to the separate universal target", errors)
    nonimplications = set(target.get("does_not_imply", []))
    require(
        {"reasoning_specificity", "universal_structure", "primitive_necessity", "minimality", "uniqueness"} <= nonimplications,
        "THM-TARGET-001 is missing mandatory non-implications",
        errors,
    )
    authorization = target.get("w5_authorization", {})
    require(authorization.get("authorized") is False, "W5 authorization must be false", errors)
    require(
        set(authorization.get("blocked_by", [])) >= {"OBS-SC-010", "W3.5-SDG-001"},
        "W5 authorization must be blocked by W4 and W3.5",
        errors,
    )

    claims_by_id = {item.get("id"): item for item in claims.get("claims", [])}
    for claim_id in ("CLM-REP-CAPACITY", "CLM-UNIVERSAL-STRUCTURE"):
        require(claim_id in claims_by_id, f"missing central claim {claim_id}", errors)
    if "CLM-REP-CAPACITY" in claims_by_id:
        require(claims_by_id["CLM-REP-CAPACITY"].get("track") == "REP", "representation-capacity claim must use REP track", errors)
        require(
            "CLM-UNIVERSAL-STRUCTURE" in claims_by_id["CLM-REP-CAPACITY"].get("does_not_imply", []),
            "representation-capacity claim must explicitly not imply universal structure",
            errors,
        )
    if "CLM-UNIVERSAL-STRUCTURE" in claims_by_id:
        require(claims_by_id["CLM-UNIVERSAL-STRUCTURE"].get("track") == "USD", "universal-structure claim must use USD track", errors)
        require(claims_by_id["CLM-UNIVERSAL-STRUCTURE"].get("current_status") == "unresolved", "universal-structure claim must remain unresolved", errors)

    standard_text = PATHS["standard"].read_text(encoding="utf-8")
    central_text = PATHS["central"].read_text(encoding="utf-8")
    proof_text = PATHS["proof_roadmap"].read_text(encoding="utf-8")
    neutral_text = PATHS["neutral_roadmap"].read_text(encoding="utf-8")
    readme_text = PATHS["readme"].read_text(encoding="utf-8")
    makefile_text = PATHS["makefile"].read_text(encoding="utf-8")
    task_text = PATHS["task_generator"].read_text(encoding="utf-8")
    status_text = PATHS["status_generator"].read_text(encoding="utf-8")
    dashboard_text = PATHS["dashboard_generator"].read_text(encoding="utf-8")

    require("faithful representation" in standard_text and "universal structure" in standard_text, "separation standard lacks core non-implication", errors)
    require("W3.5" in central_text and "representation track" in central_text.lower(), "central program must contain W3.5 and track separation", errors)
    require(proof_text.find("W3.5") < proof_text.find("W5"), "proof roadmap must place W3.5 before W5", errors)
    require("THM-US-TARGET-001" in neutral_text, "architecture-neutral roadmap must include the universal target", errors)
    require("W3.5" in readme_text and "universal-structure discovery" in readme_text.lower(), "README must expose W3.5 and discovery status", errors)
    require(makefile_text.count("python tools/check_representation_discovery_separation.py") == 3, "separation checker must run in health, health-fast, and research-check", errors)
    for name, text in (
        ("task generator", task_text),
        ("status generator", status_text),
        ("dashboard generator", dashboard_text),
    ):
        require("W3.5" in text, f"{name} must preserve W3.5 status", errors)
        require("W5" in text and "block" in text.lower(), f"{name} must preserve the W5 block", errors)

    if errors:
        print("Representation-discovery separation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Representation-discovery separation PASS "
        "(W0-W3 preserved as REP; W3.5 frozen; W4 parallel; W5 blocked; USD target unresolved)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
