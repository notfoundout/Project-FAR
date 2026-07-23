#!/usr/bin/env python3
"""Validate the frozen universality remainder theorem registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_OBLIGATIONS = {
    "G1": "single_kernel_semantic_composition",
    "G2": "open_world_structural_maximality",
    "G3": "inaccessibility_and_epistemic_maximality",
}

EXPECTED_PREDECESSORS = {
    "foundation": 282,
    "target_class": 283,
    "faithfulness_contract": 284,
    "representation_universe": 285,
    "machinery_closure": 286,
    "equivalence": 287,
    "component_necessity_start": 288,
    "component_independence": 293,
    "sufficiency": 294,
    "relative_maximality": 295,
    "terminal_adjudication": 296,
    "post_terminal_evaluation": 297,
}

REQUIRED_NONCLAIMS = {
    "unrestricted_metaphysical_universality",
    "open_world_maximality_from_finite_search",
    "hidden_cognition_recovery_without_warrant",
    "unique_final_ontology",
    "predetermined_confirmation",
}


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("registry root must be an object")
    return value


def validate_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("schema") != "universality-remainder-theorem/1.0":
        errors.append("unexpected schema")
    if data.get("program_id") != "POST-UPP-URT-001":
        errors.append("unexpected program_id")
    if data.get("status") != "frozen":
        errors.append("status must be frozen")

    if data.get("frozen_predecessors") != EXPECTED_PREDECESSORS:
        errors.append("frozen predecessor map changed")

    obligations = data.get("obligations")
    if not isinstance(obligations, list):
        errors.append("obligations must be a list")
        obligations = []

    seen: dict[str, str] = {}
    for obligation in obligations:
        if not isinstance(obligation, dict):
            errors.append("every obligation must be an object")
            continue
        obligation_id = obligation.get("id")
        name = obligation.get("name")
        if not isinstance(obligation_id, str) or not isinstance(name, str):
            errors.append("every obligation requires string id and name")
            continue
        if obligation_id in seen:
            errors.append(f"duplicate obligation id: {obligation_id}")
        seen[obligation_id] = name
        if obligation.get("initial_status") != "unresolved":
            errors.append(f"{obligation_id} must begin unresolved")
        substitutes = obligation.get("disallowed_substitutes")
        if not isinstance(substitutes, list) or not substitutes:
            errors.append(f"{obligation_id} requires disallowed substitutes")

    if seen != EXPECTED_OBLIGATIONS:
        errors.append("obligation set changed")

    if data.get("successor_order") != ["G1", "G2", "G3_and_terminal_adjudication"]:
        errors.append("successor order changed")

    reopening = data.get("allowed_reopening_labels")
    if set(reopening or []) != {
        "replication",
        "mechanization",
        "defect_correction",
        "premise_strengthening",
    }:
        errors.append("allowed reopening labels changed")

    nonclaims = set(data.get("global_nonclaims") or [])
    if not REQUIRED_NONCLAIMS.issubset(nonclaims):
        errors.append("required global nonclaims missing")

    completed = data.get("completed_work_not_to_reopen_without_delta")
    if not isinstance(completed, list) or len(completed) < 15:
        errors.append("completed-work nonredundancy ledger is incomplete")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("theory/evaluation/universality-remainder-theorem-v1.0.json"),
    )
    args = parser.parse_args()

    try:
        data = _load(args.path)
        errors = validate_registry(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: universality remainder theorem registry is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
