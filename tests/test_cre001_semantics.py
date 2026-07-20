from __future__ import annotations
import re, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CRE001SemanticRegressionTests(unittest.TestCase):
    def test_semantics_are_prospective_not_retrospective(self):
        formal=(ROOT/'theory/evaluation/comparative-representation/experiments/CRE-001/semantics/formal-semantics.md').read_text(encoding='utf-8')
        generated=(ROOT/'docs/reports/project-status-generated.md').read_text(encoding='utf-8')
        self.assertIn('formalized after completion of deterministic CRE-001', formal)
        self.assertIn('frozen for future experiments beginning with CRE-002', formal)
        self.assertIn('not independent evidence supporting CRE-001', formal)
        self.assertIn('cannot be used as retrospective validation of CRE-001', formal)
        self.assertIn('CRE-001: deterministic comparison complete at its registered retrospective scope under compiler-authored declared interpretations', generated)
        self.assertNotIn('Established at CRE-001 ' + 'vocabulary-semantics scope', generated)
        self.assertNotRegex(generated, 'CRE-001.*formal vocabulary ' + 'licensing.*' + 'estab' + 'lished')

    def test_frozen_semantic_specification_is_consistent(self):
        cp=subprocess.run([sys.executable,'tools/check_cre001_semantics.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertIn('CRE-001 SEMANTIC CHECK PASSED', cp.stdout)

    def test_generated_task_ids_and_provenance_are_unambiguous(self):
        path=ROOT/'docs/planning/next-actions.md'
        before=path.read_text(encoding='utf-8')
        cp=subprocess.run([sys.executable,'tools/generate_next_tasks.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        text=path.read_text(encoding='utf-8')
        self.assertEqual(text,before,'next-actions.md must match the canonical generator output')
        ranked=text.split('## Maintainer Task Briefs',1)[0]
        ids=re.findall(r'^### ([A-Z]+-\d{3}):', ranked, re.M)
        self.assertEqual(len(ids),len(set(ids)))
        self.assertIn('### STRATEGIC-001: Resolve the formal role of P8', ranked)
        self.assertIn('### STRATEGIC-002: Build the S_core construction and obstruction ledger', ranked)
        self.assertIn('### STRATEGIC-003: Prove formal negative-control lemmas', ranked)
        self.assertIn('- Source: deduction-first strategic priority', ranked)
        self.assertNotIn('Formalize faithful representation and nontriviality', ranked)
        self.assertNotIn('Freeze THM-TARGET-001 and premise ledger', ranked)
        self.assertNotIn('Plan independent replication of CRE-002-EXT-001', ranked)
        self.assertNotIn('Source gap:', ranked)

if __name__=='__main__': unittest.main()
