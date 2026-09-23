from __future__ import annotations

import unittest

from tests.test_living_autonomous_review import (
    FakeModel,
    NOW,
    ROOT,
    URL,
    decision_record,
    meta,
    source_fixture,
)
from tools import run_living_autonomous_review as ar


class AttackRetrievalFailureModel(FakeModel):
    def generate(self, *, role, prompt, schema, urls=None):
        result, metadata = super().generate(role=role, prompt=prompt, schema=schema, urls=urls)
        if role == "attack":
            metadata = meta(False, URL)
        return result, metadata


class SplitSourceModel(FakeModel):
    ATTACK_URL = "https://example.org/attack-source"
    REPLICATION_URL = "https://example.org/replication-source"

    def generate(self, *, role, prompt, schema, urls=None):
        result, metadata = super().generate(role=role, prompt=prompt, schema=schema, urls=urls)
        if role == "attack":
            result = dict(result)
            result["source_urls_used"] = [self.ATTACK_URL]
            metadata = meta(True, self.ATTACK_URL)
        elif role == "replication":
            result = dict(result)
            result["source_urls_used"] = [self.REPLICATION_URL]
            metadata = meta(True, self.REPLICATION_URL)
        return result, metadata


class ForeignCandidateSourceModel(FakeModel):
    FOREIGN_URL = "https://example.org/unrelated-but-retrieved"

    def generate(self, *, role, prompt, schema, urls=None):
        result, metadata = super().generate(role=role, prompt=prompt, schema=schema, urls=urls)
        if role in {"screening", "attack", "replication"}:
            result = dict(result)
            result["source_urls_used"] = [self.FOREIGN_URL]
            metadata = meta(True, self.FOREIGN_URL)
        return result, metadata


class IrrelevantMatchedScreeningModel(FakeModel):
    def generate(self, *, role, prompt, schema, urls=None):
        result, metadata = super().generate(role=role, prompt=prompt, schema=schema, urls=urls)
        if role == "screening":
            result = dict(result)
            rows = [dict(row) for row in result["claim_assessments"]]
            rows[0]["relevant"] = False
            rows[0]["premise_match"] = True
            rows[0]["scope_match"] = True
            result["claim_assessments"] = rows
            result["relevant"] = False
            result["affected_claim_ids"] = []
            result["premise_match"] = True
            result["scope_match"] = True
        return result, metadata


class NegativeEvidenceBindingTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path

        self.tmp = tempfile.TemporaryDirectory()
        self.source = Path(self.tmp.name)
        source_fixture(self.source)

    def tearDown(self):
        self.tmp.cleanup()

    def test_attack_retrieval_failure_cannot_become_negative_disposition(self):
        plan = ar.build_plan(
            ROOT,
            self.source,
            AttackRetrievalFailureModel("ADJACENT_NO_CONTRADICTION"),
            NOW,
        )
        self.assertEqual("source_blocked", plan["status"])
        self.assertFalse(plan["review_files"])
        self.assertEqual(1, len(plan["inbox_files"]))

    def test_negative_roles_must_share_one_retrieved_primary_source(self):
        plan = ar.build_plan(
            ROOT,
            self.source,
            SplitSourceModel("ADJACENT_NO_CONTRADICTION"),
            NOW,
        )
        self.assertEqual("source_blocked", plan["status"])
        self.assertFalse(plan["review_files"])

    def test_all_roles_citing_same_retrieved_non_candidate_source_is_rejected(self):
        plan = ar.build_plan(
            ROOT,
            self.source,
            ForeignCandidateSourceModel("ADJACENT_NO_CONTRADICTION"),
            NOW,
        )
        self.assertEqual("source_blocked", plan["status"])
        self.assertFalse(plan["review_files"])
        attempt = next(iter(plan["inbox_files"].values())).decode("utf-8")
        self.assertIn("outside the frozen candidate source set", attempt)

    def test_irrelevant_screen_cannot_claim_exact_premise_or_scope_match(self):
        plan = ar.build_plan(
            ROOT,
            self.source,
            IrrelevantMatchedScreeningModel("IRRELEVANT_FALSE_POSITIVE"),
            NOW,
        )
        self.assertEqual("review_retry_blocked", plan["status"])
        self.assertFalse(plan["review_files"])
        attempt = next(iter(plan["inbox_files"].values())).decode("utf-8")
        self.assertIn("premise/scope match requires per-claim relevance", attempt)


