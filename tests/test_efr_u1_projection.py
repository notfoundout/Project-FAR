"""Synthetic checks of the frozen U1 projection template; no field-study data."""
from pathlib import Path
import unittest

from mechanization.far_mechanization.contract_v2 import canonical_json, contract_sha256, validate_contract

ROOT = Path(__file__).resolve().parents[1]


class EfrU1ProjectionTests(unittest.TestCase):
    def document(self, collision):
        text = (ROOT / 'docs/research/external-falsification-and-replication/02-u1-projection.md').read_text()
        code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
        rows = [{'id': 'x1', 'value': 'first', 'required_behavior': False, 'representation': 'a'},
                {'id': 'x2', 'value': 'second', 'required_behavior': True,
                 'representation': 'a' if collision else 'b'}]
        scope = {'rows': rows, 'investigation_id': 'S01001'}
        exec(compile(code, 'frozen-u1-projection', 'exec'), scope)
        contract = scope['contract']
        decoder = {}
        for row in rows:
            decoder.setdefault(canonical_json(row['representation']), {
                'representation_value': row['representation'], 'behavior_value': row['required_behavior']})
        stamp = '2026-09-06T00:00:00Z'
        return {'format_version': 'far-ir/2.0', 'id': contract['id'], 'contract': contract,
                'report': {'outcome': 'PROVED', 'evidence': {'kind': 'factorization',
                           'status': 'CHECKED_FINITE_EXPLICIT',
                           'decoder_table': [decoder[k] for k in sorted(decoder)]}, 'failure_report': []},
                'provenance': {'producer': 'EFR-U1', 'created_at': stamp,
                               'sources': [{'path': 'synthetic.json', 'sha256': '0' * 64}]},
                'freeze': {'status': 'FROZEN', 'frozen_at': stamp,
                           'contract_sha256': contract_sha256(contract)}}

    def test_native_rows_project_to_checked_preservation(self):
        result = validate_contract(self.document(False))
        self.assertTrue(result.success, result.diagnostics)

    def test_same_construction_exposes_loss_without_changing_the_candidate(self):
        document = self.document(True)
        result = validate_contract(document)
        self.assertFalse(result.success)
        self.assertNotIn('SCHEMA_CONSTRAINT_VIOLATION', {d.code for d in result.diagnostics})
        self.assertEqual(document['report']['outcome'], 'PROVED')
        self.assertTrue(any('FACTORIZATION' in d.code for d in result.diagnostics))


if __name__ == '__main__':
    unittest.main()
