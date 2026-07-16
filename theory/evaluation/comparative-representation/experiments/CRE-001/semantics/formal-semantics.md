# Vocabulary Semantics Baseline 1.0


## Status Vocabulary

- **Supported**: prospectively frozen for CRE-002 and later experiments by explicit baseline definitions and this specification.
- **Unsupported**: not established and not licensed by this specification.
- **Unknown**: not determined by available repository evidence.
- **Assumed**: required CRE-001-scoped assumption recorded explicitly.
- **Implementation-specific**: property of the deterministic compiler/verifier artifacts, not primitive semantics.

## Chronology and Prospective Authority

- Vocabulary Semantics Baseline 1.0 was formalized after completion of deterministic CRE-001.
- It was informed by lessons learned during CRE-001.
- It is frozen for future experiments beginning with CRE-002.
- It is not independent evidence supporting CRE-001.
- It cannot be used as retrospective validation of CRE-001.
- CRE-001 demonstrates only that compiler-authored declared interpretations successfully compiled, lowered, and verified under the registered deterministic reference.


## Scope

This document records Vocabulary Semantics Baseline 1.0 for the official vocabulary primitives. It is a prospective baseline for CRE-002 and later experiments. It does not retroactively validate CRE-001, does not license CRE-001 results, and does not modify deterministic results, compiler behavior, verifier behavior, or FAR theory.

## Supported

- Prospective primitive semantic specifications for Vocabulary A, B, and C, frozen as Baseline 1.0 for CRE-002 and later experiments.

- Explicit derived-machinery classifications.

- Prospective semantic licensing tables for future experiments beginning with CRE-002.

## Unsupported

- Universal sufficiency, primitive-only sufficiency, necessity, minimality, independence, superiority, FAR proof, and universal reasoning structure.

## Unknown

- Whether these semantics suffice for any non-CRE-001 scenario.

- Whether a simpler vocabulary can dominate any official vocabulary.

## Assumed

- CRE-001 scenario scope and registered ambiguity policies remain fixed.

## Implementation-specific

- Compiler lowering rules and verifier depth remain implementation artifacts, not semantic definitions.

## CRE-001-VOCAB-A-1.0

### Object

- Identifier: `CRE-001-VOCAB-A-1.0:Object`

- Formal definition: Within CRE-001 scope, Object denotes a discrete item, entity, token, state-bearing item, rule, or record treated as a unit of representation. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: unit individuation

- Permitted commitments: unit individuation; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: object identity is by declared identifier within CRE-001 mapping scope

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Object used with recorded role in CRE-001 mapping

- Non-examples: Object used to import an unrecorded domain rule or universal conclusion

### Relation

- Identifier: `CRE-001-VOCAB-A-1.0:Relation`

- Formal definition: Within CRE-001 scope, Relation denotes an explicit connection, ordering, dependency, constraint, permission, prohibition, or status association among objects. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: explicit typed connection among Objects

- Permitted commitments: explicit typed connection among Objects; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: relation identity is by relation identifier, endpoints, role, and scope

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Relation used with recorded role in CRE-001 mapping

- Non-examples: Relation used to import an unrecorded domain rule or universal conclusion

### Transformation

- Identifier: `CRE-001-VOCAB-A-1.0:Transformation`

- Formal definition: Within CRE-001 scope, Transformation denotes an explicit change, update, transition, rule application, or state modification applied to objects and relations. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: explicit operation on Objects/Relations

- Permitted commitments: explicit operation on Objects/Relations; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: transformation identity is by transition/update identifier, guard/effect content, and scope

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Transformation used with recorded role in CRE-001 mapping

- Non-examples: Transformation used to import an unrecorded domain rule or universal conclusion

## CRE-001-VOCAB-B-1.0

### State

- Identifier: `CRE-001-VOCAB-B-1.0:State`

- Formal definition: Within CRE-001 scope, State denotes a complete or partial assignment of values, statuses, records, or conditions at a discrete point in the system history. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: discrete configuration snapshot

- Permitted commitments: discrete configuration snapshot; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: state identity is by assignment/status/history-point content within declared scope

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: State used with recorded role in CRE-001 mapping

- Non-examples: State used to import an unrecorded domain rule or universal conclusion

### Transition

- Identifier: `CRE-001-VOCAB-B-1.0:Transition`

- Formal definition: Within CRE-001 scope, Transition denotes an explicit movement from one state to another, including any update, rule application, status change, or history extension. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: movement/update between States

