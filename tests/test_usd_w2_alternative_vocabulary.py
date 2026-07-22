from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / 'theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json'
CHECKER = ROOT / 'tools/check_usd_w2_alternative_vocabulary.py'

class AlternativeVocabularyCompetitionTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        run = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn('PASS', run.stdout)

    def test_required_competition_is_present(self) -> None:
        data = json.loads(RESULT.read_text(encoding='utf-8'))
        ids = {c['id'] for c in data['candidates']}
        self.assertEqual(ids, {'FARA-001','GREL-001','LTS-PROV-001','ARG-HIST-001'})
        self.assertGreaterEqual(sum(c['independently_motivated'] for c in data['candidates']), 2)

    def test_tradeoffs_do_not_create_winner(self) -> None:
        data = json.loads(RESULT.read_text(encoding='utf-8'))
        self.assertIsNone(data['winner'])
        self.assertEqual(data['terminal_result'], 'multiple_incomparable_successful_vocabularies')
        self.assertTrue(any(p['classification'] == 'incomparable_tradeoff' for p in data['pairwise_results']))

    def test_broader_hypotheses_remain_unresolved(self) -> None:
        effect = json.loads(RESULT.read_text(encoding='utf-8'))['hypothesis_effect']
        for key in ('USD-H-EXIST','USD-H-INV','USD-H-NEC','USD-H-MIN','USD-H-NO'):
            self.assertEqual(effect[key], 'unresolved')

if __name__ == '__main__':
    unittest.main()
