#!/usr/bin/env python3
"""Fail-closed validator and report generator for FARA-INV-W5-001."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ARTIFACT=ROOT/'theory/evaluation/fara-w5-cross-representation-invariance-v1.0.json'
REPORT=ROOT/'theory/evaluation/generated-fara-w5-invariance-summary.md'
DIMENSIONS=('structural','semantic','operational','dependency','information','historical')
STATUSES={'Pass','Partial','Fail','Unknown'}
FAMILIES={'lsts','trs','graphs','logic','traces','tables'}
TOPICS={'deterministic transitions','probabilistic information','nonmonotonic revision','paraconsistent consequence','causal intervention','changing rules or semantics','identity merge and deletion','provenance-sensitive history','distributed partial order','external oracle dependence','continuous case','embodied case'}
TERMINALS={'bounded invariance under a frozen representation class','explicit representation-sensitive counterexample','unresolved because equivalence, recovery, or coverage is insufficient'}
OWNER_FIELDS=('id','proof_object_id','claim_id','theorem_id')
CANONICAL_SHA256='ddfa8b7b4a4df733cb9c6dfcef1d464a68b7d35d8504d9e22692f0c57522eb48'

def load(): return json.loads(ARTIFACT.read_text())
def digest(data): return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def _owners(v,out):
 if isinstance(v,dict):
  for k,x in v.items():
   if k in OWNER_FIELDS and isinstance(x,str): out.add((k,x))
   _owners(x,out)
 elif isinstance(v,list):
  for x in v:_owners(x,out)
def duplicate_owner_paths(data):
 expected={(f,data[f]) for f in OWNER_FIELDS}; hits=[]
 for p in (ROOT/'theory/evaluation').glob('*.json'):
  if p==ARTIFACT:continue
  try:x=json.loads(p.read_text())
  except Exception:continue
  got=set();_owners(x,got)
  if expected&got:hits.append(str(p.relative_to(ROOT)))
 return hits

def validate(data, canonical=True):
 assert data['id']=='FARA-INV-W5-001' and data['proof_object_id']=='FARA-W5-PROOF-001'
 assert data['claim_id']=='CLM-INV-W5-001' and data['theorem_id']=='THM-INV-001'
 assert data['terminal_result'] in TERMINALS and data['terminal_result']=='explicit representation-sensitive counterexample'
 ar=data['authority_recovery']; assert ar['prompt_discrepancy'] and ar['canonical_objective']
 assert ar['dependencies']==['FARA-W1-PRIMITIVE-INDEPENDENCE-001','FARA-OPS-W2-001','FARA-REP-W4-001']
 assert ar['w0_w4_preservation']=={'W0':'unchanged; no claim consumed','W1':'unchanged; all seven primitive outcomes unresolved','W2':'unchanged; bounded coordinate result only','W3':'unchanged and not consumed','W4':'unchanged; finite archive boundary used only as declared dependency'}
 c=data['contract']; assert set(c['invariance_kinds'])=={'notation','serialization','implementation','representational','observational','behavioral','semantic','proof_result'}
 assert tuple(c['preservation_dimensions'])==DIMENSIONS and set(c['outputs'])==TERMINALS
 assert c['equivalence_criteria'].startswith('commitment equality') and 'never defined by conclusion agreement' in c['equivalence_criteria']
 assert 'decoder-held rule or conclusion' in c['forbidden_hidden_machinery']
 assert set(data['representation_families'])==FAMILIES
 for f,s in data['representation_families'].items(): assert s['independent_specification'] and s['not_superficial_reason']
 assert len(data['cases'])==12 and {x['topic'] for x in data['cases']}==TOPICS
 for x in data['cases']:
  assert len(x['representations'])==2 and set(x['representations'])<=FAMILIES
  assert set(x['encodings'])==set(x['representations']) and set(x['decoder_or_recovery'])==set(x['representations'])
  assert set(x['preservation'])==set(DIMENSIONS) and set(x['preservation'].values())<=STATUSES
  assert x['losses_ambiguities_failures'] or x['classification']=='positive'
  assert x['hidden_assumptions'] or x['classification']=='positive'
  if x['recovery']=='exact': assert all(v=='Pass' for v in x['preservation'].values()) and x['conclusion_agreement'] is True
  if x['classification']=='unresolved': assert x['conclusion_agreement'] is None and x['recovery']=='unknown'
  if x['classification']=='negative': assert x['conclusion_agreement'] is False and any(v=='Fail' for v in x['preservation'].values())
 assert {x['kind'] for x in data['counterexamples']}=={'equivalent-source/different-conclusion','inequivalent-source/collapse','representation-dependent-minimality','decoder-smuggling','circularity'}
 assert data['claim_levels']['universal_invariance']=='not established'
 assert data['claim_levels']['all_registered_representations'].startswith('refuted')
 assert 'bounded invariance implies universal invariance' in data['nonclaims']
 assert data['remaining_obligations']==['independent specification and replication of each family','formal semantic equivalence for nonclassical consequence','nonfinite recovery theory for continuous systems','environment-inclusive embodied equivalence','oracle transcript/live-service boundary adjudication']
 assert len(data['self_review'])==8
 if canonical: assert digest(data)==CANONICAL_SHA256, 'canonical claim map, equivalence, fixture, or obligation drift'

def report(d):
 lines=['# Generated FARA W5 cross-representation invariance summary','', 'Generated deterministically by `python tools/check_fara_w5_invariance.py --write`.','', '## Authority recovery','',d['authority_recovery']['canonical_objective'],'',f"**Prompt discrepancy:** {d['authority_recovery']['prompt_discrepancy']}",'','## Representation families','']
 lines += [f"- **{k} — {v['name']}:** {v['independent_specification']}" for k,v in d['representation_families'].items()]
 lines += ['','## Preservation and conclusion-agreement matrix','','| Fixture | Pair | S/Sem/O/D/I/H | Recovery | Agreement | Result |','|---|---|---|---|---|---|']
 for x in d['cases']:
  vec='/'.join(x['preservation'][q] for q in DIMENSIONS); ag='Unknown' if x['conclusion_agreement'] is None else str(x['conclusion_agreement'])
  lines.append(f"| {x['id']} {x['topic']} | {' ↔ '.join(x['representations'])} | {vec} | {x['recovery']} | {ag} | {x['classification']} |")
 lines += ['','## Counterexamples','']+[f"- **{x['id']} ({x['kind']}):** {x['witness']}" for x in d['counterexamples']]
 for title,key in [('Strongest established result','strongest_result'),('Refuted claims','refuted_claims'),('Unresolved claims','unresolved_claims'),('Explicit nonclaims','nonclaims'),('Remaining obligations','remaining_obligations'),('Self-review','self_review')]:
  lines += ['',f'## {title}','']
  v=d[key];lines += [v] if isinstance(v,str) else [f'- {z}' for z in v]
 return '\n'.join(lines)+'\n'
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();d=load();validate(d)
 expected=report(d)
 if a.write:REPORT.write_text(expected)
 else:assert REPORT.read_text()==expected,'generated report stale'
 assert not duplicate_owner_paths(d),f'duplicate identifier owners: {duplicate_owner_paths(d)}'
 print('FARA W5 invariance: PASS (6 families; 12 fixtures; 5 counterexamples)')
if __name__=='__main__':main()
