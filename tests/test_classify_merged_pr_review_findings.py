import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "classify_merged_pr_review_findings.py"
spec = importlib.util.spec_from_file_location("classifier", MODULE_PATH)
assert spec and spec.loader
classifier = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = classifier
spec.loader.exec_module(classifier)


class ClassifierTests(unittest.TestCase):
    def thread(self, *, resolved=False, outdated=False, body="Fix this"):
        return {
            "id": "THREAD_1",
            "pr_number": 12,
            "path": "example.md",
            "line": 4,
            "is_resolved": resolved,
            "is_outdated": outdated,
            "comments": [{"id": "COMMENT_1", "body": body, "url": "https://example.test"}],
        }

    def test_open_thread_is_unresolved(self):
        findings = classifier.classify([self.thread()], {})
        self.assertEqual(findings[0].disposition, "unresolved")

    def test_resolved_thread_is_not_assumed_correct(self):
        findings = classifier.classify([self.thread(resolved=True)], {})
        self.assertEqual(findings[0].disposition, "uncertain_manual_review_required")

    def test_outdated_resolved_thread_is_not_assumed_obsolete(self):
        findings = classifier.classify([self.thread(resolved=True, outdated=True)], {})
        self.assertEqual(findings[0].disposition, "uncertain_manual_review_required")

    def test_empty_comment_is_non_actionable(self):
        findings = classifier.classify([self.thread(body="")], {})
        self.assertEqual(findings[0].disposition, "non_actionable")

    def test_definitive_override_requires_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "overrides.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "decisions": [{
                    "finding_id": "PR12:THREAD_1",
                    "disposition": "resolved_correctly",
                    "evidence": [],
                    "rationale": "",
                }],
            }), encoding="utf-8")
            with self.assertRaises(SystemExit):
                classifier.load_overrides(path)

    def test_supported_override_is_applied(self):
        override = {
            "PR12:THREAD_1": {
                "finding_id": "PR12:THREAD_1",
                "disposition": "resolved_correctly",
                "confidence": "manual_high",
                "evidence": ["Verified current file and regression test."],
                "rationale": "The reported defect no longer reproduces.",
            }
        }
        findings = classifier.classify([self.thread(resolved=True)], override)
        self.assertEqual(findings[0].disposition, "resolved_correctly")
        self.assertEqual(findings[0].confidence, "manual_high")

    def test_duplicate_threads_fail_closed(self):
        with self.assertRaises(SystemExit):
            classifier.classify([self.thread(), self.thread()], {})

    def test_markdown_claim_is_rendered_as_inert_text(self):
        body = "**<sub>![P1 Badge](https://img.example/badge.svg)</sub> Fix [link](https://example.test) and `code`**"
        findings = classifier.classify([self.thread(body=body)], {})
        report = classifier.render_markdown(findings, Path("threads.json"))
        self.assertIn("P1 Badge Fix link and 'code'", report)
        self.assertNotIn("](https://", report)
        self.assertNotIn("<sub>", report)

    def test_legacy_project_status_token_is_neutralized_in_markdown(self):
        findings = classifier.classify([self.thread(body="Replace PROJECT_STATUS.md now")], {})
        report = classifier.render_markdown(findings, Path("threads.json"))
        self.assertIn("PROJECT_STATUS[.]md", report)
        self.assertNotIn("PROJECT_STATUS.md", report)


if __name__ == "__main__":
    unittest.main()
