#!/usr/bin/env python3
"""Validate SCORE-W0-PROOF-001 and its conservative repository integration."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/s-core-w0-normalization-proof-v1.0.md"
REG = ROOT / "theory/evaluation/s-core-w0-normalization-proof.json"
FIXTURES = ROOT / "theory/evaluation/s-core-w0-reference-fixtures.json"
LEDGER = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
REFERENCE = ROOT / "tools/s_core_w0_reference.py"
TEST = ROOT / "tests/test_s_core_w0_reference.py"
AUDIT = ROOT / "docs/audits/s-core-w0-proof-audit.md"
MAKEFILE = ROOT / "Makefile"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (DOC, REG, FIXTURES, LEDGER, TARGET, GATES, REFERENCE, TEST, AUDIT, MAKEFILE):
        assert path.is_file(), f"missing W0 artifact: {path.relative_to(ROOT)}"

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "S_core W0 Normalization Kernel Proof v1.0",
        "SCORE-W0-PROOF-001",
        "Therefore `LEM-SC-001` is proved",
        "Therefore `LEM-SC-002` is proved",
        "Therefore `LEM-SC-003` is proved",
        "Therefore `LEM-SC-004` is proved",
        "OBS-SC-001` is resolved as `scope_boundary_established",
        "No FARA target component",
        "proof-assistant verification or independent proof review",
    ):
        assert phrase in text, f"W0 proof missing required phrase: {phrase}"

    proof = load(REG)
    assert proof.get("schema_version") == "1.0"
    assert proof.get("proof_id") == "SCORE-W0-PROOF-001"
    assert proof.get("version") == "1.0"
    assert proof.get("status") == "project_authored_human_checkable_proof"
    assert proof.get("source_scope") == "S_core"
    assert proof.get("proof_artifact") == DOC.relative_to(ROOT).as_posix()
    assert proof.get("reference_implementation") == REFERENCE.relative_to(ROOT).as_posix()
    assert proof.get("reference_tests") == TEST.relative_to(ROOT).as_posix()
    assert proof.get("reference_fixtures") == FIXTURES.relative_to(ROOT).as_posix()
    assert proof.get("audit_artifact") == AUDIT.relative_to(ROOT).as_posix()

    results = {item["id"]: item for item in proof.get("results", [])}
    assert set(results) == {"LEM-SC-001", "LEM-SC-002", "LEM-SC-003", "LEM-SC-004", "OBS-SC-001"}
    for lemma_id in ("LEM-SC-001", "LEM-SC-002", "LEM-SC-003", "LEM-SC-004"):
        assert results[lemma_id].get("status") == "proved"
        assert results[lemma_id].get("proof_sections")
    assert results["OBS-SC-001"].get("status") == "scope_boundary_established"

    dependency_audit = proof.get("dependency_audit", {})
    for key in ("uses_target_structure", "uses_fara_adequacy", "uses_faithful_split_satisfiability", "uses_external_process_correspondence"):
        assert dependency_audit.get(key) is False
    assert dependency_audit.get("all_dependencies_frozen_or_proved_in_package") is True

    verification = proof.get("verification", {})
    assert verification.get("human_proof_status") == "complete_project_authored"
    assert verification.get("machine_check_status") == "bounded_executable_reference_only"
    assert verification.get("proof_assistant_status") == "not_started"
    assert verification.get("independent_review_status") == "not_started"

    effect = proof.get("ledger_effect", {})
    assert effect == {
        "proved_obligations": 4,
        "scope_boundaries_established": 1,
        "open_obligations": 32,
        "completed_wave": "W0",
        "active_wave": "W1",
    }
    assert proof.get("next_required_artifact") == "W1 base-carrier and direct-axis construction proof package"

    fixtures = load(FIXTURES)
    assert fixtures.get("schema_version") == "1.0"
    assert fixtures.get("fixture_set_id") == "SCORE-W0-FIXTURES-001"
    assert len(fixtures.get("fixtures", [])) >= 2
    assert len(fixtures.get("negative_fixtures", [])) >= 2

    ledger = load(LEDGER)
    by_id = {item["id"]: item for item in ledger.get("obligations", [])}
    for lemma_id in ("LEM-SC-001", "LEM-SC-002", "LEM-SC-003", "LEM-SC-004"):
        assert by_id[lemma_id].get("status") == "proved"
        assert DOC.relative_to(ROOT).as_posix() in by_id[lemma_id].get("evidence", [])
        assert REG.relative_to(ROOT).as_posix() in by_id[lemma_id].get("evidence", [])
    assert by_id["OBS-SC-001"].get("status") == "scope_boundary_established"
    assert DOC.relative_to(ROOT).as_posix() in by_id["OBS-SC-001"].get("evidence", [])
    summary = ledger.get("execution_summary", {})
    assert summary.get("total") == 37
    assert summary.get("proved") == 4
    assert summary.get("scope_boundary_established") == 1
    assert summary.get("open") == 32
    assert ledger.get("next_required_artifact") == "W1 base-carrier and direct-axis construction proof package"

    target = load(TARGET)
    program = target.get("lemma_program", {})
    assert program.get("status") == "w0_complete_w1_active"
    assert program.get("proved_obligations") == 4
    assert program.get("established_scope_boundaries") == 1
    assert program.get("open_obligations") == 32
    assert program.get("completed_waves") == ["W0"]
    assert program.get("active_wave") == "W1"
    assert set(program.get("active_obligations", [])) == {
        "LEM-SC-005", "LEM-SC-006", "LEM-SC-007", "LEM-SC-008", "LEM-SC-009", "LEM-SC-012", "LEM-SC-014"
    }
    assert target.get("proof_status") == "partial_lemmas_only"
    assert target.get("machine_check_status") == "bounded_executable_reference_only"
    assert target.get("independent_review_status") == "not_started"
    assert target.get("next_required_artifact") == "W1 base-carrier and direct-axis construction proof package"

    gates = load(GATES)
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["mechanized-proof-verification"]["status"] == "not_satisfied"
    assert by_name["independent-proof-review"]["status"] == "not_satisfied"

    makefile = MAKEFILE.read_text(encoding="utf-8")
    assert makefile.count("python tools/check_s_core_w0.py") == 3

    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_s_core_w0_reference.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr

    print("S_core W0 proof: PASS (4 lemmas proved; 1 scope boundary; W1 active)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
