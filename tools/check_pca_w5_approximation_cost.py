"""Recompute the complete governed PCA-W5 finite-explicit result set."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mechanization.far_mechanization.contract_v21 import validate_contract
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=json.loads((ROOT/'research/results/pca-w5-approximation-and-cost/manifest.json').read_text())
 errors=[]
 for item in manifest['artifacts']:
  p=ROOT/item['path']
  if not p.is_file():errors.append(f"MISSING {item['path']}")
  elif sha(p)!=item['sha256']:errors.append(f"HASH {item['path']}")
 for rel in manifest['checked_records']:
  d=json.loads((ROOT/rel).read_text());r=validate_contract(d)
  errors += [f'{rel}: {x.code}: {x.message}' for x in r.diagnostics]
 if errors:
  print('\n'.join(errors));return 1
 print(f"PCA-W5 PASS: {len(manifest['checked_records'])} records; terminal verdict {manifest['terminal_verdict']}");return 0
if __name__=='__main__':raise SystemExit(main())
