#!/usr/bin/env python3
"""Validate Project FAR research gates and claim boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/research-gates.json"
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"

ALLOWED_GATE_STATUS = {"not_satisfied", "in_progress", "satisfied", "blocked", "retired"}
ALLOWED_CLAIM_STATUS = {
    "unresolved",
    "partially_supported",
    "supported_at_registered_control_scope",
    "not_established",
    "not_established_generally",
    "supported",
    "weakened",
    "refuted",
}
REQUIRED_GATE_NAMES = {
    "external-observation-contract",
    "negative-controls",
    "full-cost-accounting",
    "anti-reintroduction-ablation",
    "independent-replication",
    "private-holdout-counterexample-challenge",
    "nonclaim-audit",
    "formal-theorem-target",
    "premise-ledger-and-semantics",
    "faithful-representation-definition",
    "scoped-representation-proof",
    "primitive-lower-bounds",
    "minimality-universe-and-proof",
    "mechanized-proof-verification",
    "independent-proof-review",
    "representation-discovery-separation",
    "generic-baseline-frozen",
    "universal-structure-target-frozen",
    "reasoning-contrast-scope-framework-frozen",
    "reasoning-contrast-corpus-frozen",
    "baseline-factorization-resolved",
    "fara-specificity-resolved",
    "reasoning-contrast-execution",
    "universal-structure-result",
    "formal-negative-controls",
}
REQUIRED_CLAIM_IDS = {
    "CLM-REP-CAPACITY",
    "CLM-UNIVERSAL-STRUCTURE",
    "CLM-EXISTENCE",
    "CLM-SUFFICIENCY",
    "CLM-UNIVERSALITY",
    "CLM-NECESSITY",
    "CLM-MINIMALITY",
    "CLM-NONTRIVIALITY",
    "CLM-ECONOMY",
    "CLM-INDEPENDENCE",
}
REQUIRED_POLICY_TRUE = {
    "unsatisfied_gate_blocks_stronger_claim",
    "unknown_is_not_pass",
    "internal_multi_implementation_is_not_external_independence",
    "theory_change_after_freeze_creates_new_version",
    "failed_frozen_results_are_immutable",
    "tradeoffs_must_not_be_reported_as_wins",
    "satisfied_gate_requires_evidence",
    "central_claim_updates_require_registry_change",
    "proof_construction_not_blocked_by_empirical_replication",
    "independent_replication_gates_only_independent_empirical_confirmation",
    "theorem_claim_requires_explicit_assumptions_and_scope",
    "experimental_evidence_is_not_deductive_proof",
    "mechanization_does_not_validate_axioms",
    "independent_review_is_separate_claim_dimension",
    "representation_does_not_imply_universal_structure",
    "common_schema_does_not_imply_reasoning_specificity",
    "finite_core_does_not_imply_general_universality",
    "w5_requires_w3_5_resolution",
    "dashboard_tracks_may_not_be_aggregated",
    "concrete_scope_requires_registered_instances",
    "w5_authorization_requires_linked_immutable_evidence",
    "factorization_dimensions_may_not_be_collapsed",
    "formal_negative_controls_do_not_satisfy_empirical_negative_controls",
    "registered_nontriviality_does_not_imply_fara_specificity",
}
REQUIRED_UPDATE_POLICY_TRUE = {
    "evidence_for_and_against_required",
    "unknown_is_not_pass",
    "failures_are_immutable",
    "scope_changes_must_be_versioned",
    "stronger_status_requires_linked_artifacts",
    "theorem_and_replication_status_must_remain_separate",
    "experimental_results_may_not_be_promoted_to_proof",
    "proof_claims_require_explicit_assumptions_and_scope",
    "representation_progress_may_not_update_universal_structure_status",
    "track_statuses_may_not_be_aggregated",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    for path in (REGISTRY, CLAIMS):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        return report(errors)

    data = load(REGISTRY)
    claims_data = load(CLAIMS)
    if data.get("schema_version") != "1.0":
        errors.append("research gate schema_version must equal 1.0")
    if data.get("research_mode") != "deduction_first_with_parallel_empirical_validation":
        errors.append("research_mode mismatch")

    artifacts = data.get("required_canonical_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("required_canonical_artifacts must be a nonempty list")
        artifacts = []
    for relative in artifacts:
        if not isinstance(relative, str) or not relative:
            errors.append("invalid canonical artifact path")
        elif not (ROOT / relative).is_file():
            errors.append(f"missing canonical artifact: {relative}")

    gates = data.get("gates")
    if not isinstance(gates, list):
        errors.append("gates must be a list")
        gates = []
    ids: set[str] = set()
    names: set[str] = set()
    by_name: dict[str, dict] = {}
    for gate in gates:
        if not isinstance(gate, dict):
            errors.append("every gate must be an object")
            continue
        gate_id = gate.get("id")
        name = gate.get("name")
        if not isinstance(gate_id, str) or not gate_id:
            errors.append("gate requires id")
        elif gate_id in ids:
            errors.append(f"duplicate gate id: {gate_id}")
        else:
            ids.add(gate_id)
        if not isinstance(name, str) or not name:
            errors.append(f"gate {gate_id} requires name")
            continue
        if name in names:
            errors.append(f"duplicate gate name: {name}")
        names.add(name)
        by_name[name] = gate
        if gate.get("status") not in ALLOWED_GATE_STATUS:
            errors.append(f"gate {name} has invalid status")
        if not isinstance(gate.get("required_before"), list) or not gate["required_before"]:
            errors.append(f"gate {name} requires required_before")
        standard = gate.get("standard")
        if not isinstance(standard, str) or not (ROOT / standard).is_file():
            errors.append(f"gate {name} standard is missing")
        evidence = gate.get("evidence")
        if not isinstance(evidence, list):
            errors.append(f"gate {name} evidence must be a list")
            continue
        if gate.get("status") == "satisfied" and not evidence:
            errors.append(f"gate {name} cannot be satisfied without evidence")
        for relative in evidence:
            if not isinstance(relative, str) or not (ROOT / relative).exists():
                errors.append(f"gate {name} evidence does not exist: {relative}")

    missing = REQUIRED_GATE_NAMES - names
    if missing:
        errors.append("missing required gates: " + ", ".join(sorted(missing)))
    if "reasoning-contrast-scope-frozen" in names:
        errors.append("ambiguous reasoning-contrast-scope-frozen gate must not exist")

    empirical_nc = by_name.get("negative-controls", {})
    formal_nc = by_name.get("formal-negative-controls", {})
    if empirical_nc.get("status") != "not_satisfied":
        errors.append("empirical negative-controls gate must remain not_satisfied")
    if formal_nc.get("status") != "satisfied":
        errors.append("formal-negative-controls gate must be satisfied after W4")
    if len(formal_nc.get("evidence", [])) < 3:
        errors.append("formal-negative-controls gate lacks proof, registry, or fixture evidence")
    if by_name.get("scoped-representation-proof", {}).get("status") != "not_satisfied":
        errors.append("scoped-representation-proof must remain not_satisfied before W5")
    if by_name.get("baseline-factorization-resolved", {}).get("status") != "not_satisfied":
        errors.append("baseline factorization must remain unresolved")
    if by_name.get("reasoning-contrast-corpus-frozen", {}).get("status") != "not_satisfied":
        errors.append("reasoning/contrast corpus must remain unfrozen")
    if by_name.get("independent-replication", {}).get("required_before") != ["independent_empirical_confirmation_claim"]:
        errors.append("independent replication may gate only independent empirical confirmation")

    policy = data.get("claim_policy")
    if not isinstance(policy, dict):
        errors.append("claim_policy must be an object")
    else:
        for key in REQUIRED_POLICY_TRUE:
            if policy.get(key) is not True:
                errors.append(f"claim_policy.{key} must be true")

    authorized = data.get("current_authorized_work")
    paused = data.get("paused_by_default")
    if not isinstance(authorized, list) or not authorized:
        errors.append("current_authorized_work must be nonempty")
        authorized = []
    if not isinstance(paused, list) or not paused:
        errors.append("paused_by_default must be nonempty")
        paused = []
    overlap = set(authorized) & set(paused)
    if overlap:
        errors.append("authorized and paused work overlap: " + ", ".join(sorted(overlap)))

    if claims_data.get("schema_version") != "1.0":
        errors.append("central claim schema_version must equal 1.0")
    if claims_data.get("research_mode") != "deduction_first_with_separate_validation_dimensions":
        errors.append("central claims must separate validation dimensions")
    claims = claims_data.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be a list")
        claims = []
    claim_ids: set[str] = set()
    for claim in claims:
        claim_id = claim.get("id") if isinstance(claim, dict) else None
        if not isinstance(claim_id, str) or not claim_id:
            errors.append("claim requires id")
            continue
        if claim_id in claim_ids:
            errors.append(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        if claim.get("current_status") not in ALLOWED_CLAIM_STATUS:
            errors.append(f"claim {claim_id} has invalid status: {claim.get('current_status')}")
        for field in ("maximum_supported_scope", "primary_resolution_mode", "required_next_test", "supporting_validation", "falsification_condition"):
            if not isinstance(claim.get(field), str) or not claim[field]:
                errors.append(f"claim {claim_id} requires {field}")
        if not isinstance(claim.get("nonclaims"), list) or not claim["nonclaims"]:
            errors.append(f"claim {claim_id} requires nonclaims")
    missing_claims = REQUIRED_CLAIM_IDS - claim_ids
    if missing_claims:
        errors.append("missing claims: " + ", ".join(sorted(missing_claims)))

    dimensions = claims_data.get("claim_dimensions")
    for key in ("theorem_status", "mechanization_status", "independent_proof_review_status", "empirical_replication_status", "application_status", "research_track"):
        if not isinstance(dimensions, dict) or key not in dimensions:
            errors.append(f"missing claim dimension: {key}")
    update_policy = claims_data.get("update_policy")
    for key in REQUIRED_UPDATE_POLICY_TRUE:
        if not isinstance(update_policy, dict) or update_policy.get(key) is not True:
            errors.append(f"central claim update_policy.{key} must be true")

    return report(errors, gate_count=len(gates), claim_count=len(claims))


def report(errors: list[str], gate_count: int = 0, claim_count: int = 0) -> int:
    if errors:
        print("Research gate validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Research gate validation PASS ({gate_count} gates; {claim_count} claims; formal W4 control gate separated from empirical controls)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
