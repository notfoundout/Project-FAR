#!/usr/bin/env python3
"""Validate SCORE-W4-PROOF-001 and its bounded repository effects."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from s_core_w4_negative_controls import CONTROL_IDS, CONTROL_SPEC, run_suite

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/s-core-w4-negative-control-proof-v1.0.md"
REG = ROOT / "theory/evaluation/s-core-w4-negative-control-proof.json"
FIX = ROOT / "theory/evaluation/s-core-w4-negative-control-fixtures.json"
SOURCE_FIX = ROOT / "theory/evaluation/s-core-w3-reference-fixtures.json"
AUDIT = ROOT / "docs/audits/s-core-w4-proof-audit.md"
LEDGER = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"
FAITHFUL = ROOT / "theory/evaluation/faithful-representation-specification-v1.0.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"
TEST = ROOT / "tests/test_s_core_w4_negative_controls.py"
MAKE = ROOT / "Makefile"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    paths = (DOC, REG, FIX, SOURCE_FIX, AUDIT, LEDGER, FAITHFUL, TARGET, GATES, CLAIMS, TEST, MAKE)
    for path in paths:
        assert path.is_file(), path

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "S_core W4 Formal Negative-Control Proof v1.0",
        "SCORE-W4-PROOF-001",
        "OBS-SC-010",
        "NC-01",
        "NC-10",
        "does not quantify over every possible invalid representation",
        "W5 remains mechanically blocked",
    ):
        assert phrase in text, phrase

    registry = load(REG)
    assert registry["proof_id"] == "SCORE-W4-PROOF-001"
    assert registry["status"] == "complete_project_authored"
    assert registry["program_track"] == "REP"
    assert registry["obligation"] == "OBS-SC-010"
    result = registry["result"]
    assert result["status"] == "obstruction_established"
    assert result["global_nontriviality_status"] == "proved_for_registered_control_families_over_S_core"
    assert result["all_invalid_representations_rejected"] is False
    assert result["faithful_split_satisfiability_proved"] is False

    controls = {item["id"]: item for item in registry["control_results"]}
    assert set(controls) == set(CONTROL_IDS)
    for control_id in CONTROL_IDS:
        assert controls[control_id]["family_status"] == "proved_rejected_when_applicable"
        assert controls[control_id]["diagnostic"] == CONTROL_SPEC[control_id]["diagnostic"]
        assert controls[control_id]["violated_clauses"] == CONTROL_SPEC[control_id]["violated_clauses"]

    fixture = load(FIX)
    assert fixture["fixture_set_id"] == "SCORE-W4-NEGATIVE-CONTROLS-001"
    assert fixture["status"] == "frozen_executed"
    manifest = {item["id"]: item for item in fixture["controls"]}
    assert set(manifest) == set(CONTROL_IDS)
    assert fixture["execution_summary"] == {
        "total_controls": 10,
        "rejected_expected_reason": 10,
        "unexpected_pass": 0,
        "wrong_reason": 0,
        "not_applicable": 0,
        "implementation_defect": 0,
    }

    source = load(SOURCE_FIX)["source"]
    executable = run_suite(source)
    assert len(executable) == 10
    assert {item["id"] for item in executable} == set(CONTROL_IDS)
    for item in executable:
        assert item["status"] == "rejected_expected_reason", item
        expected = manifest[item["id"]]
        assert item["diagnostic"] == expected["expected_diagnostic"]
        assert item["violated_clauses"] == expected["expected_violated_clauses"]

    ledger = load(LEDGER)
    by_id = {item["id"]: item for item in ledger["obligations"]}
    assert by_id["OBS-SC-010"]["status"] == "obstruction_established"
    assert by_id["OBS-SC-010"]["evidence"] == [
        "docs/research/s-core-w4-negative-control-proof-v1.0.md",
        "theory/evaluation/s-core-w4-negative-control-proof.json",
    ]
    summary = ledger["execution_summary"]
    assert (summary["proved"], summary["obstruction_established"], summary["scope_boundary_established"], summary["refuted"], summary["open"]) == (24, 1, 1, 8, 3)
    assert ledger["completed_waves"] == ["W0", "W1", "W2", "W3", "W4"]
    assert ledger["active_wave"] == "W5_blocked"
    assert ledger["active_obligations"] == []
    assert set(ledger["blocked_obligations"]) == {"ASM-SC-001", "ASM-SC-002", "ASM-SC-003"}

    faithful = load(FAITHFUL)
    nontriviality = faithful["nontriviality"]
    assert nontriviality["formal_negative_control_status"] == "proved_OBS-SC-010"
    assert nontriviality["global_nontrivial_status"] == "proved_for_registered_control_families_over_S_core"
    assert faithful["witness_assembly"]["does_not_establish_faithful_split"] is True

    target = load(TARGET)
    program = target["lemma_program"]
    assert program["status"] == "w0_w1_w2_w3_w4_complete_w5_blocked_by_w3_5"
    assert program["established_obstructions"] == 1
    assert program["open_obligations"] == 3
    assert target["w5_authorization"]["authorized"] is False
    assert target["w5_authorization"]["blocked_by"] == ["W3.5-SDG-001"]

    gates = {item["name"]: item for item in load(GATES)["gates"]}
    assert gates["formal-negative-controls"]["status"] == "satisfied"
    assert gates["formal-negative-controls"]["evidence"] == [
        "docs/research/s-core-w4-negative-control-proof-v1.0.md",
        "theory/evaluation/s-core-w4-negative-control-proof.json",
        "theory/evaluation/s-core-w4-negative-control-fixtures.json",
    ]
    assert gates["scoped-representation-proof"]["status"] == "not_satisfied"
    assert gates["baseline-factorization-resolved"]["status"] == "satisfied"
    assert gates["baseline-factorization-resolved"]["evidence"]
    assert gates["fara-specificity-resolved"]["status"] == "not_satisfied"
    assert gates["reasoning-contrast-execution"]["status"] == "not_satisfied"
    assert gates["universal-structure-result"]["status"] == "not_satisfied"

    claims = {item["id"]: item for item in load(CLAIMS)["claims"]}
    assert claims["CLM-NONTRIVIALITY"]["current_status"] == "supported_at_registered_control_scope"
    assert claims["CLM-UNIVERSAL-STRUCTURE"]["current_status"] == "unresolved"
    assert claims["CLM-UNIVERSALITY"]["current_status"] == "not_established"
    assert claims["CLM-NECESSITY"]["current_status"] == "not_established"
    assert claims["CLM-MINIMALITY"]["current_status"] == "not_established"

    assert MAKE.read_text(encoding="utf-8").count("python tools/check_s_core_w4.py") == 3
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_s_core_w4_negative_controls.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr

    print("S_core W4 proof: PASS (10 control families rejected at registered scope; OBS-SC-010 established; factorization may advance independently; W5 still blocked by remaining W3.5 evidence)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
