# Ontology

## Purpose

This document defines the ontology of FARA.

The ontology specifies the classes of entities assumed to exist within the architecture.

It does not define their semantics or behavior.

---

## Ontological Commitment

FARA is committed only to entities required for the representation of structured, explicit, auditable reasoning.

No additional entities should be introduced without demonstrating their necessity.

---

## Fundamental Entities

The current ontology includes the following categories of entities.

- Representations
- Representational Structures
- Interpretations
- Investigations
- Reasoning Calculi

These constitute the candidate primitive entities of the architecture.

Formal definitions are maintained in:

`theory/definitions.md`

---

## Derived Entities

The following entities are currently regarded as derived.

- Reasoning States
- Transition Signatures
- Possibility Spaces
- Ω (Admissibility Structures)
- Resolutions

Their existence depends upon relationships among the primitive entities.

---

## Ontological Neutrality

The ontology is independent of any particular reasoning calculus or application domain.

It specifies only the entities required by the architecture, not the rules governing their use.

---

## Research Status

The ontology remains provisional.

Future work may eliminate, refine, or introduce ontological commitments if required by formal analysis or validation.

The long-term objective is to identify the minimal ontology sufficient to support the architecture.
