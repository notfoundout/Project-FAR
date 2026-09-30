#!/usr/bin/env python3
"""Dependency-aware, fail-closed reconciliation for the FAR Research corpus."""
from __future__ import annotations
import argparse, glob, hashlib, json, re, sys
from pathlib import Path
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
CORPUS=Path('research/corpus/corpus-v1.0.json'); OUTPUT=Path('research/corpus/synthesis-v1.0.json'); STATUS=Path('docs/research/current-research-frontier.md')
LIVING_RECONCILIATION=Path('research/living/corpus-reconciliation-v1.0.json')
LEVELS={'EVIDENCE','INFERENCE','HYPOTHESIS','UNRESOLVED'}; RELATIONS={'SUPPORTS','CONTRADICTS','QUALIFIES','CORRECTS','SUPERSEDES','UNRESOLVED'}
ARCH={'already_representable_enforceable','representable_assurance_incomplete','existing_extension_point','genuine_architecture_gap','contradiction','unresolved'}
def canonical(v): return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def digest(b): return hashlib.sha256(b).hexdigest()
def load(p,root=ROOT): return json.loads((root/p).read_text())
def file_record(path,root=ROOT):
 p=root/path; return {'path':path.as_posix(),'sha256':digest(p.read_bytes()),'size':p.stat().st_size}

def inventory(data,root=ROOT):
 rules=data['inventory_rules']; records={}
 for category in ('required_declared_globs','automatic_lead_globs','snapshot_globs'):
  for pattern in rules[category]:
   for raw in glob.glob(str(root/pattern),recursive=True):
    p=Path(raw)
    if p.is_file() and not p.is_symlink():
     rel=p.relative_to(root); rec=file_record(rel,root); rec['category']=category; records[rel.as_posix()]=rec
 return [records[k] for k in sorted(records)]

def saturation_observations(root=ROOT):
 p=root/'research/corpus/snapshots/pr-571/research/saturation-falsification-001/findings-v1.0.json'
 if not p.exists(): return []
 x=json.loads(p.read_text()); out=[]
 for f in x['findings']:
  out.append({'claim_key':f['id'],'epistemic_class':'EVIDENCE','statement':f['evidence'],'scope':x['campaign_conclusion']['scope'],'relation':'SUPPORTS','uncertainty':f.get('minimal_repair',''),'mechanism_ids':['MEC-SATURATION-ATTACKS'],'dependencies':[],'supersedes':[],'corrects':[],'external_source_ids':f['source_ids'],'architecture_disposition':f['disposition'],'literal_mapping':f['baseline_mapping']})
 return out

def living_leads(root=ROOT):
 rows_by_id={}
 snapshot=root/'research/corpus/snapshots/pr-490-manifest-v1.0.json'
 if snapshot.exists():
  manifest=json.loads(snapshot.read_text())
  for item in manifest.get('candidate_blobs',[]):
   cid=Path(item['path']).stem
   rows_by_id[cid]={'id':cid,'path':item['path'],'sha256':item['sha256'],'git_blob':item['git_blob'],'source_key':None,'review_status':'DISCOVERED_PR490','evidence_usable':False,'snapshot_head':manifest['head_sha']}
 rows=[]
 for p in sorted((root/'research/living/inbox/candidates').glob('FAR-LIT-*.json')):
  x=json.loads(p.read_text()); cid=x.get('id',p.stem); row=rows_by_id.get(cid,{'id':cid}); row.update({'current_main_path':str(p.relative_to(root)),'current_main_sha256':digest(p.read_bytes()),'source_key':x.get('source_key'),'review_status':'DISCOVERED','evidence_usable':False}); rows_by_id[cid]=row
 for p in sorted((root/'research/corpus/external').glob('*.json')):
  x=json.loads(p.read_text()); rows_by_id[p.stem]={'id':p.stem,'path':str(p.relative_to(root)),'sha256':digest(p.read_bytes()),'source_key':x.get('origin'),'review_status':x.get('review_status','DISCOVERY_LEAD'),'evidence_usable':bool(x.get('primary_evidence_verified',False) and x.get('review_status')=='REVIEWED_SOURCE')}
 return [rows_by_id[k] for k in sorted(rows_by_id)]

