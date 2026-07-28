# FARA Dependency Graph

## Purpose

This document records the dependency structure among the core concepts and documents of the Foundational Architecture of Reasoning Analysis (FARA).

It is a maintenance artifact intended to prevent circular definitions, duplicated terminology, and architectural drift.

This document does not introduce new definitions.

---

## Document Dependency Order

The core FARA document dependency order is:

```text
theory/definitions/definitions.md
  -> frameworks/FARA/primitives.md
  -> frameworks/FARA/ontology.md
  -> frameworks/FARA/semantics.md
  -> frameworks/FARA/reasoning-states.md
  -> frameworks/FARA/transition-signatures.md
  -> frameworks/FARA/admissibility-structure.md
```

Navigation and maintenance documents depend on the whole FARA set:

```text
frameworks/FARA/architecture.md
frameworks/FARA/document-map.md
frameworks/FARA/dependency-graph.md
frameworks/FARA/design-principles.md
```

---

## Concept Dependency Flow

The core conceptual dependency flow is:

```text
Object
Property
Relation
Representation
Interpretation
Investigation
Reasoning Calculus
  -> Representational Structure
  -> Reasoning Process
  -> Reasoning State
  -> Reasoning State Representation
  -> Transformation Rule
  -> Transformation Execution
  -> Transformation Result
  -> Transition Signature
  -> Reasoning Trace
  -> Candidate
  -> Admissibility
  -> Admissibility Classification
  -> Admissibility Structure (Ω)
  -> Resolution Rule
  -> Resolution Execution
  -> Resolution
```

This flow expresses conceptual dependency, not chronological reasoning order.

---

## Candidate Primitive Basis

The current candidate primitive basis is:

- Object
- Property
- Relation
- Representation
- Interpretation
- Investigation
- Reasoning Calculus

These concepts are listed in:

`primitives.md`

and organized in:

`ontology.md`

Candidate primitive status is provisional and remains subject to grounding investigations.

The completed W1 execution in `research/primitive-independence-w1-result.md` does not establish that these nodes are mutually or jointly independent. It identifies dependency hazards
`Object <- Representation <- Object`, `Representation <-> Interpretation`, and
`Investigation <-> Reasoning Calculus`. These are audit warnings rather than derived
edges or equivalence proofs; all seven adjudications remain unresolved.

---

## Derived Concept Dependencies

### Representational Structure

Depends on:

- Representation
- Relation
- Structure

---

### Semantic Content

Depends on:

- Representation
- Interpretation

---

### Reasoning Process

Depends on:

- Investigation
- Reasoning Calculus
- Representation

---

### Reasoning State

Depends on:

- Investigation
- Reasoning Process
- State

---

### Reasoning State Representation

Depends on:

- Reasoning State
- Representation

---

### Reasoning State Record

Depends on:

- Reasoning State Representation
- Artifact

---

### Transformation Rule

Depends on:

- Representation
- Reasoning Calculus

---

### Transformation Execution

Depends on:

- Transformation Rule
- Reasoning Process

---

### Transformation Result

Depends on:

- Transformation Execution
- Representation

---

### Transition Signature

Depends on:

- Transformation Execution
- Reasoning State Representation
- Representation

---

### Reasoning Trace

Depends on:

- Transition Signature
- Reasoning Process

---

### Candidate

Depends on:

- Representation
- Investigation

---

### Admissibility

Depends on:

- Candidate
- Reasoning Calculus
- Investigation

---

### Admissibility Classification

Depends on:

- Candidate
- Admissibility
- Criterion

---

### Admissibility Structure (Ω)

Depends on:

- Candidate
- Admissibility Classification
- Investigation
- Reasoning Calculus

---

### Resolution Rule

Depends on:

- Admissibility Structure (Ω)
- Reasoning Calculus

---

### Resolution Execution

Depends on:

- Resolution Rule
- Admissibility Structure (Ω)

---

### Resolution

Depends on:

- Resolution Execution
- Candidate

---

## Dependency Constraints

The following constraints must be preserved:

- No derived concept should be listed as a candidate primitive unless reduction attempts justify reclassification.
- No architectural document should redefine a term already canonically defined in `theory/definitions/definitions.md`.
- No document should collapse a rule with an execution.
- No document should collapse an object with its representation.
- No document should collapse a record with the object recorded.
- No document should collapse admissibility with Ω.
- No document should collapse resolution rules, resolution executions, and resolutions.

---

## Bounded operator-evaluation dependency (FARA-OPS-W2-001)

