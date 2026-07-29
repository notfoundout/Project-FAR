# Candidate Primitives

## Purpose

This document records the concepts currently treated as candidate primitives within the Foundational Architecture of Reasoning Analysis (FARA).

A candidate primitive is a concept that has not yet been successfully reduced to simpler concepts within the current framework. Candidate status remains provisional and does not establish global irreducibility, necessity, independence, or minimality.

Canonical definitions remain in:

`theory/definitions/definitions.md`

The scoped formal status used here is established by:

`docs/research/fara-canonical-kernel-v1.0.md`

---

## Primitive Policy

A concept belongs in this registry only when:

- no complete scoped reduction has been established;
- no simpler definition preserves the required expressive commitments within the active scope;
- any claimed reduction or independence result identifies its model class, equivalence relation, and objective.

Formal support sorts used by an implementation are not automatically conceptual primitives.

---

## Current Candidate Primitives

The current Project FAR v1.0 candidate primitive concepts are:

- Object
- Relation
- Representation
- Interpretation
- Reasoning Calculus

These form the current unreduced conceptual basis used by the canonical identity-bearing many-sorted relational kernel.

No claim is made that all five are globally necessary, mutually independent, permanently fundamental, or minimal outside the declared Project FAR v1.0 scope.

---

## Scoped Reductions Established by the Canonical Kernel

The following concepts are no longer listed as candidate primitives for Project FAR v1.0:

- **Property** — derived as a unary relation occurrence.
- **Investigation** — derived as an explicitly identified context whose content is the tuple of objective, conditions, and reasoning-calculus reference.

The kernel also derives:

- Semantic Content from Interpretation applied to Representation;
- Transformation Execution from an identity-bearing Event applying a Rule;
- Transformation Result from the Event's output State;
- Transition Signature from a Representation of an Event;
- Reasoning Trace from an ordered collection of Events.

These are scoped formal reductions. They do not prove that the same reductions are globally mandatory in every possible ontology or reasoning architecture.

---

## Formal Support Categories

The canonical kernel uses additional typed carriers such as Meaning, Rule, State, Event, Objective, Condition, Relation Type, Relation Occurrence, Role, and Provenance.

Their presence in the formal signature records identity, typing, auditability, and reconstruction obligations. It does not by itself classify each support category as a conceptual primitive.

---

## Derived Architectural Concepts

Derived concepts include, but are not limited to:

### Structural

- Property
- Structure
- Component
- System
- Class
- Domain

### Representational

- Representational Structure
- Representation Mapping
- Representation Transformation
- Representation Fidelity
- Representation Completeness
- Representation Consistency
- Representation Invariance
- Semantic Content

### Reasoning and transition

- Investigation
- Reasoning Process
- Reasoning State
- Reasoning State Representation
- Reasoning State Record
- Transformation Rule
- Transformation Execution
- Transformation Result
- Transition Signature
- Reasoning Trace

### Decision

- Candidate
- Criterion
- Admissibility
- Admissibility Classification
- Admissibility Structure (Ω)
- Resolution Rule
- Resolution Execution
- Resolution

---

## Research Objectives

Remaining primitive research includes:

- reducing the five retained candidate concepts where possible;
- establishing scoped independence only under explicit formal contracts;
- testing whether identity-bearing relation occurrences suffice in untested domains;
- determining whether additional concepts are required for nonfinite, embodied, distributed, or oracle-dependent systems;
- distinguishing conceptual primitives from implementation support sorts.

---

## Version Status

This registry is canonical for Project FAR v1.0 repository usage. It remains revisable through explicit grounding investigations, proofs, counterexamples, or validated representational failures.
