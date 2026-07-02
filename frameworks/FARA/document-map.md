# FARA Document Map

## Purpose

This document maps the core documents of the Foundational Architecture of Reasoning Analysis (FARA).

It identifies where concepts are defined, where architectural roles are specified, and how contributors should locate the canonical source for each concept.

This document is a navigation artifact. It does not introduce new definitions.

---

## Canonical Definitions

All formal terminology used throughout FARA is canonically defined in:

`theory/definitions/definitions.md`

No FARA document should redefine canonical terminology independently.

Framework documents may specify architectural roles, relationships, examples, or implementation implications, but canonical definitions remain centralized.

---

## Core FARA Documents

| Document | Role |
|---|---|
| `architecture.md` | Architectural overview and layer organization |
| `primitives.md` | Current candidate primitive registry |
| `ontology.md` | Conceptual organization of candidate primitives and derived concepts |
| `semantics.md` | Representation, interpretation, and meaning relationships |
| `reasoning-states.md` | Architectural role of reasoning states |
| `transition-signatures.md` | Architectural role of transition signatures |
| `admissibility-structure.md` | Architectural role of the Admissibility Structure (Ω) |
| `document-map.md` | Navigation map for FARA documents |
| `dependency-graph.md` | Dependency order among FARA concepts and documents |
| `design-principles.md` | Centralized architectural principles |

---

## Concept Locations

| Concept | Canonical Definition | Architectural Discussion |
|---|---|---|
| Object | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md` |
| Property | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md` |
| Relation | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md` |
| Representation | `theory/definitions/definitions.md` | `semantics.md`, `ontology.md`, `primitives.md` |
| Represented Object | `theory/definitions/definitions.md` | `semantics.md` |
| Representational Structure | `theory/definitions/definitions.md` | `semantics.md`, `ontology.md` |
| Interpretation | `theory/definitions/definitions.md` | `semantics.md`, `ontology.md`, `primitives.md` |
| Semantic Content | `theory/definitions/definitions.md` | `semantics.md` |
| Investigation | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md`, `reasoning-states.md` |
| Reasoning Calculus | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md` |
| Reasoning State | `theory/definitions/definitions.md` | `reasoning-states.md`, `ontology.md` |
| Reasoning State Representation | `theory/definitions/definitions.md` | `reasoning-states.md` |
| Reasoning State Record | `theory/definitions/definitions.md` | `reasoning-states.md` |
| Transformation Rule | `theory/definitions/definitions.md` | `transition-signatures.md`, `ontology.md` |
| Transformation Execution | `theory/definitions/definitions.md` | `transition-signatures.md`, `ontology.md` |
| Transformation Result | `theory/definitions/definitions.md` | `transition-signatures.md` |
| Transition Signature | `theory/definitions/definitions.md` | `transition-signatures.md`, `ontology.md` |
| Reasoning Trace | `theory/definitions/definitions.md` | `reasoning-states.md`, `transition-signatures.md`, `ontology.md` |
| Candidate | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Admissibility | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Admissibility Classification | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Admissibility Structure (Ω) | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Resolution Rule | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Resolution Execution | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Resolution | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |

---

## Recommended Reading Order

For a new reader, the recommended order is:

1. `architecture.md`
2. `document-map.md`
3. `design-principles.md`
4. `primitives.md`
5. `ontology.md`
6. `semantics.md`
7. `reasoning-states.md`
8. `transition-signatures.md`
9. `admissibility-structure.md`
10. `theory/definitions/definitions.md` for canonical terminology as needed

For formal work, begin with:

1. `theory/definitions/definitions.md`
2. `primitives.md`
3. `ontology.md`
4. `dependency-graph.md`

---

## Rules for Adding New Concepts

A new concept should not be added directly to multiple documents.

The correct order is:

1. Define the concept canonically in `theory/definitions/definitions.md`, or explicitly mark it as non-canonical if it is only exploratory.
2. Place it in `ontology.md` as either candidate primitive or derived.
3. If it is a candidate primitive, list it in `primitives.md` with justification.
4. Add architectural discussion in the relevant FARA document.
5. Update this document map.
6. Update `dependency-graph.md` if the concept changes dependencies.

---

## Maintenance Policy

This document should be updated whenever:

- a new FARA document is added;
- a concept moves between primitive and derived status;
- a canonical definition is added or revised;
- an architectural document changes scope;
- a new dependency relationship is introduced.

The document map is not a proof artifact. It is a repository maintenance artifact intended to prevent duplication, drift, and inconsistent terminology.