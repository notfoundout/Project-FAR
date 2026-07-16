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
        self.assertIn('CRE-001 demonstrates only that compiler-authored declared interpretations successfully compiled, lowered, and verified under the registered deterministic reference', generated)
        self.assertNotIn('Established at CRE-001 ' + 'vocabulary-semantics scope', generated)
        self.assertNotRegex(generated, 'CRE-001.*formal vocabulary ' + 'licensing.*' + 'estab' + 'lished')

    def test_frozen_semantic_specification_is_consistent(self):
        cp=subprocess.run([sys.executable,'tools/check_cre001_semantics.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertIn('CRE-001 SEMANTIC CHECK PASSED', cp.stdout)

    def test_generated_task_ids_and_provenance_are_unambiguous(self):
        cp=subprocess.run([sys.executable,'tools/generate_next_tasks.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        text=(ROOT/'docs/planning/next-actions.md').read_text(encoding='utf-8')
        ranked=text.split('## Maintainer Task Briefs',1)[0]
        ids=re.findall(r'^### ([A-Z]+-\d{3}):', ranked, re.M)
        self.assertEqual(len(ids),len(set(ids)))
        self.assertIn('### STRATEGIC-001: Design and preregister CRE-002', ranked)
        self.assertIn('- Source: strategic roadmap priority', ranked)
        strategic=ranked.split('### TASK-054:',1)[0]
        self.assertNotIn('Source gap:', strategic)

if __name__=='__main__': unittest.main()
