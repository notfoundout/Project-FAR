#!/usr/bin/env python3
"""Validate the frozen S_core construction and obstruction lemma ledger."""
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


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_acyclic(obligations: list[dict]) -> None:
    ids = {item["id"] for item in obligations}
    incoming = {item["id"]: set(item.get("depends_on", [])) for item in obligations}
    for item_id, deps in incoming.items():
        assert deps <= ids, f"{item_id} has unknown dependencies: {sorted(deps - ids)}"
        assert item_id not in deps, f"{item_id} depends on itself"
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
    for path in (DOC, REG, TARGET, GATES, MAKEFILE):
        assert path.is_file(), f"missing S_core lemma-ledger artifact: {path.relative_to(ROOT)}"

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "S_core Construction and Obstruction Lemma Ledger v1.0",
        "registered_unexecuted",
        "LEM-SC-001",
        "LEM-SC-024",
        "OBS-SC-010",
        "ASM-SC-003",
        "Failure of one attempted construction does not establish nonexistence",
        "does not prove any listed lemma",
        "Prove or refute the W0 source-normalization kernel",
    ):
        assert phrase in text, f"lemma ledger missing required phrase: {phrase}"

    data = load(REG)
    assert data.get("schema_version") == "1.0"
    assert data.get("ledger_id") == "SCORE-LEMMA-LEDGER-001"
    assert data.get("version") == "1.0"
    assert data.get("status") == "frozen_dependency_decomposition_registered_unexecuted"
    assert data.get("theorem_target") == "THM-TARGET-001"
    assert data.get("source_scope") == "S_core"
    assert data.get("faithful_predicate") == "Faithful_split"

    obligations = data.get("obligations", [])
    assert len(obligations) == 37
    ids = [item.get("id") for item in obligations]
    assert len(ids) == len(set(ids)), "lemma identifiers must be unique"
    assert set(ids) == {
        *{f"LEM-SC-{i:03d}" for i in range(1, 25)},
        *{f"OBS-SC-{i:03d}" for i in range(1, 11)},
        *{f"ASM-SC-{i:03d}" for i in range(1, 4)},
    }
    classes = Counter(item.get("class") for item in obligations)
    assert classes == {"construction": 24, "obstruction": 10, "assembly": 3}
    assert all(item.get("status") == "registered_unproved" for item in obligations)
    assert all(item.get("evidence") == [] for item in obligations)
    assert_acyclic(obligations)

    mandatory = set(data.get("mandatory_features", []))
    covered = {feature for item in obligations for feature in item.get("covers", [])}
    assert mandatory == covered, f"feature coverage mismatch: missing={sorted(mandatory-covered)} extra={sorted(covered-mandatory)}"
    assert len(mandatory) == 20

    summary = data.get("execution_summary", {})
    assert summary == {
        "total": 37,
        "construction": 24,
        "obstruction": 10,
        "assembly": 3,
        "proved": 0,
        "obstruction_established": 0,
        "refuted": 0,
        "open": 37,
    }
    assert data.get("next_required_artifact") == "W0 proof package for LEM-SC-001 through LEM-SC-004"

    target = load(TARGET)
    assert target.get("lemma_ledger_artifact") == DOC.relative_to(ROOT).as_posix()
    assert target.get("lemma_ledger_registry") == REG.relative_to(ROOT).as_posix()
    program = target.get("lemma_program", {})
    assert program.get("status") == "registered_unexecuted"
    assert program.get("total_obligations") == 37
    assert program.get("open_obligations") == 37
    assert program.get("proved_obligations") == 0
    family = {item["id"]: item for item in target.get("theorem_family", [])}
    assert family["THM-CORE-REP-001"].get("blocked_by") == ["lemma_ledger_execution"]
    assert family["THM-CORE-COMMON-001"].get("blocked_by") == ["lemma_ledger_execution"]
    assert target.get("next_required_artifact") == "W0 proof package for LEM-SC-001 through LEM-SC-004"

    gates = load(GATES)
    required = set(gates.get("required_canonical_artifacts", []))
    assert DOC.relative_to(ROOT).as_posix() in required
    assert REG.relative_to(ROOT).as_posix() in required
    by_name = {gate["name"]: gate for gate in gates.get("gates", [])}
    assert by_name["scoped-representation-proof"]["status"] == "not_satisfied"
    assert by_name["scoped-representation-proof"]["evidence"] == []

    makefile = MAKEFILE.read_text(encoding="utf-8")
    assert makefile.count("python tools/check_s_core_lemma_ledger.py") == 3

    print("S_core lemma ledger: PASS (37 obligations registered; 0 proved; W0 next)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
