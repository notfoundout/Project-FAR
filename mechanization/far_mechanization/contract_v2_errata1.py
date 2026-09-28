"""far-ir/2.0 verification as corrected by specification errata 1.

The frozen baseline ``contract_v2`` stays byte-identical: it is git-blob pinned as the
preregistered ``PCA-W6`` protocol base, it is the ``EFR-001`` v1.0 baseline command, and
``contract_v2_strict`` (bound by the ``EFR-001`` comparator amendment v2.0) wraps it. The 2026-09
root-of-trust audit found four baseline behaviors that contradict the specification or leave a
clean-room result undetermined. ``docs/specification/far-ir-2.0-errata-1.md`` corrects them, and
this module implements the baseline specification as corrected:

* intake accepts RFC 8259 JSON only: ``NaN``/``Infinity`` and a repeated member name yield
  ``UNREADABLE_CONTRACT``, and an in-memory non-finite number yields one
  ``SCHEMA_CONSTRAINT_VIOLATION``;
* quotient classes are the declared entries, identified by position: a repeated class id is
  ``DUPLICATE_QUOTIENT_CLASS`` rather than a merge, and overlapping classes are not a partition;
* a ``FROZEN`` record whose ``frozen_at`` is not an RFC3339 date-time is ``FREEZE_TIME_INVALID``.

Every other rule, and the stage structure, is the baseline's own code: a record that triggers none
of these corrections gets exactly the baseline diagnostics. ``EFR-001-R2-INPUT-AMENDMENT-1.2`` names
this module as the ``far-ir/2.0`` reference for the ``EFR-R2`` frozen expected result. Current
verification adds the determinate-outcome rule on top of it (``contract_v2_strict_v11``).

A file is read and parsed exactly once.
"""
from __future__ import annotations

import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from .contract_v2 import (
        FORMAT_VERSION,
        REPO_ROOT,
        SCHEMA_PATH,
        ContractDiagnostic,
        ContractValidationResult,
        _check_collision,
        _check_cross_field_contract as _check_cross_field_contract_baseline,
        _check_factorization,
        _explicit_tables,
        _key,
        _schema_errors,
        canonical_json,
        contract_sha256,
    )
except ImportError:  # Loaded as a standalone file (no parent package), as the commercial bridge does.
    import importlib.util as _importlib_util
    import sys as _sys

    _BASELINE_PATH = Path(__file__).resolve().with_name("contract_v2.py")
    _BASELINE_NAME = f"{__name__}._baseline_contract_v2"
    _spec = _importlib_util.spec_from_file_location(_BASELINE_NAME, _BASELINE_PATH)
    if _spec is None or _spec.loader is None:
        raise ImportError(f"cannot load baseline far-ir/2.0 verifier {_BASELINE_PATH}")
    _baseline = _importlib_util.module_from_spec(_spec)
    _sys.modules[_BASELINE_NAME] = _baseline
    _spec.loader.exec_module(_baseline)
    FORMAT_VERSION = _baseline.FORMAT_VERSION
    REPO_ROOT = _baseline.REPO_ROOT
    SCHEMA_PATH = _baseline.SCHEMA_PATH
    ContractDiagnostic = _baseline.ContractDiagnostic
    ContractValidationResult = _baseline.ContractValidationResult
    _check_collision = _baseline._check_collision
    _check_cross_field_contract_baseline = _baseline._check_cross_field_contract
    _check_factorization = _baseline._check_factorization
    _explicit_tables = _baseline._explicit_tables
    _key = _baseline._key
    _schema_errors = _baseline._schema_errors
    canonical_json = _baseline.canonical_json
    contract_sha256 = _baseline.contract_sha256

__all__ = [
    "FORMAT_VERSION",
    "REPO_ROOT",
    "SCHEMA_PATH",
    "ContractDiagnostic",
    "ContractValidationResult",
    "canonical_json",
    "contract_sha256",
    "load_and_validate",
    "load_document",
    "validate_contract",
]

RFC3339_DATE_TIME = re.compile(
    r"\A[0-9]{4}-[0-9]{2}-[0-9]{2}[Tt][0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?([Zz]|[+-][0-9]{2}:[0-9]{2})\Z"
)


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key {key!r}: RFC 8259 leaves its meaning parser-dependent")
        result[key] = value
    return result


def _reject_constant(name: str) -> object:
    raise ValueError(f"{name} is not a JSON value")


def _non_json_numbers(value: object) -> bool:
    if isinstance(value, float):
        return not math.isfinite(value)
    if isinstance(value, dict):
        return any(_non_json_numbers(item) for item in value.values())
    if isinstance(value, list):
        return any(_non_json_numbers(item) for item in value)
    return False


