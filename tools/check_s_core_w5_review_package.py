#!/usr/bin/env python3
"""Validate the frozen S_core W5 independent proof-review package."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/s-core-w5-independent-review-package-v1.0.json"
PACKAGE = ROOT / "docs/review/s-core-w5-independent-proof-review-package-v1.0.md"
FORM = ROOT / "docs/templates/s-core-w5-independent-proof-review-form-v1.0.md"
AUDIT = ROOT / "docs/audits/s-core-w5-independent-review-package-audit.md"

EXPECTED_OUTCOMES = {"verified", "verified_with_errata", "not_verified", "inconclusive"}
REQUIRED_DIMENSIONS = {
    "scope_and_quantification",
    "definition_independence_and_non_circularity",
    "assumption_completeness",
    "uniform_constructor_totality",
    "P1_through_P8I_preservation",
    "history_and_dependency_fidelity",
    "nontriviality_and_hidden_machinery",
    "proof_dependency_soundness",
    "lean_statement_alignment",
    "countermodel_and_boundary_search",
    "claim_boundary_compliance",
}
REQUIRED_NONCLAIMS = {
    "independent_proof_verification",
    "S_IRD_representation",
    "primitive_necessity",
    "minimality",
    "uniqueness",
    "universal_structure",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    for path in (REGISTRY, PACKAGE, FORM, AUDIT):
        require(path.is_file(), f"missing review-package artifact: {path.relative_to(ROOT)}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    require(data.get("package_id") == "SCORE-W5-REVIEW-001", "wrong package id")
    require(data.get("status") == "frozen_review_package", "package must be frozen")
    require(data.get("theorem_id") == "THM-CORE-REP-001", "wrong theorem id")
    require(data.get("theorem_scope") == "S_core", "review scope must remain S_core")
    require(data.get("proof_status") == "proved_for_S_core", "bounded proof status missing")
    require(data.get("independent_review_status") == "not_started", "package must not claim completed review")
    require(set(data.get("review_outcomes", [])) == EXPECTED_OUTCOMES, "review outcomes changed")
    require(REQUIRED_DIMENSIONS <= set(data.get("review_dimensions", [])), "review dimensions incomplete")
    require(REQUIRED_NONCLAIMS <= set(data.get("unsupported_claims", [])), "required nonclaims missing")

    paths = [item.get("path") for item in data.get("required_source_artifacts", [])]
    require(len(paths) == len(set(paths)), "duplicate source artifact")
    require(len(paths) >= 14, "review package source list is incomplete")
    for rel in paths:
        require(isinstance(rel, str) and rel, "invalid source artifact path")
        require((ROOT / rel).is_file(), f"missing frozen source artifact: {rel}")

    blob_bound = {
        item["path"]: item.get("git_blob_sha")
        for item in data["required_source_artifacts"]
        if item.get("git_blob_sha")
    }
    require(
        blob_bound.get("theory/evaluation/s-core-w5-theorem-assembly-proof.json")
        == "f51409aff1b27ea08e1876ff7f760edc4ec12439",
        "W5 assembly registry binding changed",
    )
    require(
        blob_bound.get("theory/evaluation/s-core-w5-lean-mechanization.json")
        == "7089104b7395d3d8fca024dbf639c8b7547dd707",
        "W5 mechanization registry binding changed",
    )

    package_text = PACKAGE.read_text(encoding="utf-8")
    form_text = FORM.read_text(encoding="utf-8")
    for phrase in (
        "Review has not been executed",
        "RG-15",
        "in-scope counterexample",
        "strictly simpler equivalent target",
        "does not establish independent verification",
    ):
        require(phrase in package_text, f"package boundary missing: {phrase}")
    for outcome in EXPECTED_OUTCOMES:
        require(outcome in form_text, f"review form missing outcome: {outcome}")
    require("Do not delete resolved objections" in form_text, "objection preservation rule missing")

    print("S_core W5 independent review package: valid and frozen; review not executed")


if __name__ == "__main__":
    main()
