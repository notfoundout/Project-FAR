#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory/equivalence/upp-representation-equivalence-v1.0.json"
MODEL = ROOT / "theory/equivalence/upp_representation_equivalence_v1.py"
RESULT = ROOT / "theory/evaluation/upp-w6-equivalence-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
AUDIT = ROOT / "docs/research/upp-w6-equivalence-audit.md"
TEST = ROOT / "tests/test_upp_w6_equivalence.py"
TERMINAL = "bidirectional_commitment_equivalence_frozen_with_anti_collapse_and_unknown_boundary"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"UPP-W6 CHECK FAILED: {message}")


def load(path: Path) -> dict:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (SPEC, MODEL, RESULT, QUEUE, AUDIT, TEST):
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")

    spec = load(SPEC)
    result = load(RESULT)
    queue = load(QUEUE)

    require(spec["program_id"] == "POST-TUE-UPP-001", "wrong program id")
    require(spec["workstream"] == "UPP-W6-EQUIVALENCE", "wrong workstream")
    require(spec["target_pr"] == 287, "wrong target PR")
    require(set(spec["verdicts"]) == {"equivalent", "non_equivalent", "unknown"}, "wrong verdict set")
    require(len(spec["required_dimensions"]) == 10, "all ten dimensions must be registered")
    require(len(set(spec["required_dimensions"])) == 10, "duplicate dimensions")
    require(all(spec["positive_equivalence_conditions"].values()), "positive conditions must remain enabled")
    require(len(spec["anti_collapse_rules"]) >= 8, "anti-collapse boundary weakened")
    require(spec["next_action"] == {"target_pr": 288, "workstream": "UPP-W7-RECOVERABLE-COMMITMENT"}, "wrong next action")

    require(result["terminal_result"] == TERMINAL, "terminal result mismatch")
    require(result["public_evaluation_authorized"] is False, "public evaluation gate opened")
    require("RCCD necessity" in result["not_established"], "necessity nonclaim missing")
    require("the terminal universal theorem" in result["not_established"], "universal-theorem nonclaim missing")

    completed = queue["completed_workstreams"]
    require(completed[-1] == {"target_pr": 287, "workstream": "UPP-W6-EQUIVALENCE", "result": TERMINAL}, "queue completion mismatch")
    require([x["target_pr"] for x in completed] == list(range(281, 288)), "completed PR history is not contiguous")
    require(queue["next_action"] == {"target_pr": 288, "workstream": "UPP-W7-RECOVERABLE-COMMITMENT"}, "queue not advanced")
    require(queue["ordered_followups"] == list(range(289, 297)), "followup ordering mismatch")
    require(queue["public_evaluation_authorized"] is False, "public evaluation gate opened in queue")

    audit = AUDIT.read_text(encoding="utf-8")
    for phrase in ("Anti-collapse boundary", "Three-valued adjudication", TERMINAL, "Public evaluation remains unauthorized"):
        require(phrase in audit, f"audit missing {phrase!r}")

    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_w6_equivalence.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise SystemExit("UPP-W6 CHECK FAILED: adversarial tests failed")

    print("UPP-W6 CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
