#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-extension-result-v1.0.json"
PROOF = ROOT / "docs/research/usd-w1-continuous-dynamics-extension-proof-v1.0.md"
AUDIT = ROOT / "docs/audits/usd-w1-continuous-dynamics-extension-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (SCOPE, FIXTURES, RESULT, PROOF, AUDIT):
        assert path.is_file(), path
    scope, fixtures, result = load(SCOPE), load(FIXTURES), load(RESULT)
    proof = PROOF.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert scope["scope_id"] == "USD-W1-CD-SCOPE-001"
    assert scope["version"] == "1.1"
    assert scope["status"] == "frozen_executed"
    assert scope["feature_family"] == "continuous_dynamics"
    assert scope["source_class"] == "S_cd_lip_eff"
    admission = scope["admission_rule"]
    assert admission["candidate_independent"] is True
    assert "Lipschitz" in admission["dynamics"]
    assert "computable finite event enumerator" in admission["events"]
    assert "certified rational crossing brackets" in admission["events"]
    assert "proving that no crossing is omitted" in admission["events"]
    assert "isolated guard crossings without computable completeness certificates" in admission["exclusions"]
    assert "nonunique flows" in admission["exclusions"]
    assert "Zeno event accumulation" in admission["exclusions"]
    prohibited = set(scope["observation_boundary"]["prohibited"])
    assert {"future-trajectory oracle", "exact-real equality oracle", "unregistered search for missed guard crossings", "finite time grid treated as the exact trajectory"} <= prohibited

    obligations = set(scope["preservation_obligations"])
    expected_obligations = {f"CD-EXT-{i:03d}_{suffix}" for i, suffix in [
        (1, "total_uniform_constructor"), (2, "flow_semantics_preserved"),
        (3, "time_and_order_preserved"), (4, "guard_and_reset_semantics_preserved"),
        (5, "commitment_ground_dependency_preserved"), (6, "history_and_revision_preserved"),
        (7, "error_refinement_coherent"), (8, "no_discretization_collapse"),
        (9, "registered_negative_controls_rejected"),
    ]}
    assert obligations == expected_obligations

    by_id = {item["id"]: item for item in fixtures["fixtures"]}
    assert set(by_id) == {
        "CD-LIN-001", "CD-NLIN-001", "CD-HYB-001", "CD-NEG-GRID-001",
        "CD-NEG-ORACLE-001", "CD-BOUND-UNCERT-EVENT-001",
        "CD-BOUND-NONUNIQ-001", "CD-BOUND-ZENO-001",
    }
    assert all(by_id[item]["kind"] == "positive" for item in ("CD-LIN-001", "CD-NLIN-001", "CD-HYB-001"))
    assert all(by_id[item]["kind"] == "negative" for item in ("CD-NEG-GRID-001", "CD-NEG-ORACLE-001"))
    boundaries = ("CD-BOUND-UNCERT-EVENT-001", "CD-BOUND-NONUNIQ-001", "CD-BOUND-ZENO-001")
    assert all(by_id[item]["kind"] == "scope_boundary" for item in boundaries)
    mutations = set(fixtures["mutation_targets"])
    assert "remove_event_completeness_certificate_requirement" in mutations
    assert "permit_undeclared_missed_event_search" in mutations
    assert "accept_fixed_grid_as_exact" in mutations
    assert "promote_terminal_outcome_to_extension_proved" in mutations
    assert "promote_universal_structure_claim" in mutations

    assert result["result_id"] == "USD-W1-CD-RESULT-001"
    assert result["version"] == "1.1"
    assert result["status"] == "complete_bounded_extension_proved"
    assert result["scope_contract"] == scope["scope_id"]
    assert result["source_class"] == scope["source_class"]
    assert result["new_target_primitive"] is False
    assert set(result["proved_obligations"]) == obligations
    assert result["terminal_outcome"] == "proper_subclass_only"
    fixture_results = result["fixture_results"]
    assert all(fixture_results[item] == "pass" for item in ("CD-LIN-001", "CD-NLIN-001", "CD-HYB-001"))
    assert all(fixture_results[item] == "rejected" for item in ("CD-NEG-GRID-001", "CD-NEG-ORACLE-001"))
    assert all(fixture_results[item] == "excluded" for item in boundaries)

    theorem_effect = result["theorem_effect"]
    assert theorem_effect["THM-IRD-EXT-001"] == "partial_progress_third_feature_subclass_resolved"
    assert all(theorem_effect[key] == "unresolved" for key in ("THM-US-EXIST-001", "THM-US-INV-001", "THM-US-NEC-001", "THM-US-MIN-001"))
    claim_effect = result["claim_effect"]
    assert claim_effect["effective_lipschitz_continuous_dynamics_representation"] == "proved_for_certificate_bounded_S_cd_lip_eff"
    assert claim_effect["all_continuous_dynamics_representation"] == "unresolved"
    assert claim_effect["S_IRD_representation"] == "unresolved"
    assert claim_effect["universal_structure"] == "unresolved"
    assert result["machine_check_status"] == "not_mechanized"
    assert result["independent_review_status"] == "not_started"

    assert "Isolatedness alone is not treated as an effective recovery theorem" in proof
    assert "computable completeness evidence" in proof
    assert "proper_subclass_only" in proof
    assert "does not establish all continuous dynamics" in proof
    assert "candidate vocabulary" in audit
    assert "The correct terminal outcome is `proper_subclass_only`" in audit

    print("USD-W1 continuous-dynamics extension: PASS (certificate-bounded S_cd_lip_eff proved; broader claims unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
