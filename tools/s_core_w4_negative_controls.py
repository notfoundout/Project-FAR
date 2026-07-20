#!/usr/bin/env python3
"""Executable representatives for SCORE-W4-PROOF-001 negative-control families."""
from __future__ import annotations

import copy
from typing import Any

from s_core_w3_reference import (
    W3Error,
    construct_witness,
    semantic_agreement,
    validate_package,
    verify_witness,
)

CONTROL_IDS = tuple(f"NC-{index:02d}" for index in range(1, 11))

CONTROL_SPEC: dict[str, dict[str, Any]] = {
    "NC-01": {
        "name": "lookup-table substitution",
        "diagnostic": "process_and_commitment_structure_lost",
        "violated_clauses": ["P4", "P5", "P7"],
        "detection_mode": "operational",
    },
    "NC-02": {
        "name": "dependency collapse",
        "diagnostic": "distinct_dependency_roles_collapsed",
        "violated_clauses": ["P4_relation_reflection"],
        "detection_mode": "structural",
    },
    "NC-03": {
        "name": "history erasure",
        "diagnostic": "material_history_or_revision_erased",
        "violated_clauses": ["P7_order_or_revision_reflection"],
        "detection_mode": "historical",
    },
    "NC-04": {
        "name": "hidden rule modification",
        "diagnostic": "undeclared_operational_machinery",
        "violated_clauses": ["AdmissibleRecovery", "LedgerComplete"],
        "detection_mode": "operational",
    },
    "NC-05": {
        "name": "label-only semantics",
        "diagnostic": "semantic_claim_reduced_to_label",
        "violated_clauses": ["SemAgree", "lexical_invariance"],
        "detection_mode": "semantic",
    },
    "NC-06": {
        "name": "unrestricted interpreter",
        "diagnostic": "unrestricted_external_interpreter",
        "violated_clauses": ["AdmissibleRecovery", "Uniform", "LedgerComplete"],
        "detection_mode": "machinery",
    },
    "NC-07": {
        "name": "hidden auxiliary state",
        "diagnostic": "protected_information_relocated_outside_witness",
        "violated_clauses": ["image_accountability", "LedgerComplete"],
        "detection_mode": "machinery",
    },
    "NC-08": {
        "name": "provenance deletion",
        "diagnostic": "material_provenance_deleted",
        "violated_clauses": ["P4", "P7", "Pres_8I"],
        "detection_mode": "historical",
    },
    "NC-09": {
        "name": "output-equivalent process substitution",
        "diagnostic": "output_equivalence_without_process_equivalence",
        "violated_clauses": ["P4", "P5", "P6", "P7"],
        "detection_mode": "operational",
    },
    "NC-10": {
        "name": "primitive smuggling",
        "diagnostic": "function_relocated_into_unaccounted_metadata",
        "violated_clauses": ["LedgerComplete", "machinery_accounting"],
        "detection_mode": "machinery",
    },
}


