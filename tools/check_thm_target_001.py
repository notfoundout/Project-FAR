#!/usr/bin/env python3
"""Validate the frozen THM-TARGET-001 theorem target and premise ledger."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/thm-target-001-v1.0.md"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
LEDGER = ROOT / "theory/evaluation/thm-target-001-premise-ledger.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(text: str, phrases: list[str], label: str) -> None:
    for phrase in phrases:
        assert phrase in text, f"{label} missing required phrase: {phrase}"


def main() -> int:
    for path in [DOC, TARGET, LEDGER, GATES, CLAIMS]:
        assert path.is_file(), f"missing THM-TARGET-001 artifact: {path.relative_to(ROOT)}"

    doc = DOC.read_text(encoding="utf-8")
    require(
        doc,
        [
            "Frozen prospective theorem target and premise boundary",
            "### 1.2 Finite explicit core `S_core`",
            "### 1.3 General extension class `S_IRD`",
            "### 2.1 FARA theorem-facing package",
            "## 5. P8 parameter",
            "## 7. Uniformity and nontriviality",
            "### THM-CORE-COMMON-001",
            "### THM-CORE-REP-001",
            "### THM-IRD-EXT-001",
            "### THM-IMP-001",
            "This artifact does not establish",
            "Create a frozen faithful-representation specification",
        ],
        "THM-TARGET-001 document",
    )
    for prohibited in [
        "THM-CORE-REP-001 is proved",
        "FARA is universal",
        "FARA is minimal",
        "P8 has been resolved",
    ]:
        assert prohibited not in doc, f"theorem target contains prohibited claim: {prohibited}"

    target = load(TARGET)
    assert target.get("schema_version") == "1.0"
    assert target.get("theorem_target_id") == "THM-TARGET-001"
    assert target.get("version") == "1.0"
    assert target.get("status") == "frozen_unproved"
    assert target.get("proof_status") == "none"
    assert target.get("machine_check_status") == "not_started"
    assert target.get("independent_review_status") == "not_started"
    assert target.get("source_artifact") == "docs/research/thm-target-001-v1.0.md"
    assert target.get("premise_ledger") == "theory/evaluation/thm-target-001-premise-ledger.json"

    source_classes = target.get("source_classes", {})
    assert set(source_classes) == {"S_core", "S_IRD"}
    assert source_classes["S_core"].get("status") == "frozen_initial_scope"
    assert source_classes["S_IRD"].get("status") == "frozen_extension_target"

    target_class = target.get("target_class", {})
    assert target_class.get("id") == "A_FARA"
    assert target_class.get("adds_new_primitive") is False
    assert target_class.get("tuple") == [
        "U", "Pi", "R", "Rep", "S", "I", "Inv", "C", "Sigma", "Theta", "H", "Omega", "Res", "Prov"
    ]

    witness = target.get("representation_witness", {})
    assert witness.get("tuple") == ["E", "D", "M", "iota", "kappa"]
    assert witness.get("uniform_construction_required") is True
    assert witness.get("complete_machinery_ledger_required") is True
    assert witness.get("source_specific_unrestricted_decoder_allowed") is False

    assert target.get("preservation_obligations") == [
        "P1_configuration",
        "P2_commitment",
        "P3_stake_and_alternative",
        "P4_ground_and_justification",
        "P5_admissibility_and_dynamics",
        "P6_consequence",
        "P7_historical_and_path",
    ]
    p8 = target.get("p8", {})
    assert p8.get("status") == "unresolved_theorem_parameter"
    assert p8.get("allowed_values") == ["coordinate", "side_condition", "split"]
    assert p8.get("proof_acceptance_blocked_until_resolved") is True

    theorem_family = target.get("theorem_family", [])
    by_id = {item.get("id"): item for item in theorem_family}
    required_ids = {
        "THM-CORE-COMMON-001",
        "THM-CORE-REP-001",
        "THM-IRD-EXT-001",
        "THM-P8-CORR-001",
        "THM-PRIM-NEC-001",
        "THM-MIN-001",
        "THM-EQUIV-001",
        "THM-IMP-001",
    }
    assert required_ids == set(by_id)
    assert all(item.get("status") != "proved" for item in theorem_family)
    assert by_id["THM-CORE-REP-001"].get("scope") == "S_core"
    assert by_id["THM-IRD-EXT-001"].get("scope") == "S_IRD"

    gate_snapshot = target.get("current_gates", {})
    assert gate_snapshot.get("formal_theorem_target") == "satisfied"
    assert gate_snapshot.get("premise_ledger_and_semantics") == "in_progress"
    for name in [
        "faithful_representation_definition",
        "scoped_representation_proof",
        "primitive_lower_bounds",
        "minimality_universe_and_proof",
        "mechanized_proof_verification",
        "independent_proof_review",
    ]:
        assert gate_snapshot.get(name) == "not_satisfied"

    ledger = load(LEDGER)
    assert ledger.get("schema_version") == "1.0"
    assert ledger.get("ledger_id") == "THM-TARGET-001-PREMISES"
    assert ledger.get("version") == "1.0"
    assert ledger.get("status") == "frozen_with_explicit_open_parameters"
    entries = ledger.get("entries", [])
    assert len(entries) == 22
    ids = [entry.get("id") for entry in entries]
    assert len(ids) == len(set(ids))
    assert ids == [f"PRM-{i:03d}" for i in range(1, 23)]
    allowed_classes = {
        "definition",
        "typing_or_well_formedness_condition",
        "imported_frozen_specification",
        "substantive_axiom",
        "scope_restriction",
        "evidence_condition",
        "conjecture",
        "unresolved_theorem_parameter",
    }
    classifications = Counter(entry.get("classification") for entry in entries)
    assert set(classifications) <= allowed_classes
    assert classifications == Counter(ledger.get("classification_counts", {}))
    assert any(entry.get("status") == "open" for entry in entries)
    assert any(entry.get("status") == "explicitly_absent" for entry in entries)

    gate_effect = ledger.get("gate_effect", {})
    assert gate_effect == {
        "formal-theorem-target": "satisfied",
        "premise-ledger-and-semantics": "in_progress",
        "faithful-representation-definition": "not_satisfied",
    }

    gates = load(GATES)
    gates_by_name = {gate.get("name"): gate for gate in gates.get("gates", [])}
    formal_target = gates_by_name["formal-theorem-target"]
    assert formal_target.get("status") == "satisfied"
    assert set(formal_target.get("evidence", [])) == {
        "docs/research/thm-target-001-v1.0.md",
        "theory/evaluation/thm-target-001.json",
        "theory/evaluation/thm-target-001-premise-ledger.json",
    }
    premise_gate = gates_by_name["premise-ledger-and-semantics"]
    assert premise_gate.get("status") == "in_progress"
    assert "theory/evaluation/thm-target-001-premise-ledger.json" in premise_gate.get("evidence", [])
    for name in [
        "faithful-representation-definition",
        "scoped-representation-proof",
        "primitive-lower-bounds",
        "minimality-universe-and-proof",
        "mechanized-proof-verification",
        "independent-proof-review",
    ]:
        assert gates_by_name[name].get("status") != "satisfied"

    claims = load(CLAIMS)
    for claim in claims.get("claims", []):
        if claim.get("id") in {"CLM-EXISTENCE", "CLM-UNIVERSALITY", "CLM-NECESSITY", "CLM-MINIMALITY"}:
            assert claim.get("current_status") != "supported"

    print("THM-TARGET-001 validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
