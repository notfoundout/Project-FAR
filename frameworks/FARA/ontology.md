# Ontology

## Purpose

This document specifies the current conceptual organization of FARA and distinguishes candidate primitive concepts from derived concepts.

Canonical terminology remains in:

`theory/definitions/definitions.md`

The canonical formal foundation is specified and validated by:

`theory/formal/fara-canonical-kernel-v1.0.json`

`docs/research/fara-canonical-kernel-v1.0.md`

---

## Ontological Organization

FARA distinguishes:

- candidate primitive concepts;
- derived concepts;
- formal support categories used to make identity, typing, provenance, and execution explicit.

These categories must not be conflated. A carrier or relation appearing in the formal kernel is not automatically a conceptual primitive.

---

## Candidate Primitive Concepts

The current Project FAR v1.0 candidate primitive concepts are:

- Object
- Relation
- Representation
- Interpretation
- Reasoning Calculus

Candidate status is provisional. The canonical-kernel decision establishes repository authority and a scoped formal basis, not global irreducibility or universal minimality.

---

## Derived Concepts

### Property

Property is derived as a unary relation occurrence: a Relation Type instantiated by an identity-bearing Relation Occurrence with one participant role.

### Investigation

Investigation content is derived from an objective, applicable conditions, and a Reasoning Calculus reference. An investigation record may carry its own identity for traceability without making Investigation a primitive conceptual category.

### Semantic Content

Semantic Content is derived from the application of an Interpretation to a Representation.

### Execution and Result

A Transformation Execution is represented by an identity-bearing Event applying a Rule within an Investigation. A Transformation Result is the Event's output State.

### Transition and trace

A Transition Signature is a Representation of an Event. A Reasoning Trace is an ordered collection of Events represented by explicit precedence relations.

Additional derived concepts include the structural, representational, decision, evidence, and formal concepts listed in `primitives.md` and defined in the canonical definitions.

---

## Formal Support Categories

The canonical kernel provides typed identity-bearing support for:

- Meaning;
- Rule;
- State;
- Event;
- Investigation record;
- Objective;
- Condition;
- Relation Type;
- Relation Occurrence;
- Role;
- Provenance.

These support categories make mandatory FARA separations executable:

- object / representation;
- structure / interpretation;
- rule / execution / result;
- investigation context / reasoning process;
- relation type / relation occurrence;
- event identity / event order / event provenance.

---

## Canonical Formal Foundation

The canonical Project FAR v1.0 foundation is an identity-bearing many-sorted relational kernel.

Typed-hypergraph and algebraic/state-transition structures are admissible derived views when translations, sidecars, and reconstruction obligations are explicit. They are not coequal canonical foundations.

The earlier frozen comparison among extensional relational, typed-hypergraph, and algebraic/state-transition candidates remains historical Research evidence. Its Pareto result is not overwritten.

---

## Reduction Principle

Whenever a concept can be completely defined in terms of simpler concepts without loss of required expressive commitments relative to the active scope and objective, it must be treated as derived.

A valid reduction must identify:

- the source and target vocabularies;
- the model class;
- the equivalence or preservation relation;
- the reconstruction procedure;
- any external machinery or sidecar;
- the exact scope of the conclusion.

---

## Research Status

Unresolved questions include:

- whether the five retained candidate concepts can be reduced further;
- whether the kernel survives independent implementation and external benchmark corpora;
- whether nonfinite continuous, embodied, distributed, or live-oracle systems require material extensions;
- whether the formal support categories can be reduced without losing identity, provenance, or auditability.

---

## Version Status

This ontology is canonical for Project FAR v1.0 repository usage and remains subject to evidence-driven revision.