class ExactClaimWitnessTests(unittest.TestCase):
    CLAIMS = {"FAR-CORE-001", "FAR-CORE-002"}

    @staticmethod
    def screening():
        return {
            "primary_source_verified": True,
            "relevant": True,
            "source_urls_used": [URL],
            "evaluated_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "claim_assessments": [
                {
                    "claim_id": "FAR-CORE-001",
                    "relevant": True,
                    "premise_match": True,
                    "scope_match": False,
                    "reason": "premise only",
                },
                {
                    "claim_id": "FAR-CORE-002",
                    "relevant": True,
                    "premise_match": False,
                    "scope_match": True,
                    "reason": "scope only",
                },
            ],
            "affected_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "premise_match": True,
            "scope_match": True,
            "summary": "split screening witness",
            "evidence_locations": ["source"],
            "limits": [],
        }

    @staticmethod
    def split_contradiction_attack():
        return {
            "contradiction_found": True,
            "prior_art_found": False,
            "prior_art_strength": "NONE",
            "source_urls_used": [URL],
            "evaluated_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "claim_assessments": [
                {
                    "claim_id": "FAR-CORE-001",
                    "contradiction_found": True,
                    "prior_art_found": False,
                    "prior_art_strength": "NONE",
                    "reason": "attack on first claim",
                },
                {
                    "claim_id": "FAR-CORE-002",
                    "contradiction_found": False,
                    "prior_art_found": False,
                    "prior_art_strength": "NONE",
                    "reason": "no attack on second claim",
                },
            ],
            "affected_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "exact_reason": "aggregate contradiction",
            "reproducible_attack": "bounded counterexample",
            "source_locations": ["source"],
            "limits": [],
        }

    @staticmethod
    def split_contradiction_replication():
        return {
            "contradiction_found": True,
            "prior_art_found": False,
            "prior_art_strength": "NONE",
            "source_urls_used": [URL],
            "evaluated_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "claim_assessments": [
                {
                    "claim_id": "FAR-CORE-001",
                    "contradiction_found": False,
                    "prior_art_found": False,
                    "prior_art_strength": "NONE",
                    "attack_reproduced": False,
                    "reason": "did not reproduce first claim",
                },
                {
                    "claim_id": "FAR-CORE-002",
                    "contradiction_found": True,
                    "prior_art_found": False,
                    "prior_art_strength": "NONE",
                    "attack_reproduced": True,
                    "reason": "different claim contradicted",
                },
            ],
            "affected_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "independent_reason": "aggregate reproduction",
            "attack_reproduced": True,
            "source_locations": ["source"],
            "limits": [],
        }

    @staticmethod
    def split_prior_attack():
        return {
            "contradiction_found": False,
            "prior_art_found": True,
            "prior_art_strength": "DIRECT",
            "source_urls_used": [URL],
            "evaluated_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "claim_assessments": [
                {
                    "claim_id": "FAR-CORE-001",
                    "contradiction_found": False,
                    "prior_art_found": True,
                    "prior_art_strength": "DIRECT",
                    "reason": "direct prior art for first claim",
                },
                {
                    "claim_id": "FAR-CORE-002",
                    "contradiction_found": False,
                    "prior_art_found": False,
                    "prior_art_strength": "NONE",
                    "reason": "no prior art for second claim",
                },
            ],
            "affected_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "exact_reason": "aggregate direct prior art",
            "reproducible_attack": "",
            "source_locations": ["source"],
            "limits": [],
        }

    @staticmethod
    def split_prior_replication():
        return {
            "contradiction_found": False,
            "prior_art_found": True,
            "prior_art_strength": "DIRECT",
            "source_urls_used": [URL],
            "evaluated_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "claim_assessments": [
                {
                    "claim_id": "FAR-CORE-001",
                    "contradiction_found": False,
                    "prior_art_found": False,
                    "prior_art_strength": "NONE",
                    "attack_reproduced": False,
                    "reason": "no prior art for first claim",
                },
                {
                    "claim_id": "FAR-CORE-002",
                    "contradiction_found": False,
                    "prior_art_found": True,
                    "prior_art_strength": "DIRECT",
                    "attack_reproduced": False,
                    "reason": "direct prior art for second claim",
                },
            ],
            "affected_claim_ids": ["FAR-CORE-001", "FAR-CORE-002"],
            "independent_reason": "aggregate direct prior art",
            "attack_reproduced": False,
            "source_locations": ["source"],
            "limits": [],
        }

    def test_project_change_cannot_compose_witness_across_claims(self):
        policy = ar.load_json(ROOT / ar.POLICY)
        with self.assertRaisesRegex(ar.CandidateReviewError, "single exact claim|complete exact per-claim"):
            ar.validate_decision(
                decision_record("PROJECT_CHANGE_REQUIRED"),
                policy,
                ROOT,
                self.CLAIMS,
                self.screening(),
                self.split_contradiction_attack(),
                self.split_contradiction_replication(),
                meta(),
                meta(),
                meta(),
            )

    def test_prior_art_lead_cannot_compose_witness_across_claims(self):
        policy = ar.load_json(ROOT / ar.POLICY)
        with self.assertRaisesRegex(ar.CandidateReviewError, "single exact claim|complete exact per-claim"):
            ar.validate_decision(
                decision_record("N1_PRIOR_ART_LEAD"),
                policy,
                ROOT,
                self.CLAIMS,
                self.screening(),
                self.split_prior_attack(),
                self.split_prior_replication(),
                meta(),
                meta(),
                meta(),
            )


if __name__ == "__main__":
    unittest.main()
