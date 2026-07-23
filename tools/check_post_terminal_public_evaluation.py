#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "theory" / "evaluation" / "post-terminal-public-evaluation-program-v1.0.json"
MODEL = ROOT / "theory" / "evaluation" / "post_terminal_public_evaluation_v1.py"
GOVERNANCE = ROOT / "docs" / "governance" / "post-terminal-public-evaluation-program-v1.0.md"
DISCLOSURE = ROOT / "docs" / "research" / "post-terminal-public-evaluation-disclosure-v1.0.md"
QUEUE = ROOT / "theory" / "evaluation" / "post-tue-universal-proof-queue-checkpoint-v1.0.json"
README = ROOT / "README.md"
EXPECTED = "strictly_weakened_relative_rccd_universality_theorem_proved_with_complete_dependency_audit_and_open_world_boundary"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def load_model():
    spec = importlib.util.spec_from_file_location("post_terminal_eval_checker", MODEL)
    if spec is None or spec.loader is None:
        fail("cannot load evaluation model")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def main() -> int:
    for path in (PROGRAM, MODEL, GOVERNANCE, DISCLOSURE, QUEUE, README):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    program = load_json(PROGRAM)
    queue = load_json(QUEUE)
    model = load_model()

    if program.get("program_id") != "POST-TERM-EVAL-001" or program.get("predecessor_terminal_pr") != 296:
        fail("program identity mismatch")
    if program.get("predecessor_terminal_result") != EXPECTED:
        fail("terminal result mismatch")
    if queue.get("status") != "complete" or queue.get("terminal_outcome") != "strictly_weakened_universal_theorem_proved":
        fail("predecessor queue is not terminal")
    if queue.get("terminal_next_action") is not None or queue.get("terminal_public_evaluation_authorized") is not True:
        fail("terminal authority fields malformed")
    if program.get("public_evaluation_authorized") is not True or program.get("new_deductive_claim_requires_new_program") is not True:
        fail("evaluation or new-program gate malformed")

    required = set(model.REQUIRED_DISCLOSURES)
    aliases = {
        "exact_theorem_and_version": "exact_theorem",
        "all_frozen_premises": "frozen_premises",
        "finite_registered_maximality_boundary": "finite_maximality_boundary",
        "non_kernel_checked_end_to_end_semantic_composition": "non_kernel_checked_terminal_composition",
        "unknown_is_neither_support_nor_defeat": "unknown_discipline",
        "all_nonclaims": "nonclaims",
        "evidence_type_labels": "evidence_type",
    }
    normalized = {aliases.get(normalize(x), normalize(x)) for x in program.get("required_disclosures", [])}
    if required - normalized:
        fail(f"program omits disclosure controls: {sorted(required - normalized)}")

    canonical = model.assess(model.canonical_submission())
    if canonical.verdict is not model.Verdict.CONFIRMED or canonical.impact is not model.Impact.UPGRADE_EVIDENCE:
        fail("canonical independent review assessment mismatch")

    disclosure = DISCLOSURE.read_text(encoding="utf-8").lower()
    for phrase in ("strictly weakened", "not one kernel-checked proof object", "not open-world maximality", "unknown"):
        if phrase not in disclosure:
            fail(f"public disclosure omits {phrase}")

    readme = README.read_text(encoding="utf-8")
    if EXPECTED not in readme or "There is no `UPP-W16`" not in readme:
        fail("README does not expose terminal result and closed queue")

    test = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_post_terminal_public_evaluation.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if test.returncode:
        sys.stderr.write(test.stdout + test.stderr)
        fail("post-terminal evaluation tests failed")

    print("PASS: post-terminal public evaluation program is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
