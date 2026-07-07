# External System Evaluation — Coq

## Overview

Coq is an interactive theorem prover based on the Calculus of Inductive Constructions. It tests FAR against dependent type theory, proof-state manipulation, inductive definitions, tactics, and kernel checking.

## Investigation

Determine whether Coq proof construction and verification can be represented using the five FAR primitives.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Prove a theorem or verify a construction in a formal context. |
| Representation | Terms, types, propositions, contexts, tactics, proof scripts, proof terms, and inductive objects. |
| Representational Structure | Dependency structure among terms, contexts, inductive definitions, and proof states. |
| Interpretation | Type-theoretic interpretation of propositions, terms, and constructions. |
| Reasoning Calculus | Kernel type checking, conversion, tactic-induced transformations, and induction principles. |

## Pressure Point

The pressure comes from dependent typing and proof-as-construction semantics. These require specialized interpretation and calculus, but they remain explicit.

## Classification

`fits FAR`

## Justification

Coq's accepted reasoning is kernel-checked. Its proof states and proof objects are explicit enough to map directly to FAR's representations, structures, interpretations, and calculus-governed transitions. Tactic search may be operationally complex, but accepted proof artifacts remain auditable.

## Sixth Primitive Assessment

No sixth primitive is currently indicated.

## Confidence

Provisional.

## Remaining Questions

- Whether proof automation should be evaluated separately from proof validation.
- Whether extraction and computation should be treated as reasoning calculus extensions.
