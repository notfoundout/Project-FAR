from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.check_fare_theorem_ids import DEFAULT_PROOFS_ROOT, validate


def theorem(identifier: str) -> str:
    return f"# Mathematical Theorem\n\n## Identifier\n\n{identifier}\n"


class FareTheoremIdHygieneTests(unittest.TestCase):
    def test_current_active_corpus_has_unique_ids(self) -> None:
        self.assertEqual(validate(DEFAULT_PROOFS_ROOT), [])

    def test_duplicate_active_identifier_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "foundations").mkdir(parents=True)
            (root / "geometry").mkdir(parents=True)
            (root / "foundations" / "MT-001.md").write_text(
                theorem("MT-001"), encoding="utf-8"
            )
            (root / "geometry" / "other.md").write_text(
                theorem("MT-001"), encoding="utf-8"
            )
            issues = validate(root)
            self.assertEqual(len(issues), 1)
            self.assertIn("duplicate active FARE theorem id MT-001", issues[0])
            self.assertIn("foundations/MT-001.md", issues[0])
            self.assertIn("geometry/other.md", issues[0])

    def test_archived_identifier_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "foundations").mkdir(parents=True)
            (root / "archive" / "legacy").mkdir(parents=True)
            (root / "foundations" / "MT-001.md").write_text(
                theorem("MT-001"), encoding="utf-8"
            )
            (root / "archive" / "legacy" / "old.md").write_text(
                theorem("MT-001"), encoding="utf-8"
            )
            self.assertEqual(validate(root), [])


if __name__ == "__main__":
    unittest.main()
