#!/usr/bin/env python3
"""Validate SCORE-W2-PROOF-001 and its conservative repository integration."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/s-core-w2-dynamics-history-proof-v1.0.md"
REG = ROOT / "theory/evaluation/s-core-w2-dynamics-history-proof.json"
FIXTURES = ROOT / "theory/evaluation/s-core-w2-reference-fixtures.json"
LEDGER = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
REFERENCE = ROOT / "tools/s_core_w2_reference.py"
TEST = ROOT / "tests/test_s_core_w2_reference.py"
AUDIT = ROOT / "docs/audits/s-core-w2-proof-audit.md"
MAKEFILE = ROOT / "Makefile"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (DOC, REG, FIXTURES, LEDGER, TARGET, GATES, REFERENCE, TEST, AUDIT, MAKEFILE):
        assert path.is_file(), f"missing W2 artifact: {path.relative_to(ROOT)}"

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "S_core W2 Dynamics, History, Revision, and Self-Modification Proof v1.0",
        "SCORE-W2-PROOF-001",
        "Therefore `LEM-SC-010` is proved",
        "Therefore `LEM-SC-011` is proved",
        "Therefore `LEM-SC-013` is proved",
        "Therefore `LEM-SC-015` is proved",
        "Therefore `LEM-SC-016` is proved",
        "`OBS-SC-004` is therefore **refuted**",
        "`OBS-SC-005` is therefore **refuted**",
        "admissible target-only recovery",
        "proof-assistant verification or independent proof review",
    ):
        assert phrase in text, f"W2 proof missing required phrase: {phrase}"

    proof = load(REG)
    assert proof.get("schema_version") == "1.0"
    assert proof.get("proof_id") == "SCORE-W2-PROOF-001"
    assert proof.get("version") == "1.0"
    assert proof.get("status") == "project_authored_human_checkable_proof"
    assert proof.get("source_scope") == "S_core"
    assert proof.get("proof_artifact") == DOC.relative_to(ROOT).as_posix()
    assert proof.get("reference_implementation") == REFERENCE.relative_to(ROOT).as_posix()
    assert proof.get("reference_tests") == TEST.relative_to(ROOT).as_posix()
    assert proof.get("reference_fixtures") == FIXTURES.relative_to(ROOT).as_posix()
    assert proof.get("audit_artifact") == AUDIT.relative_to(ROOT).as_posix()
    assert proof.get("target_schema", {}).get("id") == "DYN-HISTORY-1.0"
    assert proof.get("target_schema", {}).get("adds_new_primitive") is False
    assert proof.get("target_schema", {}).get("reuses_w1_images") is True

    results = {item["id"]: item for item in proof.get("results", [])}
    assert set(results) == {"LEM-SC-010", "LEM-SC-011", "LEM-SC-013", "LEM-SC-015", "LEM-SC-016", "OBS-SC-004", "OBS-SC-005"}
    for lemma_id in ("LEM-SC-010", "LEM-SC-011", "LEM-SC-013", "LEM-SC-015", "LEM-SC-016"):
        assert results[lemma_id].get("status") == "proved"
        assert results[lemma_id].get("proof_sections")
    for obstruction_id in ("OBS-SC-004", "OBS-SC-005"):
        assert results[obstruction_id].get("status") == "refuted"
        assert results[obstruction_id].get("scope")

    dependency_audit = proof.get("dependency_audit", {})
    for key in (
        "uses_w3_recovery", "uses_global_semantic_agreement", "uses_complete_cross_axis_coherence",
        "uses_complete_machinery_ledger", "uses_distributed_composition", "uses_complete_constructor_uniformity",
        "uses_faithful_split_satisfiability", "uses_external_process_correspondence",
    ):
        assert dependency_audit.get(key) is False
    assert dependency_audit.get("all_dependencies_frozen_or_proved_in_package") is True

    verification = proof.get("verification", {})
    assert verification.get("human_proof_status") == "complete_project_authored"
    assert verification.get("machine_check_status") == "bounded_executable_reference_only"
    assert verification.get("reference_test_count") == 11
    assert verification.get("proof_assistant_status") == "not_started"
    assert verification.get("independent_review_status") == "not_started"

    effect = proof.get("ledger_effect", {})
    assert effect == {
        "proved_obligations": 16,
        "refuted_obstruction_hypotheses": 4,
        "scope_boundaries_established": 1,
        "open_obligations": 16,
        "completed_waves": ["W0", "W1", "W2"],
        "active_wave": "W3",
    }

    fixtures = load(FIXTURES)
    assert fixtures.get("schema_version") == "1.0"
    assert fixtures.get("fixture_set_id") == "SCORE-W2-FIXTURES-001"
    assert len(fixtures.get("fixtures", [])) >= 2
    assert len(fixtures.get("negative_fixtures", [])) >= 2

    ledger = load(LEDGER)
    by_id = {item["id"]: item for item in ledger.get("obligations", [])}
    evidence = [DOC.relative_to(ROOT).as_posix(), REG.relative_to(ROOT).as_posix()]
    for lemma_id in ("LEM-SC-010", "LEM-SC-011", "LEM-SC-013", "LEM-SC-015", "LEM-SC-016"):
        assert by_id[lemma_id].get("status") == "proved"
        assert by_id[lemma_id].get("evidence") == evidence
    for obstruction_id in ("OBS-SC-004", "OBS-SC-005"):
        assert by_id[obstruction_id].get("status") == "refuted"
        assert by_id[obstruction_id].get("evidence") == evidence
    summary = ledger.get("execution_summary", {})
    assert summary.get("total") == 37
    assert summary.get("proved") == 16
    assert summary.get("refuted") == 4
    assert summary.get("scope_boundary_established") == 1
    assert summary.get("open") == 16
    assert ledger.get("completed_waves") == ["W0", "W1", "W2"]
    assert ledger.get("active_wave") == "W3"
    assert set(ledger.get("active_obligations", [])) == {f"LEM-SC-{i:03d}" for i in range(17, 25)}

    target = load(TARGET)
    program = target.get("lemma_program", {})
    assert program.get("status") == "w0_w1_w2_complete_w3_active"
    assert program.get("proved_obligations") == 16
    assert program.get("refuted_obstruction_hypotheses") == 4
    assert program.get("established_scope_boundaries") == 1
    assert program.get("open_obligations") == 16
    assert program.get("completed_waves") == ["W0", "W1", "W2"]
    assert program.get("active_wave") == "W3"
    assert target.get("proof_status") == "partial_lemmas_only"
    assert target.get("independent_review_status") == "not_started"

    gates = load(GATES)
    required = set(gates.get("required_canonical_artifacts", []))
    for path in (DOC, REG, FIXTURES, AUDIT):
        assert path.relative_to(ROOT).as_posix() in required
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["scoped-representation-proof"]["evidence"] == []
    assert by_name["mechanized-proof-verification"]["status"] == "not_satisfied"
    assert by_name["independent-proof-review"]["status"] == "not_satisfied"

    makefile = MAKEFILE.read_text(encoding="utf-8")
    assert makefile.count("python tools/check_s_core_w2.py") == 3

    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_s_core_w2_reference.py"],
        cwd=ROOT, text=True, capture_output=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr

    print("S_core W2 proof: PASS (5 lemmas proved; 2 obstruction hypotheses refuted; W3 active)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
