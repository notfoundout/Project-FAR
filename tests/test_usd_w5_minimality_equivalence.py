from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w5-minimality-equivalence-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w5_minimality_equivalence.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class MinimalityEquivalenceTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_candidate_universe_and_successful_set_are_frozen(self) -> None:
        contract = load(CONTRACT)
        self.assertEqual(
            set(contract["candidate_universe"]),
            {"FARA-001", "LTS-PROV-001", "GREL-001", "ARG-HIST-001"},
        )
        self.assertEqual(set(contract["successful_candidates"]), {"FARA-001", "LTS-PROV-001"})

    def test_two_distinct_minimal_classes_remain(self) -> None:
        result = load(RESULT)
        minima = {
            candidate
            for candidate, row in result["candidate_results"].items()
            if row["minimal_in_frozen_universe"]
        }
        self.assertEqual(minima, {"FARA-001", "LTS-PROV-001"})
        self.assertEqual(result["pareto_relations"]["FARA_vs_LTS_PROV"], "incomparable")
        self.assertEqual(result["translation_tests"]["round_trip_equivalence"], "fail")
        self.assertEqual(result["terminal_outcome"], "multiple_incomparable_minima")

    def test_dominated_candidates_are_not_minima(self) -> None:
        result = load(RESULT)
        self.assertFalse(result["candidate_results"]["GREL-001"]["minimal_in_frozen_universe"])
        self.assertFalse(result["candidate_results"]["ARG-HIST-001"]["minimal_in_frozen_universe"])
        self.assertIn("FARA-001", result["candidate_results"]["ARG-HIST-001"]["dominated_by"])

    def test_shortcuts_and_broad_claims_remain_blocked(self) -> None:
        result = load(RESULT)
        self.assertTrue(all(value == "rejected" for value in result["negative_control_results"].values()))
        self.assertEqual(result["claim_effect"]["unique_minimum"], "refuted_in_frozen_candidate_universe")
        self.assertEqual(result["claim_effect"]["global_minimality"], "unresolved")
        self.assertEqual(result["claim_effect"]["universal_structure"], "unresolved")
        self.assertEqual(result["independent_review_status"], "not_started")


if __name__ == "__main__":
    unittest.main()
