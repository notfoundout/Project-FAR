#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/ikd-w2-expanded-candidate-competition-v1.0.json"
FREEZE = ROOT / "theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json"
DOC = ROOT / "docs/research/ikd-w2-expanded-candidate-competition-v1.0.md"
AUDIT = ROOT / "docs/audits/ikd-w2-expanded-candidate-competition-audit.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (RESULT, FREEZE, DOC, AUDIT):
        assert path.is_file(), path
    result = load(RESULT)
    freeze = load(FREEZE)
    doc = DOC.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert result["competition_id"] == "IKD-W2-EXPANDED-COMP-001"
    assert result["status"] == "complete_bounded_comparison"
    assert result["parent_freeze"] == freeze["freeze_id"]
    frozen = {item["id"] for item in freeze["frozen_candidates"]}
    evaluated = set(result["candidate_results"])
    assert frozen <= evaluated
    assert {"FARA-001", "LTS-PROV-001"} <= evaluated
    assert set(result["successful_set"]) == {"FARA-001", "LTS-PROV-001", "COALG-DYN-001"}
    for candidate in result["successful_set"]:
        assert result["candidate_results"][candidate]["coverage"] == "pass"
        assert result["candidate_results"][candidate]["preservation"] == "pass"
    for candidate in frozen - {"COALG-DYN-001"}:
        assert result["candidate_results"][candidate]["coverage"] == "partial"
        assert "boundary" in result["candidate_results"][candidate]
    assert len(result["negative_controls"]) >= 6
    assert all(item.endswith("rejected") for item in result["negative_controls"])
    assert len(result["frontier_relations"]) == 3
    assert all(item[2] == "incomparable" for item in result["frontier_relations"])
    assert result["aggregation"] == "pareto_only_no_scalar_score"
    assert result["winner"] is None
    assert result["terminal_result"] == "three_incomparable_successful_architectures_in_frozen_bounded_scope"
    assert result["next_decisive_workstream"] == "IKD-W3-COMMON-FACTOR"
    assert "Three architectures satisfy" in doc
    assert "Partial preservation is not treated as success" in audit
    assert "expanded_competition_complete_three_incomparable_successful_architectures" in audit
    print("IKD-W2 expanded candidate competition: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
