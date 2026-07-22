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
    assert streams[0]["id"] == "IKD-W1-CANDIDATE-ARCHITECTURES"
    assert len(streams[0]["minimum_families"]) >= 6
    assert streams[-1]["id"] == "IKD-W9-TERMINAL-ADJUDICATION"

    outcomes = set(program["terminal_outcomes"])
    assert outcomes == {
        "one_nontrivial_common_kernel",
        "multiple_translation_equivalent_kernels",
        "multiple_incomparable_kernels_no_deeper_factor_within_search",
        "generic_structured_system_properties_only",
        "bounded_no_single_kernel",
        "unresolved",
    }

    rules = "\n".join(program["decision_rules"])
    assert "derived from accepted dependencies" in rules
    assert "Cross-feature conjunctions" in rules
    assert "Equivalent reintroduction" in rules
    assert "not global proof of nonexistence" in rules
    assert "External validation remains deferred" in rules

    gate = program["release_condition_for_external_packages"]
    assert gate["required_terminal_artifact"] == "IKD-W9-TERMINAL-ADJUDICATION"
    assert set(gate["allowed_internal_statuses"]) == outcomes

    assert queue["queue_id"] == "POST-USD-IKD-QUEUE-001"
    assert queue["parent_program"] == program["program_id"]
    assert queue["registration_pr"] == 260
    assert queue["next_action"]["target_pr"] == 261
    assert queue["next_action"]["workstream"] == "IKD-W1-CANDIDATE-ARCHITECTURES"
    assert [item["target_pr"] for item in queue["ordered_followups"]] == list(range(262, 270))
    assert "release EVC-W1 external review package" in queue["blocked_actions"]

    assert evc["program_id"] == "POST-USD-EVC-001"
    assert evc["status"] == "registered_unexecuted"
    assert "External-package hold" in research
    assert "PR #261 must freeze" in research
    assert "Separate featurewise success is not treated as compositional closure" in audit
    assert "Failure to find a common factor is not global proof of nonexistence" in audit
    assert "internal_discovery_continuation_registered_external_execution_deferred" in audit

    print("POST-USD internal discovery continuation: PASS (external execution deferred; PR #261 authorized)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
