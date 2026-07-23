from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "theory/evaluation/tue-w2-defeating-condition-campaign-protocol-v1.0.json"
CORPUS = ROOT / "theory/evaluation/tue-w2-defeating-condition-campaign-corpus-v1.0.json"
RESULT = ROOT / "theory/evaluation/tue-w2-defeating-condition-campaign-result-v1.0.json"
DOC = ROOT / "docs/research/tue-w2-defeating-condition-campaign-v1.0.md"
AUDIT = ROOT / "docs/audits/tue-w2-defeating-condition-campaign-audit.md"
QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (PROTOCOL, CORPUS, RESULT, DOC, AUDIT, QUEUE):
        require(path.exists(), f"missing artifact: {path.relative_to(ROOT)}")
    protocol, corpus, result, queue = map(load, (PROTOCOL, CORPUS, RESULT, QUEUE))
    require(protocol["campaign_id"] == "TUE-W2-DEFEATING-CONDITION-CAMPAIGN-001", "wrong campaign")
    conditions = [item["id"] for item in protocol["frozen_conditions"]]
    require(conditions == ["DC-1-SIXTH-PRIMITIVE", "DC-2-RCCD-ESCAPE", "DC-3-CIRCULARITY", "DC-4-PLURAL-KERNEL", "DC-5-ABLATION"], "five conditions changed")
    require("A single established defeating condition changes the campaign outcome regardless of the other four results." in protocol["evidence_rules"], "weakest-gate override missing")
    cases = corpus["cases"]
    require(len(cases) >= 20, "attack corpus too small")
    require(set(item["condition"] for item in cases) == set(conditions), "not all conditions attacked")
    require(all(item["disposition"] in set(protocol["dispositions"]) for item in cases), "invalid disposition")
    require(any(item["disposition"] == "unresolved" for item in cases), "Unknown boundary was erased")
    require(result["terminal_outcome"] == "no_defeating_condition_established", "unexpected result")
    require(len(result["condition_results"]) == 5, "five condition results required")
    require(all(item["result"] == "not_established" for item in result["condition_results"]), "condition result conflicts with terminal outcome")
    checkpoint = result["historical_queue_checkpoint"]
    require(checkpoint == {"completed_workstreams":[276,277,278],"next_pr":279,"next_workstream":"TUE-W3-DEEPER-KERNEL","ordered_followups":[280]}, "W2 historical queue checkpoint changed")
    completed = [item["target_pr"] for item in queue["completed_workstreams"]]
    require(completed[:3] == checkpoint["completed_workstreams"], "live queue lost W2 history")
    if queue["status"] == "complete":
        require(queue["next_action"] is None and queue["ordered_followups"] == [], "terminal queue closure malformed")
    else:
        require(queue["next_action"]["target_pr"] in (279, 280), "live queue escaped authorized sequence")
        require(queue["next_action"]["workstream"] in ("TUE-W3-DEEPER-KERNEL", "TUE-W4-FINAL-QUESTION-ANSWER"), "unauthorized workstream")
    prose = DOC.read_text(encoding="utf-8") + AUDIT.read_text(encoding="utf-8")
    for token in ("Unknown", "not established", "PR #279", "External review"):
        require(token in prose, f"missing prose control: {token}")
    print("PASS: TUE-W2 attacks all five defeating conditions without erasing Unknowns or inflating scope")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
