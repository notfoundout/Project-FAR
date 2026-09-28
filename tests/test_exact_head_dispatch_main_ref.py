"""A dispatched exact-head review must execute the trusted workflow from main, not an arbitrary ref."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "exact-head-assurance.yml"


class ExactHeadDispatchMainRefTests(unittest.TestCase):
    def test_preflight_rejects_non_main_workflow_ref(self) -> None:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        step = next(
            item for item in workflow["jobs"]["exact-head-assurance"]["steps"]
            if item.get("name") == "Validate dispatched identity before checkout"
        )
        self.assertEqual(step["env"]["FAR_ASSURANCE_DISPATCH_REF"], "${{ github.ref }}")
        self.assertIn('[[ "$FAR_ASSURANCE_DISPATCH_REF" == "refs/heads/main" ]]', step["run"])
        with tempfile.TemporaryDirectory() as directory:
            base = "a" * 40
            common = dict(
                os.environ,
                FAR_ASSURANCE_DISPATCH_BASE=base,
                FAR_ASSURANCE_DISPATCH_HEAD="b" * 40,
                FAR_ASSURANCE_DISPATCH_WORKFLOW_SHA=base,
            )
            bad = subprocess.run(
                ["bash", "-c", step["run"]],
                env={**common, "FAR_ASSURANCE_DISPATCH_REF": "refs/heads/attacker"},
                cwd=directory,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(bad.returncode, 0)
            good = subprocess.run(
                ["bash", "-c", step["run"]],
                env={**common, "FAR_ASSURANCE_DISPATCH_REF": "refs/heads/main"},
                cwd=directory,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(good.returncode, 0, good.stderr)


if __name__ == "__main__":
    unittest.main()
