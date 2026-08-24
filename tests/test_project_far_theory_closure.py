from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/check_project_far_theory_closure.py"
SPEC = importlib.util.spec_from_file_location("project_far_theory_closure_check", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ProjectFARTheoryClosureTest(unittest.TestCase):
    def test_repository_conforms_to_terminal_theory(self):
        self.assertEqual([], MODULE.validate())

    def test_exact_claim_set_is_closed(self):
        ledger = MODULE._load(ROOT / "theory/terminal/project-far-core-theory-v1.0.json")
        self.assertEqual(
            {f"FAR-CORE-{i:03d}" for i in range(1, 15)},
            {row["id"] for row in ledger["claims"]},
        )

    def test_historical_upp_is_not_current_authority(self):
        old = MODULE._load(ROOT / "theory/evaluation/post-terminal-public-evaluation-program-v1.0.json")
        self.assertEqual("superseded", old["status"])
        self.assertEqual("POST-CLOSURE-001", old["superseded_by"])


if __name__ == "__main__":
    unittest.main()
