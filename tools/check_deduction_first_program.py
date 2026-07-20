#!/usr/bin/env python3
"""Validate the deduction-first dependency structure after P8 resolution."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "standard": ROOT / "docs/governance/deduction-first-research-standard.md",
    "central": ROOT / "docs/governance/central-research-program.md",
    "roadmap": ROOT / "docs/planning/deduction-first-proof-roadmap.md",
    "arch_roadmap": ROOT / "docs/planning/architecture-neutral-research-roadmap.md",
    "target_doc": ROOT / "docs/research/thm-target-001-v1.0.md",
    "target": ROOT / "theory/evaluation/thm-target-001.json",
    "ledger": ROOT / "theory/evaluation/thm-target-001-premise-ledger.json",
    "faithful_doc": ROOT / "docs/research/faithful-representation-specification-v1.0.md",
    "faithful_reg": ROOT / "theory/evaluation/faithful-representation-specification-v1.0.json",
    "p8_doc": ROOT / "docs/research/p8-theorem-role-decision-v1.0.md",
    "p8_reg": ROOT / "theory/evaluation/p8-theorem-role-decision.json",
    "gates": ROOT / "theory/evaluation/research-gates.json",
    "claims": ROOT / "theory/evaluation/central-claim-registry.json",
    "makefile": ROOT / "Makefile",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in FILES.values():
        assert path.is_file(), f"missing deduction-first artifact: {path.relative_to(ROOT)}"

    standard = FILES["standard"].read_text(encoding="utf-8")
    assert "The primary route to an answer is therefore deductive" in standard
    assert "It is not required before attempting a mathematical proof" in standard

    target = load(FILES["target"])
    assert target.get("status") == "frozen_unproved"
    assert target.get("proof_status") == "none"
    assert target.get("p8", {}).get("status") == "resolved_split"
    assert target.get("p8", {}).get("selected_value") == "split"
    assert target.get("next_required_artifact") == "S_core construction and obstruction lemma ledger"

    ledger = load(FILES["ledger"])
    assert ledger.get("version") == "1.2"
    assert ledger.get("gate_effect", {}).get("formal-theorem-target") == "satisfied"
    assert ledger.get("gate_effect", {}).get("premise-ledger-and-semantics") == "satisfied"
    assert ledger.get("gate_effect", {}).get("faithful-representation-definition") == "satisfied"
    assert "P8 mode" not in ledger.get("open_items", [])

    p8 = load(FILES["p8_reg"])
    assert p8.get("selected_mode") == "split"
    assert p8.get("proof_status") == "none"
    assert p8["external_obligation"]["not_implied_by_formal_representation"] is True

    gates = load(FILES["gates"])
    assert gates.get("research_mode") == "deduction_first_with_parallel_empirical_validation"
    required = set(gates.get("required_canonical_artifacts", []))
    for relative in (
        "docs/research/thm-target-001-v1.0.md",
        "docs/research/faithful-representation-specification-v1.0.md",
        "docs/research/p8-theorem-role-decision-v1.0.md",
        "theory/evaluation/p8-theorem-role-decision.json",
    ):
        assert relative in required
    by_name = {g["name"]: g for g in gates.get("gates", [])}
    assert by_name["formal-theorem-target"]["status"] == "satisfied"
    assert by_name["premise-ledger-and-semantics"]["status"] == "satisfied"
    assert by_name["faithful-representation-definition"]["status"] == "satisfied"
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["independent-replication"]["required_before"] == ["independent_empirical_confirmation_claim"]

    claims = load(FILES["claims"])
    assert claims.get("research_mode") == "deduction_first_with_separate_validation_dimensions"
    for claim in claims.get("claims", []):
        if claim.get("id") in {"CLM-EXISTENCE", "CLM-UNIVERSALITY", "CLM-NECESSITY", "CLM-MINIMALITY"}:
            assert claim.get("current_status") != "supported"

    makefile = FILES["makefile"].read_text(encoding="utf-8")
    assert makefile.count("python tools/check_p8_theorem_role.py") == 3
    assert makefile.count("python tools/check_faithful_representation.py") == 3

    print("Deduction-first research program: PASS (P8 split; lemma stage next)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
