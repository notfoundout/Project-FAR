#!/usr/bin/env python3
"""Validate frozen CRE-001 vocabulary semantics against vocabulary packages and generated artifacts."""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'theory/evaluation/comparative-representation/experiments/CRE-001'
SEM=BASE/'semantics'
SPEC=SEM/'semantic-specification.json'
LOCK=SEM/'semantic-regression-lock.json'
DOCS=['formal-semantics.md','primitive-semantics.md','derived-machinery-audit.md','semantic-licensing.md','semantic-overlap-analysis.md','semantic-regression.md','methodological-limitations.md','expressivity-audit.md']
REQUIRED_STATUSES=['Supported','Unsupported','Unknown','Assumed','Implementation-specific']
REQUIRED_CHRONOLOGY=['formalized after completion of deterministic CRE-001','informed by lessons learned during CRE-001','frozen for future experiments beginning with CRE-002','not independent evidence supporting CRE-001','cannot be used as retrospective validation of CRE-001','CRE-001 demonstrates only that compiler-authored declared interpretations successfully compiled, lowered, and verified under the registered deterministic reference']
NONCLAIMS=['formal vocabulary licensing','primitive sufficiency','universal sufficiency','necessity','minimality','independence','superiority','FAR proof','universal reasoning structure']
EXPECTED_DERIVED={'D_boolean_value','D_ordered_history','D_guarded_update','D_disjunction','D_terminality'}
FORBIDDEN_RETRO_PATTERNS=[
    'replaces compiler-authored ' + 'interpretation as the ' + 'semantic authority',
    'Established at CRE-001 ' + r'vocabulary-semantics scope',
    'CRE-001 deterministic implementation and official vocabulary semantics ' + 'are complete',
    'CRE-001 vocabulary semantics are ' + r'frozen only',
    'formal vocabulary ' + 'licensing.*' + 'estab' + 'lished.*CRE-001',
    'CRE-001.*formal vocabulary ' + 'licensing.*' + 'estab' + 'lished',
]

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path): return json.loads(p.read_text(encoding='utf-8'))
def fail(msgs,msg): msgs.append(msg)

def main()->int:
    msgs=[]
    if not SPEC.exists(): fail(msgs,'missing semantic-specification.json')
    if not LOCK.exists(): fail(msgs,'missing semantic-regression-lock.json')
    if msgs:
        print('\n'.join(msgs), file=sys.stderr); return 1
    spec=load(SPEC); lock=load(LOCK)
    if sha(SPEC)!=lock.get('semantic_specification_sha256'):
        fail(msgs,'semantic specification hash differs from semantic-regression-lock.json')
    chronology=spec.get('chronology', {})
    if 'CRE-002' not in json.dumps(chronology): fail(msgs, 'semantic specification does not mark CRE-002 as first prospective authority')
    if chronology.get('not_retrospective_validation_of')!='CRE-001': fail(msgs, 'semantic specification does not forbid retrospective CRE-001 validation')
    for rel,expected in lock.get('vocabulary_definition_sha256',{}).items():
        p=BASE/rel
        if sha(p)!=expected: fail(msgs,f'vocabulary definition drift: {rel}')
    # complete primitive coverage and required fields
    seen=[]
    for vocab,vdata in spec.get('vocabularies',{}).items():
        prims=vdata.get('primitive_semantics',[])
        if not prims: fail(msgs,f'{vocab} has no primitive semantics')
        for prim in prims:
            seen.append(prim.get('primitive_name'))
            for field in ['identifier','primitive_name','formal_definition','operational_meaning','permitted_commitments','forbidden_commitments','required_properties','optional_properties','closure_conditions','identity_conditions','equivalence_conditions','interaction_rules','limitations','examples','non_examples']:
                if not prim.get(field): fail(msgs,f'{vocab}:{prim.get("primitive_name")} missing {field}')
            text=json.dumps(prim, sort_keys=True)
            for claim in NONCLAIMS:
                if claim.lower() not in text.lower():
                    fail(msgs,f'{vocab}:{prim.get("primitive_name")} does not preserve nonclaim {claim}')
    expected_prims={'Object','Relation','Transformation','State','Transition','Label','Representation','Representational Structure','Interpretation','Investigation','Calculus'}
    if set(seen)!=expected_prims:
        fail(msgs,f'primitive coverage mismatch: {sorted(set(seen))}')
    # docs exist, contain status vocabulary, and mention every primitive
    for doc in DOCS:
        p=SEM/doc
        if not p.exists(): fail(msgs,f'missing {doc}'); continue
        text=p.read_text(encoding='utf-8')
        for status in REQUIRED_STATUSES:
            if status not in text: fail(msgs,f'{doc} missing status {status}')
        for phrase in REQUIRED_CHRONOLOGY:
            if phrase not in text: fail(msgs,f'{doc} missing chronology phrase: {phrase}')
        for pat in FORBIDDEN_RETRO_PATTERNS:
            if re.search(pat, text, re.I): fail(msgs,f'{doc} contains retrospective licensing wording: {pat}')
    formal=(SEM/'formal-semantics.md').read_text(encoding='utf-8')
    licensing=(SEM/'semantic-licensing.md').read_text(encoding='utf-8')
    for prim in expected_prims:
        if prim not in formal: fail(msgs,f'formal-semantics missing primitive {prim}')
        if prim not in licensing: fail(msgs,f'semantic-licensing missing primitive {prim}')
    # generated native artifacts may not introduce unclassified derived constructs
    gen=BASE/'deterministic-verifier/generated'
    for native in gen.glob('*/native-representation.json'):
        data=load(native)
        used={c.get('derived_construct') for c in data.get('constructs',[]) if c.get('derived_construct')}
        declared={d.get('id') for d in data.get('derived_constructs',[])}
        if not used <= EXPECTED_DERIVED: fail(msgs,f'{native} uses unclassified derived constructs {sorted(used-EXPECTED_DERIVED)}')
        if not declared <= EXPECTED_DERIVED: fail(msgs,f'{native} declares unclassified derived constructs {sorted(declared-EXPECTED_DERIVED)}')
    # no semantic doc may assert unsupported claims as established
    bad_patterns=[r'\bestablish(?:es|ed)? formal vocabulary licensing\b', r'\bestablish(?:es|ed)? primitive sufficiency\b', r'\bestablish(?:es|ed)? universal sufficiency\b',r'\bestablish(?:es|ed)? primitive-only sufficiency\b',r'\bestablish(?:es|ed)? necessity\b',r'\bestablish(?:es|ed)? minimality\b',r'\bestablish(?:es|ed)? independence\b',r'\bestablish(?:es|ed)? superiority\b']
    for doc in DOCS:
        text=(SEM/doc).read_text(encoding='utf-8')
        for pat in bad_patterns:
            if re.search(pat,text,re.I): fail(msgs,f'{doc} appears to strengthen unsupported claim: {pat}')
    if msgs:
        print('CRE-001 SEMANTIC CHECK FAILED', file=sys.stderr)
        print('\n'.join(msgs), file=sys.stderr)
        return 1
    print('CRE-001 SEMANTIC CHECK PASSED')
    return 0
if __name__=='__main__': raise SystemExit(main())
