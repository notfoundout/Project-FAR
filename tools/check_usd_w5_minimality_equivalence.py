#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w5-minimality-equivalence-result-v1.0.json"
REPORT = ROOT / "docs/research/usd-w5-minimality-equivalence-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w5-minimality-equivalence-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (CONTRACT, RESULT, REPORT, AUDIT):
        assert path.is_file(), path

    contract, result = load(CONTRACT), load(RESULT)
    report = REPORT.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert contract["contract_id"] == "USD-W5-MIN-EQUIV-CONTRACT-001"
    assert contract["status"] == "frozen_executed"
    assert contract["workstream"] == "USD-W5-MIN-EQUIV"
    assert set(contract["candidate_universe"]) == {"FARA-001", "LTS-PROV-001", "GREL-001", "ARG-HIST-001"}
    assert set(contract["successful_candidates"]) == {"FARA-001", "LTS-PROV-001"}
    assert contract["translation_equivalence"]["requires_total_bidirectional_translation"] is True
    assert contract["translation_equivalence"]["requires_round_trip_commitment_equivalence"] is True
    assert contract["cost_preorder"]["scalarization_forbidden"] is True
    assert contract["cost_preorder"]["tradeoffs_count_as_incomparability"] is True
    assert len(contract["obligations"]) == 8
    assert len(contract["negative_controls"]) == 5

    assert result["result_id"] == "USD-W5-MIN-EQUIV-RESULT-001"
    assert result["status"] == "complete_bounded_classification"
    assert result["contract"] == contract["contract_id"]
    assert set(result["candidate_results"]) == set(contract["candidate_universe"])
    minima = {name for name, row in result["candidate_results"].items() if row["minimal_in_frozen_universe"]}
    assert minima == {"FARA-001", "LTS-PROV-001"}
    assert result["candidate_results"]["GREL-001"]["minimal_in_frozen_universe"] is False
    assert result["candidate_results"]["ARG-HIST-001"]["minimal_in_frozen_universe"] is False
    assert result["translation_tests"]["round_trip_equivalence"] == "fail"
    assert result["pareto_relations"]["FARA_vs_LTS_PROV"] == "incomparable"
    assert set(result["obligation_results"]) == set(contract["obligations"])
    assert all(value == "pass" for value in result["obligation_results"].values())
    assert set(result["negative_control_results"]) == set(contract["negative_controls"])
    assert all(value == "rejected" for value in result["negative_control_results"].values())
    assert result["terminal_outcome"] == "multiple_incomparable_minima"
    assert result["claim_effect"]["USD-H-MIN"] == "resolved_for_frozen_candidate_universe"
    assert result["claim_effect"]["unique_minimum"] == "refuted_in_frozen_candidate_universe"
    assert result["claim_effect"]["global_minimality"] == "unresolved"
    assert result["claim_effect"]["universal_structure"] == "unresolved"
    assert result["independent_review_status"] == "not_started"
    assert result["next_workstream"] == "USD-W6-INDEPENDENCE"

    assert "multiple_incomparable_minima" in report
    assert "No scalar score is permitted" in report
    assert "does not show that no future vocabulary can dominate both classes" in report
    assert "No scalar score was introduced" in audit
    assert "Global minimality and exhaustive no-go remain unresolved" in audit

    print("USD-W5 minimality/equivalence: PASS (multiple incomparable minima in frozen universe; global claims unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