- Permitted commitments: movement/update between States; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: transition identity is by source condition, target/effect, rule role, and history extension

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Transition used with recorded role in CRE-001 mapping

- Non-examples: Transition used to import an unrecorded domain rule or universal conclusion

### Label

- Identifier: `CRE-001-VOCAB-B-1.0:Label`

- Formal definition: Within CRE-001 scope, Label denotes a name, marker, tag, status, condition marker, or identifier attached to a state, transition, or recorded item. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: attached marker or identifier

- Permitted commitments: attached marker or identifier; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: label identity is by label token, attachment target, and label role

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Label used with recorded role in CRE-001 mapping

- Non-examples: Label used to import an unrecorded domain rule or universal conclusion

## CRE-001-VOCAB-C-1.0

### Representation

- Identifier: `CRE-001-VOCAB-C-1.0:Representation`

- Formal definition: Within CRE-001 scope, Representation denotes an explicit represented item, proposition, rule, state element, transition record, or output record. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: explicit represented item

- Permitted commitments: explicit represented item; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: representation identity is by represented content, role, and identifier

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Representation used with recorded role in CRE-001 mapping

- Non-examples: Representation used to import an unrecorded domain rule or universal conclusion

### Representational Structure

- Identifier: `CRE-001-VOCAB-C-1.0:Representational_Structure`

- Formal definition: Within CRE-001 scope, Representational Structure denotes explicit structure over representations, including ordering, dependency, rule-status structure, transition structure, admissibility structure, or history structure. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: explicit organization over representations

- Permitted commitments: explicit organization over representations; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: structure identity is by participating representations, relation type, and constraints

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Representational Structure used with recorded role in CRE-001 mapping

- Non-examples: Representational Structure used to import an unrecorded domain rule or universal conclusion

### Interpretation

- Identifier: `CRE-001-VOCAB-C-1.0:Interpretation`

- Formal definition: Within CRE-001 scope, Interpretation denotes the policy or assignment that gives represented items their scenario meaning, truth condition, status meaning, or output meaning. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: meaning/status/truth/output policy

- Permitted commitments: meaning/status/truth/output policy; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: interpretation identity is by policy assignment and target representation

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Interpretation used with recorded role in CRE-001 mapping

- Non-examples: Interpretation used to import an unrecorded domain rule or universal conclusion

### Investigation

- Identifier: `CRE-001-VOCAB-C-1.0:Investigation`

- Formal definition: Within CRE-001 scope, Investigation denotes the bounded task or question that fixes what must be represented and preserved for the mapping. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: bounded preservation task

- Permitted commitments: bounded preservation task; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: investigation identity is by objective, scope, and success criteria

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Investigation used with recorded role in CRE-001 mapping

- Non-examples: Investigation used to import an unrecorded domain rule or universal conclusion

### Calculus

- Identifier: `CRE-001-VOCAB-C-1.0:Calculus`

- Formal definition: Within CRE-001 scope, Calculus denotes the explicit rule-governed procedure, transition policy, admissibility standard, update rule, or stopping rule used to move between states or judge transitions. It licenses only explicit, finitely identified uses satisfying its source definition and recorded role.

- Operational meaning: rule-governed transition/judgment procedure

- Permitted commitments: rule-governed transition/judgment procedure; explicit CRE-001-scoped representation when provenance and role are recorded

- Forbidden commitments: unstated domain rules; unbounded semantics; proof of universal sufficiency; proof of primitive-only sufficiency; necessity/minimality/independence/superiority claims; universal reasoning structure claims; formal vocabulary licensing for CRE-001; primitive sufficiency claims

- Required properties: explicit identifier; declared role; CRE-001 scope; traceable source; no scenario alteration

- Optional properties: human-readable label; provenance note; link to derived construct when used

- Closure conditions: closed under finite CRE-001-scoped composition when every component remains explicit and no forbidden commitment is introduced

- Identity conditions: calculus identity is by rule set, admissibility policy, update behavior, and stopping condition

- Equivalence conditions: equivalent only when identifier, role, scope, operational contribution, and licensed commitments match

- Interaction rules: may interact with other primitives only through explicit derived machinery or recorded mapping relations; does not silently import another vocabulary primitive

- Limitations: formalized after deterministic CRE-001; prospective for CRE-002 and later only; does not retroactively validate CRE-001 or license stronger project-level conclusions

- Examples: Calculus used with recorded role in CRE-001 mapping

- Non-examples: Calculus used to import an unrecorded domain rule or universal conclusion
