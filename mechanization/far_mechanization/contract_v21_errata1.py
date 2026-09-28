"""far-ir/2.1 verification as corrected by specification errata 1.

The executed ``contract_v21`` stays byte-identical: its SHA-256 is pinned by the completed
``PCA-W5`` manifest. That verifier iterates required-behavior values as a Python set in the loss
checks, so when a record has more than one ``METRIC_LOSS_DOMAIN_MISMATCH`` or
``LOSS_METRIC_MISMATCH`` their relative order varies with ``PYTHONHASHSEED``. The diagnostic
sequence is normative, so ``docs/specification/far-ir-2.1-errata-1.md`` fixes that order: for each
distinct required-behavior value in first-occurrence order of ``required_behavior.table`` rows and,
within it, each distinct declared action in first-occurrence order.

This module runs the executed verifier unchanged and puts exactly those loss-check diagnostics
into that order. Every other diagnostic, its position, and every success/failure outcome are the
executed verifier's. ``EFR-001-R2-INPUT-AMENDMENT-1.2`` names this module as the ``far-ir/2.1``
reference for the ``EFR-R2`` frozen expected result, and it is the verifier for every current
far-ir/2.1 surface.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

try:
    from .contract_v21 import (
        FORMAT_VERSION,
        REPO_ROOT,
        SCHEMA_PATH,
        Diagnostic,
        Result,
        _key,
        canonical_json,
        contract_sha256,
        validate_contract as validate_contract_executed,
    )
except ImportError:  # Loaded as a standalone file (no parent package), as the commercial bridge does.
    import importlib.util as _importlib_util
    import sys as _sys

    _EXECUTED_PATH = Path(__file__).resolve().with_name("contract_v21.py")
    _EXECUTED_NAME = f"{__name__}._executed_contract_v21"
    _spec = _importlib_util.spec_from_file_location(_EXECUTED_NAME, _EXECUTED_PATH)
    if _spec is None or _spec.loader is None:
        raise ImportError(f"cannot load executed far-ir/2.1 verifier {_EXECUTED_PATH}")
    _executed = _importlib_util.module_from_spec(_spec)
    _sys.modules[_EXECUTED_NAME] = _executed
    _spec.loader.exec_module(_executed)
    FORMAT_VERSION = _executed.FORMAT_VERSION
    REPO_ROOT = _executed.REPO_ROOT
    SCHEMA_PATH = _executed.SCHEMA_PATH
    Diagnostic = _executed.Diagnostic
    Result = _executed.Result
    _key = _executed._key
    canonical_json = _executed.canonical_json
    contract_sha256 = _executed.contract_sha256
    validate_contract_executed = _executed.validate_contract

__all__ = [
    "FORMAT_VERSION",
    "REPO_ROOT",
    "SCHEMA_PATH",
    "Diagnostic",
    "Result",
    "canonical_json",
    "contract_sha256",
    "load_and_validate",
    "validate_contract",
]

LOSS_CHECK_CODES = frozenset({"METRIC_LOSS_DOMAIN_MISMATCH", "LOSS_METRIC_MISMATCH"})


def validate_contract(document: object) -> Any:
    """Validate one in-memory document under far-ir/2.1 as corrected by errata 1."""
    result = validate_contract_executed(document)
    positions = [index for index, diagnostic in enumerate(result.diagnostics) if diagnostic.code in LOSS_CHECK_CODES]
    if len(positions) < 2:
        return result
    # Loss checks run only after Stage 1 passed, so the tables are well formed and case ids unique.
    # The executed verifier's message for each check is exactly "<truth>,<action>" in canonical JSON.
    contract = document["contract"]  # type: ignore[index]
    truths = dict.fromkeys(_key(row["value"]) for row in contract["required_behavior"]["table"])
    actions = dict.fromkeys(_key(value) for value in contract["approximation"]["loss"]["actions"])
    rank = {f"{truth},{action}": order for order, (truth, action) in enumerate((t, a) for t in truths for a in actions)}
    diagnostics = list(result.diagnostics)
    ordered = sorted((diagnostics[index] for index in positions), key=lambda diagnostic: rank[diagnostic.message])
    for index, diagnostic in zip(positions, ordered):
        diagnostics[index] = diagnostic
    return Result(tuple(diagnostics))


def load_and_validate(path: str | Path) -> Any:
    # Intake is the executed verifier's, unchanged.
    try:
        return validate_contract(json.loads(Path(path).read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        return Result((Diagnostic("UNREADABLE_CONTRACT", str(error)),))


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.contract_v21_errata1")
    parser.add_argument("path")
    args = parser.parse_args(argv)
    result = load_and_validate(args.path)
    print("PASS" if result.success else "FAIL")
    for diagnostic in result.diagnostics:
        print(f"{diagnostic.code}: {diagnostic.message}")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
