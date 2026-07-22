from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "theory/evaluation/post-usd-internal-discovery-continuation-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json"


class PostUSDInternalDiscoveryContinuationTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_validator_passes(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_post_usd_internal_discovery_continuation.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_external_packages_are_preserved_but_deferred(self):
        program = self.load(PROGRAM)
        disposition = program["external_package_disposition"]
        for key in (
            "EVC-W1-EXTERNAL-PROOF-REVIEW",
            "EVC-W2-R3-TECHNICAL-REPLICATION",
            "EVC-W3-R4-ADVERSARIAL-REPLICATION",
        ):
            self.assertEqual(disposition[key], "frozen_preserved_execution_deferred")
        self.assertIn("not withdrawn", disposition["rule"])

    def test_execution_order_is_complete_and_contiguous(self):
        program = self.load(PROGRAM)
        streams = program["workstreams"]
        self.assertEqual([item["sequence"] for item in streams], list(range(1, 10)))
        self.assertEqual([item["target_pr"] for item in streams], list(range(260, 269)))
        self.assertEqual(streams[-1]["id"], "IKD-W9-TERMINAL-ADJUDICATION")

    def test_no_premature_universal_or_external_claim(self):
        program = self.load(PROGRAM)
        nonclaims = set(program["nonclaims"])
        self.assertIn("a universal structure has been discovered", nonclaims)
        self.assertIn("existing external packages have been executed", nonclaims)
        self.assertIn("failure to find a common kernel proves global nonexistence", nonclaims)

    def test_next_action_is_candidate_architecture_freeze(self):
        queue = self.load(QUEUE)
        self.assertEqual(queue["next_action"]["target_pr"], 260)
        self.assertEqual(queue["next_action"]["workstream"], "IKD-W1-CANDIDATE-ARCHITECTURES")
        self.assertIn("anti-derivative and hidden-reconstruction tests", queue["next_action"]["deliverables"])

    def test_terminal_outcomes_include_positive_negative_and_unresolved(self):
        program = self.load(PROGRAM)
        outcomes = set(program["terminal_outcomes"])
        self.assertIn("one_nontrivial_common_kernel", outcomes)
        self.assertIn("bounded_no_single_kernel", outcomes)
        self.assertIn("unresolved", outcomes)


if __name__ == "__main__":
    unittest.main()
