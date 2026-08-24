# FARA Schema Roles

Historical path: `frameworks/FARA/primitives.md`

Status: **Accepted role registry; former candidate-primitive classification superseded**

## Purpose

This document records the seven named schema roles used by Project FAR's finite explicit auditable v1 representation schema. Under `PROJECT-FAR-CORE-THEORY-1.0`, they are **not global primitives** and their count is not representation invariant.

Canonical definitions remain in `theory/definitions/definitions.md`.

## Current schema and contract roles

| Role | Terminal classification |
|---|---|
| Object | schema role for distinguishable items |
| Property | schema role; representable as a unary relation in the accepted kernel |
| Relation | schema role; reifiable, splittable, or combinable under faithful presentations |
| Representation | comparison-contract and schema role |
| Interpretation | consequence-affecting contract parameter |
| Investigation | scope/provenance aggregate and schema role |
| Reasoning Calculus | consequence-determining parameter when it changes behavior or classifications |

These roles are mandatory fields only where the Project FAR v1 engineering contract requires them. A target need not natively contain the same ontology.

## Derived architectural concepts

The following remain derived or optional views:

- representational structures, mappings, transformations, fidelity, completeness, consistency, and invariance;
- reasoning processes, states, state records, transformations, transition signatures, and traces;
- candidates, criteria, admissibility classifications, Ω, resolution rules, executions, and resolutions;
- claims, evidence, observations, assumptions, hypotheses, explanations, predictions, and counterexamples;
- models, frameworks, theories, architectures, equivalences, reductions, and expressive-power claims.

Ω is a derived materialized classification/provenance view. Resolve is derived rule application.

## Reduction and equivalence policy

Primitive-count arguments must first freeze the admitted vocabulary, reification/tagging rules, definability, equivalence, and cost order. Without that contract, reification, tagging, splitting, and combination change the number and names of primitives without information loss.

No future document may promote these seven roles to a universal or irreducible basis merely because the canonical FARA schema uses separate carriers.

## Research boundary

Domain-specific necessity or implementation-cost claims may be studied under an explicit contract. The global primitive-independence and primitive-minimality search is closed by `FAR-CORE-007`; it is not an open FARA objective.
