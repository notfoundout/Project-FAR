#!/usr/bin/env python3
"""Validate FAITHFUL-REP-001 after completion of the source-side W0 kernel."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/faithful-representation-specification-v1.0.md"
REG = ROOT / "theory/evaluation/faithful-representation-specification-v1.0.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
PREMISES = ROOT / "theory/evaluation/thm-target-001-premise-ledger.json"
P8_DECISION = ROOT / "theory/evaluation/p8-theorem-role-decision.json"
LEMMA_REG = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"
W0_DOC = ROOT / "docs/research/s-core-w0-normalization-proof-v1.0.md"
W0_REG = ROOT / "theory/evaluation/s-core-w0-normalization-proof.json"
GATES = ROOT / "theory/evaluation/research-gates.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_true(mapping: dict, keys: set[str], label: str) -> None:
    for key in sorted(keys):
        assert mapping.get(key) is True, f"{label}.{key} must be true"


def main() -> int:
    for path in (DOC, REG, TARGET, PREMISES, P8_DECISION, LEMMA_REG, W0_DOC, W0_REG, GATES):
        assert path.is_file(), f"missing faithful-representation artifact: {path.relative_to(ROOT)}"

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "strong typed correspondence",
        "Relation preservation and reflection",
        "finite labeled probabilistic bisimulation",
        "Cross-axis coherence",
        "P8 parameterized clauses",
        "Uniform construction",
        "Complete machinery ledger",
        "Faithful_{m_8}",
        "unknown` blocks theorem acceptance",
        "does not prove that any source object has a faithful FARA representation",
    ):
        assert phrase in text, f"faithful specification missing required phrase: {phrase}"

    data = load(REG)
    assert data.get("schema_version") == "1.0"
    assert data.get("specification_id") == "FAITHFUL-REP-001"
    assert data.get("version") == "1.0"
    assert data.get("status") == "frozen_definition_w0_source_kernel_proved_target_satisfiability_unproved"
    assert data.get("source_scope") == "S_core"
    assert data.get("source_artifact") == DOC.relative_to(ROOT).as_posix()
    assert data.get("theorem_target") == "THM-TARGET-001"
    assert data.get("lemma_ledger_registry") == LEMMA_REG.relative_to(ROOT).as_posix()
    assert data.get("w0_proof_artifact") == W0_DOC.relative_to(ROOT).as_posix()
    assert data.get("w0_proof_registry") == W0_REG.relative_to(ROOT).as_posix()

    source = data.get("source_contract", {})
    assert source.get("tuple") == ["tau_S", "Mat", "ValEq", "App"]
    require_true(source, {"owned_by_source", "materiality_closure_required", "exclusion_certificate_required"}, "source_contract")
    assert source.get("target_may_weaken") is False
    assert source.get("unknown_applicability_allowed_for_theorem") is False
    assert source.get("finite_normalization_status") == "proved_LEM-SC-001"
    assert source.get("canonical_reduct_extraction_status") == "proved_LEM-SC-002"
    assert source.get("materiality_closure_and_applicability_status") == "proved_LEM-SC-003"
    assert source.get("source_isomorphism_transport_status") == "proved_LEM-SC-004"
    assert source.get("nonfinite_closure_status") == "outside_S_core_OBS-SC-001"

    axes = data.get("axis_reducts", [])
    assert [axis.get("id") for axis in axes] == [f"P{i}" for i in range(1, 8)]
    assert len({axis.get("name") for axis in axes}) == 7
    assert all(axis.get("required_content") for axis in axes)
    extraction = data.get("axis_reduct_extraction", {})
    assert extraction.get("status") == "proved_source_side"
    assert extraction.get("proof_obligation") == "LEM-SC-002"
    assert extraction.get("includes_internal_P8I_reduct") is True
    assert extraction.get("does_not_establish_target_preservation") is True

    recovery = data.get("recovery_contract", {})
    require_true(recovery, {"fixed_versioned_interface", "target_only_after_construction", "deterministic", "terminates_on_S_core", "pure", "derived_relations_declared_in_ledger"}, "recovery_contract")
    for key in ("source_identifier_allowed", "external_narrative_allowed", "evaluator_input_allowed", "hidden_oracle_allowed"):
        assert recovery.get(key) is False, f"recovery_contract.{key} must be false"

    correspondence = data.get("correspondence_package", {})
    assert correspondence.get("tuple") == ["phi_i", "psi_i", "rho_i"]
    require_true(correspondence, {"totality", "type_preservation", "element_injectivity", "relation_preservation", "relation_reflection", "attribute_preservation_under_source_equivalence", "exact_equality_default", "image_accountability"}, "correspondence_package")

    semantics = data.get("semantic_agreement", {})
    require_true(semantics, {"source_declared_equivalence", "bridges_declared_and_ledgered"}, "semantic_agreement")
    assert semantics.get("lexical_labels_sufficient") is False
    assert semantics.get("semantic_strengthening_allowed") is False

    coherence = data.get("cross_axis_coherence", {})
    require_true(coherence, {"required", "semantic_compatibility_required", "duplication_must_be_ledgered"}, "cross_axis_coherence")
    assert coherence.get("conflicts_allowed") is False

    p8 = data.get("p8", {})
    assert p8.get("selected_mode") == "split"
    assert set(p8.get("allowed_modes", [])) == {"coordinate", "side_condition", "split"}
    assert p8.get("clauses_frozen_for_all_modes") is True
    assert p8.get("proof_acceptance_blocked_until_selection") is False
    assert p8.get("internal_predicate") == "Pres_8I"
    assert p8.get("external_predicate") == "Corr_8E"
    for mode in ("coordinate", "side_condition", "split"):
        assert p8.get(mode), f"missing P8 clause: {mode}"

    p8_decision = load(P8_DECISION)
    assert p8_decision.get("selected_mode") == "split"
    assert p8_decision.get("internal_obligation", {}).get("predicate") == "Pres_8I"
    assert p8_decision.get("external_obligation", {}).get("predicate") == "Corr_8E"
    assert p8_decision.get("external_obligation", {}).get("not_implied_by_formal_representation") is True

    uniformity = data.get("uniformity", {})
    require_true(uniformity, {"one_identifier_version_definition_and_input_schema", "helpers_fixed_and_ledgered", "source_isomorphism_equivariance_required", "effective_and_terminating_on_S_core"}, "uniformity")
    assert uniformity.get("case_identifier_branching_allowed") is False
    assert uniformity.get("case_database_allowed") is False
    assert uniformity.get("source_reaccess_after_construction_allowed_for_recovery") is False
    assert uniformity.get("source_normalization_equivariance_status") == "proved_LEM-SC-004"
    assert uniformity.get("target_constructor_equivariance_status") == "unproved_LEM-SC-022"

    composition = data.get("compositional_accountability", {})
    require_true(composition, {"conditional_on_declared_decomposition", "component_encoding_required", "interface_mapping_required", "cross_component_relations_required", "restriction_commutes_up_to_declared_equivalence", "indecomposable_declaration_allowed"}, "compositional_accountability")

    machinery = data.get("machinery_ledger", {})
    require_true(machinery, {"finite_dependency_graph_required", "all_E_D_M_iota_dependencies_resolve"}, "machinery_ledger")
    assert machinery.get("metadata_is_free") is False
    assert len(machinery.get("covers", [])) >= 10
    assert machinery.get("missing_dependency_effect") == "inadmissible_hidden_machinery"

    controls = data.get("nontriviality", {}).get("negative_control_mapping", {})
    assert set(controls) == {f"NC-{i:02d}" for i in range(1, 11)}
    assert all(controls[key] for key in controls)
    assert "Pres_8I" in controls["NC-08"]

    required_formula = {"WF_S_core", "WF_A_FARA", "WF_W", "AdmissibleRecovery", "all_applicable_Pres_1_through_Pres_7", "Pres_8I", "SemAgree", "Coherent", "Uniform", "CompAccount", "LedgerComplete", "Nontrivial"}
    assert set(data.get("faithful_formula", [])) == required_formula
    assert data.get("decision_semantics", {}).get("unknown") == "blocks_theorem_acceptance"
    assert data.get("next_required_artifact") == "W1 base-carrier and direct-axis construction proof package"
    assert "actual-process correspondence is established" in data.get("nonclaims", [])
    assert "any W1 through W5 obligation is proved" in data.get("nonclaims", [])

    lemma = load(LEMMA_REG)
    assert lemma.get("ledger_id") == "SCORE-LEMMA-LEDGER-001"
    assert lemma.get("status") == "frozen_dependency_decomposition_w0_complete_w1_active"
    assert lemma.get("execution_summary", {}).get("proved") == 4
    assert lemma.get("execution_summary", {}).get("scope_boundary_established") == 1
    assert lemma.get("execution_summary", {}).get("open") == 32

    w0 = load(W0_REG)
    assert w0.get("proof_id") == "SCORE-W0-PROOF-001"
    assert w0.get("verification", {}).get("proof_assistant_status") == "not_started"
    assert w0.get("verification", {}).get("independent_review_status") == "not_started"

    target = load(TARGET)
    current = target.get("current_gates", {})
    assert current.get("formal_theorem_target") == "satisfied"
    assert current.get("premise_ledger_and_semantics") == "satisfied"
    assert current.get("faithful_representation_definition") == "satisfied"
    assert current.get("scoped_representation_proof") == "not_satisfied"
    assert target.get("proof_status") == "partial_lemmas_only"
    core = {item.get("id"): item for item in target.get("theorem_family", [])}["THM-CORE-REP-001"]
    assert core.get("predicate") == "Faithful_split"
    assert core.get("blocked_by") == ["lemma_ledger_execution"]

    premises = load(PREMISES)
    by_id = {item.get("id"): item for item in premises.get("entries", [])}
    for premise_id in ("PRM-011", "PRM-012"):
        premise = by_id[premise_id]
        assert premise.get("status") == "semantics_frozen_unproved_satisfiability"
        assert not premise.get("blocks")
    assert "P8 mode" not in premises.get("open_items", [])

    gates = load(GATES)
    by_name = {gate.get("name"): gate for gate in gates.get("gates", [])}
    for name in ("formal-theorem-target", "premise-ledger-and-semantics", "faithful-representation-definition"):
        assert by_name[name].get("status") == "satisfied", f"{name} must be satisfied"
        assert by_name[name].get("evidence"), f"{name} requires evidence"
    assert by_name["scoped-representation-proof"].get("status") == "not_satisfied"
    assert by_name["mechanized-proof-verification"].get("status") == "not_satisfied"
    assert by_name["independent-proof-review"].get("status") == "not_satisfied"

    print("FAITHFUL-REP-001 validation PASS (source W0 proved; target construction unproved; W1 active)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
