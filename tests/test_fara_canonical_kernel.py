import copy
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import check_fara_canonical_kernel as checker
from theory.foundation.fara_canonical_kernel import kernel


class CanonicalKernelResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(checker.SPEC.read_text())
        cls.proof = json.loads(checker.PROOF.read_text())

    def test_fresh_proof_and_report(self):
        self.assertEqual(kernel.build_proof(copy.deepcopy(self.spec)), self.proof)
        self.assertEqual(
            [],
            checker.validate(
                self.spec,
                self.proof,
                checker.REPORT.read_text(),
                check_historical=False,
            ),
        )

    def test_gate_results_are_executable_not_spec_authored(self):
        self.assertTrue(all("gates" not in row for row in self.spec["candidates"]))
        rows = {row["id"]: row for row in self.proof["candidate_adjudication"]}
        self.assertEqual(
            "provisional-canonical-candidate",
            rows["identity-bearing-many-sorted-relational"]["classification"],
        )
        self.assertTrue(
            all(
                item["pass"]
                for item in rows["identity-bearing-many-sorted-relational"][
                    "gate_evidence"
                ].values()
            )
        )
        self.assertFalse(
            rows["many-sorted-extensional-relational"]["gate_evidence"][
                "identity_bearing_occurrences"
            ]["pass"]
        )
        self.assertFalse(
            rows["typed-hypergraph"]["gate_evidence"]["encoding_neutrality"][
                "pass"
            ]
        )

    def test_candidate_authored_gate_booleans_are_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec["candidates"][2]["gates"] = {
            gate: True for gate in kernel.MANDATORY_GATES
        }
        errors = checker.validate(spec, self.proof, check_historical=False)
        self.assertIn("candidate-authored gate booleans", errors)

    def test_parallel_occurrences_survive_kernel_and_hypergraph_roundtrip(self):
        model = kernel.sample_model()
        self.assertEqual([], kernel.validate_model(model))
        self.assertEqual(2, len(model["sorts"]["RelationOccurrence"]))
        self.assertEqual(1, len(kernel.extensional_occurrence_projection(model)))
        restored = kernel.from_typed_hypergraph(kernel.to_typed_hypergraph(model))
        self.assertEqual(
            kernel.canonical(kernel.normalized_model(model)),
            kernel.canonical(kernel.normalized_model(restored)),
        )

    def test_algebraic_view_requires_explicit_sidecar(self):
        model = kernel.sample_model()
        view = kernel.to_algebraic_view(model)
        restored = kernel.from_algebraic_view(copy.deepcopy(view))
        self.assertEqual(
            kernel.canonical(kernel.normalized_model(model)),
            kernel.canonical(kernel.normalized_model(restored)),
        )
        del view["sidecar"]
        with self.assertRaisesRegex(ValueError, "sidecar"):
            kernel.from_algebraic_view(view)

    def test_event_requires_exactly_one_rule_input_output_and_investigation(self):
        relation_and_error = (
            ("applies", ["e1", "rule-second"], "exactly one rule"),
            ("input_state", ["e1", "s1"], "exactly one input state"),
            ("output_state", ["e1", "s0"], "exactly one output state"),
            ("occurs_in", ["e1", "inv-2"], "exactly one investigation"),
        )
        for relation, extra, expected in relation_and_error:
            with self.subTest(relation=relation):
                model = kernel.sample_model()
                if relation == "applies":
                    model["sorts"]["Rule"].append("rule-second")
                    model["relations"]["contains_rule"].append(
                        ["calc-1", "rule-second"]
                    )
                if relation == "occurs_in":
                    model["sorts"]["Investigation"].append("inv-2")
                model["relations"][relation].append(extra)
                self.assertTrue(
                    any(expected in error for error in kernel.validate_model(model))
                )
                with self.assertRaises(ValueError):
                    kernel.to_algebraic_view(model)

    def test_event_without_provenance_is_rejected(self):
        model = kernel.sample_model()
        model["relations"]["provenance_of"] = [
            row for row in model["relations"]["provenance_of"] if row[0] != "e1"
        ]
        self.assertIn(
            "event without explicit provenance: e1", kernel.validate_model(model)
        )

    def test_cross_sort_collapse_and_precedence_cycles_fail(self):
        model = kernel.sample_model()
        model["sorts"]["Representation"].append("source-temperature")
        self.assertIn(
            "cross-sort identity collision: source-temperature",
            kernel.validate_model(model),
        )
        model = kernel.sample_model()
        model["relations"]["precedes"].append(["e2", "e1"])
        self.assertIn(
            "precedes relation contains a cycle", kernel.validate_model(model)
        )

    def test_lifecycle_cannot_be_promoted_in_research_artifact(self):
        for field, value in (("status", "Accepted"),):
            spec = copy.deepcopy(self.spec)
            spec[field] = value
            self.assertTrue(checker.validate(spec, self.proof, check_historical=False))
        spec = copy.deepcopy(self.spec)
        spec["lifecycle"]["acceptance"] = "complete"
        self.assertIn(
            "premature acceptance or promotion",
            checker.validate(spec, self.proof, check_historical=False),
        )

    def test_historical_artifact_mutation_fails(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            spec = copy.deepcopy(self.spec)
            spec["historical_artifacts"] = {}
            for index, relative in enumerate(("a.txt", "b.txt")):
                path = root / relative
                data = f"frozen-{index}\n".encode()
                path.write_bytes(data)
                spec["historical_artifacts"][relative] = {
                    "base_commit": "base",
                    "git_blob_sha": checker.git_blob_sha(data),
                }
            self.assertEqual([], checker.validate_historical(spec, root=root))
            (root / "a.txt").write_text("mutated\n")
            self.assertTrue(checker.validate_historical(spec, root=root))

    def test_stale_proof_and_report_fail(self):
        proof = copy.deepcopy(self.proof)
        proof["proposed_foundation"] = "typed-hypergraph"
        self.assertIn(
            "stale proof object",
            checker.validate(self.spec, proof, check_historical=False),
        )
        self.assertIn(
            "stale generated report",
            checker.validate(
                self.spec,
                self.proof,
                checker.REPORT.read_text() + "fabricated\n",
                check_historical=False,
            ),
        )


if __name__ == "__main__":
    unittest.main()
