from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/ikd-w2-expanded-candidate-competition-v1.0.json"


class IKDW2ExpandedCandidateCompetitionTests(unittest.TestCase):
    def load(self) -> dict:
        return json.loads(RESULT.read_text(encoding="utf-8"))

    def test_validator_passes(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_ikd_w2_expanded_candidate_competition.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_successful_frontier_is_exact(self):
        result = self.load()
        self.assertEqual(set(result["successful_set"]), {"FARA-001", "LTS-PROV-001", "COALG-DYN-001"})
        self.assertTrue(all(relation[2] == "incomparable" for relation in result["frontier_relations"]))

    def test_all_frozen_new_candidates_are_evaluated(self):
        result = self.load()
        expected = {"PROC-CAT-001", "CAUSAL-SCM-001", "PROOF-TYPE-001", "INFO-FLOW-001", "COALG-DYN-001", "ALG-REWRITE-001"}
        self.assertTrue(expected <= set(result["candidate_results"]))

    def test_partial_candidates_retain_boundaries(self):
        result = self.load()
        for candidate, record in result["candidate_results"].items():
            if record["coverage"] == "partial":
                self.assertEqual(record["preservation"], "partial")
                self.assertTrue(record["boundary"])

    def test_no_scalar_winner(self):
        result = self.load()
        self.assertEqual(result["aggregation"], "pareto_only_no_scalar_score")
        self.assertIsNone(result["winner"])

    def test_claim_boundaries_remain(self):
        result = self.load()
        nonclaims = set(result["nonclaims"])
        self.assertIn("candidate exhaustiveness", nonclaims)
        self.assertIn("universal structure", nonclaims)
        self.assertIn("global no-go", nonclaims)


if __name__ == "__main__":
    unittest.main()