def _is_rfc3339(value: object) -> bool:
    if not isinstance(value, str) or not RFC3339_DATE_TIME.match(value):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00" if value[-1] in "Zz" else value)
    except ValueError:
        return False
    return True


def _check_cross_field_contract(document: Mapping[str, Any], errors: list[Any]) -> None:
    stage2: list[Any] = []
    _check_cross_field_contract_baseline(document, stage2)
    freeze = document["freeze"]
    if freeze["status"] == "FROZEN" and not _is_rfc3339(freeze.get("frozen_at")):
        diagnostic = ContractDiagnostic(
            "FREEZE_TIME_INVALID", f"frozen_at must be an RFC3339 date-time, got {freeze.get('frozen_at')!r}"
        )
        # FREEZE_TIME_INVALID immediately precedes FREEZE_HASH_MISMATCH, the baseline's last Stage 2 code.
        at_end = not stage2 or stage2[-1].code != "FREEZE_HASH_MISMATCH"
        stage2.insert(len(stage2) if at_end else len(stage2) - 1, diagnostic)
    errors.extend(stage2)


def _check_quotient(document: Mapping[str, Any], errors: list[Any]) -> None:
    evidence = document["report"]["evidence"]
    if evidence["status"] != "CHECKED_FINITE_EXPLICIT":
        return
    tables = _explicit_tables(document, errors)
    if tables is None:
        return
    case_ids, behavior, _representation = tables
    # Classes are the declared entries, identified by position: a repeated class id must not merge
    # two declared classes into one (which would certify a split partition as the exact quotient).
    membership: dict[str, int] = {}
    class_ids: set[str] = set()
    overlapping: set[str] = set()
    for index, cls in enumerate(evidence["classes"]):
        class_id = str(cls["id"])
        if class_id in class_ids:
            errors.append(ContractDiagnostic("DUPLICATE_QUOTIENT_CLASS", f"quotient class id {class_id} is declared more than once", ("report", "evidence", "classes", index)))
        class_ids.add(class_id)
        for case_id in cls["case_ids"]:
            case_id = str(case_id)
            if case_id in membership:
                errors.append(ContractDiagnostic("QUOTIENT_OVERLAP", f"case {case_id} occurs in more than one quotient class"))
                overlapping.add(case_id)
            membership[case_id] = index
    expected = set(case_ids)
    if set(membership) != expected or overlapping:
        # Overlapping classes are not a partition either; pairwise class relations over them would
        # be computed from an arbitrary assignment, so the check stops here.
        errors.append(ContractDiagnostic("QUOTIENT_NOT_PARTITION", f"quotient classes must partition source_domain missing={sorted(expected-set(membership))} extra={sorted(set(membership)-expected)} overlapping={sorted(overlapping)}"))
        return
    for left in case_ids:
        for right in case_ids:
            same_behavior = _key(behavior[left]) == _key(behavior[right])
            same_class = membership[left] == membership[right]
            if same_class and not same_behavior:
                errors.append(ContractDiagnostic("QUOTIENT_CLASS_NOT_BEHAVIOR_CONSTANT", f"cases {left} and {right} share a class but differ in required behavior"))
            if evidence["claims_exact_observational_quotient"] and same_behavior != same_class:
                errors.append(ContractDiagnostic("QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL", f"class relation differs from beta-kernel for cases {left} and {right}"))


def validate_contract(document: object) -> Any:
    """Validate one in-memory document under far-ir/2.0 as corrected by errata 1."""
    if _non_json_numbers(document):
        # NaN and infinities are not JSON values (RFC 8259 section 6), so no schema can admit them.
        return ContractValidationResult((ContractDiagnostic("SCHEMA_CONSTRAINT_VIOLATION", "non-finite number is not a JSON value"),))
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


def load_document(path: str | Path) -> tuple[object | None, Any | None]:
    """Read and parse ``path`` exactly once as RFC 8259 JSON: ``(document, None)`` or ``(None, failure)``."""
    try:
        raw = Path(path).read_bytes()
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_strict_object, parse_constant=_reject_constant), None
    except (OSError, ValueError) as exc:  # ValueError covers JSONDecodeError and UnicodeDecodeError.
        return None, ContractValidationResult((ContractDiagnostic("UNREADABLE_CONTRACT", str(exc)),))


def load_and_validate(path: str | Path) -> Any:
    document, failure = load_document(path)
    if failure is not None:
        return failure
    return validate_contract(document)


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.contract_v2_errata1")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = load_and_validate(args.path)
    if args.json:
        print(json.dumps({"success": result.success, "diagnostics": [{"code": d.code, "message": d.message, "path": list(d.path)} for d in result.diagnostics]}, indent=2, sort_keys=True))
    else:
        print("PASS" if result.success else "FAIL")
        for diagnostic in result.diagnostics:
            print(f"{diagnostic.code}: {diagnostic.message}")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
