"""Tests for the merged-PR review inventory validator."""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import tempfile
import unittest

from tools.check_merged_pr_review_inventory import REL, validate


class InventoryValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.directory = self.root / REL
        self.directory.mkdir(parents=True)
        frozen = self.root / "frozen.txt"
        frozen.write_text("immutable")
        self.sha = "a" * 40
        self.prs = {"audited_main_sha": self.sha, "records": [{"pr_number": 1, "retrieval_status": {"all": "complete"}}]}
        self.comments = {"audited_main_sha": self.sha, "records": [{"source_id": 10, "record_type": "inline_review_comment", "pr_number": 1}]}
        self.threads = {"audited_main_sha": self.sha, "records": [{"thread_id": "T1", "pr_number": 1}]}
        self.manifest = {
            "audited_main_sha": self.sha,
            "counts": {"merged_prs_reported_by_github": 1, "merged_prs_retrieved_from_github": 1, "merged_prs_inferred_from_git_history": 1, "review_submissions_retrieved": 0, "inline_comments_retrieved": 1, "issue_comments_inspected": 0, "threads_retrieved": 1},
            "pagination": {"complete": True, "page_count": 1, "pages_or_cursors": [1], "skipped_pages": []},
            "counts_per_pr": [{"pr_number": 1, "reviews": {"status": "complete", "count": 0}}],
            "retrieval_errors": [], "inaccessible_records": [], "api_or_permission_limitations": [],
            "completeness_status": "COMPLETE",
            "frozen_evidence_baseline": [{"path": "frozen.txt", "sha256": hashlib.sha256(b"immutable").hexdigest()}],
        }
        self.write()

    def tearDown(self): self.temp.cleanup()

    def write(self):
        for name, data in (("raw-pr-inventory.json", self.prs), ("raw-review-comments.json", self.comments), ("raw-review-threads.json", self.threads), ("retrieval-manifest.json", self.manifest)):
            (self.directory / name).write_text(json.dumps(data))

    def assert_invalid(self, text):
        self.write(); self.assertTrue(any(text in item for item in validate(self.root)), validate(self.root))

    def test_positive(self): self.assertEqual([], validate(self.root, self.sha))
    def test_missing_pr(self): self.manifest["counts"]["merged_prs_retrieved_from_github"] = 0; self.assert_invalid("missing PR")
    def test_missing_comment(self): self.comments["records"] = []; self.assert_invalid("comment count")
    def test_duplicate_conflicting_comment_id(self):
        duplicate = copy.deepcopy(self.comments["records"][0]); duplicate["pr_number"] = 2; self.comments["records"].append(duplicate); self.assert_invalid("duplicate conflicting")
    def test_missing_thread_id(self): del self.threads["records"][0]["thread_id"]; self.assert_invalid("lacks thread_id")
    def test_count_mismatch(self): self.manifest["counts"]["threads_retrieved"] = 2; self.assert_invalid("thread count")
    def test_skipped_page(self): self.manifest["pagination"]["skipped_pages"] = [2]; self.assert_invalid("skipped")
    def test_unreported_api_failure(self): self.manifest["counts_per_pr"][0]["reviews"]["status"] = "failed"; self.assert_invalid("not reported")
    def test_false_complete(self): self.manifest["inaccessible_records"] = [{"id": 2}]; self.assert_invalid("does not satisfy")
    def test_mismatched_main_sha(self): self.assertTrue(any("expected" in e for e in validate(self.root, "b" * 40)))
    def test_omitted_limitation(self): self.manifest["retrieval_errors"] = [{"status": 500}]; self.assert_invalid("limitation is omitted")
    def test_frozen_evidence_mutation(self): (self.root / "frozen.txt").write_text("changed"); self.assertTrue(any("mutation" in e for e in validate(self.root)))


if __name__ == "__main__": unittest.main()
