from __future__ import annotations
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from parse_far import load_far_yaml

BASE='''investigation: x
representations:
{reps}
relations:
{rels}
rules:
  - id: r
    inputs: [{inputs}]
    output: {output}
transitions:
  - id: t1
    source: s0
    rule: r
    target: s1
    status: draft
    order: 1
'''
def rep(i): return f'  - id: {i}\n    kind: claim\n    content: {i}\n'
def rel(i,s,t): return f'  - id: {i}\n    type: supports\n    source: {s}\n    target: {t}\n'
class ReasoningEngineRegressionTests(unittest.TestCase):
    def load(self,text):
        with tempfile.NamedTemporaryFile('w',suffix='.far.yaml',delete=False) as f:
            f.write(text); name=f.name
        return load_far_yaml(Path(name))
    def test_modal_fixture_terminates(self):
        cp=subprocess.run([sys.executable,'tools/reasoning_engine.py','examples/far/reasoning-systems/modal-logic.far.yaml'],cwd=ROOT,text=True,capture_output=True,timeout=5)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('cycles: 0',cp.stdout)
    def test_simple_acyclic_chain(self):
        far=self.load(BASE.format(reps=rep('a')+rep('b')+rep('c'), rels=rel('r1','a','b')+rel('r2','b','c'), inputs='a, b', output='c'))
        self.assertEqual(far.detect_cycles(), [])
    def test_diamond_convergent_dependency_not_cycle(self):
        far=self.load(BASE.format(reps=rep('a')+rep('b')+rep('c')+rep('d'), rels=rel('r1','a','b')+rel('r2','a','c')+rel('r3','b','d')+rel('r4','c','d'), inputs='a, b', output='d'))
        self.assertEqual(far.detect_cycles(), [])
    def test_genuine_cycle_detected(self):
        far=self.load(BASE.format(reps=rep('a')+rep('b'), rels=rel('r1','a','b')+rel('r2','b','a'), inputs='a', output='b'))
        self.assertEqual(far.detect_cycles(), [['a','b','a']])
    def test_repeated_references_to_one_node_not_cycle(self):
        far=self.load(BASE.format(reps=rep('a')+rep('b')+rep('c'), rels=rel('r1','a','c')+rel('r2','b','c')+rel('r3','a','c'), inputs='a, b', output='c'))
        self.assertEqual(far.detect_cycles(), [])
    def test_malformed_reference_rejected(self):
        far=self.load(BASE.format(reps=rep('a'), rels=rel('r1','a','missing'), inputs='a', output='a'))
        self.assertTrue(any('unknown target' in e for e in far.validate_well_formed()))
    def test_deterministic_repeated_json_execution(self):
        cmd=[sys.executable,'tools/reasoning_engine.py','--json','examples/far/reasoning-systems/modal-logic.far.yaml']
        a=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=5).stdout
        b=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=5).stdout
        self.assertEqual(json.loads(a), json.loads(b))
