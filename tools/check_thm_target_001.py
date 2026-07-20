#!/usr/bin/env python3
"""Validate frozen THM-TARGET-001, faithful semantics, and resolved split P8."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/thm-target-001-v1.0.md"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
LEDGER = ROOT / "theory/evaluation/thm-target-001-premise-ledger.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"
FAITHFUL = ROOT / "docs/research/faithful-representation-specification-v1.0.md"
P8DOC = ROOT / "docs/research/p8-theorem-role-decision-v1.0.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (DOC, TARGET, LEDGER, GATES, CLAIMS, FAITHFUL, P8DOC):
        assert path.is_file(), f"missing theorem artifact: {path.relative_to(ROOT)}"

    doc = DOC.read_text(encoding="utf-8")
    for phrase in ("Frozen prospective theorem target and premise boundary", "Finite explicit core `S_core`", "General extension class `S_IRD`", "THM-CORE-REP-001", "THM-IMP-001", "This artifact does not establish"):
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

    family = {item["id"]: item for item in target.get("theorem_family", [])}
    required = {"THM-CORE-COMMON-001","THM-CORE-REP-001","THM-IRD-EXT-001","THM-P8-CORR-001","THM-PRIM-NEC-001","THM-MIN-001","THM-EQUIV-001","THM-IMP-001"}
    assert set(family) == required
    assert all(item.get("status") != "proved" for item in family.values())
    assert family["THM-CORE-REP-001"].get("predicate") == "Faithful_split"
    assert family["THM-P8-CORR-001"].get("predicate") == "Corr_8E"

    snapshot = target.get("current_gates", {})
    assert snapshot.get("formal_theorem_target") == "satisfied"
    assert snapshot.get("premise_ledger_and_semantics") == "satisfied"
    assert snapshot.get("faithful_representation_definition") == "satisfied"
    for name in ("scoped_representation_proof","primitive_lower_bounds","minimality_universe_and_proof","mechanized_proof_verification","independent_proof_review"):
        assert snapshot.get(name) == "not_satisfied"

    ledger = load(LEDGER)
    assert ledger.get("version") == "1.2"
    entries = ledger.get("entries", [])
    assert len(entries) == 22
    assert [x.get("id") for x in entries] == [f"PRM-{i:03d}" for i in range(1, 23)]
    prm10 = next(x for x in entries if x["id"] == "PRM-010")
    assert prm10.get("status") == "resolved_frozen"
    assert prm10.get("decision") == "split"
    assert "P8 mode" not in ledger.get("open_items", [])

    gates = load(GATES)
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["formal-theorem-target"]["status"] == "satisfied"
    assert by_name["premise-ledger-and-semantics"]["status"] == "satisfied"
    assert by_name["faithful-representation-definition"]["status"] == "satisfied"
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"

    claims = load(CLAIMS)
    for claim in claims.get("claims", []):
        if claim.get("id") in {"CLM-EXISTENCE", "CLM-UNIVERSALITY", "CLM-NECESSITY", "CLM-MINIMALITY"}:
            assert claim.get("current_status") != "supported"

    print("THM-TARGET-001 validation: PASS (faithful semantics frozen; P8 split; no proof claim)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
