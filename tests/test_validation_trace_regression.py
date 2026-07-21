from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from far_validation.tracing import _matches, _normalize_observed


class TraceContractRegressionTests(unittest.TestCase):
    def test_repository_root_metadata_is_not_a_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertIsNone(_normalize_observed(str(root), root, root))

    def test_double_star_glob_matches_zero_nested_directories(self) -> None:
        self.assertTrue(_matches("tools/check_one.py", ("tools/**/*.py",)))
        self.assertTrue(_matches("mechanization/model.py", ("mechanization/**/*.py",)))


if __name__ == "__main__":
    unittest.main()
