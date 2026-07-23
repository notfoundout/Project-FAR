from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "theory/evaluation/post-tue-universal-proof-program-v1.0.json"

EXPECTED_WORKSTREAMS = [
    "UPP-W0-REGISTRATION",
    "UPP-W1-FOUNDATION",
    "UPP-W2-CLASS",
    "UPP-W3-CONTRACT",
    "UPP-W4-REPRESENTATIONS",
    "UPP-W5-MACHINERY-CLOSURE",
    "UPP-W6-EQUIVALENCE",
    "UPP-W7-R1",
    "UPP-W8-R2",
    "UPP-W9-R3",
    "UPP-W10-R4",
    "UPP-W11-R5",
    "UPP-W12-SUFFICIENCY",
    "UPP-W13-IRREDUCIBILITY",
    "UPP-W14-MAXIMALITY",
    "UPP-W15-TERMINAL-THEOREM",
]

EXPECTED_OUTCOMES = {
    "full_registered_universal_theorem_proved",
    "strictly_weakened_universal_theorem_proved",
    "rccd_requires_extension_or_revision",
    "rccd_universality_defeated",
    "proof_blocked_by_indispensable_unproved_assumption",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    data = json.loads(PROGRAM.read_text(encoding="utf-8"))

    require(data["schema_version"] == "1.0", "unexpected schema version")
    require(data["program_id"] == "POST-TUE-UPP-001", "unexpected program id")
    require(data["status"] == "registered", "program must be registered")

    checkpoint = data["starting_checkpoint"]
    require(checkpoint["source_pr"] == 280, "program must start from PR 280")
    require(
        checkpoint["classification"]
        == "terminal_finite_internal_adjudication_evidence_not_universal_proof",
        "PR 280 must not be promoted into universal proof",
    )

    workstreams = data["workstreams"]
    require(len(workstreams) == 16, "expected sixteen workstreams")
    require([item["sequence"] for item in workstreams] == list(range(1, 17)), "invalid sequence")
    require([item["target_pr"] for item in workstreams] == list(range(281, 297)), "invalid PR plan")
    require([item["id"] for item in workstreams] == EXPECTED_WORKSTREAMS, "invalid workstream ids")

    require(set(data["terminal_outcomes"]) == EXPECTED_OUTCOMES, "terminal outcomes changed")

    standard = data["proof_standard"]
    for key in (
        "finite_testing_is_not_proof",
        "absence_of_counterexample_is_not_universality",
        "central_claims_must_be_mechanized",
        "definitions_must_not_encode_the_conclusion",
        "hidden_machinery_is_charged",
        "unknown_is_neither_support_nor_defeat",
        "failed_lemma_requires_revision_or_weakening",
        "supportive_work_may_not_be_inserted_to_force_the_preferred_outcome",
    ):
        require(standard.get(key) is True, f"proof control disabled: {key}")

    gate = data["release_gate"]
    require(gate["public_evaluation_authorized"] is False, "release gate must remain closed")
    require("terminal UPP-W15 outcome" in gate["authorization_condition"], "release condition weakened")

    require(data["next_action"] == {"target_pr": 282, "workstream": "UPP-W1-FOUNDATION"}, "wrong next action")
    require(data["ordered_followups"] == list(range(283, 297)), "wrong followup queue")

    print("PASS: universal proof program registration is internally consistent")


if __name__ == "__main__":
    main()
