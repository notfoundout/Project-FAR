# FARA Architecture

## Purpose

This document provides the architectural overview of the Foundational Architecture of Reasoning Analysis (FARA).

FARA specifies the conceptual architecture used by Project FAR to represent structured, explicit, auditable reasoning.

The canonical definitions of all formal terminology are maintained in:

`theory/definitions/definitions.md`

This document is an orientation layer. It does not introduce independent definitions.

---

## Architectural Objective

FARA seeks to determine whether structured reasoning can be represented by a common architecture composed of candidate primitives and derived concepts.

The architecture is designed to support:

- explicit representation;
- auditability;
- reasoning-state tracking;
- transition documentation;
- admissibility classification;
- resolution selection;
- future formalization and proof.

FARA does not prescribe how reasoning must be performed.

It specifies how reasoning may be represented and analyzed.

---

## Core Documents

The core FARA documents are:

- `architecture.md` — architectural overview and document relationships;
- `primitives.md` — current candidate primitive registry;
- `ontology.md` — conceptual organization of candidate primitives and derived concepts;
- `semantics.md` — relationship between representation, interpretation, and meaning;
- `reasoning-states.md` — architectural role of reasoning states;
- `transition-signatures.md` — architectural role of transition signatures;
- `admissibility-structure.md` — architectural role of the Admissibility Structure (Ω).

Supporting navigation and maintenance documents:

- `document-map.md` — location of canonical concept discussions;
- `dependency-graph.md` — dependency order among FARA concepts and documents;
- `design-principles.md` — centralized architectural principles.

---

## Architectural Layers

FARA is organized into the following layers.

### 1. Canonical Definitions Layer

The definitions layer establishes repository-wide terminology.

Primary artifact:

`theory/definitions/definitions.md`

All FARA documents depend on this layer.

---

### 2. Primitive Registry Layer

The primitive registry identifies concepts currently treated as candidate primitives.

Primary artifact:

`primitives.md`

Candidate primitive status is provisional and remains subject to reduction.

---

### 3. Ontology Layer

The ontology organizes concepts into candidate primitive and derived categories.

Primary artifact:

`ontology.md`

The ontology must remain synchronized with the primitive registry.

---

### 4. Representational Layer

The representational layer distinguishes representations, represented objects, representational structures, interpretation, and semantic content.

Primary artifacts:

- `theory/definitions/definitions.md`
- `semantics.md`

---

### 5. Reasoning-State Layer

The reasoning-state layer describes the state of an investigation at stages of a reasoning process.

Primary artifact:

`reasoning-states.md`

This layer separates reasoning states from reasoning state representations and records.

---

### 6. Transition Layer

The transition layer records transformation executions between reasoning state representations.

Primary artifact:

`transition-signatures.md`

This layer separates transformation rules, executions, results, and transition signatures.

---

### 7. Admissibility and Resolution Layer

The admissibility layer records classifications of candidates under a reasoning calculus.

Primary artifact:

`admissibility-structure.md`

This layer separates admissibility, admissibility classification, Ω, resolution rules, resolution executions, and resolutions.

---

## Concept Flow

The core conceptual flow is:

```text
Definitions
  -> Candidate Primitives
  -> Ontology
  -> Representational Structure
  -> Reasoning State Representation
  -> Transition Signature
  -> Reasoning Trace
  -> Admissibility Structure (Ω)
  -> Resolution
```

This flow is architectural, not temporal. A reasoning process may revisit or revise earlier representations.

---

## Required Category Separations

FARA depends on the following distinctions:

- object is distinct from representation;
- represented object is distinct from representation;
- reasoning state is distinct from reasoning state representation;
- reasoning state representation is distinct from reasoning state record;
- transformation rule is distinct from transformation execution;
- transformation execution is distinct from transformation result;
- transition signature is distinct from transformation execution;
- admissibility is distinct from admissibility classification;
- admissibility classification is distinct from Ω;
- resolution rule is distinct from resolution execution;
- resolution execution is distinct from resolution.

These distinctions are mandatory architectural constraints, not stylistic preferences.

---

## Relationship to FARO

FARA specifies what the reasoning architecture contains.

FARO should specify operations performed over that architecture.

In short:

```text
FARA: what exists architecturally
FARO: what happens operationally
```

This boundary should remain explicit during future development.

---

## Current Status

FARA is stabilized as a v1.0 architectural baseline.

Stabilization means that the current documents are internally synchronized and suitable for downstream work.

It does not mean that minimality, universality, or irreducibility have been proven.

Those remain active research questions.