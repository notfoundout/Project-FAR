# External System Evaluation — SMT Solving

## Overview

SMT solving extends SAT-style search with background theories such as arithmetic, arrays, bit-vectors, or uninterpreted functions.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Determine satisfiability modulo selected theories. |
| Representation | Formulas, terms, theory symbols, assignments, constraints, lemmas, and certificates. |
| Representational Structure | Boolean structure, theory-specific term structure, and solver dependency graphs. |
| Interpretation | Theory semantics for the selected background domains. |
| Reasoning Calculus | DPLL(T), theory propagation, conflict explanation, lemma learning, and certificate checking. |

## Pressure Point

SMT pressures FAR through multiple simultaneous semantics: Boolean search plus theory interpretation.

## Classification

`conservative extension`

## Justification

SMT requires domain-specific theory interpretation and calculus integration, but those are conservative extensions of Interpretation and Reasoning Calculus. No new primitive is indicated.

## Confidence

Provisional.
