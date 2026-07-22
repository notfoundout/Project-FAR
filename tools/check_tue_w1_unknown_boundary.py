from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/tue-w1-unknown-boundary-v1.0.json"
PROGRAM = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"
DOC = ROOT / "docs/research/tue-w1-unknown-boundary-v1.0.md"
AUDIT = ROOT / "docs/audits/tue-w1-unknown-boundary-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    for path in (RESULT, PROGRAM, QUEUE, DOC, AUDIT):
        require(path.exists(), f"missing required artifact: {path.relative_to(ROOT)}")
    result, program, queue = map(load, (RESULT, PROGRAM, QUEUE))
    require(result["parent_program"] == program["program_id"] == "POST-SC-TUE-001", "parent program mismatch")
    require(result["target_pr"] == 277, "wrong target PR")
    require(result["program_outcome_mapping"] in program["workstreams"][0]["terminal_outcomes"], "unregistered W1 outcome")
    require(result["next_decisive_workstream"] == "TUE-W2-DEFEATING-CONDITION-CAMPAIGN", "wrong next workstream")
    contract = result["frozen_measurement_contract"]
    for key in ("pre_mapping_source_distinctions_required","candidate_generation_trace_required_for_creative_case","reason_or_salience_elicitation_required_for_moral_case","selective_ground_defeat_intervention_required","path_sensitive_retest_required","uniform_query_interface_required","missing_evidence_is_unknown_not_pass","retrospective_rationalization_not_equivalent_to_process_ground","all_prompting_logging_elicitation_and_decoder_machinery_charged"):
        require(contract.get(key) is True, f"measurement control weakened: {key}")
    cases = result["cases"]
    require([case["id"] for case in cases] == ["UB-CREATIVE-INSTRUMENTED", "UB-MORAL-ELICITED", "UB-INACCESSIBLE-GENERAL"], "case registry changed")
    require(cases[0]["classification"] == "unknown_resolved_within_rccd", "creative case not adjudicated")
    require(cases[1]["classification"] == "principled_inaccessibility_boundary", "moral boundary erased")
    require(cases[2]["classification"] == "principled_inaccessibility_boundary", "inaccessible boundary erased")
    require(cases[2]["rccd_realization"] is None, "inaccessible case falsely mapped as success")
    require(result["counts"] == {"unknowns_resolved_within_rccd":1,"genuine_extension_required":0,"principled_inaccessibility_boundary":2,"mixed_or_unresolved":0}, "terminal counts inconsistent")
    completed = [x["target_pr"] for x in queue["completed_workstreams"]]
    require(completed[:2] == [276, 277], "TUE-W1 completion record changed")
    require(completed == list(range(276, 276 + len(completed))), "queue progression is not contiguous")
    if len(completed) == 2:
        require(queue["next_action"]["target_pr"] == 278, "queue did not advance to PR 278")
        require(queue["ordered_followups"] == [279, 280], "follow-up sequence changed")
    else:
        expected_next = completed[-1] + 1
        if expected_next <= 280:
            require(queue["next_action"]["target_pr"] == expected_next, "later queue progression is invalid")
            require(queue["ordered_followups"] == list(range(expected_next + 1, 281)), "later follow-up sequence invalid")
        else:
            require(queue["status"] == "complete" and queue["next_action"] is None and queue["ordered_followups"] == [], "terminal queue state invalid")
    nonclaims = set(result["nonclaims"])
    for claim in ("inaccessible systems satisfy RCCD", "inaccessible systems refute RCCD", "actual cognitive or physical implementation of RCCD", "external validation"):
        require(claim in nonclaims, f"missing nonclaim: {claim}")
    text = DOC.read_text(encoding="utf-8") + AUDIT.read_text(encoding="utf-8")
    for phrase in ("Unknown is neither Pass nor Fail", "principled_inaccessibility_boundary", "No genuine extension"):
        require(phrase in text, f"documentation missing boundary phrase: {phrase}")
    print("PASS: TUE-W1 unknown-boundary package is complete and remains valid through authorized queue progression")


if __name__ == "__main__":
    main()
