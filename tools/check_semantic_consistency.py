#!/usr/bin/env python3
"""Validate the canonical semantic registry and its documentary contracts."""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/governance/semantic-consistency.json"


def validate() -> list[str]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    errors: list[str] = []
    order = data["dependency_order"]
    rank = {name: index for index, name in enumerate(order)}
    if len(rank) != len(order):
        errors.append("dependency_order contains duplicates")
    for dependent, prerequisite in data["dependencies"]:
        if dependent not in rank or prerequisite not in rank:
            errors.append(f"unknown dependency layer: {dependent} -> {prerequisite}")
        elif rank[prerequisite] >= rank[dependent]:
            errors.append(f"reversed/circular dependency: {dependent} -> {prerequisite}")

    terms = [entry["term"] for entry in data["canonical_terms"]]
    duplicates = sorted({term for term in terms if terms.count(term) > 1})
    if duplicates:
        errors.append("duplicate canonical term ownership: " + ", ".join(duplicates))
    allowed_statuses = {"schema-role", "contract-role", "contract-parameter", "derived", "derived-procedural", "derived-materialized-view", "theory-constrained-method", "workflow-verb", "independent-method", "protocol-artifact", "decision-rule"}
    for entry in data["canonical_terms"]:
        if not entry.get("owner") or entry.get("status") not in allowed_statuses:
            errors.append(f"unclassified canonical term: {entry.get('term')}")

    claim_ids = [claim["id"] for claim in data["strong_claims"]]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("duplicate strong-claim identifier")
    for claim in data["strong_claims"]:
        if not claim.get("status") or not claim.get("scope"):
            errors.append(f"strong claim lacks status/scope: {claim.get('id')}")

    required_procedures = {"FAR workflow", "canonicalization", "Pareto comparison", "fail report", "uncertainty output"}
    if missing := required_procedures - set(data["procedures"]):
        errors.append("unclassified procedure(s): " + ", ".join(sorted(missing)))
    if not data.get("theorem_families"):
        errors.append("theorem/proof families are not classified")
    for relative in data["required_documents"]:
        if not (ROOT / relative).is_file():
            errors.append(f"missing canonical audit document: {relative}")

    active = [ROOT / "README.md", ROOT / "docs/ARCHITECTURE.md", ROOT / "docs/CANONICAL_MAP.md"]
    for path in active:
        text = path.read_text(encoding="utf-8")
        if "Accepted Root Theory" in text or "the Meta-Theory depends" in text:
            errors.append(f"active canonical document promotes legacy terminology: {path.relative_to(ROOT)}")
    terminology = (ROOT / "docs/glossary/canonical-terminology.md").read_text(encoding="utf-8")
    for term in terms:
        if f"| {term} |" not in terminology:
            errors.append(f"registry term missing from terminology authority: {term}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("semantic consistency: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("semantic consistency: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
