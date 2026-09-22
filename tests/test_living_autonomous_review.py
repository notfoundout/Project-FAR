from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tools import run_living_autonomous_review as ar

ROOT = Path(__file__).resolve().parents[1]
CID = "FAR-LIT-FFFFFFFF00000001"
NOW = datetime(2026, 9, 22, 20, 0, tzinfo=timezone.utc)


def meta(ok: bool = True):
    return {
        "model": "fake",
        "url_context_metadata": {
            "urlMetadata": [{
                "retrievedUrl": "https://doi.org/10.0000/far-test",
                "urlRetrievalStatus": "URL_RETRIEVAL_STATUS_SUCCESS" if ok else "URL_RETRIEVAL_STATUS_ERROR",
            }]
        },
        "grounding_metadata": {},
        "usage_metadata": {},
    }


class FakeModel:
    def __init__(self, disposition: str, *, verified: bool = True, implementation: bool = False):
        self.disposition = disposition
        self.verified = verified
        self.implementation = implementation
        self.calls = []

    def generate(self, *, role, prompt, schema, urls=None):
        self.calls.append(role)
        if role == "screening":
            return {
                "primary_source_verified": self.verified,
                "relevant": True,
                "source_urls_used": ["https://doi.org/10.0000/far-test"],
                "affected_claim_ids": ["FAR-CORE-001"],
                "premise_match": True,
                "scope_match": True,
                "summary": "Direct source review.",
                "evidence_locations": ["primary source"],
                "limits": [],
            }, meta(self.verified)
        if role == "attack":
            change = self.disposition == "PROJECT_CHANGE_REQUIRED"
            prior = self.disposition == "N1_PRIOR_ART_LEAD"
            return {
                "contradiction_found": change,
                "prior_art_found": prior,
                "affected_claim_ids": ["FAR-CORE-001"] if (change or prior) else [],
                "exact_reason": "bounded attack",
                "reproducible_attack": "construct the bound counterexample" if change else "",
                "source_locations": ["primary source"],
                "limits": [],
            }, meta()
        if role == "replication":
            change = self.disposition == "PROJECT_CHANGE_REQUIRED"
            prior = self.disposition == "N1_PRIOR_ART_LEAD"
            return {
                "contradiction_found": change,
                "prior_art_found": prior,
                "affected_claim_ids": ["FAR-CORE-001"] if (change or prior) else [],
                "independent_reason": "independent bounded check",
                "attack_reproduced": change,
                "source_locations": ["primary source"],
                "limits": [],
            }, meta()
        if role == "adjudication":
            change = self.disposition == "PROJECT_CHANGE_REQUIRED"
            return {
                "disposition": self.disposition,
                "project_change_required": change,
                "scientific_targets": ["docs/research/living-autonomous-test.md"] if change else [],
                "implementation_required": self.implementation if change else False,
                "implementation_targets": ["tools/living-autonomous-test.py"] if (change and self.implementation) else [],
                "rationale": "test adjudication",
                "limits": [],
            }, {}
        if role == "scientific_change_generator":
            return {"files": [{"path": "docs/research/living-autonomous-test.md", "content": "# corrected\n"}]}, {}
        if role == "implementation_change_generator":
            return {"files": [{"path": "tools/living-autonomous-test.py", "content": "VALUE = 1\n"}]}, {}
        raise AssertionError(role)


def source_fixture(root: Path):
    candidate = {
        "schema_version": "1.0",
        "record_type": "CANDIDATE_LITERATURE",
        "authority": "Research",
        "authority_boundary": "Research candidate only.",
        "candidate_id": CID,
        "source_key": "doi:10.0000/far-test",
        "sources": [{
            "provider": "OpenAlex",
            "doi": "10.0000/far-test",
            "url": "https://doi.org/10.0000/far-test",
            "title": "FAR test source",
        }],
        "potential_claim_ids": ["FAR-CORE-001"],
        "lifecycle": {"stage": "DISCOVERED"},
        "triage": {"status": "UNREVIEWED_CANDIDATE"},
    }
    path = root / ar.CANDIDATES / f"{CID}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(candidate, sort_keys=True) + "\n", encoding="utf-8")
    state = {
        "core_claim_review_queue": [{
            "candidate_id": CID,
            "claim_ids": ["FAR-CORE-001"],
            "downstream_claim_ids": ["FAR-CORE-002"],
            "attention_terms": ["counterexample"],
        }]
    }
    p = root / ar.STATE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, sort_keys=True) + "\n", encoding="utf-8")


class AutonomousLivingReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.source = Path(self.tmp.name)
        source_fixture(self.source)

    def tearDown(self):
        self.tmp.cleanup()

    def test_source_verification_failure_records_retry_only(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("ADJACENT_NO_CONTRADICTION", verified=False), NOW)
        self.assertEqual("source_blocked", plan["status"])
        self.assertFalse(plan["review_files"])
        attempt = next(iter(plan["inbox_files"]))
        self.assertIn("autonomous-review-attempts", attempt)

    def test_adjacent_review_prepares_human_authority_pr_bytes(self):
        model = FakeModel("ADJACENT_NO_CONTRADICTION")
        plan = ar.build_plan(ROOT, self.source, model, NOW)
        self.assertEqual("review_ready", plan["status"])
        self.assertEqual(["screening", "attack", "replication", "adjudication"], model.calls)
        reviews = json.loads(plan["review_files"][ar.REVIEWS.as_posix()])
        row = reviews["reviewed_candidates"][-1]
        self.assertEqual(CID, row["candidate_id"])
        self.assertEqual("ADJACENT_NO_CONTRADICTION", row["disposition"])
        snapshots = json.loads(plan["review_files"][ar.SNAPSHOT_AUTHS.as_posix()])
        self.assertEqual(CID, snapshots["authorizations"][-1]["candidate_id"])
        self.assertFalse(any("promotion-proposals" in p for p in plan["inbox_files"]))

    def test_project_change_builds_exact_scientific_package(self):
        model = FakeModel("PROJECT_CHANGE_REQUIRED")
        plan = ar.build_plan(ROOT, self.source, model, NOW)
        self.assertEqual("review_ready", plan["status"])
        self.assertIn("scientific_change_generator", model.calls)
        reviews = json.loads(plan["review_files"][ar.REVIEWS.as_posix()])
        row = reviews["reviewed_candidates"][-1]
        self.assertEqual("PROJECT_CHANGE_REQUIRED", row["disposition"])
        self.assertTrue(row["proposal_id"].startswith("FAR-LIVING-PROP-AUTO-"))
        self.assertFalse(row["implementation_required"])
        self.assertIn(ar.PROMOTION_AUTHS.as_posix(), plan["review_files"])
        self.assertTrue(any("promotion-proposals" in p for p in plan["inbox_files"]))
        self.assertTrue(any("promotion-payloads" in p for p in plan["inbox_files"]))

    def test_project_change_can_prepare_separate_implementation_package(self):
        model = FakeModel("PROJECT_CHANGE_REQUIRED", implementation=True)
        plan = ar.build_plan(ROOT, self.source, model, NOW)
        reviews = json.loads(plan["review_files"][ar.REVIEWS.as_posix()])
        row = reviews["reviewed_candidates"][-1]
        self.assertTrue(row["implementation_required"])
        self.assertTrue(row["implementation_proposal_id"].startswith("FAR-LIVING-IMPL-AUTO-"))
        self.assertIn(ar.IMPLEMENTATION_AUTHS.as_posix(), plan["review_files"])
        self.assertTrue(any("implementation-proposals" in p for p in plan["inbox_files"]))
        self.assertTrue(any("implementation-payloads" in p for p in plan["inbox_files"]))

    def test_recent_source_block_skips_candidate(self):
        attempt = self.source / ar.ATTEMPTS / f"{CID}.json"
        attempt.parent.mkdir(parents=True, exist_ok=True)
        attempt.write_text(json.dumps({"next_retry_utc": "2026-09-23T20:00:00Z"}) + "\n")
        self.assertIsNone(ar.select_candidate(ROOT, self.source, NOW))

    def test_materializer_separates_review_and_inbox_surfaces(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("ADJACENT_NO_CONTRADICTION"), NOW)
        out = self.source / "out"
        ar.materialize(plan, out)
        self.assertTrue((out / "manifest.json").is_file())
        self.assertTrue((out / "review" / ar.REVIEWS).is_file())
        self.assertFalse((out / "inbox" / ar.REVIEWS).exists())


if __name__ == "__main__":
    unittest.main()
