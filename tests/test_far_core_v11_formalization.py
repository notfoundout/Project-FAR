from __future__ import annotations

import unittest

from tools import check_far_core_v11_formalization as checker


class FARCoreV11FormalizationTests(unittest.TestCase):
    def test_machine_ledger_and_lean_sources_align(self):
        generated, _report, errors = checker.expected()
        self.assertEqual(errors, [])
        self.assertEqual(generated["w2_summary"]["formalized"], 13)
        self.assertEqual(generated["w2_summary"]["partial_obstruction"], 1)
        self.assertEqual(generated["w2_summary"]["contradiction_reopen_required"], 0)

    def test_no_w2_axiom_or_placeholder(self):
        generated, _report, _errors = checker.expected()
        self.assertEqual(generated["w2_summary"]["forbidden_placeholders"], 0)

    def test_generated_views_are_current(self):
        self.assertEqual(checker.main([]), 0)


if __name__ == "__main__":
    unittest.main()
