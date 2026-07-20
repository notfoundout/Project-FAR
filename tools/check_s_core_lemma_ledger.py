#!/usr/bin/env python3
"""Validate the frozen S_core lemma ledger through completed W2."""
from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/s-core-construction-obstruction-ledger-v1.0.md"
REG = ROOT / "theory/evaluation/s-core-construction-obstruction-ledger.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
MAKEFILE = ROOT / "Makefile"
WAVE_ORDER = {f"W{i}": i for i in range(6)}
TERMINAL = {"proved", "refuted", "obstruction_established", "scope_boundary_established", "superseded"}
PROOF_FILES = {
    "W0": (ROOT / "docs/research/s-core-w0-normalization-proof-v1.0.md", ROOT / "theory/evaluation/s-core-w0-normalization-proof.json"),
    "W1": (ROOT / "docs/research/s-core-w1-direct-axis-proof-v1.0.md", ROOT / "theory/evaluation/s-core-w1-direct-axis-proof.json"),
    "W2": (ROOT / "docs/research/s-core-w2-dynamics-history-proof-v1.0.md", ROOT / "theory/evaluation/s-core-w2-dynamics-history-proof.json"),
}
PROVED_BY_WAVE = {
    "W0": {f"LEM-SC-{i:03d}" for i in range(1, 5)},
    "W1": {"LEM-SC-005", "LEM-SC-006", "LEM-SC-007", "LEM-SC-008", "LEM-SC-009", "LEM-SC-012", "LEM-SC-014"},
    "W2": {"LEM-SC-010", "LEM-SC-011", "LEM-SC-013", "LEM-SC-015", "LEM-SC-016"},
}
REFUTED_BY_WAVE = {"W1": {"OBS-SC-003", "OBS-SC-006"}, "W2": {"OBS-SC-004", "OBS-SC-005"}}
W3_ACTIVE = {f"LEM-SC-{i:03d}" for i in range(17, 25)}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_dependency_graph(obligations: list[dict]) -> None:
    by_id = {item["id"]: item for item in obligations}
    incoming = {item_id: set(item.get("depends_on", [])) for item_id, item in by_id.items()}
    for item_id, deps in incoming.items():
        assert deps <= set(by_id), f"{item_id} has unknown dependencies"
        assert item_id not in deps
        for dep in deps:
            assert WAVE_ORDER[by_id[dep]["wave"]] <= WAVE_ORDER[by_id[item_id]["wave"]]
    outgoing: dict[str, set[str]] = defaultdict(set)
    for item_id, deps in incoming.items():
        for dep in deps:
            outgoing[dep].add(item_id)
    ready = deque(sorted(item_id for item_id, deps in incoming.items() if not deps))
    seen = []
    while ready:
        item_id = ready.popleft(); seen.append(item_id)
        for child in sorted(outgoing[item_id]):
            incoming[child].remove(item_id)
            if not incoming[child]: ready.append(child)
    assert len(seen) == len(obligations), "lemma dependency graph must be acyclic"


