"""far-ir/2.0 comparison-contract validation.

JSON Schema checks document shape. This module adds only finite-explicit semantic checks that
can actually be decided from a record: factorization, collision, exact observational quotient,
reference coverage, and freeze hashing. It deliberately does not infer domain correspondence,
novelty, empirical utility, approximation semantics, or contract-free universality.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "far-contract-v2.schema.json"
FORMAT_VERSION = "far-ir/2.0"


@dataclass(frozen=True, slots=True)
class ContractDiagnostic:
    code: str
    message: str
    path: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class ContractValidationResult:
    diagnostics: tuple[ContractDiagnostic, ...]

    @property
    def success(self) -> bool:
        return not self.diagnostics


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def contract_sha256(contract: Mapping[str, Any]) -> str:
    """Hash only the contract object, avoiding self-referential document hashing."""
    return hashlib.sha256(canonical_json(contract).encode("utf-8")).hexdigest()


def _key(value: object) -> str:
    return canonical_json(value)


def _load_schema() -> Mapping[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _schema_errors(document: object) -> list[ContractDiagnostic]:
    schema = _load_schema()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        ContractDiagnostic("SCHEMA_CONSTRAINT_VIOLATION", error.message, tuple(error.path))
        for error in sorted(validator.iter_errors(document), key=lambda e: (tuple(e.path), e.message))
    ]


def _indexed_table(entries: Sequence[Mapping[str, Any]], label: str, errors: list[ContractDiagnostic]) -> dict[str, object]:
    result: dict[str, object] = {}
    for i, entry in enumerate(entries):
        case_id = str(entry["case_id"])
        if case_id in result:
            errors.append(ContractDiagnostic("DUPLICATE_CASE_VALUE", f"{label} has duplicate case_id {case_id}", (label, i)))
        else:
            result[case_id] = entry["value"]
    return result


def _explicit_tables(document: Mapping[str, Any], errors: list[ContractDiagnostic]) -> tuple[list[str], dict[str, object], dict[str, object]] | None:
    contract = document["contract"]
    domain = contract["source_domain"]
    behavior = contract["required_behavior"]
    representation = contract["representation"]
    if domain["kind"] != "finite_explicit" or domain["status"] != "EXPLICIT":
        errors.append(ContractDiagnostic("CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN", "checked evidence requires source_domain kind finite_explicit with EXPLICIT status"))
        return None
    case_ids = [str(case["id"]) for case in domain["cases"]]
    if len(case_ids) != len(set(case_ids)):
        errors.append(ContractDiagnostic("DUPLICATE_DOMAIN_CASE", "source_domain case identifiers must be unique"))
    behavior_table = _indexed_table(behavior["table"], "required_behavior", errors)
    representation_table = _indexed_table(representation["table"], "representation", errors)
    expected = set(case_ids)
    for label, table in (("required_behavior", behavior_table), ("representation", representation_table)):
        missing = sorted(expected - set(table))
        extra = sorted(set(table) - expected)
        if missing or extra:
            errors.append(ContractDiagnostic("CASE_TABLE_COVERAGE_MISMATCH", f"{label} coverage mismatch missing={missing} extra={extra}"))
    if behavior["status"] != "EXPLICIT" or representation["status"] != "EXPLICIT":
        errors.append(ContractDiagnostic("CHECK_REQUIRES_EXPLICIT_TABLES", "checked evidence requires EXPLICIT required_behavior and representation tables"))
    if errors:
        return None
    return case_ids, behavior_table, representation_table


def _check_factorization(document: Mapping[str, Any], errors: list[ContractDiagnostic]) -> None:
    evidence = document["report"]["evidence"]
    if evidence["status"] != "CHECKED_FINITE_EXPLICIT":
        return
    tables = _explicit_tables(document, errors)
    if tables is None:
        return
    case_ids, behavior, representation = tables
    decoder: dict[str, object] = {}
    for i, entry in enumerate(evidence["decoder_table"]):
        key = _key(entry["representation_value"])
        value = entry["behavior_value"]
        if key in decoder and _key(decoder[key]) != _key(value):
            errors.append(ContractDiagnostic("NONFUNCTIONAL_DECODER", "decoder_table assigns two behavior values to one representation value", ("report", "evidence", "decoder_table", i)))
        decoder[key] = value
    for case_id in case_ids:
        rep_key = _key(representation[case_id])
        if rep_key not in decoder:
            errors.append(ContractDiagnostic("DECODER_UNDEFINED", f"decoder has no value for representation of case {case_id}"))
        elif _key(decoder[rep_key]) != _key(behavior[case_id]):
            errors.append(ContractDiagnostic("FACTORIZATION_FAILURE", f"d(r(x)) != beta(x) for case {case_id}"))


def _check_collision(document: Mapping[str, Any], errors: list[ContractDiagnostic]) -> None:
    evidence = document["report"]["evidence"]
    if evidence["status"] != "CHECKED_FINITE_EXPLICIT":
        return
    tables = _explicit_tables(document, errors)
    if tables is None:
        return
    case_ids, behavior, representation = tables
    left, right = str(evidence["left_case_id"]), str(evidence["right_case_id"])
    valid = set(case_ids)
    if left not in valid or right not in valid:
        errors.append(ContractDiagnostic("COLLISION_CASE_UNKNOWN", "collision witness case ids must belong to source_domain"))
        return
    if left == right:
        errors.append(ContractDiagnostic("COLLISION_REQUIRES_DISTINCT_CASES", "collision witness must name two distinct cases"))
    if _key(representation[left]) != _key(representation[right]):
        errors.append(ContractDiagnostic("COLLISION_REPRESENTATION_DIFFERS", "collision witness cases do not share the same representation value"))
    if _key(behavior[left]) == _key(behavior[right]):
        errors.append(ContractDiagnostic("COLLISION_BEHAVIOR_AGREES", "collision witness cases do not differ in required behavior"))


def _check_quotient(document: Mapping[str, Any], errors: list[ContractDiagnostic]) -> None:
    evidence = document["report"]["evidence"]
    if evidence["status"] != "CHECKED_FINITE_EXPLICIT":
        return
    tables = _explicit_tables(document, errors)
    if tables is None:
        return
    case_ids, behavior, _representation = tables
    membership: dict[str, str] = {}
    for cls in evidence["classes"]:
        class_id = str(cls["id"])
        for case_id in cls["case_ids"]:
            case_id = str(case_id)
            if case_id in membership:
                errors.append(ContractDiagnostic("QUOTIENT_OVERLAP", f"case {case_id} occurs in more than one quotient class"))
            membership[case_id] = class_id
    expected = set(case_ids)
    if set(membership) != expected:
        errors.append(ContractDiagnostic("QUOTIENT_NOT_PARTITION", f"quotient classes must partition source_domain missing={sorted(expected-set(membership))} extra={sorted(set(membership)-expected)}"))
        return
    for left in case_ids:
        for right in case_ids:
            same_behavior = _key(behavior[left]) == _key(behavior[right])
            same_class = membership[left] == membership[right]
            if same_class and not same_behavior:
                errors.append(ContractDiagnostic("QUOTIENT_CLASS_NOT_BEHAVIOR_CONSTANT", f"cases {left} and {right} share a class but differ in required behavior"))
            if evidence["claims_exact_observational_quotient"] and same_behavior != same_class:
                errors.append(ContractDiagnostic("QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL", f"class relation differs from beta-kernel for cases {left} and {right}"))


def _check_cross_field_contract(document: Mapping[str, Any], errors: list[ContractDiagnostic]) -> None:
    contract = document["contract"]
    report = document["report"]
    evidence = report["evidence"]
    mode = contract["mode"]
    kind = evidence["kind"]
    outcome = report["outcome"]

    if kind == "unknown" and outcome != "Unknown":
        errors.append(ContractDiagnostic("UNKNOWN_EVIDENCE_REQUIRES_UNKNOWN_OUTCOME", "unknown evidence must have outcome Unknown"))
    if outcome == "Unknown" and kind != "unknown":
        errors.append(ContractDiagnostic("UNKNOWN_OUTCOME_REQUIRES_UNKNOWN_EVIDENCE", "outcome Unknown must use unknown evidence"))
    if mode == "Unknown" and outcome != "Unknown":
        errors.append(ContractDiagnostic("UNKNOWN_CONTRACT_MODE_REQUIRES_UNKNOWN_OUTCOME", "Unknown contract mode cannot certify a non-Unknown outcome"))
    if mode == "approximate" and evidence.get("status") == "CHECKED_FINITE_EXPLICIT":
        errors.append(ContractDiagnostic("W5_SEMANTICS_NOT_ESTABLISHED", "W3 does not certify checked approximate factorization/collision/quotient semantics; approximation fields are declarations only"))
    if evidence.get("status") == "CHECKED_FINITE_EXPLICIT":
        expected = "REFUTED" if kind == "collision" else "PROVED"
        if outcome != expected:
            errors.append(ContractDiagnostic("CHECKED_EVIDENCE_OUTCOME_MISMATCH", f"checked {kind} evidence requires outcome {expected}"))

    observation_ids = [item["id"] for item in contract["observation_contexts"]]
    if len(observation_ids) != len(set(observation_ids)):
        errors.append(ContractDiagnostic("DUPLICATE_OBSERVATION_CONTEXT", "observation_context ids must be unique"))
    transformation_ids = [item["id"] for item in contract["admitted_transformations"]]
    if len(transformation_ids) != len(set(transformation_ids)):
        errors.append(ContractDiagnostic("DUPLICATE_TRANSFORMATION", "admitted_transformations ids must be unique"))

    freeze = document["freeze"]
    if freeze["status"] == "FROZEN":
        actual = contract_sha256(contract)
        if freeze["contract_sha256"] != actual:
            errors.append(ContractDiagnostic("FREEZE_HASH_MISMATCH", f"contract_sha256 mismatch expected={actual} actual={freeze['contract_sha256']}"))


def validate_contract(document: object) -> ContractValidationResult:
    errors = _schema_errors(document)
    if errors or not isinstance(document, Mapping):
        return ContractValidationResult(tuple(errors))
    _check_cross_field_contract(document, errors)
    evidence = document["report"]["evidence"]
    if evidence["kind"] == "factorization":
        _check_factorization(document, errors)
    elif evidence["kind"] == "collision":
        _check_collision(document, errors)
    elif evidence["kind"] == "quotient":
        _check_quotient(document, errors)
    return ContractValidationResult(tuple(errors))


def load_and_validate(path: str | Path) -> ContractValidationResult:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ContractValidationResult((ContractDiagnostic("UNREADABLE_CONTRACT", str(exc)),))
    return validate_contract(document)


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.contract_v2")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = load_and_validate(args.path)
    if args.json:
        print(json.dumps({"success": result.success, "diagnostics": [d.__dict__ if hasattr(d, "__dict__") else {"code": d.code, "message": d.message, "path": list(d.path)} for d in result.diagnostics]}, indent=2, sort_keys=True))
    else:
        print("PASS" if result.success else "FAIL")
        for diagnostic in result.diagnostics:
            print(f"{diagnostic.code}: {diagnostic.message}")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
