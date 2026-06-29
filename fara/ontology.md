# Ontology

## Purpose

This document defines the ontology of the Foundational Architecture of Reasoning Analysis (FARA).

The ontology specifies the classes of objects assumed to exist within the architecture.

It does not define the meaning, behavior, or admissibility of those objects.

---

## Definition

Within FARA, the ontology consists of the objects required to represent structured, explicit, auditable reasoning.

The canonical definitions of these objects are maintained in:

`theory/definitions.md`

---

## Objective

The objective of the ontology is to identify the objects required by the architecture while minimizing unnecessary ontological commitments.

Only objects required for representation should be included.

---

## Fundamental Objects

The current architecture recognizes the following fundamental objects.

- Representation
- Representational Structure
- Interpretation
- Investigation
- Reasoning Calculus

These objects serve as the architectural foundation of FARA.

---

## Derived Objects

The following objects are currently regarded as derived from the fundamental objects.

- Reasoning State
- Transition Signature
- Candidate
- Admissibility Structure (Ω)
- Resolution

Derived objects are defined in terms of the fundamental objects and their relationships.

---

## Ontological Neutrality

The ontology is independent of:

- any particular reasoning calculus,
- any application domain,
- any implementation,
- and any specific reasoning methodology.

It specifies only the objects required by the architecture.

---

## Relationships

The ontology identifies the existence of architectural objects.

The relationships among those objects are defined elsewhere within FARA.

Semantics assigns meaning to representations.

Reasoning states organize representations.

Transition signatures represent transformations.

The Admissibility Structure (Ω) classifies candidates.

---

## Research Status

The ontology remains provisional.

Current research investigates:

- ontological reduction,
- independence of candidate primitives,
- minimal ontological commitments,
- and alternative architectural formulations.
