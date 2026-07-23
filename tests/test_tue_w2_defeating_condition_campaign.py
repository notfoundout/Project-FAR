from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "theory/evaluation/tue-w2-defeating-condition-campaign-protocol-v1.0.json"
CORPUS = ROOT / "theory/evaluation/tue-w2-defeating-condition-campaign-corpus-v1.0.json"
RESULT = ROOT / "theory/evaluation/tue-w2-defeating-condition-campaign-result-v1.0.json"
QUEUE = ROOT / "theory/evaluation/tue-w2-queue-checkpoint-v1.0.json"
LIVE_QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"


class TUEW2DefeatingConditionCampaignTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_checker_passes(self) -> None:
        completed = subprocess.run([sys.executable, str(ROOT / "tools/check_tue_w2_defeating_condition_campaign.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_all_five_conditions_are_exact(self) -> None:
        ids = [item["id"] for item in self.load(PROTOCOL)["frozen_conditions"]]
        self.assertEqual(ids, ["DC-1-SIXTH-PRIMITIVE", "DC-2-RCCD-ESCAPE", "DC-3-CIRCULARITY", "DC-4-PLURAL-KERNEL", "DC-5-ABLATION"])

    def test_every_condition_has_attacks(self) -> None:
        protocol = self.load(PROTOCOL)
        cases = self.load(CORPUS)["cases"]
        expected = {item["id"] for item in protocol["frozen_conditions"]}
        self.assertEqual({item["condition"] for item in cases}, expected)
        self.assertGreaterEqual(len(cases), 20)

    def test_unknown_is_preserved(self) -> None:
        cases = self.load(CORPUS)["cases"]
        self.assertTrue(any(item["disposition"] == "unresolved" for item in cases))
        limits = self.load(RESULT)["remaining_limits"]
        self.assertTrue(any("principled inaccessibility boundary" in item for item in limits))

    def test_terminal_outcome_follows_five_results(self) -> None:
        result = self.load(RESULT)
        self.assertEqual(result["terminal_outcome"], "no_defeating_condition_established")
        self.assertEqual(len(result["condition_results"]), 5)
        self.assertTrue(all(item["result"] == "not_established" for item in result["condition_results"]))

    def test_queue_advances_only_to_279(self) -> None:
        queue = self.load(QUEUE)
        self.assertEqual([item["target_pr"] for item in queue["completed_workstreams"]], [276, 277, 278])
        self.assertEqual(queue["next_action"]["target_pr"], 279)
        self.assertEqual(queue["next_action"]["workstream"], "TUE-W3-DEEPER-KERNEL")
        self.assertEqual(queue["ordered_followups"], [280])

    def test_terminal_live_queue_is_closed(self) -> None:
        queue = self.load(LIVE_QUEUE)
        self.assertEqual(queue["status"], "complete")
        self.assertIsNone(queue["next_action"])
        self.assertEqual(queue["ordered_followups"], [])


if __name__ == "__main__":
    unittest.main()
