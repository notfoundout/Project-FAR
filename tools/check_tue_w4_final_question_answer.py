from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/tue-w4-final-question-answer-v1.0.json"
CLOSURE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json"
PROGRAM = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-v1.0.json"
DOC = ROOT / "docs/research/tue-w4-final-question-answer-v1.0.md"
AUDIT = ROOT / "docs/audits/tue-w4-final-question-answer-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    for path in (RESULT, CLOSURE, PROGRAM, DOC, AUDIT):
        require(path.exists(), f"missing artifact: {path.relative_to(ROOT)}")
    result, closure, program = map(load, (RESULT, CLOSURE, PROGRAM))
    require(result["parent_program"] == program["program_id"] == closure["parent_program"] == "POST-SC-TUE-001", "program mismatch")
    require(program["status"] == "registered_unexecuted", "registration contract was mutated")
    require(program["hard_stopping_rule"]["terminal_pr"] == 280, "hard stop changed")
    require(result["target_pr"] == 280, "wrong terminal PR")
    require(result["terminal_outcome"] in program["workstreams"][3]["terminal_outcomes"], "unregistered outcome")
    require(result["terminal_outcome"] == "maximal_effective_rccd_universality", "unexpected terminal outcome")
    require(result["program_disposition"] == "closed_with_final_internal_answer", "program not closed by terminal result")
    require(result["next_action"] is None and result["authorized_internal_followups"] == [], "followups remain")
    require(len(result["defeating_conditions_preserved"]) == 5, "defeating conditions changed")
    require(closure["status"] == "complete", "closure not complete")
    require(closure["program_disposition"] == "closed_with_final_internal_answer", "closure disposition wrong")
    require(closure["next_action"] is None and closure["ordered_followups"] == [], "closure still active")
    require([x["target_pr"] for x in closure["completed_workstreams"]] == [276, 277, 278, 279, 280], "completion sequence wrong")
    text = DOC.read_text(encoding="utf-8") + AUDIT.read_text(encoding="utf-8")
    for phrase in ("Unknown is neither Pass nor Fail", "maximal_effective_rccd_universality", "next_action: null", "metaphysical fundamentality"):
        require(phrase in text, f"missing boundary phrase: {phrase}")
    print("PASS: TUE-W4 issues the bounded terminal answer and closes supportive internal discovery")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
