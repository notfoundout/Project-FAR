#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory/necessity/upp-w8-constrained-evolution-v1.0.json"
MODEL = ROOT / "theory/necessity/upp_w8_constrained_evolution_v1.py"
RESULT = ROOT / "theory/evaluation/upp-w8-constrained-evolution-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
AUDIT = ROOT / "docs/research/upp-w8-constrained-evolution-audit.md"
TEST = ROOT / "tests/test_upp_w8_constrained_evolution.py"
TERMINAL = "constrained_evolution_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"UPP-W8 CHECK FAILED: {message}")


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
    require(spec["workstream"] == "UPP-W8-CONSTRAINED-EVOLUTION", "wrong workstream")
    require(spec["target_pr"] == 289, "wrong target PR")
    require(set(spec["verdicts"]) == {"proved", "refuted", "unknown"}, "wrong verdict set")
    require(len(spec["antecedent_premises"]) == 6, "premise set weakened")
    require(len(spec["witness_obligations"]) == 8, "witness obligations weakened")
    require(len(spec["anti_trivialization_rules"]) >= 8, "anti-trivialization boundary weakened")
    require(len(spec["separating_countermodels"]) >= 7, "countermodel coverage weakened")
    require(spec["next_action"] == {"target_pr": 290, "workstream": "UPP-W9-DEPENDENCY-STRUCTURE"}, "wrong next action")
    require(spec["public_evaluation_authorized"] is False, "public evaluation gate opened")

    require(result["terminal_result"] == TERMINAL, "terminal result mismatch")
    require(result["theorem_status"] == "proved_relative_to_registered_premises", "theorem status mismatch")
    require("the terminal universal theorem" in result["not_established"], "universal-theorem nonclaim missing")
    require(result["public_evaluation_authorized"] is False, "result opened public evaluation")

    completed = queue["completed_workstreams"]
    require(completed[-1] == {"target_pr": 289, "workstream": "UPP-W8-CONSTRAINED-EVOLUTION", "result": TERMINAL}, "queue completion mismatch")
    require([x["target_pr"] for x in completed] == list(range(281, 290)), "completed PR history is not contiguous")
    require(queue["next_action"] == {"target_pr": 290, "workstream": "UPP-W9-DEPENDENCY-STRUCTURE"}, "queue not advanced")
    require(queue["ordered_followups"] == list(range(291, 297)), "followup ordering mismatch")
    require(queue["public_evaluation_authorized"] is False, "queue opened public evaluation")

    audit = AUDIT.read_text(encoding="utf-8")
    for phrase in ("Theorem witness", "Contradiction structure", "Separating countermodels", TERMINAL, "Public evaluation remains unauthorized"):
        require(phrase in audit, f"audit missing {phrase!r}")

    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_w8_constrained_evolution.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise SystemExit("UPP-W8 CHECK FAILED: adversarial tests failed")

    print("UPP-W8 CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
