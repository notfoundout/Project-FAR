from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from mechanization.far_mechanization.socratic_epistemic import (
    FORMAT_VERSION,
    SCHEMA_PATH,
    validate_socratic_record,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "socratic-epistemic-extensions"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def codes(document: dict) -> set[str]:
    return {item.code for item in validate_socratic_record(document).diagnostics}


class SocraticEpistemicExtensionTests(unittest.TestCase):
    def test_schema_is_valid_and_versioned(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertEqual(FORMAT_VERSION, "socratic-epistemic-extensions/1.0")
        self.assertEqual(schema["properties"]["schema_version"]["const"], FORMAT_VERSION)

    def test_all_positive_fixtures_validate(self) -> None:
        names = [
            "valid-expertise-assertion.json",
            "valid-expertise-applicability.json",
            "valid-epistemic-boundary.json",
            "valid-elenchus-session.json",
        ]
        for name in names:
            with self.subTest(name=name):
                result = validate_socratic_record(load(name))
                self.assertTrue(result.success, result.diagnostics)

    def test_expertise_cannot_transfer_domains_by_assertion(self) -> None:
        document = load("valid-expertise-applicability.json")
        document["record"]["claim_scope"]["domain"] = "economics"
        document["record"]["dimensions"]["domain"]["claim_value"] = "economics"
        self.assertIn("UNJUSTIFIED_EXPERTISE_MATCH", codes(document))

    def test_supported_expertise_rejects_material_scope_mismatch(self) -> None:
        document = load("valid-expertise-applicability.json")
        document["record"]["claim_scope"]["domain"] = "economics"
        assessment = document["record"]["dimensions"]["domain"]
        assessment["claim_value"] = "economics"
        assessment["status"] = "MISMATCH"
        assessment["rationale"] = "Different domains"
        self.assertIn("EXPERTISE_SCOPE_OVERREACH", codes(document))

    def test_expertise_dimension_values_must_be_bound_to_scopes(self) -> None:
        document = load("valid-expertise-applicability.json")
        document["record"]["dimensions"]["method"]["claim_value"] = "survey analysis"
        self.assertIn("EXPERTISE_DIMENSION_VALUE_MISMATCH", codes(document))

    def test_epistemic_boundary_requires_reason_for_unknown(self) -> None:
        document = load("valid-epistemic-boundary.json")
        del document["record"]["unknown"][0]["reason"]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))

    def test_epistemic_boundary_requires_conditions_for_conditional_claim(self) -> None:
        document = load("valid-epistemic-boundary.json")
        del document["record"]["conditionally_established"][0]["condition_refs"]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))

    def test_epistemic_boundary_prevents_cross_category_collapse(self) -> None:
        document = load("valid-epistemic-boundary.json")
        duplicate = copy.deepcopy(document["record"]["established"][0])
        duplicate["reason"] = "Artificial mutation"
        document["record"]["unknown"].append(duplicate)
        self.assertIn("BOUNDARY_CATEGORY_COLLISION", codes(document))

    def test_closed_boundary_must_reference_canonical_closure_record(self) -> None:
        document = load("valid-epistemic-boundary.json")
        document["record"]["closure_record_refs"] = []
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))

    def test_elenchus_response_must_reference_recorded_question(self) -> None:
        document = load("valid-elenchus-session.json")
        document["record"]["response_events"][0]["question_id"] = "missing-question"
        self.assertIn("ELENCHUS_RESPONSE_UNKNOWN_QUESTION", codes(document))

    def test_elenchus_revision_cannot_overwrite_commitment(self) -> None:
        document = load("valid-elenchus-session.json")
        revision = document["record"]["revisions"][0]
        revision["to_commitment_id"] = revision["from_commitment_id"]
        self.assertIn("ELENCHUS_REVISION_OVERWRITES_HISTORY", codes(document))

    def test_elenchus_revision_requires_monotone_version(self) -> None:
        document = load("valid-elenchus-session.json")
        document["record"]["commitments"][2]["version"] = 1
        self.assertIn("ELENCHUS_REVISION_VERSION_ORDER", codes(document))

    def test_elenchus_contradiction_requires_explicit_basis_and_calculus(self) -> None:
        document = load("valid-elenchus-session.json")
        document["record"]["contradictions"] = [{
            "id": "x1",
            "commitment_refs": ["c2", "c3"],
            "interpretation": "same context",
            "basis": "claimed incompatibility"
        }]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))

    def test_elenchus_contradiction_references_existing_commitments(self) -> None:
        document = load("valid-elenchus-session.json")
        document["record"]["contradictions"] = [{
            "id": "x1",
            "commitment_refs": ["c2", "missing"],
            "interpretation": "same context",
            "calculus": "classical propositional logic",
            "basis": "P and not-P"
        }]
        self.assertIn("ELENCHUS_CONTRADICTION_UNKNOWN_COMMITMENT", codes(document))

    def test_elenchus_derived_implication_must_name_recorded_premises(self) -> None:
        document = load("valid-elenchus-session.json")
        document["record"]["derived_implications"][0]["premise_refs"] = ["missing"]
        self.assertIn("ELENCHUS_IMPLICATION_UNKNOWN_PREMISE", codes(document))


if __name__ == "__main__":
    unittest.main()
