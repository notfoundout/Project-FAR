#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path
import yaml
from common_health import ROOT, iter_files, rel
errors=[]; registry_ids=defaultdict(list); proof_ids=defaultdict(list); adversarial_ids=defaultdict(list)
REGISTRY_NAMES=('registry','adversarial')

def resolve_ref(p, v):
    cands=[(p.parent/v).resolve(), (ROOT/v).resolve()]
    return any(c.exists() for c in cands)

for p in iter_files({'.yaml','.yml'}):
    try:
        data=yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'{rel(p)}: invalid YAML: {e}'); continue
    if isinstance(data, dict) and isinstance(data.get('id'), (str,int)):
        if 'proof-objects' in p.parts and p.name.startswith('T-'):
            proof_ids[str(data['id'])].append(p)
        elif any(n in p.name for n in REGISTRY_NAMES):
            registry_ids[str(data['id'])].append(p)
    def walk(x, parent_key=''):
        if isinstance(x, dict):
            if any(n in p.name for n in REGISTRY_NAMES) and isinstance(x.get('id'), (str,int)):
                key=(rel(p), str(x['id']))
                registry_ids[str(x['id'])].append(p)
            for k,v in x.items():
                kl=str(k).lower()
                if isinstance(v,str) and (kl.endswith('path') or kl.endswith('file') or kl in {'path','file','fixture','report','source'}):
                    if not v.startswith(('http://','https://')) and ('/' in v or '.' in v) and not resolve_ref(p, v):
                        errors.append(f'{rel(p)}: referenced path missing: {v}')
                walk(v, kl)
        elif isinstance(x, list):
            for v in x: walk(v, parent_key)
    walk(data)
# Unique top-level proof-object ids.
for idv,paths in proof_ids.items():
    if len(paths)>1: errors.append(f'duplicate proof object id {idv}: '+', '.join(sorted({rel(p) for p in paths})))
# Unique adversarial case ids within adversarial suite files.
for p in iter_files({'.yaml','.yml'}):
    if 'adversarial' not in p.name: continue
    try: data=yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception: continue
    local=defaultdict(int)
    def ids(x):
        if isinstance(x, dict):
            if isinstance(x.get('id'), (str,int)): local[str(x['id'])]+=1
            for v in x.values(): ids(v)
        elif isinstance(x, list):
            for v in x: ids(v)
    ids(data)
    for idv,count in local.items():
        if count>1: errors.append(f'{rel(p)}: duplicate adversarial suite id {idv}')
for e in errors: print('FAIL', e)
if errors: raise SystemExit(1)
print('Repository hygiene OK')
