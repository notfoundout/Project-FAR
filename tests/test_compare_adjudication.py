from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from mechanization.far_mechanization.compare_adjudication import (
    ADJUDICATION_SCHEMA,
    COMPARISON_SCHEMA,
    PACKAGE_SCHEMA,
    InterfaceError,
    adjudicate,
    artifact_sha256,
    canonical_json_bytes,
    compare_packages,
    main,
    normalize_package,
)


def package(package_id: str, *, alternate: bool = False) -> dict:
    claims = [
        {
            "claim_id": "claim.temperature",
            "statement": "Temperature exceeded the configured threshold" if not alternate else "Temperature did not exceed the configured threshold",
            "status": "observed" if not alternate else "contradicted",
            "support": ["trace.sensor-1"],
            "assumptions": ["sensor-1 calibrated"],
            "contradicts": [],
            "boundaries": ["single execution"],
        },
        {
            "claim_id": "claim.action",
            "statement": "The controller entered caution mode",
            "status": "derived",
            "support": ["rule.R4", "trace.transition-9"],
            "assumptions": [],
            "contradicts": [],
            "boundaries": ["recorded transition only"],
        },
    ]
    if alternate:
        claims.pop()
        claims.append(
            {
                "claim_id": "claim.new",
                "statement": "A new rule was proposed",
                "status": "declared",
                "support": ["proposal.P1"],
                "assumptions": [],
                "contradicts": [],
                "boundaries": ["proposal, not acceptance"],
            }
        )
    return {
        "schema": PACKAGE_SCHEMA,
        "package_id": package_id,
        "subject_id": "run-001",
        "claims": claims,
        "boundaries": ["No benchmark outcome access", "No generalized superiority claim"],
        "metadata": {"producer": "test"},
    }


class PackageValidationTests(unittest.TestCase):
    def test_normalization_is_deterministic_and_sorts_set_like_fields(self) -> None:
        raw = package("pkg-left")
        raw["claims"].reverse()
        raw["boundaries"].reverse()
        normalized = normalize_package(raw)
        self.assertEqual([c["claim_id"] for c in normalized["claims"]], ["claim.action", "claim.temperature"])
        self.assertEqual(canonical_json_bytes(normalized), canonical_json_bytes(normalize_package(copy.deepcopy(raw))))

    def test_unknown_top_level_field_fails_closed(self) -> None:
        raw = package("pkg-left")
        raw["truth"] = True
        with self.assertRaisesRegex(InterfaceError, "unsupported fields"):
            normalize_package(raw)

    def test_unknown_claim_status_fails_closed(self) -> None:
        raw = package("pkg-left")
        raw["claims"][0]["status"] = "proven"
        with self.assertRaisesRegex(InterfaceError, "unsupported"):
            normalize_package(raw)

    def test_duplicate_claim_id_fails_closed(self) -> None:
        raw = package("pkg-left")
        raw["claims"].append(copy.deepcopy(raw["claims"][0]))
        with self.assertRaisesRegex(InterfaceError, "duplicate claim_id"):
            normalize_package(raw)

    def test_unknown_contradiction_reference_fails_closed(self) -> None:
        raw = package("pkg-left")
        raw["claims"][0]["contradicts"] = ["claim.missing"]
        with self.assertRaisesRegex(InterfaceError, "unknown claim IDs"):
            normalize_package(raw)

    def test_nested_metadata_extension_channel_is_rejected(self) -> None:
        raw = package("pkg-left")
        raw["metadata"]["hidden"] = {"truth": True}
        with self.assertRaisesRegex(InterfaceError, "JSON scalar"):
            normalize_package(raw)


class ComparisonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.left = package("pkg-left")
        self.right = package("pkg-right", alternate=True)

    def test_comparison_is_deterministic_and_content_addressed(self) -> None:
        first = compare_packages(self.left, self.right)
        second = compare_packages(copy.deepcopy(self.left), copy.deepcopy(self.right))
        self.assertEqual(first, second)
        self.assertEqual(first["schema"], COMPARISON_SCHEMA)
        self.assertTrue(first["comparison_id"].startswith("comparison-"))
        self.assertEqual(first["claim_boundary"], "Mechanical comparison only; no truth, policy, or normative determination.")

    def test_comparison_preserves_contradiction_and_one_sided_claims(self) -> None:
        result = compare_packages(self.left, self.right)
        classes = {finding["claim_id"]: finding["classification"] for finding in result["findings"]}
        self.assertEqual(classes["claim.temperature"], "contradiction")
        self.assertEqual(classes["claim.action"], "left_only")
        self.assertEqual(classes["claim.new"], "right_only")

    def test_input_order_is_semantically_canonical(self) -> None:
        reordered = copy.deepcopy(self.left)
        reordered["claims"].reverse()
        reordered["boundaries"].reverse()
        self.assertEqual(compare_packages(self.left, self.right), compare_packages(reordered, self.right))

    def test_identical_packages_are_not_a_comparison(self) -> None:
        left = package("pkg-left")
        with self.assertRaisesRegex(InterfaceError, "distinct canonical packages"):
            compare_packages(left, copy.deepcopy(left))

    def test_left_and_right_orientation_is_preserved(self) -> None:
        forward = compare_packages(self.left, self.right)
        reverse = compare_packages(self.right, self.left)
        self.assertNotEqual(forward["comparison_id"], reverse["comparison_id"])
        self.assertEqual(forward["left"]["package_id"], "pkg-left")
        self.assertEqual(reverse["left"]["package_id"], "pkg-right")


class AdjudicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.comparison = compare_packages(package("pkg-left"), package("pkg-right", alternate=True))

    def record(self) -> dict:
        return {
            "schema": ADJUDICATION_SCHEMA,
            "comparison_sha256": artifact_sha256(self.comparison),
            "adjudicator": "reviewer-001",
            "decisions": [
                {
                    "finding_id": finding["finding_id"],
                    "disposition": "unresolved",
                    "rationale": "The bounded evidence does not justify selecting either side.",
                    "support": [],
                    "limitations": ["No domain expert review"],
                }
                for finding in self.comparison["findings"]
            ],
            "dissent": ["Reviewer-002 preferred additional evidence collection"],
            "metadata": {"policy": "test-policy-v1"},
        }

    def test_adjudication_is_separate_deterministic_and_preserves_dissent(self) -> None:
        result = adjudicate(self.comparison, self.record())
        self.assertEqual(result["schema"], ADJUDICATION_SCHEMA)
        self.assertTrue(result["adjudication_id"].startswith("adjudication-"))
        self.assertEqual(result["dissent"], ["Reviewer-002 preferred additional evidence collection"])
        self.assertIn("not a truth certificate", result["claim_boundary"])
        self.assertEqual(result, adjudicate(copy.deepcopy(self.comparison), self.record()))

    def test_tampered_comparison_hash_is_rejected(self) -> None:
        record = self.record()
        record["comparison_sha256"] = "0" * 64
        with self.assertRaisesRegex(InterfaceError, "does not match"):
            adjudicate(self.comparison, record)

    def test_missing_decision_is_rejected_instead_of_silently_dropped(self) -> None:
        record = self.record()
        record["decisions"].pop()
        with self.assertRaisesRegex(InterfaceError, "explicitly decide every finding"):
            adjudicate(self.comparison, record)

    def test_unknown_finding_is_rejected(self) -> None:
        record = self.record()
        record["decisions"][0]["finding_id"] = "finding-missing"
        with self.assertRaisesRegex(InterfaceError, "unknown finding"):
            adjudicate(self.comparison, record)

    def test_duplicate_decision_is_rejected(self) -> None:
        record = self.record()
        record["decisions"].append(copy.deepcopy(record["decisions"][0]))
        with self.assertRaisesRegex(InterfaceError, "duplicate adjudication decision"):
            adjudicate(self.comparison, record)

    def test_normative_truth_disposition_is_rejected(self) -> None:
        record = self.record()
        record["decisions"][0]["disposition"] = "proven_true"
        with self.assertRaisesRegex(InterfaceError, "unsupported"):
            adjudicate(self.comparison, record)

    def test_forged_content_id_is_rejected(self) -> None:
        record = self.record()
        record["adjudication_id"] = "adjudication-forged"
        with self.assertRaisesRegex(InterfaceError, "does not match"):
            adjudicate(self.comparison, record)


class CLITests(unittest.TestCase):
    def test_cli_compare_and_adjudicate_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left_path = root / "left.json"
            right_path = root / "right.json"
            comparison_path = root / "comparison.json"
            adjudication_path = root / "adjudication.json"
            result_path = root / "result.json"
            left_path.write_text(json.dumps(package("pkg-left")), encoding="utf-8")
            right_path.write_text(json.dumps(package("pkg-right", alternate=True)), encoding="utf-8")

            self.assertEqual(main(["compare", str(left_path), str(right_path), "--output-file", str(comparison_path)]), 0)
            comparison = json.loads(comparison_path.read_text(encoding="utf-8"))
            record = {
                "schema": ADJUDICATION_SCHEMA,
                "comparison_sha256": artifact_sha256(comparison),
                "adjudicator": "reviewer-001",
                "decisions": [
                    {
                        "finding_id": finding["finding_id"],
                        "disposition": "unresolved",
                        "rationale": "Insufficient bounded evidence.",
                        "support": [],
                        "limitations": [],
                    }
                    for finding in comparison["findings"]
                ],
                "dissent": [],
            }
            adjudication_path.write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(main(["adjudicate", str(comparison_path), str(adjudication_path), "--output-file", str(result_path)]), 0)
            self.assertEqual(json.loads(result_path.read_text(encoding="utf-8"))["schema"], ADJUDICATION_SCHEMA)

    def test_cli_failure_is_nonzero_and_explained(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{}", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["validate-package", str(path)])
            self.assertEqual(code, 2)
            self.assertIn("missing required fields", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
