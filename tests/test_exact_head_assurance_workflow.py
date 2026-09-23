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

        # Exact-head may add only the dispatch trust preflight/lineage guards around the
        # canonical program. Strip those two stronger guards, normalize the intentionally
        # stronger checkout/base/artifact identities, and then require byte-structural
        # equality with the canonical merge-authority steps.
        dispatch_only_names = {
            'Validate dispatched identity before checkout',
            'Verify dispatched checkout lineage before repository code runs',
        }
        target_core = [step for step in target if step.get('name') not in dispatch_only_names]
        self.assertEqual(len(target_core), len(source))

        self.assertEqual(
            target_core[-1]['with']['name'],
            'exact-head-assurance-${{ inputs.head_sha || github.event.pull_request.head.sha || github.sha }}',
        )
        target_core[-1]['with']['name'] = source[-1]['with']['name']

        source_base = next(s for s in source if s.get('id') == 'base')
        target_base = next(s for s in target_core if s.get('id') == 'base')
        self.assertEqual(target_base.pop('env'), {
            'FAR_ASSURANCE_EVENT': '${{ github.event_name }}',
            'FAR_ASSURANCE_PR_BASE': '${{ github.event.pull_request.base.sha }}',
            'FAR_ASSURANCE_PUSH_BASE': '${{ github.event.before }}',
            'FAR_ASSURANCE_DISPATCH_BASE': '${{ inputs.base_sha }}',
        })
        self.assertIn('base="$FAR_ASSURANCE_PUSH_BASE"', target_base['run'])
        self.assertIn('workflow_dispatch) base="$FAR_ASSURANCE_DISPATCH_BASE"', target_base['run'])
        self.assertIn('git merge-base --is-ancestor "$base" HEAD', target_base['run'])
        target_base['run'] = source_base['run']  # Stronger base resolution is tested below.

        target_checkout = target_core[0]
        source_checkout = source[0]
        self.assertEqual(source_checkout['uses'], target_checkout['uses'])
        self.assertEqual(
            target_checkout['with']['ref'],
            "${{ github.event_name == 'workflow_dispatch' && inputs.head_sha || github.event.pull_request.head.sha || github.sha }}",
        )
        self.assertEqual(target_checkout['with']['fetch-depth'], 0)
        self.assertIs(target_checkout['with']['persist-credentials'], False)
        normalized_checkout = dict(target_checkout)
        normalized_checkout['with'] = dict(target_checkout['with'])
        normalized_checkout['with'].pop('ref')
        normalized_checkout['with'].pop('persist-credentials')
        self.assertEqual(source_checkout, normalized_checkout)

        self.assertEqual(source[1:], target_core[1:])
        self.assertEqual(exact['permissions'], {'contents': 'read'})
        self.assertEqual(
            exact['jobs']['exact-head-assurance']['env']['FAR_VALIDATION_CACHE_SIGNING_KEY'],
            '${{ github.token }}',
        )

    def test_dispatch_guards_run_before_repository_controlled_code(self):
        exact = yaml.safe_load((ROOT / '.github/workflows/exact-head-assurance.yml').read_text())
        steps = exact['jobs']['exact-head-assurance']['steps']
        names = [step.get('name') or step.get('uses') for step in steps]
        preflight = names.index('Validate dispatched identity before checkout')
        checkout = next(i for i, step in enumerate(steps) if step.get('uses') == 'actions/checkout@v4')
        lineage = names.index('Verify dispatched checkout lineage before repository code runs')
        setup = next(i for i, step in enumerate(steps) if step.get('uses') == 'actions/setup-python@v5')
        install = names.index('Install dependencies and trace backend')
        self.assertLess(preflight, checkout)
        self.assertLess(checkout, lineage)
        self.assertLess(lineage, setup)
        self.assertLess(lineage, install)
        self.assertIn(
            '[[ "$FAR_ASSURANCE_DISPATCH_BASE" == "$FAR_ASSURANCE_DISPATCH_WORKFLOW_SHA" ]]',
            steps[preflight]['run'],
        )
        self.assertIn(
            '[[ "$(git rev-parse HEAD^1)" == "$FAR_ASSURANCE_DISPATCH_BASE" ]]',
            steps[lineage]['run'],
        )

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
            env = dict(
                os.environ,
                FAR_ASSURANCE_EVENT='push',
                FAR_ASSURANCE_PR_BASE=parent,
                FAR_ASSURANCE_PUSH_BASE=before,
                FAR_ASSURANCE_DISPATCH_BASE='',
                GITHUB_OUTPUT=str(output),
            )
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
