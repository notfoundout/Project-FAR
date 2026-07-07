# External System Evaluation — SMT Solving

## Overview

SMT solving extends SAT-style search with background theories such as arithmetic, arrays, bit-vectors, equality, and uninterpreted functions. It is a stronger external test than pure SAT because Boolean search is combined with theory-specific reasoning.

## Investigation

Determine whether a formula is satisfiable relative to one or more background theories.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Decide satisfiability modulo selected theories. |
| Representation | Formulas, Boolean skeletons, theory atoms, assignments, conflicts, lemmas, and certificates where available. |
| Representational Structure | Clause structure, theory constraints, equality graphs, dependency relations, and conflict explanations. |
| Interpretation | Theory semantics for arithmetic, arrays, equality, bit-vectors, and other selected domains. |
| Reasoning Calculus | DPLL(T), theory propagation, conflict explanation, lemma learning, and certificate checking. |

## Pressure Point

The pressure is the interaction between generic Boolean search and multiple domain-specific theory solvers.

## Classification

`conservative extension`

## Justification

SMT solving extends SAT/CDCL with specialized interpretation and calculus for background theories. The added machinery remains within Interpretation, Representational Structure, and Reasoning Calculus.

## Sixth Primitive Assessment

No sixth primitive is currently indicated.

## Confidence

Provisional.

## Remaining Questions

- Whether mixed-theory combination needs a derived concept.
- Whether incomplete or heuristic solvers require separate treatment from checkable certificates.
