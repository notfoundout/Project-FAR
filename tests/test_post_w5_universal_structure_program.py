from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/post-w5-universal-structure-program-v1.0.json"
CHECKER = ROOT / "tools/check_post_w5_universal_structure_program.py"


class PostW5UniversalStructureProgramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_checker_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("program: valid", result.stdout)

    def test_representation_does_not_promote_universal_structure(self) -> None:
        bounded = self.data["representation_result_input"]
        self.assertEqual(bounded["scope"], "S_core")
        self.assertEqual(bounded["logical_effect_on_usd"], "none")
        self.assertIn(
            "The W5 representation theorem advances USD by logical implication",
            self.data["nonclaims"],
        )

    def test_program_preserves_competing_terminal_hypotheses(self) -> None:
        hypotheses = {item["id"]: item for item in self.data["frozen_hypotheses"]}
        self.assertEqual(hypotheses["USD-H-EXIST"]["status"], "unresolved")
        self.assertEqual(hypotheses["USD-H-NO"]["status"], "unresolved")

    def test_scope_extension_is_featurewise(self) -> None:
        workstream = next(
            item for item in self.data["workstreams"] if item["id"] == "USD-W1-SCOPE-EXT"
        )
        self.assertGreaterEqual(len(workstream["feature_families"]), 7)
        self.assertIn("partial_observability", workstream["feature_families"])
        self.assertIn("countermodel", workstream["terminal_outcomes"])

    def test_alternative_vocabulary_program_is_not_fara_only(self) -> None:
        workstream = next(
            item for item in self.data["workstreams"] if item["id"] == "USD-W2-ALT-VOCAB"
        )
        competition = workstream["minimum_competition"]
        self.assertGreaterEqual(competition["independently_motivated_non_fara_candidates"], 2)
        self.assertEqual(workstream["aggregation_rule"], "pareto_only_no_scalar_overall_winner")

    def test_no_workstream_is_reported_executed(self) -> None:
        self.assertTrue(
            all(item["status"] == "registered_unexecuted" for item in self.data["workstreams"])
        )


if __name__ == "__main__":
    unittest.main()
