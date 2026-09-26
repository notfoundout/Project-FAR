"""Current far-ir/2.0 verification, rule v1.1: errata 1 plus the determinate-outcome rule.

Rule v1.0 (``contract_v2_strict``) is the frozen baseline ``contract_v2`` followed by one rule: a
``PROVED`` or ``REFUTED`` outcome is accepted only with ``CHECKED_FINITE_EXPLICIT`` evidence. The
``EFR-001`` comparator amendment v2.0 binds that module by git blob, so it stays byte-identical.

Rule v1.1 applies the same determinate-outcome rule, taken unchanged from ``contract_v2_strict``,
to ``contract_v2_errata1`` instead of the baseline: strict RFC 8259 intake, positional quotient
class identity, overlap as non-partition, and ``FREEZE_TIME_INVALID``
(``docs/specification/far-ir-2.0-errata-1.md``). It is the verifier for every current far-ir/2.0
surface; see ``docs/specification/far-ir-2.0-current-verification.md``.

A file is read and parsed exactly once; errata 1 and the determinate-outcome rule always apply to
the same in-memory document.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

try:
    from .contract_v2_errata1 import (
        FORMAT_VERSION,
        REPO_ROOT,
        SCHEMA_PATH,
        ContractDiagnostic,
        ContractValidationResult,
        canonical_json,
        contract_sha256,
        load_document,
        validate_contract as validate_contract_errata1,
    )
    from .contract_v2_strict import _strict_diagnostics as _rule_v1_0_diagnostics
except ImportError:  # Loaded as a standalone file (no parent package), as the commercial bridge does.
    import importlib.util as _importlib_util
    import sys as _sys

    def _load_sibling(filename: str, suffix: str) -> Any:
        path = Path(__file__).resolve().with_name(filename)
        name = f"{__name__}.{suffix}"
        spec = _importlib_util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load far-ir/2.0 verifier {path}")
        module = _importlib_util.module_from_spec(spec)
        _sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    _errata1 = _load_sibling("contract_v2_errata1.py", "_errata1")
    _rule_v1_0 = _load_sibling("contract_v2_strict.py", "_rule_v1_0")
    FORMAT_VERSION = _errata1.FORMAT_VERSION
    REPO_ROOT = _errata1.REPO_ROOT
    SCHEMA_PATH = _errata1.SCHEMA_PATH
    ContractDiagnostic = _errata1.ContractDiagnostic
    ContractValidationResult = _errata1.ContractValidationResult
    canonical_json = _errata1.canonical_json
    contract_sha256 = _errata1.contract_sha256
    load_document = _errata1.load_document
    validate_contract_errata1 = _errata1.validate_contract
    _rule_v1_0_diagnostics = _rule_v1_0._strict_diagnostics

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


def validate_contract(document: object) -> Any:
    """Validate one in-memory document under current (rule v1.1) far-ir/2.0 semantics."""
    corrected = validate_contract_errata1(document)
    # Re-created in this module's diagnostic type: standalone loading gives rule v1.0 its own baseline copy.
    determinate = tuple(ContractDiagnostic(d.code, d.message, d.path) for d in _rule_v1_0_diagnostics(document))
    return ContractValidationResult(corrected.diagnostics + determinate)


def load_and_validate(path: str | Path) -> Any:
    document, failure = load_document(path)
    if failure is not None:
        return failure
    return validate_contract(document)


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.contract_v2_strict_v11")
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
