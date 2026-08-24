#!/usr/bin/env python3
"""Verify preservation and supersession of the historical UPP evaluation program."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "theory/evaluation/post-terminal-public-evaluation-program-v1.0.json"
NEW = ROOT / "theory/evaluation/post-closure-assurance-and-application-program-v1.0.json"
UPP = ROOT / "theory/terminal/upp-terminal-theorem-v1.0.json"
LEDGER = ROOT / "theory/terminal/project-far-core-theory-v1.0.json"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def main() -> int:
    for path in (OLD, NEW, UPP, LEDGER):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")
    old, new, upp, ledger = map(load, (OLD, NEW, UPP, LEDGER))
    if old.get("status") != "superseded" or old.get("superseded_by") != "POST-CLOSURE-001":
        fail("historical program is not explicitly superseded")
    if new.get("program_id") != "POST-CLOSURE-001" or new.get("core_theory_closed") is not True:
        fail("post-closure program identity or closure gate malformed")
    if upp.get("terminal_result") != old.get("predecessor_terminal_result"):
        fail("historical UPP identity was not preserved")
    if ledger.get("dispositions", {}).get("frozen_upp") != "proposition_not_refuted_derivation_defective_theorem_not_established":
        fail("current UPP disposition drifted")
    print("PASS: historical UPP program preserved and superseded by POST-CLOSURE-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
