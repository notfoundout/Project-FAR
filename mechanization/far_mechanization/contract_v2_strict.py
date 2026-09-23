"""Strict far-ir/2.0 validation: determinate outcomes must be machine-checked.

The baseline verifier in ``contract_v2`` recomputes factorization, collision, and quotient
claims only when ``report.evidence.status`` is ``CHECKED_FINITE_EXPLICIT`` (specification
section 9, Stage 3). A record whose evidence is ``DECLARED_UNCHECKED`` therefore passes the
baseline with ``outcome = PROVED`` or ``REFUTED`` even when its own explicit tables contradict
that outcome: baseline ``success`` means well-formed, not verified.

This module adds one rule on top of the unchanged baseline: a ``PROVED`` or ``REFUTED``
outcome is accepted only with ``CHECKED_FINITE_EXPLICIT`` evidence, so the determinate
outcome is always one the verifier actually recomputed. Non-determinate outcomes (``OPEN``,
``Unknown``, and the other schema values) are unaffected.

``contract_v2.py`` is git-blob pinned as the preregistered ``PCA-W6`` protocol base and is the
baseline command frozen by ``EFR-001``; this wrapper leaves it and every frozen result
unchanged. It is a stricter consumer mode, not a change to the published ``far-ir/2.0``
semantics or to any recorded campaign outcome.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence

from .contract_v2 import (
    ContractDiagnostic,
    ContractValidationResult,
    load_and_validate,
    validate_contract,
)

DETERMINATE_OUTCOMES = frozenset({"PROVED", "REFUTED"})
CHECKED_STATUS = "CHECKED_FINITE_EXPLICIT"


def _strict_diagnostics(document: object) -> list[ContractDiagnostic]:
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
                f"strict mode: outcome {outcome} requires {CHECKED_STATUS} evidence, got {status!r}",
                ("report", "evidence", "status"),
            )
        ]
    return []


def _strict(result: ContractValidationResult, document: object) -> ContractValidationResult:
    return ContractValidationResult(result.diagnostics + tuple(_strict_diagnostics(document)))


def validate_contract_strict(document: object) -> ContractValidationResult:
    return _strict(validate_contract(document), document)


def load_and_validate_strict(path: str | Path) -> ContractValidationResult:
    result = load_and_validate(path)
    if any(diagnostic.code == "UNREADABLE_CONTRACT" for diagnostic in result.diagnostics):
        return result
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    return _strict(result, document)


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.contract_v2_strict")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = load_and_validate_strict(args.path)
    if args.json:
        print(json.dumps({"success": result.success, "diagnostics": [{"code": d.code, "message": d.message, "path": list(d.path)} for d in result.diagnostics]}, indent=2, sort_keys=True))
    else:
        print("PASS" if result.success else "FAIL")
        for diagnostic in result.diagnostics:
            print(f"{diagnostic.code}: {diagnostic.message}")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
