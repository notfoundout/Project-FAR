from __future__ import annotations

import json
import unittest
from pathlib import Path

from mechanization.far_mechanization.compare_adjudication import canonical_json_bytes, compare_packages


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "compare-adjudicate-v1"


class GoldenComparisonTests(unittest.TestCase):
    def test_example_packages_reproduce_exact_golden_comparison_bytes(self) -> None:
        left = json.loads((FIXTURES / "left-package.json").read_text(encoding="utf-8"))
        right = json.loads((FIXTURES / "right-package.json").read_text(encoding="utf-8"))
        expected = (FIXTURES / "golden-comparison.json").read_bytes()
        self.assertEqual(canonical_json_bytes(compare_packages(left, right)), expected)


if __name__ == "__main__":
    unittest.main()
