#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "theory/evaluation/usd-w4-ablation-reconstruction-contract-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json"
DOC = ROOT / "docs/research/usd-w4-ablation-reconstruction-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w4-ablation-reconstruction-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (CONTRACT, RESULT, DOC, AUDIT):
        assert path.is_file(), path
    contract, result = load(CONTRACT), load(RESULT)
    doc, audit = DOC.read_text(encoding="utf-8"), AUDIT.read_text(encoding="utf-8")

    assert contract["contract_id"] == "USD-W4-ABL-CONTRACT-001"
    assert contract["status"] == "frozen_executed"
    assert contract["workstream"] == "USD-W4-ABLATION"
    assert set(contract["tested_vocabularies"]) == {"FARA-001", "LTS-PROV-001"}
    assert set(contract["ablation_modes"]) == {"direct_removal", "alternative_reconstruction", "equivalent_reintroduction"}
    assert len(contract["fara_units"]) == 5
    assert len(contract["lts_prov_units"]) == 5
    assert len(contract["preservation_obligations"]) == 8
    assert "decoders recovery maps and source-specific adapters" in contract["complete_cost_accounting"]

    assert result["result_id"] == "USD-W4-ABL-RESULT-001"
    assert result["status"] == "complete_bounded_local_necessity_supported"
    assert result["contract"] == contract["contract_id"]
    assert set(result["vocabulary_results"]["FARA-001"]) == set(contract["fara_units"])
    assert set(result["vocabulary_results"]["LTS-PROV-001"]) == set(contract["lts_prov_units"])
    allowed = {"locally_load_bearing", "equivalently_reintroduced"}
    assert all(value in allowed for values in result["vocabulary_results"].values() for value in values.values())
    assert result["reconstruction_summary"]["successful_strictly_cheaper_non_equivalent_reconstructions"] == []
    assert result["reconstruction_summary"]["all_reintroduced_machinery_charged"] is True
    assert set(result["obligation_results"]) == set(contract["preservation_obligations"])
    assert all(value == "pass" for value in result["obligation_results"].values())
    assert result["comparison_effect"]["FARA_vs_LTS_PROV"] == "bounded_incomparability_preserved"
    assert result["comparison_effect"]["winner"] == "none"
    assert result["terminal_outcome"] == "bounded_local_necessity_supported"
    assert result["claim_effect"]["H_N_local"] == "supported_on_frozen_benchmark_for_tested_units"
    assert result["claim_effect"]["H_N_global"] == "unresolved"
    assert result["claim_effect"]["THM-US-MIN-001"] == "unresolved"
    assert result["next_workstream"] == "USD-W5-MIN-EQUIV"
    assert result["independent_review_status"] == "not_started"

    assert "No strictly cheaper non-equivalent reconstruction" in doc
    assert "does not prove global necessity" in doc
    assert "Equivalent reintroductions were counted as machinery" in audit
    assert "Global necessity and minimality remain unresolved" in audit

    print("USD-W4 ablation and reconstruction: PASS (bounded local necessity supported; global necessity unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
