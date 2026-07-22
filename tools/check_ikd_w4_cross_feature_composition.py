#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/ikd-w4-cross-feature-composition-v1.0.json"
RESEARCH = ROOT / "docs/research/ikd-w4-cross-feature-composition-v1.0.md"
AUDIT = ROOT / "docs/audits/ikd-w4-cross-feature-composition-audit.md"
PARENT = ROOT / "theory/evaluation/ikd-w3-common-factor-v1.0.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (RESULT, RESEARCH, AUDIT, PARENT):
        assert path.is_file(), path

    result = load(RESULT)
    parent = load(PARENT)
    research = RESEARCH.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert result["result_id"] == "IKD-W4-CROSS-FEATURE-COMP-001"
    assert result["status"] == "complete_bounded_composition_analysis"
    assert result["parent_program"] == "POST-USD-IKD-001"
    assert result["parent_common_factor"] == parent["result_id"]
    assert result["target_pr"] == 264
    assert result["kernel_under_test"] == "RCCD-001"
    assert parent["common_factor"]["id"] == "RCCD-001"
    assert len(result["feature_families"]) == 6
    assert len(set(result["feature_families"])) == 6

    contract = result["composition_contract"]
    assert contract["direct_execution_required"] is True
    assert contract["featurewise_success_not_closure"] is True
    assert contract["shared_state_identity_required"] is True
    assert contract["future_information_oracles_prohibited"] is True
    assert contract["all_adapters_schedulers_tail_certificates_and_canonicalizers_charged"] is True

    cases = result["executed_case_classes"]
    assert cases["pairwise"]["count"] == 15
    assert len(cases["pairwise"]["case_ids"]) == 15
    assert cases["triple"]["count"] == 20
    assert len(cases["triple"]["case_ids"]) == 20
    assert cases["leave_one_out_five_feature"]["count"] == 6
    assert len(cases["leave_one_out_five_feature"]["case_ids"]) == 6
    assert cases["all_six"]["count"] == 1
    assert cases["all_six"]["case_ids"] == ["IC-CD-PO-OH-SC-NS"]

    construction = result["all_six_construction"]
    assert len(construction["rccd_preservation"]) == 5
    assert "uniform bounded-query recovery" in construction["rccd_preservation"]
    assert len(result["interaction_findings"]) >= 6
    assert len(result["negative_controls"]) >= 8
    assert "featurewise_passes_multiplied_without_joint_construction_rejected" in result["negative_controls"]

    assert result["terminal_result"] == "bounded_cross_feature_compositional_closure_supported_with_explicit_compatibility_conditions"
    effect = result["claim_effect"]
    assert effect["rccd_joint_realizability_on_frozen_effective_scope"] == "supported"
    assert effect["arbitrary_feature_conjunctions"] == "not_supported"
    assert effect["universal_structure"] == "unresolved"
    assert result["next_decisive_workstream"] == "IKD-W5-EXPANDED-INVARIANCE"
    assert "RCCD-001 is globally universal" in result["nonclaims"]

    assert "Separate featurewise representation results do not imply closure under conjunction" in research
    assert "all 15 pairwise conjunctions" in research
    assert "all 20 triple conjunctions" in research
    assert "bounded_cross_feature_compositional_closure_supported_with_explicit_compatibility_conditions" in audit
    assert "External-package execution remains deferred" in audit

    print("IKD-W4 cross-feature composition: PASS (42 joint cases; all-six bounded effective construction supported)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
