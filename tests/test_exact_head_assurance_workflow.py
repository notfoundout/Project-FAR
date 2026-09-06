"""The exact-head lane must retain the whole canonical assurance program."""
from pathlib import Path
import os
import subprocess
import tempfile
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
        source_base = next(s for s in source if s.get('id') == 'base')
        target_base = next(s for s in target if s.get('id') == 'base')
        self.assertEqual(target_base.pop('env'), {
            'FAR_ASSURANCE_EVENT': '${{ github.event_name }}',
            'FAR_ASSURANCE_PR_BASE': '${{ github.event.pull_request.base.sha }}',
            'FAR_ASSURANCE_PUSH_BASE': '${{ github.event.before }}',
        })
        self.assertIn('base="$FAR_ASSURANCE_PUSH_BASE"', target_base['run'])
        self.assertIn('git merge-base --is-ancestor "$base" HEAD', target_base['run'])
        target_base['run'] = source_base['run']  # Stronger base resolution is tested below.
        self.assertEqual(source[1:], target[1:])
        self.assertEqual(source[0]['uses'], target[0]['uses'])
        self.assertEqual(target[0]['with']['ref'], '${{ github.event.pull_request.head.sha || github.sha }}')
        self.assertEqual(target[0]['with']['fetch-depth'], 0)
        self.assertIs(target[0]['with']['persist-credentials'], False)
        self.assertEqual(exact['permissions'], {'contents': 'read'})
        self.assertEqual(exact['jobs']['exact-head-assurance']['env']['FAR_VALIDATION_CACHE_SIGNING_KEY'], '${{ github.token }}')

    def test_push_base_covers_every_advanced_commit_and_rejects_missing_base(self):
        exact = yaml.safe_load((ROOT / '.github/workflows/exact-head-assurance.yml').read_text())
        script = next(s['run'] for s in exact['jobs']['exact-head-assurance']['steps'] if s.get('id') == 'base')
        with tempfile.TemporaryDirectory() as folder:
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=folder, stderr=subprocess.DEVNULL, text=True).strip()
            git('init', '-q')
            git('config', 'user.name', 'Assurance Test')
            git('config', 'user.email', 'assurance@example.invalid')
            git('commit', '--allow-empty', '-qm', 'previous main')
            before = git('rev-parse', 'HEAD')
            git('commit', '--allow-empty', '-qm', 'first change')
            git('commit', '--allow-empty', '-qm', 'second change')
            parent = git('rev-parse', 'HEAD^')
            output = Path(folder) / 'output'
            env = dict(os.environ, FAR_ASSURANCE_EVENT='push', FAR_ASSURANCE_PR_BASE=parent,
                       FAR_ASSURANCE_PUSH_BASE=before, GITHUB_OUTPUT=str(output))
            subprocess.run(['bash', '-c', script], cwd=folder, env=env, check=True, capture_output=True)
            self.assertEqual(output.read_text(), f'sha={before}\n')
            self.assertNotEqual(before, parent)
            for bad in ('', '0' * 40, 'not-a-sha'):
                output.unlink(missing_ok=True)
                env['FAR_ASSURANCE_PUSH_BASE'] = bad
                result = subprocess.run(['bash', '-c', script], cwd=folder, env=env, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
