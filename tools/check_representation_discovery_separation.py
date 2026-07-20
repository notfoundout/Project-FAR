#!/usr/bin/env python3
"""Enforce separation between finite representation results and universal-structure discovery."""
from __future__ import annotations

import hashlib
import json
import re
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
    "ledger": ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json",
    "central": ROOT / "docs/governance/central-research-program.md",
    "proof_roadmap": ROOT / "docs/planning/deduction-first-proof-roadmap.md",
    "neutral_roadmap": ROOT / "docs/planning/architecture-neutral-research-roadmap.md",
    "readme": ROOT / "README.md",
    "makefile": ROOT / "Makefile",
    "task_generator": ROOT / "tools/generate_next_tasks.py",
    "status_generator": ROOT / "tools/project_status_report.py",
    "dashboard_generator": ROOT / "tools/update_readme_dashboard.py",
}

TERMINAL_OBLIGATION_STATUSES = {
    "proved",
    "refuted",
    "obstruction_established",
    "scope_boundary_established",
    "superseded",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def gate_map(gates: dict) -> dict[str, dict]:
    return {item.get("name"): item for item in gates.get("gates", [])}


def obligation_map(ledger: dict) -> dict[str, dict]:
    return {item.get("id"): item for item in ledger.get("obligations", [])}


def authorization_errors(
    w35: dict,
    target: dict,
    scope: dict,
    gates: dict,
    ledger: dict,
    root: Path = ROOT,
) -> list[str]:
    """Return W5 authorization errors.

    The current frozen state is valid while both authorization flags are false.
    Once either flag is true, every evidence and dependency condition is mandatory.
    """
    errors: list[str] = []
    w35_authorized = w35.get("w5_authorized") is True
    target_authorized = target.get("w5_authorization", {}).get("authorized") is True

    if not (w35_authorized or target_authorized):
        require(
            set(target.get("w5_authorization", {}).get("blocked_by", []))
            >= {"OBS-SC-010", "W3.5-SDG-001"},
            "unauthorized W5 state must retain both W4 and W3.5 blockers",
            errors,
        )
        return errors

    require(w35_authorized and target_authorized, "W5 authorization flags must agree", errors)
    require(w35.get("status") == "resolved", "W3.5 status must be resolved", errors)

    obs = obligation_map(ledger).get("OBS-SC-010", {})
    require(
        obs.get("status") in TERMINAL_OBLIGATION_STATUSES,
        "OBS-SC-010 must have a terminal ledger status",
        errors,
    )
    require(
        scope.get("concrete_corpus_status") == "frozen",
        "the concrete reasoning and contrast corpus must be frozen",
        errors,
    )
    require(scope.get("positive_instances"), "positive instance registry must be nonempty", errors)
    require(scope.get("contrast_instances"), "contrast instance registry must be nonempty", errors)

    dimensions = w35.get("current_results", {}).get("factorization", {})
    allowed_dimensions = w35.get("factorization_result_dimensions", {})
    for dimension, allowed in allowed_dimensions.items():
        value = dimensions.get(dimension)
        require(value in allowed, f"factorization dimension {dimension} has invalid value", errors)
        require(value != "unresolved", f"factorization dimension {dimension} remains unresolved", errors)

    require(
        w35.get("current_results", {}).get("fara_specificity")
        not in {None, "unresolved", "not_executed"},
        "FARA-specificity remains unresolved",
        errors,
    )
    require(
        w35.get("current_results", {}).get("reasoning_discrimination") == "complete",
        "reasoning/contrast discrimination must be complete",
        errors,
    )
    require(
        w35.get("current_results", {}).get("candidate_invariants") == "complete",
        "candidate-invariant classification must be complete",
        errors,
    )
    require(
        w35.get("current_results", {}).get("machinery_and_cost") == "complete",
        "machinery and cost accounting must be complete",
        errors,
    )

    artifacts = w35.get("required_result_artifacts", [])
    require(bool(artifacts), "W3.5 required result artifact list is empty", errors)
    for artifact in artifacts:
        label = artifact.get("id", "<missing-id>")
        require(artifact.get("status") == "complete", f"{label} is not complete", errors)
        path = artifact.get("path")
        require(isinstance(path, str) and bool(path), f"{label} lacks a path", errors)
        require(
            isinstance(artifact.get("artifact_id"), str) and bool(artifact.get("artifact_id")),
            f"{label} lacks an immutable artifact id",
            errors,
        )
        digest = artifact.get("content_sha256")
        require(isinstance(digest, str) and HEX64.fullmatch(digest) is not None, f"{label} lacks a valid SHA-256 digest", errors)
        if isinstance(path, str) and path:
            full_path = root / path
            require(full_path.is_file(), f"{label} artifact path does not exist: {path}", errors)
            if full_path.is_file() and isinstance(digest, str) and HEX64.fullmatch(digest):
                actual = hashlib.sha256(full_path.read_bytes()).hexdigest()
                require(actual == digest, f"{label} SHA-256 digest does not match its artifact", errors)

    gates_by_name = gate_map(gates)
    for name in w35.get("authorization_contract", {}).get(
        "requires_research_gates_satisfied_with_evidence", []
    ):
        gate = gates_by_name.get(name, {})
        require(gate.get("status") == "satisfied", f"research gate {name} is not satisfied", errors)
        require(bool(gate.get("evidence")), f"research gate {name} lacks evidence", errors)

    require(
        target.get("w5_authorization", {}).get("blocked_by") == [],
        "authorized W5 state must clear target blockers",
        errors,
    )
    require(bool(w35.get("authorization_evidence")), "W3.5 authorization evidence is empty", errors)
    return errors


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
    ledger = load(PATHS["ledger"])

    require(baseline.get("baseline_id") == "GREL-001", "generic baseline id must be GREL-001", errors)
    require(baseline.get("status") == "frozen_prospective", "generic baseline must be frozen prospectively", errors)
    require(baseline.get("reasoning_specific_primitives") == [], "generic baseline must contain no reasoning-specific primitives", errors)
    require(baseline.get("single_scalar_classification_prohibited") is True, "factorization may not collapse to one scalar", errors)
    dimensions = baseline.get("result_dimensions", {})
    current = baseline.get("current_result", {})
    required_dimensions = {
        "expressiveness",
        "translation",
        "constraint_strength",
        "reasoning_specificity",
        "cost_relation",
        "overall_interpretation",
    }
    require(set(dimensions) == required_dimensions, "generic baseline result dimensions are incomplete", errors)
    require(set(current) == required_dimensions, "generic baseline current result dimensions are incomplete", errors)
    require(all(current.get(name) == "unresolved" for name in required_dimensions), "generic baseline results must remain unresolved before execution", errors)

    admission = scope.get("admission_rules", {})
    for key in (
        "positive_independent_of_fara",
        "positive_independent_of_candidate",
        "contrast_independent_of_fara_failure",
        "contrast_independent_of_candidate_absence",
        "admission_decision_must_precede_candidate_scoring",
    ):
        require(admission.get(key) is True, f"RCS-001 admission rule {key} must be true", errors)
    require(scope.get("framework_frozen") is True, "RCS-001 admission framework must be frozen", errors)
    require(scope.get("concrete_corpus_status") == "not_frozen", "RCS-001 concrete corpus must remain unfrozen on creation", errors)
    require(scope.get("positive_instances") == [], "RCS-001 positive instance registry must start empty", errors)
    require(scope.get("contrast_instances") == [], "RCS-001 contrast instance registry must start empty", errors)
    require(
        scope.get("execution_status") == "blocked_until_concrete_corpus_frozen",
        "RCS-001 execution must remain blocked until corpus freeze",
        errors,
    )

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
    require(w35.get("factorization_result_dimensions") == dimensions, "W3.5 dimensions must match GREL-001", errors)
    required_artifacts = w35.get("required_result_artifacts", [])
    require(len(required_artifacts) >= 8, "W3.5 must register all required result artifacts", errors)
    for artifact in required_artifacts:
        require(set(artifact) >= {"id", "kind", "status", "path", "artifact_id", "content_sha256"}, "W3.5 artifact record is incomplete", errors)
        require(artifact.get("status") == "missing", "prospective W3.5 artifacts must start missing", errors)

    require(candidates.get("registry_id") == "US-CANDIDATES-001", "candidate registry id mismatch", errors)
    candidate_items = candidates.get("candidates", [])
    require(len(candidate_items) >= 10, "candidate registry must contain a broad initial hypothesis set", errors)
    require(all(item.get("current_classification") == "unresolved" for item in candidate_items), "candidate invariants may not be prejudged", errors)

    gates_by_name = gate_map(gates)
    expected_gate_status = {
        "representation-discovery-separation": "satisfied",
        "generic-baseline-frozen": "satisfied",
        "universal-structure-target-frozen": "satisfied",
        "reasoning-contrast-scope-framework-frozen": "satisfied",
        "reasoning-contrast-corpus-frozen": "not_satisfied",
        "baseline-factorization-resolved": "not_satisfied",
        "fara-specificity-resolved": "not_satisfied",
        "reasoning-contrast-execution": "not_satisfied",
        "universal-structure-result": "not_satisfied",
    }
    for name, status in expected_gate_status.items():
        require(name in gates_by_name, f"missing research gate {name}", errors)
        if name in gates_by_name:
            require(gates_by_name[name].get("status") == status, f"research gate {name} must be {status}", errors)
    require("reasoning-contrast-scope-frozen" not in gates_by_name, "ambiguous concrete scope-frozen gate must not remain", errors)

    policy = gates.get("claim_policy", {})
    for key in (
        "representation_does_not_imply_universal_structure",
        "common_schema_does_not_imply_reasoning_specificity",
        "finite_core_does_not_imply_general_universality",
        "w5_requires_w3_5_resolution",
        "dashboard_tracks_may_not_be_aggregated",
        "concrete_scope_requires_registered_instances",
        "w5_authorization_requires_linked_immutable_evidence",
        "factorization_dimensions_may_not_be_collapsed",
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
    for theorem_id in ("THM-CORE-COMMON-001", "THM-CORE-REP-001", "THM-IMP-001"):
        theorem = next((item for item in target.get("theorem_family", []) if item.get("id") == theorem_id), {})
        require(
            "specificity_discovery_bridge" in theorem.get("blocked_by", []),
            f"{theorem_id} must be blocked by the specificity/discovery bridge",
            errors,
        )

    errors.extend(authorization_errors(w35, target, scope, gates, ledger, ROOT))

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
        "(REP isolated; RCS framework frozen; corpus open; dimensioned W3.5; W5 evidence-blocked)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
