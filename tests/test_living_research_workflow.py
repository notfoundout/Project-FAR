from __future__ import annotations

import unittest
from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/living-research.yml"


def step_block(text: str, name: str) -> str:
    marker = f"      - name: {name}\n"
    start = text.index(marker)
    end = text.find("\n      - name: ", start + len(marker))
    return text[start:] if end == -1 else text[start:end]


class LivingResearchWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_post_push_governance_surfaces_run_independently(self):
        rolling = step_block(self.text, "Create or refresh rolling research PR")
        queue = step_block(self.text, "Maintain core-claim review queue issue")
        validation = step_block(self.text, "Dispatch explicit validation for automated head")

        self.assertIn("id: rolling_pr", rolling)
        self.assertIn("continue-on-error: true", rolling)

        self.assertIn("id: review_queue", queue)
        self.assertIn("if: always() && steps.push.outputs.changed == 'true'", queue)
        self.assertIn("continue-on-error: true", queue)

        self.assertIn("id: validation_dispatch", validation)
        self.assertIn("if: always() && steps.push.outputs.changed == 'true'", validation)
        self.assertIn("continue-on-error: true", validation)

    def test_terminal_guard_fails_after_preserving_results(self):
        guard = step_block(self.text, "Fail if required post-push governance surfaces failed")

        self.assertIn("if: always() && steps.push.outputs.changed == 'true'", guard)
        self.assertIn("ROLLING_PR_OUTCOME: ${{ steps.rolling_pr.outcome }}", guard)
        self.assertIn("REVIEW_QUEUE_OUTCOME: ${{ steps.review_queue.outcome }}", guard)
        self.assertIn("VALIDATION_DISPATCH_OUTCOME: ${{ steps.validation_dispatch.outcome }}", guard)
        self.assertIn("Research data was preserved", guard)
        self.assertIn("exit 1", guard)

        self.assertLess(
            self.text.index("- name: Create or refresh rolling research PR"),
            self.text.index("- name: Maintain core-claim review queue issue"),
        )
        self.assertLess(
            self.text.index("- name: Maintain core-claim review queue issue"),
            self.text.index("- name: Dispatch explicit validation for automated head"),
        )
        self.assertLess(
            self.text.index("- name: Dispatch explicit validation for automated head"),
            self.text.index("- name: Fail if required post-push governance surfaces failed"),
        )


if __name__ == "__main__":
    unittest.main()
