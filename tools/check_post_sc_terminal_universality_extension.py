from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"
DOC = ROOT / "docs/research/post-sc-terminal-universality-extension-v1.0.md"
AUDIT = ROOT / "docs/audits/post-sc-terminal-universality-extension-audit.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (PROGRAM, QUEUE, DOC, AUDIT):
        require(path.exists(), f"missing artifact: {path.relative_to(ROOT)}")

    program = load(PROGRAM)
    queue = load(QUEUE)

    require(program["program_id"] == "POST-SC-TUE-001", "wrong program id")
    require(program["status"] == "registered_unexecuted", "program must remain unexecuted")
    require(program["registration_pr"] == 276, "registration PR must be 276")
    require(program["parent_adjudication"] == "SC-W6-FINAL-INTERNAL-ADJUDICATION-001", "wrong parent")

    workstreams = program["workstreams"]
    require([w["sequence"] for w in workstreams] == [1, 2, 3, 4], "sequence must be contiguous")
    require([w["target_pr"] for w in workstreams] == [277, 278, 279, 280], "target PRs must be 277-280")
    require([w["id"] for w in workstreams] == [
        "TUE-W1-UNKNOWN-BOUNDARY",
        "TUE-W2-DEFEATING-CONDITION-CAMPAIGN",
        "TUE-W3-DEEPER-KERNEL",
        "TUE-W4-FINAL-QUESTION-ANSWER",
    ], "unexpected workstream order")

    require(len(program["frozen_sc_w6_defeating_conditions"]) == 5, "all five defeating conditions must be frozen")
    require(program["hard_stopping_rule"]["terminal_pr"] == 280, "terminal PR must be 280")
    require(program["hard_stopping_rule"]["external_review_disposition"] == "deferred_until_pr_280_final_answer", "external review must remain deferred")

    final_outcomes = set(workstreams[-1]["terminal_outcomes"])
    require(final_outcomes == {
        "maximal_effective_rccd_universality",
        "rccd_requires_extension_or_plural_kernel",
        "unrestricted_question_evidentially_underdetermined",
    }, "final outcomes must preserve positive, negative/plural, and epistemic-boundary answers")

    require(queue["queue_id"] == "POST-SC-TUE-QUEUE-001", "wrong queue id")
    require(queue["status"] == "frozen", "queue must be frozen")
    require(queue["next_action"]["target_pr"] == 277, "PR 277 must be next")
    require(queue["next_action"]["workstream"] == "TUE-W1-UNKNOWN-BOUNDARY", "wrong next workstream")
    require(queue["ordered_followups"] == [278, 279, 280], "wrong follow-up sequence")
    require("external proof review before PR 280" in queue["blocked_actions"], "external review block missing")
    require("insert additional supportive workstreams" in queue["blocked_actions"], "anti-confirmation block missing")

    prose = DOC.read_text(encoding="utf-8") + AUDIT.read_text(encoding="utf-8")
    for token in ("Unknown is not", "PR #280", "defeating condition", "External review"):
        require(token in prose, f"missing prose control: {token}")

    print("PASS: terminal universality extension program is registered, bounded, adversarial, and stopped at PR 280")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
