#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-nonfinite-stochasticity-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-nonfinite-stochasticity-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-nonfinite-stochasticity-extension-result-v1.0.json"
PROOF = ROOT / "docs/research/usd-w1-nonfinite-stochasticity-extension-proof-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w1-nonfinite-stochasticity-extension-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (SCOPE, FIXTURES, RESULT, PROOF, AUDIT):
        assert path.is_file(), path
    scope, fixtures, result = load(SCOPE), load(FIXTURES), load(RESULT)
    proof = PROOF.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert scope["scope_id"] == "USD-W1-NFS-SCOPE-001"
    assert scope["status"] == "frozen_executed"
    assert scope["feature_family"] == "non_finite_support_stochasticity"
    assert scope["source_class"] == "S_stoch_eff"
    admission = scope["admission_rule"]
    assert admission["candidate_independent"] is True
    assert "certified effective tail bounds" in admission["kernels"]
    assert "certified positive probability" in admission["conditioning"]
    assert "noncomputable probability measures or kernels" in admission["exclusions"]
    assert any("conditioning on null" in item for item in admission["exclusions"])
    prohibited = set(scope["observation_boundary"]["prohibited"])
    assert {"exact infinite sum oracle", "future random-outcome oracle", "finite support truncation treated as the exact distribution", "undeclared null-event regularization"} <= prohibited

    obligations = set(scope["preservation_obligations"])
    expected = {f"NFS-EXT-{i:03d}_{suffix}" for i, suffix in [
        (1, "total_uniform_constructor"), (2, "probability_mass_preserved"),
        (3, "expectation_queries_preserved"), (4, "conditioning_and_update_preserved"),
        (5, "commitment_ground_dependency_preserved"), (6, "history_and_revision_preserved"),
        (7, "tail_refinement_coherent"), (8, "no_finite_support_collapse"),
        (9, "registered_negative_controls_rejected"),
    ]}
    assert obligations == expected

    by_id = {item["id"]: item for item in fixtures["fixtures"]}
    positives = ("NFS-GEO-001", "NFS-POISSON-001", "NFS-MARKOV-001")
    negatives = ("NFS-NEG-TRUNC-001", "NFS-NEG-ORACLE-001")
    boundaries = ("NFS-BOUND-NULL-001", "NFS-BOUND-NONCOMP-001", "NFS-BOUND-UNBOUNDED-001")
    assert set(by_id) == set(positives + negatives + boundaries)
    assert all(by_id[item]["kind"] == "positive" for item in positives)
    assert all(by_id[item]["kind"] == "negative" for item in negatives)
    assert all(by_id[item]["kind"] == "scope_boundary" for item in boundaries)
    mutations = set(fixtures["mutation_targets"])
    assert "remove_tail_certificate_requirement" in mutations
    assert "accept_finite_truncation_as_exact" in mutations
    assert "permit_null_event_conditioning_without_interface" in mutations
    assert "promote_universal_structure_claim" in mutations

    assert result["result_id"] == "USD-W1-NFS-RESULT-001"
    assert result["status"] == "complete_bounded_extension_proved"
    assert result["scope_contract"] == scope["scope_id"]
    assert result["source_class"] == scope["source_class"]
    assert result["new_target_primitive"] is False
    assert set(result["proved_obligations"]) == obligations
    assert result["terminal_outcome"] == "proper_subclass_only"
    values = result["fixture_results"]
    assert all(values[item] == "pass" for item in positives)
    assert all(values[item] == "rejected" for item in negatives)
    assert all(values[item] == "excluded" for item in boundaries)

    effect = result["theorem_effect"]
    assert effect["THM-IRD-EXT-001"] == "partial_progress_sixth_feature_subclass_resolved"
    assert all(effect[key] == "unresolved" for key in ("THM-US-EXIST-001", "THM-US-INV-001", "THM-US-NEC-001", "THM-US-MIN-001"))
    claims = result["claim_effect"]
    assert claims["effective_nonfinite_stochastic_representation"] == "proved_for_S_stoch_eff"
    assert claims["all_stochastic_reasoning_representation"] == "unresolved"
    assert claims["S_IRD_representation"] == "unresolved"
    assert claims["universal_structure"] == "unresolved"
    assert result["machine_check_status"] == "not_mechanized"
    assert result["independent_review_status"] == "not_started"

    assert "finite support truncation" in proof
    assert "proper_subclass_only" in proof
    assert "does not establish all stochastic reasoning systems" in proof
    assert "candidate vocabulary" in audit
    assert "The correct terminal outcome is `proper_subclass_only`" in audit

    print("USD-W1 non-finite stochasticity extension: PASS (S_stoch_eff proved; broader claims unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
