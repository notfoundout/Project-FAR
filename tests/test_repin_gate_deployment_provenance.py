from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "far_validation" / "repin_gate_workflow.yml"


class RepinGateDeploymentProvenanceTests(unittest.TestCase):
    """The separate gate must execute both modes from one immutable Project-FAR checkout."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_checkout_is_bound_to_far_deployed_commit(self) -> None:
        self.assertIn("FAR_DEPLOYED_COMMIT: REPLACE_WITH_40_HEX_MAIN_COMMIT", self.text)
        self.assertIn('"$FAR_DEPLOYED_COMMIT"', self.text)
        self.assertIn(
            'test "$(git -C deploy rev-parse HEAD)" = "$FAR_DEPLOYED_COMMIT"',
            self.text,
        )

    def test_audit_executes_the_audit_from_that_checkout(self) -> None:
        self.assertIn(
            "python3 deploy/far_validation/repin_protection_audit.py",
            self.text,
        )
        self.assertNotIn("repin_protection_audit.py --bootstrap", self.text)

    def test_evaluate_executes_the_gate_from_the_same_checkout(self) -> None:
        self.assertIn(
            "python3 deploy/far_validation/repin_gate_app.py actions --mode evaluate",
            self.text,
        )

    def test_neither_mode_executes_project_far_candidate_paths(self) -> None:
        self.assertNotIn("python3 far_validation/repin_protection_audit.py", self.text)
        self.assertNotIn("python3 far_validation/repin_gate_app.py actions", self.text)


if __name__ == "__main__":
    unittest.main()
