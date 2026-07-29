import copy
import importlib.util
import json
import pathlib
import subprocess
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
        cls.source_spec = checker.load(ROOT / cls.protocol["source_campaign"]["spec_path"])
        cls.source_proof = checker.load(ROOT / cls.protocol["source_campaign"]["proof_path"])
        cls.good_history = {
            "verified": True,
            "errors": [],
            "freeze_commit": cls.protocol["fixture_corpus"]["freeze_commit"],
            "implementation_commit": cls.protocol["fixture_corpus"]["implementation_commit"],
            "fixture_unchanged_since_freeze": True,
            "implementation_absent_at_freeze": True,
            "freeze_ancestor_of_implementation": True,
        }

    def build(self, **overrides):
        values = dict(
            protocol=copy.deepcopy(self.protocol),
            fixtures=copy.deepcopy(self.fixtures),
            result=copy.deepcopy(self.result),
            source_spec=copy.deepcopy(self.source_spec),
            source_proof=copy.deepcopy(self.source_proof),
            fresh_result=copy.deepcopy(self.result),
            script_text=checker.SCRIPT.read_text(),
            history=copy.deepcopy(self.good_history),
        )
        values.update(overrides)
        return checker.build_adjudication(**values)

    def test_fresh_isolated_execution_matches_committed_result(self):
        self.assertEqual(self.result, checker.run_isolated())

    def test_canonical_adjudication_is_replicated(self):
        adjudication = self.build()
        self.assertEqual("replicated", adjudication["decision"])
        self.assertEqual([], adjudication["errors"])
        self.assertTrue(adjudication["agreement"]["matches_source_classifications_and_failed_gates"])

    def test_protocol_is_outcome_blind(self):
        self.assertFalse(checker.protocol_has_outcome_leakage(self.protocol))
        bad = copy.deepcopy(self.protocol)
        bad["candidates"][0]["failed_gates"] = []
        self.assertTrue(checker.protocol_has_outcome_leakage(bad))

    def test_unverified_history_blocks_replication(self):
        history = copy.deepcopy(self.good_history)
        history["verified"] = False
        history["errors"] = ["fixture freeze is not ancestral"]
        adjudication = self.build(history=history)
        self.assertEqual("not_replicated", adjudication["decision"])
        self.assertIn("history proof: fixture freeze is not ancestral", adjudication["errors"])

    def test_source_kernel_dependency_is_rejected(self):
        adjudication = self.build(
            script_text=checker.SCRIPT.read_text()
            + '\nrequire("../../theory/foundation/fara_canonical_kernel/kernel.py")\n'
        )
        self.assertEqual("not_replicated", adjudication["decision"])
        self.assertTrue(any("dependency" in error for error in adjudication["errors"]))

    def test_process_module_is_rejected(self):
        adjudication = self.build(
            script_text=checker.SCRIPT.read_text().replace(
                'const path = require("path");',
                'const path = require("path");\nconst cp = require("child_process");',
            )
        )
        self.assertEqual("not_replicated", adjudication["decision"])
        self.assertTrue(any("runtime-module" in error or "dependency" in error for error in adjudication["errors"]))

    def test_algebraic_gate_results_respond_to_view_changes(self):
        script = f"""
const r = require({json.dumps(str(checker.SCRIPT))});
const fixture = JSON.parse(require('fs').readFileSync({json.dumps(str(checker.FIXTURES))}, 'utf8')).scenarios[0];
const model = r.materializeScenario(fixture);
const view = r.toAlgebraic(model);
const before = r.deriveAlgebraicGates(view);
view.schema.push('Object', 'Representation', 'Interpretation', 'Provenance', 'RelationOccurrence');
view.provenance = [];
const after = r.deriveAlgebraicGates(view);
process.stdout.write(JSON.stringify({{before, after}}));
"""
        completed = subprocess.run(["node", "-e", script], text=True, capture_output=True, check=True)
        observed = json.loads(completed.stdout)
        for gate in (
            "representation_object_separation",
            "interpretation_separation",
            "identity_bearing_occurrences",
            "explicit_provenance_and_order",
        ):
            self.assertFalse(observed["before"][gate]["pass"])
            self.assertTrue(observed["after"][gate]["pass"])

    def test_stale_result_is_rejected(self):
        bad = copy.deepcopy(self.result)
        bad["provisional_result"] = ["typed-hypergraph"]
        adjudication = self.build(result=bad)
        self.assertIn("committed result differs from fresh isolated execution", adjudication["errors"])

    def test_candidate_disagreement_is_rejected(self):
        bad = copy.deepcopy(self.result)
        bad["candidate_adjudication"][0]["classification"] = "admissible-derived-view"
        adjudication = self.build(result=bad, fresh_result=bad)
        self.assertIn("candidate classifications or failed-gate sets disagree with source proof", adjudication["errors"])

    def test_failed_gate_evidence_drift_is_rejected(self):
        bad = copy.deepcopy(self.result)
        bad["candidate_adjudication"][0]["gate_results"]["identity_bearing_occurrences"]["pass"] = True
        adjudication = self.build(result=bad, fresh_result=bad)
        self.assertTrue(any("failed-gate drift" in error for error in adjudication["errors"]))

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
                source.write_bytes((ROOT / self.protocol["source_campaign"][key]).read_bytes())
            adjudication = self.build(root=root)
            self.assertIn("neutral fixture blob lock mismatch", adjudication["errors"])

    def test_external_investigator_independence_remains_unclaimed(self):
        adjudication = self.build()
        self.assertEqual("not established", adjudication["independence"]["external_investigator_independence"])
        self.assertEqual("pending separate PR", adjudication["lifecycle_consequence"]["acceptance"])
        self.assertFalse(adjudication["lifecycle_consequence"]["canonical_authority_changed"])

    def test_generated_artifacts_are_current(self):
        adjudication = self.build()
        self.assertEqual(adjudication, checker.load(checker.ADJUDICATION))
        self.assertEqual(checker.render(adjudication), checker.REPORT.read_text())


if __name__ == "__main__":
    unittest.main()
