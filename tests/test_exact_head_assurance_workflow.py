"""The exact-head lane must retain the whole canonical assurance program."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class ExactHeadAssuranceWorkflowTests(unittest.TestCase):
    def test_exact_head_lane_cannot_omit_or_change_canonical_assurance_steps(self):
        canonical = yaml.safe_load((ROOT / '.github/workflows/validator-assurance.yml').read_text())
        exact = yaml.safe_load((ROOT / '.github/workflows/exact-head-assurance.yml').read_text())
        source = canonical['jobs']['merge-authority']['steps']
        target = exact['jobs']['exact-head-assurance']['steps']
        self.assertEqual(target[-1]["with"]["name"], "exact-head-assurance-${{ github.event.pull_request.head.sha || github.sha }}")
        target[-1]["with"]["name"] = source[-1]["with"]["name"]
        self.assertEqual(source[1:], target[1:])
        self.assertEqual(source[0]['uses'], target[0]['uses'])
        self.assertEqual(target[0]['with']['ref'], '${{ github.event.pull_request.head.sha || github.sha }}')
        self.assertEqual(target[0]['with']['fetch-depth'], 0)
        self.assertIs(target[0]['with']['persist-credentials'], False)
        self.assertEqual(exact['permissions'], {'contents': 'read'})
        self.assertEqual(exact['jobs']['exact-head-assurance']['env']['FAR_VALIDATION_CACHE_SIGNING_KEY'], '${{ github.token }}')


if __name__ == '__main__':
    unittest.main()
