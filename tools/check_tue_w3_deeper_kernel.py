from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "theory/evaluation/tue-w3-deeper-kernel-protocol-v1.0.json"
CANDIDATES = ROOT / "theory/evaluation/tue-w3-deeper-kernel-candidates-v1.0.json"
RESULT = ROOT / "theory/evaluation/tue-w3-deeper-kernel-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/tue-w3-queue-checkpoint-v1.0.json"
LIVE_QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"
DOC = ROOT / "docs/research/tue-w3-deeper-kernel-v1.0.md"
AUDIT = ROOT / "docs/audits/tue-w3-deeper-kernel-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    for path in (PROTOCOL, CANDIDATES, RESULT, QUEUE, LIVE_QUEUE, DOC, AUDIT):
        require(path.exists(), f"missing artifact: {path.relative_to(ROOT)}")
    protocol, corpus, result, queue = map(load, (PROTOCOL, CANDIDATES, RESULT, QUEUE))
    live_queue = load(LIVE_QUEUE)
    require(protocol["parent_program"] == result["parent_program"] == "POST-SC-TUE-001", "parent mismatch")
    require(protocol["target_pr"] == result["target_pr"] == 279, "wrong target PR")
    require(len(protocol["rccd_components"]) == 5, "RCCD component set weakened")
    require(len(protocol["success_conditions"]) >= 6 and len(protocol["failure_conditions"]) >= 6, "reduction controls incomplete")
    require(result["terminal_outcome"] in protocol["terminal_outcomes"], "unregistered outcome")
    require(result["terminal_outcome"] == "rccd_irreducible_at_registered_level", "unexpected terminal result")
    require(len(corpus["candidates"]) >= 10, "candidate search too small")
    require(len(corpus["paired_distinction_tests"]) == 5, "paired distinctions incomplete")
    require(result["accepted_strictly_deeper_kernels"] == 0, "strict deeper kernel count inconsistent")
    require(result["candidate_count"] == len(corpus["candidates"]), "candidate count inconsistent")
    require(len(result["component_results"]) == 5, "component adjudication incomplete")
    require(queue["next_action"]["target_pr"] == 280, "queue did not advance to PR 280")
    require(queue["ordered_followups"] == [], "follow-up queue must contain only terminal action")
    require([x["target_pr"] for x in queue["completed_workstreams"]] == [276, 277, 278, 279], "completed sequence incorrect")
    require(live_queue["status"] == "complete", "live queue did not close")
    require(live_queue["next_action"] is None and live_queue["ordered_followups"] == [], "terminal queue malformed")
    prose = DOC.read_text(encoding="utf-8") + AUDIT.read_text(encoding="utf-8")
    for phrase in ("rccd_irreducible_at_registered_level", "not proof of metaphysical fundamentality", "queue advances exactly once"):
        require(phrase in prose, f"missing boundary phrase: {phrase}")
    print("PASS: TUE-W3 deeper-kernel adjudication is complete and bounded")


if __name__ == "__main__":
    main()
