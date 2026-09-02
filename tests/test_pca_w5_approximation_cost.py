from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from mechanization.far_mechanization.contract_v21 import (
    SCHEMA_PATH,
    contract_sha256,
    validate_contract,
)
from tools.check_pca_w5_approximation_cost import audit_manifest

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "conformance/far-ir-2.1"
MANIFEST = ROOT / "research/results/pca-w5-approximation-and-cost/manifest.json"


def load(name: str = "valid-frontier.json") -> dict:
    return json.loads((FIX / name).read_text(encoding="utf-8"))


def codes(document: object) -> set[str]:
    return {diagnostic.code for diagnostic in validate_contract(document).diagnostics}


def rehash(document: dict) -> None:
    document["freeze"]["contract_sha256"] = contract_sha256(document["contract"])


class W5Tests(unittest.TestCase):
    def test_additive_version_preserves_v20(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertEqual(schema["properties"]["format_version"]["const"], "far-ir/2.1")
        predecessor = json.loads((ROOT / "schemas/far-contract-v2.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(predecessor["properties"]["format_version"]["const"], "far-ir/2.0")

    def test_frontier_randomized_and_zero_boundary_controls(self) -> None:
        self.assertTrue(validate_contract(load()).success)
        self.assertTrue(validate_contract(load("valid-zero-boundary.json")).success)

    def test_checked_evidence_requires_explicit_behavior_and_representation(self) -> None:
        document = load()
        document["contract"]["required_behavior"]["status"] = "DECLARED"
        rehash(document)
        self.assertIn("CHECK_REQUIRES_EXPLICIT_BEHAVIOR", codes(document))

        document = load()
        document["contract"]["representation"]["status"] = "Unknown"
        rehash(document)
        self.assertIn("CHECK_REQUIRES_EXPLICIT_REPRESENTATION", codes(document))

    def test_checked_evidence_requires_frozen_contract(self) -> None:
        document = load()
        document["freeze"]["status"] = "DRAFT"
        document["freeze"]["frozen_at"] = None
        document["freeze"]["contract_sha256"] = None
        self.assertIn("CHECK_REQUIRES_FROZEN_CONTRACT", codes(document))

    def test_random_probability_mutation(self) -> None:
        document = load()
        document["report"]["evidence"]["candidates"][0]["decoder_table"][0]["distribution"][0]["probability"] = "1/3"
        self.assertIn("DECODER_NOT_PROBABILITY", codes(document))

    def test_reference_and_aggregation_are_operational(self) -> None:
        document = load()
        document["contract"]["approximation"]["reference"]["weights"][0]["weight"] = "3/4"
        rehash(document)
        self.assertIn("REFERENCE_NOT_PROBABILITY", codes(document))

        document = load()
        document["contract"]["approximation"]["aggregation"] = "maximum"
        rehash(document)
        # Candidate "dominated" has one case loss 1: expected-feasible, maximum-infeasible.
        self.assertIn("FEASIBLE_SET_MISMATCH", codes(document))

    def test_zero_tolerance_expected_boundary_is_reference_support_relative(self) -> None:
        document = load("valid-zero-boundary.json")
        weights = document["contract"]["approximation"]["reference"]["weights"]
        weights[0]["weight"] = "1"
        weights[1]["weight"] = "0"
        # "dominated" is exact on case.zero and wrong only on zero-mass case.one.
        document["report"]["evidence"]["claimed_feasible"] = ["exact", "dominated"]
        document["report"]["evidence"]["exact_recovery_claims"] = ["exact", "dominated"]
        rehash(document)
        result = validate_contract(document)
        self.assertTrue(result.success, result.diagnostics)

    def test_duplicate_reference_case_is_not_silently_aggregated(self) -> None:
        document = load()
        document["contract"]["approximation"]["reference"]["weights"][1]["case_id"] = "case.zero"
        rehash(document)
        self.assertIn("DUPLICATE_REFERENCE_CASE", codes(document))

    def test_incomplete_case_table_fails_closed_without_exception(self) -> None:
        document = load()
        document["contract"]["representation"]["table"].pop()
        rehash(document)
        self.assertIn("CASE_TABLE_COVERAGE_MISMATCH", codes(document))

    def test_metric_axioms_and_loss_link(self) -> None:
        document = load()
        document["contract"]["approximation"]["metric"]["entries"][1]["distance"] = "0"
        rehash(document)
        diagnostics = codes(document)
        self.assertIn("METRIC_SEPARATION_FAILURE", diagnostics)
        self.assertIn("LOSS_METRIC_MISMATCH", diagnostics)

    def test_tolerance_is_not_implicit(self) -> None:
        document = load()
        document["contract"]["approximation"]["tolerance"] = "1/3"
        rehash(document)
        self.assertIn("FEASIBLE_SET_MISMATCH", codes(document))

    def test_pareto_is_not_least(self) -> None:
        document = load()
        document["report"]["evidence"]["claimed_least_elements"] = ["exact"]
        self.assertIn("LEAST_SET_MISMATCH", codes(document))

        document = load()
        document["report"]["evidence"]["claimed_pareto_minimal"] = ["exact"]
        self.assertIn("PARETO_SET_MISMATCH", codes(document))

    def test_cost_is_multidimensional_partial_order(self) -> None:
        document = load()
        document["report"]["evidence"]["candidates"][0]["costs"][0]["dimension_id"] = "evaluation"
        self.assertIn("COST_COVERAGE_MISMATCH", codes(document))

    def test_duplicate_decoder_action_is_not_silently_aggregated(self) -> None:
        document = load()
        distribution = document["report"]["evidence"]["candidates"][0]["decoder_table"][0]["distribution"]
        distribution[1]["action"] = False
        self.assertIn("DUPLICATE_DECODER_ACTION", codes(document))

    def test_false_exact_recovery_rejected(self) -> None:
        document = load()
        document["report"]["evidence"]["exact_recovery_claims"].append("randomized")
        self.assertIn("EXACT_RECOVERY_SET_MISMATCH", codes(document))

    def test_freeze_provenance_binding(self) -> None:
        document = load()
        document["contract"]["frame"]["description"] = "mutation"
        self.assertIn("FREEZE_HASH_MISMATCH", codes(document))


class W5ManifestTests(unittest.TestCase):
    def load_manifest(self) -> dict:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_governed_manifest_passes_independent_audit(self) -> None:
        self.assertEqual(audit_manifest(ROOT, self.load_manifest()), [])

    def test_manifest_cannot_make_checked_record_loop_vacuous(self) -> None:
        manifest = self.load_manifest()
        manifest["checked_records"] = []
        errors = audit_manifest(ROOT, manifest)
        self.assertTrue(any(error.startswith("W5_CHECKED_RECORD_SET_MISMATCH") for error in errors))

    def test_manifest_cannot_make_artifact_loop_vacuous(self) -> None:
        manifest = self.load_manifest()
        manifest["artifacts"] = []
        errors = audit_manifest(ROOT, manifest)
        self.assertTrue(any(error.startswith("W5_ARTIFACT_SET_MISMATCH") for error in errors))

    def test_manifest_must_bind_semantic_verifier_and_campaign_checker(self) -> None:
        manifest = self.load_manifest()
        manifest["artifacts"] = [
            item
            for item in manifest["artifacts"]
            if item["path"]
            not in {
                "mechanization/far_mechanization/contract_v21.py",
                "tools/check_pca_w5_approximation_cost.py",
            }
        ]
        errors = audit_manifest(ROOT, manifest)
        self.assertTrue(any(error.startswith("W5_ARTIFACT_SET_MISMATCH") for error in errors))

    def test_manifest_metadata_cannot_promote_an_unregistered_verdict(self) -> None:
        manifest = self.load_manifest()
        manifest["terminal_verdict"] = "PROVED_UNIVERSALLY"
        errors = audit_manifest(ROOT, manifest)
        self.assertTrue(any(error.startswith("W5_MANIFEST_METADATA_MISMATCH terminal_verdict") for error in errors))


class W5LeanAlignmentTests(unittest.TestCase):
    def test_pinned_workflow_compiles_w5_artifact(self) -> None:
        workflow = (ROOT / ".github/workflows/pca-w5.yml").read_text(encoding="utf-8")
        self.assertIn("lean mechanization/lean/W5ApproximationCost.lean", workflow)
        self.assertEqual(
            (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip(),
            "leanprover/lean4:v4.19.0",
        )

    def test_w5_artifact_has_no_admissions(self) -> None:
        source = (ROOT / "mechanization/lean/W5ApproximationCost.lean").read_text(encoding="utf-8")
        for forbidden in ("sorry", "admit", "axiom "):
            self.assertNotIn(forbidden, source)
        for theorem in (
            "random_not_leq_exact",
            "exact_not_leq_random",
            "no_least_of_two",
            "zero_sum_boundary",
        ):
            self.assertIn(f"theorem {theorem}", source)


if __name__ == "__main__":
    unittest.main()
