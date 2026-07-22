from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SCoreW5ReviewPackageTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run(
            [sys.executable, "tools/check_s_core_w5_review_package.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("review not executed", completed.stdout)

    def test_package_preserves_independence_boundary(self) -> None:
        registry = json.loads(
            (ROOT / "theory/evaluation/s-core-w5-independent-review-package-v1.0.json").read_text()
        )
        self.assertEqual(registry["independent_review_status"], "not_started")
        self.assertEqual(registry["replication_layer"], "none_review_not_executed")
        self.assertIn("independent_proof_verification", registry["unsupported_claims"])
        self.assertIn("universal_structure", registry["unsupported_claims"])

    def test_adversarial_review_is_mandatory(self) -> None:
        registry = json.loads(
            (ROOT / "theory/evaluation/s-core-w5-independent-review-package-v1.0.json").read_text()
        )
        attempts = set(registry["mandatory_adversarial_tests"])
        self.assertIn("construct_an_in_scope_counterexample", attempts)
        self.assertIn("identify_an_unstated_axiom", attempts)
        self.assertIn("compare_human_proof_with_Lean_statement", attempts)
        self.assertIn("attempt_strictly_simpler_equivalent_target", attempts)


if __name__ == "__main__":
    unittest.main()
