#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "theory/evaluation/evc-w4-candidate-expansion-protocol-v1.0.json"
A = ROOT / "theory/evaluation/evc-w4-candidate-admission-template-v1.0.json"
R = ROOT / "theory/evaluation/evc-w4-candidate-expansion-result-template-v1.0.json"
M = ROOT / "theory/evaluation/evc-w4-candidate-expansion-manifest-v1.0.json"
G = ROOT / "docs/research/evc-w4-candidate-expansion-guide-v1.0.md"
D = ROOT / "docs/audits/evc-w4-candidate-expansion-package-audit.md"
PARENT = ROOT / "theory/evaluation/post-w5-usd-next-program-v1.0.json"

def load(path):
    assert path.exists(), f"missing: {path.relative_to(ROOT)}"
    return json.loads(path.read_text())

def main():
    p, a, r, m, parent = map(load, (P, A, R, M, PARENT))
    assert p["protocol_id"] == "EVC-W4-CANDIDATE-EXPANSION-001"
    assert p["status"] == "frozen_unexecuted"
    assert p["parent_program"] == "POST-USD-EVC-001"
    assert len(p["material_novelty_tests"]) == 4
    assert len(p["evaluation_stages"]) == 10
    expected = {"frontier_unchanged", "new_equivalent_minimum", "new_incomparable_minimum", "new_dominant_candidate", "no_successful_new_candidate", "unresolved"}
    assert set(p["terminal_outcomes"]) == expected
    assert set(r["allowed_terminal_outcomes"]) == expected
    assert r["frontier_before"] == ["FARA-001", "LTS-PROV-001"]
    assert set(a["allowed_admission_outcomes"]) == {"admitted", "rejected_not_materially_new", "unresolved"}
    assert all(v is False for v in m["release_state"].values())
    assert "theory/evaluation/post-w5-usd-next-program-v1.0.json" in m["required_artifacts"]
    assert len(m["required_controls"]) == 7
    workstreams = {w["id"] for w in parent["workstreams"]}
    assert "EVC-W4-CANDIDATE-EXPANSION" in workstreams
    text = (G.read_text() + D.read_text()).lower()
    for term in ("unexecuted", "exhaust", "actual-process", "scalar"):
        assert term in text
    print("EVC-W4 candidate expansion package: PASS")

if __name__ == "__main__":
    main()
