#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "theory/evaluation/usd-w6-independence-contract-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w6-independence-result-v1.0.json"
DOC = ROOT / "docs/research/usd-w6-independence-execution-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w6-independence-audit.md"

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    for path in (CONTRACT, RESULT, DOC, AUDIT):
        assert path.is_file(), path
    contract, result = load(CONTRACT), load(RESULT)
    doc = DOC.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    assert contract["contract_id"] == "USD-W6-IND-CONTRACT-001"
    assert contract["workstream"] == "USD-W6-INDEPENDENCE"
    assert contract["status"] == "frozen_executed"
    assert len(contract["layers"]) == 5
    assert contract["layers"]["internal_multi_implementation_robustness"]["status"] == "executed"
    for layer in ("independent_proof_review", "R3_independent_technical_replication", "R4_adversarial_conceptual_replication", "R5_cross_context_replication"):
        assert contract["layers"][layer]["status"] == "not_executed"
    assert "one agent cannot establish human or organizational independence" in contract["independence_rules"]
    assert result["result_id"] == "USD-W6-IND-RESULT-001"
    assert result["contract"] == contract["contract_id"]
    assert result["terminal_outcome"] == "internal_robustness_only"
    assert result["internal_execution"]["isolated_implementations"] == 3
    assert result["internal_execution"]["artifact_cross_access"] is False
    assert result["internal_execution"]["separate_verifier"] is True
    assert result["internal_execution"]["deterministic_comparison"] == "pass"
    assert result["internal_execution"]["mutation_campaign"] == "pass"
    assert result["claim_effect"]["independent_verification_claim"] == "prohibited"
    assert result["claim_effect"]["universal_structure"] == "unresolved"
    assert "One agent can isolate computational paths" in doc
    assert "internal implementation replication" in audit
    assert "The correct result is `internal_robustness_only`" in audit
    print("USD-W6 independence: PASS (internal robustness only; external independence unresolved)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
