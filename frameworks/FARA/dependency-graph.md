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

## Maintenance Policy

This dependency graph should be updated whenever:

- a candidate primitive is added or removed;
- a derived concept is added;
- a canonical definition changes;
- a concept dependency changes;
- an architectural document is added, removed, or re-scoped.

Dependency updates should be justified by grounding investigations, artifact audits, or explicit architectural revisions.