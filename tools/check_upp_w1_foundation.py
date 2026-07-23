from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory/foundation/upp-foundation-v1.0.json"
RESULT = ROOT / "theory/evaluation/upp-w1-foundation-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
MODEL = ROOT / "theory/foundation/upp_foundation_v1.py"

REQUIRED_SORTS = {
    "Identifier", "TimeIndex", "Commitment", "State", "Transition",
    "Dependency", "HistoryEvent", "ReasoningFact", "Observation",
    "RecoveryWitness", "ReasoningSystem",
}
REQUIRED_PRIMITIVES = {
    "identifier", "time_index", "commitment", "state", "transition",
    "dependency", "history_event", "reasoning_fact", "observation",
    "recovery_witness", "reasoning_system",
}
REQUIRED_SEPARATIONS = {
    "object identity is distinct from content equality",
    "state is distinct from observation of state",
    "transition occurrence is distinct from transition admissibility",
    "dependency is distinct from mere temporal succession",
    "history event is distinct from an enlarged present-state encoding",
    "representation is distinct from recovery procedure",
    "recovery failure is distinct from evidential unknown",
    "normative classification is distinct from empirical occurrence",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def load_model():
    spec = importlib.util.spec_from_file_location("upp_foundation_v1", MODEL)
    if spec is None or spec.loader is None:
        fail("cannot import foundation model")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    foundation = load_json(SPEC)
    result = load_json(RESULT)
    queue = load_json(QUEUE)
    module = load_model()

    if foundation.get("workstream") != "UPP-W1-FOUNDATION":
        fail("wrong foundation workstream")
    if foundation.get("result") != "typed_foundation_established_without_rccd_entailment":
        fail("unexpected foundation result")
    sorts = {entry["id"] for entry in foundation.get("sorts", [])}
    if sorts != REQUIRED_SORTS:
        fail(f"foundation sorts differ: missing={sorted(REQUIRED_SORTS - sorts)} extra={sorted(sorts - REQUIRED_SORTS)}")
    if set(foundation.get("semantic_separations", [])) != REQUIRED_SEPARATIONS:
        fail("semantic separations are incomplete or changed")
    neutrality = foundation.get("foundation_neutrality", {})
    forbidden_true = [key for key, value in neutrality.items() if key.endswith(("_defined", "_proved", "_asserted")) and value is True]
    if forbidden_true:
        fail(f"foundation improperly asserts downstream result: {forbidden_true}")
    if len(foundation.get("prohibited_inferences", [])) < 6:
        fail("anti-inflation controls are incomplete")
    if set(foundation.get("assumption_kinds", [])) != {x.value for x in module.AssumptionKind}:
        fail("assumption kinds disagree with executable model")
    if module.FOUNDATION_PRIMITIVES != frozenset(REQUIRED_PRIMITIVES):
        fail("executable primitive set disagrees with specification")
    if result.get("status") != "complete" or result.get("unknowns_promoted") is not False:
        fail("result status or Unknown discipline invalid")
    if result.get("public_evaluation_authorized") is not False:
        fail("release gate opened prematurely")

    completed = {(x.get("target_pr"), x.get("workstream"), x.get("result")) for x in queue.get("completed_workstreams", [])}
    required_completion = (282, "UPP-W1-FOUNDATION", "typed_foundation_established_without_rccd_entailment")
    if required_completion not in completed:
        fail("UPP-W1 is not preserved in completed queue history")
    next_action = queue.get("next_action")
    if next_action is not None and next_action.get("target_pr", 0) < 283:
        fail("queue regressed behind UPP-W2")
    if 282 in queue.get("ordered_followups", []):
        fail("completed UPP-W1 remains in ordered followups")
    if queue.get("public_evaluation_authorized") is not False:
        fail("queue release gate opened prematurely")

    print("PASS: UPP-W1 foundation artifacts are complete, neutral, and preserved in monotonic queue history")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
