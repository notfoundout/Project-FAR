#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory/machinery/upp-w5-machinery-closure-v1.0.json"
RESULT = ROOT / "theory/evaluation/upp-w5-machinery-closure-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
TEST = ROOT / "tests/test_upp_w5_machinery_closure.py"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    for path in (SPEC, RESULT, QUEUE, TEST):
        if not path.is_file():
            fail(f"missing required artifact: {path.relative_to(ROOT)}")
    spec = json.loads(SPEC.read_text())
    result = json.loads(RESULT.read_text())
    queue = json.loads(QUEUE.read_text())
    if spec["workstream"] != "UPP-W5-MACHINERY-CLOSURE":
        fail("wrong machinery closure workstream")
    if result["terminal_result"] != "transitive_machinery_closure_frozen_with_fixed_point_and_hidden_dependency_failure":
        fail("unexpected terminal result")
    if spec["public_evaluation_authorized"] or result["public_evaluation_authorized"]:
        fail("public evaluation gate opened prematurely")
    completed = {item["target_pr"]: item for item in queue["completed_workstreams"]}
    if completed.get(286, {}).get("result") != result["terminal_result"]:
        fail("queue does not preserve PR 286 result")
    if queue["next_action"] != {"target_pr": 287, "workstream": "UPP-W6-EQUIVALENCE"}:
        fail("queue did not advance exactly to PR 287")
    if queue["public_evaluation_authorized"]:
        fail("queue opened public evaluation")
    proc = subprocess.run([sys.executable, str(TEST)], cwd=ROOT)
    if proc.returncode:
        fail("machinery closure tests failed")
    print("UPP-W5 machinery closure artifacts verified")


if __name__ == "__main__":
    main()
