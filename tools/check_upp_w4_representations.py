from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory/representations/upp-representation-universe-v1.0.json"
RESULT = ROOT / "theory/evaluation/upp-w4-representations-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
MODEL = ROOT / "theory/representations/upp_representation_universe_v1.py"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("upp_representation_universe_v1", MODEL)
    if spec is None or spec.loader is None:
        fail("cannot import representation model")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    spec = load_json(SPEC)
    result = load_json(RESULT)
    queue = load_json(QUEUE)
    model = load_model()

    if spec.get("universe_id") != "E_STAR_V1" or len(spec.get("admissibility_criteria", [])) != 6:
        fail("representation universe identity or criterion count changed")
    statements = " ".join(x["statement"] for x in spec["admissibility_criteria"])
    if not model.text_is_kernel_neutral(statements):
        fail("kernel vocabulary leaked into E* criteria")
    if set(spec.get("included_encoding_families", [])) != {x.value for x in model.EncodingFamily}:
        fail("encoding-family coverage disagrees with executable model")
    if set(spec.get("support_kinds", [])) != {x.value for x in model.SupportKind}:
        fail("support inventory disagrees with executable model")

    good = model.RepresentationCandidate("good", model.EncodingFamily.SYMBOLIC, True, True, True, True, frozenset({model.SupportKind.DECODER}), True, True)
    bad = model.RepresentationCandidate("bad", model.EncodingFamily.GRAPH, True, True, False, True, frozenset(), True, True)
    unknown = model.RepresentationCandidate("unknown", model.EncodingFamily.LEARNED, True, True, True, None, frozenset(), True, True)
    if model.classify(good).value != "admissible" or model.classify(bad).value != "inadmissible" or model.classify(unknown).value != "unknown":
        fail("three-valued admissibility classifier is invalid")

    if result.get("rccd_necessity_proved") or result.get("machinery_closure_proved") or result.get("representation_equivalence_proved") or result.get("unknowns_promoted"):
        fail("downstream result inflated")
    completed = {x["target_pr"]: x for x in queue.get("completed_workstreams", [])}
    if completed.get(285, {}).get("result") != result.get("terminal_result"):
        fail("queue does not preserve completed PR 285 result")
    next_action = queue.get("next_action")
    if next_action is not None and next_action.get("target_pr", 0) < 286:
        fail("queue regressed before PR 286")
    if queue.get("public_evaluation_authorized"):
        fail("release gate opened")

    print("PASS: UPP-W4 E* is broad, effective, support-complete, neutral, and history-consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
