# FARA Dependency Graph

Terminal note: `primitives.md` is now the schema-role registry at a historical path. References below to candidate-primitive campaigns describe bounded historical investigations and do not restore current primitive status.

## Purpose

This document records the dependency structure among the core concepts and documents of the Foundational Architecture of Reasoning Analysis (FARA).

It is a maintenance artifact intended to prevent circular definitions, duplicated terminology, and architectural drift.

This document does not introduce new definitions.

---

## Document Dependency Order

The core FARA document dependency order is:

```text
theory/definitions/definitions.md
  -> frameworks/FARA/primitives.md (schema-role registry)
  -> frameworks/FARA/ontology.md
  -> frameworks/FARA/formal-kernel.md
  -> frameworks/FARA/semantics.md
  -> frameworks/FARA/reasoning-states.md
  -> frameworks/FARA/transition-signatures.md
  -> frameworks/FARA/admissibility-structure.md
```

The formal kernel consumes canonical definitions plus the schema-role and ontology classifications. It provides a scoped target architecture; it does not redefine canonical terminology or make the seven roles global primitives.

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
  -> Ontological classification
  -> Accepted formal carrier architecture
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

## Current Schema-Role Basis

Project FAR v1 uses these named schema or contract roles:

- Object
- Property
- Relation
- Representation
- Interpretation
- Investigation
- Reasoning Calculus

They are registered in `primitives.md` and organized in `ontology.md`. They are not global primitives. `FAR-CORE-007` proves that faithful reification/tagging can change primitive counts, so historical independence campaigns cannot promote the seven-field presentation into a representation-independent basis.

The completed W1 execution in `research/primitive-independence-w1-result.md` remains bounded historical evidence. Its dependency hazards are useful audit warnings, not current primitive adjudications.

`FARA-FORMAL-KERNEL-001` instantiates the seven roles within the finite explicit auditable v1 engineering contract and does not establish a native common ontology or contract-free minimality.

---

## Accepted Formal-Kernel Dependency (`FARA-FORMAL-KERNEL-001`)

The accepted formal kernel depends on:

- canonical definitions in `theory/definitions/definitions.md`;
- the seven-role v1 schema registry in `primitives.md`;
- the conceptual classifications in `ontology.md`;
- the mandatory category separations and design constraints in FARA;
- the accepted source execution `FARA-CANONICAL-KERNEL-001`;
- the clean-room implementation replication `FARA-CANONICAL-KERNEL-REPLICATION-001`;
- the Acceptance record `docs/governance/fara-formal-kernel-acceptance-v1.0.md`;
- the Promotion record `docs/governance/fara-formal-kernel-promotion-v1.0.md`.

The dependency consequence is:

```text
canonical definitions
  + schema-role/ontology classifications
  + mandatory FARA architectural gates
  + accepted and replicated evidence
    -> identity-bearing many-sorted relational formal kernel
      -> optional typed-hypergraph derived view
      -> optional algebraic/state-transition backend view
```

The kernel is canonical only for Project FAR v1.0 finite explicit auditable representational architecture. It is not a prerequisite for claims outside that scope and does not establish global uniqueness, universality, primitive necessity/minimality, completeness, nonfinite/oracle/embodied coverage, or external-investigator independence.

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

- No schema role should be called a global primitive without a new scoped contract and an invariant lower-bound theorem.
- No architectural document should redefine a term already canonically defined in `theory/definitions/definitions.md`.
- No document should collapse a rule with an execution.
- No document should collapse an object with its representation.
- No document should collapse a record with the object recorded.
- No document should collapse admissibility with Ω.
- No document should collapse resolution rules, resolution executions, and resolutions.
- No derived graph or operation view should be treated as the canonical FARA foundation without a new accepted and promoted lifecycle record.
- No use of the accepted formal kernel should omit its registered scope and nonclaims.

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

## W5 cross-representation invariance dependency (`FARA-INV-W5-001`)

W5 preserves W0–W4 and consumes only W1's unresolved boundary, W2's bounded coordinate boundary, and W4's representation-contract boundary. W3 is explicitly not consumed. Its six representation families, equivalence criterion, fixtures, and translation machinery are auxiliary research objects, not new FARA prerequisites. The registered counterexamples refute representation independence only in the frozen campaign.

---

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

## Expanded bounded executable campaign (Research)

`FARA-EXPANDED-BOUND-001` depends on the historical core-formalization and foundation-comparison specifications and executable implementations. Its additive proof object records hashes for the six historical specification/proof/report artifacts, explicit carrier bounds 0..4, exhaustive unary/binary axis costs, and regenerated trace manifests. External oracle, continuous, hybrid, and embodied semantics remain unavailable and therefore Unknown.

---

## Maintenance Policy

This dependency graph should be updated whenever:

- a schema role is added, removed, or re-scoped;
- a derived concept is added;
- a canonical definition changes;
- a concept dependency changes;
- an architectural document is added, removed, or re-scoped;
- the accepted formal kernel, its scope, or its derived-view policy changes.

Dependency updates should be justified by grounding investigations, artifact audits, accepted promotion records, or explicit architectural revisions.
