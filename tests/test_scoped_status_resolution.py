from __future__ import annotations
import subprocess, sys, unittest
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]

def text(path: str) -> str:
    return (ROOT/path).read_text(encoding="utf-8")

class ScopedStatusResolutionTests(unittest.TestCase):
    def test_t001_and_t002_metadata_are_conditional_with_deletion_scope(self):
        data=yaml.safe_load(text('theory/metadata/theorems.yaml'))['theorems']
        by_id={t['id']: t for t in data}
        self.assertEqual(by_id['T-001']['status'], 'Established (Conditional)')
        self.assertIn('deletion-only reduction standard', by_id['T-001']['scope'])
        self.assertEqual(by_id['T-002']['status'], 'Established (Conditional)')
        self.assertIn('current Project FAR definitions and deletion-only reduction standard', by_id['T-002']['scope'])
        self.assertEqual(by_id['T-001']['assurance_level'], 'semantically_constrained_proof_object')
        self.assertEqual(by_id['T-002']['assurance_level'], 'semantically_constrained_proof_object')

    def test_theorem_catalog_is_conditional_not_global(self):
        t=text('theory/theorems/theorems.md')
        self.assertIn('T-001 — Conditional Primitive Minimality', t)
        self.assertIn('Status: Established (Conditional).', t)
        self.assertIn('does not establish global minimality', t)
        self.assertIn('does not establish absolute independence', t)

    def test_vi002_and_vi003_remain_research(self):
        vi2=text('research/validation/investigations/VI-002-primitive-minimality.md')
        vi3=text('research/validation/investigations/VI-003-primitive-independence.md')
        self.assertRegex(vi2, r'## Status\n\nResearch')
        self.assertIn('Full investigation: active', vi2)
        self.assertNotIn('**PASS (Provisional)**', vi2)
        self.assertRegex(vi3, r'## Status\n\nResearch')
        self.assertIn('VI-003 remains incomplete', vi3)

    def test_open_questions_have_conditional_and_global_entries(self):
        oq=text('research/open-problems/open-questions.md')
        for title,status in [
            ('Conditional Primitive Minimality','Resolved (Conditional)'),
            ('Global Primitive Minimality','Active'),
            ('Conditional Primitive Independence','Resolved (Conditional)'),
            ('Global Primitive Independence','Active')]:
            self.assertIn(f'## {title}', oq)
            self.assertIn(f'**Status:** {status}', oq)

    def test_canonical_summaries_do_not_claim_global_resolution(self):
        combined=text('README.md')+'\n'+text('docs/project-status.md')
        self.assertIn('global primitive minimality', combined.lower())
        self.assertIn('global primitive independence', combined.lower())
        self.assertNotIn('global primitive minimality is established', combined.lower())
        self.assertNotIn('global primitive independence is established', combined.lower())
        self.assertIn('CRE-001 remains unexecuted', combined)
        self.assertIn('universality', combined.lower())

    def test_status_consistency_checker_has_no_scoped_primitive_contradiction(self):
        cp=subprocess.run([sys.executable,'tools/check_status_consistency.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertIn('Contradictions: 0', cp.stdout)

    def test_generated_theorem_metadata_current(self):
        cp=subprocess.run([sys.executable,'tools/generate_theorem_index.py','--check'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)

if __name__ == '__main__':
    unittest.main()
