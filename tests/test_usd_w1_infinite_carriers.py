from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class USDW1InfiniteCarriersTests(unittest.TestCase):
    def load(self, path: str):
        return json.loads((ROOT / path).read_text(encoding='utf-8'))

    def test_validator_passes(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / 'tools/check_usd_w1_infinite_carriers.py')],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn('PASS', completed.stdout)

    def test_scope_is_candidate_independent_and_bounded(self):
        scope = self.load('theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json')
        self.assertTrue(scope['candidate_independent'])
        self.assertIn('uncountable_carriers', scope['excluded_cases'])
        self.assertIn('non_effectively_presented_countable_carriers', scope['excluded_cases'])

    def test_negative_controls_are_rejected(self):
        result = self.load('theory/evaluation/usd-w1-infinite-carriers-extension-result-v1.0.json')
        self.assertEqual(result['fixture_results']['INF-NEG-TRUNC-001'], 'rejected')
        self.assertEqual(result['fixture_results']['INF-NEG-ORACLE-001'], 'rejected')
        self.assertEqual(result['fixture_results']['INF-BOUNDARY-NONCOMP-001'], 'excluded_preserved')

    def test_claim_boundaries_remain_closed(self):
        result = self.load('theory/evaluation/usd-w1-infinite-carriers-extension-result-v1.0.json')
        self.assertEqual(result['terminal_outcome'], 'proper_subclass_only')
        self.assertEqual(result['claim_effect']['S_IRD_representation'], 'unresolved')
        self.assertEqual(result['claim_effect']['universal_structure'], 'unresolved')
        self.assertEqual(result['machine_check_status'], 'not_mechanized')
        self.assertEqual(result['independent_review_status'], 'not_started')


if __name__ == '__main__':
    unittest.main()
