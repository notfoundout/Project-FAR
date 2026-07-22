#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/s-core-w5-theorem-assembly-proof-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-w5-theorem-assembly-proof.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
 for p in (DOC,REG,LEDGER): assert p.is_file(),p
 text=DOC.read_text(encoding='utf-8'); assert 'ASM-SC-001' in text and 'ASM-SC-002' in text and 'ASM-SC-003' in text; assert 'does not establish representation of `S_IRD`' in text
 r=load(REG); assert r['proof_id']=='SCORE-W5-PROOF-001' and r['status']=='complete_bounded_deductive_assembly'; assert r['source_scope']=='S_core' and r['faithful_predicate']=='Faithful_split' and r['p8_mode']=='split'; assert r['premise_change'] is False and r['source_scope_change'] is False and r['target_interface_change'] is False and r['new_target_primitive'] is False
 by={x['id']:x for x in r['assembly_results']}; assert set(by)=={'ASM-SC-001','ASM-SC-002','ASM-SC-003'}; assert all(x['status']=='proved' for x in by.values()); assert by['ASM-SC-001']['theorem_effect']['THM-CORE-COMMON-001']=='proved_for_S_core'; assert by['ASM-SC-002']['theorem_effect']['THM-CORE-REP-001']=='proved_for_S_core'; assert by['ASM-SC-003']['theorem_effect']['THM-IMP-001']=='refuted_for_S_core_under_frozen_target'
 effects=r['claim_effect']; assert effects['bounded_common_schema_existence']=='proved' and effects['bounded_faithful_representation']=='proved'; assert effects['S_IRD_representation']=='unresolved' and effects['universal_structure']=='unresolved'; assert effects['primitive_necessity']=='not_established' and effects['minimality']=='not_established' and effects['uniqueness']=='not_established'
 l=load(LEDGER); items={x['id']:x for x in l['obligations']}; assert all(items[f'ASM-SC-{i:03d}']['status']=='proved' for i in range(1,4)); assert l['execution_summary']['open']==0 and l['execution_summary']['proved']==27
 print('S_core W5 theorem assembly: PASS (bounded theorem proved; broader claims unresolved)'); return 0
if __name__=='__main__': raise SystemExit(main())
