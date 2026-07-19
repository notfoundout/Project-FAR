#!/usr/bin/env python3
"""Validate Project FAR's deduction-first research gates and claim boundaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/research-gates.json"
CLAIM_REGISTRY = ROOT / "theory/evaluation/central-claim-registry.json"

ALLOWED_STATUS = {"not_satisfied", "in_progress", "satisfied", "blocked", "retired"}
ALLOWED_CLAIM_STATUS = {
    "unresolved",
    "partially_supported",
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
}

REQUIRED_CLAIM_IDS = {
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
}

REQUIRED_CLAIM_UPDATE_POLICY_TRUE = {
    "evidence_for_and_against_required",
    "unknown_is_not_pass",
    "failures_are_immutable",
    "scope_changes_must_be_versioned",
    "stronger_status_requires_linked_artifacts",
    "theorem_and_replication_status_must_remain_separate",
    "experimental_results_may_not_be_promoted_to_proof",
    "proof_claims_require_explicit_assumptions_and_scope",
}

REQUIRED_CLAIM_DIMENSIONS = {
    "theorem_status",
    "mechanization_status",
    "independent_proof_review_status",
    "empirical_replication_status",
    "application_status",
}

THEOREM_GATE_NAMES = {
    "formal-theorem-target",
    "premise-ledger-and-semantics",
    "faithful-representation-definition",
    "scoped-representation-proof",
    "primitive-lower-bounds",
    "minimality-universe-and-proof",
    "mechanized-proof-verification",
    "independent-proof-review",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def read_json(path: Path, label: str, errors: list[str]) -> dict:
    if not path.is_file():
        fail(f"missing {label}: {path.relative_to(ROOT)}", errors)
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {label}: {exc}", errors)
        return {}
    if not isinstance(data, dict):
        fail(f"{label} must contain a JSON object", errors)
        return {}
    return data


def validate_gate_shape(gate: dict, seen_ids: set[str], seen_names: set[str], errors: list[str]) -> None:
    gate_id = gate.get("id")
    name = gate.get("name")
    status = gate.get("status")
    required_before = gate.get("required_before")
    evidence = gate.get("evidence")
    standard = gate.get("standard")

    if not isinstance(gate_id, str) or not gate_id:
        fail("every gate requires a non-empty id", errors)
    elif gate_id in seen_ids:
        fail(f"duplicate gate id: {gate_id}", errors)
    else:
        seen_ids.add(gate_id)

    if not isinstance(name, str) or not name:
        fail(f"gate {gate_id or '<unknown>'} requires a non-empty name", errors)
    elif name in seen_names:
        fail(f"duplicate gate name: {name}", errors)
    else:
        seen_names.add(name)

    if status not in ALLOWED_STATUS:
        fail(f"gate {gate_id or '<unknown>'} has invalid status: {status!r}", errors)

    if not isinstance(required_before, list) or not required_before:
        fail(f"gate {gate_id or '<unknown>'} requires a non-empty required_before list", errors)

    if not isinstance(standard, str) or not standard.strip():
        fail(f"gate {gate_id or '<unknown>'} requires a standard path", errors)
    elif not (ROOT / standard).is_file():
        fail(f"gate {gate_id or '<unknown>'} standard does not exist: {standard}", errors)

    if not isinstance(evidence, list):
        fail(f"gate {gate_id or '<unknown>'} evidence must be a list", errors)
    elif status == "satisfied" and not evidence:
        fail(f"gate {gate_id or '<unknown>'} cannot be satisfied without evidence", errors)
    else:
        for relative in evidence:
            if not isinstance(relative, str) or not relative.strip():
                fail(f"gate {gate_id or '<unknown>'} has an invalid evidence path", errors)
            elif not (ROOT / relative).exists():
                fail(f"gate {gate_id or '<unknown>'} evidence does not exist: {relative}", errors)


def main() -> int:
    errors: list[str] = []
    data = read_json(REGISTRY, "research gate registry", errors)
    claims_data = read_json(CLAIM_REGISTRY, "central claim registry", errors)

    if data.get("schema_version") != "1.0":
        fail("research gate schema_version must equal 1.0", errors)
    if data.get("research_mode") != "deduction_first_with_parallel_empirical_validation":
        fail("research_mode must be deduction_first_with_parallel_empirical_validation", errors)

    artifacts = data.get("required_canonical_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        fail("required_canonical_artifacts must be a non-empty list", errors)
        artifacts = []
    else:
        for relative in artifacts:
            if not isinstance(relative, str) or not relative.strip():
                fail("canonical artifact paths must be non-empty strings", errors)
                continue
            if not (ROOT / relative).is_file():
                fail(f"missing canonical artifact: {relative}", errors)

    required_deduction_artifacts = {
        "docs/governance/deduction-first-research-standard.md",
        "docs/planning/deduction-first-proof-roadmap.md",
    }
    missing_deduction_artifacts = required_deduction_artifacts - set(artifacts)
    if missing_deduction_artifacts:
        fail(
            "missing deduction-first canonical artifacts: "
            + ", ".join(sorted(missing_deduction_artifacts)),
            errors,
        )

    gates = data.get("gates")
    if not isinstance(gates, list):
        fail("gates must be a list", errors)
        gates = []

    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    gates_by_name: dict[str, dict] = {}
    for gate in gates:
        if not isinstance(gate, dict):
            fail("every gate must be an object", errors)
            continue
        validate_gate_shape(gate, seen_ids, seen_names, errors)
        name = gate.get("name")
        if isinstance(name, str):
            gates_by_name[name] = gate

    missing_names = REQUIRED_GATE_NAMES - seen_names
    if missing_names:
        fail("missing required gates: " + ", ".join(sorted(missing_names)), errors)

    for theorem_gate_name in THEOREM_GATE_NAMES:
        gate = gates_by_name.get(theorem_gate_name)
        if gate is None:
            continue
        if gate.get("standard") != "docs/governance/deduction-first-research-standard.md":
            fail(f"{theorem_gate_name} must use the deduction-first standard", errors)

    replication_gate = gates_by_name.get("independent-replication", {})
    if replication_gate.get("required_before") != ["independent_empirical_confirmation_claim"]:
        fail(
            "independent-replication must gate only independent_empirical_confirmation_claim",
            errors,
        )

    representation_gate = gates_by_name.get("scoped-representation-proof", {})
    if "representation_theorem_proof_claim" not in representation_gate.get("required_before", []):
        fail("scoped-representation-proof must gate representation theorem proof claims", errors)

    policy = data.get("claim_policy")
    if not isinstance(policy, dict):
        fail("claim_policy must be an object", errors)
    else:
        for key in sorted(REQUIRED_POLICY_TRUE):
            if policy.get(key) is not True:
                fail(f"claim_policy.{key} must be true", errors)

    authorized = data.get("current_authorized_work")
    paused = data.get("paused_by_default")
    if not isinstance(authorized, list) or not authorized:
        fail("current_authorized_work must be a non-empty list", errors)
        authorized = []
    if not isinstance(paused, list) or not paused:
        fail("paused_by_default must be a non-empty list", errors)
        paused = []

    required_authorized = {
        "theorem_target_and_scope",
        "premise_ledger",
        "faithful_representation_definition",
        "scoped_representation_proof",
        "formal_countermodel_search",
        "primitive_lower_bounds",
        "proof_mechanization",
    }
    missing_authorized = required_authorized - set(authorized)
    if missing_authorized:
        fail("missing authorized deductive work: " + ", ".join(sorted(missing_authorized)), errors)

    overlap = set(authorized) & set(paused)
    if overlap:
        fail("work cannot be both authorized and paused: " + ", ".join(sorted(overlap)), errors)

    if claims_data.get("schema_version") != "1.0":
        fail("central claim registry schema_version must equal 1.0", errors)
    if claims_data.get("research_mode") != "deduction_first_with_separate_validation_dimensions":
        fail("central claim registry must separate theorem and validation dimensions", errors)

    claims = claims_data.get("claims")
    if not isinstance(claims, list):
        fail("central claim registry claims must be a list", errors)
        claims = []

    seen_claims: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            fail("every central claim must be an object", errors)
            continue
        claim_id = claim.get("id")
        status = claim.get("current_status")
        if not isinstance(claim_id, str) or not claim_id:
            fail("every central claim requires a non-empty id", errors)
            continue
        if claim_id in seen_claims:
            fail(f"duplicate central claim id: {claim_id}", errors)
        seen_claims.add(claim_id)
        if status not in ALLOWED_CLAIM_STATUS:
            fail(f"central claim {claim_id} has invalid status: {status!r}", errors)
        for field in (
            "maximum_supported_scope",
            "primary_resolution_mode",
            "required_next_test",
            "supporting_validation",
            "falsification_condition",
        ):
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                fail(f"central claim {claim_id} requires {field}", errors)
        nonclaims = claim.get("nonclaims")
        if not isinstance(nonclaims, list) or not nonclaims:
            fail(f"central claim {claim_id} requires nonclaims", errors)

    missing_claims = REQUIRED_CLAIM_IDS - seen_claims
    if missing_claims:
        fail("missing required central claims: " + ", ".join(sorted(missing_claims)), errors)

    dimensions = claims_data.get("claim_dimensions")
    if not isinstance(dimensions, dict):
        fail("central claim registry claim_dimensions must be an object", errors)
    else:
        missing_dimensions = REQUIRED_CLAIM_DIMENSIONS - set(dimensions)
        if missing_dimensions:
            fail("missing claim dimensions: " + ", ".join(sorted(missing_dimensions)), errors)

    update_policy = claims_data.get("update_policy")
    if not isinstance(update_policy, dict):
        fail("central claim registry update_policy must be an object", errors)
    else:
        for key in sorted(REQUIRED_CLAIM_UPDATE_POLICY_TRUE):
            if update_policy.get(key) is not True:
                fail(f"central claim update_policy.{key} must be true", errors)

    if errors:
        print("Research gate validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Research gate validation PASS "
        f"({len(gates)} gates, {len(artifacts)} canonical artifacts, {len(claims)} central claims)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
