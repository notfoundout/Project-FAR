# External System Evaluation — Lean

## Overview

Lean is an interactive theorem prover based on a dependent type theory and a small trusted kernel. It is a high-value external test because it contains explicit representations, proof states, tactics, terms, elaboration, and kernel validation.

## Investigation

Determine whether Lean proof construction and verification can be represented using the five FAR primitives.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Prove or verify a theorem in a formal environment. |
| Representation | Terms, types, declarations, goals, hypotheses, tactics, proof terms, and theorem statements. |
| Representational Structure | Context structure, dependency graph, term syntax, type dependencies, and proof-state transitions. |
| Interpretation | Lean's formal semantics for terms and types under its kernel and elaboration environment. |
| Reasoning Calculus | Kernel rules, tactic transformations, type checking, and proof validation. |

## Pressure Point

The main pressure is complexity, not primitive failure. Lean includes elaboration and automation, but the checked proof object remains explicit relative to the kernel.

## Classification

`fits FAR`

## Justification

Lean naturally separates representations, contexts, semantics, and calculus-governed validation. Tactics may be opaque as search procedures, but their accepted outputs are kernel-checkable. FAR can evaluate the explicit proof artifact even when tactic generation is not itself transparent.

## Sixth Primitive Assessment

No sixth primitive is currently indicated. Lean's proof process maps directly to FAR's existing categories.

## Confidence

Provisional.

## Remaining Questions

- Whether tactic search should be evaluated as reasoning or as proof-object generation.
- Whether elaboration deserves a derived concept in future external validation.
