#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL = ROOT / "theory" / "irreducibility" / "upp_irreducibility_maximality_v1.py"
SPEC = ROOT / "theory" / "irreducibility" / "upp-irreducibility-maximality-v1.0.json"
RESULT = ROOT / "theory" / "evaluation" / "upp-w14-irreducibility-maximality-result-v1.0.json"
QUEUE = ROOT / "theory" / "evaluation" / "post-tue-universal-proof-queue-checkpoint-v1.0.json"
DOC = ROOT / "docs" / "research" / "upp-w14-maximality-v1.0.md"
AUDIT = ROOT / "docs" / "audits" / "upp-w14-maximality-audit.md"
EXPECTED = "relative_rccd_maximality_established_under_frozen_extension_rules_with_registered_countermodel_closure_and_open_world_boundary"
NEXT = {"target_pr": 296, "workstream": "UPP-W15-TERMINAL-THEOREM"}

def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")

def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_model():
    spec = importlib.util.spec_from_file_location("upp_w14_checker", MODEL)
    if spec is None or spec.loader is None:
        fail("cannot load model")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def main() -> int:
    for path in (MODEL, SPEC, RESULT, QUEUE, DOC, AUDIT):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")
    model = load_model()
    specification, result, queue = map(load_json, (SPEC, RESULT, QUEUE))
    if specification.get("workstream") != "UPP-W14-MAXIMALITY" or specification.get("target_pr") != 295:
        fail("registered workstream mismatch")
    if specification.get("terminal_result") != EXPECTED or result.get("terminal_result") != EXPECTED:
        fail("terminal result mismatch")
    ledger = model.canonical_ledger()
    if model.validate_ledger(ledger):
        fail("canonical search ledger is incomplete")
    if model.maximality_verdict(ledger) is not model.Verdict.PROVED:
        fail("canonical maximality assessment does not prove")
    if specification.get("next_workstream") != NEXT or result.get("next_workstream") != NEXT:
        fail("terminal theorem successor mismatch")
    entry = next((x for x in queue.get("completed_workstreams", []) if x.get("target_pr") == 295), None)
    if entry is None or entry.get("workstream") != "UPP-W14-MAXIMALITY" or entry.get("result") != EXPECTED:
        fail("queue omits PR #295 completion")
    if queue.get("next_action") != NEXT or queue.get("ordered_followups") != []:
        fail("queue does not advance exactly to PR #296")
    if any(x.get("public_evaluation_authorized") is not False for x in (specification, result, queue)):
        fail("public evaluation gate opened early")
    text = DOC.read_text(encoding="utf-8").lower() + AUDIT.read_text(encoding="utf-8").lower()
    for phrase in ("frozen extension", "open-world", "unknown", "absence of counterexample"):
        if phrase not in text:
            fail(f"documentation omits {phrase}")
    test = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_w14_irreducibility_maximality.py"], cwd=ROOT)
    if test.returncode:
        fail("maximality tests failed")
    print("PASS: UPP-W14 maximality package is internally consistent")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
