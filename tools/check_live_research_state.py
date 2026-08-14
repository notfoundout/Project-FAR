#!/usr/bin/env python3
"""Validate the noncanonical live-research ledger.

Checks the invariants that keep the reconstruction honest:

- every target and issue carries provenance and one of the three confidence
  classes;
- no defeated objection has drifted back into a live state;
- ``READY_UNDER_INTERNAL_PROTOCOL`` is never described as Acceptance;
- targets whose defining artifacts are NOT_RECOVERED are not authorized for
  execution;
- raw evidence in the store still hashes to what the index recorded.

Exits nonzero on any violation. The ledger is runtime state under ``.far/``;
when it is absent this check is a no-op.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial.evidence import EvidenceStore  # noqa: E402
from far_adversarial.ledger import (  # noqa: E402
    CONFIDENCE_CLASSES,
    DEFEATED_ISSUE_STATES,
    LIVE_ISSUE_STATES,
    Ledger,
    READY_UNDER_INTERNAL_PROTOCOL,
)

STATE_ROOT = ROOT / ".far" / "research" / "presenting-far"
LEDGER_PATH = STATE_ROOT / "live-theory-state.json"
EVIDENCE_ROOT = STATE_ROOT / "evidence"

FORBIDDEN_PROMOTIONS = ("is Accepted", "constitutes Acceptance", "is Promoted",
                        "equals Acceptance")


def check() -> list[str]:
    problems: list[str] = []
    if not LEDGER_PATH.exists():
        return problems
    ledger = Ledger.load(LEDGER_PATH)

    if "not_acceptance" not in ledger.meta:
        problems.append("ledger meta does not record the non-Acceptance boundary")

    for tid, target in sorted(ledger.targets.items()):
        if not target.provenance:
            problems.append(f"{tid}: no provenance")
        if target.confidence_class not in CONFIDENCE_CLASSES:
            problems.append(f"{tid}: unknown confidence class {target.confidence_class!r}")
        if target.status == READY_UNDER_INTERNAL_PROTOCOL:
            joined = " ".join(target.notes) + " " + ledger.meta.get("not_acceptance", "")
            if "not Acceptance" not in joined and "not Project FAR Acceptance" not in joined:
                problems.append(f"{tid}: READY recorded without a non-Acceptance note")
        if target.missing_evidence and target.authorized:
            problems.append(
                f"{tid}: authorized for execution while defining evidence is missing"
            )
        for text in [target.original_formulation, target.current_formulation, *target.notes]:
            for phrase in FORBIDDEN_PROMOTIONS:
                if phrase in text:
                    problems.append(f"{tid}: unsupported promotion wording {phrase!r}")

    for iid, issue in sorted(ledger.issues.items()):
        if not issue.provenance:
            problems.append(f"{iid}: no provenance")
        if issue.confidence_class not in CONFIDENCE_CLASSES:
            problems.append(f"{iid}: unknown confidence class {issue.confidence_class!r}")
        if not issue.history:
            problems.append(f"{iid}: no immutable history")
            continue
        # A defeated objection must never be followed by a live state.
        seen_defeat = False
        for event in issue.history:
            if seen_defeat and event.to_state in LIVE_ISSUE_STATES:
                problems.append(
                    f"{iid}: reopened after {event.from_state} -> {event.to_state}"
                )
            if event.to_state in DEFEATED_ISSUE_STATES:
                seen_defeat = True
        if seen_defeat and issue.state in LIVE_ISSUE_STATES:
            problems.append(f"{iid}: defeated objection is live again ({issue.state})")

    if EVIDENCE_ROOT.exists():
        problems.extend(EvidenceStore(EVIDENCE_ROOT).verify_integrity())
    return problems


def main() -> int:
    problems = check()
    if not LEDGER_PATH.exists():
        print(f"live research ledger absent at {LEDGER_PATH}: nothing to check")
        return 0
    if problems:
        print("FAIL: live research state violations")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("PASS: live research state invariants hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
