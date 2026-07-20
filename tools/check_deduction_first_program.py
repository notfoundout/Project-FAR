#!/usr/bin/env python3
"""Validate the deduction-first dependency structure after the W0 source proof."""
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
    "premises": ROOT / "theory/evaluation/thm-target-001-premise-ledger.json",
    "faithful_doc": ROOT / "docs/research/faithful-representation-specification-v1.0.md",
    "faithful_reg": ROOT / "theory/evaluation/faithful-representation-specification-v1.0.json",
    "p8_doc": ROOT / "docs/research/p8-theorem-role-decision-v1.0.md",
    "p8_reg": ROOT / "theory/evaluation/p8-theorem-role-decision.json",
    "lemma_doc": ROOT / "docs/research/s-core-construction-obstruction-ledger-v1.0.md",
    "lemma_reg": ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json",
    "w0_doc": ROOT / "docs/research/s-core-w0-normalization-proof-v1.0.md",
    "w0_reg": ROOT / "theory/evaluation/s-core-w0-normalization-proof.json",
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

    central = FILES["central"].read_text(encoding="utf-8")
    assert "SCORE-LEMMA-LEDGER-001" in central
    assert "W0" in central
    assert "W1" in central

    roadmap = FILES["roadmap"].read_text(encoding="utf-8")
    assert "Stage D4 — Construction and obstruction lemmas" in roadmap
    assert "**Status:** active" in roadmap
    assert "W0" in roadmap
    assert "W1" in roadmap

    arch_roadmap = FILES["arch_roadmap"].read_text(encoding="utf-8")
    assert "Milestone 8 — Construction and obstruction lemmas" in arch_roadmap
    assert "W0" in arch_roadmap
    assert "W1" in arch_roadmap

    target = load(FILES["target"])
    assert target.get("status") == "frozen_unproved"
    assert target.get("proof_status") == "partial_lemmas_only"
    assert target.get("machine_check_status") == "bounded_executable_reference_only"
    assert target.get("p8", {}).get("status") == "resolved_split"
    assert target.get("p8", {}).get("selected_value") == "split"
    assert target.get("next_required_artifact") == "W1 base-carrier and direct-axis construction proof package"
    program = target.get("lemma_program", {})
    assert program.get("status") == "w0_complete_w1_active"
    assert program.get("total_obligations") == 37
    assert program.get("proved_obligations") == 4
    assert program.get("established_scope_boundaries") == 1
    assert program.get("open_obligations") == 32
    assert program.get("completed_waves") == ["W0"]
    assert set(program.get("active_obligations", [])) == {"LEM-SC-005", "LEM-SC-006", "LEM-SC-007", "LEM-SC-008", "LEM-SC-009", "LEM-SC-012", "LEM-SC-014"}

    premises = load(FILES["premises"])
    assert premises.get("version") in {"1.2", "1.3"}
    assert premises.get("gate_effect", {}).get("formal-theorem-target") == "satisfied"
    assert premises.get("gate_effect", {}).get("premise-ledger-and-semantics") == "satisfied"
    assert premises.get("gate_effect", {}).get("faithful-representation-definition") == "satisfied"
    assert "P8 mode" not in premises.get("open_items", [])

    p8 = load(FILES["p8_reg"])
    assert p8.get("selected_mode") == "split"
    assert p8["external_obligation"]["not_implied_by_formal_representation"] is True

    lemma = load(FILES["lemma_reg"])
    assert lemma.get("ledger_id") == "SCORE-LEMMA-LEDGER-001"
    assert lemma.get("status") == "frozen_dependency_decomposition_w0_complete_w1_active"
    summary = lemma.get("execution_summary", {})
    assert summary.get("total") == 37
    assert summary.get("proved") == 4
    assert summary.get("scope_boundary_established") == 1
    assert summary.get("open") == 32
    by_id = {item["id"]: item for item in lemma.get("obligations", [])}
    assert all(by_id[item_id].get("status") == "proved" for item_id in ("LEM-SC-001", "LEM-SC-002", "LEM-SC-003", "LEM-SC-004"))
    assert by_id["OBS-SC-001"].get("status") == "scope_boundary_established"

    w0 = load(FILES["w0_reg"])
    assert w0.get("proof_id") == "SCORE-W0-PROOF-001"
    assert w0.get("status") == "project_authored_human_checkable_proof"
    assert w0.get("ledger_effect", {}).get("active_wave") == "W1"
    assert w0.get("verification", {}).get("proof_assistant_status") == "not_started"
    assert w0.get("verification", {}).get("independent_review_status") == "not_started"

    gates = load(FILES["gates"])
    assert gates.get("research_mode") == "deduction_first_with_parallel_empirical_validation"
    required = set(gates.get("required_canonical_artifacts", []))
    for relative in (
        "docs/research/thm-target-001-v1.0.md",
        "docs/research/faithful-representation-specification-v1.0.md",
        "docs/research/p8-theorem-role-decision-v1.0.md",
        "docs/research/s-core-construction-obstruction-ledger-v1.0.md",
        "theory/evaluation/s-core-construction-obstruction-ledger.json",
        "docs/research/s-core-w0-normalization-proof-v1.0.md",
        "theory/evaluation/s-core-w0-normalization-proof.json",
    ):
        assert relative in required
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["formal-theorem-target"]["status"] == "satisfied"
    assert by_name["premise-ledger-and-semantics"]["status"] == "satisfied"
    assert by_name["faithful-representation-definition"]["status"] == "satisfied"
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["scoped-representation-proof"]["evidence"] == []
    assert by_name["mechanized-proof-verification"]["status"] == "not_satisfied"
    assert by_name["independent-proof-review"]["status"] == "not_satisfied"
    assert by_name["independent-replication"]["required_before"] == ["independent_empirical_confirmation_claim"]

    claims = load(FILES["claims"])
    assert claims.get("research_mode") == "deduction_first_with_separate_validation_dimensions"
    for claim in claims.get("claims", []):
        if claim.get("id") in {"CLM-EXISTENCE", "CLM-UNIVERSALITY", "CLM-NECESSITY", "CLM-MINIMALITY"}:
            assert claim.get("current_status") != "supported"

    makefile = FILES["makefile"].read_text(encoding="utf-8")
    for checker in (
        "check_faithful_representation.py",
        "check_p8_theorem_role.py",
        "check_s_core_lemma_ledger.py",
        "check_s_core_w0.py",
    ):
        assert makefile.count(f"python tools/{checker}") == 3

    print("Deduction-first research program: PASS (W0 complete; W1 active; theorem gate closed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
