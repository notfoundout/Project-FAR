import copy
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "replication_checker", ROOT / "tools/check_fara_canonical_kernel_replication.py"
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class CleanRoomReplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = checker.load(checker.PROTOCOL)
        cls.fixtures = checker.load(checker.FIXTURES)
        cls.result = checker.load(checker.RESULT)
        cls.source_spec = checker.load(
            ROOT / cls.protocol["source_campaign"]["spec_path"]
        )
        cls.source_proof = checker.load(
            ROOT / cls.protocol["source_campaign"]["proof_path"]
        )

    def build(self, **overrides):
        values = dict(
            protocol=copy.deepcopy(self.protocol),
            fixtures=copy.deepcopy(self.fixtures),
            result=copy.deepcopy(self.result),
            source_spec=copy.deepcopy(self.source_spec),
            source_proof=copy.deepcopy(self.source_proof),
            fresh_result=copy.deepcopy(self.result),
            script_text=checker.SCRIPT.read_text(),
        )
        values.update(overrides)
        return checker.build_adjudication(**values)

    def test_fresh_isolated_execution_matches_committed_result(self):
        self.assertEqual(self.result, checker.run_isolated())

    def test_canonical_adjudication_is_replicated(self):
        adjudication = self.build()
        self.assertEqual("replicated", adjudication["decision"])
        self.assertEqual([], adjudication["errors"])
        self.assertTrue(
            adjudication["agreement"][
                "matches_source_classifications_and_failed_gates"
            ]
        )

    def test_protocol_is_outcome_blind(self):
        self.assertFalse(checker.protocol_has_outcome_leakage(self.protocol))
        bad = copy.deepcopy(self.protocol)
        bad["candidates"][0]["failed_gates"] = []
        self.assertTrue(checker.protocol_has_outcome_leakage(bad))

    def test_source_kernel_dependency_is_rejected(self):
        adjudication = self.build(
            script_text=checker.SCRIPT.read_text()
            + '\nrequire("../../theory/foundation/fara_canonical_kernel/kernel.py")\n'
        )
        self.assertEqual("not_replicated", adjudication["decision"])
        self.assertTrue(
            any("dependency" in error for error in adjudication["errors"])
        )

    def test_network_or_process_module_is_rejected(self):
        adjudication = self.build(
            script_text=checker.SCRIPT.read_text().replace(
                'const path = require("path");',
                'const path = require("path");\nconst cp = require("child_process");',
            )
        )
        self.assertEqual("not_replicated", adjudication["decision"])
        self.assertTrue(
            any(
                "runtime modules" in error or "dependency" in error
                for error in adjudication["errors"]
            )
        )

    def test_stale_result_is_rejected(self):
        bad = copy.deepcopy(self.result)
        bad["provisional_result"] = ["typed-hypergraph"]
        adjudication = self.build(result=bad)
        self.assertIn(
            "committed result differs from fresh isolated execution",
            adjudication["errors"],
        )

    def test_candidate_disagreement_is_rejected(self):
        bad = copy.deepcopy(self.result)
        bad["candidate_adjudication"][0][
            "classification"
        ] = "admissible-derived-view"
        adjudication = self.build(result=bad, fresh_result=bad)
        self.assertIn(
            "candidate classifications or failed-gate sets disagree with source proof",
            adjudication["errors"],
        )

    def test_failed_gate_evidence_drift_is_rejected(self):
        bad = copy.deepcopy(self.result)
        bad["candidate_adjudication"][0]["gate_results"][
            "identity_bearing_occurrences"
        ]["pass"] = True
        adjudication = self.build(result=bad, fresh_result=bad)
        self.assertTrue(
            any("failed-gate drift" in error for error in adjudication["errors"])
        )

    def test_premature_acceptance_is_rejected(self):
        bad = copy.deepcopy(self.result)
        bad["lifecycle"]["acceptance"] = "complete"
        adjudication = self.build(result=bad, fresh_result=bad)
        self.assertIn("premature acceptance", adjudication["errors"])

    def test_fixture_blob_lock_mutation_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            relative = pathlib.Path(self.protocol["fixture_corpus"]["path"])
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_text("{}\n")
            for key in ("spec_path", "proof_path"):
                source = root / self.protocol["source_campaign"][key]
                source.parent.mkdir(parents=True, exist_ok=True)
                original = ROOT / self.protocol["source_campaign"][key]
                source.write_bytes(original.read_bytes())
            adjudication = checker.build_adjudication(
                copy.deepcopy(self.protocol),
                copy.deepcopy(self.fixtures),
                copy.deepcopy(self.result),
                copy.deepcopy(self.source_spec),
                copy.deepcopy(self.source_proof),
                root=root,
                script_text=checker.SCRIPT.read_text(),
                fresh_result=copy.deepcopy(self.result),
            )
            self.assertIn(
                "neutral fixture blob lock mismatch", adjudication["errors"]
            )

    def test_external_investigator_independence_remains_unclaimed(self):
        adjudication = self.build()
        self.assertEqual(
            "not established",
            adjudication["independence"]["external_investigator_independence"],
        )
        self.assertEqual(
            "pending separate PR",
            adjudication["lifecycle_consequence"]["acceptance"],
        )
        self.assertFalse(
            adjudication["lifecycle_consequence"]["canonical_authority_changed"]
        )

    def test_generated_artifacts_are_current(self):
        adjudication = self.build()
        self.assertEqual(adjudication, checker.load(checker.ADJUDICATION))
        self.assertEqual(checker.render(adjudication), checker.REPORT.read_text())


if __name__ == "__main__":
    unittest.main()
