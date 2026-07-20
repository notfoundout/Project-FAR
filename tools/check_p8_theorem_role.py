#!/usr/bin/env python3
"""Validate the frozen P8 split decision after W0 source-side progress."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/p8-theorem-role-decision-v1.0.md"
REG = ROOT / "theory/evaluation/p8-theorem-role-decision.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
PREMISES = ROOT / "theory/evaluation/thm-target-001-premise-ledger.json"
LEMMA_REG = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"
W0_DOC = ROOT / "docs/research/s-core-w0-normalization-proof-v1.0.md"
W0_REG = ROOT / "theory/evaluation/s-core-w0-normalization-proof.json"
GATES = ROOT / "theory/evaluation/research-gates.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (DOC, REG, TARGET, PREMISES, LEMMA_REG, W0_DOC, W0_REG, GATES):
        assert path.is_file(), f"missing P8 artifact: {path.relative_to(ROOT)}"

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Selected mode: **`split`**",
        "P8-I — Internal evidential-status preservation",
        "P8-E — External process-to-presentation correspondence",
        "Faithful_split",
        "ApplicableFaithful",
        "does not prove a representation theorem",
    ):
        assert phrase in text, f"P8 decision missing phrase: {phrase}"

    reg = load(REG)
    assert reg.get("decision_id") == "P8-ROLE-001"
    assert reg.get("selected_mode") == "split"
    assert reg.get("status") == "frozen_unproved"
    assert reg.get("proof_status") == "none"
    assert reg["internal_obligation"]["predicate"] == "Pres_8I"
    assert reg["internal_obligation"]["source_reduct_extraction_status"] == "proved_LEM-SC-002"
    assert reg["internal_obligation"]["target_preservation_status"] == "unproved_LEM-SC-014"
    assert reg["external_obligation"]["predicate"] == "Corr_8E"
    assert reg["external_obligation"]["not_implied_by_formal_representation"] is True
    assert reg.get("lemma_ledger_registry") == LEMMA_REG.relative_to(ROOT).as_posix()
    assert reg.get("w0_proof_artifact") == W0_DOC.relative_to(ROOT).as_posix()
    assert reg.get("w0_proof_registry") == W0_REG.relative_to(ROOT).as_posix()
    assert reg.get("next_required_artifact") == "W1 base-carrier and direct-axis construction proof package"
    assert "Pres_8I target preservation is proved" in reg.get("nonclaims", [])

    target = load(TARGET)
    p8 = target.get("p8", {})
    assert p8.get("status") == "resolved_split"
    assert p8.get("selected_value") == "split"
    assert p8.get("internal_predicate") == "Pres_8I"
    assert p8.get("external_predicate") == "Corr_8E"
    assert p8.get("proof_acceptance_blocked_until_resolved") is False
    assert target.get("proof_status") == "partial_lemmas_only"
    assert target.get("next_required_artifact") == "W1 base-carrier and direct-axis construction proof package"

    family = {item["id"]: item for item in target.get("theorem_family", [])}
    assert family["THM-CORE-REP-001"].get("predicate") == "Faithful_split"
    assert "p8_resolution" not in family["THM-CORE-REP-001"].get("blocked_by", [])
    assert family["THM-CORE-REP-001"].get("blocked_by") == ["lemma_ledger_execution"]
    assert family["THM-P8-CORR-001"].get("predicate") == "Corr_8E"

    premises = load(PREMISES)
    prm10 = next(item for item in premises["entries"] if item["id"] == "PRM-010")
    assert prm10.get("status") == "resolved_frozen"
    assert prm10.get("decision") == "split"
    assert "P8 mode" not in premises.get("open_items", [])

    lemma = load(LEMMA_REG)
    assert lemma.get("ledger_id") == "SCORE-LEMMA-LEDGER-001"
    assert lemma.get("status") == "frozen_dependency_decomposition_w0_complete_w1_active"
    assert lemma.get("execution_summary", {}).get("proved") == 4
    assert lemma.get("execution_summary", {}).get("scope_boundary_established") == 1
    assert lemma.get("execution_summary", {}).get("open") == 32
    by_id = {item["id"]: item for item in lemma.get("obligations", [])}
    assert by_id["LEM-SC-002"].get("status") == "proved"
    assert by_id["LEM-SC-014"].get("status") == "registered_unproved"

    w0 = load(W0_REG)
    assert w0.get("proof_id") == "SCORE-W0-PROOF-001"
    assert next(item for item in w0["results"] if item["id"] == "LEM-SC-002")["status"] == "proved"

    gates = load(GATES)
    required = set(gates.get("required_canonical_artifacts", []))
    for relative in (
        "docs/research/p8-theorem-role-decision-v1.0.md",
        "theory/evaluation/p8-theorem-role-decision.json",
        "docs/research/s-core-construction-obstruction-ledger-v1.0.md",
        "theory/evaluation/s-core-construction-obstruction-ledger.json",
        "docs/research/s-core-w0-normalization-proof-v1.0.md",
        "theory/evaluation/s-core-w0-normalization-proof.json",
    ):
        assert relative in required
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"

    print("P8 theorem-role decision: PASS (P8I source reduct extracted; target Pres_8I unproved; W1 active)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
