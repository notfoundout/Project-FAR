"""Current authoritative far-ir/2.0 verification: determinate outcomes must be machine-checked.

The baseline verifier in ``contract_v2`` recomputes factorization, collision, and quotient
claims only when ``report.evidence.status`` is ``CHECKED_FINITE_EXPLICIT`` (specification
section 9, Stage 3). A record whose evidence is ``DECLARED_UNCHECKED`` therefore passes the
baseline with ``outcome = PROVED`` or ``REFUTED`` even when its own explicit tables contradict
that outcome: baseline ``success`` means well-formed, not verified.

This module is the verifier for every current far-ir/2.0 surface (conformance, migration, the
commercial semantic audit, and any new campaign). It runs the unchanged baseline and adds one
rule: a ``PROVED`` or ``REFUTED`` outcome is accepted only with ``CHECKED_FINITE_EXPLICIT``
evidence, so every determinate outcome is one the verifier actually recomputed. Non-determinate
outcomes (``OPEN``, ``Unknown``, and the other schema values) are unaffected.

``contract_v2.py`` stays byte-identical because it is git-blob pinned as the preregistered
``PCA-W6`` protocol base and is the baseline command frozen by ``EFR-001`` v1.0. Using it
directly is reserved for reproducing those historical records; the registry in
``verifier_authority`` and ``tests/test_contract_v2_verifier_authority.py`` enforce that split.

A file is read and parsed exactly once; baseline and strict rules always apply to the same
in-memory document.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from .contract_v2 import (
        FORMAT_VERSION,
        REPO_ROOT,
        SCHEMA_PATH,
        ContractDiagnostic,
        ContractValidationResult,
        canonical_json,
        contract_sha256,
        validate_contract as validate_contract_baseline,
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
    canonical_json = _baseline.canonical_json
    contract_sha256 = _baseline.contract_sha256
    validate_contract_baseline = _baseline.validate_contract

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

DETERMINATE_OUTCOMES = frozenset({"PROVED", "REFUTED"})
CHECKED_STATUS = "CHECKED_FINITE_EXPLICIT"


def _strict_diagnostics(document: object) -> list[Any]:
    if not isinstance(document, Mapping):
        return []
    report = document.get("report")
    if not isinstance(report, Mapping):
        return []
    evidence = report.get("evidence")
    status = evidence.get("status") if isinstance(evidence, Mapping) else None
    outcome = report.get("outcome")
    if outcome in DETERMINATE_OUTCOMES and status != CHECKED_STATUS:
        return [
            ContractDiagnostic(
                "DETERMINATE_OUTCOME_UNCHECKED",
                f"outcome {outcome} requires {CHECKED_STATUS} evidence, got {status!r}",
                ("report", "evidence", "status"),
            )
        ]
    return []


def validate_contract(document: object) -> Any:
    """Validate one in-memory document under current (strict) far-ir/2.0 semantics."""
    baseline = validate_contract_baseline(document)
    return ContractValidationResult(baseline.diagnostics + tuple(_strict_diagnostics(document)))


def load_document(path: str | Path) -> tuple[object | None, Any | None]:
    """Read and parse ``path`` exactly once, returning ``(document, None)`` or ``(None, failure)``."""
    try:
        raw = Path(path).read_bytes()
        return json.loads(raw.decode("utf-8")), None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, ContractValidationResult((ContractDiagnostic("UNREADABLE_CONTRACT", str(exc)),))


def load_and_validate(path: str | Path) -> Any:
    """Single-snapshot load: the baseline and strict rules both see the same parsed document."""
    document, failure = load_document(path)
    if failure is not None:
        return failure
    return validate_contract(document)


# Explicit aliases for callers that must name the strict mode.
validate_contract_strict = validate_contract
load_and_validate_strict = load_and_validate


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.contract_v2_strict")
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
