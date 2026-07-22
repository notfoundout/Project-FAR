from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-v1.0.json"
QUEUE = ROOT / "theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json"


class PostSCTerminalUniversalityExtensionTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_validator_passes(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_post_sc_terminal_universality_extension.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_program_registration_remains_frozen(self) -> None:
        program = self.load(PROGRAM)
        self.assertEqual(program["program_id"], "POST-SC-TUE-001")
        self.assertEqual(program["status"], "registered_unexecuted")
        self.assertEqual(program["registration_pr"], 276)
        self.assertEqual(program["parent_adjudication"], "SC-W6-FINAL-INTERNAL-ADJUDICATION-001")

    def test_sequence_is_exactly_277_through_280(self) -> None:
        workstreams = self.load(PROGRAM)["workstreams"]
        self.assertEqual([item["target_pr"] for item in workstreams], [277, 278, 279, 280])
        self.assertEqual([item["sequence"] for item in workstreams], [1, 2, 3, 4])

    def test_current_queue_is_contiguous_and_authorized(self) -> None:
        queue = self.load(QUEUE)
        completed = [item["target_pr"] for item in queue["completed_workstreams"]]
        self.assertEqual(completed, list(range(276, 276 + len(completed))))
        if queue["status"] == "complete":
            self.assertEqual(completed, [276, 277, 278, 279, 280])
            self.assertIsNone(queue["next_action"])
            self.assertEqual(queue["ordered_followups"], [])
        else:
            expected_next = completed[-1] + 1
            self.assertEqual(queue["next_action"]["target_pr"], expected_next)
            self.assertEqual(queue["ordered_followups"], list(range(expected_next + 1, 281)))

    def test_all_defeating_conditions_are_frozen(self) -> None:
        program = self.load(PROGRAM)
        self.assertEqual(len(program["frozen_sc_w6_defeating_conditions"]), 5)
        self.assertIn("A genuine counterexample or extension overrides accumulated supportive mappings.", program["decision_rules"])

    def test_terminal_outcomes_do_not_force_confirmation(self) -> None:
        outcomes = set(self.load(PROGRAM)["workstreams"][-1]["terminal_outcomes"])
        self.assertEqual(outcomes, {
            "maximal_effective_rccd_universality",
            "rccd_requires_extension_or_plural_kernel",
            "unrestricted_question_evidentially_underdetermined",
        })

    def test_hard_stop_and_external_deferral(self) -> None:
        program = self.load(PROGRAM)
        queue = self.load(QUEUE)
        self.assertEqual(program["hard_stopping_rule"]["terminal_pr"], 280)
        self.assertEqual(program["hard_stopping_rule"]["external_review_disposition"], "deferred_until_pr_280_final_answer")
        self.assertIn("external proof review before PR 280", queue["blocked_actions"])
        self.assertIn("insert additional supportive workstreams", queue["blocked_actions"])


if __name__ == "__main__":
    unittest.main()
