from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "research/evidence-authority-model/validate_candidate.py"
SPEC = importlib.util.spec_from_file_location("evidence_authority_execution", VALIDATOR)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_evidence_authority_primary_v5() -> None:
    result = MODULE.run_full_validation()
    positive = result["positive_validation"]
    summary = {
        "overall": result["overall"],
        "errors": result["errors"],
        "evidence_digest": result["evidence_digest"],
        "frozen_base_commit": positive["frozen_base_commit"],
        "frozen_tree_sha": positive["frozen_tree_sha"],
        "discovery_input_count": positive["discovery_input_count"],
        "discovery_input_digest": positive["discovery_input_digest"],
        "proof_path_count": positive["proof_path_count"],
        "negative_control_count": result["negative_control_count"],
        "all_negative_controls_detected": result["all_negative_controls_detected"],
        "synthetic_manifest_entry_count": positive["activation_manifest_probe"]["entry_count"],
        "synthetic_decision_record_count": positive["activation_manifest_probe"]["entry_count"] + 1,
        "declared_numeric_priority_order": positive["declared_numeric_priority_order"],
        "unequal_priority_probe": positive["unequal_priority_probe"],
        "canonical_id_records": MODULE._canonical_id_rule()["required_sentinels"],
        "artifact_map_key_records": MODULE._artifact_map_key_rule()["required_sentinels"],
        "control_ids": [item["control_id"] for item in result["negative_controls"]],
    }
    print("BEGIN_EVIDENCE_AUTHORITY_PRIMARY_V5")
    print(json.dumps(summary, sort_keys=True))
    print("END_EVIDENCE_AUTHORITY_PRIMARY_V5")

    assert result["overall"] == "pass", result["errors"]
    assert positive["proof_path_count"] == 56
    assert positive["activation_manifest_probe"]["entry_count"] == 56
    assert result["negative_control_count"] == 42
    assert result["all_negative_controls_detected"] is True
    assert positive["declared_numeric_priority_order"] == "lower_is_higher"
    assert positive["unequal_priority_probe"]["selected_numeric_priority"] == 1
