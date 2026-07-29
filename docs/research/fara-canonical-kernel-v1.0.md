# Canonical FARA Formal Kernel v1.0

Status: **Accepted for Project FAR v1.0**

Campaign: `FARA-CANONICAL-KERNEL-001`

## Decision

FARA's canonical formal foundation for Project FAR v1.0 is an **identity-bearing many-sorted relational kernel**.

Typed-hypergraph and algebraic/state-transition structures remain admissible derived views when their translations, external machinery, and reconstruction sidecars are explicit and commitment-preserving. This is a scoped architectural decision, not a claim that one formalism is the globally unique foundation of reasoning.

## Decision rule

A canonical FARA foundation must satisfy every frozen architectural gate:

1. representation/object separation;
2. rule/execution/result separation;
3. interpretation separation;
4. calculus independence;
5. architecture/operation separation;
6. identity-bearing occurrences;
7. explicit provenance and order;
8. encoding neutrality.

These gates are drawn from FARA's existing architectural and design constraints. They are treated as admissibility conditions for the canonical kernel rather than weighted comparison dimensions.

## Kernel

The executable kernel provides disjoint identity-bearing carriers for Object, Representation, Meaning, Interpretation, ReasoningCalculus, Rule, State, Event, Investigation, Objective, Condition, RelationType, RelationOccurrence, Role, and Provenance.

Its primitive relation registry records denotation, interpretation assignment, calculus/rule membership, event rule application, input and output states, investigation context, objective and conditions, identity-bearing relation occurrences, participant roles, event order, provenance, and transition-signature representation.

Property is a derived unary relation occurrence. Investigation content is derived from objective, conditions, and calculus references. SemanticContent is derived by interpretation application. A TransitionSignature is a representation of an Event. A ReasoningTrace is a derived ordered collection of Events.

## Executable evidence

The proof object builds and validates a model containing two distinct relation occurrences with identical type and participants. Pure extensional projection collapses the pair, while the canonical kernel and the typed-hypergraph derived view preserve both identities.

The typed-hypergraph translation performs an exact round trip. The algebraic/state-transition translation performs an exact round trip only with an explicit sidecar carrying nonoperational FARA commitments. Without that sidecar, source/representation separation, interpretation, investigation context, provenance, and relation-occurrence identity are not reconstructible.

## Relationship to earlier foundation comparison

`FARA-FOUNDATION-COMP-001` remains valid historical Research evidence about its three frozen candidate implementations and seventeen Pareto dimensions. Its terminal result—multiple foundations remain Pareto-incomparable—has not been rewritten.

The canonical decision is later and narrower. It applies FARA's mandatory architecture gates and an identity-bearing repair that was not one of the three frozen candidates. Therefore the earlier Pareto result and the current canonical selection are not contradictory.

## Primitive-status effect

The kernel establishes scoped formal reductions for:

- Property as a unary relation occurrence;
- Investigation content as objective, conditions, and calculus reference;
- SemanticContent as interpretation application;
- Execution as an Event applying a Rule;
- Result as the Event's output State.

This removes Property and Investigation from the current candidate-primitive registry for Project FAR v1.0. It does not establish global primitive minimality or necessity for the remaining concepts.

## Nonclaims

This decision does not establish:

- a globally unique foundation of reasoning;
- universal representation of every reasoning system;
- global primitive necessity;
- global minimality;
- completeness;
- nonfinite continuous semantics;
- live-oracle semantics;
- embodied environment semantics;
- independent replication.

## Validation

The checker rebuilds the proof object, validates every typed relation, rejects cross-sort identity collapse, rejects forged or incomplete Events, rejects cyclic event order, verifies exact typed-hypergraph reconstruction, verifies the charged algebraic sidecar boundary, detects extensional occurrence-identity loss, and rejects stale or mutated specifications, proofs, and reports.
