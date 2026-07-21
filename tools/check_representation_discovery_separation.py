#!/usr/bin/env python3
"""Enforce separation between bounded representation results and universal-structure discovery."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from check_w3_5_candidate_tests import validate as validate_candidates
from check_w3_5_corpus_freeze import validate as validate_corpus
from check_w3_5_factorization import validate as validate_factorization
from check_w3_5_specificity import validate as validate_specificity

ROOT = Path(__file__).resolve().parents[1]
PATHS = {
    "standard": ROOT / "docs/governance/representation-discovery-separation-standard-v1.0.md",
    "baseline_doc": ROOT / "docs/research/generic-relational-baseline-v1.0.md",
    "baseline": ROOT / "theory/evaluation/generic-relational-baseline-v1.0.json",
    "scope_doc": ROOT / "docs/research/reasoning-and-contrast-scope-v1.0.md",
    "scope": ROOT / "theory/evaluation/reasoning-and-contrast-scope-v1.0.json",
    "corpus_doc": ROOT / "docs/research/w3-5-concrete-corpus-freeze-v1.0.md",
    "corpus_result": ROOT / "theory/evaluation/w3-5-corpus-freeze-result-v1.0.json",
    "factor_doc": ROOT / "docs/research/w3-5-grel-fara-factorization-v1.0.md",
    "factor_result": ROOT / "theory/evaluation/w3-5-factorization-result-v1.0.json",
    "specificity_doc": ROOT / "docs/research/w3-5-reasoning-discrimination-and-specificity-v1.0.md",
    "discrimination_result": ROOT / "theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json",
    "specificity_result": ROOT / "theory/evaluation/w3-5-fara-specificity-result-v1.0.json",
    "candidate_doc": ROOT / "docs/research/w3-5-candidate-ablation-and-reconstruction-v1.0.md",
    "candidate_result": ROOT / "theory/evaluation/w3-5-candidate-test-result-v1.0.json",
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
TERMINAL = {"proved", "refuted", "obstruction_established", "scope_boundary_established", "superseded"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DIMS = {"expressiveness", "translation", "constraint_strength", "reasoning_specificity", "cost_relation", "overall_interpretation"}
EXPECTED_FACTOR = {
    "expressiveness": "equivalent",
    "translation": "bidirectional",
    "constraint_strength": "fara_stricter",
    "reasoning_specificity": "not_established",
    "cost_relation": "tradeoff",
    "overall_interpretation": "fara_constrained_equivalent",
}
EXPECTED_CANDIDATE_COUNTS = {
    "derivable": 6,
    "replaceable": 1,
    "architecture_dependent": 1,
    "scope_dependent": 1,
    "generic_system_property": 3,
}
EXPECTED_CANDIDATE_AGGREGATE = "no_registered_candidate_indispensable_within_frozen_class"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(ok: bool, message: str, errors: list[str]) -> None:
    if not ok:
        errors.append(message)


def gate_map(gates: dict) -> dict:
    return {item.get("name"): item for item in gates.get("gates", [])}


def obligation_map(ledger: dict) -> dict:
    return {item.get("id"): item for item in ledger.get("obligations", [])}


def authorization_errors(w35: dict, target: dict, scope: dict, gates: dict, ledger: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    w35_authorized = w35.get("w5_authorized") is True
    target_authorized = target.get("w5_authorization", {}).get("authorized") is True
    obstruction = obligation_map(ledger).get("OBS-SC-010", {})
    obstruction_terminal = obstruction.get("status") in TERMINAL
    blockers = set(target.get("w5_authorization", {}).get("blocked_by", []))

    if not (w35_authorized or target_authorized):
        require("W3.5-SDG-001" in blockers, "unauthorized W5 state must retain W3.5-SDG-001", errors)
        require(("OBS-SC-010" not in blockers) if obstruction_terminal else ("OBS-SC-010" in blockers), "OBS-SC-010 blocker state is inconsistent", errors)
        return errors

    require(w35_authorized and target_authorized, "W5 authorization flags must agree", errors)
    require(w35.get("status") == "resolved", "W3.5 status must be resolved", errors)
    require(obstruction_terminal, "OBS-SC-010 must have a terminal ledger status", errors)
    require(scope.get("concrete_corpus_status") == "frozen", "the concrete reasoning and contrast corpus must be frozen", errors)
    require(bool(scope.get("positive_instances")), "positive instance registry must be nonempty", errors)
    require(bool(scope.get("contrast_instances")), "contrast instance registry must be nonempty", errors)

    current = w35.get("current_results", {})
    dimensions = current.get("factorization", {})
    allowed = w35.get("factorization_result_dimensions", {})
    for dimension, options in allowed.items():
        value = dimensions.get(dimension)
        require(value in options, f"factorization dimension {dimension} has invalid value", errors)
        require(value != "unresolved", f"factorization dimension {dimension} remains unresolved", errors)
    require(current.get("fara_specificity") not in {None, "unresolved", "not_executed"}, "fara_specificity must be terminal", errors)
    require(current.get("reasoning_discrimination") not in {None, "unresolved", "not_executed"}, "reasoning_discrimination must be terminal", errors)
    require(current.get("candidate_invariants") == "complete_no_indispensable_candidate", "candidate_invariants must be complete", errors)
    require(current.get("machinery_and_cost") == "complete", "machinery_and_cost must be complete", errors)

    artifacts = w35.get("required_result_artifacts", [])
    require(bool(artifacts), "W3.5 required result artifact list is empty", errors)
    for artifact in artifacts:
        label = artifact.get("id", "<missing-id>")
        require(artifact.get("status") == "complete", f"{label} is not complete", errors)
        path = artifact.get("path")
        digest = artifact.get("content_sha256")
        require(isinstance(path, str) and bool(path), f"{label} lacks a path", errors)
        require(isinstance(artifact.get("artifact_id"), str) and bool(artifact.get("artifact_id")), f"{label} lacks an immutable artifact id", errors)
        require(isinstance(digest, str) and HEX64.fullmatch(digest) is not None, f"{label} lacks a valid SHA-256 digest", errors)
        if isinstance(path, str) and path:
            file_path = root / path
            require(file_path.is_file(), f"{label} artifact path does not exist: {path}", errors)
            if file_path.is_file() and isinstance(digest, str) and HEX64.fullmatch(digest):
                require(hashlib.sha256(file_path.read_bytes()).hexdigest() == digest, f"{label} SHA-256 digest does not match its artifact", errors)

    gates_by_name = gate_map(gates)
    for name in w35.get("authorization_contract", {}).get("requires_research_gates_satisfied_with_evidence", []):
        require(gates_by_name.get(name, {}).get("status") == "satisfied", f"research gate {name} is not satisfied", errors)
        require(bool(gates_by_name.get(name, {}).get("evidence")), f"research gate {name} lacks evidence", errors)
    require(target.get("w5_authorization", {}).get("blocked_by") == [], "authorized W5 state must clear target blockers", errors)
    require(bool(w35.get("authorization_evidence")), "W3.5 authorization evidence is empty", errors)
    return errors


def main() -> int:
    errors: list[str] = []
    for name, path in PATHS.items():
        require(path.is_file(), f"missing {name}: {path.relative_to(ROOT)}", errors)
    if errors:
        return report(errors)

    baseline = load(PATHS["baseline"])
    scope = load(PATHS["scope"])
    corpus = load(PATHS["corpus_result"])
    factor = load(PATHS["factor_result"])
    discrimination = load(PATHS["discrimination_result"])
    specificity = load(PATHS["specificity_result"])
    candidate_result = load(PATHS["candidate_result"])
    universal_target = load(PATHS["us_target"])
    w35 = load(PATHS["w35"])
    candidates = load(PATHS["candidates"])
    gates = load(PATHS["gates"])
    claims = load(PATHS["claims"])
    target = load(PATHS["target"])
    ledger = load(PATHS["ledger"])

    require(baseline.get("baseline_id") == "GREL-001", "generic baseline id must be GREL-001", errors)
    require(baseline.get("status") == "factorization_complete", "generic baseline must record completed factorization", errors)
    require(baseline.get("reasoning_specific_primitives") == [], "generic baseline must contain no reasoning-specific primitives", errors)
    require(baseline.get("single_scalar_classification_prohibited") is True, "factorization may not collapse to one scalar", errors)
    dimensions = baseline.get("result_dimensions", {})
    current_factor = baseline.get("current_result", {})
    require(set(dimensions) == DIMS, "generic baseline result dimensions are incomplete", errors)
    require(set(current_factor) == DIMS, "generic baseline current result dimensions are incomplete", errors)
    require(current_factor == EXPECTED_FACTOR, "generic baseline factorization results differ from frozen result", errors)
    require(factor.get("artifact_id") == "W35-FACTOR-RESULT-001" and factor.get("status") == "complete", "factorization result must be complete", errors)
    require(factor.get("dimensions") == EXPECTED_FACTOR, "factorization result dimensions changed", errors)
    require(factor.get("factorization_contract", {}).get("primitive_reduction_established") is False, "factorization must not be promoted to primitive reduction", errors)
    require(validate_factorization(ROOT).get("status") == "pass", "factorization validation failed", errors)

    require(discrimination.get("artifact_id") == "W35-SCOPE-RESULT-001" and discrimination.get("status") == "complete", "reasoning discrimination result must be complete", errors)
    require(specificity.get("artifact_id") == "W35-SPEC-RESULT-001" and specificity.get("status") == "complete_qualified_negative", "specificity result must remain a qualified negative", errors)
    require(specificity.get("result", {}).get("unique_discriminative_capacity_of_fara") == "refuted_at_registered_scope", "FARA uniqueness must remain refuted at registered scope", errors)
    require(specificity.get("result", {}).get("fara_reasoning_specificity_general") == "not_established", "general FARA specificity must remain unestablished", errors)
    require(specificity.get("result", {}).get("fara_primitive_necessity") == "not_established", "FARA primitive necessity must remain unestablished", errors)
    require(validate_specificity(ROOT).get("status") == "pass", "specificity validation failed", errors)

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
    require(scope.get("concrete_corpus_status") == "frozen", "RCS-001 concrete corpus must be frozen", errors)
    require(scope.get("concrete_corpus_id") == "RCS-CORPUS-001", "RCS-001 concrete corpus id mismatch", errors)
    require(len(scope.get("positive_instances", [])) == 8, "RCS-001 positive registry must contain eight frozen instances", errors)
    require(len(scope.get("contrast_instances", [])) == 8, "RCS-001 contrast registry must contain eight frozen instances", errors)
    require(len(scope.get("disputed_instances", [])) == 2, "RCS-001 disputed registry must preserve two cases", errors)
    require(scope.get("execution_status") == "ready_for_candidate_neutral_execution", "RCS-001 frozen registry execution status changed", errors)
    require(scope.get("candidate_scoring_status") == "not_started", "RCS-001 freeze metadata must preserve pre-scoring state", errors)
    require(corpus.get("status") == "complete", "RCS-CORPUS-001 freeze result must be complete", errors)
    require(corpus.get("claim_impact", {}).get("W5_authorized") is False, "corpus freeze may not authorize W5", errors)
    errors.extend(validate_corpus(ROOT))

    require(candidate_result.get("artifact_id") == "W35-CANDIDATE-RESULT-001", "candidate-result identity changed", errors)
    require(candidate_result.get("status") == "complete", "candidate-result artifact must be complete", errors)
    require(candidate_result.get("classification_counts") == EXPECTED_CANDIDATE_COUNTS, "candidate classification counts changed", errors)
    require(candidate_result.get("aggregate_result") == EXPECTED_CANDIDATE_AGGREGATE, "candidate aggregate result changed", errors)
    require(candidate_result.get("claim_effect", {}).get("universal_structure") == "unresolved", "candidate result promoted universal structure", errors)
    require(candidate_result.get("claim_effect", {}).get("W5_authorized") is False, "candidate result authorized W5", errors)
    require(validate_candidates(ROOT).get("status") == "pass", "candidate validation failed", errors)

    require(universal_target.get("target_id") == "THM-US-TARGET-001", "universal target id mismatch", errors)
    require(universal_target.get("status") == "frozen_prospective", "universal target must be frozen prospectively", errors)
    require(universal_target.get("representation_track_implication") == "none", "REP must have no automatic USD implication", errors)
    required_theorems = {"THM-US-EXIST-001", "THM-US-INV-001[K]", "THM-US-DISC-001[K]", "THM-US-NEC-001[K]", "THM-US-RED-001[K]", "THM-US-MIN-001", "THM-US-EQUIV-001", "THM-US-NO-001"}
    require(required_theorems <= {item.get("id") for item in universal_target.get("theorem_families", [])}, "universal target is missing theorem families", errors)
    require(all(item.get("status") != "proved" for item in universal_target.get("theorem_families", [])), "candidate execution may not prove a universal theorem", errors)

    require(w35.get("gate_id") == "W3.5-SDG-001", "W3.5 gate id mismatch", errors)
    require(w35.get("position") == "after_W3_before_W5", "W3.5 must be after W3 and before W5", errors)
    require(w35.get("status") == "in_progress_candidate_complete", "W3.5 status must record candidate-complete progress only", errors)
    require(w35.get("W5_blocked_until_resolved") is True, "W5 must be blocked until W3.5 resolves", errors)
    require(w35.get("w5_authorized") is False, "W5 must not be authorized", errors)
    require(w35.get("factorization_result_dimensions") == dimensions, "W3.5 dimensions must match GREL-001", errors)
    require(w35.get("current_results", {}).get("factorization") == EXPECTED_FACTOR, "W3.5 factorization result changed", errors)

    artifacts = w35.get("required_result_artifacts", [])
    require(len(artifacts) >= 8, "W3.5 must register required artifacts", errors)
    for artifact in artifacts:
        require(set(artifact) >= {"id", "kind", "status", "path", "artifact_id", "content_sha256"}, "W3.5 artifact record is incomplete", errors)
    artifact_map = {artifact.get("id"): artifact for artifact in artifacts}
    completed = {"W35-CORPUS-RESULT", "W35-FACTOR-RESULT", "W35-SCOPE-RESULT", "W35-SPEC-RESULT", "W35-CANDIDATE-RESULT"}
    for artifact_id in completed:
        artifact = artifact_map.get(artifact_id, {})
        require(artifact.get("status") == "complete", f"{artifact_id} must be complete", errors)
        require(isinstance(artifact.get("path"), str) and bool(artifact.get("path")), f"{artifact_id} lacks a path", errors)
        require(isinstance(artifact.get("artifact_id"), str) and bool(artifact.get("artifact_id")), f"{artifact_id} lacks an immutable artifact id", errors)
        require(isinstance(artifact.get("content_sha256"), str) and HEX64.fullmatch(artifact.get("content_sha256")) is not None, f"{artifact_id} lacks a valid digest", errors)
    for artifact_id in ("W35-COST-RESULT", "W35-CLAIM-RESULT", "W35-FAILURE-RESULT"):
        require(artifact_map.get(artifact_id, {}).get("status") == "missing", f"{artifact_id} must remain missing", errors)

    current = w35.get("current_results", {})
    require(current.get("reasoning_contrast_corpus") == "frozen", "W3.5 corpus result must be frozen", errors)
    require(current.get("reasoning_discrimination") == "bounded_role_conjunctive_discrimination_established", "reasoning discrimination result changed", errors)
    require(current.get("fara_specificity") == "not_unique_at_registered_scope", "FARA specificity result changed", errors)
    require(current.get("candidate_invariants") == "complete_no_indispensable_candidate", "candidate invariants must record completed bounded negative result", errors)
    require(current.get("machinery_and_cost") == "not_executed", "machinery and cost must remain unexecuted", errors)

    require(candidates.get("registry_id") == "US-CANDIDATES-001", "candidate registry id mismatch", errors)
    candidate_items = candidates.get("candidates", [])
    require(len(candidate_items) == 12, "candidate registry must contain twelve executed hypotheses", errors)
    require(all(item.get("current_classification") in EXPECTED_CANDIDATE_COUNTS for item in candidate_items), "candidate registry contains a nonterminal or unauthorized classification", errors)
    require(all(item.get("current_classification") != "indispensable_within_frozen_class" for item in candidate_items), "candidate indispensability was inflated", errors)
    require(candidates.get("aggregate_result") == EXPECTED_CANDIDATE_AGGREGATE, "candidate registry aggregate differs from result", errors)

    gates_by_name = gate_map(gates)
    expected_gates = {
        "representation-discovery-separation": "satisfied",
        "generic-baseline-frozen": "satisfied",
        "universal-structure-target-frozen": "satisfied",
        "reasoning-contrast-scope-framework-frozen": "satisfied",
        "reasoning-contrast-corpus-frozen": "satisfied",
        "baseline-factorization-resolved": "satisfied",
        "fara-specificity-resolved": "satisfied",
        "reasoning-contrast-execution": "satisfied",
        "universal-structure-result": "not_satisfied",
        "formal-negative-controls": "satisfied",
    }
    for name, status in expected_gates.items():
        require(gates_by_name.get(name, {}).get("status") == status, f"research gate {name} must be {status}", errors)
    for name in ("baseline-factorization-resolved", "fara-specificity-resolved", "reasoning-contrast-execution"):
        require(bool(gates_by_name.get(name, {}).get("evidence")), f"{name} must have evidence", errors)
    require("reasoning-contrast-scope-frozen" not in gates_by_name, "ambiguous scope-frozen gate must not remain", errors)

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
        "registered_nontriviality_does_not_imply_fara_specificity",
    ):
        require(policy.get(key) is True, f"claim_policy.{key} must be true", errors)

    require(target.get("program_track") == "REP", "THM-TARGET-001 must be REP", errors)
    require(target.get("universal_structure_target") == "THM-US-TARGET-001", "REP target must point to USD target", errors)
    require({"reasoning_specificity", "universal_structure", "primitive_necessity", "minimality", "uniqueness"} <= set(target.get("does_not_imply", [])), "REP target lacks non-implications", errors)
    for theorem_id in ("THM-CORE-COMMON-001", "THM-CORE-REP-001", "THM-IMP-001"):
        theorem = next((item for item in target.get("theorem_family", []) if item.get("id") == theorem_id), {})
        require("specificity_discovery_bridge" in theorem.get("blocked_by", []), f"{theorem_id} must remain blocked by incomplete W3.5", errors)
    errors.extend(authorization_errors(w35, target, scope, gates, ledger, ROOT))

    claims_by_id = {item.get("id"): item for item in claims.get("claims", [])}
    require("CLM-UNIVERSAL-STRUCTURE" in claims_by_id.get("CLM-REP-CAPACITY", {}).get("does_not_imply", []), "REP claim must not imply USD", errors)
    require(claims_by_id.get("CLM-UNIVERSAL-STRUCTURE", {}).get("track") == "USD", "universal claim must use USD", errors)
    require(claims_by_id.get("CLM-UNIVERSAL-STRUCTURE", {}).get("current_status") == "unresolved", "universal claim must remain unresolved", errors)

    standard = PATHS["standard"].read_text(encoding="utf-8")
    central = PATHS["central"].read_text(encoding="utf-8")
    proof = PATHS["proof_roadmap"].read_text(encoding="utf-8")
    neutral = PATHS["neutral_roadmap"].read_text(encoding="utf-8")
    readme = PATHS["readme"].read_text(encoding="utf-8")
    makefile = PATHS["makefile"].read_text(encoding="utf-8")
    require("faithful representation" in standard and "universal structure" in standard, "separation standard lacks non-implication", errors)
    require("W3.5" in central and "representation track" in central.lower(), "central program lacks track separation", errors)
    require(proof.find("W3.5") < proof.find("W5"), "proof roadmap must place W3.5 before W5", errors)
    require("THM-US-TARGET-001" in neutral, "neutral roadmap lacks USD target", errors)
    require("W3.5" in readme and "universal-structure discovery" in readme.lower(), "README lacks W3.5/USD", errors)
    require(makefile.count("python tools/check_representation_discovery_separation.py") == 3, "separation checker must run three times", errors)
    require(makefile.count("python tools/check_w3_5_corpus_freeze.py") == 3, "corpus-freeze checker must run three times", errors)
    require(makefile.count("python tools/check_w3_5_factorization.py") == 3, "factorization checker must run three times", errors)
    require(makefile.count("python tools/check_w3_5_specificity.py") == 3, "specificity checker must run three times", errors)
    require(makefile.count("python tools/check_w3_5_candidate_tests.py") == 3, "candidate checker must run three times", errors)
    for name, path in (("task generator", PATHS["task_generator"]), ("status generator", PATHS["status_generator"]), ("dashboard generator", PATHS["dashboard_generator"])):
        text = path.read_text(encoding="utf-8")
        require("W3.5" in text, f"{name} must preserve W3.5", errors)
        require("W5" in text and "block" in text.lower(), f"{name} must preserve W5 block", errors)
    return report(errors)


def report(errors: list[str]) -> int:
    if errors:
        print("Representation-discovery separation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Representation-discovery separation PASS (REP isolated; corpus, factorization, specificity, and registered candidates complete; no indispensable candidate; W5 blocked; USD unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
