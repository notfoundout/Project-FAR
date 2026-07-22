#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w6-global-reconstruction-v1.0.json'
RESEARCH=ROOT/'docs/research/ikd-w6-global-reconstruction-v1.0.md'
AUDIT=ROOT/'docs/audits/ikd-w6-global-reconstruction-audit.md'
def main()->int:
    for path in (RESULT,RESEARCH,AUDIT): assert path.is_file(),path
    data=json.loads(RESULT.read_text(encoding='utf-8'))
    assert data['result_id']=='IKD-W6-GLOBAL-RECONSTRUCTION-001'
    assert data['status']=='complete_expanded_registered_reconstruction_search'
    assert data['target_pr']==266 and data['kernel_under_test']=='RCCD-001'
    contract=data['reconstruction_contract']
    for key in ('semantic_and_operational_preservation_required','dependency_revision_and_historical_identity_preserved','uniform_bounded_query_recovery_required','strict_cost_improvement_required_for_replacement','all_synthesis_search_decoding_and_certificate_machinery_charged','equivalent_reintroduction_counted_as_rccd'):
        assert contract[key] is True,key
    bases=data['searched_bases']; assert len(bases)>=14
    results={x['result'] for x in bases}
    assert {'fail','equivalent_reintroduction','no_strict_improvement'}<=results
    ids={x['id'] for x in bases}; assert {'RB-REL','RB-TRANS','RB-PROV','RB-CAUSAL','RB-PROOF','RB-TYPE','RB-PROC','RB-COALG','RB-INFO','RB-ALG','RB-CAT','RB-DYN','RB-DB','RB-MDL'}<=ids
    assert len(data['automated_search']['families'])>=7
    assert len(data['automated_search']['adversarial_objectives'])>=6
    assert len(data['surviving_countermodels'])>=5
    assert len(data['machinery_ledger'])>=10
    assert data['terminal_result']=='no_strictly_cheaper_non_equivalent_reconstruction_found_in_expanded_registered_search'
    effect=data['claim_effect']; assert effect['rccd_survives_expanded_alternative_basis_search']=='supported'; assert effect['global_necessity']=='not_yet_proved'
    assert data['next_decisive_workstream']=='IKD-W7-LOWER-BOUNDS'
    nonclaims='\n'.join(data['nonclaims']); assert 'every logically possible vocabulary' in nonclaims; assert 'globally necessary' in nonclaims
    research=RESEARCH.read_text(encoding='utf-8'); audit=AUDIT.read_text(encoding='utf-8')
    assert 'Failure to find a replacement is not treated as a proof of global nonexistence' in audit
    assert 'no_strictly_cheaper_non_equivalent_reconstruction_found_in_expanded_registered_search' in research
    print('IKD-W6 expanded global reconstruction: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
