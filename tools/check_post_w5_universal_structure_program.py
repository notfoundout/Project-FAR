#!/usr/bin/env python3
"""Validate the frozen post-W5 universal-structure program."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/post-w5-universal-structure-program-v1.0.json"
DOCUMENT = ROOT / "docs/research/post-w5-universal-structure-program-v1.0.md"

REQUIRED_WORKSTREAMS = {
    "USD-W1-SCOPE-EXT",
    "USD-W2-ALT-VOCAB",
    "USD-W3-INVARIANCE",
    "USD-W4-NECESSITY",
    "USD-W5-MIN-EQUIV",
    "USD-W6-INDEPENDENCE",
}
REQUIRED_HYPOTHESES = {
    "USD-H-EXIST",
    "USD-H-INV",
    "USD-H-DISC",
    "USD-H-NEC",
    "USD-H-MIN",
    "USD-H-NO",
}
REQUIRED_OUTCOMES = {
    "one_universal_kernel",
    "proper_subclass_kernel",
    "translation_equivalent_kernels",
    "incomparable_kernels",
    "generic_structured_system_properties_only",
    "no_single_nontrivial_kernel",
    "unresolved",
}
REQUIRED_RULES = {
    "unknown_is_not_pass",
    "bounded_success_is_not_universality",
    "representation_is_not_necessity",
    "failure_to_find_counterexample_is_not_proof",
    "candidate_specific_scope_selection_is_prohibited",
    "hidden_interpreters_and_metadata_smuggling_are_prohibited",
    "equivalent_reintroduction_counts_against_elimination",
    "tradeoffs_are_not_wins",
    "material_post_freeze_change_creates_new_version",
    "negative_and_no_go_results_are_terminal_scientific_results",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(REGISTRY.is_file(), f"missing registry: {REGISTRY.relative_to(ROOT)}")
    require(DOCUMENT.is_file(), f"missing document: {DOCUMENT.relative_to(ROOT)}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    document = DOCUMENT.read_text(encoding="utf-8")

    require(data.get("program_id") == "POST-W5-USD-001", "wrong program id")
    require(data.get("version") == "1.0", "wrong program version")
    require(data.get("status") == "frozen_prospective_unexecuted", "program must remain prospective and unexecuted")
    require(data.get("program_track") == "USD", "program must remain on the USD track")
    require(data.get("governing_target") == "THM-US-TARGET-001", "wrong governing theorem target")

    representation_input = data.get("representation_result_input", {})
    require(representation_input.get("theorem") == "THM-CORE-REP-001", "missing bounded representation input")
    require(representation_input.get("scope") == "S_core", "bounded input scope changed")
    require(representation_input.get("logical_effect_on_usd") == "none", "REP must not imply USD")

    hypotheses = {item.get("id") for item in data.get("frozen_hypotheses", [])}
    require(hypotheses == REQUIRED_HYPOTHESES, f"hypothesis set mismatch: {hypotheses}")
    require(all(item.get("status") == "unresolved" for item in data["frozen_hypotheses"]), "prospective hypotheses must remain unresolved")

    workstreams = {item.get("id"): item for item in data.get("workstreams", [])}
    require(set(workstreams) == REQUIRED_WORKSTREAMS, f"workstream set mismatch: {set(workstreams)}")
    require(all(item.get("status") == "registered_unexecuted" for item in workstreams.values()), "workstreams must remain unexecuted")

    feature_families = set(workstreams["USD-W1-SCOPE-EXT"].get("feature_families", []))
    require({"partial_observability", "semantic_change", "actual_process_correspondence"} <= feature_families, "scope extension families incomplete")

    competition = workstreams["USD-W2-ALT-VOCAB"].get("minimum_competition", {})
    require(competition.get("independently_motivated_non_fara_candidates", 0) >= 2, "alternative competition is not materially plural")
    require(workstreams["USD-W2-ALT-VOCAB"].get("aggregation_rule") == "pareto_only_no_scalar_overall_winner", "competition aggregation changed")

    rules = data.get("decision_rules", {})
    require(REQUIRED_RULES <= set(rules), "required decision rules missing")
    require(all(rules[key] is True for key in REQUIRED_RULES), "required decision rules must be enabled")

    require(set(data.get("valid_program_outcomes", [])) == REQUIRED_OUTCOMES, "valid outcome set changed")
    require(data.get("next_decisive_execution") == "USD-W1-SCOPE-EXT", "next decisive execution changed")

    release_gate = data.get("release_gate", {})
    universal_gate = set(release_gate.get("universal_structure_claim", []))
    require({
        "coverage_resolved_for_declared_scope",
        "representation_invariance_resolved",
        "reasoning_discrimination_resolved",
        "reconstruction_and_necessity_resolved",
        "minimality_or_equivalence_classified",
        "claim_scope_matches_proof_scope",
    } <= universal_gate, "universal release gate is incomplete")

    required_document_fragments = [
        "The first result does not logically imply the second.",
        "Unknown is not Pass.",
        "Bounded success is not universality.",
        "Representation is not necessity.",
        "Tradeoffs are not wins.",
        "partial observability",
        "Independent verification additionally requires",
    ]
    for fragment in required_document_fragments:
        require(fragment in document, f"missing controlling document fragment: {fragment}")

    print("post-W5 universal-structure program: valid")


if __name__ == "__main__":
    main()
