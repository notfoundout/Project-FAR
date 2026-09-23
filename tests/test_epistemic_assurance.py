from __future__ import annotations

import unittest
import json
from pathlib import Path

from far_validation.epistemic_assurance import (
    EpistemicAssuranceError,
    validate_abstention,
    validate_audit_assurance,
    validate_source_lineage,
    validate_source_lineage_set,
    validate_temporal_state,
)


class SourceLineageTests(unittest.TestCase):
    def test_base_source_rejects_multiple_unjustified_roots_in_schema_and_semantics(self) -> None:
        schema = json.loads((Path(__file__).resolve().parents[1] / "schemas" / "far-source-lineage-v1.schema.json").read_text())
        base_rule = schema["allOf"][0]["then"]["properties"]["root_lineage_ids"]
        self.assertEqual(base_rule["maxItems"], 1)
        for relationship in ("origin", "independent"):
            with self.subTest(relationship=relationship):
                record = {
                    "schema": "far-source-lineage/1.0", "source_id": "base",
                    "relationship": relationship, "upstream_source_ids": [],
                    "root_lineage_ids": ["root-a", "root-b"],
                }
                with self.assertRaisesRegex(EpistemicAssuranceError, "exactly one root"):
                    validate_source_lineage(record)

    def test_dependent_source_requires_upstream(self) -> None:
        with self.assertRaisesRegex(EpistemicAssuranceError, "requires upstream"):
            validate_source_lineage({
                "source_id": "s2",
                "relationship": "copied",
                "upstream_source_ids": [],
                "root_lineage_ids": ["root-a"],
            })

    def test_source_cannot_depend_on_itself(self) -> None:
        with self.assertRaisesRegex(EpistemicAssuranceError, "itself"):
            validate_source_lineage({
                "source_id": "s1",
                "relationship": "copied",
                "upstream_source_ids": ["s1"],
                "root_lineage_ids": ["root-a"],
            })

    def test_multi_origin_derivation_inherits_all_root_lineages(self) -> None:
        records = [
            {"source_id": "a", "relationship": "origin", "upstream_source_ids": [], "root_lineage_ids": ["root-a"]},
            {"source_id": "b", "relationship": "independent", "upstream_source_ids": [], "root_lineage_ids": ["root-b"]},
            {"source_id": "c", "relationship": "mixed_derivation", "upstream_source_ids": ["a", "b"], "root_lineage_ids": ["root-a", "root-b"]},
        ]
        self.assertEqual(validate_source_lineage_set(records), records)

    def test_dependent_lineage_union_cannot_be_forged(self) -> None:
        records = [
            {"source_id": "a", "relationship": "origin", "upstream_source_ids": [], "root_lineage_ids": ["root-a"]},
            {"source_id": "b", "relationship": "copied", "upstream_source_ids": ["a"], "root_lineage_ids": ["fake-root"]},
        ]
        with self.assertRaisesRegex(EpistemicAssuranceError, "upstream lineage union"):
            validate_source_lineage_set(records)

    def test_cycle_is_rejected(self) -> None:
        records = [
            {"source_id": "a", "relationship": "copied", "upstream_source_ids": ["b"], "root_lineage_ids": ["root-a"]},
            {"source_id": "b", "relationship": "copied", "upstream_source_ids": ["a"], "root_lineage_ids": ["root-a"]},
        ]
        with self.assertRaisesRegex(EpistemicAssuranceError, "cycle"):
            validate_source_lineage_set(records)


class TemporalStateTests(unittest.TestCase):
    def test_interval_end_cannot_precede_start(self) -> None:
        with self.assertRaisesRegex(EpistemicAssuranceError, "precedes"):
            validate_temporal_state({
                "subject_id": "e1",
                "state": "active",
                "valid_time": {"start": "2026-09-02T00:00:00Z", "end": "2026-09-01T00:00:00Z"},
                "known_time": {"start": "2026-09-03T00:00:00Z", "end": None},
            })

    def test_superseded_state_names_replacement(self) -> None:
        record = {
            "subject_id": "e1",
            "state": "superseded",
            "valid_time": {"start": "2026-09-01T00:00:00Z", "end": "2026-09-10T00:00:00Z"},
            "known_time": {"start": "2026-09-01T00:00:00Z", "end": None},
            "superseded_by_subject_ids": ["e2"],
        }
        self.assertEqual(validate_temporal_state(record), record)


class AbstentionTests(unittest.TestCase):
    def test_abstention_requires_reopen_condition(self) -> None:
        with self.assertRaisesRegex(EpistemicAssuranceError, "reopen"):
            validate_abstention({
                "target_id": "c1",
                "reason": "source_inaccessible",
                "blocking_dimensions": ["source_integrity"],
                "rationale": "Primary artifact unavailable.",
                "reopen_conditions": [],
            })

    def test_invalid_calibration_is_rejected(self) -> None:
        with self.assertRaisesRegex(EpistemicAssuranceError, "coverage_target"):
            validate_abstention({
                "target_id": "c1",
                "reason": "insufficient_search_coverage",
                "blocking_dimensions": ["search_coverage"],
                "rationale": "Coverage target was not met.",
                "reopen_conditions": ["Run additional retrieval."],
                "calibration": {"coverage_target": 1.1},
            })


class AuditAssuranceTests(unittest.TestCase):
    def test_unknown_or_missing_overall_status_fails_direct_semantic_validation(self) -> None:
        for status in (None, "typo"):
            with self.subTest(status=status):
                record = {
                    "audit_id": "audit-1", "checks": self._checks(),
                    "unresolved_defeaters": [],
                }
                if status is not None:
                    record["overall_status"] = status
                with self.assertRaisesRegex(EpistemicAssuranceError, "overall_status"):
                    validate_audit_assurance(record)

    def _checks(self, status: str = "pass") -> dict:
        names = (
            "source_integrity",
            "interpretation_fidelity",
            "search_coverage",
            "evidence_adjudication",
            "inference_adjudication",
            "reproducibility",
            "hostile_source_isolation",
        )
        return {name: {"status": status, "evidence": ["record-1"]} for name in names}

    def test_assured_rejects_unknown_check(self) -> None:
        checks = self._checks()
        checks["search_coverage"] = {"status": "unknown", "evidence": []}
        with self.assertRaisesRegex(EpistemicAssuranceError, "incompatible"):
            validate_audit_assurance({
                "audit_id": "audit-1",
                "checks": checks,
                "unresolved_defeaters": [],
                "overall_status": "assured",
            })

    def test_pass_requires_evidence(self) -> None:
        checks = self._checks()
        checks["source_integrity"] = {"status": "pass", "evidence": []}
        with self.assertRaisesRegex(EpistemicAssuranceError, "requires evidence"):
            validate_audit_assurance({
                "audit_id": "audit-1",
                "checks": checks,
                "unresolved_defeaters": [],
                "overall_status": "assured",
            })

    def test_assured_rejects_unresolved_defeater(self) -> None:
        with self.assertRaisesRegex(EpistemicAssuranceError, "unresolved"):
            validate_audit_assurance({
                "audit_id": "audit-1",
                "checks": self._checks(),
                "unresolved_defeaters": ["d1"],
                "overall_status": "assured",
            })

    def test_bounded_requires_an_actual_boundary(self) -> None:
        with self.assertRaisesRegex(EpistemicAssuranceError, "requires an unknown"):
            validate_audit_assurance({
                "audit_id": "audit-1",
                "checks": self._checks(),
                "unresolved_defeaters": [],
                "overall_status": "bounded",
            })


if __name__ == "__main__":
    unittest.main()
