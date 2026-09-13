from __future__ import annotations

import unittest
from pathlib import Path

from tools.run_living_research_implementation import expected_sealed_rows

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools/run_living_research_implementation.py"


class LivingResearchImplementationRunnerTests(unittest.TestCase):
    def test_expected_seal_rows_are_derived_only_from_protected_plan(self) -> None:
        plan = {
            "proposals": [
                {
                    "proposal_id": "FAR-LIVING-IMPL-ONE",
                    "operations": [
                        {"path": "tools/b.py", "result_sha256": "b" * 64},
                        {"path": "tools/a.py", "result_sha256": "a" * 64},
                    ],
                }
            ]
        }
        self.assertEqual(
            [
                {"path": "tools/a.py", "sha256": "a" * 64, "proposal_id": "FAR-LIVING-IMPL-ONE"},
                {"path": "tools/b.py", "sha256": "b" * 64, "proposal_id": "FAR-LIVING-IMPL-ONE"},
            ],
            expected_sealed_rows(plan),
        )

    def test_recovery_verifier_binds_manifest_to_plan_and_single_commit(self) -> None:
        text = RUNNER.read_text(encoding="utf-8")
        self.assertIn('manifest.get("proposals") != plan["proposals"]', text)
        self.assertIn('manifest.get("sealed_files") != expected_rows', text)
        self.assertIn('git("rev-list", "--parents", "-n", "1", head)', text)
        self.assertIn('git("rev-list", "--count", f"{plan[\'base_main_sha\']}..{head}")', text)
        self.assertIn('head = verify_existing(branch, plan)', text)


if __name__ == "__main__":
    unittest.main()
