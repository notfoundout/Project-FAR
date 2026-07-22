#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json"
RESEARCH = ROOT / "docs/research/ikd-w1-candidate-architecture-freeze-v1.0.md"
AUDIT = ROOT / "docs/audits/ikd-w1-candidate-architecture-freeze-audit.md"
PARENT = ROOT / "theory/evaluation/post-usd-internal-discovery-continuation-v1.0.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (FREEZE, RESEARCH, AUDIT, PARENT):
        assert path.is_file(), path

    freeze = load(FREEZE)
    parent = load(PARENT)
    research = RESEARCH.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert freeze["freeze_id"] == "IKD-W1-CANDIDATE-FREEZE-001"
    assert freeze["status"] == "frozen_unexecuted"
    assert freeze["parent_program"] == "POST-USD-IKD-001"
    assert freeze["target_pr"] == 261
    assert parent["program_id"] == freeze["parent_program"]

    rule = freeze["admission_rule"]
    assert rule["candidate_independent"] is True
    assert rule["admission_before_scoring"] is True
    assert len(rule["required_declaration"]) >= 10
    assert "not_a_hidden_commitment_equivalent_reconstruction" in rule["material_novelty_tests"]
    assert "unrestricted_interpreter" in rule["automatic_rejection"]
    assert "winner_compatible_admission_only" in rule["automatic_rejection"]

    candidates = freeze["frozen_candidates"]
    assert len(candidates) == 6
    assert len({item["id"] for item in candidates}) == 6
    assert len({item["family"] for item in candidates}) == 6
    required_families = {
        "process_or_category_theoretic",
        "causal_model",
        "proof_or_type_theoretic",
        "information_flow",
        "dynamical_or_coalgebraic",
        "algebraic",
    }
    assert {item["family"] for item in candidates} == required_families
    for candidate in candidates:
        assert candidate["status"] == "admitted_frozen_unscored"
        assert candidate["conceptual_source"]
        assert len(candidate["primitive_commitments"]) >= 4
        assert candidate["distinctive_constraint"]

    contract = freeze["comparison_contract"]
    assert len(contract["preservation_dimensions"]) == 6
    assert contract["aggregation"] == "pareto_only_no_scalar_score"
    assert contract["candidate_specific_repair"] == "prohibited"
    assert contract["unknown_rule"] == "Unknown is unresolved and is not Pass"

    gate = freeze["execution_gate"]
    assert gate["next_workstream"] == "IKD-W2-EXPANDED-COMPETITION"
    assert "candidate_scoring" in gate["prohibited_before_merge"]
    assert "universal_structure_claim" in gate["prohibited_before_merge"]

    assert "Candidate families are frozen before scoring" in audit
    assert "Equivalent reintroduction is not elimination" in audit
    assert "Merging this freeze authorizes `IKD-W2-EXPANDED-COMPETITION`" in research
    assert "candidate_architecture_universe_frozen_unexecuted" in audit

    print("IKD-W1 candidate architecture freeze: PASS (6 materially distinct families; unscored)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
