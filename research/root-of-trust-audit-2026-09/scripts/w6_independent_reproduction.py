"""Independent PCA-W6 reproduction under three JSON Schema validators.

    python w6_independent_reproduction.py current  <repository root>
    python w6_independent_reproduction.py frozen   <repository root> <dir containing jsonschema/>
    <python with upstream jsonschema> w6_independent_reproduction.py upstream <repository root>

For "frozen", extract the protocol-base validator first:
    mkdir -p /tmp/w6shim/jsonschema && git show 2cecf2e21cc27208f606dcd38337af4369e66af2:jsonschema/__init__.py > /tmp/w6shim/jsonschema/__init__.py

It does not import the W6 checker or the FAR verifier. It applies its own mutation (per the
preregistration text) and decides sufficiency by partition refinement with numbers compared as
exact rationals (1 == 1.0), a deliberately different equality from canonical JSON. Audit result
under all three validators: schema-only baseline 0/6, schema accepts 6/6 clean, oracle says
clean sufficient 6/6, mutants insufficient 6/6, native lossy insufficient 6/6.
"""
import json, sys, copy, importlib, os
from fractions import Fraction
from decimal import Decimal
mode = sys.argv[1]  # frozen | current | upstream
REPO = sys.argv[2]
if mode == 'frozen':
    sys.path.insert(0, sys.argv[3])
elif mode == 'current':
    sys.path.insert(0, REPO)
import jsonschema
print(mode, "validator from", jsonschema.__file__)
def norm(v):
    if isinstance(v, bool) or v is None: return ('lit', v)
    if isinstance(v, (int, float)): return ('num', Fraction(Decimal(repr(v))) if isinstance(v, float) else Fraction(v))
    if isinstance(v, str): return ('str', v)
    if isinstance(v, list): return ('arr', tuple(norm(x) for x in v))
    if isinstance(v, dict): return ('obj', tuple(sorted((k, norm(x)) for k, x in v.items())))
    raise TypeError(v)
def sufficient(doc):
    c = doc['contract']
    ids = [x['id'] for x in c['source_domain']['cases']]
    beh = {r['case_id']: norm(r['value']) for r in c['required_behavior']['table']}
    rep = {r['case_id']: norm(r['value']) for r in c['representation']['table']}
    assert sorted(ids) == sorted(beh) == sorted(rep) and len(ids) == len(set(ids))
    blocks = {}
    for i in ids: blocks.setdefault(rep[i], set()).add(beh[i])
    return all(len(b) == 1 for b in blocks.values())
schema = json.load(open(os.path.join(REPO, 'schemas/far-contract-v2.schema.json')))
V = jsonschema.Draft202012Validator(schema)
man = json.load(open(os.path.join(REPO, 'research/results/pca-w4-domain-contracts/manifest.json')))
rows = []
for rec in man['records']:
    doc = json.load(open(os.path.join(REPO, rec['path'])))
    if rec['variant'] != 'repaired':
        rows.append((rec['path'].split('/')[-1], 'native-lossy', not list(V.iter_errors(doc)), sufficient(doc))); continue
    # my own mutation per preregistration text: second case's representation := first case's
    m = copy.deepcopy(doc)
    first, second = [x['id'] for x in m['contract']['source_domain']['cases']]
    t = {r['case_id']: r for r in m['contract']['representation']['table']}
    t[second]['value'] = copy.deepcopy(t[first]['value'])
    rows.append((rec['path'].split('/')[-1], 'clean', not list(V.iter_errors(doc)), sufficient(doc)))
    rows.append((rec['path'].split('/')[-1], 'mutant', not list(V.iter_errors(m)), sufficient(m)))
for r in rows: print(r)
clean = [r for r in rows if r[1]=='clean']; mut = [r for r in rows if r[1]=='mutant']; lossy=[r for r in rows if r[1]=='native-lossy']
print("schema-only baseline detects mutants:", sum(not r[2] for r in mut), "/", len(mut))
print("schema accepts clean:", sum(r[2] for r in clean), "/", len(clean))
print("oracle: clean sufficient", sum(r[3] for r in clean), "/", len(clean), "; mutants insufficient", sum(not r[3] for r in mut), "/", len(mut), "; native lossy insufficient", sum(not r[3] for r in lossy), "/", len(lossy))