The W2 evaluation depends on the canonical glossary definitions of Construct, Differentiate, and Restrict plus the explicitly noncanonical `finite_coordinate_trace_v1` model. Its bounded result is induced by the premise that each operator exclusively controls one observable coordinate under componentwise equality. The model and result are not prerequisites of FARA and do not establish canonical or global operator necessity. Resolve and Select remain outside-scope unresolved because the model contains neither declared-rule representation nor rule execution.

---

## Common-architecture evaluation dependency (FARA-ARCH-W3-001)

W3 preserves W0, the unresolved W1 independence result, and W2's coordinate-separation boundary as frozen upstream results. Its by-construction CTC result depends on `B_W3_closed_explicit`, the six-dimensional `E_W3` preservation criterion, and complete declared observables/determinants supplied in charged typed payloads. The oracle countermodel refutes only lossless universal reconstruction from explicit internal state alone. W3 is not a prerequisite of canonical FARA and establishes no native common structure, necessity, uniqueness, minimality, or open-world universality.

---

## W4 representation-boundary dependency (FARA-REP-W4-001)

The W4 execution depends only on canonical definitions, the registered six-dimensional preservation basis, W1's unresolved primitive-independence boundary, and W2's coordinate-separation-induced bounded boundary. It does not consume W3. `finite_tagged_archive_v1` is explicitly auxiliary and is not a new FARA prerequisite. Hidden interpreters, external stores, live oracles, physical environments, and infinite-precision services are outside its admissible machinery closure.

---

## Maintenance Policy

## W5 cross-representation invariance dependency (`FARA-INV-W5-001`)

W5 preserves W0–W4 and consumes only W1's unresolved boundary, W2's bounded coordinate boundary, and W4's representation-contract boundary. W3 is explicitly not consumed. Its six representation families, equivalence criterion, fixtures, and translation machinery are auxiliary research objects, not new FARA prerequisites. The registered counterexamples refute representation independence only in the frozen campaign.

---

This dependency graph should be updated whenever:

- a candidate primitive is added or removed;
- a derived concept is added;
- a canonical definition changes;
- a concept dependency changes;
- an architectural document is added, removed, or re-scoped.

Dependency updates should be justified by grounding investigations, artifact audits, or explicit architectural revisions.

## Vocabulary-pressure evaluation dependency (`FARA-VOC-001`)

This unnumbered campaign addresses `UQ-T7`; repository authority does not designate it as FARA W6. It freezes the seven provisional candidate primitives without changing them, preserves W0–W5, and uses W4/W5 cases only as registered phenomena. Its extension classifications are bounded to the auxiliary finite interpretation and establish no global primitive necessity.

## Core-formalization research dependency (`FARA-CORE-FORMAL-001`)

This descriptively named, unnumbered campaign executes two remaining `FARA-VOC-001` obligations: formal derivation/composition rules and W1 circular-definition resolution. It preserves the canonical prose and W0–W5 results. Its acyclic many-sorted signature is an auxiliary finite test target; three non-equivalent coherent foundations remain, so it is not a canonical replacement, W7, uniqueness result, or global independence result.

## Foundation-comparison research dependency (`FARA-FOUNDATION-COMP-001`)

This descriptively named, unnumbered campaign executes the selection obligation retained by `FARA-CORE-PROOF-001`, `OP-10`, and `UQ-T11`. It freezes, executes, and compares the three retained coherent foundations without changing their PR #421 definitions. Its 19-case finite corpus, translations, reconstructions, witnesses, ablations, accounting, and Pareto relation are auxiliary research evidence. Many-sorted relational dominates algebraic/state-transition under the frozen dimensions, while typed hypergraph remains Pareto-incomparable with many-sorted relational. The terminal result remains multiple foundations remain Pareto-incomparable, not W7, canonical selection, global superiority, necessity, minimality, completeness, or universality.

<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: start -->
- Mapping totals (Pass/Partial/Fail/Unknown): `{"algebraic-state-transition":{"Fail":4,"Partial":0,"Pass":12,"Unknown":3},"many-sorted-relational":{"Fail":3,"Partial":0,"Pass":13,"Unknown":3},"typed-hypergraph":{"Fail":0,"Partial":0,"Pass":16,"Unknown":3}}`
- Dominance edges: `[["many-sorted-relational","algebraic-state-transition"]]`
- Terminal result: **multiple foundations remain Pareto-incomparable**
- Nonclaims: `["canonical uniqueness","global superiority","universal representation","global minimality","primitive necessity","completeness","universality"]`
- Remaining obligations: `["independent replication","nonfinite continuous semantics","environment-inclusive embodied semantics","live-oracle semantics","neutral external benchmark corpus","complete old prose source-model class"]`
<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: end -->
