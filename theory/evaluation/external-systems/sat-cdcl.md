# External System Evaluation — SAT/CDCL Solving

## Overview

SAT solving determines whether a Boolean formula is satisfiable. Conflict-driven clause learning adds structured search, implication graphs, conflict analysis, and learned clauses.

## Investigation

Determine whether SAT/CDCL reasoning can be represented using the five FAR primitives.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Determine whether a Boolean formula is satisfiable or unsatisfiable. |
| Representation | Variables, literals, clauses, assignments, conflicts, implication graphs, learned clauses, and certificates. |
| Representational Structure | Clause-variable incidence, assignment dependencies, implication graph, and conflict structure. |
| Interpretation | Boolean valuation semantics. |
| Reasoning Calculus | Unit propagation, decision rules, conflict analysis, clause learning, backjumping, and certificate checking. |

## Pressure Point

The pressure is operational complexity. CDCL is search-heavy, but its transitions and certificates are explicit.

## Classification

`fits FAR`

## Justification

SAT/CDCL maps cleanly to FAR because its reasoning artifacts are explicit and machine-checkable. Clauses and assignments are representations, implication graphs are representational structure, Boolean valuation gives interpretation, and CDCL rules provide calculus.

## Sixth Primitive Assessment

No sixth primitive is currently indicated.

## Confidence

Provisional.

## Remaining Questions

- Whether heuristic branching should be treated as reasoning or search policy.
- Whether proof certificates are sufficient for evaluating solver output independently of search history.
