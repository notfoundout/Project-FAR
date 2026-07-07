# External System Evaluation — Hoare Logic

## Overview

Hoare logic reasons about program correctness using triples relating preconditions, programs, and postconditions.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Determine whether a program satisfies a specification. |
| Representation | Programs, preconditions, postconditions, invariants, triples, and proof obligations. |
| Representational Structure | Program syntax, control-flow structure, state-transition structure, and invariant dependencies. |
| Interpretation | State-based semantics of program execution. |
| Reasoning Calculus | Assignment, sequencing, conditional, loop, consequence, and invariant rules. |

## Pressure Point

Hoare logic pressures FAR through program-state semantics and invariant reasoning.

## Classification

`conservative extension`

## Justification

The required machinery is a state-transition interpretation and program-specific calculus. Both are expressible within existing FAR primitives.

## Confidence

Provisional.
