#!/usr/bin/env python3
"""Validate the deduction-first research dependency structure."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STANDARD = ROOT / "docs/governance/deduction-first-research-standard.md"
CENTRAL = ROOT / "docs/governance/central-research-program.md"
PRIORITY = ROOT / "docs/governance/research-priority-reset.md"
ANTI_SELF_CLARIFICATION = ROOT / "docs/governance/anti-self-validation-deduction-clarification.md"
PROOF_ROADMAP = ROOT / "docs/planning/deduction-first-proof-roadmap.md"
ARCH_ROADMAP = ROOT / "docs/planning/architecture-neutral-research-roadmap.md"
THEOREM_DOC = ROOT / "docs/research/thm-target-001-v1.0.md"
THEOREM_REGISTRY = ROOT / "theory/evaluation/thm-target-001.json"
PREMISE_LEDGER = ROOT / "theory/evaluation/thm-target-001-premise-ledger.json"
THEOREM_CHECKER = ROOT / "tools/check_thm_target_001.py"
NEXT_ACTIONS = ROOT / "docs/planning/next-actions.md"
PROJECT_STATUS = ROOT / "docs/reports/project-status-generated.md"
README = ROOT / "README.md"
MAKEFILE = ROOT / "Makefile"
GATES = ROOT / "theory/evaluation/research-gates.json"
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"
NEXT_GENERATOR = ROOT / "tools/generate_next_tasks.py"
STATUS_GENERATOR = ROOT / "tools/project_status_report.py"
DASHBOARD_GENERATOR = ROOT / "tools/update_readme_dashboard.py"
PLANNER = ROOT / "tools/self_advancement_plan.py"

REQUIRED_FILES = [
    STANDARD,
    CENTRAL,
    PRIORITY,
    ANTI_SELF_CLARIFICATION,
    PROOF_ROADMAP,
    ARCH_ROADMAP,
    THEOREM_DOC,
    THEOREM_REGISTRY,
    PREMISE_LEDGER,
    THEOREM_CHECKER,
    NEXT_ACTIONS,
    PROJECT_STATUS,
    README,
    MAKEFILE,
    GATES,
    CLAIMS,
    NEXT_GENERATOR,
    STATUS_GENERATOR,
    DASHBOARD_GENERATOR,
    PLANNER,
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_phrases(path: Path, phrases: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        assert phrase in text, f"{path.relative_to(ROOT)} missing required phrase: {phrase}"


def prohibit_phrases(path: Path, phrases: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        assert phrase not in text, f"{path.relative_to(ROOT)} retains obsolete phrase: {phrase}"


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
            "THM-TARGET-001",
        ],
    )
    require_phrases(
        PRIORITY,
        [
            "`THM-TARGET-001` and its premise ledger are now frozen",
            "The immediate objective is to formalize the faithful-representation relation and resolve P8",
            "Independent validation strengthens confidence in the result",
        ],
    )
    require_phrases(
        ANTI_SELF_CLARIFICATION,
        [
            "The Anti-Self-Validation Standard does not prohibit Project FAR authors",
            "independent empirical replication must occur before a representation theorem may be attempted",
            "independent replication is required before claiming independent empirical confirmation",
            "formal theorem gates are required before claiming a theorem",
        ],
    )
    require_phrases(
        THEOREM_DOC,
        [
            "Frozen prospective theorem target and premise boundary",
            "Finite explicit core `S_core`",
            "General extension class `S_IRD`",
            "THM-CORE-REP-001",
            "THM-IMP-001",
            "This artifact does not establish",
        ],
    )
    require_phrases(
        PROOF_ROADMAP,
        [
            "Independent empirical replication is a parallel supporting track",
            "Stage D1 — Freeze the theorem target",
            "Status:** complete prospectively",
            "Stage D3 — Formalize faithful representation",
            "Status:** active immediate stage",
        ],
    )
    require_phrases(
        ARCH_ROADMAP,
        [
            "## Milestone 6 — THM-TARGET-001 theorem target and premise ledger",
            "**Status:** complete prospectively",
            "## Milestone 7 — Faithful-representation formalization",
            "**Status:** active immediate milestone",
            "PBTS-001 replication proceeds in parallel",
        ],
    )
    require_phrases(
        README,
        [
            "The project is now deduction-first",
            "THM-TARGET-001",
            "faithful-representation formalization and P8 resolution",
            "They do not serve as prerequisites for constructing a proof",
        ],
    )
    require_phrases(
        NEXT_ACTIONS,
        [
            "### STRATEGIC-001: Formalize faithful representation and nontriviality",
            "### STRATEGIC-002: Resolve the formal role of P8",
            "### STRATEGIC-003: Build the S_core construction and obstruction ledger",
            "THM-TARGET-001 is frozen",
        ],
    )
    require_phrases(
        PROJECT_STATUS,
        [
            "## Current Research Mode",
            "Primary mode: deduction-first with parallel empirical validation",
            "Frozen central artifact: `THM-TARGET-001` v1.0",
            "Formal-theorem-target gate: satisfied",
            "Premise-ledger-and-semantics gate: in progress",
            "Current theorem status: no representation theorem",
        ],
    )
    require_phrases(
        NEXT_GENERATOR,
        [
            "Generate the active deduction-first strategic task queue",
            "Formalize faithful representation and nontriviality",
            "Resolve the formal role of P8",
            "THM-TARGET-001 is frozen",
        ],
    )
    require_phrases(
        STATUS_GENERATOR,
        [
            "Frozen central artifact: `THM-TARGET-001` v1.0",
            "Immediate central work: formalize `Pres_1` through `Pres_7` and `Faithful_m8`, then resolve P8",
        ],
    )
    require_phrases(
        DASHBOARD_GENERATOR,
        [
            "Current project phase: faithful-representation formalization and P8 resolution",
            "In-progress work: formalize Pres_1 through Pres_7 and Faithful_m8; resolve P8",
            "Parallel supporting work: PBTS-001 independent replication",
        ],
    )
    require_phrases(MAKEFILE, ["python tools/check_thm_target_001.py"])
    require_phrases(PLANNER, ["(?:TASK|STRATEGIC)"])

    obsolete = [
        "Blocked until Milestone 5 produces three valid independent primary submissions",
        "Valid independent replication or a separately frozen PB revision precedes representation-theorem work",
        "Independent replication is now the primary evidential bottleneck",
        "Current project phase: post-CRE-001 prospective semantics baseline; CRE-002 preparation",
        "Plan independent replication of CRE-002-EXT-001",
        "Current project phase: deduction-first theorem-target freeze",
        "In-progress work: freeze THM-TARGET-001 and its premise ledger",
    ]
    for path in [ARCH_ROADMAP, NEXT_ACTIONS, PROJECT_STATUS, README, NEXT_GENERATOR, STATUS_GENERATOR, DASHBOARD_GENERATOR]:
        prohibit_phrases(path, obsolete)

    gates = read_json(GATES)
    assert gates.get("research_mode") == "deduction_first_with_parallel_empirical_validation"
    required_artifacts = set(gates.get("required_canonical_artifacts", []))
    assert {
        "docs/research/thm-target-001-v1.0.md",
        "theory/evaluation/thm-target-001.json",
        "theory/evaluation/thm-target-001-premise-ledger.json",
    } <= required_artifacts
    policy = gates.get("claim_policy", {})
    assert policy.get("proof_construction_not_blocked_by_empirical_replication") is True
    assert policy.get("independent_replication_gates_only_independent_empirical_confirmation") is True
    assert policy.get("experimental_evidence_is_not_deductive_proof") is True
    assert policy.get("independent_review_is_separate_claim_dimension") is True

    by_name = {gate.get("name"): gate for gate in gates.get("gates", [])}
    assert by_name["independent-replication"].get("required_before") == ["independent_empirical_confirmation_claim"]

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

    formal_target = by_name["formal-theorem-target"]
    assert formal_target.get("status") == "satisfied"
    assert set(formal_target.get("evidence", [])) == {
        "docs/research/thm-target-001-v1.0.md",
        "theory/evaluation/thm-target-001.json",
        "theory/evaluation/thm-target-001-premise-ledger.json",
    }
    assert by_name["premise-ledger-and-semantics"].get("status") == "in_progress"
    for name in required_theorem_gates - {"formal-theorem-target", "premise-ledger-and-semantics"}:
        assert by_name[name].get("status") != "satisfied", f"{name} has no registered proof evidence yet"

    target = read_json(THEOREM_REGISTRY)
    assert target.get("status") == "frozen_unproved"
    assert target.get("proof_status") == "none"
    assert target.get("p8", {}).get("status") == "unresolved_theorem_parameter"

    ledger = read_json(PREMISE_LEDGER)
    assert ledger.get("status") == "frozen_with_explicit_open_parameters"
    assert ledger.get("gate_effect", {}).get("formal-theorem-target") == "satisfied"
    assert ledger.get("gate_effect", {}).get("premise-ledger-and-semantics") == "in_progress"

    claims = read_json(CLAIMS)
    assert claims.get("research_mode") == "deduction_first_with_separate_validation_dimensions"
    assert "docs/research/thm-target-001-v1.0.md" in claims.get("governing_documents", [])
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
