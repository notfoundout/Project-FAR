#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory/foundation/upp-dependency-structure-v1.0.json"
RESULT = ROOT / "theory/evaluation/upp-w9-dependency-structure-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
EXPECTED = "dependency_structure_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    spec = json.loads(SPEC.read_text())
    result = json.loads(RESULT.read_text())
    queue = json.loads(QUEUE.read_text())
    require(spec["target_pr"] == 290, "wrong target PR")
    require(spec["status"] == "complete", "workstream not complete")
    require(spec["terminal_result"] == EXPECTED, "wrong terminal result")
    require(set(spec["dependency_kinds"]) == {"support", "defeat", "revision", "replacement", "admissibility", "provenance"}, "dependency kinds drifted")
    require(len(spec["antecedents"]) == 7, "antecedent set drifted")
    require(len(spec["countermodels"]) >= 7, "countermodel coverage weakened")
    require(result["terminal_result"] == EXPECTED, "result mismatch")
    completed = {(x["target_pr"], x["workstream"], x["result"]) for x in queue["completed_workstreams"]}
    require((290, "UPP-W9-DEPENDENCY-STRUCTURE", EXPECTED) in completed, "queue lacks completed W9")
    require(queue["next_action"] == {"target_pr": 291, "workstream": "UPP-W10-SEMANTIC-INTERPRETATION"}, "queue did not advance exactly")
    require(queue["public_evaluation_authorized"] is False, "public evaluation gate opened")
    proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_dependency_structure.py"], cwd=ROOT)
    require(proc.returncode == 0, "dependency tests failed")
    print("UPP-W9 dependency-structure validation passed")


if __name__ == "__main__":
    main()
