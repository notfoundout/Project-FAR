import copy
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import check_fara_expanded_campaign as checker


class ExpandedCampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(checker.SPEC.read_text())
        cls.proof = json.loads(checker.PROOF.read_text())

    def validate_without_upstream(self, proof=None, report=None):
        return checker.validate(
            self.spec,
            self.proof if proof is None else proof,
            checker.REPORT.read_text() if report is None else report,
            check_upstream=False,
        )

    def test_fresh_executable_evidence(self):
        self.assertEqual(
            [],
            checker.validate(
                self.spec,
                self.proof,
                checker.REPORT.read_text(),
            ),
        )

    def test_every_relation_is_constructed_admitted_and_evaluated(self):
        axes = {axis["arity"]: axis for axis in self.proof["enumeration_axes"]}
        self.assertEqual(31, axes[1]["evaluated"])
        self.assertEqual(66067, axes[2]["evaluated"])
        self.assertEqual(
            66098,
            self.proof["cost_accounting"][
                "relation_interpretations_constructed_and_evaluated"
            ],
        )
        for axis in axes.values():
            self.assertEqual(
                "materialize-validate-evaluate-v3", axis["algorithm"]
            )
            self.assertEqual(axis["constructed"], axis["admissible"])
            self.assertEqual(axis["admissible"], axis["evaluated"])
            self.assertEqual(0, axis["rejected"])
            self.assertTrue(axis["execution_digest"])
            self.assertTrue(axis["result_digest"])
            for row in axis["per_size"]:
                self.assertEqual(row["interpretations"], row["constructed"])
                self.assertEqual(row["constructed"], row["admissible"])
                self.assertEqual(row["admissible"], row["evaluated"])

    def test_axis_calls_constructor_and_evaluator_for_every_mask(self):
        original_constructor = checker.relation_from_mask
        original_evaluator = checker.evaluate_relation
        calls = {"construct": 0, "evaluate": 0}

        def counted_constructor(carrier, arity, mask):
            calls["construct"] += 1
            return original_constructor(carrier, arity, mask)

        def counted_evaluator(carrier, arity, relation):
            calls["evaluate"] += 1
            return original_evaluator(carrier, arity, relation)

        expected = sum(1 << (n**2) for n in range(3))
        with mock.patch.object(
            checker, "relation_from_mask", counted_constructor
        ), mock.patch.object(checker, "evaluate_relation", counted_evaluator):
            summary = checker.enumerate_axis(2, 2)
        self.assertEqual(expected, summary["evaluated"])
        self.assertEqual(expected, calls["construct"])
        self.assertEqual(expected, calls["evaluate"])

    def test_relation_content_drives_reduct_evaluation_and_result_digest(self):
        empty = checker.evaluate_relation(("o0",), 1, ())
        full = checker.evaluate_relation(("o0",), 1, (("o0",),))
        self.assertTrue(empty["paired_reduct_verified"])
        self.assertTrue(full["paired_reduct_verified"])
        self.assertEqual(empty["reduct_digest"], full["reduct_digest"])
        self.assertNotEqual(
            empty["alternate_relation_digest"], full["alternate_relation_digest"]
        )

        baseline = checker.enumerate_axis(2, 2)
        original_evaluator = checker.evaluate_relation

        def changed_evaluator(carrier, arity, relation):
            result = original_evaluator(carrier, arity, relation)
            result["content_checksum"] = checker.digest(relation)
            return result

        with mock.patch.object(checker, "evaluate_relation", changed_evaluator):
            changed = checker.enumerate_axis(2, 2)
        self.assertEqual(baseline["execution_digest"], changed["execution_digest"])
        self.assertNotEqual(baseline["result_digest"], changed["result_digest"])

        with mock.patch.object(
            checker, "relation_from_mask", lambda carrier, arity, mask: ()
        ):
            with self.assertRaises(ValueError):
                checker.enumerate_axis(1, 1)

    def test_countermodel_coverage_is_truthful_admissible_and_bounded(self):
        expected_supported = {
            "Object": [1, 2, 3, 4],
            "Property": [1, 2, 3, 4],
            "Relation": [1, 2, 3, 4],
            "Representation": [1, 2, 3, 4],
            "Interpretation": [1, 2, 3, 4],
            "Investigation": [0, 1, 2, 3, 4],
            "ReasoningCalculus": [0, 1, 2, 3, 4],
        }
        evidence = self.proof["countermodel_evidence"]
        self.assertEqual(30, evidence["witness_count"])
        self.assertEqual(60, evidence["model_count"])
        self.assertEqual(60, self.proof["cost_accounting"]["paired_reduct_models"])
        for target, bounds in expected_supported.items():
            self.assertEqual(
                bounds,
                self.proof["countermodel_coverage"][target]["supported_bounds"],
            )
        records, coverage = checker.build_countermodels(self.spec)
        self.assertEqual(
            evidence, checker.summarize_countermodels(records, coverage)
        )
        for record in records:
            self.assertEqual([], checker.validate_countermodel(record, 4))
            self.assertLessEqual(
                max(record["actual_carrier_sizes"]), record["support_bound"]
            )
            if record["target"] == "Object":
                self.assertEqual(
                    [record["support_bound"] - 1, record["support_bound"]],
                    record["actual_carrier_sizes"],
                )

    def test_invalid_witnesses_fail_even_when_verified_is_forged(self):
        valid = checker.countermodel("Object", 4, 4)
        self.assertIsNotNone(valid)
        overflow = copy.deepcopy(valid)
        overflow["model_b"]["Object"].append("o4")
        overflow["verified"] = True
        self.assertTrue(checker.validate_countermodel(overflow, 4))

        malformed = {
            "target": "Property",
            "support_bound": 0,
            "actual_carrier_sizes": [0, 0],
            "model_a": checker.base_model(0),
            "model_b": checker.base_model(0),
            "reduct_a": {},
            "reduct_b": {},
            "verified": True,
            "validation_errors": [],
        }
        malformed["model_b"]["Property"] = [[]]
        self.assertTrue(checker.validate_countermodel(malformed, 4))

        external = copy.deepcopy(checker.countermodel("Representation", 1, 4))
        external["model_b"]["Representation"] = {"t0": "external"}
        external["verified"] = True
        self.assertTrue(checker.validate_countermodel(external, 4))

        orphan = copy.deepcopy(checker.countermodel("Interpretation", 1, 4))
        orphan["model_b"]["Representation"] = {}
        orphan["verified"] = True
        self.assertTrue(checker.validate_countermodel(orphan, 4))

        tampered = copy.deepcopy(valid)
        tampered["actual_carrier_sizes"] = [4, 4]
        tampered["verified"] = True
        self.assertTrue(checker.validate_countermodel(tampered, 4))

    def test_stale_fabricated_incomplete_and_overclaimed_proofs_fail_closed(self):
        mutations = [
            lambda proof: proof.__setitem__("spec_digest", "0" * 64),
            lambda proof: proof["enumeration_axes"].pop(),
            lambda proof: proof["countermodel_evidence"]["by_target"].pop(),
            lambda proof: proof["countermodel_coverage"]["Object"].__setitem__(
                "unsupported_bounds", []
            ),
            lambda proof: proof["unknown_cases"].__setitem__("oracle", "Pass"),
            lambda proof: proof["conclusions"].__setitem__(
                "foundation", "global superiority"
            ),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                proof = copy.deepcopy(self.proof)
                mutation(proof)
                self.assertTrue(self.validate_without_upstream(proof=proof))

    def test_historical_identities_are_fixed_and_write_cannot_bless_mutation(self):
        self.assertEqual(
            self.spec["historical_artifacts"], self.proof["historical_artifacts"]
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            isolated = copy.deepcopy(self.spec)
            for index, (relative, record) in enumerate(
                isolated["historical_artifacts"].items()
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                data = f"immutable-{index}\n".encode()
                path.write_bytes(data)
                record["git_blob_sha"] = checker.git_blob_sha(data)
            victim = root / next(iter(isolated["historical_artifacts"]))
            victim.write_text(victim.read_text() + "mutated\n")
            with self.assertRaises(ValueError):
                checker.write_all(isolated, root=root, validate_upstream=False)

    def test_report_and_external_boundary_fail_closed(self):
        self.assertEqual(
            {
                "oracle": "Unknown",
                "continuous": "Unknown",
                "hybrid": "Unknown",
                "embodied": "Unknown",
            },
            self.proof["unknown_cases"],
        )
        errors = self.validate_without_upstream(
            report=checker.REPORT.read_text() + "fabricated\n"
        )
        self.assertIn("stale report", errors)


if __name__ == "__main__":
    unittest.main()
