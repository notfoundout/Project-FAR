#!/usr/bin/env python3
"""Validate Project FAR's prospective anti-self-validation research gates."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/research-gates.json"
ALLOWED_STATUS = {"not_satisfied", "in_progress", "satisfied", "blocked", "retired"}
REQUIRED_GATE_NAMES = {
    "external-observation-contract",
    "negative-controls",
    "full-cost-accounting",
    "anti-reintroduction-ablation",
    "independent-replication",
    "private-holdout-counterexample-challenge",
    "nonclaim-audit",
}
REQUIRED_POLICY_TRUE = {
    "unsatisfied_gate_blocks_stronger_claim",
    "unknown_is_not_pass",
    "internal_multi_implementation_is_not_external_independence",
    "theory_change_after_freeze_creates_new_version",
    "failed_frozen_results_are_immutable",
    "tradeoffs_must_not_be_reported_as_wins",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    if not REGISTRY.is_file():
        print(f"FAIL: missing research gate registry: {REGISTRY.relative_to(ROOT)}")
        return 1

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read research gate registry: {exc}")
        return 1

    if data.get("schema_version") != "1.0":
        fail("schema_version must equal 1.0", errors)

    artifacts = data.get("required_canonical_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        fail("required_canonical_artifacts must be a non-empty list", errors)
    else:
        for relative in artifacts:
            if not isinstance(relative, str) or not relative.strip():
                fail("canonical artifact paths must be non-empty strings", errors)
                continue
            if not (ROOT / relative).is_file():
                fail(f"missing canonical artifact: {relative}", errors)

    gates = data.get("gates")
    if not isinstance(gates, list):
        fail("gates must be a list", errors)
        gates = []

    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    for gate in gates:
        if not isinstance(gate, dict):
            fail("every gate must be an object", errors)
            continue
        gate_id = gate.get("id")
        name = gate.get("name")
        status = gate.get("status")
        required_before = gate.get("required_before")

        if not isinstance(gate_id, str) or not gate_id:
            fail("every gate requires a non-empty id", errors)
        elif gate_id in seen_ids:
            fail(f"duplicate gate id: {gate_id}", errors)
        else:
            seen_ids.add(gate_id)

        if not isinstance(name, str) or not name:
            fail(f"gate {gate_id or '<unknown>'} requires a non-empty name", errors)
        elif name in seen_names:
            fail(f"duplicate gate name: {name}", errors)
        else:
            seen_names.add(name)

        if status not in ALLOWED_STATUS:
            fail(f"gate {gate_id or '<unknown>'} has invalid status: {status!r}", errors)

        if not isinstance(required_before, list) or not required_before:
            fail(f"gate {gate_id or '<unknown>'} requires a non-empty required_before list", errors)

    missing_names = REQUIRED_GATE_NAMES - seen_names
    if missing_names:
        fail("missing required gates: " + ", ".join(sorted(missing_names)), errors)

    policy = data.get("claim_policy")
    if not isinstance(policy, dict):
        fail("claim_policy must be an object", errors)
    else:
        for key in sorted(REQUIRED_POLICY_TRUE):
            if policy.get(key) is not True:
                fail(f"claim_policy.{key} must be true", errors)

    authorized = data.get("current_authorized_work")
    paused = data.get("paused_by_default")
    if not isinstance(authorized, list) or not authorized:
        fail("current_authorized_work must be a non-empty list", errors)
    if not isinstance(paused, list) or not paused:
        fail("paused_by_default must be a non-empty list", errors)

    overlap = set(authorized or []) & set(paused or [])
    if overlap:
        fail("work cannot be both authorized and paused: " + ", ".join(sorted(overlap)), errors)

    if errors:
        print("Research gate validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Research gate validation PASS ({len(gates)} gates, {len(artifacts)} canonical artifacts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
