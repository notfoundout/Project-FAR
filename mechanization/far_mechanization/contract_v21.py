"""Decidable finite-explicit far-ir/2.1 approximation and cost semantics.

All arithmetic is exact. Random decoders, reference mass, metric/loss tables,
aggregation, tolerance, product cost preorder, Pareto minima, least elements,
and zero-loss exact-recovery boundaries are recomputed rather than trusted.
"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping, Sequence
from jsonschema import Draft202012Validator

REPO_ROOT=Path(__file__).resolve().parents[2]
SCHEMA_PATH=REPO_ROOT/'schemas/far-contract-v2.1.schema.json'
FORMAT_VERSION='far-ir/2.1'
@dataclass(frozen=True,slots=True)
class Diagnostic: code:str; message:str; path:tuple[object,...]=()
@dataclass(frozen=True,slots=True)
class Result:
 diagnostics:tuple[Diagnostic,...]
 @property
 def success(self): return not self.diagnostics

def canonical_json(v:object)->str:return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def contract_sha256(c:Mapping[str,Any])->str:return hashlib.sha256(canonical_json(c).encode()).hexdigest()
def key(v:object)->str:return canonical_json(v)
def frac(v:object)->Fraction:return Fraction(str(v))
def add(e:list[Diagnostic],code:str,msg:str):e.append(Diagnostic(code,msg))
def indexed(rows,label,e):
 out={}
 for row in rows:
  cid=str(row['case_id'])
  if cid in out:add(e,'DUPLICATE_CASE_VALUE',f'{label}: {cid}')
  out[cid]=row['value']
 return out

def validate_contract(doc:object)->Result:
 schema=json.loads(SCHEMA_PATH.read_text()); Draft202012Validator.check_schema(schema)
 es=[Diagnostic('SCHEMA_CONSTRAINT_VIOLATION',x.message,tuple(x.path)) for x in Draft202012Validator(schema).iter_errors(doc)]
 if es or not isinstance(doc,Mapping):return Result(tuple(es))
 c=doc['contract']; ev=doc['report']['evidence']; ap=c.get('approximation')
 if c['mode']!='approximate' or ev['kind']!='approximation_cost':add(es,'W5_MODE_EVIDENCE_REQUIRED','far-ir/2.1 checked records require approximate mode and approximation_cost evidence')
 if doc['report']['outcome']!='PROVED':add(es,'CHECKED_EVIDENCE_OUTCOME_MISMATCH','checked approximation evidence requires PROVED')
 if c['source_domain']['kind']!='finite_explicit' or c['source_domain']['status']!='EXPLICIT':add(es,'CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN','finite explicit domain required')
 ids=[str(x['id']) for x in c['source_domain']['cases']]
 if len(ids)!=len(set(ids)):add(es,'DUPLICATE_DOMAIN_CASE','case ids')
 beh=indexed(c['required_behavior']['table'],'behavior',es); rep=indexed(c['representation']['table'],'representation',es)
 if set(beh)!=set(ids) or set(rep)!=set(ids):add(es,'CASE_TABLE_COVERAGE_MISMATCH','behavior and representation must cover domain exactly')
 if not ap:return Result(tuple(es))
 # reference probability
 weights={}
 for x in ap['reference']['weights']:
  cid=str(x['case_id']); weights[cid]=weights.get(cid,Fraction())+frac(x['weight'])
 if set(weights)!=set(ids):add(es,'REFERENCE_COVERAGE_MISMATCH','reference must cover every case exactly')
 if any(v<0 for v in weights.values()) or sum(weights.values())!=1:add(es,'REFERENCE_NOT_PROBABILITY','reference weights must be nonnegative and sum to one')
 # metric totality and axioms over declared values
 vals={key(v):v for v in ap['metric']['values']}; metric={}
 for x in ap['metric']['entries']:
  pair=(key(x['left']),key(x['right']))
  if pair in metric:add(es,'DUPLICATE_METRIC_ENTRY',str(pair))
  metric[pair]=frac(x['distance'])
 expected={(a,b) for a in vals for b in vals}
 if set(metric)!=expected:add(es,'METRIC_NOT_TOTAL','metric table must cover declared values exactly')
 else:
  for a in vals:
   if metric[a,a]!=0:add(es,'METRIC_IDENTITY_FAILURE',a)
   for b in vals:
    if metric[a,b]!=metric[b,a]:add(es,'METRIC_SYMMETRY_FAILURE',f'{a},{b}')
    if a!=b and metric[a,b]==0:add(es,'METRIC_SEPARATION_FAILURE',f'{a},{b}')
    for z in vals:
     if metric[a,z]>metric[a,b]+metric[b,z]:add(es,'METRIC_TRIANGLE_FAILURE',f'{a},{b},{z}')
 # loss totality
 actions={key(v):v for v in ap['loss']['actions']}; truths={key(v) for v in beh.values()}; loss={}
 for x in ap['loss']['entries']:
  pair=(key(x['truth']),key(x['action']))
  if pair in loss:add(es,'DUPLICATE_LOSS_ENTRY',str(pair))
  loss[pair]=frac(x['loss'])
 if set(loss)!={(t,a) for t in truths for a in actions}:add(es,'LOSS_NOT_TOTAL','loss must cover behavior range x action set exactly')
 # metric connects all truth/action values and loss must equal metric (declared operational semantics)
 for t in truths:
  for a in actions:
   if (t,a) not in metric:add(es,'METRIC_LOSS_DOMAIN_MISMATCH',f'{t},{a}')
   elif (t,a) in loss and metric[t,a]!=loss[t,a]:add(es,'LOSS_METRIC_MISMATCH',f'{t},{a}')
 dims=[x['id'] for x in ap['cost_preorder']['dimensions']]
 if len(dims)!=len(set(dims)):add(es,'DUPLICATE_COST_DIMENSION','dimension ids')
 candidates={}; agg={}; exact=set()
 for cand in ev['candidates']:
  cid=cand['id']
  if cid in candidates:add(es,'DUPLICATE_CANDIDATE',cid);continue
  costs={x['dimension_id']:frac(x['value']) for x in cand['costs']}
  if set(costs)!=set(dims) or len(cand['costs'])!=len(dims):add(es,'COST_COVERAGE_MISMATCH',cid)
  decoder={}
  for row in cand['decoder_table']:
   rk=key(row['representation_value']); dist={}
   for item in row['distribution']:
    ak=key(item['action']); dist[ak]=dist.get(ak,Fraction())+frac(item['probability'])
   if rk in decoder:add(es,'DUPLICATE_DECODER_ENTRY',cid)
   if set(dist)-set(actions):add(es,'DECODER_UNKNOWN_ACTION',cid)
   if any(x<0 for x in dist.values()) or sum(dist.values())!=1:add(es,'DECODER_NOT_PROBABILITY',cid)
   decoder[rk]=dist
  used={key(rep[x]) for x in ids}
  if set(decoder)!=used:add(es,'DECODER_COVERAGE_MISMATCH',cid)
  per=[]; is_exact=True
  for x in ids:
   dist=decoder.get(key(rep[x]),{}); t=key(beh[x]); value=sum((p*loss.get((t,a),Fraction()) for a,p in dist.items()),Fraction())
   per.append((weights.get(x,Fraction()),value))
   if value!=0:is_exact=False
  value=max((v for _,v in per),default=Fraction()) if ap['aggregation']=='maximum' else sum((w*v for w,v in per),Fraction())
  agg[cid]=value
  if is_exact:exact.add(cid)
  candidates[cid]=costs
 feasible={x for x,v in agg.items() if v<=frac(ap['tolerance'])}
 def leq(a,b):return all(candidates[a].get(d,Fraction(-1))<=candidates[b].get(d,Fraction(-1)) for d in dims)
 pareto={a for a in feasible if not any(b!=a and leq(b,a) and not leq(a,b) for b in feasible)}
 least={a for a in feasible if all(leq(a,b) for b in feasible)}
 claims=[('claimed_feasible',feasible,'FEASIBLE_SET_MISMATCH'),('claimed_pareto_minimal',pareto,'PARETO_SET_MISMATCH'),('claimed_least_elements',least,'LEAST_SET_MISMATCH'),('exact_recovery_claims',exact,'EXACT_RECOVERY_SET_MISMATCH')]
 for field,actual,code in claims:
  if set(ev[field])!=actual:add(es,code,f'claimed={sorted(ev[field])} computed={sorted(actual)}')
 # zero loss iff action equals truth follows from metric separation; ensure randomized exact distributions concentrate there
 if frac(ap['tolerance'])==0 and feasible!=exact:add(es,'ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE','zero tolerance feasible set must equal exact recovery set')
 if doc['freeze']['status']=='FROZEN' and doc['freeze']['contract_sha256']!=contract_sha256(c):add(es,'FREEZE_HASH_MISMATCH','contract hash')
 return Result(tuple(es))

def load_and_validate(path):
 try:return validate_contract(json.loads(Path(path).read_text()))
 except (OSError,json.JSONDecodeError) as x:return Result((Diagnostic('UNREADABLE_CONTRACT',str(x)),))
def main(argv:Sequence[str]|None=None):
 import argparse
 p=argparse.ArgumentParser();p.add_argument('path');a=p.parse_args(argv);r=load_and_validate(a.path)
 print('PASS' if r.success else 'FAIL');[print(f'{d.code}: {d.message}') for d in r.diagnostics];return 0 if r.success else 1
if __name__=='__main__':raise SystemExit(main())
