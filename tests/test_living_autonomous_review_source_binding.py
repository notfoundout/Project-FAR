from __future__ import annotations

import unittest

from tests.test_living_autonomous_review import FakeModel, NOW, ROOT, URL, meta, source_fixture
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


if __name__ == "__main__":
    unittest.main()
