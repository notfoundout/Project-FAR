#!/usr/bin/env python3
"""Validate the deduction-first research dependency structure."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STANDARD = ROOT / "docs/governance/deduction-first-research-standard.md"
CENTRAL = ROOT / "docs/governance/central-research-program.md"
PRIORITY = ROOT / "docs/governance/research-priority-reset.md"
PROOF_ROADMAP = ROOT / "docs/planning/deduction-first-proof-roadmap.md"
ARCH_ROADMAP = ROOT / "docs/planning/architecture-neutral-research-roadmap.md"
README = ROOT / "README.md"
GATES = ROOT / "theory/evaluation/research-gates.json"
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"

REQUIRED_FILES = [
    STANDARD,
    CENTRAL,
    PRIORITY,
    PROOF_ROADMAP,
    ARCH_ROADMAP,
    README,
    GATES,
    CLAIMS,
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_phrases(path: Path, phrases: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        assert phrase in text, f"{path.relative_to(ROOT)} missing required phrase: {phrase}"


def main() -> int:
    for path in REQUIRED_FILES:
        assert path.is_file(), f"missing required deduction-first artifact: {path.relative_to(ROOT)}"

    require_phrases(
        STANDARD,
        [
            "The primary route to an answer is therefore deductive",
            "do not gate construction of a proof",
            "Independent replication remains required before claiming independent empirical confirmation",
            "It is not required before attempting a mathematical proof",
        ],
    )
    require_phrases(
        CENTRAL,
        [
            "The primary route to an answer is therefore deduction",
            "They do not gate drafting, proving, refuting, or mechanizing a theorem",
            "The immediate central task is to freeze the scoped representation-theorem target and premise ledger",
        ],
    )
    require_phrases(
        PRIORITY,
        [
            "The next milestone is a frozen theorem target and premise ledger",
            "recruitment is no longer the immediate central dependency",
            "Independent validation strengthens confidence in the result",
        ],
    )
    require_phrases(
        PROOF_ROADMAP,
        [
            "Independent empirical replication is a parallel supporting track",
            "Create and freeze `THM-TARGET-001`",
            "They may not be used as a substitute for D1-D8",
        ],
    )
    require_phrases(
        ARCH_ROADMAP,
        [
            "parallel and nonblocking for theorem construction",
            "## Milestone 6 — THM-TARGET-001 theorem target and premise ledger",
            "PBTS-001 replication proceeds in parallel",
        ],
    )
    require_phrases(
        README,
        [
            "The project is now deduction-first",
            "The active objective is to freeze `THM-TARGET-001`",
            "They do not serve as prerequisites for constructing a proof",
        ],
    )

    arch_text = ARCH_ROADMAP.read_text(encoding="utf-8")
    assert "Blocked until Milestone 5 produces three valid independent primary submissions" not in arch_text
    assert "Valid independent replication or a separately frozen PB revision precedes representation-theorem work" not in arch_text

    gates = read_json(GATES)
    assert gates.get("research_mode") == "deduction_first_with_parallel_empirical_validation"
    policy = gates.get("claim_policy", {})
    assert policy.get("proof_construction_not_blocked_by_empirical_replication") is True
    assert policy.get("independent_replication_gates_only_independent_empirical_confirmation") is True
    assert policy.get("experimental_evidence_is_not_deductive_proof") is True
    assert policy.get("independent_review_is_separate_claim_dimension") is True

    by_name = {gate.get("name"): gate for gate in gates.get("gates", [])}
    replication = by_name["independent-replication"]
    assert replication.get("required_before") == ["independent_empirical_confirmation_claim"]

    required_theorem_gates = {
        "formal-theorem-target",
        "premise-ledger-and-semantics",
        "faithful-representation-definition",
        "scoped-representation-proof",
        "primitive-lower-bounds",
        "minimality-universe-and-proof",
        "mechanized-proof-verification",
        "independent-proof-review",
    }
    assert required_theorem_gates <= set(by_name)
    for name in required_theorem_gates:
        assert by_name[name].get("standard") == "docs/governance/deduction-first-research-standard.md"
        assert by_name[name].get("status") != "satisfied", f"{name} has no registered evidence yet"

    claims = read_json(CLAIMS)
    assert claims.get("research_mode") == "deduction_first_with_separate_validation_dimensions"
    dimensions = claims.get("claim_dimensions", {})
    assert {
        "theorem_status",
        "mechanization_status",
        "independent_proof_review_status",
        "empirical_replication_status",
        "application_status",
    } <= set(dimensions)

    for claim in claims.get("claims", []):
        assert claim.get("primary_resolution_mode"), f"{claim.get('id')} missing primary resolution mode"
        assert claim.get("supporting_validation"), f"{claim.get('id')} missing supporting validation"

    assert all(
        claim.get("current_status") not in {"supported"}
        for claim in claims.get("claims", [])
        if claim.get("id") in {
            "CLM-EXISTENCE",
            "CLM-UNIVERSALITY",
            "CLM-NECESSITY",
            "CLM-MINIMALITY",
        }
    )

    print("Deduction-first research program: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
