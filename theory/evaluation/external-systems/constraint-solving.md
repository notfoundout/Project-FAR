# External System Evaluation — Constraint Solving

## Overview

Constraint solving determines assignments satisfying explicit constraints over finite, numeric, logical, or structured domains.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Determine whether constraints have a satisfying assignment. |
| Representation | Variables, domains, constraints, assignments, conflicts, and solutions. |
| Representational Structure | Constraint graph, domain restrictions, dependency relations, and search tree. |
| Interpretation | Domain semantics for variable assignments and constraint satisfaction. |
| Reasoning Calculus | Propagation, pruning, consistency checking, branching, and solution validation. |

## Pressure Point

The pressure is domain-specific propagation and search.

## Classification

`fits FAR`

## Justification

Constraint solving maps directly when variables, domains, constraints, and solver transitions are explicit. Domain-specific propagators are calculus rules rather than new primitives.

## Confidence

Provisional.
