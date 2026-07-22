#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w3-common-factor-v1.0.json'
COMP=ROOT/'theory/evaluation/ikd-w2-expanded-candidate-competition-v1.0.json'
RESEARCH=ROOT/'docs/research/ikd-w3-common-factor-v1.0.md'
AUDIT=ROOT/'docs/audits/ikd-w3-common-factor-audit.md'
def load(path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    for path in (RESULT,COMP,RESEARCH,AUDIT): assert path.is_file(),path
    result=load(RESULT); comp=load(COMP)
    assert result['result_id']=='IKD-W3-COMMON-FACTOR-001'
    assert result['status']=='complete_bounded_common_factor_search'
    assert result['target_pr']==263
    assert result['successful_architectures']==comp['successful_set']
    assert result['method']['candidate_neutral'] is True
    assert result['method']['label_intersection_insufficient'] is True
    assert result['method']['generic_graph_or_state_transition_structure_insufficient'] is True
    factors={x['id']:x for x in result['tested_factor_candidates']}
    assert factors['CF-GRAPH']['classification']=='rejected_generic'
    assert factors['CF-INTERPRETER']['classification']=='rejected_escape_hatch'
    assert factors['RCCD-001']['classification']=='supported_boundedly'
    kernel=result['common_factor']
    assert kernel['id']=='RCCD-001'
    assert len(kernel['commitments'])==5
    assert set(kernel['architecture_realizations'])==set(comp['successful_set'])
    assert 'need not share labels' in kernel['translation_rule']
    assert 'equivalent reintroductions are charged' in kernel['cost_rule']
    controls=set(result['negative_controls'])
    for required in ('dependency_erasure_rejected','retroactive_history_rewrite_rejected','unrestricted_interpreter_rejected','source_specific_decoder_rejected','future_history_access_rejected','generic_transition_structure_rejected_as_sufficient'): assert required in controls
    assert result['terminal_result']=='one_bounded_nontrivial_common_factor_candidate_supported'
    assert result['claim_effect']['common_factor_existence_on_frozen_scope']=='supported'
    assert result['claim_effect']['universal_structure']=='unresolved'
    assert result['next_decisive_workstream']=='IKD-W4-CROSS-FEATURE-COMPOSITION'
    assert 'Separate featurewise success is not compositional closure' in RESEARCH.read_text(encoding='utf-8')
    assert 'bounded_nontrivial_common_factor_candidate_supported_composition_unresolved' in AUDIT.read_text(encoding='utf-8')
    print('IKD-W3 common-factor search: PASS (RCCD-001 supported boundedly; composition unresolved)')
    return 0
if __name__=='__main__': raise SystemExit(main())
