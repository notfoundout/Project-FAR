from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude" / "skills" / "far-clean-room-auditor" / "SKILL.md"
ORCHESTRATOR = ROOT / ".claude" / "skills" / "far-research-orchestrator" / "SKILL.md"


class CleanRoomAuditorSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.orchestrator = ORCHESTRATOR.read_text(encoding="utf-8")

    def test_frontmatter_and_repository_routing(self):
        self.assertRegex(self.skill, r"(?m)^name: far-clean-room-auditor$")
        self.assertIn("AGENTS.md", self.skill)
        self.assertIn("docs/governance/research-execution-charter.md", self.skill)
        self.assertIn("docs/project-status.md", self.skill)
        self.assertIn("docs/CANONICAL_MAP.md", self.skill)
        self.assertIn("far-canonical-source-resolver", self.skill)

    def test_core_evidence_first_invariants_are_persistent(self):
        required = (
            "Search before concluding",
            "Resolve controlling authority by role",
            "Freeze the exact claim before testing",
            "Atomize composite claims",
            "Separate premise types",
            "Keep evidence distinct from inference",
            "Actively seek failure",
            "Treat absence as bounded",
            "Track provenance and lineage",
            "Never upgrade uncertainty",
            "Require proof closure",
            "Preserve conflicts",
            "typed verdict",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill)

    def test_premise_and_verdict_vocabularies_are_explicit(self):
        for premise_type in (
            "EVIDENCE",
            "DEFINITION/CONSTRAINT",
            "ASSUMPTION",
            "DERIVATION",
            "INFERENCE",
        ):
            self.assertIn(f"`{premise_type}`", self.skill)

        for verdict in (
            "VERIFIED",
            "SUPPORTED",
            "FALSIFIED",
            "OPEN",
            "BLOCKED",
            "UNDERDETERMINED",
            "NOT APPLICABLE",
        ):
            self.assertRegex(self.skill, rf"(?m)^- \*\*{re.escape(verdict)}\*\*")

    def test_overclaim_guards_cover_project_relevant_promotions(self):
        guards = (
            "bounded result -> universal result",
            "internal result -> external result",
            "successful execution -> theoretical proof",
            "formal proof -> empirical utility",
            "replication -> independence",
            "schema validity -> semantic correctness",
            "repository placement -> authority",
            "finite corpus performance -> population performance",
        )
        for guard in guards:
            with self.subTest(guard=guard):
                self.assertIn(guard, self.skill)

    def test_research_orchestrator_routes_independent_audit_here(self):
        self.assertIn("far-clean-room-auditor", self.orchestrator)
        self.assertIn("far-theory-auditor", self.orchestrator)


if __name__ == "__main__":
    unittest.main()