def main() -> int:
    required_paths = [DOC, REG, TARGET, GATES, MAKEFILE]
    for pair in PROOF_FILES.values(): required_paths.extend(pair)
    for path in required_paths:
        assert path.is_file(), f"missing S_core lemma-ledger artifact: {path.relative_to(ROOT)}"

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "S_core Construction and Obstruction Lemma Ledger v1.0",
        "W0, W1, and W2 complete; W3 active",
        "LEM-SC-010` — deterministic dynamics construction — **proved**",
        "LEM-SC-016` — self-modification and rule-version change — **proved**",
        "OBS-SC-004` — dynamics-bisimulation mismatch — **refuted**",
        "OBS-SC-005` — history-and-path collapse — **refuted**",
        "Execute the W3 global-witness package",
    ):
        assert phrase in text, f"lemma ledger missing required phrase: {phrase}"

    data = load(REG)
    assert data.get("schema_version") == "1.0"
    assert data.get("ledger_id") == "SCORE-LEMMA-LEDGER-001"
    assert data.get("version") == "1.0"
    assert data.get("status") == "frozen_dependency_decomposition_w0_w1_w2_complete_w3_active"
    assert data.get("theorem_target") == "THM-TARGET-001"
    assert data.get("source_scope") == "S_core"
    assert data.get("faithful_predicate") == "Faithful_split"
    assert set(data.get("waves", {})) == set(WAVE_ORDER)
    assert data.get("completed_waves") == ["W0", "W1", "W2"]
    assert data.get("active_wave") == "W3"
    assert data.get("proof_packages") == [pair[1].relative_to(ROOT).as_posix() for pair in PROOF_FILES.values()]

    obligations = data.get("obligations", [])
    assert len(obligations) == 37
    ids = [item["id"] for item in obligations]
    assert len(ids) == len(set(ids))
    assert set(ids) == {*{f"LEM-SC-{i:03d}" for i in range(1, 25)}, *{f"OBS-SC-{i:03d}" for i in range(1, 11)}, *{f"ASM-SC-{i:03d}" for i in range(1, 4)}}
    assert Counter(item["class"] for item in obligations) == {"construction": 24, "obstruction": 10, "assembly": 3}
    assert all(item["status"] in set(data["allowed_statuses"]) for item in obligations)
    assert_dependency_graph(obligations)

    by_id = {item["id"]: item for item in obligations}
    for wave, item_ids in PROVED_BY_WAVE.items():
        evidence = [path.relative_to(ROOT).as_posix() for path in PROOF_FILES[wave]]
        for item_id in item_ids:
            assert by_id[item_id]["status"] == "proved"
            assert by_id[item_id]["evidence"] == evidence
    w0_evidence = [path.relative_to(ROOT).as_posix() for path in PROOF_FILES["W0"]]
    assert by_id["OBS-SC-001"]["status"] == "scope_boundary_established"
    assert by_id["OBS-SC-001"]["evidence"] == w0_evidence
    for wave, item_ids in REFUTED_BY_WAVE.items():
        evidence = [path.relative_to(ROOT).as_posix() for path in PROOF_FILES[wave]]
        for item_id in item_ids:
            assert by_id[item_id]["status"] == "refuted"
            assert by_id[item_id]["evidence"] == evidence

    for item in obligations:
        evidence = item.get("evidence")
        assert isinstance(evidence, list)
        if item["status"] in TERMINAL:
            assert evidence
            for relative in evidence: assert (ROOT / relative).is_file(), relative
        elif item["status"] == "registered_unproved":
            assert evidence == []

    active = set(data.get("active_obligations", []))
    assert active == W3_ACTIVE
    assert all(by_id[item_id]["wave"] == "W3" and by_id[item_id]["status"] == "registered_unproved" for item_id in active)
    mandatory = set(data.get("mandatory_features", []))
    covered = {feature for item in obligations for feature in item.get("covers", [])}
    assert mandatory == covered and len(mandatory) == 20

    counts = Counter(item["status"] for item in obligations)
    summary = data.get("execution_summary", {})
    assert summary == {"total":37,"construction":24,"obstruction":10,"assembly":3,"proved":16,"obstruction_established":0,"scope_boundary_established":1,"refuted":4,"open":16}
    for key in ("proved", "obstruction_established", "scope_boundary_established", "refuted"):
        assert counts[key] == summary[key]
    assert sum(counts[name] for name in ("registered_unproved", "proof_in_progress", "blocked", "unknown")) == summary["open"]

    target = load(TARGET)
    program = target.get("lemma_program", {})
    assert program.get("status") == "w0_w1_w2_complete_w3_active"
    assert program.get("proved_obligations") == 16
    assert program.get("refuted_obstruction_hypotheses") == 4
    assert program.get("scope_boundaries_established") == 1
    assert program.get("open_obligations") == 16
    assert program.get("completed_waves") == ["W0", "W1", "W2"]
    assert program.get("active_wave") == "W3"
    family = {item["id"]: item for item in target.get("theorem_family", [])}
    assert family["THM-CORE-REP-001"]["blocked_by"] == ["lemma_ledger_execution"]
    assert family["THM-CORE-COMMON-001"]["blocked_by"] == ["lemma_ledger_execution"]
    assert target.get("next_required_artifact") == data.get("next_required_artifact")

    gates = load(GATES)
    required = set(gates.get("required_canonical_artifacts", []))
    for path in required_paths[:-1]:
        assert path.relative_to(ROOT).as_posix() in required
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["scoped-representation-proof"]["evidence"] == []

    makefile = MAKEFILE.read_text(encoding="utf-8")
    for checker in ("check_s_core_lemma_ledger.py", "check_s_core_w0.py", "check_s_core_w1.py", "check_s_core_w2.py"):
        assert makefile.count(f"python tools/{checker}") == 3

    print("S_core lemma ledger: PASS (W0-W2 complete; 16 proved; 4 refuted; 1 boundary; 16 open; W3 active)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
