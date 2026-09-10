"""Tests for the merged-PR review inventory validator."""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import tempfile
import unittest

from tools.check_merged_pr_review_inventory import REL, ROOT as REPO_ROOT, validate


class InventoryValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.directory = self.root / REL
        self.directory.mkdir(parents=True)
        self.sha = "a" * 40
        self.prs = {
            "schema_version": 2,
            "pull_requests": [{"number": 1, "merged_at": "2026-01-01T00:00:00Z", "merge_commit_sha": "b" * 40}],
        }
        self.comments = {
            "schema_version": 2,
            "comments": [
                {"id": 10, "kind": "inline_review_comment", "pr_number": 1, "in_reply_to_id": None},
                {"id": 11, "kind": "issue_comment", "pr_number": 1},
            ],
        }
        self.reviews = {"schema_version": 2, "reviews": [{"id": 20, "pr_number": 1}]}
        self.threads = {"schema_version": 2, "threads": [{"id": "T1", "pr_number": 1}]}
        self.manifest = {
            "schema_version": 2,
            "repository": "notfoundout/Project-FAR",
            "audited_sha": self.sha,
            "completeness_status": "COMPLETE",
            "counts": {
                "merged_pull_requests": 1,
                "issue_comments": 1,
                "inline_review_comments": 1,
                "review_submissions": 1,
                "review_threads": 1,
            },
            "retrievals": [
                {"endpoint": "GET /repos/{owner}/{repo}/pulls?state=closed", "pr_number": None, "pages": 1, "items": 1, "complete": True, "errors": []},
                {"endpoint": "GET /repos/{owner}/{repo}/issues/{pr}/comments", "pr_number": 1, "pages": 1, "items": 1, "complete": True, "errors": []},
                {"endpoint": "GET /repos/{owner}/{repo}/pulls/{pr}/reviews", "pr_number": 1, "pages": 1, "items": 1, "complete": True, "errors": []},
                {"endpoint": "GET /repos/{owner}/{repo}/pulls/{pr}/comments", "pr_number": 1, "pages": 1, "items": 1, "complete": True, "errors": []},
                {"endpoint": "GraphQL pullRequest.reviewThreads", "pr_number": 1, "pages": 1, "items": 1, "complete": True, "errors": []},
            ],
            "integrity": {
                "mapping_errors": [],
                "invalid_reply_parent_ids": [],
                "uniqueness_checks": {
                    name: {"ok": True, "duplicates_or_nulls": []}
                    for name in ("pull_requests", "review_comments", "issue_comments", "reviews", "threads")
                },
            },
        }
        (self.directory / "inventory-summary.md").write_text("summary\n", encoding="utf-8")
        (self.directory / "retrieval-limitations.md").write_text("none\n", encoding="utf-8")
        self.write()
        self.freeze_evidence_hashes()

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def git_blob_sha1(path: pathlib.Path) -> str:
        raw = path.read_bytes()
        return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()

    def write(self):
        for name, data in (
            ("raw-pr-inventory.json", self.prs),
            ("raw-review-comments.json", self.comments),
            ("raw-review-submissions.json", self.reviews),
            ("raw-review-threads.json", self.threads),
            ("retrieval-manifest.json", self.manifest),
        ):
            (self.directory / name).write_text(json.dumps(data), encoding="utf-8")

    def freeze_evidence_hashes(self):
        names = (
            "inventory-summary.md",
            "raw-pr-inventory.json",
            "raw-review-comments.json",
            "raw-review-submissions.json",
            "raw-review-threads.json",
            "retrieval-limitations.md",
        )
        payload = {
            "schema_version": 1,
            "hash_kind": "git_blob_sha1",
            "git_blob_sha1": {name: self.git_blob_sha1(self.directory / name) for name in names},
        }
        (self.directory / "evidence-hashes.json").write_text(json.dumps(payload), encoding="utf-8")

    def assert_invalid(self, text):
        self.write()
        failures = validate(self.root)
        self.assertTrue(any(text in item for item in failures), failures)

    def test_positive(self):
        self.assertEqual([], validate(self.root, self.sha))

    def test_checked_in_inventory_is_validated(self):
        self.assertEqual([], validate(REPO_ROOT))

    def test_schema_mismatch(self):
        self.prs["schema_version"] = 1
        self.assert_invalid("schema_version")

    def test_missing_pr(self):
        self.prs["pull_requests"] = []
        self.assert_invalid("count mismatch")

    def test_missing_comment(self):
        self.comments["comments"] = self.comments["comments"][1:]
        self.assert_invalid("count mismatch")

    def test_duplicate_identical_comment_id(self):
        self.comments["comments"].append(copy.deepcopy(self.comments["comments"][0]))
        self.assert_invalid("duplicate comment id")

    def test_duplicate_conflicting_comment_id(self):
        duplicate = copy.deepcopy(self.comments["comments"][0])
        duplicate["kind"] = "issue_comment"
        self.comments["comments"].append(duplicate)
        self.assert_invalid("duplicate comment id")

    def test_missing_thread_id(self):
        del self.threads["threads"][0]["id"]
        self.assert_invalid("lacks id")

    def test_per_pr_endpoint_omission(self):
        self.manifest["retrievals"] = [
            item for item in self.manifest["retrievals"]
            if item.get("endpoint") != "GraphQL pullRequest.reviewThreads"
        ]
        self.assert_invalid("exactly one retrieval")

    def test_per_pr_endpoint_duplicate(self):
        self.manifest["retrievals"].append(copy.deepcopy(self.manifest["retrievals"][1]))
        self.assert_invalid("exactly one retrieval")

    def test_per_pr_count_mismatch(self):
        self.manifest["retrievals"][2]["items"] = 0
        self.assert_invalid("retrieval count mismatch")

    def test_count_mismatch(self):
        self.manifest["counts"]["review_threads"] = 2
        self.assert_invalid("manifest count mismatch")

    def test_skipped_page(self):
        self.manifest["retrievals"][1]["complete"] = False
        self.manifest["retrievals"][1]["errors"] = ["skipped page 2"]
        self.assert_invalid("retrieval incomplete")

    def test_unreported_api_failure(self):
        self.manifest["retrievals"][1]["complete"] = False
        self.manifest["retrievals"][1]["errors"] = ["HTTP 500"]
        self.assert_invalid("retrieval incomplete")

    def test_omitted_limitation(self):
        self.manifest["retrievals"][1]["errors"] = ["HTTP 500"]
        self.assert_invalid("retrieval incomplete")

    def test_false_complete(self):
        self.manifest["integrity"]["mapping_errors"] = ["bad mapping"]
        self.assert_invalid("mapping errors")

    def test_mismatched_main_sha(self):
        self.assertTrue(any("expected" in item for item in validate(self.root, "b" * 40)))

    def test_reply_parent_must_exist(self):
        self.comments["comments"][0]["in_reply_to_id"] = 999
        self.assert_invalid("reply parent missing")

    def test_frozen_evidence_mutation(self):
        path = self.directory / "raw-pr-inventory.json"
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        failures = validate(self.root)
        self.assertTrue(any("frozen evidence mutation detected" in item for item in failures), failures)


if __name__ == "__main__":
    unittest.main()