def validate(data,root=ROOT):
 errors=[]; schema=json.loads((ROOT/'schemas/far-research-corpus-v1.schema.json').read_text())
 errors += ['schema: '+e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(data)]
 ids={}; collections=(('source',data.get('sources',[])),('mechanism',data.get('mechanism_catalog',[])),('conclusion',data.get('conclusion_rules',[])),('frontier',data.get('frontier_rules',[])))
 for kind,rows in collections:
  for row in rows:
   rid=row.get('id');
   if not isinstance(rid,str) or not re.fullmatch(r'[A-Z][A-Z0-9-]+',rid or ''): errors.append(f'invalid {kind} identity {rid!r}')
   elif rid in ids: errors.append(f'duplicate identity {rid}')
   else: ids[rid]=kind
 sources={s.get('id'):s for s in data.get('sources',[])}; mechs={m.get('id'):m for m in data.get('mechanism_catalog',[])}; conclusions={c.get('id'):c for c in data.get('conclusion_rules',[])}
 source_ids=set(sources); claim_ids={o.get('claim_key') for s in sources.values() for o in s.get('observations',[])}
 declared={s.get('path') for s in sources.values() if s.get('path')}
 # Exact external-ref manifests bind every copied PR #571 byte and the complete #490 lead index.
 pr571=root/'research/corpus/snapshots/pr-571-manifest-v1.0.json'
 if pr571.exists():
  manifest=json.loads(pr571.read_text())
  for item in manifest.get('files',[]):
   path=root/'research/corpus/snapshots/pr-571'/item['path']
   if not path.is_file() or digest(path.read_bytes())!=item['sha256']: errors.append('PR #571 snapshot drift: '+item['path'])
 pr490=root/'research/corpus/snapshots/pr-490-manifest-v1.0.json'
 if pr490.exists():
  manifest=json.loads(pr490.read_text()); blobs=manifest.get('candidate_blobs',[])
  if manifest.get('candidate_count')!=len(blobs) or len({b.get('path') for b in blobs})!=len(blobs): errors.append('PR #490 candidate inventory incomplete or duplicate')
  for item in blobs:
   if not re.fullmatch(r'[0-9a-f]{40}',item.get('git_blob','')) or not re.fullmatch(r'[0-9a-f]{64}',item.get('sha256','')): errors.append('PR #490 invalid content identity: '+str(item.get('path')))
 inv=inventory(data,root)
 for rec in inv:
  if rec['category']=='required_declared_globs' and rec['path'] not in declared: errors.append('unclassified material input: '+rec['path'])
 for s in sources.values():
  if not all(k in s for k in ('evidence_class','scope','history','supersedes','corrects','observations')): errors.append(f'incomplete provenance semantics: {s.get("id")}')
  if any(x not in source_ids for x in s.get('supersedes',[])+s.get('corrects',[])): errors.append(f'source history has missing identity: {s.get("id")}')
  if s.get('availability')=='available':
   p=root/(s.get('path') or '')
   if not p.is_file() or p.is_symlink(): errors.append(f'source unavailable or unsafe: {s.get("id")}')
   elif digest(p.read_bytes())!=s.get('sha256'): errors.append(f'source hash mismatch: {s.get("id")}')
  elif s.get('availability') not in {'missing','withdrawn'}: errors.append(f'invalid availability: {s.get("id")}')
  if s.get('kind') in {'ai_summary','scheduled_task_summary'} and s.get('evidence_usable'): errors.append(f'AI/summary source promoted as evidence: {s.get("id")}')
  for o in s.get('observations',[]):
   if o.get('epistemic_class') not in LEVELS: errors.append(f'invalid epistemic class: {o.get("claim_key")}')
   if o.get('relation') not in RELATIONS: errors.append(f'invalid relation: {o.get("claim_key")}')
   if not o.get('scope') or not o.get('uncertainty'): errors.append(f'incomplete observation semantics: {o.get("claim_key")}')
   if any(mid not in mechs for mid in o.get('mechanism_ids',[])): errors.append(f'observation has missing mechanism: {o.get("claim_key")}')
   if any(x not in claim_ids for x in o.get('dependencies',[])+o.get('supersedes',[])+o.get('corrects',[])): errors.append(f'observation history has missing identity: {o.get("claim_key")}')
   if o.get('epistemic_class')=='EVIDENCE' and (not s.get('evidence_usable') or s.get('availability')!='available'): errors.append(f'evidence lacks verified available source: {o.get("claim_key")}')
 names={}
 for m in mechs.values():
  labels=[m.get('name','')]+m.get('aliases',[])
  for label in labels:
   norm=re.sub(r'[^a-z0-9]+','',label.lower())
   if norm in names and names[norm]!=m.get('id'): errors.append(f'duplicate mechanism: {m.get("id")} and {names[norm]}')
   names[norm]=m.get('id')
  if m.get('architecture_class') not in ARCH or not m.get('literal_comparison'): errors.append(f'invalid architecture comparison: {m.get("id")}')
  if m.get('architecture_class')=='genuine_architecture_gap' and not m.get('gap_proof'): errors.append(f'unproved genuine architecture gap: {m.get("id")}')
 graph={}
 for c in conclusions.values():
  if c.get('result_class') not in LEVELS: errors.append(f'invalid conclusion class: {c.get("id")}')
  if any(m not in mechs for m in c.get('required_mechanisms',[])): errors.append(f'conclusion has missing mechanism: {c.get("id")}')
  if any(d not in conclusions for d in c.get('depends_on_conclusions',[])): errors.append(f'conclusion has missing dependency: {c.get("id")}')
  graph[c.get('id')]=c.get('depends_on_conclusions',[])
 visiting=set(); visited=set()
 def visit(n):
  if n in visiting: errors.append('circular support at '+n); return
  if n in visited:return
  visiting.add(n)
  for d in graph.get(n,[]):visit(d)
  visiting.remove(n);visited.add(n)
 for n in graph:visit(n)
 for f in data.get('frontier_rules',[]):
  if any(c not in conclusions for c in f.get('conclusion_ids',[])): errors.append(f'frontier has missing conclusion: {f.get("id")}')
 return sorted(set(errors))

