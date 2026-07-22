#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'theory/evaluation/sc-w5-held-out-contexts-v1.0.json'
DOC=ROOT/'docs/research/sc-w5-held-out-contexts-v1.0.md'
AUDIT=ROOT/'docs/audits/sc-w5-held-out-contexts-audit.md'
def main()->int:
    for p in (DATA,DOC,AUDIT): assert p.is_file(),p
    d=json.loads(DATA.read_text(encoding='utf-8'))
    assert d['artifact_id']=='SC-W5-HELD-OUT-CONTEXTS-001'
    assert d['status']=='complete_internal_held_out_context_adjudication'
    assert len(d['selection_controls']['strata'])==12
    assert len(d['primitive_extension_rule']['required_conditions'])==7
    assert len(d['contexts'])==12
    assert [x['id'] for x in d['contexts']]==[f'HO-{i:02d}' for i in range(1,13)]
    counts=d['counts']; assert counts=={'total':12,'pass_no_new_primitive':10,'unresolved_evidential_boundary':2,'genuine_primitive_extension':0,'faithful_rccd_failure':0}
    assert sum(x['result']=='pass_no_new_primitive' for x in d['contexts'])==10
    assert sum(x['result']=='unresolved_evidential_boundary' for x in d['contexts'])==2
    for x in d['contexts']:
        assert set(x['rccd_realization'])=={'R1','R2','R3','R4','R5'}
    assert d['terminal_result']=='held_out_contexts_add_no_genuine_kernel_primitive_and_produce_no_faithful_rccd_counterexample_with_two_evidential_unknowns'
    assert d['next_decisive_workstream']=='SC-W6-FINAL-INTERNAL-ADJUDICATION'
    assert any('not counted as positive' in s for s in d['claim_boundary'])
    text=DOC.read_text(encoding='utf-8'); assert 'Ten contexts' in text and 'Two contexts remain evidentially unresolved' in text
    print('SC-W5 held-out contexts: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
