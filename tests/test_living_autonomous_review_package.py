from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tools import check_living_autonomous_review_package as checker
from tools import promote_living_research as promoter
from tools import run_living_autonomous_review as ar
from tests.test_living_autonomous_review import CID, FakeModel, source_fixture

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 9, 22, 20, 0, tzinfo=timezone.utc)


class AutonomousReviewPackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.source = self.workspace / "source"
        self.source.mkdir()
        source_fixture(self.source)

    def tearDown(self):
        self.tmp.cleanup()

    def package(self, disposition: str, **kwargs):
        plan = ar.build_plan(ROOT, self.source, FakeModel(disposition, **kwargs), NOW)
        out = self.workspace / ("package-" + disposition.lower())
        ar.materialize(plan, out)
        return out

    def artifact(self, package: Path) -> Path:
        roots = list((package / "review" / ar.REVIEW_ROOT).iterdir())
        self.assertEqual(1, len(roots))
        return roots[0]

    def test_valid_adjacent_package_passes(self):
        package = self.package("ADJACENT_NO_CONTRADICTION")
        self.assertEqual([], checker.validate(ROOT, package))

    def test_valid_prior_art_package_passes(self):
        package = self.package("N1_PRIOR_ART_LEAD")
        self.assertEqual([], checker.validate(ROOT, package))

    def test_valid_project_change_package_passes(self):
        package = self.package("PROJECT_CHANGE_REQUIRED")
        self.assertEqual([], checker.validate(ROOT, package))

    def test_valid_project_change_with_implementation_passes(self):
        package = self.package("PROJECT_CHANGE_REQUIRED", implementation=True)
        self.assertEqual([], checker.validate(ROOT, package))

    def test_project_change_requires_direct_relevance(self):
        package = self.package("PROJECT_CHANGE_REQUIRED")
        path = self.artifact(package) / "observation.json"
        value = json.loads(path.read_text())
        value["screening"]["relevant"] = False
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
        errors = checker.validate(ROOT, package)
        self.assertTrue(any("direct relevance" in error for error in errors), errors)

    def test_prior_art_requires_replication(self):
        package = self.package("N1_PRIOR_ART_LEAD")
        path = self.artifact(package) / "replication.json"
        value = json.loads(path.read_text())
        value["prior_art_found"] = False
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
        errors = checker.validate(ROOT, package)
        self.assertTrue(any("not reproduced" in error for error in errors), errors)

    def test_irrelevant_requires_screening_irrelevance(self):
        package = self.package("IRRELEVANT_FALSE_POSITIVE")
        errors = checker.validate(ROOT, package)
        self.assertTrue(any("requires screening.relevant=false" in error for error in errors), errors)

    def test_source_blocked_has_no_authority_bytes(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("ADJACENT_NO_CONTRADICTION", verified=False), NOW)
        package = self.workspace / "blocked"
        ar.materialize(plan, package)
        self.assertEqual([], checker.validate(ROOT, package))
        self.assertFalse((package / "review").exists())

    def test_noop_scientific_operation_is_rejected(self):
        target = "docs/project-status.md"
        raw = (ROOT / target).read_bytes()
        inbox = self.workspace / "inbox"
        source_path = "research/living/inbox/promotion-payloads/FAR-LIVING-PROP-TEST/noop.md"
        payload = inbox / source_path
        payload.parent.mkdir(parents=True)
        payload.write_bytes(raw)
        operation = {
            "op": "write_file",
            "path": target,
            "source_path": source_path,
            "expected_main_sha256": promoter.h(raw),
            "result_sha256": promoter.h(raw),
        }
        with self.assertRaisesRegex(checker.PackageError, "no-op replacement"):
            checker.check_operation(ROOT, inbox, operation, implementation_surface=False)


if __name__ == "__main__":
    unittest.main()