def derive(data,root=ROOT):
 inv=inventory(data,root); findings={}; source_state=[]
 for s in data['sources']:
  active=s['availability']=='available' and s['evidence_usable']
  obs=list(s['observations'])
  if s.get('auto_extractor')=='saturation_falsification_001' and active: obs+=saturation_observations(root)
  source_state.append({'id':s['id'],'path':s.get('path'),'sha256':s.get('sha256'),'availability':s['availability'],'evidence_usable':s['evidence_usable'],'active':active,'evidence_class':s['evidence_class'],'scope':s['scope'],'history':s['history'],'supersedes':s['supersedes'],'corrects':s['corrects']})
  if not active: continue
  for o in obs:
   key=o['claim_key']; projection={k:o.get(k) for k in ('epistemic_class','statement','scope','relation','uncertainty','mechanism_ids','dependencies','supersedes','corrects')}
   if key in findings and {k:findings[key][k] for k in projection}!=projection: raise ValueError('conflicting normalized finding '+key)
   row=findings.setdefault(key,dict(projection,id=key,provenance=[])); row['provenance'].append({'source_id':s['id'],'source_sha256':s.get('sha256'),'version':s.get('version')})
 active_mechs={m for f in findings.values() if f['relation']!='CONTRADICTS' for m in f['mechanism_ids']}; contradictory={m for f in findings.values() if f['relation']=='CONTRADICTS' for m in f['mechanism_ids']}
 mechanisms=[]
 for m in sorted(data['mechanism_catalog'],key=lambda x:x['id']):
  evidence=sorted(f['id'] for f in findings.values() if m['id'] in f['mechanism_ids'])
  mechanisms.append({**m,'finding_ids':evidence,'active':m['id'] in active_mechs,'contradicted':m['id'] in contradictory,'dependency_sha256':digest(canonical([findings[i] for i in evidence]))})
 result_by={}; pending={r['id']:r for r in data['conclusion_rules']}
 while pending:
  ready=[r for r in pending.values() if all(d in result_by for d in r['depends_on_conclusions'])]
  if not ready: raise ValueError('conclusion dependency cycle')
  for rule in ready:
   missing=[m for m in rule['required_mechanisms'] if m not in active_mechs]; contrad=[m for m in rule['required_mechanisms'] if m in contradictory]; stale_deps=[d for d in rule['depends_on_conclusions'] if result_by[d]['epistemic_class']=='UNRESOLVED']
   supported=not missing and not contrad and not stale_deps
   row={'id':rule['id'],'epistemic_class':rule['result_class'] if supported else 'UNRESOLVED','disposition':rule['supported_disposition'] if supported else rule['missing_disposition'],'statement':rule['statement'] if supported else 'Downstream synthesis invalidated: required evidence or conclusion dependencies are unavailable, withdrawn, corrected, or contradicted.','required_mechanisms':rule['required_mechanisms'],'depends_on_conclusions':rule['depends_on_conclusions'],'missing_mechanisms':missing,'contradicted_mechanisms':contrad,'stale_dependencies':stale_deps,'counterevidence':rule['counterevidence']}
   row['dependency_sha256']=digest(canonical({'mechanisms':[m for m in mechanisms if m['id'] in rule['required_mechanisms']],'dependencies':[result_by[d] for d in rule['depends_on_conclusions']]})); result_by[row['id']]=row;del pending[rule['id']]
 conclusions=[result_by[r['id']] for r in data['conclusion_rules']]
 frontier=[]
 for f in data['frontier_rules']:
  linked=[result_by[c] for c in f['conclusion_ids']]; classes={x['epistemic_class'] for x in linked}; cls='UNRESOLVED' if 'UNRESOLVED' in classes else f['epistemic_class']
  frontier.append({**f,'epistemic_class':cls,'status':'OPEN' if cls in {'UNRESOLVED','HYPOTHESIS'} else 'BOUNDED_CURRENT','dependency_sha256':digest(canonical(linked))})
 leads=living_leads(root)
 return {'format_version':'far-research-synthesis/1.1','authority':'Research','generator_sha256':digest(Path(__file__).read_bytes()),'schema_sha256':digest((ROOT/'schemas/far-research-corpus-v1.schema.json').read_bytes()),'corpus_sha256':digest(canonical(data)),'inventory':inv,'inventory_sha256':digest(canonical(inv)),'inventory_complete':True,'sources':source_state,'normalized_findings':sorted(findings.values(),key=lambda x:x['id']),'mechanisms':mechanisms,'conclusions':conclusions,'frontier':frontier,'untrusted_leads':leads,'untrusted_lead_count':len(leads),'nonclaims':data['nonclaims']}

