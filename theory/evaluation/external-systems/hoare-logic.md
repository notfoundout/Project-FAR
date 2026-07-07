# External System Evaluation — Hoare Logic

## Overview

Hoare logic reasons about program correctness using triples of preconditions, programs, and postconditions. It pressures FAR through program-state semantics and rule-governed verification.

## Investigation

Determine whether a program satisfies a postcondition whenever it starts in a state satisfying a precondition.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Verify partial or total correctness of a program. |
| Representation | Hoare triples, programs, assertions, variables, states, invariants, and proof obligations. |
| Representational Structure | Program syntax, state-transition structure, assertion dependency, and control-flow structure. |
| Interpretation | Semantics of program execution and assertion satisfaction over states. |
| Reasoning Calculus | Assignment, sequence, conditional, loop, consequence, and invariant rules. |

## Pressure Point

The pressure is state-indexed correctness, especially loops and invariants.

## Classification

`conservative extension`

## Justification

Hoare logic requires program semantics and a verification calculus, but both are representable as Interpretation and Reasoning Calculus over explicit program and assertion representations.

## Sixth Primitive Assessment

No sixth primitive is currently indicated.

## Confidence

Provisional.

## Remaining Questions

- Whether loop invariants and variants should be registered as derived concepts.
- Whether total correctness requires separate termination machinery.
