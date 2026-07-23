from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "theory/evaluation/tue-w3-deeper-kernel-protocol-v1.0.json"
CANDIDATES = ROOT / "theory/evaluation/tue-w3-deeper-kernel-candidates-v1.0.json"
RESULT = ROOT / "theory/evaluation/tue-w3-deeper-kernel-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"


class TUEW3DeeperKernelTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_checker_passes(self) -> None:
        cp = subprocess.run([sys.executable, str(ROOT / "tools/check_tue_w3_deeper_kernel.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("PASS", cp.stdout)

    def test_strict_reduction_standard_is_not_label_counting(self) -> None:
        protocol = self.load(PROTOCOL)
        self.assertIn("the substrate is non-vacuous and excludes at least one non-reasoning structure", protocol["success_conditions"])
        self.assertIn("the substrate is merely a conjunction or renaming of R1-R5", protocol["failure_conditions"])

    def test_candidate_search_includes_rejections_compressions_and_vacuity(self) -> None:
        results = {x["result"] for x in self.load(CANDIDATES)["candidates"]}
        self.assertTrue({"rejected", "rccd_equivalent_compression", "vacuous"}.issubset(results))

    def test_all_components_are_adjudicated(self) -> None:
        components = self.load(RESULT)["component_results"]
        self.assertEqual([x["component"] for x in components], ["R1", "R2", "R3", "R4", "R5"])

    def test_terminal_outcome_is_registered_level_only(self) -> None:
        result = self.load(RESULT)
        self.assertEqual(result["terminal_outcome"], "rccd_irreducible_at_registered_level")
        self.assertIn("registered-level irreducibility is not metaphysical fundamentality", result["remaining_limits"])

    def test_queue_advances_exactly_to_terminal_pr(self) -> None:
        queue = self.load(QUEUE)
        self.assertEqual([x["target_pr"] for x in queue["completed_workstreams"]], [276, 277, 278, 279])
        self.assertEqual(queue["next_action"]["target_pr"], 280)
        self.assertEqual(queue["ordered_followups"], [])


if __name__ == "__main__":
    unittest.main()
