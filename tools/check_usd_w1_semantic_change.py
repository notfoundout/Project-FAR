#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-semantic-change-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-semantic-change-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-semantic-change-extension-result-v1.0.json"
PROOF = ROOT / "docs/research/usd-w1-semantic-change-extension-proof-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w1-semantic-change-extension-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (SCOPE, FIXTURES, RESULT, PROOF, AUDIT):
        assert path.is_file(), path

    scope, fixtures, result = load(SCOPE), load(FIXTURES), load(RESULT)
    proof = PROOF.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert scope["scope_id"] == "USD-W1-SC-SCOPE-001"
    assert scope["status"] == "frozen_executed"
    assert scope["feature_family"] == "semantic_change"
    assert scope["source_class"] == "S_sem_eff"
    admission = scope["admission_rule"]
    assert admission["candidate_independent"] is True
    assert "partial-correspondence map" in admission["translation_contract"]
    assert "unresolved commitments" in admission["translation_contract"]
    assert "retroactive erasure of prior semantic states" in admission["exclusions"]
    prohibited = set(scope["observation_boundary"]["prohibited"])
    assert {"timeless label identity treated as semantic identity", "future-semantics oracle", "source-instance-specific decoder", "silent replacement of unresolved translation by equivalence"} <= prohibited

    obligations = set(scope["preservation_obligations"])
    expected = {f"SC-EXT-{i:03d}_{suffix}" for i, suffix in [
        (1, "total_uniform_constructor"), (2, "versioned_denotation_preserved"),
        (3, "inferential_role_preserved"), (4, "translation_effects_preserved"),
        (5, "commitment_ground_dependency_preserved"), (6, "semantic_history_and_revision_preserved"),
        (7, "unresolved_translation_remains_explicit"), (8, "no_label_identity_collapse"),
        (9, "registered_negative_controls_rejected"),
    ]}
    assert obligations == expected

    by_id = {item["id"]: item for item in fixtures["fixtures"]}
    positives = ("SC-RENAME-001", "SC-SPLIT-001", "SC-RULE-001")
    negatives = ("SC-NEG-LABEL-001", "SC-NEG-ERASE-001")
    boundaries = ("SC-BOUND-ORACLE-001", "SC-BOUND-GLOBAL-001")
    assert set(by_id) == set(positives + negatives + boundaries)
    assert all(by_id[item]["kind"] == "positive" for item in positives)
    assert all(by_id[item]["kind"] == "negative" for item in negatives)
    assert all(by_id[item]["kind"] == "scope_boundary" for item in boundaries)
    mutations = set(fixtures["mutation_targets"])
    assert "treat_label_identity_as_semantic_identity" in mutations
    assert "convert_unresolved_translation_to_equivalent" in mutations
    assert "promote_universal_structure_claim" in mutations

    assert result["result_id"] == "USD-W1-SC-RESULT-001"
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
    assert theorem_effect["THM-IRD-EXT-001"] == "partial_progress_fifth_feature_subclass_resolved"
    assert all(theorem_effect[key] == "unresolved" for key in ("THM-US-EXIST-001", "THM-US-INV-001", "THM-US-NEC-001", "THM-US-MIN-001"))
    claims = result["claim_effect"]
    assert claims["effective_semantic_change_representation"] == "proved_for_S_sem_eff"
    assert claims["all_semantic_change_representation"] == "unresolved"
    assert claims["S_IRD_representation"] == "unresolved"
    assert claims["universal_structure"] == "unresolved"
    assert result["machine_check_status"] == "not_mechanized"
    assert result["independent_review_status"] == "not_started"

    assert "does not infer equivalence from shared spelling" in proof
    assert "proper_subclass_only" in proof
    assert "candidate vocabulary" in audit
    assert "The correct terminal outcome is `proper_subclass_only`" in audit

    print("USD-W1 semantic-change extension: PASS (S_sem_eff proved; broader claims unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
