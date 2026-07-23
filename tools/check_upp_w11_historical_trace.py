#!/usr/bin/env python3
"""Deterministic consistency checker for UPP-W11-HISTORICAL-TRACE."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "theory" / "history" / "upp_historical_trace_v1.py"
SPEC_PATH = ROOT / "theory" / "history" / "upp-historical-trace-v1.0.json"
RESULT_PATH = ROOT / "theory" / "evaluation" / "upp-w11-historical-trace-result-v1.0.json"
QUEUE_PATH = ROOT / "theory" / "evaluation" / "post-tue-universal-proof-queue-checkpoint-v1.0.json"
DOC_PATH = ROOT / "docs" / "research" / "upp-w11-historical-trace-v1.0.md"
AUDIT_PATH = ROOT / "docs" / "audits" / "upp-w11-historical-trace-audit.md"

EXPECTED_RESULT = "historical_trace_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"
EXPECTED_NEXT = {"target_pr": 293, "workstream": "UPP-W12-COMPONENT-INDEPENDENCE"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def load_model():
    spec = importlib.util.spec_from_file_location("upp_historical_trace_v1_checker", MODEL_PATH)
    if spec is None or spec.loader is None:
        fail("cannot construct model loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    for path in (MODEL_PATH, SPEC_PATH, RESULT_PATH, QUEUE_PATH, DOC_PATH, AUDIT_PATH):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    model = load_model()
    specification = load_json(SPEC_PATH)
    result = load_json(RESULT_PATH)
    queue = load_json(QUEUE_PATH)

    if specification.get("program_id") != "POST-TUE-UPP-001":
        fail("wrong program id")
    if specification.get("workstream") != "UPP-W11-HISTORICAL-TRACE":
        fail("wrong workstream")
    if specification.get("target_pr") != 292:
        fail("wrong target PR")
    if specification.get("terminal_result") != EXPECTED_RESULT:
        fail("specification terminal result mismatch")
    if result.get("terminal_result") != EXPECTED_RESULT:
        fail("result artifact terminal result mismatch")
    if specification.get("next_workstream") != EXPECTED_NEXT:
        fail("specification next workstream mismatch")
    if result.get("next_workstream") != EXPECTED_NEXT:
        fail("result next workstream mismatch")
    if specification.get("public_evaluation_authorized") is not False:
        fail("specification improperly opens public evaluation")
    if result.get("public_evaluation_authorized") is not False:
        fail("result improperly opens public evaluation")

    antecedents = tuple(specification.get("antecedents", ()))
    obligations = tuple(specification.get("witness_obligations", ()))
    anti = tuple(specification.get("anti_trivialization", ()))
    if antecedents != tuple(model.FROZEN_ANTECEDENT_IDS):
        fail("antecedent registry differs from executable model")
    if obligations != tuple(model.FROZEN_WITNESS_OBLIGATION_IDS):
        fail("witness obligation registry differs from executable model")
    if anti != tuple(model.ANTI_TRIVIALIZATION_CASES):
        fail("anti-trivialization registry differs from executable model")

    completed = queue.get("completed_workstreams", [])
    entry = next((item for item in completed if item.get("target_pr") == 292), None)
    if entry is None:
        fail("queue does not record PR #292 completion")
    if entry.get("workstream") != "UPP-W11-HISTORICAL-TRACE":
        fail("queue records wrong PR #292 workstream")
    if entry.get("result") != EXPECTED_RESULT:
        fail("queue records wrong PR #292 result")

    next_action = queue.get("next_action", {})
    next_pr = next_action.get("target_pr")
    if not isinstance(next_pr, int) or next_pr < EXPECTED_NEXT["target_pr"]:
        fail("queue regresses before PR #293")
    followups = queue.get("ordered_followups", [])
    completed_prs = {item.get("target_pr") for item in completed}
    if any(pr in completed_prs for pr in followups):
        fail("queue leaves completed PRs in ordered followups")
    if any(not isinstance(pr, int) or pr <= next_pr for pr in followups):
        fail("queue followups are not strictly after next action")
    if followups != sorted(set(followups)):
        fail("queue followups are not unique and ordered")
    if queue.get("public_evaluation_authorized") is not False:
        fail("queue improperly opens public evaluation")

    if "final snapshot" not in DOC_PATH.read_text(encoding="utf-8").lower():
        fail("research note omits snapshot countermodel")
    if "three-valued" not in AUDIT_PATH.read_text(encoding="utf-8").lower():
        fail("audit omits three-valued discipline")

    print("PASS: UPP-W11 historical-trace package is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
