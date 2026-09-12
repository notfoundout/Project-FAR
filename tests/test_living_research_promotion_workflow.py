from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
WORKFLOW=ROOT/".github/workflows/living-research-promotion.yml"
RUNNER=ROOT/"tools/run_living_research_promotion.py"
README=ROOT/"research/living/README.md"
TEST_RUNNER=ROOT/"tools/run_tests.py"
PROMOTION_TEST=ROOT/"tests/test_living_research_promotion.py"

class PromotionWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow=WORKFLOW.read_text(encoding="utf-8")
        cls.runner=RUNNER.read_text(encoding="utf-8")
        cls.readme=README.read_text(encoding="utf-8")
        cls.test_runner=TEST_RUNNER.read_text(encoding="utf-8")
        cls.promotion_test=PROMOTION_TEST.read_text(encoding="utf-8")

    def test_workflow_has_one_canonical_transaction_entrypoint(self):
        self.assertIn("ref: main",self.workflow)
        self.assertIn("python -m tools.run_living_research_promotion",self.workflow)
        self.assertNotIn("python tools/run_living_research_promotion.py",self.workflow)
        self.assertNotIn("gh pr create",self.workflow)
        self.assertNotIn("git add -A",self.workflow)
        self.assertNotIn("automation/living-research-inbox",self.workflow)

    def test_documented_promotion_entrypoints_use_module_execution(self):
        self.assertIn("python -m tools.run_living_research_promotion",self.readme)
        self.assertIn("python -m tools.check_living_promotion_head",self.readme)
        self.assertNotIn("python tools/run_living_research_promotion.py",self.readme)
        self.assertNotIn("python tools/check_living_promotion_head.py",self.readme)

    def test_runner_freezes_exact_permanent_source_and_base(self):
        self.assertIn('SOURCE_PR = 490',self.runner)
        self.assertIn('SOURCE_BRANCH = "automation/living-research-inbox"',self.runner)
        self.assertIn('"state": "OPEN"',self.runner)
        self.assertIn('"isDraft": True',self.runner)
        self.assertIn('PR #490 advanced during promotion',self.runner)
        self.assertIn('main advanced during promotion',self.runner)

    def test_branch_identity_binds_full_source_and_base_hashes(self):
        self.assertIn('automation/living-promotion-{source_sha}-{base_sha}',self.runner)
        self.assertNotIn('[:0:45]',self.runner)

    def test_review_memory_is_not_snapshot_authority(self):
        self.assertIn('SNAPSHOT_AUTHS',self.runner)
        self.assertIn('ACCEPTED_FOR_MECHANICAL_SNAPSHOT',self.runner)
        self.assertIn('review_record_sha256',self.runner)
        self.assertIn('review_basis_sha256',self.runner)
        self.assertIn('snapshot_authorization_required',self.runner)

    def test_runner_stages_only_authorized_paths_and_never_self_merges(self):
        self.assertIn('git("add", "--", *to_stage)',self.runner)
        self.assertNotIn('git("add", "-A")',self.runner)
        self.assertNotIn('gh("pr", "merge"',self.runner)
        self.assertNotIn('branches/main/protection',self.runner)
        self.assertIn('validator-assurance.yml',self.runner)

    def test_precommit_and_final_head_verification_are_independent_layers(self):
        self.assertIn('git("commit", "-m"',self.runner)
        self.assertNotIn('--no-verify',self.runner)
        self.assertIn('integrity.verify(ROOT)',self.runner)
        self.assertIn('rglob("test_*.py")',self.test_runner)
        self.assertIn('check_living_promotion_head',self.promotion_test)
        self.assertIn('test_checked_out_repository_head_is_integrity_valid',self.promotion_test)

if __name__=="__main__": unittest.main()
