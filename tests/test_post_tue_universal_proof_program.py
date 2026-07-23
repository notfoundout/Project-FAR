from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "theory/evaluation/post-tue-universal-proof-program-v1.0.json"


class UniversalProofProgramTests(unittest.TestCase):
    def load(self) -> dict:
        return json.loads(PROGRAM.read_text(encoding="utf-8"))

    def test_checker_passes(self) -> None:
        cp = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_post_tue_universal_proof_program.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("PASS", cp.stdout)

    def test_pr_280_is_evidence_not_proof(self) -> None:
        checkpoint = self.load()["starting_checkpoint"]
        self.assertEqual(checkpoint["source_pr"], 280)
        self.assertEqual(
            checkpoint["classification"],
            "terminal_finite_internal_adjudication_evidence_not_universal_proof",
        )

    def test_program_is_outcome_neutral(self) -> None:
        outcomes = set(self.load()["terminal_outcomes"])
        self.assertEqual(
            outcomes,
            {
                "full_registered_universal_theorem_proved",
                "strictly_weakened_universal_theorem_proved",
                "rccd_requires_extension_or_revision",
                "rccd_universality_defeated",
                "proof_blocked_by_indispensable_unproved_assumption",
            },
        )

    def test_release_gate_is_closed(self) -> None:
        gate = self.load()["release_gate"]
        self.assertFalse(gate["public_evaluation_authorized"])
        self.assertIn("UPP-W15", gate["authorization_condition"])

    def test_queue_advances_to_foundation(self) -> None:
        data = self.load()
        self.assertEqual(data["next_action"], {"target_pr": 282, "workstream": "UPP-W1-FOUNDATION"})
        self.assertEqual(data["ordered_followups"], list(range(283, 297)))


if __name__ == "__main__":
    unittest.main()
