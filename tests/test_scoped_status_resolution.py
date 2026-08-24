from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ScopedStatusResolutionTests(unittest.TestCase):
    def test_historical_conditional_theorems_remain_scoped(self):
        data = yaml.safe_load(text("theory/metadata/theorems.yaml"))["theorems"]
        by_id = {item["id"]: item for item in data}
        self.assertEqual(by_id["T-001"]["status"], "Established (Conditional)")
        self.assertIn("deletion-only reduction standard", by_id["T-001"]["scope"])
        self.assertEqual(by_id["T-002"]["status"], "Established (Conditional)")
        self.assertIn(
            "current Project FAR definitions and deletion-only reduction standard",
            by_id["T-002"]["scope"],
        )

        catalog = text("theory/theorems/theorems.md")
        self.assertIn("T-001 — Conditional Primitive Minimality", catalog)
        self.assertIn("Status: Established (Conditional).", catalog)
        self.assertIn("does not establish global minimality", catalog)
        self.assertIn("does not establish absolute independence", catalog)

    def test_historical_investigation_records_are_preserved(self):
        vi2 = text("research/validation/investigations/VI-002-primitive-minimality.md")
        vi3 = text("research/validation/investigations/VI-003-primitive-independence.md")
        self.assertRegex(vi2, r"## Status\n\nResearch")
        self.assertRegex(vi3, r"## Status\n\nResearch")
        self.assertIn("VI-003 remains incomplete", vi3)

    def test_old_open_question_path_is_explicitly_superseded(self):
        old = text("research/open-problems/open-questions.md")
        self.assertIn("Historical Open Questions Register (Superseded)", old)
        self.assertIn("Historical / superseded as current authority", old)
        self.assertIn("Global Primitive Minimality", old)
        self.assertIn("Closed: no nontrivial contract-free minimum exists", old)
        self.assertIn("Global Primitive Independence", old)
        self.assertIn("Closed at global contract-free scope", old)
        self.assertNotIn("**Status:** Active", old)
        self.assertNotIn("**Status:** Open", old)

    def test_canonical_summaries_follow_terminal_result(self):
        combined = (
            text("README.md")
            + "\n"
            + text("docs/project-status.md")
            + "\n"
            + text("frameworks/FARA/primitives.md")
        ).lower()
        self.assertIn(
            "nontrivial contract-free minimal architecture is impossible",
            combined,
        )
        self.assertIn("unique minimal observational quotient", combined)
        self.assertIn("schema or contract roles, not global primitives", combined)
        self.assertIn(
            "global primitive-independence and primitive-minimality search is closed",
            combined,
        )
        self.assertNotIn("global primitive minimality is established", combined)
        self.assertNotIn("global primitive independence is established", combined)
        self.assertIn("finite", combined)
        self.assertIn("universality", combined)

    def test_status_consistency_checker_has_no_scoped_primitive_contradiction(self):
        cp = subprocess.run(
            [sys.executable, "tools/check_status_consistency.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("Contradictions: 0", cp.stdout)

    def test_generated_theorem_metadata_current(self):
        cp = subprocess.run(
            [sys.executable, "tools/generate_theorem_index.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)


if __name__ == "__main__":
    unittest.main()
