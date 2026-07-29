import copy
import importlib.util
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXECUTOR = ROOT / "research/theory-dependency-audit/execute.py"
SPEC = importlib.util.spec_from_file_location("audit", EXECUTOR)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class TheoryDependencyAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(audit.SPEC_PATH.read_text())
        cls.committed = json.loads(audit.RESULT_PATH.read_text())

    def git(self, root, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check,
        )

    def materialize_frozen_sources(self):
        temp = tempfile.TemporaryDirectory()
        root = pathlib.Path(temp.name)
        for rel in self.spec["source_locks"]:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(
                audit.read_base_blob(ROOT, self.spec["base_commit"], rel)
            )
        return temp, root

    def refresh(self, root, spec, rel):
        spec["source_locks"][rel] = audit.git_blob_sha((root / rel).read_bytes())

    def mutate(self, root, spec, rel, old, new):
        path = root / rel
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))
        self.refresh(root, spec, rel)

    def check_row(self, result, check_id):
        return next(row for row in result["checks"] if row["id"] == check_id)

    def test_preregistration_commits_precede_execution_and_result(self):
        def path_commit(path):
            return self.git(ROOT, "log", "-1", "--format=%H", "--", path).stdout.strip()

        question = path_commit("research/theory-dependency-audit/question-v1.0.md")
        specification = path_commit(
            "research/theory-dependency-audit/execution-spec-v1.0.json"
        )
        executor = path_commit("research/theory-dependency-audit/execute.py")
        result = path_commit("research/theory-dependency-audit/result-v1.0.json")

        self.assertTrue(question and specification and executor and result)
        self.git(ROOT, "merge-base", "--is-ancestor", question, specification)
        self.git(ROOT, "merge-base", "--is-ancestor", specification, executor)
        self.git(ROOT, "merge-base", "--is-ancestor", executor, result)
        self.git(
            ROOT,
            "cat-file",
            "-e",
            f"{executor}^:research/theory-dependency-audit/question-v1.0.md",
        )
        self.git(
            ROOT,
            "cat-file",
            "-e",
            f"{executor}^:research/theory-dependency-audit/execution-spec-v1.0.json",
        )
        absent = self.git(
            ROOT,
            "cat-file",
            "-e",
            f"{executor}^:research/theory-dependency-audit/result-v1.0.json",
            check=False,
        )
        self.assertNotEqual(0, absent.returncode)

    def test_committed_result_matches_frozen_base_execution(self):
        self.assertEqual(self.committed, audit.execute())

    def test_execution_is_deterministic(self):
        self.assertEqual(audit.execute(), audit.execute())

    def test_every_source_lock_is_verified(self):
        self.assertTrue(
            all(
                row["verified"]
                for row in audit.execute()["source_lock_results"].values()
            )
        )

    def test_mutable_worktree_does_not_change_frozen_git_evidence(self):
        temp, root = self.materialize_frozen_sources()
        self.addCleanup(temp.cleanup)
        self.git(root, "init")
        self.git(root, "config", "user.email", "audit@example.invalid")
        self.git(root, "config", "user.name", "Audit Fixture")
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "frozen source fixture")
        base = self.git(root, "rev-parse", "HEAD").stdout.strip()

        spec = copy.deepcopy(self.spec)
        spec["base_commit"] = base
        path = root / "theory/definitions/definitions.md"
        path.write_text("MUTATED WORKTREE\n")

        result = audit.execute(spec, root=root, source_mode="git")
        self.assertTrue(
            result["source_lock_results"][
                "theory/definitions/definitions.md"
            ]["verified"]
        )
        self.assertEqual("Pass", self.check_row(result, "C1")["content_result"])

    def test_source_admissibility_summary_is_exact(self):
        summary = audit.execute()["source_admissibility"]
        self.assertEqual(
            {"Accepted": 4, "Provisional": 1, "Unknown": 4},
            summary["counts"],
        )
        self.assertFalse(summary["all_selected_sources_accepted"])

    def test_primitive_registry_is_provisional(self):
        row = audit.execute()["source_admissibility"]["artifacts"][
            "frameworks/FARA/primitives.md"
        ]
        self.assertEqual("Provisional", row["acceptance_state"])
        self.assertFalse(row["acceptance_verified"])

    def test_unstatused_sources_remain_unknown(self):
        artifacts = audit.execute()["source_admissibility"]["artifacts"]
        for rel in (
            "theory/definitions/definitions.md",
            "docs/governance/semantic-consistency.json",
            "frameworks/FAR/dependency-graph.md",
            "frameworks/FARO/dependency-graph.md",
        ):
            self.assertEqual("Unknown", artifacts[rel]["acceptance_state"])

    def test_explicitly_accepted_sources_are_verified(self):
        artifacts = audit.execute()["source_admissibility"]["artifacts"]
        for rel in (
            "frameworks/FARA/formal-kernel.md",
            "docs/glossary/canonical-terminology.md",
            "docs/governance/framework-boundaries.md",
            "docs/governance/derivation-status-matrix.md",
        ):
            self.assertEqual("Accepted", artifacts[rel]["acceptance_state"])

    def test_proof_inventory_omission_preserves_unknown(self):
        proof = audit.execute()["proof_scope"]
        self.assertFalse(proof["selected_in_frozen_source_set"])
        self.assertFalse(proof["positive_derivation_proof_verified"])
        self.assertFalse(proof["proof_absence_verified"])
        self.assertEqual("Unknown", proof["status"])

    def test_candidate_adjudication_is_all_unknown(self):
        result = audit.execute()
        self.assertEqual(
            {
                "split_authority": "Unknown",
                "undifferentiated_owner": "Unknown",
            },
            result["candidate_adjudication"]["authority_models"],
        )
        self.assertEqual(
            {
                "logical_derivation": "Unknown",
                "artifact_workflow_contract": "Unknown",
                "unclassified_dependency": "Unknown",
            },
            result["candidate_adjudication"]["dependency_models"],
        )

    def test_checks_separate_content_from_admissibility(self):
        result = audit.execute()
        statuses = {row["id"]: row["status"] for row in result["checks"]}
        self.assertEqual(
            {
                "C1": "Unknown",
                "C2": "Unknown",
                "C3": "Unknown",
                "C4": "Pass",
                "C5": "Unknown",
                "C6": "Unknown",
                "C7": "Pass",
            },
            statuses,
        )
        self.assertEqual("Pass", self.check_row(result, "C1")["content_result"])
        self.assertEqual("Fail", self.check_row(result, "C3")["content_result"])
        self.assertEqual("Pass", self.check_row(result, "C5")["content_result"])

    def test_discovery_is_unsupported_failure_outcome(self):
        result = audit.execute()
        self.assertFalse(result["discovery"]["supported"])
        self.assertEqual(
            "no_reconciliation_discovery_supported",
            result["discovery"]["finding"],
        )
        self.assertEqual("complete", result["lifecycle"]["discovery"])
        self.assertEqual("failure report", result["lifecycle"]["outcome"])

    def test_report_uses_allowed_research_status(self):
        report = (
            ROOT / "research/theory-dependency-audit/report-v1.0.md"
        ).read_text()
        self.assertIn("Status: **Research**", report)
        self.assertIn("Outcome: **failure report**", report)
        self.assertNotIn("Status: **Research failure report**", report)

    def test_formal_kernel_acceptance_removal_yields_unknown(self):
        temp, root = self.materialize_frozen_sources()
        self.addCleanup(temp.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate(
            root,
            spec,
            "frameworks/FARA/formal-kernel.md",
            "Status: **Accepted**",
            "Status: **Research**",
        )
        result = audit.execute(spec, root=root, source_mode="worktree")
        self.assertEqual("Unknown", self.check_row(result, "C4")["status"])

    def test_protocol_content_mutation_fails_for_accepted_sources(self):
        temp, root = self.materialize_frozen_sources()
        self.addCleanup(temp.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate(
            root,
            spec,
            "docs/governance/derivation-status-matrix.md",
            "| evaluator mapping | CRP/FARO | empirical protocol |",
            "| evaluator mapping | CRP/FARO | derived theorem |",
        )
        result = audit.execute(spec, root=root, source_mode="worktree")
        self.assertEqual("Fail", self.check_row(result, "C7")["status"])

    def test_accepting_far_dependency_does_not_cure_missing_proof_scope(self):
        temp, root = self.materialize_frozen_sources()
        self.addCleanup(temp.cleanup)
        spec = copy.deepcopy(self.spec)
        path = root / "frameworks/FAR/dependency-graph.md"
        path.write_text("Status: **Accepted**\n" + path.read_text())
        self.refresh(root, spec, "frameworks/FAR/dependency-graph.md")
        result = audit.execute(spec, root=root, source_mode="worktree")
        self.assertEqual("Pass", self.check_row(result, "C5")["status"])
        self.assertEqual(
            "Unknown",
            result["candidate_adjudication"]["dependency_models"][
                "logical_derivation"
            ],
        )

    def test_worktree_source_drift_fails_closed_in_fixture_mode(self):
        temp, root = self.materialize_frozen_sources()
        self.addCleanup(temp.cleanup)
        path = root / "frameworks/FARA/primitives.md"
        path.write_text(path.read_text() + "\ndrift\n")
        with self.assertRaisesRegex(ValueError, "frozen source identity mismatch"):
            audit.execute(
                copy.deepcopy(self.spec),
                root=root,
                source_mode="worktree",
            )

    def test_standard_targets_run_audit_and_tests(self):
        makefile = (ROOT / "Makefile").read_text()
        for target in ("health:", "health-fast:", "research-check:"):
            section = makefile.split(target, 1)[1].split("\n\n", 1)[0]
            self.assertIn(
                "python research/theory-dependency-audit/execute.py", section
            )
            self.assertIn(
                "python -m unittest tests.test_theory_dependency_audit -v",
                section,
            )

    def test_nonclaims_block_promotion(self):
        nonclaims = set(audit.execute()["nonclaims"])
        self.assertIn("accepted authority model", nonclaims)
        self.assertIn("accepted dependency classification", nonclaims)
        self.assertIn("experiment preregistration authorization", nonclaims)
        self.assertIn("experiment execution authorization", nonclaims)


if __name__ == "__main__":
    unittest.main()
