#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / 'theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json'
FIXTURES = ROOT / 'theory/evaluation/usd-w1-infinite-carriers-fixtures-v1.0.json'
RESULT = ROOT / 'theory/evaluation/usd-w1-infinite-carriers-extension-result-v1.0.json'
PROOF = ROOT / 'docs/research/usd-w1-infinite-carriers-extension-proof-v1.0.md'
AUDIT = ROOT / 'docs/audits/usd-w1-infinite-carriers-extension-audit.md'


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    for path in (SCOPE, FIXTURES, RESULT, PROOF, AUDIT):
        assert path.is_file(), path
    scope = load(SCOPE)
    fixtures = load(FIXTURES)
    result = load(RESULT)
    assert scope['scope_id'] == 'USD-W1-INF-SCOPE-001'
    assert scope['status'] == 'frozen_executed'
    assert scope['feature_family'] == 'infinite_carriers'
    assert scope['source_class'] == 'S_inf_eff'
    assert scope['candidate_independent'] is True
    assert scope['material_change_requires_new_version'] is True
    obligations = scope['preservation_obligations']
    assert len(obligations) == 8 and len(set(obligations)) == 8
    assert {'uncountable_carriers', 'non_effectively_presented_countable_carriers', 'actual_process_correspondence'} <= set(scope['excluded_cases'])
    by_id = {item['id']: item for item in fixtures['fixtures']}
    assert set(by_id) == {'INF-NAT-STEP-001', 'INF-TREE-001', 'INF-PREFIX-001', 'INF-NEG-TRUNC-001', 'INF-NEG-ORACLE-001', 'INF-BOUNDARY-NONCOMP-001'}
    assert result['result_id'] == 'USD-W1-INF-RESULT-001'
    assert result['status'] == 'complete_bounded_extension_proved'
    assert result['scope_contract'] == scope['scope_id']
    assert result['source_class'] == 'S_inf_eff'
    assert result['new_target_primitive'] is False
    assert set(result['proved_obligations']) == set(obligations)
    assert result['terminal_outcome'] == 'proper_subclass_only'
    expected = {item['id']: item['expected'] for item in fixtures['fixtures']}
    assert result['fixture_results'] == expected
    assert result['theorem_effect']['THM-IRD-EXT-001'] == 'partial_progress_second_feature_subclass_resolved'
    assert result['claim_effect']['effective_countable_infinite_carrier_representation'] == 'proved_for_S_inf_eff'
    assert result['claim_effect']['S_IRD_representation'] == 'unresolved'
    assert result['claim_effect']['universal_structure'] == 'unresolved'
    assert result['machine_check_status'] == 'not_mechanized'
    assert result['independent_review_status'] == 'not_started'
    proof = PROOF.read_text(encoding='utf-8')
    for obligation in obligations:
        assert obligation.split('_', 1)[0] in proof
    assert 'proper_subclass_only' in proof
    assert 'does not establish `S_IRD` representation' in proof
    audit = AUDIT.read_text(encoding='utf-8')
    assert 'finite truncation' in audit and 'oracle' in audit
    print('USD-W1 infinite carriers: PASS (S_inf_eff proved; broader claims unresolved)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
