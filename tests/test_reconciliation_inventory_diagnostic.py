"""Temporary exhaustive diagnostic for merged-review reconciliation work."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs/audits/merged-pr-review-classification/findings.json"
DECISIONS = ROOT / "docs/audits/merged-pr-review-reconciliation/reconciliation-decisions.json"


class ReconciliationInventoryDiagnostic(unittest.TestCase):
    def test_print_undispositioned_findings(self) -> None:
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))
        explicit = {item["finding_id"] for item in decisions["decisions"]}
        source = [item for item in baseline["findings"]
                  if item.get("disposition") == "resolved_incorrectly"
                  and item["finding_id"] not in explicit]
        self.assertEqual(len({item["finding_id"] for item in source}), len(source))
        print("RECONCILIATION_UNDISPOSITIONED_BEGIN")
        for item in source:
            claim = " ".join(str(item.get("reviewer_claim", "")).split())
            print(json.dumps({"id": item["finding_id"], "risk": item.get("risk"),
                              "path": item.get("path"), "line": item.get("line"),
                              "claim": claim[:360]}, sort_keys=True))
        print("RECONCILIATION_UNDISPOSITIONED_END")


if __name__ == "__main__":
    unittest.main()
