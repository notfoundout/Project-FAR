from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1"
RAW = RECORD / "CRE-001-E01-claude-sonnet-medium-pilot-v1.raw.json"
META = RECORD / "CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json"
REVIEW = RECORD / "CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md"

class Cre001PilotArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw_bytes = RAW.read_bytes()
        self.raw = json.loads(self.raw_bytes)
        self.meta = json.loads(META.read_text(encoding="utf-8"))
        self.review = REVIEW.read_text(encoding="utf-8")

    def test_raw_artifact_exists_and_is_valid_json(self) -> None:
        self.assertTrue(RAW.is_file())
        self.assertIsInstance(self.raw, dict)

    def test_checksum_and_byte_count_match_metadata(self) -> None:
        self.assertEqual(hashlib.sha256(self.raw_bytes).hexdigest(), self.meta["raw_artifact_checksum_sha256"])
        self.assertEqual(len(self.raw_bytes), self.meta["raw_artifact_byte_count"])
        self.assertEqual(self.meta["raw_artifact_checksum_algorithm"], "SHA-256")

    def test_metadata_points_to_exact_raw_artifact(self) -> None:
        self.assertEqual(ROOT / self.meta["raw_artifact_path"], RAW)
        self.assertTrue(self.meta["raw_artifact_immutable"])
        self.assertFalse(self.meta["raw_preservation_pending"])

    def test_pilot_is_noncanonical_excluded_and_concluded(self) -> None:
        self.assertFalse(self.meta["canonical_cre_001_primary_mapping"])
        self.assertFalse(self.meta["canonical_ingestion_eligibility"])
        self.assertIn("pilot-artifacts", RAW.parts)
        self.assertEqual(self.meta["pilot_track_status"], "concluded")
        self.assertEqual(self.meta["pilot_track_disposition"], "superseded by deterministic verification")
        self.assertEqual(self.meta["next_action"], "build deterministic CRE-001 verifier")
        self.assertIn("correction loop intentionally stopped", self.meta["evaluator_rerun_status"])

    def test_review_is_separate_from_raw_output(self) -> None:
        forbidden = {"reviewer_status", "finding_identifiers", "canonical_ingestion_eligibility", "noncanonical_reasons"}
        self.assertTrue(forbidden.isdisjoint(self.raw.keys()))
        self.assertIn("Required corrections identified during review", self.review)
        self.assertIn("Why the evaluator track was concluded", self.review)
        self.assertNotIn("Required corrections identified during review", RAW.read_text(encoding="utf-8"))

    def test_official_outputs_do_not_reference_raw_pilot(self) -> None:
        official_roots = [
            ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/execution/validated-submissions",
            ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/execution/adjudication",
            ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/execution/metric-outputs",
            ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/results",
        ]
        needle = RAW.name
        for official_root in official_roots:
            if not official_root.exists():
                continue
            for path in official_root.rglob("*"):
                if path.is_file():
                    self.assertNotIn(needle, path.read_text(encoding="utf-8", errors="ignore"), str(path))

if __name__ == "__main__":
    unittest.main()
