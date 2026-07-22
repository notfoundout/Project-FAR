#!/usr/bin/env python3
"""Validate the frozen EVC-W2 R3 independent replication package."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "theory/evaluation/evc-w2-r3-technical-replication-protocol-v1.0.json"
MANIFEST_PATH = ROOT / "theory/evaluation/evc-w2-r3-replication-package-manifest-v1.0.json"
RESULT_PATH = ROOT / "theory/evaluation/evc-w2-r3-replication-result-template-v1.0.json"
MUTATION_PATH = ROOT / "theory/evaluation/evc-w2-r3-mutation-corpus-v1.0.json"
W1_MANIFEST_PATH = ROOT / "theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json"
PARENT_PATH = ROOT / "theory/evaluation/post-w5-usd-next-program-v1.0.json"
GUIDE_PATH = ROOT / "docs/research/evc-w2-r3-replicator-guide-v1.0.md"
AUDIT_PATH = ROOT / "docs/audits/evc-w2-r3-replication-package-audit.md"

EXPECTED_TARGETS = {
    "R3-T1-W2-FRONTIER": "multiple_incomparable_successful_vocabularies",
    "R3-T2-W3-INVARIANCE": "bounded_invariance_supported",
    "R3-T3-W4-ABLATION": "bounded_local_necessity_supported",
    "R3-T4-W5-MIN-EQUIV": "multiple_incomparable_minima",
    "R3-T5-TERMINAL-SYNTHESIS": "bounded_incomparable_kernels_external_validation_pending",
}
EXPECTED_MUTATIONS = {
    "R3-MUT-EQUIV-COLLAPSE",
    "R3-MUT-HIDDEN-COST-DELETE",
    "R3-MUT-INVARIANCE-INFLATE",
    "R3-MUT-NECESSITY-INFLATE",
    "R3-MUT-UNIQUE-MINIMUM",
    "R3-MUT-COUNTEREXAMPLE-DROP",
    "R3-MUT-INDEPENDENCE-INFLATE",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate() -> list[str]:
    errors: list[str] = []
    required_paths = [
        PROTOCOL_PATH,
        MANIFEST_PATH,
        RESULT_PATH,
        MUTATION_PATH,
        W1_MANIFEST_PATH,
        PARENT_PATH,
        GUIDE_PATH,
        AUDIT_PATH,
    ]
    for path in required_paths:
        if not path.is_file():
            errors.append(f"missing required artifact: {path.relative_to(ROOT)}")
    if errors:
        return errors

    protocol = load_json(PROTOCOL_PATH)
    manifest = load_json(MANIFEST_PATH)
    result = load_json(RESULT_PATH)
    mutations = load_json(MUTATION_PATH)
    w1_manifest = load_json(W1_MANIFEST_PATH)
    parent = load_json(PARENT_PATH)

    if protocol.get("protocol_id") != "EVC-W2-R3-TECHNICAL-REPLICATION-001":
        errors.append("unexpected R3 protocol identifier")
    if protocol.get("status") != "frozen_unexecuted":
        errors.append("R3 protocol must remain frozen_unexecuted")
    if protocol.get("parent_program") != "POST-USD-EVC-001":
        errors.append("R3 protocol must resolve to POST-USD-EVC-001")
    if protocol.get("evidence_layer") != "R3_independent_technical_replication":
        errors.append("R3 evidence layer is not explicit")

    disqualifying = set(protocol.get("replicator_eligibility", {}).get("disqualifying", []))
    if not any("shared agent-controlled" in item for item in disqualifying):
        errors.append("shared agent-controlled work must be disqualifying")
    if not any("same organization" in item for item in disqualifying):
        errors.append("same-organization internal rewrites must be disqualifying")

    targets = {
        item.get("id"): item.get("expected_classification")
        for item in protocol.get("mandatory_replication_targets", [])
    }
    if targets != EXPECTED_TARGETS:
        errors.append("mandatory R3 targets or expected classifications changed")

    protocol_mutations = set(protocol.get("mandatory_mutations", []))
    if len(protocol_mutations) != 7:
        errors.append("protocol must retain seven mandatory mutation descriptions")

    outcomes = set(protocol.get("target_outcomes", []))
    if outcomes != {"replicated", "partially_replicated", "not_replicated", "unresolved"}:
        errors.append("R3 terminal outcome set changed")

    if manifest.get("status") != "frozen_unreleased":
        errors.append("R3 manifest must remain frozen_unreleased")
    release_state = manifest.get("release_state", {})
    forbidden_true = [
        "replicator_recruited",
        "implementation_frozen",
        "reference_results_unsealed",
        "replication_started",
        "replication_completed",
    ]
    if any(release_state.get(key) is True for key in forbidden_true):
        errors.append("R3 release state falsely records execution")
    if release_state.get("release_commit") is not None:
        errors.append("unreleased R3 package cannot have a release commit")
    if release_state.get("first_access_timestamp") is not None:
        errors.append("unreleased R3 package cannot record first access")

    manifest_text = json.dumps(manifest, sort_keys=True)
    if "post-w5-usd-next-program-v1.0.json" not in manifest_text:
        errors.append("R3 manifest omits the POST-USD-EVC-001 parent artifact")
    if "evc-w2-r3-mutation-corpus-v1.0.json" not in manifest_text:
        errors.append("R3 manifest omits the mutation corpus")
    if "original executable implementations are not silently included" not in manifest_text:
        errors.append("R3 manifest does not enforce clean-room implementation separation")

    result_target_ids = {item.get("target_id") for item in result.get("target_results", [])}
    if result_target_ids != set(EXPECTED_TARGETS):
        errors.append("result template target set differs from protocol")
    result_mutation_ids = {item.get("mutation_id") for item in result.get("mutation_results", [])}
    if result_mutation_ids != EXPECTED_MUTATIONS:
        errors.append("result template mutation set differs from corpus")
    declaration = result.get("replicator_declaration", {})
    if declaration.get("original_implementation_used") is not False:
        errors.append("result template must default original implementation reuse to false")
    if declaration.get("shared_agent_or_author_control") is not False:
        errors.append("result template must default shared control to false")
    if result.get("initial_outcome") is not None:
        errors.append("unexecuted result template cannot contain an outcome")

    mutation_ids = {item.get("id") for item in mutations.get("mutations", [])}
    if mutation_ids != EXPECTED_MUTATIONS:
        errors.append("mutation corpus changed or is incomplete")
    protected_gates = {item.get("protected_gate") for item in mutations.get("mutations", [])}
    if len(protected_gates) != 7:
        errors.append("each R3 mutation must protect a distinct registered gate")

    parent_workstreams = {item.get("id") for item in parent.get("workstreams", [])}
    if "EVC-W2-R3-TECHNICAL-REPLICATION" not in parent_workstreams:
        errors.append("parent program does not register EVC-W2")

    w1_text = json.dumps(w1_manifest, sort_keys=True)
    if "post-w5-usd-next-program-v1.0.json" not in w1_text:
        errors.append("EVC-W1 manifest still omits the parent POST-USD-EVC-001 artifact")
    if "the parent POST-USD-EVC-001 registration artifact is included" not in w1_text:
        errors.append("EVC-W1 completeness checks do not enforce the parent program")

    guide = GUIDE_PATH.read_text(encoding="utf-8")
    audit = AUDIT_PATH.read_text(encoding="utf-8")
    for phrase in ["separate human or organization", "reference outputs remain sealed", "Claim boundary"]:
        if phrase not in guide:
            errors.append(f"replicator guide missing required phrase: {phrase}")
    for phrase in ["frozen_unexecuted", "No replicator has been recruited", "Prior package correction"]:
        if phrase not in audit:
            errors.append(f"audit missing required phrase: {phrase}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("EVC-W2 R3 replication package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
