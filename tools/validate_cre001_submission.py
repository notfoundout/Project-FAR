#!/usr/bin/env python3
"""Validate future CRE-001 evaluator submission bundles.

This operational validator is for ingestion checks only. Synthetic fixtures used
with it are not evaluator mappings and must not be entered into CRE-001 results.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXECUTION = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/execution"
ASSIGNMENT_KEY = EXECUTION / "assignments/internal/assignment-key.json"
VALID_PRESERVATION = {"Pass", "Partial", "Fail", "Unknown"}
ASSIGNMENT_RE = re.compile(r"^CRE-001-E0[1-9]$")
EXPERIMENT = "CRE-001"
LEAKAGE_TERMS = {
    "Vocabulary A",
    "Vocabulary B",
    "Vocabulary C",
    "FAR target",
    "baseline vocabulary",
    "expected outcome",
    "prior FAR mapping",
    "comparative hypothesis",
}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc


def require(obj: dict[str, Any], field: str, where: str) -> Any:
    if field not in obj or obj[field] in (None, "", "PENDING"):
        raise ValidationError(f"{where}: missing required field {field}")
    return obj[field]


def walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for child in value.values():
            out.extend(walk_strings(child))
        return out
    if isinstance(value, list):
        out: list[str] = []
        for child in value:
            out.extend(walk_strings(child))
        return out
    return []


def assignment_map() -> dict[str, str]:
    key = load_json(ASSIGNMENT_KEY)
    return {row["assignment_identifier"]: row["assigned_vocabulary_version"] for row in key["assignments"]}


def validate_unknowns(mapping: dict[str, Any]) -> None:
    declared = mapping.get("declared_unknown_values", [])
    if not isinstance(declared, list):
        raise ValidationError("mapping: declared_unknown_values must be a list")
    for item in declared:
        if not isinstance(item, dict):
            raise ValidationError("mapping: Unknown declarations must be objects")
        require(item, "unknown_id", "Unknown declaration")
        require(item, "scope", "Unknown declaration")
        require(item, "reason", "Unknown declaration")


def validate_preservation(mapping: dict[str, Any], cir: dict[str, Any]) -> None:
    args = require(mapping, "preservation_arguments", "mapping")
    if not isinstance(args, dict):
        raise ValidationError("mapping: preservation_arguments must be an object")
    for key in ["p_s_structural", "p_m_semantic", "p_o_operational", "p_d_dependency", "p_i_information", "p_h_historical"]:
        entry = require(args, key, "mapping.preservation_arguments")
        value = require(entry, "value", f"mapping.preservation_arguments.{key}")
        if value not in VALID_PRESERVATION:
            raise ValidationError(f"mapping.preservation_arguments.{key}: malformed preservation value {value!r}")
        if value == "Unknown" and not mapping.get("declared_unknown_values"):
            raise ValidationError(f"mapping.preservation_arguments.{key}: Unknown requires declared_unknown_values")
    vector = require(cir, "preservation_vector", "cir")
    for key in ["p_s", "p_m", "p_o", "p_d", "p_i", "p_h"]:
        value = require(vector, key, "cir.preservation_vector")
        if value not in VALID_PRESERVATION:
            raise ValidationError(f"cir.preservation_vector.{key}: malformed preservation value {value!r}")


def validate_bundle(path: Path) -> None:
    bundle = load_json(path)
    experiment = require(bundle, "experiment", "bundle")
    if experiment != EXPERIMENT:
        raise ValidationError(f"bundle: invalid experiment {experiment!r}")
    assignment = require(bundle, "assignment_identifier", "bundle")
    if not ASSIGNMENT_RE.match(assignment):
        raise ValidationError(f"bundle: invalid assignment identifier {assignment!r}")
    evaluator = require(bundle, "evaluator_identifier", "bundle")
    if not re.match(r"^CRE-001-EVALUATOR-[A-Za-z0-9_-]+$", evaluator):
        raise ValidationError(f"bundle: invalid evaluator identifier {evaluator!r}")
    submission_id = require(bundle, "submission_identifier", "bundle")
    mapping = require(bundle, "mapping_submission", "bundle")
    cir = require(bundle, "cir_submission", "bundle")
    provenance = require(bundle, "provenance", "bundle")
    if not isinstance(provenance, dict):
        raise ValidationError("bundle: provenance must be an object")
    require(provenance, "provenance_record_identifier", "provenance")
    require(provenance, "operator_or_evaluator", "provenance")
    require(provenance, "created_at", "provenance")

    assignments = assignment_map()
    expected_vocab = assignments.get(assignment)
    for label, doc in [("mapping", mapping), ("cir", cir)]:
        if require(doc, "experiment", label) != EXPERIMENT:
            raise ValidationError(f"{label}: experiment mismatch")
        if require(doc, "assignment_identifier", label) != assignment:
            raise ValidationError(f"{label}: assignment mismatch")
        if require(doc, "vocabulary_version", label) != expected_vocab:
            raise ValidationError(f"{label}: assignment mismatch for vocabulary_version")
    if require(mapping, "evaluator_identifier", "mapping") != evaluator:
        raise ValidationError("mapping: evaluator mismatch")
    if require(cir, "provenance_record_identifier", "cir") != provenance["provenance_record_identifier"]:
        raise ValidationError("cir: provenance mismatch")
    assumptions = require(mapping, "assumptions", "mapping")
    if not isinstance(assumptions, list):
        raise ValidationError("mapping: assumptions must be a list")
    for assumption in assumptions:
        if not isinstance(assumption, dict) or not assumption.get("assumption_id") or not assumption.get("statement"):
            raise ValidationError("mapping: undeclared or malformed assumption")
    validate_unknowns(mapping)
    validate_preservation(mapping, cir)
    text = "\n".join(walk_strings({"bundle": bundle, "mapping": mapping, "cir": cir}))
    for term in LEAKAGE_TERMS:
        if term in text:
            raise ValidationError(f"bundle: vocabulary leakage detected: {term}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    seen: dict[str, Path] = {}
    errors: list[str] = []
    for path in args.paths:
        try:
            data = load_json(path)
            sid = require(data, "submission_identifier", str(path))
            if sid in seen:
                raise ValidationError(f"{path}: duplicate submission identifier {sid!r}; first seen in {seen[sid]}")
            seen[sid] = path
            validate_bundle(path)
        except ValidationError as exc:
            errors.append(str(exc))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(args.paths)} CRE-001 submission bundle(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
