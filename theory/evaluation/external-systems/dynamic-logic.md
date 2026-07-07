# External System Evaluation — Dynamic Logic

## Overview

Dynamic logic reasons about programs or actions and their effects using modal operators indexed by programs. It combines logical consequence with transition semantics.

## Investigation

Determine whether dynamic logic can be represented using the five FAR primitives.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Determine whether a property holds after executing a program or action. |
| Representation | Program expressions, states, formulas, modalities, preconditions, and postconditions. |
| Representational Structure | State-transition relations, program composition, sequencing, choice, iteration, and modality indexing. |
| Interpretation | Relational semantics over program-induced state transitions. |
| Reasoning Calculus | Modal proof rules, program transformation rules, induction over iteration, and Hoare-style reasoning where applicable. |

## Pressure Point

The pressure is program-indexed modality. Truth is evaluated relative to possible transitions produced by represented programs.

## Classification

`conservative extension`

## Justification

Dynamic logic requires transition semantics and program-indexed interpretation. Those are specialized forms of Representational Structure and Interpretation, governed by a domain-specific Reasoning Calculus. It does not require a sixth primitive.

## Sixth Primitive Assessment

No sixth primitive is currently indicated.

## Confidence

Provisional.

## Remaining Questions

- Whether program iteration requires a reusable derived concept for fixed-point or inductive transition closure.
- Whether hybrid systems should be evaluated separately.
