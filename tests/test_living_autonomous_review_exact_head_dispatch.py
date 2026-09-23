from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AutonomousReviewExactHeadDispatchTests(unittest.TestCase):
    def test_exact_head_supports_explicit_trusted_dispatch(self):
        workflow = (ROOT / ".github/workflows/exact-head-assurance.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("head_sha:", workflow)
        self.assertIn("base_sha:", workflow)
        self.assertIn("FAR_ASSURANCE_DISPATCH_HEAD", workflow)
        self.assertIn("FAR_ASSURANCE_DISPATCH_BASE", workflow)
        self.assertIn("FAR_ASSURANCE_DISPATCH_WORKFLOW_SHA", workflow)
        self.assertIn("invalid dispatched exact-head SHA", workflow)
        self.assertIn("dispatched exact-head checkout mismatch", workflow)
        self.assertIn("dispatched exact-head base differs from trusted main workflow ref", workflow)
        self.assertIn("dispatched exact-head review head is not a direct child of frozen main", workflow)
        self.assertIn("git merge-base --is-ancestor", workflow)

        preflight = workflow.index("- name: Validate dispatched identity before checkout")
        checkout = workflow.index("- uses: actions/checkout@v4")
        lineage = workflow.index("- name: Verify dispatched checkout lineage before repository code runs")
        setup = workflow.index("- uses: actions/setup-python@v5")
        install = workflow.index("- name: Install dependencies and trace backend")
        self.assertLess(preflight, checkout)
        self.assertLess(checkout, lineage)
        self.assertLess(lineage, setup)
        self.assertLess(setup, install)

    def test_autonomous_review_dispatches_exact_head_from_protected_main(self):
        workflow = (ROOT / ".github/workflows/living-autonomous-review-v2.yml").read_text(encoding="utf-8")
        expected = (
            'gh workflow run exact-head-assurance.yml --repo "$GITHUB_REPOSITORY" --ref main '
            '\\\n            -f head_sha="$head_sha" -f base_sha="$base_sha"'
        )
        self.assertIn(expected, workflow)
        self.assertNotIn(
            'gh workflow run exact-head-assurance.yml --repo "$GITHUB_REPOSITORY" --ref "$branch"',
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
