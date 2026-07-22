#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-partial-observability-scope-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json"
PROOF = ROOT / "docs/research/usd-w1-partial-observability-extension-proof-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w1-partial-observability-extension-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(scope: dict, result: dict, fixtures: dict, proof_text: str, audit_text: str) -> None:
    assert scope["scope_id"] == "USD-W1-PO-SCOPE-001"
    assert scope["parent_program"] == "POST-W5-USD-001"
    assert scope["workstream"] == "USD-W1-SCOPE-EXT"
    assert scope["feature_family"] == "partial_observability"
    assert scope["source_class"] == "S_po_fin"
    assert scope["candidate_independent_admission"] is True
    required = set(scope["requirements"])
    assert {
        "finite_nonempty_latent_state_set",
        "finite_nonempty_observation_set",
        "explicit_total_observation_relation_or_finite_support_kernel",
        "policy_depends_only_on_observation_history",
        "explicit_commitments_grounds_dependencies_and_revision_history",
    } <= required
    prohibited = set(scope["observation_boundary"]["prohibited"])
    assert {
        "policy_access_to_true_latent_state",
        "target_decoder_with_source_specific_oracle",
        "metadata_smuggling_of_true_state_into_observed_commitment",
        "evaluator_repair",
    } <= prohibited
    assert "actual_process_correspondence" in scope["excluded_cases"]

    assert result["result_id"] == "USD-W1-PO-RESULT-001"
    assert result["status"] == "complete_bounded_extension_proved"
    assert result["scope_contract"] == scope["scope_id"]
    assert result["source_class"] == scope["source_class"]
    assert result["target_class"] == "A_FARA"
    assert result["new_target_primitive"] is False
    assert result["terminal_outcome"] == "proper_subclass_only"
    obligations = set(result["proved_obligations"])
    assert obligations == {f"PO-EXT-{i:03d}_{name}" for i, name in [
        (1, "total_uniform_constructor"),
        (2, "observation_indistinguishability_preserved"),
        (3, "information_state_preserved"),
        (4, "policy_measurability_preserved"),
        (5, "transition_observation_update_preserved"),
        (6, "commitment_ground_dependency_preserved"),
        (7, "history_and_revision_preserved"),
        (8, "no_true_state_leakage"),
        (9, "registered_negative_controls_rejected"),
    ]}
    assert result["fixture_results"] == {
        "PO-DET-001": "pass",
        "PO-STOCH-001": "pass",
        "PO-HIST-001": "pass",
        "PO-NEG-LEAK-001": "rejected",
        "PO-NEG-COLLAPSE-001": "rejected",
    }
    effects = result["claim_effect"]
    assert effects["finite_partial_observability_representation"] == "proved_for_S_po_fin"
    assert effects["S_IRD_representation"] == "unresolved"
    assert effects["universal_structure"] == "unresolved"
    assert effects["primitive_necessity"] == "not_established"
    assert effects["minimality"] == "not_established"
    assert effects["uniqueness"] == "not_established"
    assert result["machine_check_status"] == "not_mechanized"
    assert result["independent_review_status"] == "not_started"

    assert fixtures["fixture_set_id"] == "USD-W1-PO-FIXTURES-001"
    by_id = {item["id"]: item for item in fixtures["fixtures"]}
    assert set(by_id) == set(result["fixture_results"])
    assert by_id["PO-NEG-LEAK-001"]["violation"] == "policy_selects_action_from_unobserved_true_state"
    assert by_id["PO-NEG-COLLAPSE-001"]["violation"] == "target_merges_distinct_information_states_with_different_admissible_actions"

    for token in ["PO-EXT-001", "PO-EXT-009", "No true-state leakage", "proper_subclass_only"]:
        assert token in proof_text
    assert "does not establish representation of all partially observable reasoning" in proof_text
    assert "Pass for the registered bounded extension claim" in audit_text
    assert "Broader extension and USD claims remain unresolved" in audit_text


def main() -> int:
    for path in (SCOPE, RESULT, FIXTURES, PROOF, AUDIT):
        assert path.is_file(), path
    validate(load(SCOPE), load(RESULT), load(FIXTURES), PROOF.read_text(encoding="utf-8"), AUDIT.read_text(encoding="utf-8"))
    print("USD-W1 partial observability: PASS (finite explicit subclass proved; broader claims unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
