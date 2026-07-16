# CRE-001 Expressivity Audit


## Status Vocabulary

- **Supported**: established for frozen CRE-001 vocabulary-semantics scope by explicit source definitions and this specification.
- **Unsupported**: not established and not licensed by this specification.
- **Unknown**: not determined by available repository evidence.
- **Assumed**: required CRE-001-scoped assumption recorded explicitly.
- **Implementation-specific**: property of the deterministic compiler/verifier artifacts, not primitive semantics.


## CRE-001-VOCAB-A-1.0

### Primitive Definitions

- object individuation

- relations may express ordering/dependency/constraint/permission/prohibition/status association

- transformations may express transition/update/rule application/state modification

### Derived Constructs

- boolean/status values

- ordered history

- guarded update records

- bounded disjunction

- terminal blocking policy

### Compiler Interpretation

- Object as value/status/rule/history carrier

- Relation as precondition/status/order/prohibition/output/invariant/ambiguity carrier

- Transformation as transition schema and update carrier

### Lowering Rules

- atomic variables, guards, updates, terminal condition, outputs, invariants, ambiguity policies

### Implementation Assumptions

- finite identifier set

- boolean truth/status carrier

- append-only ordered history

- registered ambiguity policies

## CRE-001-VOCAB-B-1.0

### Primitive Definitions

- state as assignment/status/record/condition at discrete history point

- transition as movement/update/status change/history extension

- label as name/marker/status/condition/identifier attached to state/transition/item

### Derived Constructs

- boolean/status labels

- history labels

- guard/update labels

- bounded disjunction labels

- terminal labels

### Compiler Interpretation

- Label carries most atomic values and conditions

- Transition carries transition schema

- State supports configuration semantics through labeled assignments

### Lowering Rules

- labels lower to variables/guards/effects/outputs when their attachment role is explicit

### Implementation Assumptions

- labels are stable identifiers

- state snapshots are finite

- transition effects are deterministic under registered policy

## CRE-001-VOCAB-C-1.0

### Primitive Definitions

- representation of propositions/rules/state elements/transition records/output records

- structure over ordering/dependency/rule-status/transition/admissibility/history

- interpretation policies for meaning/truth/status/output

- investigation scope

- calculus procedure/policy/update/stopping

### Derived Constructs

- boolean interpretations

- history structure

- calculus guard/update records

- halt disjunction

- terminal configuration

### Compiler Interpretation

- Investigation fixes CRE-001 preservation objective

- Interpretation carries truth/status/output meanings

- Calculus carries transitions, guards, updates, prohibitions and policies

- Representational Structure carries state/history/rule-status organization

- Representation carries scenario items

### Lowering Rules

- typed representations and structures lower to common execution model fields

### Implementation Assumptions

- policy assignments are explicit

- calculus is deterministic under registered ambiguity policies

- investigation scope is CRE-001 only
