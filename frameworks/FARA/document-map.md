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

Framework documents may specify architectural roles, relationships, examples, formal carrier names, or implementation implications, but canonical definitions remain centralized.

---

## Core FARA Documents

| Document | Role |
|---|---|
| `architecture.md` | Architectural overview and layer organization |
| `formal-kernel.md` | Accepted identity-bearing many-sorted relational formal kernel within the registered v1.0 scope |
| `primitives.md` | Current FARA schema-role registry (historical path) |
| `ontology.md` | Conceptual organization of schema roles, derived concepts, and optional views |
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
| Object | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md`, `formal-kernel.md` |
| Property | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md`, `formal-kernel.md` |
| Relation | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md`, `formal-kernel.md` |
| Representation | `theory/definitions/definitions.md` | `semantics.md`, `ontology.md`, `primitives.md`, `formal-kernel.md` |
| Represented Object | `theory/definitions/definitions.md` | `semantics.md`, `formal-kernel.md` |
| Representational Structure | `theory/definitions/definitions.md` | `semantics.md`, `ontology.md`, `formal-kernel.md` |
| Interpretation | `theory/definitions/definitions.md` | `semantics.md`, `ontology.md`, `primitives.md`, `formal-kernel.md` |
| Semantic Content | `theory/definitions/definitions.md` | `semantics.md`, `formal-kernel.md` |
| Investigation | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md`, `reasoning-states.md`, `formal-kernel.md` |
| Reasoning Calculus | `theory/definitions/definitions.md` | `ontology.md`, `primitives.md`, `formal-kernel.md` |
| Reasoning State | `theory/definitions/definitions.md` | `reasoning-states.md`, `ontology.md`, `formal-kernel.md` |
| Reasoning State Representation | `theory/definitions/definitions.md` | `reasoning-states.md`, `formal-kernel.md` |
| Reasoning State Record | `theory/definitions/definitions.md` | `reasoning-states.md` |
| Transformation Rule | `theory/definitions/definitions.md` | `transition-signatures.md`, `ontology.md`, `formal-kernel.md` |
| Transformation Execution | `theory/definitions/definitions.md` | `transition-signatures.md`, `ontology.md`, `formal-kernel.md` |
| Transformation Result | `theory/definitions/definitions.md` | `transition-signatures.md`, `formal-kernel.md` |
| Transition Signature | `theory/definitions/definitions.md` | `transition-signatures.md`, `ontology.md`, `formal-kernel.md` |
| Reasoning Trace | `theory/definitions/definitions.md` | `reasoning-states.md`, `transition-signatures.md`, `ontology.md`, `formal-kernel.md` |
| Candidate | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Admissibility | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Admissibility Classification | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Admissibility Structure (Ω) | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Resolution Rule | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Resolution Execution | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Resolution | `theory/definitions/definitions.md` | `admissibility-structure.md`, `ontology.md` |
| Formal carrier architecture | local formal symbols mapped to canonical terminology | `formal-kernel.md` |

---

## Recommended Reading Order

For a new reader, the recommended order is:

1. `architecture.md`
2. `formal-kernel.md`
3. `document-map.md`
4. `design-principles.md`
5. `primitives.md`
6. `ontology.md`
7. `semantics.md`
8. `reasoning-states.md`
9. `transition-signatures.md`
10. `admissibility-structure.md`
11. `theory/definitions/definitions.md` for canonical terminology as needed

For formal work, begin with:

1. `theory/definitions/definitions.md`
2. `primitives.md`
3. `ontology.md`
4. `formal-kernel.md`
5. `dependency-graph.md`

---

## Rules for Adding New Concepts

A new concept should not be added directly to multiple documents.

The correct order is:

1. Define the concept canonically in `theory/definitions/definitions.md`, or explicitly mark it as a local formal symbol or non-canonical exploratory term.
2. Place it in `ontology.md` as a schema role, derived concept, or optional view.
3. If it is a mandatory v1 schema role, list it in `primitives.md` with the governing contract justification.
4. Add architectural discussion in the relevant FARA document.
5. Update this document map.
6. Update `dependency-graph.md` if the concept changes dependencies.

`formal-kernel.md` may introduce scoped formal carrier names only when it maps them explicitly to canonical FARA terminology and does not silently create global primitive claims.

---

## Maintenance Policy

This document should be updated whenever:

- a new FARA document is added;
- a concept moves between schema-role, derived, or optional-view status;
- a canonical definition is added or revised;
- an architectural document changes scope;
- a new dependency relationship is introduced;
- the accepted formal kernel changes.

The document map is not a proof artifact. It is a repository maintenance artifact intended to prevent duplication, drift, and inconsistent terminology.
