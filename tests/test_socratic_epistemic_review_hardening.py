from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from mechanization.far_mechanization.socratic_epistemic import (
    validate_expertise_applicability_binding,
    validate_epistemic_boundary_binding,
    validate_socratic_record,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "socratic-epistemic-extensions"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def codes(document: dict) -> set[str]:
    return {item.code for item in validate_socratic_record(document).diagnostics}


class SocraticEpistemicReviewHardeningTests(unittest.TestCase):
    def test_whitespace_only_required_strings_and_bridges_are_rejected(self) -> None:
        for field in ("applicability_id", "basis"):
            document = load("valid-expertise-applicability.json")
            document["record"][field] = " \t "
            with self.subTest(field=field):
                self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))
        document = load("valid-expertise-applicability.json")
        document["record"]["claim_scope"]["domain"] = "economics"
        dimension = document["record"]["dimensions"]["domain"]
        dimension["claim_value"] = "economics"
        dimension["bridge"] = " \t "
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))
        document = load("valid-elenchus-session.json")
        document["record"]["commitments"][1]["context"] = "another context"
        document["record"]["derived_implications"][0]["context_bridges"] = [{
            "premise_ref": "c2", "bridge": " \t ",
        }]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))

    def test_expertise_binding_rejects_expired_or_premature_evaluation(self) -> None:
        applicability = load("valid-expertise-applicability.json")
        assertion = load("valid-expertise-assertion.json")
        assertion["record"]["valid_until"] = "2026-09-23T00:00:00Z"
        for evaluated_at in ("2026-09-22T23:59:59Z", "2026-09-23T00:00:01Z"):
            with self.subTest(evaluated_at=evaluated_at):
                applicability["record"]["evaluated_at"] = evaluated_at
                result = validate_expertise_applicability_binding(
                    applicability, assertion, self.claim_snapshot(applicability),
                )
                self.assertIn("EXPERTISE_EVALUATION_OUTSIDE_VALIDITY", {d.code for d in result.diagnostics})
        applicability["record"]["evaluated_at"] = "2026-09-23T00:00:00Z"
        self.assertTrue(validate_expertise_applicability_binding(
            applicability, assertion, self.claim_snapshot(applicability),
        ).success)

    def test_boundary_binds_entire_view_and_disposition_to_resolved_closure(self) -> None:
        boundary = load("valid-epistemic-boundary.json")
        snapshot = copy.deepcopy(boundary["record"])
        del snapshot["provenance"]
        del snapshot["boundary_version"]
        self.assertTrue(validate_epistemic_boundary_binding(boundary, snapshot).success)
        for field, value in (
            ("claim_version", "2.0"),
            ("evidence_cutoff", "2026-09-24T00:00:00Z"),
            ("search_frame", "different search frame"),
            ("closure_status", "Resolved"),
            ("established", []),
            ("closure_record_refs", ["unrelated.closure"]),
        ):
            with self.subTest(field=field):
                forged = copy.deepcopy(boundary)
                forged["record"][field] = value
                result = validate_epistemic_boundary_binding(forged, snapshot)
                self.assertIn("BOUNDARY_CLOSURE_MISMATCH", {d.code for d in result.diagnostics})
        forged = copy.deepcopy(boundary)
        forged["record"]["claim_disposition"]["status"] = "REFUTED"
        result = validate_epistemic_boundary_binding(forged, snapshot)
        self.assertIn("BOUNDARY_CLOSURE_MISMATCH", {d.code for d in result.diagnostics})

    def test_boundary_disposition_is_required_and_time_bound(self) -> None:
        document = load("valid-epistemic-boundary.json")
        del document["record"]["claim_disposition"]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))
        document = load("valid-epistemic-boundary.json")
        document["record"]["claim_disposition"]["decided_at"] = "yesterday"
        self.assertIn("BOUNDARY_INVALID_DISPOSITION_TIME", codes(document))
        document = load("valid-epistemic-boundary.json")
        document["record"]["claim_disposition"]["status"] = "OTHER"
        self.assertIn("BOUNDARY_INVALID_TARGET_STATUS", codes(document))

    def claim_snapshot(self, applicability: dict) -> dict:
        record = applicability["record"]
        return {
            "claim_id": record["claim_id"],
            "claim_version": record["claim_version"],
            "scope": copy.deepcopy(record["claim_scope"]),
        }

    def test_expertise_applicability_requires_assertion_version(self) -> None:
        applicability = load("valid-expertise-applicability.json")
        del applicability["record"]["expertise_assertion_version"]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(applicability))

    def test_expertise_applicability_requires_claim_version(self) -> None:
        applicability = load("valid-expertise-applicability.json")
        del applicability["record"]["claim_version"]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(applicability))

    def test_expertise_applicability_binds_exact_source_revisions(self) -> None:
        applicability = load("valid-expertise-applicability.json")
        assertion = load("valid-expertise-assertion.json")
        result = validate_expertise_applicability_binding(
            applicability,
            assertion,
            self.claim_snapshot(applicability),
        )
        self.assertTrue(result.success, result.diagnostics)

    def test_expertise_binding_rejects_stale_assertion_version(self) -> None:
        applicability = load("valid-expertise-applicability.json")
        assertion = load("valid-expertise-assertion.json")
        assertion["record"]["version"] = "2.0"
        result = validate_expertise_applicability_binding(
            applicability,
            assertion,
            self.claim_snapshot(applicability),
        )
        self.assertIn(
            "EXPERTISE_ASSERTION_VERSION_MISMATCH",
            {item.code for item in result.diagnostics},
        )

    def test_expertise_binding_rejects_resolved_assertion_scope_drift(self) -> None:
        applicability = load("valid-expertise-applicability.json")
        assertion = load("valid-expertise-assertion.json")
        assertion["record"]["scope"]["method"] = "general medicine"
        result = validate_expertise_applicability_binding(
            applicability,
            assertion,
            self.claim_snapshot(applicability),
        )
        self.assertIn(
            "EXPERTISE_ASSERTION_SCOPE_MISMATCH",
            {item.code for item in result.diagnostics},
        )

    def test_expertise_binding_rejects_stale_claim_version(self) -> None:
        applicability = load("valid-expertise-applicability.json")
        assertion = load("valid-expertise-assertion.json")
        snapshot = self.claim_snapshot(applicability)
        snapshot["claim_version"] = "2.0"
        result = validate_expertise_applicability_binding(applicability, assertion, snapshot)
        self.assertIn(
            "EXPERTISE_CLAIM_VERSION_MISMATCH",
            {item.code for item in result.diagnostics},
        )

    def test_expertise_binding_rejects_resolved_scope_drift(self) -> None:
        applicability = load("valid-expertise-applicability.json")
        assertion = load("valid-expertise-assertion.json")
        snapshot = self.claim_snapshot(applicability)
        snapshot["scope"]["population"] = "children"
        result = validate_expertise_applicability_binding(applicability, assertion, snapshot)
        self.assertIn(
            "EXPERTISE_CLAIM_SCOPE_MISMATCH",
            {item.code for item in result.diagnostics},
        )

    def test_boundary_detail_requires_per_item_basis(self) -> None:
        document = load("valid-epistemic-boundary.json")
        del document["record"]["falsifiers"][0]["basis_refs"]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))

    def test_boundary_detail_cannot_fall_back_to_raw_string(self) -> None:
        document = load("valid-epistemic-boundary.json")
        document["record"]["limitations"] = ["untraceable limitation"]
        self.assertIn("SCHEMA_CONSTRAINT_VIOLATION", codes(document))

    def test_implication_rejects_unbridged_context_collapse(self) -> None:
        document = load("valid-elenchus-session.json")
        document["record"]["commitments"][1]["context"] = "unrelated context"
        self.assertIn("ELENCHUS_IMPLICATION_CONTEXT_MISMATCH", codes(document))

    def test_implication_accepts_explicit_context_bridge(self) -> None:
        document = load("valid-elenchus-session.json")
        document["record"]["commitments"][1]["context"] = "adjacent evidentiary context"
        document["record"]["derived_implications"][0]["context_bridges"] = [{
            "premise_ref": "c2",
            "bridge": "The respondent explicitly applies c2 to the definition context for this comparison.",
        }]
        result = validate_socratic_record(document)
        self.assertTrue(result.success, result.diagnostics)

    def test_implication_bridge_must_name_an_actual_premise(self) -> None:
        document = load("valid-elenchus-session.json")
        document["record"]["derived_implications"][0]["context_bridges"] = [{
            "premise_ref": "c3",
            "bridge": "Artificial bridge mutation.",
        }]
        self.assertIn("ELENCHUS_IMPLICATION_BRIDGE_UNKNOWN_PREMISE", codes(document))


if __name__ == "__main__":
    unittest.main()
