from __future__ import annotations

import copy
import unittest

from mechanization.far_mechanization.compare_adjudication import (
    ADJUDICATION_SCHEMA,
    PACKAGE_SCHEMA,
    InterfaceError,
    adjudicate,
    artifact_sha256,
    compare_packages,
    normalize_comparison,
)


def package(package_id: str, statement: str) -> dict:
    return {
        "schema": PACKAGE_SCHEMA,
        "package_id": package_id,
        "subject_id": "subject-001",
        "claims": [
            {
                "claim_id": "claim-001",
                "statement": statement,
                "status": "observed",
                "support": ["evidence-001"],
                "assumptions": [],
                "contradicts": [],
                "boundaries": ["bounded observation"],
            }
        ],
        "boundaries": ["No truth certification"],
        "metadata": {},
    }


class ComparisonIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.comparison = compare_packages(package("left", "A"), package("right", "Not A"))

    def test_canonical_comparison_round_trip(self) -> None:
        self.assertEqual(normalize_comparison(self.comparison), self.comparison)

    def test_forged_comparison_id_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.comparison)
        candidate["comparison_id"] = "comparison-" + "0" * 24
        with self.assertRaisesRegex(InterfaceError, "comparison_id"):
            normalize_comparison(candidate)

    def test_forged_finding_id_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.comparison)
        candidate["findings"][0]["finding_id"] = "finding-" + "0" * 24
        with self.assertRaisesRegex(InterfaceError, "finding_id"):
            normalize_comparison(candidate)

    def test_forged_classification_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.comparison)
        candidate["findings"][0]["classification"] = "agreement"
        with self.assertRaisesRegex(InterfaceError, "classification"):
            normalize_comparison(candidate)

    def test_forged_mechanical_difference_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.comparison)
        candidate["findings"][0]["mechanical_differences"]["statement_equal"] = True
        with self.assertRaisesRegex(InterfaceError, "mechanical_differences"):
            normalize_comparison(candidate)

    def test_forged_summary_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.comparison)
        candidate["summary"] = {"agreement": 1}
        with self.assertRaisesRegex(InterfaceError, "summary"):
            normalize_comparison(candidate)

    def test_noncanonical_finding_order_is_rejected(self) -> None:
        expanded = compare_packages(
            {
                **package("left", "A"),
                "claims": package("left", "A")["claims"]
                + [
                    {
                        "claim_id": "claim-002",
                        "statement": "B",
                        "status": "declared",
                        "support": [],
                        "assumptions": [],
                        "contradicts": [],
                        "boundaries": [],
                    }
                ],
            },
            package("right", "Not A"),
        )
        expanded["findings"].reverse()
        with self.assertRaisesRegex(InterfaceError, "canonical claim order"):
            normalize_comparison(expanded)


class AdjudicationReplayTests(unittest.TestCase):
    def test_canonical_adjudication_can_be_revalidated_without_change(self) -> None:
        comparison = compare_packages(package("left", "A"), package("right", "Not A"))
        raw = {
            "schema": ADJUDICATION_SCHEMA,
            "comparison_sha256": artifact_sha256(comparison),
            "adjudicator": "reviewer-001",
            "decisions": [
                {
                    "finding_id": comparison["findings"][0]["finding_id"],
                    "disposition": "unresolved",
                    "rationale": "Insufficient bounded evidence.",
                    "support": [],
                    "limitations": ["No replication"],
                }
            ],
            "dissent": [],
        }
        canonical = adjudicate(comparison, raw)
        self.assertEqual(adjudicate(comparison, canonical), canonical)

    def test_claim_boundary_tampering_is_rejected(self) -> None:
        comparison = compare_packages(package("left", "A"), package("right", "Not A"))
        raw = {
            "schema": ADJUDICATION_SCHEMA,
            "comparison_sha256": artifact_sha256(comparison),
            "adjudicator": "reviewer-001",
            "decisions": [
                {
                    "finding_id": comparison["findings"][0]["finding_id"],
                    "disposition": "unresolved",
                    "rationale": "Insufficient bounded evidence.",
                    "support": [],
                    "limitations": [],
                }
            ],
            "dissent": [],
            "claim_boundary": "Truth certificate",
        }
        with self.assertRaisesRegex(InterfaceError, "claim_boundary"):
            adjudicate(comparison, raw)


if __name__ == "__main__":
    unittest.main()
