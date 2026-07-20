#!/usr/bin/env python3
"""Validate the frozen P8 split decision and conservative claim boundary."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/p8-theorem-role-decision-v1.0.md"
REG = ROOT / "theory/evaluation/p8-theorem-role-decision.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
LEDGER = ROOT / "theory/evaluation/thm-target-001-premise-ledger.json"
GATES = ROOT / "theory/evaluation/research-gates.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (DOC, REG, TARGET, LEDGER, GATES):
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
    assert reg["external_obligation"]["predicate"] == "Corr_8E"
    assert reg["external_obligation"]["not_implied_by_formal_representation"] is True

    target = load(TARGET)
    p8 = target.get("p8", {})
    assert p8.get("status") == "resolved_split"
    assert p8.get("selected_value") == "split"
    assert p8.get("internal_predicate") == "Pres_8I"
    assert p8.get("external_predicate") == "Corr_8E"
    assert p8.get("proof_acceptance_blocked_until_resolved") is False
    assert target.get("proof_status") == "none"
    assert target.get("next_required_artifact") == "S_core construction and obstruction lemma ledger"

    family = {x["id"]: x for x in target.get("theorem_family", [])}
    assert family["THM-CORE-REP-001"].get("predicate") == "Faithful_split"
    assert "p8_resolution" not in family["THM-CORE-REP-001"].get("blocked_by", [])
    assert family["THM-P8-CORR-001"].get("predicate") == "Corr_8E"

    ledger = load(LEDGER)
    prm10 = next(x for x in ledger["entries"] if x["id"] == "PRM-010")
    assert prm10.get("status") == "resolved_frozen"
    assert prm10.get("decision") == "split"
    assert "P8 mode" not in ledger.get("open_items", [])

    gates = load(GATES)
    required = set(gates.get("required_canonical_artifacts", []))
    assert "docs/research/p8-theorem-role-decision-v1.0.md" in required
    assert "theory/evaluation/p8-theorem-role-decision.json" in required

    print("P8 theorem-role decision: PASS (split; no theorem claim)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
