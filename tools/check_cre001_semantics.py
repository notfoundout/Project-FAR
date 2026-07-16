#!/usr/bin/env python3
"""Validate prospective CRE vocabulary semantics against sources and generated artifacts."""
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
    'replaces compiler-authored interpretation as the semantic authority',
    r'Established at CRE-001 vocabulary-semantics scope',
    'CRE-001 deterministic implementation and official vocabulary semantics are complete',
    r'CRE-001 vocabulary semantics are frozen only',
    r'formal vocabulary licensing.*established.*CRE-001',
    r'CRE-001.*formal vocabulary licensing.*established',
]

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path:Path): return json.loads(path.read_text(encoding='utf-8'))
def fail(messages,message): messages.append(message)

def main()->int:
    messages=[]
    if not SPEC.exists(): fail(messages,'missing semantic-specification.json')
    if not LOCK.exists(): fail(messages,'missing semantic-regression-lock.json')
    if messages:
        print('\n'.join(messages),file=sys.stderr); return 1
    spec=load(SPEC); lock=load(LOCK)
    if sha(SPEC)!=lock.get('semantic_specification_sha256'):
        fail(messages,'semantic specification hash differs from semantic-regression-lock.json')
    chronology=spec.get('chronology',{})
    if 'CRE-002' not in json.dumps(chronology): fail(messages,'semantic specification does not mark CRE-002 as first prospective authority')
    if chronology.get('not_retrospective_validation_of')!='CRE-001': fail(messages,'semantic specification does not forbid retrospective CRE-001 validation')
    for rel,expected in lock.get('vocabulary_definition_sha256',{}).items():
        path=BASE/rel
        if sha(path)!=expected: fail(messages,f'vocabulary definition drift: {rel}')
    seen=[]; primitive_records=[]
    for vocab,vdata in spec.get('vocabularies',{}).items():
        prims=vdata.get('primitive_semantics',[])
        if not prims: fail(messages,f'{vocab} has no primitive semantics')
        for prim in prims:
            primitive_records.append((vocab,prim)); seen.append(prim.get('primitive_name'))
            for field in ['identifier','primitive_name','formal_definition','operational_meaning','permitted_commitments','forbidden_commitments','required_properties','optional_properties','closure_conditions','identity_conditions','equivalence_conditions','interaction_rules','limitations','examples','non_examples']:
                if not prim.get(field): fail(messages,f'{vocab}:{prim.get("primitive_name")} missing {field}')
            text=json.dumps(prim,sort_keys=True).lower()
            for claim in NONCLAIMS:
                if claim.lower() not in text: fail(messages,f'{vocab}:{prim.get("primitive_name")} does not preserve nonclaim {claim}')
    expected={'Object','Relation','Transformation','State','Transition','Label','Representation','Representational Structure','Interpretation','Investigation','Calculus'}
    if set(seen)!=expected: fail(messages,f'primitive coverage mismatch: {sorted(set(seen))}')
    doc_text={}
    for doc in DOCS:
        path=SEM/doc
        if not path.exists(): fail(messages,f'missing {doc}'); continue
        text=path.read_text(encoding='utf-8'); doc_text[doc]=text
        for status in REQUIRED_STATUSES:
            if status not in text: fail(messages,f'{doc} missing status {status}')
        for phrase in REQUIRED_CHRONOLOGY:
            if phrase not in text: fail(messages,f'{doc} missing chronology phrase: {phrase}')
        for pattern in FORBIDDEN_RETRO_PATTERNS:
            if re.search(pattern,text,re.I): fail(messages,f'{doc} contains retrospective licensing wording: {pattern}')
    formal=doc_text.get('formal-semantics.md',''); primitive_doc=doc_text.get('primitive-semantics.md',''); licensing=doc_text.get('semantic-licensing.md','')
    for vocab,prim in primitive_records:
        name=prim['primitive_name']; definition=prim['formal_definition']
        if name not in formal: fail(messages,f'formal-semantics missing primitive {name}')
        if name not in licensing: fail(messages,f'semantic-licensing missing primitive {name}')
        if definition not in formal and definition not in primitive_doc:
            fail(messages,f'{vocab}:{name} formal definition differs from semantic-specification.json')
    gen=BASE/'deterministic-verifier/generated'
    for native in gen.glob('*/native-representation.json'):
        data=load(native)
        used={c.get('derived_construct') for c in data.get('constructs',[]) if c.get('derived_construct')}
        declared={d.get('id') for d in data.get('derived_constructs',[])}
        if not used<=EXPECTED_DERIVED: fail(messages,f'{native} uses unclassified derived constructs {sorted(used-EXPECTED_DERIVED)}')
        if not declared<=EXPECTED_DERIVED: fail(messages,f'{native} declares unclassified derived constructs {sorted(declared-EXPECTED_DERIVED)}')
    bad=[r'\bestablish(?:es|ed)? formal vocabulary licensing\b',r'\bestablish(?:es|ed)? primitive sufficiency\b',r'\bestablish(?:es|ed)? universal sufficiency\b',r'\bestablish(?:es|ed)? primitive-only sufficiency\b',r'\bestablish(?:es|ed)? necessity\b',r'\bestablish(?:es|ed)? minimality\b',r'\bestablish(?:es|ed)? independence\b',r'\bestablish(?:es|ed)? superiority\b',r'\bis a FAR proof\b']
    for doc,text in doc_text.items():
        for pattern in bad:
            if re.search(pattern,text,re.I): fail(messages,f'{doc} appears to strengthen unsupported claim: {pattern}')
    if messages:
        print('CRE-001 SEMANTIC CHECK FAILED',file=sys.stderr); print('\n'.join(messages),file=sys.stderr); return 1
    print('CRE-001 SEMANTIC CHECK PASSED'); return 0

if __name__=='__main__': raise SystemExit(main())
