#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w5-expanded-invariance-v1.0.json'
RESEARCH=ROOT/'docs/research/ikd-w5-expanded-invariance-v1.0.md'
AUDIT=ROOT/'docs/audits/ikd-w5-expanded-invariance-audit.md'
def load(path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    for path in (RESULT,RESEARCH,AUDIT): assert path.is_file(),path
    r=load(RESULT)
    assert r['result_id']=='IKD-W5-EXPANDED-INVARIANCE-001'
    assert r['status']=='complete_bounded_expanded_invariance_analysis'
    assert r['target_pr']==265 and r['kernel_under_test']=='RCCD-001'
    c=r['invariance_contract']
    for key in ('bidirectional_commitment_recovery_required','operational_consequences_preserved','dependency_and_ground_structure_preserved','revision_and_historical_identity_preserved','bounded_query_interface_preserved','all_encoders_decoders_adapters_canonicalizers_and_proof_objects_charged','unrestricted_interpreters_prohibited','future_information_oracles_prohibited'): assert c[key] is True,key
    tx=r['executed_transformations']; assert len(tx)==12
    assert len({x['id'] for x in tx})==12; assert all(x['result']=='pass' for x in tx)
    names={x['name'] for x in tx}
    required={'event_state_interchange','semantic_dualization','causal_intervention_encoding','proof_object_encoding','type_theoretic_encoding','process_algebra_encoding','coalgebraic_encoding','history_event_sourcing_encoding','probability_representation_change','partial_observation_factorization','continuous_discrete_time_normalization','history_rechunking_and_state_factorization'}
    assert names==required
    rejected=set(r['rejected_non_equivalences'])
    for item in ('dependency_erasure','retroactive_revision_rewrite','semantic_version_merging','scheduler_hiding','future_history_access','unrestricted_interpreter_or_source_specific_decoder'): assert item in rejected
    assert len(r['machinery_ledger'])>=10
    assert r['terminal_result']=='bounded_expanded_representation_invariance_supported'
    assert r['claim_effect']['all_possible_representation_changes']=='not_supported'
    assert r['next_decisive_workstream']=='IKD-W6-GLOBAL-RECONSTRUCTION'
    nonclaims='\n'.join(r['nonclaims'])
    for phrase in ('every conceivable encoding','globally necessary','actual-process correspondence','external validation'): assert phrase in nonclaims
    assert 'twelve materially different families' in RESEARCH.read_text(encoding='utf-8')
    assert 'Behavioral or observational equivalence is not internal-process identity' in AUDIT.read_text(encoding='utf-8')
    print('IKD-W5 expanded invariance: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