def _copy(package: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(package)


def apply_control(
    control_id: str,
    source: dict[str, Any],
    package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construct one canonical representative of a frozen negative-control family."""
    if control_id not in CONTROL_SPEC:
        raise ValueError(f"unknown control: {control_id}")
    baseline = construct_witness(source) if package is None else package
    mutated = _copy(baseline)
    E = mutated["W"]["E"]

    if control_id == "NC-01":
        mutated["A"]["Theta"] = []
        mutated["A"]["Omega"]["transition_statuses"] = []
        for key in (
            "events",
            "order",
            "causal",
            "provenance",
            "revisions",
            "modifications",
            "dependency_ancestry",
            "path_conditions",
        ):
            mutated["A"]["H"][key] = []

    elif control_id == "NC-02":
        support = E["occ:p4:support"]
        defeat = E["occ:p4:defeat"]
        role_pairs = mutated["A"]["R"]["occurrence_role"]
        support_role = next(role for occurrence, role in role_pairs if occurrence == support)
        mutated["A"]["R"]["occurrence_role"] = [
            [occurrence, support_role if occurrence == defeat else role]
            for occurrence, role in role_pairs
        ]

    elif control_id == "NC-03":
        for key in (
            "order",
            "causal",
            "revisions",
            "modifications",
            "dependency_ancestry",
            "path_conditions",
        ):
            mutated["A"]["H"][key] = []

    elif control_id == "NC-04":
        mutated["W"]["kappa"]["forbidden"]["undeclared_executable"] = True
        mutated["control_environment"] = {
            "undeclared_rule_override": "replace active rule behavior after construction"
        }

    elif control_id == "NC-05":
        subject = E["commitment:c1"]
        interpretation = next(
            item for item in mutated["A"]["I"] if item.get("subject") == subject
        )
        interpretation["denotation"] = subject
        interpretation["basis"] = "display_label_only"

    elif control_id == "NC-06":
        mutated["W"]["kappa"]["external_dependencies"] = [
            "unrestricted-general-interpreter"
        ]

    elif control_id == "NC-07":
        occurrence = E["occ:p4:support"]
        saved = [
            pair
            for pair in mutated["A"]["R"]["occurrence_role"]
            if pair[0] == occurrence
        ]
        mutated["A"]["R"]["occurrence_role"] = [
            pair
            for pair in mutated["A"]["R"]["occurrence_role"]
            if pair[0] != occurrence
        ]
        mutated["hidden_auxiliary_state"] = {"removed_occurrence_role": saved}

    elif control_id == "NC-08":
        p4_prov = E["occ:p4:prov"]
        p8_prov = E["occ:p8:prov"]
        mutated["A"]["Prov"] = []
        mutated["A"]["H"]["provenance"] = []
        mutated["A"]["R"]["occurrence_role"] = [
            pair
            for pair in mutated["A"]["R"]["occurrence_role"]
            if pair[0] not in {p4_prov, p8_prov}
        ]

    elif control_id == "NC-09":
        for transition in mutated["A"]["Theta"]:
            transition["preconditions"] = []
            transition["resource_conditions"] = []
            transition["action_dependencies"] = []
            transition["observation_dependencies"] = []
        mutated["process_substitution"] = {
            "same_state_carrier": True,
            "same_transition_endpoints": True,
            "material_dependencies_replaced": True,
        }

    elif control_id == "NC-10":
        explicit_interpretation = copy.deepcopy(mutated["A"]["I"])
        mutated["A"]["I"] = []
        mutated["W"]["M"]["smuggled_interpretation"] = explicit_interpretation

    return mutated


def evaluate_control(
    control_id: str,
    source: dict[str, Any],
    package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    baseline = construct_witness(source) if package is None else package
    mutated = apply_control(control_id, source, baseline)
    validation_error: str | None = None
    try:
        validate_package(mutated)
    except (KeyError, TypeError, ValueError, W3Error) as exc:
        validation_error = str(exc)

    witness_accepted = verify_witness(source, mutated)
    semantic_ok = semantic_agreement(source, mutated)
    detected = validation_error is not None or not witness_accepted
    spec = CONTROL_SPEC[control_id]
    return {
        "id": control_id,
        "name": spec["name"],
        "status": "rejected_expected_reason" if detected else "unexpected_pass",
        "detected": detected,
        "validation_error": validation_error,
        "witness_accepted": witness_accepted,
        "semantic_agreement": semantic_ok,
        "diagnostic": spec["diagnostic"],
        "violated_clauses": list(spec["violated_clauses"]),
        "detection_mode": spec["detection_mode"],
    }


def run_suite(source: dict[str, Any]) -> list[dict[str, Any]]:
    package = construct_witness(source)
    return [evaluate_control(control_id, source, package) for control_id in CONTROL_IDS]


def suite_passes(source: dict[str, Any]) -> bool:
    results = run_suite(source)
    return len(results) == len(CONTROL_IDS) and all(
        result["status"] == "rejected_expected_reason" for result in results
    )


__all__ = [
    "CONTROL_IDS",
    "CONTROL_SPEC",
    "apply_control",
    "evaluate_control",
    "run_suite",
    "suite_passes",
]
