# External System Evaluation — Higher-Order Logic

## Overview

Higher-order logic extends quantification beyond individuals to predicates, functions, relations, or other higher-order objects. It is a strong external test because it pressures the boundary between representation and interpretation.

## Investigation

Determine whether higher-order consequence can be evaluated using the five FAR primitives.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Determine whether a higher-order formula follows from higher-order assumptions. |
| Representation | Formulas, variables, predicates, functions, relations, types, and proof steps. |
| Representational Structure | Binding structure, type structure, application structure, and dependency relations among formulas. |
| Interpretation | Higher-order semantics assigning domains to individuals and higher-order objects. |
| Reasoning Calculus | Higher-order inference rules, beta/eta conversion where applicable, and proof rules. |

## Pressure Point

The pressure is not the existence of higher-order objects. FAR can treat those objects as representations. The pressure is whether interpretation must quantify over richer semantic domains.

## Classification

`conservative extension`

## Justification

Higher-order logic requires a specialized interpretation policy and calculus for higher-order quantification. That is more than a direct first-order mapping, but it does not require a sixth primitive. The missing machinery is semantic and calculational, both already assigned to existing FAR primitive categories.

## Sixth Primitive Assessment

No sixth primitive is currently indicated. Higher-order domains expand Interpretation and Reasoning Calculus rather than adding a new primitive kind.

## Confidence

Provisional.

## Remaining Questions

- Whether full semantics versus Henkin semantics should be represented as separate interpretation policies.
- Whether higher-order unification needs a derived concept in future analysis.
