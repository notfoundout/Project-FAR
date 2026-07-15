#!/usr/bin/env python3
from __future__ import annotations
import sys, yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOWED={"narrative_argument","structurally_checked_proof_object","semantically_constrained_proof_object","machine_verified_formal_proof","independently_reviewed_proof"}
def main():
    data=yaml.safe_load((ROOT/'theory/metadata/theorems.yaml').read_text())
    errors=[]
    for t in data.get('theorems',[]):
        a=t.get('assurance_level')
        if a not in ALLOWED: errors.append(f"{t.get('id')} invalid assurance_level {a}")
        if a=='machine_verified_formal_proof': errors.append(f"{t.get('id')} claims unsupported machine proof")
        if 'conditional' in str(t.get('title','')).lower() and 'conditional' not in str(t.get('scope','')).lower() and t.get('theorem_category')!='conditional': errors.append(f"{t.get('id')} conditional title lacks conditional metadata")
    if errors:
        print('PROOF ASSURANCE CHECK FAILED'); print('\n'.join('- '+e for e in errors)); return 1
    print('Proof assurance metadata OK'); return 0
if __name__=='__main__': raise SystemExit(main())
