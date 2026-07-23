#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL = ROOT / "theory" / "terminal" / "upp_terminal_theorem_v1.py"
SPEC = ROOT / "theory" / "terminal" / "upp-terminal-theorem-v1.0.json"
RESULT = ROOT / "theory" / "evaluation" / "upp-w15-terminal-theorem-result-v1.0.json"
QUEUE = ROOT / "theory" / "evaluation" / "post-tue-universal-proof-queue-checkpoint-v1.0.json"
DISCLOSURE = ROOT / "docs" / "research" / "upp-w15-terminal-theorem-v1.0.md"
AUDIT = ROOT / "docs" / "audits" / "upp-w15-terminal-theorem-audit.md"
EXPECTED = "strictly_weakened_relative_rccd_universality_theorem_proved_with_complete_dependency_audit_and_open_world_boundary"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def load_model():
    spec = importlib.util.spec_from_file_location("upp_terminal_checker", MODEL)
    if spec is None or spec.loader is None:
        fail("cannot load model")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    for path in (MODEL, SPEC, RESULT, QUEUE, DISCLOSURE, AUDIT):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")
    model = load_model()
    specification, result, queue = map(load_json, (SPEC, RESULT, QUEUE))
    if specification.get("workstream") != "UPP-W15-TERMINAL-THEOREM" or specification.get("target_pr") != 296:
        fail("terminal identity mismatch")
    if specification.get("terminal_result") != EXPECTED or result.get("terminal_result") != EXPECTED:
        fail("terminal result mismatch")
    if specification.get("queue_closed") is not True or result.get("queue_closed") is not True:
        fail("terminal artifacts do not record queue closure")
    if result.get("release_gate_adjudicated") is not True:
        fail("result does not record release-gate adjudication")
    adjudication = model.adjudicate(model.canonical_evidence())
    if adjudication.outcome is not model.Outcome.WEAKENED or adjudication.verdict is not model.Verdict.PROVED:
        fail("canonical adjudication is not the registered weakened proof outcome")
    if result.get("outcome") != adjudication.outcome.value:
        fail("result outcome differs from executable adjudication")
    completed = {item.get("target_pr") for item in queue.get("completed_workstreams", [])}
    if set(range(281, 297)) - completed:
        fail("queue omits a completed UPP workstream")
    if queue.get("status") != "complete" or queue.get("next_action") is not None or queue.get("ordered_followups") != []:
        fail("terminal queue is not closed")
    if queue.get("public_evaluation_authorized") is not True:
        fail("terminal release gate not adjudicated")
    text = DISCLOSURE.read_text(encoding="utf-8").lower()
    for phrase in ("strictly weakened", "not kernel-checked", "open-world", "public evaluation"):
        if phrase not in text:
            fail(f"disclosure omits {phrase}")
    if "unknown" not in AUDIT.read_text(encoding="utf-8").lower():
        fail("audit omits Unknown discipline")
    test = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_w15_terminal_theorem.py"], cwd=ROOT)
    if test.returncode:
        fail("terminal theorem tests failed")
    print("PASS: UPP-W15 terminal theorem adjudication is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
