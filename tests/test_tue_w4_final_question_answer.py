from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/tue-w4-final-question-answer-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"


class TUEW4FinalQuestionAnswerTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_checker_passes(self) -> None:
        cp = subprocess.run([sys.executable, str(ROOT / "tools/check_tue_w4_final_question_answer.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("PASS", cp.stdout)

    def test_terminal_outcome_and_scope(self) -> None:
        result = self.load(RESULT)
        self.assertEqual(result["terminal_outcome"], "maximal_effective_rccd_universality")
        self.assertIn("maximal internally adjudicable", result["answer"])
        self.assertEqual(len(result["defeating_conditions_preserved"]), 5)

    def test_unknown_not_promoted(self) -> None:
        boundary = self.load(RESULT)["evidential_boundary"]
        self.assertIn("neither support nor defeat", boundary["inaccessible_processes"])
        self.assertIn("underdetermined", boundary["consequence"])

    def test_queue_is_terminal(self) -> None:
        queue = self.load(QUEUE)
        self.assertEqual(queue["status"], "complete")
        self.assertIsNone(queue["next_action"])
        self.assertEqual(queue["ordered_followups"], [])
        self.assertEqual([x["target_pr"] for x in queue["completed_workstreams"]], [276, 277, 278, 279, 280])

    def test_nonclaims_preserved(self) -> None:
        nonclaims = set(self.load(RESULT)["nonclaims"])
        self.assertIn("metaphysical fundamentality beneath every ontology", nonclaims)
        self.assertIn("actual cognitive, computational, or physical process correspondence", nonclaims)
        self.assertIn("external validation or independent replication", nonclaims)


if __name__ == "__main__":
    unittest.main()
