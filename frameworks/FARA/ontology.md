# FARA Ontology and Schema Organization

Status: **Accepted within the finite explicit auditable Project FAR v1 engineering contract**

## Purpose

FARA organizes the concepts required by its selected representation target. The organization is a schema, not a claim that every reasoning system natively instantiates one ontology.

## Schema roles

- Object
- Property
- Relation
- Representation
- Interpretation
- Investigation
- Reasoning Calculus

Their definitions are canonical, but their former candidate-primitive status is superseded. Reification and tagging can faithfully change primitive counts; therefore no global irreducibility or minimality follows.

## Derived and optional concepts

### Structural

Structure, Component, System, Class, and Domain.

### Representational

Representational Structure, Representation Mapping, Representation Transformation, Representation Fidelity, Representation Completeness, Representation Consistency, and Representation Invariance.

### Reasoning

Reasoning Process, Reasoning State, Reasoning State Representation, Reasoning State Record, Transformation Rule, Transformation Execution, Transition Signature, and Reasoning Trace.

States, transitions, and traces are sufficient only relative to a declared behavior contract.

### Decision

Candidate, Criterion, Admissibility, Admissibility Classification, Admissibility Structure (Ω), Resolution Rule, Resolution Execution, and Resolution.

Ω is a derived materialized view; resolution is derived rule application.

### Evidence and formal concepts

Claims, evidence, observations, assumptions, hypotheses, explanations, predictions, counterexamples, models, frameworks, theories, architectures, equivalences, reductions, and expressive-power claims.

## Relationship to the role registry

The maintained role registry is [`primitives.md`](primitives.md). The path is retained for compatibility; the document no longer asserts a primitive basis.

## Change policy

A schema change requires a demonstrated requirement, explicit contract impact, preservation/loss analysis, and the Project FAR change-control lifecycle. Successful encoding is not evidence of native common structure, and schema stability is not universality.
