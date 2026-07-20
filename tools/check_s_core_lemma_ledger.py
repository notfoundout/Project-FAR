#!/usr/bin/env python3
"""Validate the frozen S_core lemma ledger through completed W1."""
from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/s-core-construction-obstruction-ledger-v1.0.md"
REG = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
W0_DOC = ROOT / "docs/research/s-core-w0-normalization-proof-v1.0.md"
W0_REG = ROOT / "theory/evaluation/s-core-w0-normalization-proof.json"
W1_DOC = ROOT / "docs/research/s-core-w1-direct-axis-proof-v1.0.md"
W1_REG = ROOT / "theory/evaluation/s-core-w1-direct-axis-proof.json"
MAKEFILE = ROOT / "Makefile"
WAVE_ORDER = {f"W{i}": i for i in range(6)}
TERMINAL = {"proved", "refuted", "obstruction_established", "scope_boundary_established", "superseded"}
W0_PROVED = {f"LEM-SC-{i:03d}" for i in range(1, 5)}
W1_PROVED = {"LEM-SC-005", "LEM-SC-006", "LEM-SC-007", "LEM-SC-008", "LEM-SC-009", "LEM-SC-012", "LEM-SC-014"}
W1_REFUTED = {"OBS-SC-003", "OBS-SC-006"}
W2_ACTIVE = {"LEM-SC-010", "LEM-SC-011", "LEM-SC-013", "LEM-SC-015", "LEM-SC-016"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_dependency_graph(obligations: list[dict]) -> None:
    by_id = {item["id"]: item for item in obligations}
    ids = set(by_id)
    incoming = {item_id: set(item.get("depends_on", [])) for item_id, item in by_id.items()}
    for item_id, deps in incoming.items():
        assert deps <= ids, f"{item_id} has unknown dependencies: {sorted(deps - ids)}"
        assert item_id not in deps, f"{item_id} depends on itself"
        item_wave = by_id[item_id].get("wave")
        assert item_wave in WAVE_ORDER, f"{item_id} has invalid wave: {item_wave}"
        for dep in deps:
            dep_wave = by_id[dep].get("wave")
            assert dep_wave in WAVE_ORDER
            assert WAVE_ORDER[dep_wave] <= WAVE_ORDER[item_wave], f"{item_id} depends backward on {dep}"
    outgoing: dict[str, set[str]] = defaultdict(set)
    for item_id, deps in incoming.items():
        for dep in deps:
            outgoing[dep].add(item_id)
    ready = deque(sorted(item_id for item_id, deps in incoming.items() if not deps))
    seen: list[str] = []
    while ready:
        item_id = ready.popleft()
        seen.append(item_id)
        for child in sorted(outgoing[item_id]):
            incoming[child].remove(item_id)
            if not incoming[child]:
                ready.append(child)
    assert len(seen) == len(obligations), "lemma dependency graph must be acyclic"


def main() -> int:
    for path in (DOC, REG, TARGET, GATES, W0_DOC, W0_REG, W1_DOC, W1_REG, MAKEFILE):
        assert path.is_file(), f"missing S_core lemma-ledger artifact: {path.relative_to(ROOT)}"

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "S_core Construction and Obstruction Lemma Ledger v1.0",
        "W0 and W1 complete, W2 active",
        "LEM-SC-001` — finite source-contract normalization — **proved**",
        "LEM-SC-005` — target carrier allocation — **proved**",
        "OBS-SC-003` — relation-reflection collapse — **refuted**",
        "OBS-SC-006` — evidential-status impossibility — **refuted**",
        "W1 direct-axis results are partial lemma progress",
        "Construct or obstruct the W2 dynamics, history, revision, and self-modification package",
    ):
        assert phrase in text, f"lemma ledger missing required phrase: {phrase}"

    data = load(REG)
    assert data.get("schema_version") == "1.0"
    assert data.get("ledger_id") == "SCORE-LEMMA-LEDGER-001"
    assert data.get("version") == "1.0"
    assert data.get("status") == "frozen_dependency_decomposition_w0_w1_complete_w2_active"
    assert data.get("theorem_target") == "THM-TARGET-001"
    assert data.get("source_scope") == "S_core"
    assert data.get("faithful_predicate") == "Faithful_split"
    assert set(data.get("waves", {})) == set(WAVE_ORDER)
    assert data.get("completed_waves") == ["W0", "W1"]
    assert data.get("active_wave") == "W2"
    assert data.get("proof_packages") == [W0_REG.relative_to(ROOT).as_posix(), W1_REG.relative_to(ROOT).as_posix()]

    obligations = data.get("obligations", [])
    assert len(obligations) == 37
    ids = [item.get("id") for item in obligations]
    assert len(ids) == len(set(ids))
    assert set(ids) == {
        *{f"LEM-SC-{i:03d}" for i in range(1, 25)},
        *{f"OBS-SC-{i:03d}" for i in range(1, 11)},
        *{f"ASM-SC-{i:03d}" for i in range(1, 4)},
    }
    assert Counter(item.get("class") for item in obligations) == {"construction": 24, "obstruction": 10, "assembly": 3}
    allowed = set(data.get("allowed_statuses", []))
    assert all(item.get("status") in allowed for item in obligations)
    assert_dependency_graph(obligations)

    by_id = {item["id"]: item for item in obligations}
    w0_evidence = [W0_DOC.relative_to(ROOT).as_posix(), W0_REG.relative_to(ROOT).as_posix()]
    w1_evidence = [W1_DOC.relative_to(ROOT).as_posix(), W1_REG.relative_to(ROOT).as_posix()]
    for item_id in W0_PROVED:
        assert by_id[item_id]["status"] == "proved"
        assert by_id[item_id]["evidence"] == w0_evidence
    assert by_id["OBS-SC-001"]["status"] == "scope_boundary_established"
    assert by_id["OBS-SC-001"]["evidence"] == w0_evidence
    for item_id in W1_PROVED:
        assert by_id[item_id]["status"] == "proved"
        assert by_id[item_id]["evidence"] == w1_evidence
    for item_id in W1_REFUTED:
        assert by_id[item_id]["status"] == "refuted"
        assert by_id[item_id]["evidence"] == w1_evidence

    for item in obligations:
        evidence = item.get("evidence")
        assert isinstance(evidence, list)
        if item.get("status") in TERMINAL:
            assert evidence, f"terminal obligation requires evidence: {item['id']}"
            for relative in evidence:
                assert (ROOT / relative).is_file(), f"missing obligation evidence: {relative}"
        elif item.get("status") == "registered_unproved":
            assert evidence == [], f"unproved obligation must not carry acceptance evidence: {item['id']}"

    assert by_id["LEM-SC-014"]["wave"] == "W1"
    assert "LEM-SC-013" not in by_id["LEM-SC-014"]["depends_on"]
    active = set(data.get("active_obligations", []))
    assert active == W2_ACTIVE
    assert all(by_id[item_id]["wave"] == "W2" for item_id in active)
    assert all(by_id[item_id]["status"] == "registered_unproved" for item_id in active)

    mandatory = set(data.get("mandatory_features", []))
    covered = {feature for item in obligations for feature in item.get("covers", [])}
    assert mandatory == covered
    assert len(mandatory) == 20

    status_counts = Counter(item["status"] for item in obligations)
    summary = data.get("execution_summary", {})
    assert summary == {
        "total": 37, "construction": 24, "obstruction": 10, "assembly": 3,
        "proved": 11, "obstruction_established": 0,
        "scope_boundary_established": 1, "refuted": 2, "open": 23,
    }
    for key in ("proved", "obstruction_established", "scope_boundary_established", "refuted"):
        assert status_counts[key] == summary[key]
    assert sum(status_counts[name] for name in ("registered_unproved", "proof_in_progress", "blocked", "unknown")) == summary["open"]
    assert data.get("next_required_artifact") == "W2 dynamics history revision and self-modification proof-or-obstruction package"

    target = load(TARGET)
    assert target.get("lemma_ledger_artifact") == DOC.relative_to(ROOT).as_posix()
    assert target.get("lemma_ledger_registry") == REG.relative_to(ROOT).as_posix()
    program = target.get("lemma_program", {})
    assert program.get("status") == "w0_w1_complete_w2_active"
    assert program.get("total_obligations") == 37
    assert program.get("open_obligations") == 23
    assert program.get("proved_obligations") == 11
    assert program.get("scope_boundaries_established") == 1
    assert program.get("refuted_obstructions") == 2
    assert program.get("completed_waves") == ["W0", "W1"]
    assert program.get("active_wave") == "W2"
    family = {item["id"]: item for item in target.get("theorem_family", [])}
    assert family["THM-CORE-REP-001"].get("blocked_by") == ["lemma_ledger_execution"]
    assert family["THM-CORE-COMMON-001"].get("blocked_by") == ["lemma_ledger_execution"]
    assert target.get("next_required_artifact") == data.get("next_required_artifact")

    gates = load(GATES)
    required = set(gates.get("required_canonical_artifacts", []))
    for path in (DOC, REG, W0_DOC, W0_REG, W1_DOC, W1_REG):
        assert path.relative_to(ROOT).as_posix() in required
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["scoped-representation-proof"]["evidence"] == []

    makefile = MAKEFILE.read_text(encoding="utf-8")
    assert makefile.count("python tools/check_s_core_lemma_ledger.py") == 3
    assert makefile.count("python tools/check_s_core_w0.py") == 3
    assert makefile.count("python tools/check_s_core_w1.py") == 3

    print("S_core lemma ledger: PASS (W0/W1 complete; 11 proved; 2 refuted; 1 boundary; 23 open; W2 active)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
