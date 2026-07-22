#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "theory/evaluation/post-usd-internal-discovery-continuation-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json"
RESEARCH = ROOT / "docs/research/post-usd-internal-discovery-continuation-v1.0.md"
AUDIT = ROOT / "docs/audits/post-usd-internal-discovery-continuation-audit.md"
EVC = ROOT / "theory/evaluation/post-w5-usd-next-program-v1.0.json"
W1_FREEZE = ROOT / "theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json"
W2_RESULT = ROOT / "theory/evaluation/ikd-w2-expanded-candidate-competition-v1.0.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (PROGRAM, QUEUE, RESEARCH, AUDIT, EVC):
        assert path.is_file(), path
    program = load(PROGRAM)
    queue = load(QUEUE)
    evc = load(EVC)
    research = RESEARCH.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert program["program_id"] == "POST-USD-IKD-001"
    assert program["status"] == "registered_unexecuted"
    assert program["parent_synthesis"] == "POST-W5-USD-SYN-001"
    assert program["registration_pr"] == 260
    assert program["supersedes_as_active_program"] == "POST-USD-EVC-001"
    disposition = program["external_package_disposition"]
    assert disposition["EVC-W1-EXTERNAL-PROOF-REVIEW"] == "frozen_preserved_execution_deferred"
    assert disposition["EVC-W2-R3-TECHNICAL-REPLICATION"] == "frozen_preserved_execution_deferred"
    assert disposition["EVC-W3-R4-ADVERSARIAL-REPLICATION"] == "frozen_preserved_execution_deferred"
    assert "not withdrawn" in disposition["rule"]

    streams = program["workstreams"]
    assert len(streams) == 9
    assert [item["sequence"] for item in streams] == list(range(1, 10))
    assert [item["target_pr"] for item in streams] == list(range(261, 270))
    outcomes = set(program["terminal_outcomes"])
    assert "one_nontrivial_common_kernel" in outcomes
    assert "bounded_no_single_kernel" in outcomes
    rules = "\n".join(program["decision_rules"])
    assert "Cross-feature conjunctions" in rules
    assert "Equivalent reintroduction" in rules
    assert "External validation remains deferred" in rules

    assert queue["queue_id"] == "POST-USD-IKD-QUEUE-001"
    assert queue["parent_program"] == program["program_id"]
    next_pr = queue["next_action"]["target_pr"]
    assert next_pr in {261, 262, 263}
    if next_pr >= 262:
        assert W1_FREEZE.is_file()
        assert queue["completed_workstreams"][0]["target_pr"] == 261
    if next_pr == 263:
        assert W2_RESULT.is_file()
        result = load(W2_RESULT)
        assert result["status"] == "complete_bounded_comparison"
        assert result["next_decisive_workstream"] == "IKD-W3-COMMON-FACTOR"
        assert queue["next_action"]["workstream"] == "IKD-W3-COMMON-FACTOR"
        assert queue["completed_workstreams"][1]["target_pr"] == 262
        assert [item["target_pr"] for item in queue["ordered_followups"]] == list(range(264, 270))
    assert "release EVC-W1 external review package" in queue["blocked_actions"]
    assert evc["status"] == "registered_unexecuted"
    assert "External-package hold" in research
    assert "Separate featurewise success is not treated as compositional closure" in audit
    print(f"POST-USD internal discovery continuation: PASS (external execution deferred; PR #{next_pr} authorized)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
