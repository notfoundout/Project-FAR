#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYN = ROOT / "theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json"
NEXT = ROOT / "theory/evaluation/post-w5-usd-next-program-v1.0.json"
PROOF = ROOT / "docs/research/post-w5-usd-terminal-synthesis-v1.0.md"
AUDIT = ROOT / "docs/audits/post-w5-usd-terminal-synthesis-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (SYN, NEXT, PROOF, AUDIT):
        assert path.is_file(), path

    syn = load(SYN)
    nxt = load(NEXT)
    proof = PROOF.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert syn["synthesis_id"] == "POST-W5-USD-SYN-001"
    assert syn["status"] == "complete_bounded_synthesis"
    assert syn["parent_program"] == "POST-W5-USD-001"
    inputs = syn["inputs"]
    assert set(inputs) == {
        "USD-W1-SCOPE-EXT", "USD-W2-ALT-VOCAB", "USD-W3-INVARIANCE",
        "USD-W4-NECESSITY", "USD-W5-MIN-EQUIV", "USD-W6-INDEPENDENCE",
    }
    features = inputs["USD-W1-SCOPE-EXT"]["feature_results"]
    assert len(features) == 7
    assert sum(value == "proper_subclass_only" for value in features.values()) == 6
    assert features["actual_process_correspondence"] == "new_assumption_required"
    assert inputs["USD-W2-ALT-VOCAB"] == "multiple_incomparable_successful_vocabularies"
    assert inputs["USD-W3-INVARIANCE"] == "bounded_invariance_supported"
    assert inputs["USD-W4-NECESSITY"] == "bounded_local_necessity_supported"
    assert inputs["USD-W5-MIN-EQUIV"] == "multiple_incomparable_minima"
    assert inputs["USD-W6-INDEPENDENCE"] == "internal_robustness_only"

    hypotheses = syn["hypothesis_disposition"]
    assert hypotheses["USD-H-MIN"] == "resolved_as_multiple_incomparable_minima_in_frozen_universe"
    assert hypotheses["USD-H-NO"] == "unresolved_globally"
    gates = syn["release_gate_evaluation"]
    assert gates["eligible_external_review_completed"] == "fail"
    assert gates["coverage_resolved_for_declared_scope"] == "partial"
    assert gates["reconstruction_and_necessity_resolved"] == "local_only"
    assert syn["terminal_program_classification"] == "bounded_incomparable_kernels_external_validation_pending"
    assert syn["valid_program_outcome_mapping"] == "incomparable_kernels"

    claims = syn["claim_effect"]
    assert claims["one_universal_kernel"] == "not_established"
    assert claims["FARA_is_universal"] == "not_established"
    assert claims["LTS_PROV_is_universal"] == "not_established"
    assert claims["incomparable_kernels"] == "supported_in_frozen_universe"
    assert claims["no_single_nontrivial_kernel"] == "not_established_globally"
    assert claims["independent_verification"] == "not_established"

    assert nxt["program_id"] == "POST-USD-EVC-001"
    assert nxt["status"] == "registered_unexecuted"
    assert nxt["parent_synthesis"] == syn["synthesis_id"]
    ids = {item["id"] for item in nxt["workstreams"]}
    assert ids == {
        "EVC-W1-EXTERNAL-PROOF-REVIEW", "EVC-W2-R3-TECHNICAL-REPLICATION",
        "EVC-W3-R4-ADVERSARIAL-REPLICATION", "EVC-W4-CANDIDATE-EXPANSION",
        "EVC-W5-R5-CROSS-CONTEXT", "EVC-W6-EMPIRICAL-BRIDGE",
    }

    assert "The universal-structure release gate does not pass" in proof
    assert "bounded_incomparable_kernels_external_validation_pending" in proof
    assert "internal multi-implementation robustness is not independent verification" in proof
    assert "weakest-gate rule" in audit
    assert "does not support one universal kernel" in audit

    print("POST-W5 USD terminal synthesis: PASS (bounded incomparable kernels; external validation pending)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
