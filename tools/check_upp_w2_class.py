from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "theory/class/upp-target-class-v1.0.json"
RESULT = ROOT / "theory/evaluation/upp-w2-class-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json"
MODEL = ROOT / "theory/class/upp_target_class_v1.py"


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("upp_target_class_v1", MODEL)
    if spec is None or spec.loader is None:
        fail("cannot import class model")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    spec = load_json(SPEC)
    result = load_json(RESULT)
    queue = load_json(QUEUE)
    model = load_model()
    statements = " ".join(x["statement"] for x in spec["membership_criteria"])
    if len(spec["membership_criteria"]) != 5:
        fail("membership criteria count changed")
    if not model.criterion_text_is_rccd_independent(statements):
        fail("RCCD vocabulary leaked into membership criteria")
    positive = model.classify(model.ClassEvidence(True, True, True, True, True, True))
    negative = model.classify(model.ClassEvidence(True, False, True, True, True, True))
    unknown = model.classify(model.ClassEvidence(True, True, True, True, True, False))
    if positive.status.value != "in_scope" or negative.status.value != "out_of_scope" or unknown.status.value != "unknown":
        fail("three-valued classifier is invalid")
    if result["rccd_necessity_proved"] or result["class_maximality_proved"] or result["unknowns_promoted"]:
        fail("downstream result inflated")
    if queue["next_action"] != {"target_pr": 284, "workstream": "UPP-W3-CONTRACT"}:
        fail("queue does not advance to PR 284")
    if queue["ordered_followups"] != list(range(285, 297)):
        fail("ordered followups changed")
    if queue["public_evaluation_authorized"]:
        fail("release gate opened")
    print("PASS: UPP-W2 class is neutral, executable, three-valued, and queue-consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
