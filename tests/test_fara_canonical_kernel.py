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


class CanonicalKernelTests(unittest.TestCase):
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

    def test_only_identity_bearing_relational_kernel_passes_all_gates(self):
        rows = {
            row["id"]: row
            for row in self.proof["candidate_adjudication"]
        }
        self.assertEqual(
            "canonical-candidate",
            rows["identity-bearing-many-sorted-relational"]["classification"],
        )
        self.assertEqual(
            ["identity_bearing_occurrences"],
            rows["many-sorted-extensional-relational"]["failed_gates"],
        )
        self.assertEqual(
            ["encoding_neutrality"],
            rows["typed-hypergraph"]["failed_gates"],
        )
        self.assertEqual(
            "noncanonical",
            rows["many-sorted-extensional-relational"]["classification"],
        )
        self.assertEqual(
            "admissible-derived-view",
            rows["algebraic-state-transition"]["classification"],
        )

    def test_parallel_occurrences_survive_kernel_and_hypergraph_roundtrip(self):
        model = kernel.sample_model()
        self.assertEqual([], kernel.validate_model(model))
        self.assertEqual(2, len(model["sorts"]["RelationOccurrence"]))
        projected = kernel.extensional_occurrence_projection(model)
        self.assertEqual(1, len(projected))
        restored = kernel.from_typed_hypergraph(kernel.to_typed_hypergraph(model))
        self.assertEqual(
            kernel.canonical(kernel.normalized_model(model)),
            kernel.canonical(kernel.normalized_model(restored)),
        )
        self.assertEqual(2, len(restored["sorts"]["RelationOccurrence"]))

    def test_algebraic_view_requires_explicit_sidecar(self):
        model = kernel.sample_model()
        view = kernel.to_algebraic_view(model)
        self.assertFalse(view["standalone_complete"])
        restored = kernel.from_algebraic_view(copy.deepcopy(view))
        self.assertEqual(
            kernel.canonical(kernel.normalized_model(model)),
            kernel.canonical(kernel.normalized_model(restored)),
        )
        del view["sidecar"]
        with self.assertRaises(ValueError):
            kernel.from_algebraic_view(view)

    def test_admissibility_rejects_cross_sort_collapse_and_forged_events(self):
        model = kernel.sample_model()
        model["sorts"]["Representation"].append("source-temperature")
        self.assertIn(
            "cross-sort identity collision: source-temperature",
            kernel.validate_model(model),
        )
        model = kernel.sample_model()
        model["relations"]["applies"] = []
        self.assertIn("event without rule: e1", kernel.validate_model(model))
        self.assertIn("event without rule: e2", kernel.validate_model(model))

    def test_precedence_cycles_fail(self):
        model = kernel.sample_model()
        model["relations"]["precedes"].append(["e2", "e1"])
        self.assertIn(
            "precedes relation contains a cycle",
            kernel.validate_model(model),
        )

    def test_mutations_fail_closed(self):
        mutations = [
            lambda spec: spec.__setitem__("selected_foundation", "typed-hypergraph"),
            lambda spec: spec["mandatory_gates"].pop(),
            lambda spec: spec["candidates"][3]["gates"].__setitem__(
                "identity_bearing_occurrences", False
            ),
            lambda spec: spec["candidates"][1]["gates"].__setitem__(
                "encoding_neutrality", True
            ),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                spec = copy.deepcopy(self.spec)
                mutation(spec)
                self.assertTrue(
                    checker.validate(spec, self.proof, check_historical=False)
                )

    def test_hypergraph_edges_have_unique_identity(self):
        view = kernel.to_typed_hypergraph(kernel.sample_model())
        edge_ids = [edge["id"] for edge in view["edges"]]
        self.assertEqual(len(edge_ids), len(set(edge_ids)))

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
        proof["selected_foundation"] = "typed-hypergraph"
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
