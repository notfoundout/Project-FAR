from collections import Counter
import hashlib
import json
import unittest

from tools.efr_hd1_allocation import allocate, DOMAINS, CLASSES
from tools.efr_hd1_analysis import analyze, endpoints, prepare


class EfrHd1AnalysisTests(unittest.TestCase):
    def fixture(self, bias=False):
        data = {'reviewers': [f'R{i:02}' for i in range(24)], 'cases': [
            {'id': f'C{d:02}{k}{i:02}', 'domain': domain, 'class': label}
            for d, domain in enumerate(DOMAINS) for k, label in enumerate(CLASSES) for i in range(10)]}
        raw = json.dumps(data).encode()
        digest = hashlib.sha256(raw).hexdigest()
        labels = {c['id']: c['class'] for c in data['cases']}
        ratings = []
        for row in allocate(raw, digest)['allocation']:
            for arm, tasks in row['tasks'].items():
                for case in tasks:
                    answer = labels[case]
                    if bias and row['reviewer_id'] == 'R00' and arm == 'far':
                        answer = 'preservation' if answer == 'material_loss' else 'material_loss'
                    ratings.append(dict(reviewer_id=row['reviewer_id'], case_id=case, arm=arm, decision=answer))
        output = json.dumps({'input_manifest_sha256': digest, 'ratings': ratings}).encode()
        return raw, digest, output, hashlib.sha256(output).hexdigest()

    def test_sealed_data_and_allocation_binding_fail_closed(self):
        raw, digest, output, seal = self.fixture()
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            prepare(raw, digest, output + b' ', seal)
        data = json.loads(output)
        data['ratings'][0]['reviewer_id'] = 'OTHER'
        changed = json.dumps(data).encode()
        with self.assertRaisesRegex(ValueError, 'unallocated'):
            prepare(raw, digest, changed, hashlib.sha256(changed).hexdigest())

    def test_shared_reviewer_weight_changes_all_their_case_contributions(self):
        data, groups, _ = prepare(*self.fixture(bias=True))
        cases = {c['id']: 1 for c in data['cases']}
        weights = Counter({r: 1 for r in data['reviewers']})
        ordinary = endpoints(groups, cases, weights)
        weights['R00'] = 0
        self.assertEqual(endpoints(groups, cases, weights), (0, 0))
        weights['R00'] = 24
        amplified = endpoints(groups, cases, weights)
        self.assertLess(amplified[0], ordinary[0])
        self.assertGreater(amplified[1], ordinary[1])

    def test_full_registered_resampling_does_not_invent_a_benefit(self):
        result = analyze(*self.fixture())
        self.assertEqual(result['resamples'], 10000)
        self.assertEqual(result['observed'], ['0', '0'])
        self.assertEqual(result['percentile_bounds'], ['0', '0', '0', '0'])
        self.assertEqual(result['numerical_disposition'], 'NUMERICAL_GATES_FAIL')

    def test_missingness_and_unestimable_resample_cannot_pass(self):
        raw, digest, output, _ = self.fixture()
        data = json.loads(output)
        for row in data['ratings'][:80]:
            row['decision'] = None
        output = json.dumps(data).encode()
        result = analyze(raw, digest, output, hashlib.sha256(output).hexdigest())
        self.assertEqual(result['numerical_disposition'], 'INVALID_MISSINGNESS')
        manifest, groups, _ = prepare(*self.fixture())
        with self.assertRaisesRegex(ValueError, 'no redraw'):
            endpoints(groups, {c['id']: 1 for c in manifest['cases']}, Counter({'R00': 24}))


if __name__ == '__main__':
    unittest.main()
