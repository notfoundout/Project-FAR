#!/usr/bin/env python3
"""Validate frozen THM-TARGET-001 and the registered S_core lemma program."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/thm-target-001-v1.0.md"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
PREMISES = ROOT / "theory/evaluation/thm-target-001-premise-ledger.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"
FAITHFUL = ROOT / "docs/research/faithful-representation-specification-v1.0.md"
P8DOC = ROOT / "docs/research/p8-theorem-role-decision-v1.0.md"
LEMMA_DOC = ROOT / "docs/research/s-core-construction-obstruction-ledger-v1.0.md"
LEMMA_REG = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (DOC, TARGET, PREMISES, GATES, CLAIMS, FAITHFUL, P8DOC, LEMMA_DOC, LEMMA_REG):
        assert path.is_file(), f"missing theorem artifact: {path.relative_to(ROOT)}"

    doc = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Frozen prospective theorem target and premise boundary",
        "Finite explicit core `S_core`",
        "General extension class `S_IRD`",
        "THM-CORE-REP-001",
        "THM-IMP-001",
        "This artifact does not establish",
    ):
        assert phrase in doc

    target = load(TARGET)
    assert target.get("theorem_target_id") == "THM-TARGET-001"
    assert target.get("version") == "1.0"
    assert target.get("status") == "frozen_unproved"
    assert target.get("proof_status") == "none"
    assert target.get("machine_check_status") == "not_started"
    assert target.get("independent_review_status") == "not_started"
    assert set(target.get("source_classes", {})) == {"S_core", "S_IRD"}
    assert target["target_class"]["id"] == "A_FARA"
    assert target["target_class"]["adds_new_primitive"] is False
    assert target["representation_witness"]["tuple"] == ["E", "D", "M", "iota", "kappa"]

    obligations = target.get("preservation_obligations", [])
    assert obligations[:7] == ["P1_configuration","P2_commitment","P3_stake_and_alternative","P4_ground_and_justification","P5_admissibility_and_dynamics","P6_consequence","P7_historical_and_path"]
    assert obligations[-1] == "P8I_internal_evidential_status"

    p8 = target.get("p8", {})
    assert p8.get("status") == "resolved_split"
    assert p8.get("selected_value") == "split"
    assert p8.get("internal_predicate") == "Pres_8I"
    assert p8.get("external_predicate") == "Corr_8E"
    assert p8.get("proof_acceptance_blocked_until_resolved") is False

    assert target.get("lemma_ledger_artifact") == LEMMA_DOC.relative_to(ROOT).as_posix()
    assert target.get("lemma_ledger_registry") == LEMMA_REG.relative_to(ROOT).as_posix()
    program = target.get("lemma_program", {})
    assert program == {
        "id": "SCORE-LEMMA-LEDGER-001",
        "status": "registered_unexecuted",
        "total_obligations": 37,
        "construction_obligations": 24,
        "obstruction_obligations": 10,
        "assembly_obligations": 3,
        "proved_obligations": 0,
        "established_obstructions": 0,
        "open_obligations": 37,
        "active_wave": "W0",
        "active_obligations": ["LEM-SC-001", "LEM-SC-002", "LEM-SC-003", "LEM-SC-004"],
    }

    family = {item["id"]: item for item in target.get("theorem_family", [])}
    required = {"THM-CORE-COMMON-001","THM-CORE-REP-001","THM-IRD-EXT-001","THM-P8-CORR-001","THM-PRIM-NEC-001","THM-MIN-001","THM-EQUIV-001","THM-IMP-001"}
    assert set(family) == required
    assert all(item.get("status") != "proved" for item in family.values())
    assert family["THM-CORE-COMMON-001"].get("blocked_by") == ["lemma_ledger_execution"]
    assert family["THM-CORE-REP-001"].get("predicate") == "Faithful_split"
    assert family["THM-CORE-REP-001"].get("blocked_by") == ["lemma_ledger_execution"]
    assert family["THM-P8-CORR-001"].get("predicate") == "Corr_8E"
    assert family["THM-IMP-001"].get("blocked_by") == ["obstruction_lemma_execution"]

    snapshot = target.get("current_gates", {})
    assert snapshot.get("formal_theorem_target") == "satisfied"
    assert snapshot.get("premise_ledger_and_semantics") == "satisfied"
    assert snapshot.get("faithful_representation_definition") == "satisfied"
    for name in ("scoped_representation_proof","primitive_lower_bounds","minimality_universe_and_proof","mechanized_proof_verification","independent_proof_review"):
        assert snapshot.get(name) == "not_satisfied"
    assert target.get("next_required_artifact") == "W0 proof package for LEM-SC-001 through LEM-SC-004"
    assert "any registered lemma is proved" in target.get("nonclaims", [])

    premises = load(PREMISES)
    assert premises.get("version") == "1.2"
    entries = premises.get("entries", [])
    assert len(entries) == 22
    assert [item.get("id") for item in entries] == [f"PRM-{i:03d}" for i in range(1, 23)]
    prm10 = next(item for item in entries if item["id"] == "PRM-010")
    assert prm10.get("status") == "resolved_frozen"
    assert prm10.get("decision") == "split"
    assert "P8 mode" not in premises.get("open_items", [])

    lemma = load(LEMMA_REG)
    assert lemma.get("ledger_id") == "SCORE-LEMMA-LEDGER-001"
    assert lemma.get("version") == "1.0"
    assert lemma.get("status") == "frozen_dependency_decomposition_registered_unexecuted"
    assert len(lemma.get("obligations", [])) == 37
    assert lemma.get("execution_summary", {}).get("proved") == 0
    assert lemma.get("execution_summary", {}).get("open") == 37

    gates = load(GATES)
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["formal-theorem-target"]["status"] == "satisfied"
    assert by_name["premise-ledger-and-semantics"]["status"] == "satisfied"
    assert by_name["faithful-representation-definition"]["status"] == "satisfied"
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["scoped-representation-proof"]["evidence"] == []

    claims = load(CLAIMS)
    for claim in claims.get("claims", []):
        if claim.get("id") in {"CLM-EXISTENCE", "CLM-UNIVERSALITY", "CLM-NECESSITY", "CLM-MINIMALITY"}:
            assert claim.get("current_status") != "supported"

    print("THM-TARGET-001 validation: PASS (37 lemma obligations open; W0 next; no proof claim)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
