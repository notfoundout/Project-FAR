#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = ROOT / "theory/foundation/upp-semantic-interpretation-v1.0.json"
RESULT = ROOT / "theory/evaluation/upp-w10-semantic-interpretation-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
EXPECTED = "semantic_interpretation_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"


def main() -> int:
    spec = json.loads(SPEC.read_text())
    result = json.loads(RESULT.read_text())
    queue = json.loads(QUEUE.read_text())
    assert spec["target_pr"] == 291 and spec["status"] == "complete"
    assert len(spec["antecedent_premises"]) == 7
    assert len(spec["witness_requirements"]) == 8
    assert len(spec["anti_trivialization"]) >= 8
    assert result["terminal_result"] == EXPECTED
    completed = {x["target_pr"]: x for x in queue["completed_workstreams"]}
    assert completed[291]["result"] == EXPECTED
    assert queue["next_action"] == {"target_pr": 292, "workstream": "UPP-W11-HISTORICAL-TRACE"}
    assert queue["public_evaluation_authorized"] is False
    run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_w10_semantic_interpretation.py"], cwd=ROOT)
    return run.returncode


if __name__ == "__main__": raise SystemExit(main())
