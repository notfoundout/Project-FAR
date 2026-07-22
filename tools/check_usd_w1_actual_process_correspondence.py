#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-actual-process-correspondence-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json"
REPORT = ROOT / "docs/research/usd-w1-actual-process-correspondence-boundary-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w1-actual-process-correspondence-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (SCOPE, FIXTURES, RESULT, REPORT, AUDIT):
        assert path.is_file(), path
    scope, fixtures, result = load(SCOPE), load(FIXTURES), load(RESULT)
    report = REPORT.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert scope["scope_id"] == "USD-W1-APC-SCOPE-001"
    assert scope["status"] == "frozen_executed"
    assert scope["feature_family"] == "actual_process_correspondence"
    assert scope["source_class"] == "S_apc_evid"
    admission = scope["admission_rule"]
    assert admission["candidate_independent"] is True
    required = set(admission["required_for_positive_correspondence"])
    assert "independent process observations" in required
    assert "measurement model with error bounds" in required
    assert "registered alternative-process explanations" in required
    prohibited = set(scope["observation_boundary"]["prohibited"])
    assert "infer actual-process identity from representability alone" in prohibited
    assert "treat generated traces as independent observations" in prohibited
    assert scope["counterexample_policy"]["observationally_equivalent_distinct_processes_block_identity_inference"] is True

    obligations = set(scope["preservation_obligations"])
    assert obligations == {
        "APC-001_formal_representation_separated_from_empirical_correspondence",
        "APC-002_external_evidence_requirements_explicit",
        "APC-003_observational_equivalence_controlled",
        "APC-004_trace_provenance_classified",
        "APC-005_identity_bridge_not_assumed",
        "APC-006_negative_controls_rejected",
        "APC-007_terminal_outcome_claim_bounded",
    }

    by_id = {item["id"]: item for item in fixtures["fixtures"]}
    assert set(by_id) == {"APC-FORMAL-001", "APC-TRACE-001", "APC-OBS-EQUIV-001", "APC-MEAS-001", "APC-NEG-REP-001", "APC-NEG-LABEL-001"}
    mutations = set(fixtures["mutation_targets"])
    assert "promote_formal_faithfulness_to_empirical_correspondence" in mutations
    assert "drop_observational_equivalence_control" in mutations
    assert "promote_actual_process_claim" in mutations

    assert result["result_id"] == "USD-W1-APC-RESULT-001"
    assert result["status"] == "complete_boundary_result"
    assert result["scope_contract"] == scope["scope_id"]
    assert set(result["proved_obligations"]) == obligations
    assert result["terminal_outcome"] == "new_assumption_required"
    values = result["fixture_results"]
    assert values["APC-FORMAL-001"] == "insufficient_for_correspondence"
    assert values["APC-TRACE-001"] == "insufficient_nonindependent_evidence"
    assert values["APC-OBS-EQUIV-001"] == "blocks_identity_inference"
    assert values["APC-MEAS-001"] == "eligible_for_future_empirical_test"
    assert values["APC-NEG-REP-001"] == "rejected"
    assert values["APC-NEG-LABEL-001"] == "rejected"
    assert result["workstream_effect"]["USD-W1-SCOPE-EXT"] == "all_registered_feature_families_executed"
    assert result["next_decisive_workstream"] == "USD-W2-ALT-VOCAB"
    assert result["claim_effect"]["actual_process_correspondence"] == "not_established_new_empirical_assumption_required"
    assert result["claim_effect"]["universal_structure"] == "unresolved"

    assert "Formal faithfulness and actual-process correspondence are distinct claims" in report
    assert "new_assumption_required" in report
    assert "The next decisive workstream is `USD-W2-ALT-VOCAB`" in report
    assert "The correct terminal outcome is `new_assumption_required`" in audit

    print("USD-W1 actual-process correspondence: PASS (new empirical assumption required; no correspondence claim made)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
