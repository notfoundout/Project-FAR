#!/usr/bin/env python3
"""Fail-closed consistency check for PROJECT-FAR-CORE-THEORY-1.0."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEORY = ROOT / "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
LEDGER = ROOT / "theory/terminal/project-far-core-theory-v1.0.json"
PROGRAM = ROOT / "theory/evaluation/post-closure-assurance-and-application-program-v1.0.json"
OLD_PROGRAM = ROOT / "theory/evaluation/post-terminal-public-evaluation-program-v1.0.json"
EXPECTED_SHA256 = "b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5"
EXPECTED_VERDICT = "NONTRIVIAL CONTRACT-FREE MINIMAL ARCHITECTURE IS IMPOSSIBLE; CONTRACT-RELATIVE SUFFICIENCY AND A UNIQUE MINIMAL OBSERVATIONAL QUOTIENT ARE PROVED."
EXPECTED_CLAIMS = {f"FAR-CORE-{i:03d}" for i in range(1, 15)}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    paths = {
        "theory": root / THEORY.relative_to(ROOT),
        "ledger": root / LEDGER.relative_to(ROOT),
        "program": root / PROGRAM.relative_to(ROOT),
        "old_program": root / OLD_PROGRAM.relative_to(ROOT),
    }
    for name, path in paths.items():
        if not path.is_file():
            errors.append(f"missing {name}: {path.relative_to(root)}")
    if errors:
        return errors

    theory_bytes = paths["theory"].read_bytes()
    if hashlib.sha256(theory_bytes).hexdigest() != EXPECTED_SHA256:
        errors.append("canonical theory bytes differ from accepted detached artifact")
    theory_text = theory_bytes.decode("utf-8")
    if EXPECTED_VERDICT not in theory_text:
        errors.append("canonical theory omits exact terminal verdict")

    ledger = _load(paths["ledger"])
    if ledger.get("theory_id") != "PROJECT-FAR-CORE-THEORY-1.0":
        errors.append("core theory identity mismatch")
    if ledger.get("terminal_verdict") != EXPECTED_VERDICT:
        errors.append("machine ledger terminal verdict mismatch")
    claims = {row.get("id") for row in ledger.get("claims", [])}
    if claims != EXPECTED_CLAIMS:
        errors.append(f"core claim set mismatch: {sorted(claims ^ EXPECTED_CLAIMS)}")
    proved = {row["id"] for row in ledger.get("claims", []) if row.get("status") == "proved"}
    if proved != {f"FAR-CORE-{i:03d}" for i in range(1, 14)}:
        errors.append("FAR-CORE-001..013 must be exactly the proved claim set")
    if ledger.get("dispositions", {}).get("frozen_upp") != "proposition_not_refuted_derivation_defective_theorem_not_established":
        errors.append("frozen UPP disposition drifted")
    if ledger.get("dispositions", {}).get("omega_primitive") != "rejected":
        errors.append("Ω primitive disposition drifted")

    program = _load(paths["program"])
    if program.get("program_id") != "POST-CLOSURE-001" or program.get("status") != "registered":
        errors.append("post-closure program identity/status mismatch")
    if program.get("core_theory_closed") is not True:
        errors.append("post-closure program reopens the core")
    if program.get("next_action", {}).get("workstream") != "PCA-W1-INDEPENDENT-REVIEW":
        errors.append("post-closure next workstream drifted")

    old_program = _load(paths["old_program"])
    if old_program.get("status") != "superseded" or old_program.get("superseded_by") != "POST-CLOSURE-001":
        errors.append("historical post-terminal program is still current")

    required_text = {
        "README.md": [EXPECTED_VERDICT, "POST-CLOSURE-001", "historical UPP"],
        "docs/project-status.md": ["PROJECT-FAR-CORE-THEORY-1.0", "POST-CLOSURE-001", "theorem not established"],
        "docs/governance/framework-boundaries.md": ["contract-relative behavior", "derived materialized", "workflow verbs"],
        "frameworks/FARA/primitives.md": ["schema roles", "not global primitives"],
        "frameworks/FARA/admissibility-structure.md": ["derived materialized", "does not cause"],
        "frameworks/FAR/workflow.md": ["factorization", "collision", "comparison contract"],
        "frameworks/FARO/comparison.md": ["comparison contract", "factorization"],
        "docs/mechanization/capability-statement.md": ["does not encode a complete comparison contract", "far-ir/1.1"],
        "docs/planning/next-actions.md": ["PCA-W1-INDEPENDENT-REVIEW", "POST-CLOSURE-001"],
        "governance/repository-truth-authority-v1.json": [
            "PROJECT-FAR-CORE-THEORY-1.0",
            "POST-CLOSURE-001",
            "post-closure assurance and application",
        ],
        "docs/governance/fara-formal-kernel-promotion-v1.0.json": [
            "terminal_reclassification",
            "schema-and-contract-roles",
            "FAR-CORE-007",
        ],
        "frameworks/FARA/research/primitive-independence-w1-result.md": [
            "Historical research evidence",
            "schema or contract roles",
            "global primitive-independence/minimality search is closed",
        ],
        "theory/evaluation/generated-fara-operator-w2-summary.md": [
            "Terminal reclassification",
            "workflow verbs, not primitive operators",
            "global finite-basis search is closed",
        ],
        "research/open-problems/open-questions.md": [
            "Historical Open Questions Register (Superseded)",
            "superseded as current authority",
            "POST-CLOSURE-001",
        ],
    }
    for relative, needles in required_text.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing conformity surface: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{relative}: missing {needle!r}")

    primitives = (root / "frameworks/FARA/primitives.md").read_text(encoding="utf-8")
    for stale in ("# Current Candidate Primitives", "smallest unreduced conceptual foundation"):
        if stale in primitives:
            errors.append(f"FARA primitive registry retains superseded claim: {stale}")

    superseded_questions = (root / "research/open-problems/open-questions.md").read_text(encoding="utf-8")
    for stale in ("**Status:** Active", "**Status:** Open"):
        if stale in superseded_questions:
            errors.append(f"historical open-question path retains current status: {stale}")

    primitive_w1 = (root / "frameworks/FARA/research/primitive-independence-w1-result.md").read_text(encoding="utf-8")
    if "remains only a candidate primitive" in primitive_w1:
        errors.append("historical W1 summary retains superseded primitive implication")

    operator_w2 = (root / "theory/evaluation/generated-fara-operator-w2-summary.md").read_text(encoding="utf-8")
    if "**Global claim:** unresolved." in operator_w2:
        errors.append("historical W2 summary retains an unbounded current-open implication")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Project FAR theory-closure conformity: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Project FAR theory-closure conformity: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
