from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import reconcile_living_repo as rr


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def candidate(candidate_id: str, *, direct_core_threat: bool = True) -> dict:
    relation = rr.CORE_THREAT_RELATION if direct_core_threat else "HISTORICAL_OR_FOUNDATIONAL_CANDIDATE"
    mode = "incremental" if direct_core_threat else "historical_backfill"
    return {
        "candidate_id": candidate_id,
        "potential_claim_ids": ["FAR-CORE-001"],
        "triage": {"attention_terms": ["counterexample"], "lenses": ["formal_mathematics"]},
        "discovery": {
            "query_bindings": [
                {
                    "target_id": rr.CORE_THREAT_TARGET,
                    "candidate_relation": relation,
                    "mode": mode,
                }
            ]
        },
    }


def registry(rows: list[dict]) -> dict:
    return {
        "schema_version": "1.0",
        "program_id": "FAR-LIVING-REVIEW-DISPOSITIONS-001",
        "authority": "Research",
        "authority_boundary": rr.AUTHORITY_BOUNDARY,
        "allowed_dispositions": sorted(rr.ALLOWED_REVIEW_DISPOSITIONS),
        "reviewed_candidates": rows,
    }


def review_row(candidate_id: str, disposition: str = "ADJACENT_NO_CONTRADICTION") -> dict:
    return {
        "candidate_id": candidate_id,
        "source_key": "doi:10.1/example",
        "disposition": disposition,
        "reviewed_on": "2026-09-10",
        "review_basis": "docs/audits/example.md",
        "suppress_from_core_claim_review_queue": True,
    }


class LivingReviewDispositionTests(unittest.TestCase):
    def test_reviewed_candidate_is_preserved_but_not_requeued(self):
        candidate_id = "FAR-LIT-AAAAAAAAAAAAAAAA"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / rr.CANDIDATE_DIR / f"{candidate_id}.json"
            write_json(path, candidate(candidate_id))
            reviewed = {candidate_id: review_row(candidate_id)}
            queue, counts = rr.candidate_queue(root, {"FAR-CORE-001": []}, reviewed)
            self.assertEqual(queue, [])
            self.assertEqual(counts["candidates"], 1)
            self.assertEqual(counts["direct_core_threat"], 1)
            self.assertEqual(counts["reviewed"], 1)
            self.assertEqual(counts["review_required"], 0)
            self.assertTrue(path.is_file())

    def test_unreviewed_direct_candidate_stays_in_active_queue(self):
        candidate_id = "FAR-LIT-BBBBBBBBBBBBBBBB"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(root / rr.CANDIDATE_DIR / f"{candidate_id}.json", candidate(candidate_id))
            queue, counts = rr.candidate_queue(root, {"FAR-CORE-001": []}, {})
            self.assertEqual([item["candidate_id"] for item in queue], [candidate_id])
            self.assertEqual(counts["direct_core_threat"], 1)
            self.assertEqual(counts["reviewed"], 0)
            self.assertEqual(counts["review_required"], 1)

    def test_historical_candidate_does_not_self_escalate_to_core_queue(self):
        candidate_id = "FAR-LIT-EEEEEEEEEEEEEEEE"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(
                root / rr.CANDIDATE_DIR / f"{candidate_id}.json",
                candidate(candidate_id, direct_core_threat=False),
            )
            queue, counts = rr.candidate_queue(root, {"FAR-CORE-001": []}, {})
            self.assertEqual(queue, [])
            self.assertEqual(counts["historical"], 1)
            self.assertEqual(counts["direct_core_threat"], 0)
            self.assertEqual(counts["review_required"], 0)

    def test_registry_rejects_duplicate_candidate_ids(self):
        candidate_id = "FAR-LIT-CCCCCCCCCCCCCCCC"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(root / rr.REVIEW_DISPOSITIONS_PATH, registry([review_row(candidate_id), review_row(candidate_id)]))
            with self.assertRaisesRegex(rr.ReconciliationError, "duplicate reviewed candidate id"):
                rr.load_review_dispositions(root)

    def test_registry_rejects_unknown_disposition(self):
        candidate_id = "FAR-LIT-DDDDDDDDDDDDDDDD"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(root / rr.REVIEW_DISPOSITIONS_PATH, registry([review_row(candidate_id, "PROVED")]))
            with self.assertRaisesRegex(rr.ReconciliationError, "unknown review disposition"):
                rr.load_review_dispositions(root)

    def test_shipped_registry_retains_material_n1_lead_and_new_reviews(self):
        root = Path(__file__).resolve().parents[1]
        reviewed = rr.load_review_dispositions(root)
        self.assertGreaterEqual(len(reviewed), 19)
        self.assertEqual(reviewed["FAR-LIT-8698902E49C77D94"]["disposition"], "N1_PRIOR_ART_LEAD")
        self.assertEqual(reviewed["FAR-LIT-39EF4FD80D5956BD"]["disposition"], "IRRELEVANT_FALSE_POSITIVE")
        self.assertEqual(reviewed["FAR-LIT-C566FE21125E277F"]["disposition"], "IRRELEVANT_FALSE_POSITIVE")
        self.assertEqual(reviewed["FAR-LIT-DC526D11098789EF"]["disposition"], "ADJACENT_NO_CONTRADICTION")


if __name__ == "__main__":
    unittest.main()
