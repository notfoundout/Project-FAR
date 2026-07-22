from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_evc_w2_r3_replication_package.py"

spec = importlib.util.spec_from_file_location("check_evc_w2_r3_replication_package", CHECKER_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class EVCW2R3ReplicationPackageTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        self.assertEqual(checker.validate(), [])

    def test_protocol_remains_unexecuted_and_external(self) -> None:
        protocol = checker.load_json(checker.PROTOCOL_PATH)
        self.assertEqual(protocol["status"], "frozen_unexecuted")
        self.assertEqual(protocol["evidence_layer"], "R3_independent_technical_replication")
        required = " ".join(protocol["replicator_eligibility"]["required"])
        disqualifying = " ".join(protocol["replicator_eligibility"]["disqualifying"])
        self.assertIn("separate human or organization", required)
        self.assertIn("shared agent-controlled", disqualifying)
        self.assertIn("same organization", disqualifying)

    def test_target_classifications_are_frozen(self) -> None:
        protocol = checker.load_json(checker.PROTOCOL_PATH)
        targets = {
            item["id"]: item["expected_classification"]
            for item in protocol["mandatory_replication_targets"]
        }
        self.assertEqual(targets, checker.EXPECTED_TARGETS)

    def test_mutation_corpus_is_complete(self) -> None:
        corpus = checker.load_json(checker.MUTATION_PATH)
        mutation_ids = {item["id"] for item in corpus["mutations"]}
        self.assertEqual(mutation_ids, checker.EXPECTED_MUTATIONS)
        self.assertEqual(len({item["protected_gate"] for item in corpus["mutations"]}), 7)

    def test_release_state_cannot_imply_execution(self) -> None:
        manifest = checker.load_json(checker.MANIFEST_PATH)
        state = manifest["release_state"]
        self.assertFalse(state["replicator_recruited"])
        self.assertIsNone(state["replicator_eligible"])
        self.assertIsNone(state["release_commit"])
        self.assertIsNone(state["first_access_timestamp"])
        self.assertFalse(state["implementation_frozen"])
        self.assertFalse(state["reference_results_unsealed"])
        self.assertFalse(state["replication_started"])
        self.assertFalse(state["replication_completed"])

    def test_result_template_has_no_verdict(self) -> None:
        result = checker.load_json(checker.RESULT_PATH)
        self.assertIsNone(result["initial_outcome"])
        self.assertIsNone(result["initial_result_published_at"])
        self.assertEqual(
            set(result["allowed_outcomes"]),
            {"replicated", "partially_replicated", "not_replicated", "unresolved"},
        )

    def test_w1_manifest_parent_program_regression(self) -> None:
        manifest = checker.load_json(checker.W1_MANIFEST_PATH)
        text = json.dumps(manifest, sort_keys=True)
        self.assertIn("theory/evaluation/post-w5-usd-next-program-v1.0.json", text)
        self.assertIn("the parent POST-USD-EVC-001 registration artifact is included", text)


if __name__ == "__main__":
    unittest.main()
