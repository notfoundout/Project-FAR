#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory/necessity/upp-recoverable-commitment-v1.0.json"
MODEL = ROOT / "theory/necessity/upp_recoverable_commitment_v1.py"
RESULT = ROOT / "theory/evaluation/upp-w7-recoverable-commitment-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
AUDIT = ROOT / "docs/research/upp-w7-recoverable-commitment-audit.md"
TEST = ROOT / "tests/test_upp_w7_recoverable_commitment.py"
TERMINAL = "recoverable_commitment_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"UPP-W7 CHECK FAILED: {message}")


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
    require(spec["workstream"] == "UPP-W7-RECOVERABLE-COMMITMENT", "wrong workstream")
    require(spec["target_pr"] == 288, "wrong target PR")
    require(len(spec["premises"]) == 5, "five frozen premises required")
    require(len(spec["witness_obligations"]) == 4, "four witness obligations required")
    require(len(spec["separating_countermodels"]) >= 6, "countermodel campaign weakened")
    require(set(spec["verdicts"]) == {"proved", "refuted", "unknown"}, "wrong verdict set")
    require(result["terminal_result"] == TERMINAL, "terminal result mismatch")
    require(result["public_evaluation_authorized"] is False, "public gate opened")
    completed = queue["completed_workstreams"]
    require(completed[-1] == {"target_pr":288,"workstream":"UPP-W7-RECOVERABLE-COMMITMENT","result":TERMINAL}, "queue completion mismatch")
    require([x["target_pr"] for x in completed] == list(range(281, 289)), "completed history not contiguous")
    require(queue["next_action"] == {"target_pr":289,"workstream":"UPP-W8-CONSTRAINED-EVOLUTION"}, "queue not advanced")
    require(queue["ordered_followups"] == list(range(290, 297)), "followups wrong")
    audit = AUDIT.read_text(encoding="utf-8")
    for phrase in ("Witness construction", "Contradiction argument", "Three-valued adjudication", TERMINAL, "Public evaluation remains unauthorized"):
        require(phrase in audit, f"audit missing {phrase!r}")
    proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_w7_recoverable_commitment.py"], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        sys.stderr.write(proc.stdout + proc.stderr)
        raise SystemExit("UPP-W7 CHECK FAILED: adversarial tests failed")
    print("UPP-W7 CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
