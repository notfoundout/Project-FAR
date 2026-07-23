#!/usr/bin/env python3
"""Deterministic checker for UPP-W13-SUFFICIENCY-CONSTRUCTION."""
from __future__ import annotations
import importlib.util
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL = ROOT / "theory" / "sufficiency" / "upp_sufficiency_construction_v1.py"
SPEC = ROOT / "theory" / "sufficiency" / "upp-sufficiency-construction-v1.0.json"
RESULT = ROOT / "theory" / "evaluation" / "upp-w13-sufficiency-construction-result-v1.0.json"
QUEUE = ROOT / "theory" / "evaluation" / "post-tue-universal-proof-queue-checkpoint-v1.0.json"
DOC = ROOT / "docs" / "research" / "upp-w13-sufficiency-construction-v1.0.md"
AUDIT = ROOT / "docs" / "audits" / "upp-w13-sufficiency-construction-audit.md"
EXPECTED = "relative_rccd_sufficiency_established_by_effective_compositional_construction_and_bidirectional_reconstruction"
NEXT = {"target_pr": 295, "workstream": "UPP-W14-MAXIMALITY"}

def fail(message: str) -> None:
    print("FAIL:", message)
    raise SystemExit(1)

def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")

def load_model():
    spec = importlib.util.spec_from_file_location("upp_sufficiency_construction_v1_checker", MODEL)
    if spec is None or spec.loader is None:
        fail("cannot load executable model")
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
    if specification.get("program_id") != "POST-TUE-UPP-001" or specification.get("workstream") != "UPP-W13-SUFFICIENCY-CONSTRUCTION":
        fail("wrong program or workstream")
    if specification.get("target_pr") != 294:
        fail("wrong target PR")
    if specification.get("terminal_result") != EXPECTED or result.get("terminal_result") != EXPECTED:
        fail("terminal result mismatch")
    if specification.get("next_workstream") != NEXT or result.get("next_workstream") != NEXT:
        fail("next workstream mismatch")
    if tuple(specification.get("components", ())) != tuple(model.COMPONENTS):
        fail("component registry differs from model")
    if tuple(specification.get("anti_trivialization", ())) != tuple(model.ANTI_TRIVIALIZATION_CASES):
        fail("anti-trivialization registry differs from model")
    if model.assess(model.canonical_package()).verdict is not model.Verdict.PROVED:
        fail("canonical construction does not prove")
    completed = queue.get("completed_workstreams", [])
    entry = next((item for item in completed if item.get("target_pr") == 294), None)
    if entry is None or entry.get("workstream") != "UPP-W13-SUFFICIENCY-CONSTRUCTION" or entry.get("result") != EXPECTED:
        fail("queue does not preserve PR #294 completion")
    next_action = queue.get("next_action", {})
    if not isinstance(next_action.get("target_pr"), int) or next_action["target_pr"] < 295:
        fail("queue regressed before PR #295")
    followups = queue.get("ordered_followups", [])
    if any(not isinstance(item, int) or item <= next_action["target_pr"] for item in followups):
        fail("queue followups are not monotonic")
    if any(item.get("public_evaluation_authorized") is not False for item in (specification, result, queue)):
        fail("public evaluation gate opened")
    if "round-trip" not in DOC.read_text(encoding="utf-8").lower():
        fail("research note omits round-trip construction")
    if "three-valued" not in AUDIT.read_text(encoding="utf-8").lower():
        fail("audit omits three-valued discipline")
    completed_test = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_upp_w13_sufficiency_construction.py"], cwd=ROOT)
    if completed_test.returncode:
        fail("adversarial test suite failed")
    print("PASS: UPP-W13 sufficiency construction package is internally consistent")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