def markdown(r):
 L=['# Current FAR research frontier','','Status: **Generated dependency-aware Research synthesis; not scientific promotion authority**','',f"Corpus identity: `{r['corpus_sha256']}`",f"Inventory identity: `{r['inventory_sha256']}`",'',f"The objective inventory contains **{len(r['inventory'])} material paths**; **{r['untrusted_lead_count']} living/external items remain untrusted discovery leads**. Conclusions carry hashes of their complete downstream dependencies and invalidate when support is missing, withdrawn, corrected, or contradicted.",'','## Reconciled conclusions','','| Conclusion | Class | Disposition | Result |','|---|---|---|---|']
 for x in r['conclusions']:L.append(f"| `{x['id']}` | **{x['epistemic_class']}** | `{x['disposition']}` | {x['statement']} |")
 L+=['','## Deduplicated mechanism comparison','','| Mechanism | Classification | Evidence | Literal comparison |','|---|---|---|---|']
 for x in r['mechanisms']:L.append(f"| `{x['id']}` {x['name']} | `{x['architecture_class']}` | {len(x['finding_ids'])} normalized findings | {x['literal_comparison']} |")
 L+=['','## Frontier','']
 for x in r['frontier']:L += [f"### {x['id']}: {x['question']}",'',f"**{x['epistemic_class']} — {x['status']}.** {x['next_evidence']}",'']
 L += ['## Nonclaims','']+[f'- {n}' for n in r['nonclaims']]
 return '\n'.join(L)+'\n'

def write_living(root=ROOT):
 leads=living_leads(root); out={'format_version':'far-living-corpus-reconciliation/1.0','authority':'Research','candidate_count':len(leads),'candidate_set_sha256':digest(canonical(leads)),'candidates':leads,'promotion_authority':False}; p=root/LIVING_RECONCILIATION;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(canonical(out));return out

def freeze_external(path,origin,root=ROOT):
 raw=path.read_bytes();sha=digest(raw);d=root/'research/corpus/external';d.mkdir(parents=True,exist_ok=True);blob=d/f'{sha}.bin';blob.write_bytes(raw);receipt={'format_version':'far-frozen-input/1.1','sha256':sha,'size':len(raw),'origin':origin,'authority':'discovery_lead','executable':False,'primary_evidence_verified':False,'review_status':'DISCOVERY_LEAD','corpus_route':'research/living/corpus-reconciliation-v1.0.json'};(d/f'{sha}.json').write_bytes(canonical(receipt));write_living(root);print(blob.relative_to(root))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--living-loop',action='store_true');ap.add_argument('--ingest',type=Path);ap.add_argument('--origin',default='outside_scheduler');a=ap.parse_args()
 if a.ingest:freeze_external(a.ingest,a.origin);return 0
 if a.living_loop:write_living()
 data=load(CORPUS);err=validate(data)
 if err:print('\n'.join(err),file=sys.stderr);return 1
 try:r=derive(data)
 except ValueError as e:print(e,file=sys.stderr);return 1
 outs={OUTPUT:canonical(r),STATUS:markdown(r).encode()}
 if a.write:
  for p,b in outs.items():(ROOT/p).write_bytes(b)
 else:
  for p,b in outs.items():
   if not (ROOT/p).exists() or (ROOT/p).read_bytes()!=b:print('stale generated output: '+str(p),file=sys.stderr);return 1
 print(f"research corpus valid: {r['corpus_sha256']} inventory={r['inventory_sha256']} findings={len(r['normalized_findings'])} leads={r['untrusted_lead_count']}");return 0
if __name__=='__main__':raise SystemExit(main())
