#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w3-representation-invariance-result-v1.0.json"
PROOF = ROOT / "docs/research/usd-w3-representation-invariance-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w3-representation-invariance-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (CONTRACT, RESULT, PROOF, AUDIT):
        assert path.is_file(), path
    contract, result = load(CONTRACT), load(RESULT)
    proof = PROOF.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert contract["contract_id"] == "USD-W3-INV-CONTRACT-001"
    assert contract["status"] == "frozen_executed"
    assert contract["workstream"] == "USD-W3-INVARIANCE"
    assert set(contract["tested_vocabularies"]) == {"FARA-001", "LTS-PROV-001"}
    assert len(contract["transformations"]) == 8
    assert len(contract["obligations"]) == 8
    assert len(contract["negative_controls"]) == 5
    forbidden = set(contract["equivalence_relation"]["forbidden_shortcuts"])
    assert "shared labels treated as identity" in forbidden
    assert "discarding hidden state" in forbidden

    assert result["result_id"] == "USD-W3-INV-RESULT-001"
    assert result["status"] == "complete_bounded_invariance_supported"
    assert result["contract"] == contract["contract_id"]
    assert set(result["tested_vocabularies"]) == set(contract["tested_vocabularies"])
    assert set(result["transformation_results"]) == set(contract["transformations"])
    assert all(value == "pass" for value in result["transformation_results"].values())
    assert set(result["negative_control_results"]) == set(contract["negative_controls"])
    assert all(value == "rejected" for value in result["negative_control_results"].values())
    assert set(result["obligation_results"]) == set(contract["obligations"])
    assert all(value == "pass" for value in result["obligation_results"].values())
    assert result["terminal_outcome"] == "bounded_invariance_supported"
    assert result["comparison_effect"]["FARA_vs_LTS_PROV"].startswith("incomparability_preserved")
    assert result["claim_effect"]["THM-US-INV-001"] == "bounded_support_only"
    assert result["claim_effect"]["universal_structure"] == "unresolved"
    assert result["independent_review_status"] == "not_started"
    assert result["next_workstream"] == "USD-W4-ABLATION"

    assert "Output equality and label identity" not in proof
    assert "Shared names, matching outputs" in proof
    assert "does not prove global representation invariance" in proof
    assert "No scalar score was introduced" in audit
    assert "FARA and LTS-PROV remain incomparable" in audit

    print("USD-W3 representation invariance: PASS (bounded support only; global claims unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
