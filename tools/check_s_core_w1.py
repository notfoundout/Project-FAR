#!/usr/bin/env python3
"""Validate SCORE-W1-PROOF-001, executable corroboration, and ledger integration."""
from __future__ import annotations

import json
from pathlib import Path

from s_core_w1_reference import DIRECT_AXES, construct_target, verify_all

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/s-core-w1-direct-axis-proof-v1.0.md"
REG = ROOT / "theory/evaluation/s-core-w1-direct-axis-proof.json"
FIXTURES = ROOT / "theory/evaluation/s-core-w1-reference-fixtures.json"
LEDGER_DOC = ROOT / "docs/research/s-core-construction-obstruction-ledger-v1.0.md"
LEDGER = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
FAITHFUL = ROOT / "theory/evaluation/faithful-representation-specification-v1.0.json"
P8 = ROOT / "theory/evaluation/p8-theorem-role-decision.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
AUDIT = ROOT / "docs/audits/s-core-w1-proof-audit.md"
TEST = ROOT / "tests/test_s_core_w1_reference.py"
REFERENCE = ROOT / "tools/s_core_w1_reference.py"
MAKEFILE = ROOT / "Makefile"

PROVED = {
    "LEM-SC-005", "LEM-SC-006", "LEM-SC-007", "LEM-SC-008",
    "LEM-SC-009", "LEM-SC-012", "LEM-SC-014",
}
REFUTED = {"OBS-SC-003", "OBS-SC-006"}
W2 = {"LEM-SC-010", "LEM-SC-011", "LEM-SC-013", "LEM-SC-015", "LEM-SC-016"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (
        DOC, REG, FIXTURES, LEDGER_DOC, LEDGER, TARGET, FAITHFUL, P8,
        GATES, AUDIT, TEST, REFERENCE, MAKEFILE,
    ):
        assert path.is_file(), f"missing W1 artifact: {path.relative_to(ROOT)}"

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "S_core W1 Direct-Axis Construction Proof v1.0",
        "SCORE-W1-PROOF-001",
        "DIR-INCIDENCE-1.0",
        "Relation reflection",
        "LEM-SC-005",
        "LEM-SC-014",
        "OBS-SC-003",
        "OBS-SC-006",
        "does not yet establish the full predicates `Pres_i`",
        "W0 and W1 are complete. W2 is active",
    ):
        assert phrase in text, f"W1 proof missing phrase: {phrase}"

    reg = load(REG)
    assert reg.get("schema_version") == "1.0"
    assert reg.get("proof_id") == "SCORE-W1-PROOF-001"
    assert reg.get("version") == "1.0"
    assert reg.get("status") == "project_authored_human_checkable_proof_complete"
    assert reg.get("construction_schema") == "DIR-INCIDENCE-1.0"
    schema = reg.get("fixed_target_schema", {})
    assert schema.get("object_representation_separation") is True
    assert schema.get("new_fara_primitive_added") is False
    assert schema.get("source_case_branching") is False
    properties = reg.get("construction_properties", {})
    for key in (
        "finite_on_S_core", "total_on_direct_axis_reducts", "source_element_injective",
        "sort_preserving", "material_sort_disjointness_preserved",
        "relation_preservation", "relation_reflection", "attribute_preservation",
        "image_accountability", "lexical_label_independent",
        "direct_axis_isomorphism_equivariant", "internal_evidence_no_upgrade",
    ):
        assert properties.get(key) is True, key
    assert properties.get("complete_global_recovery_proved") is False
    assert properties.get("complete_global_machinery_ledger_proved") is False
    results = {item["id"]: item for item in reg.get("results", [])}
    assert set(results) == PROVED | REFUTED
    assert all(results[item]["status"] == "proved" for item in PROVED)
    assert all(results[item]["status"] == "refuted" for item in REFUTED)
    assert reg.get("ledger_effect") == {
        "total": 37,
        "proved": 11,
        "obstruction_established": 0,
        "scope_boundary_established": 1,
        "refuted": 2,
        "open": 23,
        "completed_waves": ["W0", "W1"],
        "active_wave": "W2",
    }
    verification = reg.get("verification", {})
    assert verification.get("human_checkable_proof") == "complete_project_authored"
    assert verification.get("executable_reference") == "complete_bounded_corroboration"
    assert verification.get("proof_assistant") == "not_started"
    assert verification.get("independent_review") == "not_started"

    fixture = load(FIXTURES)
    assert fixture.get("fixture_set_id") == "SCORE-W1-FIXTURES-001"
    assert fixture.get("constructor_schema") == "DIR-INCIDENCE-1.0"
    assert set(fixture.get("source", {}).get("axes", {})) == set(DIRECT_AXES)
    target, correspondence = construct_target(fixture["source"])
    assert target.get("schema") == "DIR-INCIDENCE-1.0"
    assert verify_all(fixture["source"], target, correspondence)
    assert len(target.get("U", [])) == len(target.get("Rep", []))
    assert {item["id"] for item in target["U"]}.isdisjoint({item["id"] for item in target["Rep"]})

    ledger = load(LEDGER)
    assert ledger.get("status") == "frozen_dependency_decomposition_w0_w1_complete_w2_active"
    assert reg.relative_to(ROOT).as_posix() in ledger.get("proof_packages", [])
    obligations = {item["id"]: item for item in ledger.get("obligations", [])}
    for item_id in PROVED:
        assert obligations[item_id]["status"] == "proved"
        assert DOC.relative_to(ROOT).as_posix() in obligations[item_id]["evidence"]
        assert REG.relative_to(ROOT).as_posix() in obligations[item_id]["evidence"]
    for item_id in REFUTED:
        assert obligations[item_id]["status"] == "refuted"
        assert DOC.relative_to(ROOT).as_posix() in obligations[item_id]["evidence"]
        assert REG.relative_to(ROOT).as_posix() in obligations[item_id]["evidence"]
    summary = ledger.get("execution_summary", {})
    assert summary == {
        "total": 37,
        "construction": 24,
        "obstruction": 10,
        "assembly": 3,
        "proved": 11,
        "obstruction_established": 0,
        "scope_boundary_established": 1,
        "refuted": 2,
        "open": 23,
    }
    assert ledger.get("completed_waves") == ["W0", "W1"]
    assert ledger.get("active_wave") == "W2"
    assert set(ledger.get("active_obligations", [])) == W2
    assert ledger.get("next_required_artifact") == "W2 dynamics history revision and self-modification proof-or-obstruction package"

    target_reg = load(TARGET)
    program = target_reg.get("lemma_program", {})
    assert program.get("status") == "w0_w1_complete_w2_active"
    assert program.get("proved_obligations") == 11
    assert program.get("refuted_obstructions") == 2
    assert program.get("scope_boundaries_established") == 1
    assert program.get("open_obligations") == 23
    assert program.get("active_wave") == "W2"
    assert set(program.get("active_obligations", [])) == W2
    assert target_reg.get("proof_status") == "partial_lemma_progress_only"
    assert target_reg.get("next_required_artifact") == ledger.get("next_required_artifact")

    faithful = load(FAITHFUL)
    assert faithful.get("w1_direct_axis_proof_registry") == REG.relative_to(ROOT).as_posix()
    assert faithful.get("direct_axis_construction_status") == "proved_without_global_recovery"
    assert faithful.get("next_required_artifact") == ledger.get("next_required_artifact")

    p8 = load(P8)
    assert p8.get("w1_direct_axis_proof_registry") == REG.relative_to(ROOT).as_posix()
    assert p8.get("internal_construction_status") == "direct_axis_embedding_proved_recovery_unproved"
    assert p8.get("external_obligation", {}).get("not_implied_by_formal_representation") is True

    gates = load(GATES)
    required = set(gates.get("required_canonical_artifacts", []))
    for path in (DOC, REG, AUDIT):
        assert path.relative_to(ROOT).as_posix() in required
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["mechanized-proof-verification"]["status"] == "not_satisfied"
    assert by_name["independent-proof-review"]["status"] == "not_satisfied"

    makefile = MAKEFILE.read_text(encoding="utf-8")
    assert makefile.count("python tools/check_s_core_w1.py") == 3

    print("S_core W1 proof: PASS (7 lemmas proved; 2 obstruction hypotheses refuted; 23 open; W2 active)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
