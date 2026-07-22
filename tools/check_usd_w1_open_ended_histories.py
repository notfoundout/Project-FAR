#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-open-ended-histories-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-open-ended-histories-extension-result-v1.0.json"
PROOF = ROOT / "docs/research/usd-w1-open-ended-histories-extension-proof-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w1-open-ended-histories-extension-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (SCOPE, FIXTURES, RESULT, PROOF, AUDIT):
        assert path.is_file(), path
    scope, fixtures, result = load(SCOPE), load(FIXTURES), load(RESULT)
    proof = PROOF.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert scope["scope_id"] == "USD-W1-OH-SCOPE-001"
    assert scope["status"] == "frozen_executed"
    assert scope["feature_family"] == "open_ended_histories"
    assert scope["source_class"] == "S_hist_eff"
    admission = scope["admission_rule"]
    assert admission["candidate_independent"] is True
    assert "no frozen terminal length" in admission["history_domain"]
    assert "total uniform procedure" in admission["prefix_access"]
    assert "finite effectively recoverable dependency cone" in admission["transition_locality"]
    assert any("rewrite an unbounded past" in item for item in admission["exclusions"])
    prohibited = set(scope["observation_boundary"]["prohibited"])
    assert {"future-history oracle", "fixed terminal horizon presented as total coverage", "source-instance-specific decoder"} <= prohibited

    obligations = set(scope["preservation_obligations"])
    expected = {f"OH-EXT-{i:03d}_{suffix}" for i, suffix in [
        (1, "total_uniform_prefix_constructor"), (2, "prefix_coherence_preserved"),
        (3, "event_identity_and_order_preserved"), (4, "dependency_cones_preserved"),
        (5, "commitment_ground_dependency_preserved"), (6, "revision_and_rule_change_history_preserved"),
        (7, "unbounded_extension_remains_available"), (8, "no_fixed_horizon_collapse"),
        (9, "registered_negative_controls_rejected"),
    ]}
    assert obligations == expected

    by_id = {item["id"]: item for item in fixtures["fixtures"]}
    assert set(by_id) == {
        "OH-LINEAR-001", "OH-BRANCH-001", "OH-REV-001", "OH-NEG-HORIZON-001",
        "OH-NEG-FUTURE-001", "OH-BOUND-INFINITE-PAST-001", "OH-BOUND-GLOBAL-REWRITE-001",
    }
    positives = ("OH-LINEAR-001", "OH-BRANCH-001", "OH-REV-001")
    negatives = ("OH-NEG-HORIZON-001", "OH-NEG-FUTURE-001")
    boundaries = ("OH-BOUND-INFINITE-PAST-001", "OH-BOUND-GLOBAL-REWRITE-001")
    assert all(by_id[item]["kind"] == "positive" for item in positives)
    assert all(by_id[item]["kind"] == "negative" for item in negatives)
    assert all(by_id[item]["kind"] == "scope_boundary" for item in boundaries)
    mutations = set(fixtures["mutation_targets"])
    assert "accept_fixed_terminal_horizon" in mutations
    assert "permit_future_history_oracle" in mutations
    assert "drop_prefix_coherence" in mutations
    assert "promote_universal_structure_claim" in mutations

    assert result["result_id"] == "USD-W1-OH-RESULT-001"
    assert result["status"] == "complete_bounded_extension_proved"
    assert result["scope_contract"] == scope["scope_id"]
    assert result["source_class"] == scope["source_class"]
    assert result["new_target_primitive"] is False
    assert set(result["proved_obligations"]) == obligations
    assert result["terminal_outcome"] == "proper_subclass_only"
    fixture_results = result["fixture_results"]
    assert all(fixture_results[item] == "pass" for item in positives)
    assert all(fixture_results[item] == "rejected" for item in negatives)
    assert all(fixture_results[item] == "excluded" for item in boundaries)

    theorem_effect = result["theorem_effect"]
    assert theorem_effect["THM-IRD-EXT-001"] == "partial_progress_fourth_feature_subclass_resolved"
    assert all(theorem_effect[key] == "unresolved" for key in ("THM-US-EXIST-001", "THM-US-INV-001", "THM-US-NEC-001", "THM-US-MIN-001"))
    claims = result["claim_effect"]
    assert claims["effective_open_ended_history_representation"] == "proved_for_S_hist_eff"
    assert claims["all_open_ended_history_representation"] == "unresolved"
    assert claims["S_IRD_representation"] == "unresolved"
    assert claims["universal_structure"] == "unresolved"
    assert result["machine_check_status"] == "not_mechanized"
    assert result["independent_review_status"] == "not_started"

    assert "coherent directed family of all finite prefixes" in proof
    assert "proper_subclass_only" in proof
    assert "does not establish all infinite histories" in proof
    assert "candidate vocabulary" in audit
    assert "The correct terminal outcome is `proper_subclass_only`" in audit

    print("USD-W1 open-ended histories extension: PASS (S_hist_eff proved; broader claims unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
