# FARA Architecture

## Purpose

This document provides the architectural overview of the Foundational Architecture of Reasoning Analysis (FARA).

FARA specifies the conceptual architecture used by Project FAR to represent structured, explicit, auditable reasoning.

The canonical definitions of all formal terminology are maintained in:

`theory/definitions/definitions.md`

This document is an orientation layer. It does not introduce independent definitions.

---

## Architectural Objective

FARA implements Project FAR's selected finite explicit auditable representation target. It does not claim that the target is a common native architecture or a basis of global primitives.

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
- `formal-kernel.md` — accepted formal carrier architecture within the registered v1.0 scope;
- `primitives.md` — schema/contract role registry retained at its historical path;
- `ontology.md` — conceptual organization of schema roles and derived concepts;
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

### 2. Schema Role Registry Layer

The role registry identifies the named fields used by the selected Project FAR v1 schema.

Primary artifact:

`primitives.md`

These fields are schema or contract roles, not global primitives. Their engineering use does not establish an invariant basis.

---

### 3. Ontology Layer

The ontology organizes schema roles and derived or optional representational concepts.

Primary artifact:

`ontology.md`

The ontology must remain synchronized with the schema-role registry.

---

### 4. Formal-Kernel Layer

The formal-kernel layer specifies the admitted identity-bearing many-sorted relational carrier architecture for Project FAR v1.0 finite explicit auditable representations.

Primary artifact:

`formal-kernel.md`

`FARA-FORMAL-KERNEL-001` is Accepted only at that scope. The kernel does not establish global primitive status, uniqueness, universality, minimality, necessity, or completeness.

---

### 5. Representational Layer

The representational layer distinguishes representations, represented objects, representational structures, interpretation, and semantic content.

Primary artifacts:

- `theory/definitions/definitions.md`
- `semantics.md`
- `formal-kernel.md`

---

### 6. Reasoning-State Layer

The reasoning-state layer describes the state of an investigation at stages of a reasoning process.

Primary artifact:

`reasoning-states.md`

This layer separates reasoning states from reasoning state representations and records.

---

### 7. Transition Layer

The transition layer records transformation executions between reasoning state representations.

Primary artifacts:

- `transition-signatures.md`
- `formal-kernel.md`

This layer separates transformation rules, executions, results, and transition signatures. The formal kernel represents executions as identity-bearing Events and requires explicit provenance and acyclic order.

---

### 8. Admissibility and Resolution Layer

The admissibility layer records classifications of candidates under a reasoning calculus.

Primary artifact:

`admissibility-structure.md`

This layer separates admissibility, admissibility classification, Ω, resolution rules, resolution executions, and resolutions.

---

## Concept Flow

The core conceptual flow is:

```text
Definitions
  -> Schema Roles
  -> Ontology
  -> Formal Kernel
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

## Accepted Formal Kernel

`FARA-FORMAL-KERNEL-001` promotes an identity-bearing many-sorted relational structure as the canonical formal kernel within Project FAR v1.0 finite explicit auditable representational architecture.

The kernel is accepted because it preserves the mandatory category separations, remains calculus-independent, separates architecture from operation, preserves parallel occurrence identity, and requires explicit provenance and event order. A separate clean-room implementation reproduced the source classifications and failed-gate sets.

Typed-hypergraph and algebraic/state-transition forms remain optional derived views. Pure extensional relational projection is insufficient as the canonical kernel where parallel occurrence identity matters.

The accepted kernel retains the role registry and does not settle broader nonfinite, oracle-dependent, embodied, full-signature, unbounded, or externally administered cases.

---

## Relationship to FARO

FARA specifies what the reasoning architecture contains.

FARO should specify operations performed over that architecture.

In short:

```text
FARA: what exists architecturally
FARO: what happens operationally
```

The formal kernel preserves this boundary by not making operation composition primitive.

This boundary should remain explicit during future development.

---

## Current Status

FARA is stabilized as a v1.0 architectural baseline.

Stabilization means that the current documents are internally synchronized and suitable for downstream work.

The scoped formal-kernel selection is Accepted under `FARA-FORMAL-KERNEL-001`.

It does not mean that global minimality, universality, primitive irreducibility, completeness, or unique foundation status have been proven.

Those remain domain-specific engineering and application questions; the contract-free global primitive/minimality branch is closed.

## Terminal theory interpretation

FARA is a candidate representation \(\rho:X\to R\). Its adequacy is never inferred from encodability alone. FAR must freeze the contract, prove a decoder/factorization or find a collision, and state whether FARA intentionally retains audit distinctions beyond the observational quotient.
