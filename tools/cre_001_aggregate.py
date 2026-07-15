#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
REQUIRED={'evaluator_id','vocabulary_id','preservation_scores','complexity_summary','sufficiency'}
VALID={'Pass','Partial','Fail','Unknown'}
def load(path: Path):
    data=json.loads(path.read_text())
    missing=REQUIRED-set(data)
    if missing: raise ValueError(f'{path}: missing {sorted(missing)}')
    if data['sufficiency'].get('existential') not in VALID or data['sufficiency'].get('reproducible') not in VALID:
        raise ValueError(f'{path}: invalid sufficiency value')
    return data
def summarize(records):
    vocab={r['vocabulary_id']: r for r in records}
    if len(vocab)!=3: raise ValueError('exactly three vocabulary mappings are required')
    return {
        'artifact_type':'CRE-001 synthetic-or-real aggregation',
        'vocabularies': sorted(vocab),
        'existential_sufficiency': {k:v['sufficiency']['existential'] for k,v in sorted(vocab.items())},
        'reproducible_sufficiency': {k:v['sufficiency']['reproducible'] for k,v in sorted(vocab.items())},
        'preservation_scores': {k:v['preservation_scores'] for k,v in sorted(vocab.items())},
        'complexity_summary': {k:v['complexity_summary'] for k,v in sorted(vocab.items())},
        'pareto_logic': 'applied only to submitted preservation and complexity summaries; Unknown remains unresolved',
        'scientific_conclusion': 'none; aggregation does not create evidence beyond registered decision rules',
    }
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('artifacts', nargs='+', type=Path); ap.add_argument('--output', type=Path)
    args=ap.parse_args()
    try: out=summarize([load(p) for p in args.artifacts])
    except Exception as e: print(f'CRE-001 AGGREGATION FAILED: {e}', file=sys.stderr); return 1
    text=json.dumps(out, indent=2, sort_keys=True)
    if args.output: args.output.write_text(text+'\n')
    else: print(text)
    return 0
if __name__=='__main__': raise SystemExit(main())
