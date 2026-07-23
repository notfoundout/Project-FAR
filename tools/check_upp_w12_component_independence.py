#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory" / "independence" / "upp-component-independence-v1.0.json"
RESULT = ROOT / "theory" / "evaluation" / "upp-w12-component-independence-result-v1.0.json"
QUEUE = ROOT / "theory" / "evaluation" / "post-tue-universal-proof-queue-checkpoint-v1.0.json"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    spec = json.loads(SPEC.read_text())
    result = json.loads(RESULT.read_text())
    queue = json.loads(QUEUE.read_text())
    expected = "five_component_relative_independence_established_by_separating_witnesses_and_anti_reduction_controls"
    if spec.get("target_pr") != 293 or spec.get("result") != expected:
        fail("registered theorem identity or result mismatch")
    components = spec.get("components", [])
    if len(components) != 5 or len(set(components)) != 5:
        fail("exactly five unique components are required")
    witnesses = spec.get("separating_witnesses", [])
    if {w.get("target") for w in witnesses} != set(components):
        fail("every component requires one separating witness")
    if not all(w.get("other_four_preserved") is True and w.get("lost") for w in witnesses):
        fail("separating witnesses must preserve the other four and lose a distinctive obligation")
    if result.get("terminal_result") != expected or result.get("status") != "complete":
        fail("result artifact mismatch")
    completed = {x.get("target_pr"): x for x in queue.get("completed_workstreams", [])}
    if completed.get(293, {}).get("result") != expected:
        fail("queue does not record PR #293 historical completion")
    terminal_complete = 296 in completed
    if terminal_complete:
        if queue.get("status") != "complete" or queue.get("next_action") is not None or queue.get("ordered_followups") != []:
            fail("terminal queue closure malformed")
    else:
        next_action = queue.get("next_action", {})
        target = next_action.get("target_pr")
        if not isinstance(target, int) or target < 294:
            fail("queue regressed before PR #294")
        followups = queue.get("ordered_followups", [])
        if any(not isinstance(item, int) or item <= target for item in followups):
            fail("ordered followups are not monotonic")
        if queue.get("public_evaluation_authorized") is not False:
            fail("public evaluation gate opened before terminal completion")
    test = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_w12_component_independence.py"], cwd=ROOT, text=True, capture_output=True)
    if test.returncode:
        sys.stderr.write(test.stdout + test.stderr)
        fail("component independence tests failed")
    print("PASS: UPP-W12 component independence artifacts are internally consistent")


if __name__ == "__main__":
    main()
