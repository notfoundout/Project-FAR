import copy
import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXECUTOR_PATH = ROOT / "research/theory-dependency-audit/execute.py"
SPEC = importlib.util.spec_from_file_location("theory_dependency_audit", EXECUTOR_PATH)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class TheoryDependencyAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(audit.SPEC_PATH.read_text())
        cls.committed = json.loads(audit.RESULT_PATH.read_text())

    def materialize_sources(self):
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        for relative in self.spec["source_locks"]:
            source = ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        return temporary, root

    def mutate_source(self, root, spec, relative, old, new):
        path = root / relative
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))
        spec["source_locks"][relative] = audit.git_blob_sha(path.read_bytes())

    def check(self, result, check_id):
        return next(row for row in result["checks"] if row["id"] == check_id)

    def test_committed_result_matches_fresh_execution(self):
        self.assertEqual(self.committed, audit.execute())

    def test_execution_is_deterministic(self):
        self.assertEqual(audit.execute(), audit.execute())

    def test_every_source_lock_is_verified(self):
        result = audit.execute()
        self.assertTrue(result["source_lock_results"])
        self.assertTrue(
            all(row["verified"] for row in result["source_lock_results"].values())
        )

    def test_candidate_adjudication_matches_registered_decision_rules(self):
        result = audit.execute()
        self.assertEqual(
            {"split_authority": "Pass", "undifferentiated_owner": "Fail"},
            result["candidate_adjudication"]["authority_models"],
        )
        self.assertEqual(
            {
                "artifact_workflow_contract": "Pass",
                "logical_derivation": "Fail",
                "unclassified_dependency": "Fail",
            },
            result["candidate_adjudication"]["dependency_models"],
        )

    def test_discovery_remains_research_and_stops_before_replication(self):
        result = audit.execute()
        self.assertEqual("Research", result["status"])
        self.assertEqual("Research finding", result["lifecycle"]["discovery"])
        self.assertEqual(
            "pending separate implementation", result["lifecycle"]["replication"]
        )
        self.assertEqual("prohibited", result["lifecycle"]["acceptance"])
        self.assertEqual("prohibited", result["lifecycle"]["promotion"])
        self.assertEqual(
            "prohibited except Research evidence",
            result["lifecycle"]["repository_change"],
        )

    def test_definition_authority_marker_removal_fails_c1(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate_source(
            root,
            spec,
            "theory/definitions/definitions.md",
            "The definitions contained in this document are canonical",
            "These definitions are merely informative",
        )
        result = audit.execute(spec, root=root)
        self.assertEqual("Fail", self.check(result, "C1")["status"])
        self.assertEqual(
            "Fail", result["candidate_adjudication"]["authority_models"]["split_authority"]
        )

    def test_candidate_primitive_deletion_fails_c2(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate_source(
            root,
            spec,
            "frameworks/FARA/primitives.md",
            "- Property\n",
            "",
        )
        result = audit.execute(spec, root=root)
        self.assertEqual("Fail", self.check(result, "C2")["status"])

    def test_current_owner_registry_incompleteness_is_measured(self):
        result = audit.execute()
        check = self.check(result, "C3")
        self.assertEqual("Fail", check["status"])
        self.assertFalse(check["measurements"]["all_seven_registered"])
        self.assertFalse(
            check["measurements"][
                "separate_definition_and_classification_fields_present"
            ]
        )
        self.assertEqual(
            ["object", "property", "relation", "representation"],
            check["measurements"]["registered_candidate_primitive_terms"],
        )

    def test_formal_kernel_nonclaim_removal_fails_c4(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate_source(
            root,
            spec,
            "frameworks/FARA/formal-kernel.md",
            "The formal carrier names do not reclassify FARA's seven candidate primitives.",
            "The formal carrier names replace the candidate primitive registry.",
        )
        result = audit.execute(spec, root=root)
        self.assertEqual("Fail", self.check(result, "C4")["status"])

    def test_far_artifact_contract_marker_removal_fails_c5(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate_source(
            root,
            spec,
            "frameworks/FAR/dependency-graph.md",
            "FARA provides the architecture used by FAR",
            "FARA is unrelated to FAR",
        )
        result = audit.execute(spec, root=root)
        self.assertEqual("Fail", self.check(result, "C5")["status"])

    def test_far_non_derivation_marker_removal_fails_c5(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate_source(
            root,
            spec,
            "docs/governance/framework-boundaries.md",
            "that its procedural choices are FARA theorems",
            "unrelated procedural note",
        )
        result = audit.execute(spec, root=root)
        self.assertEqual("Fail", self.check(result, "C5")["status"])

    def test_faro_workflow_contract_marker_removal_fails_c6(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate_source(
            root,
            spec,
            "frameworks/FARO/dependency-graph.md",
            "Supplies stable investigation methodology",
            "Supplies no investigation methodology",
        )
        result = audit.execute(spec, root=root)
        self.assertEqual("Fail", self.check(result, "C6")["status"])

    def test_faro_non_derivation_marker_removal_fails_c6(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate_source(
            root,
            spec,
            "docs/governance/framework-boundaries.md",
            "that operational choices follow necessarily from FARA/FAR",
            "unrelated operational note",
        )
        result = audit.execute(spec, root=root)
        self.assertEqual("Fail", self.check(result, "C6")["status"])

    def test_protocol_independence_marker_removal_fails_c7(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        spec = copy.deepcopy(self.spec)
        self.mutate_source(
            root,
            spec,
            "docs/governance/derivation-status-matrix.md",
            "independent design choice",
            "derived theorem",
        )
        result = audit.execute(spec, root=root)
        self.assertEqual("Fail", self.check(result, "C7")["status"])

    def test_unupdated_source_lock_fails_closed(self):
        temporary, root = self.materialize_sources()
        self.addCleanup(temporary.cleanup)
        path = root / "frameworks/FARA/primitives.md"
        path.write_text(path.read_text() + "\nmutation\n")
        with self.assertRaisesRegex(ValueError, "locked source drift"):
            audit.execute(copy.deepcopy(self.spec), root=root)

    def test_nonclaims_block_premature_promotion_and_execution(self):
        nonclaims = set(audit.execute()["nonclaims"])
        self.assertIn("accepted authority model", nonclaims)
        self.assertIn("canonical repository change", nonclaims)
        self.assertIn("experiment preregistration authorization", nonclaims)
        self.assertIn("experiment execution authorization", nonclaims)


if __name__ == "__main__":
    unittest.main()
