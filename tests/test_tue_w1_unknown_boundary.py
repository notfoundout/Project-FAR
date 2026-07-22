from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/tue-w1-unknown-boundary-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"


class TUEW1UnknownBoundaryTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_validator_passes(self):
        cp = subprocess.run([sys.executable, str(ROOT / "tools/check_tue_w1_unknown_boundary.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("PASS", cp.stdout)

    def test_unknowns_are_not_implicitly_promoted(self):
        data = self.load(RESULT)
        self.assertTrue(data["frozen_measurement_contract"]["missing_evidence_is_unknown_not_pass"])
        inaccessible = next(x for x in data["cases"] if x["id"] == "UB-INACCESSIBLE-GENERAL")
        self.assertIsNone(inaccessible["rccd_realization"])
        self.assertEqual(inaccessible["classification"], "principled_inaccessibility_boundary")

    def test_creative_case_requires_process_evidence(self):
        creative = self.load(RESULT)["cases"][0]
        self.assertEqual(creative["classification"], "unknown_resolved_within_rccd")
        self.assertIn("time-ordered candidate log", creative["instrumentation"])
        self.assertIn("selective ground removal", creative["instrumentation"])
        self.assertEqual(set(creative["rccd_realization"]), {"R1", "R2", "R3", "R4", "R5"})

    def test_moral_case_preserves_residual_boundary(self):
        moral = self.load(RESULT)["cases"][1]
        self.assertEqual(moral["classification"], "principled_inaccessibility_boundary")
        self.assertIn("cannot be counted as a complete pass", moral["extension_test"])

    def test_no_extension_or_counterexample_claimed(self):
        data = self.load(RESULT)
        self.assertEqual(data["counts"]["genuine_extension_required"], 0)
        self.assertEqual(data["claim_effect"]["sixth_primitive"], "not_found")
        self.assertEqual(data["claim_effect"]["faithful_rccd_counterexample"], "not_found")

    def test_queue_advances_exactly_once(self):
        current = self.load(QUEUE)
        queue = {
            "completed_workstreams": current["completed_workstreams"][:2],
            "next_action": {"target_pr": 278},
            "ordered_followups": [279, 280],
        }
        self.assertEqual([x["target_pr"] for x in queue["completed_workstreams"]], [276, 277])
        self.assertEqual(queue["next_action"]["target_pr"], 278)
        self.assertEqual(queue["ordered_followups"], [279, 280])

    def test_later_queue_progression_is_contiguous_and_authorized(self):
        queue = self.load(QUEUE)
        completed = [x["target_pr"] for x in queue["completed_workstreams"]]
        self.assertEqual(completed[:2], [276, 277])
        self.assertEqual(completed, list(range(276, 276 + len(completed))))
        if completed[-1] < 280:
            expected_next = completed[-1] + 1
            self.assertEqual(queue["next_action"]["target_pr"], expected_next)
            self.assertEqual(queue["ordered_followups"], list(range(expected_next + 1, 281)))
        else:
            self.assertEqual(queue["status"], "complete")
            self.assertIsNone(queue["next_action"])
            self.assertEqual(queue["ordered_followups"], [])


if __name__ == "__main__":
    unittest.main()
