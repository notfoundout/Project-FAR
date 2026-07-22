#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / 'theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json'
DOC = ROOT / 'docs/research/usd-w2-alternative-vocabulary-competition-v1.0.md'
AUDIT = ROOT / 'docs/audits/usd-w2-alternative-vocabulary-competition-audit.md'

def main() -> int:
    for path in (RESULT, DOC, AUDIT):
        assert path.is_file(), path
    data = json.loads(RESULT.read_text(encoding='utf-8'))
    assert data['competition_id'] == 'USD-W2-ALT-001'
    assert data['status'] == 'complete_bounded_comparison'
    assert data['aggregation_rule'] == 'pareto_only_no_scalar_overall_winner'
    candidates = {c['id']: c for c in data['candidates']}
    assert set(candidates) == {'FARA-001','GREL-001','LTS-PROV-001','ARG-HIST-001'}
    assert sum(bool(c['independently_motivated']) for c in candidates.values()) >= 2
    assert candidates['GREL-001']['family'] == 'generic_relational_vocabulary'
    assert data['terminal_result'] == 'multiple_incomparable_successful_vocabularies'
    assert data['winner'] is None
    pairs = {(p['left'], p['right']): p['classification'] for p in data['pairwise_results']}
    assert pairs[('FARA-001','GREL-001')] == 'FARA_pareto_dominates_on_registered_bounded_scope'
    assert pairs[('FARA-001','LTS-PROV-001')] == 'incomparable_tradeoff'
    assert data['hypothesis_effect']['USD-H-EXIST'] == 'unresolved'
    assert data['next_decisive_workstream'] == 'USD-W3-INVARIANCE'
    text = DOC.read_text(encoding='utf-8') + AUDIT.read_text(encoding='utf-8')
    for phrase in ('no scalar winner','multiple_incomparable_successful_vocabularies','does not establish'):
        assert phrase in text
    print('USD-W2 alternative-vocabulary competition: PASS')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
