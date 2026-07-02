# Foundational Discovery Protocol

## Status

Canonical Methodology

## Purpose

This protocol governs work that attempts to ground Project FAR from first principles.

It is designed to prevent framework-first reasoning.

It requires foundational concepts to be discovered, tested, reduced, and justified before they are used to support FAR, FARA, FARO, or any other framework component.

## Scope

This protocol applies to investigations whose objective is to identify necessities, primitives, axioms, definitions, or framework components underlying explicit reasoning.

It does not by itself establish any necessity, primitive, axiom, theorem, or framework component.

## Core Rule

Do not begin from FAR, FARA, FARO, representation, state, transition, candidate, admissibility, or resolution.

Begin from the weakest possible conditions under which explicit reasoning might exist.

Framework architecture may be derived only after the underlying necessities have been independently justified.

## Research Direction

The direction of discovery is:

```text
phenomenon
  ↓
necessity candidates
  ↓
reduction attempts
  ↓
primitive candidates
  ↓
definitions
  ↓
lemmas
  ↓
theorems
  ↓
derived architecture
  ↓
framework components
```

The reverse direction is prohibited for grounding work.

A framework component may not be used as evidence for the necessity of the structure it was designed to contain.

## Candidate Lifecycle

Every foundational candidate shall proceed through the following lifecycle:

1. observation;
2. question;
3. candidate statement;
4. independent definition of terms;
5. scope statement;
6. assumptions;
7. category classification;
8. removal test;
9. reduction test;
10. independence test;
11. replacement test;
12. counterexample search;
13. minimal-model test;
14. alternative-model test;
15. proof attempt;
16. proof audit;
17. failure characterization;
18. revision;
19. promotion, rejection, or open classification.

No foundational candidate may be promoted before completing the applicable tests.

## Required Tests

### Definition Test

Every term in the candidate statement shall be defined without assuming the candidate being tested.

### Category Test

Classify the candidate as one of:

- entity;
- property;
- relation;
- operation;
- process;
- rule;
- condition;
- meta-concept.

Category errors shall be treated as defects.

### Scope Test

State exactly what the candidate applies to and what it excludes.

No result may be stated more broadly than its scope permits.

### Removal Test

Remove the candidate completely.

If explicit reasoning remains possible within the stated scope, the candidate is not necessary.

### Reduction Test

Attempt to derive the candidate from weaker conditions.

If derivation succeeds, the candidate is not primitive.

### Independence Test

Attempt to derive the candidate from other accepted candidates.

If derivation succeeds, the candidate is dependent.

### Replacement Test

Attempt to replace the candidate with a different structure performing the same role.

If replacement succeeds without loss, the candidate is not uniquely justified.

### Minimal-Model Test

Construct the weakest model satisfying accepted requirements.

If the candidate is absent and explicit reasoning remains possible, the candidate is rejected or revised.

### Alternative-Model Test

Construct competing models of explicit reasoning.

If a competing model explains the same phenomena with fewer assumptions, the candidate framework is not minimal.

### Counterexample Test

Search for explicit reasoning cases that violate the candidate.

A successful counterexample requires revision, restriction, or rejection.

### Proof Audit

Every inference in a proof attempt shall be justified by a definition, assumption, prior result, construction, or explicitly stated rule.

### Failure Characterization

Failed proofs and rejected candidates shall record the failure type, such as:

- invalid inference;
- ambiguous definition;
- hidden assumption;
- overbroad scope;
- circularity;
- successful counterexample;
- insufficient model;
- category error.

## Canonization Rule

A foundational candidate may become canonical only if it has:

- precise definitions;
- explicit scope;
- explicit assumptions;
- completed applicable tests;
- no surviving decisive counterexample;
- a justification chain;
- a recorded dependency graph;
- an explicit statement of what would revise or falsify it.

Usefulness is not sufficient for canonization.

Familiarity is not sufficient for canonization.

Prior inclusion in the project is not sufficient for canonization.

## Grounding Rule

A framework component is grounded only if it is derived from accepted necessities, accepted primitives, accepted definitions, or accepted theorems.

A framework component is not grounded merely because it is documented, useful, coherent, or already present in the repository.

## Self-Test Requirement

This protocol must be tested against actual Project FAR investigations.

If it fails to guide discovery, produces circular results, blocks legitimate reasoning, or fails to expose important defects, it must be revised.

## Starting Point

The first grounding investigation shall not ask whether FARA is necessary.

It shall ask:

> What is the weakest possible structure under which explicit reasoning can exist?

Only after that question has been investigated may the project ask whether FAR, FARA, or FARO emerge from the result.
