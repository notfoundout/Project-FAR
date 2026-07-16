#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001"
FILES = [
    "README.md",
    "preregistration.md",
    "isolation-protocol.json",
    "decision-rules.json",
    "output-schema.json",
    "package-manifest.json",
    "execution-lock.json",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for name in FILES:
        if not (PKG / name).is_file():
            fail(f"missing file: {name}")

    isolation = json.loads((PKG / "isolation-protocol.json").read_text(encoding="utf-8"))
    rules = json.loads((PKG / "decision-rules.json").read_text(encoding="utf-8"))
    manifest = json.loads((PKG / "package-manifest.json").read_text(encoding="utf-8"))
    lock = json.loads((PKG / "execution-lock.json").read_text(encoding="utf-8"))
    json.loads((PKG / "output-schema.json").read_text(encoding="utf-8"))

    if isolation.get("minimum_implementation_teams", 0) < 2:
        fail("at least two implementation teams are required")
    if isolation.get("minimum_verifier_teams", 0) < 1:
        fail("an independent verifier team is required")
    if isolation["team_separation"].get("shared_personnel_permitted") is not False:
        fail("shared personnel must be prohibited")
    if isolation["team_separation"].get("verifier_personnel_may_build_candidates") is not False:
        fail("verifier personnel must be independent")
    if "contaminated" not in rules.get("submission_outcomes", {}):
        fail("contaminated outcome missing")
    if "inconclusive" not in rules.get("submission_outcomes", {}):
        fail("inconclusive outcome missing")
    if manifest.get("checksum_state") != "locked":
        fail("checksum state must remain locked")
    if not (PKG / "checksum-lock.json").is_file():
        fail("locked package requires checksum-lock.json")

    subprocess.run(
        [sys.executable, "tools/check_cre002_ext001_rep001_checksums.py"],
        cwd=ROOT,
        check=True,
    )

    phase = manifest.get("status")
    valid_phases = {
        "preregistered-checksum-locked",
        "team-registration-open",
        "superseded-not-executed",
    }
    if phase not in valid_phases:
        fail(f"unsupported administrative phase: {phase}")

    valid_lock_states = {
        "locked",
        "team-registration-open-execution-locked",
        "superseded-not-executed-permanently-locked",
    }
    if lock.get("state") not in valid_lock_states:
        fail("execution lock state is invalid")

    for key in ("execution_authorized", "compiler_implementation_authorized", "official_results_present"):
        if manifest.get(key) is not False or lock.get(key) is not False:
            fail(f"{key} must remain false")

    if phase == "team-registration-open":
        if manifest.get("team_registration_authorized") is not True:
            fail("manifest must authorize team registration")
        if lock.get("team_registration_authorized") is not True:
            fail("execution control must authorize team registration")
        for name in ("team-registration-schema.json", "team-registry.json"):
            if not (PKG / name).is_file():
                fail(f"missing registration control: {name}")

    if phase == "superseded-not-executed":
        if manifest.get("team_registration_authorized") is not False:
            fail("superseded package must prohibit team registration")
        if lock.get("team_registration_authorized") is not False:
            fail("superseded execution control must prohibit team registration")
        if manifest.get("execution_history") != "not executed":
            fail("superseded package must record that execution did not occur")
        if manifest.get("superseded_by") != "CRE-002-EXT-001-ROB-001":
            fail("superseded package must identify the robustness replacement")

    for name in ("generated", "results", "submissions"):
        if (PKG / name).exists():
            fail(f"forbidden pre-execution path exists: {name}")

    print("CRE-002-EXT-001-REP-001 PREREGISTRATION CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
