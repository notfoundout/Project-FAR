import copy
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_current_state_consistency as checker


EXPECTED_RELEASE = "v1.0.0"
PROGRAM_ID = "POST-CLOSURE-001"
NEXT_WORKSTREAM = "PCA-W1-INDEPENDENT-REVIEW"

VALID_TEXTS = {
    "readme": (
        "## Latest release: v1.0.0\n"
        "`PROJECT-FAR-CORE-THEORY-1.1`\n"
        "Historical v1.0\n"
        "## Post-closure phase\n"
    ),
    "status": (
        "Current published repository release: [`v1.0.0`]\n"
        "Current governing theory: `PROJECT-FAR-CORE-THEORY-1.1`.\n"
        "Current program: `POST-CLOSURE-001`\n"
        "| `PCA-W1-INDEPENDENT-REVIEW` | **Next / Open** | boundary |\n"
    ),
    "map": (
        "Project FAR Core Theory v1.1\n"
        "Historical Project FAR Core Theory v1.0\n"
        "Post-Closure Assurance and Application Program\n"
        "Current Project FAR release: [`releases/project-far-v1.0.0.md`](releases/project-far-v1.0.0.md)\n"
    ),
    "roadmap": (
        "Current published repository release: [`v1.0.0`]\n"
        "Current governing core: [`PROJECT-FAR-CORE-THEORY-1.1`]\n"
        "Current program: [`POST-CLOSURE-001`]\n"
        "`PCA-W1-INDEPENDENT-REVIEW` — next\n"
    ),
    "generated": (
        "# Historical Bounded-Program Status (Generated)\n"
        "not a current project-status authority\n"
    ),
    "next_actions": (
        "Program: `POST-CLOSURE-001`.\n"
        "Current review target: `PROJECT-FAR-CORE-THEORY-1.1`.\n"
        "Historical v1.0 Core\n"
        "Canonical next workstream: `PCA-W1-INDEPENDENT-REVIEW`.\n"
    ),
    "agents": (
        "If purported current-authority surfaces conflict, stop. "
        "Treat project memory as navigation only. "
        "Treat repository presence as evidence that an artifact exists, "
        "not that its contents are Accepted.\n"
    ),
}


class CurrentStateConsistencyTests(unittest.TestCase):
    def validate(self, texts):
        return checker.validate_texts(
            texts, EXPECTED_RELEASE, PROGRAM_ID, NEXT_WORKSTREAM
        )

    def test_consistent_state_passes(self):
        self.assertEqual([], self.validate(copy.deepcopy(VALID_TEXTS)))

    def test_stale_current_release_is_rejected(self):
        texts = copy.deepcopy(VALID_TEXTS)
        texts["roadmap"] += "v0.4.0 is the current release baseline\n"
        errors = self.validate(texts)
        self.assertTrue(any("stale current-state assertion" in error for error in errors))

    def test_historical_generated_report_cannot_claim_current_mode(self):
        texts = copy.deepcopy(VALID_TEXTS)
        texts["generated"] += "## Current Research Mode\n"
        errors = self.validate(texts)
        self.assertTrue(any("Current Research Mode" in error for error in errors))

    def test_next_actions_must_follow_registered_next_workstream(self):
        texts = copy.deepcopy(VALID_TEXTS)
        texts["next_actions"] = (
            "Program: `POST-CLOSURE-001`.\n"
            "Current review target: `PROJECT-FAR-CORE-THEORY-1.1`.\n"
            "Historical v1.0 Core\n"
            "Canonical next workstream: `PCA-W2-PROOF-ASSISTANT-FORMALIZATION`.\n"
        )
        errors = self.validate(texts)
        self.assertTrue(any("next-actions workstream drifted" in error for error in errors))

    def test_superseded_upp_queue_cannot_return(self):
        texts = copy.deepcopy(VALID_TEXTS)
        texts["next_actions"] += "PTE-W1-INDEPENDENT-REVIEW\n"
        errors = self.validate(texts)
        self.assertTrue(any("superseded UPP evaluation planning" in error for error in errors))

    def test_agent_routing_must_subordinate_memory(self):
        texts = copy.deepcopy(VALID_TEXTS)
        texts["agents"] = (
            "If purported current-authority surfaces conflict, stop. "
            "Treat repository presence as evidence that an artifact exists, "
            "not that its contents are Accepted.\n"
        )
        errors = self.validate(texts)
        self.assertTrue(any("subordinate memory" in error for error in errors))

    def test_historical_v1_0_cannot_be_repromoted_as_current(self):
        texts = copy.deepcopy(VALID_TEXTS)
        texts["status"] += "Current governing theory: `PROJECT-FAR-CORE-THEORY-1.0`\n"
        errors = self.validate(texts)
        self.assertTrue(any("stale current-state assertion" in error for error in errors))

    def test_program_identity_parses_registered_next_workstream(self):
        program = (
            "Program: `POST-CLOSURE-001`\n\n"
            "- `PCA-W0-REPOSITORY-CONFORMITY`: complete.\n"
            "- `PCA-W1-INDEPENDENT-REVIEW`: **open — next**. Review target is `PROJECT-FAR-CORE-THEORY-1.1`.\n"
        )
        self.assertEqual(
            (PROGRAM_ID, NEXT_WORKSTREAM), checker.program_identity(program)
        )


if __name__ == "__main__":
    unittest.main()
