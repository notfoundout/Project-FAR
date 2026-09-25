"""Differential: upstream jsonschema vs the repository-local validator.

Validates every committed document whose top-level discriminator matches a repository schema with
both validators and reports validity disagreements. Run with a Python that has upstream
jsonschema 4.22.0 installed and the repository NOT on sys.path:

    python research/root-of-trust-audit-2026-09/scripts/schema_differential.py <repository root>

Audit result (before and after the local-validator repair): 627 pairs, 0 validity disagreements.
Pairing by discriminator is deliberately loose, so "upstream-invalid" rows include intentionally
invalid fixtures and unrelated documents sharing a discriminator.
"""
import json, subprocess, sys, os, importlib.util
REPO = sys.argv[1]
os.chdir(REPO)
import jsonschema as upstream  # resolved from venv site-packages because REPO not on sys.path
assert 'site-packages' in upstream.__file__, upstream.__file__
spec = importlib.util.spec_from_file_location("shim", os.path.join(REPO, "jsonschema/_validator.py"))
shim = importlib.util.module_from_spec(spec); sys.modules["shim"] = shim; spec.loader.exec_module(shim)
files = subprocess.run(['git','ls-files'],capture_output=True,text=True).stdout.split()
docs = {}
for f in files:
    if f.endswith('.json'):
        try: docs[f] = json.load(open(f))
        except Exception: pass
schemas = {f:d for f,d in docs.items() if isinstance(d,dict) and 'json-schema' in str(d.get('$schema',''))}
pairs = []
for sf, s in schemas.items():
    props = s.get('properties', {})
    disc = {k: v['const'] for k, v in props.items() if isinstance(v, dict) and 'const' in v and k in ('format_version','schema','schema_version','ledger_id','registry_id','graph_id','inventory_id','protocol_version','artifact_format','format','native_format','package_id')}
    # use the most specific discriminators: format_version/schema alone, else all
    key = {k:v for k,v in disc.items() if k in ('format_version','schema')} or disc
    if not key: continue
    for df, d in docs.items():
        if df in schemas or not isinstance(d, dict): continue
        if all(d.get(k) == v for k, v in key.items()):
            pairs.append((sf, df))
disagree = []; up_invalid = []
for sf, df in pairs:
    s = schemas[sf]; d = docs[df]
    try:
        up = sorted(e.message for e in upstream.Draft202012Validator(s).iter_errors(d))
    except Exception as exc:
        up = [f"UPSTREAM EXCEPTION {type(exc).__name__}"]
    try:
        sh = sorted(e.message for e in shim.Draft202012Validator(s).iter_errors(d))
    except Exception as exc:
        sh = [f"SHIM EXCEPTION {exc!r}"]
    if up:
        up_invalid.append((sf, df, up[:3]))
    if bool(up) != bool(sh):
        disagree.append((sf, df, up[:3], sh[:3]))
print(f"pairs checked: {len(pairs)}")
print(f"validity disagreements: {len(disagree)}")
for row in disagree: print("DISAGREE", row)
print(f"documents invalid under upstream: {len(up_invalid)}")
for row in up_invalid: print("UPSTREAM-INVALID", row)
