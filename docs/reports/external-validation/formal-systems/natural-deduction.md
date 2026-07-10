# External Validation: Natural Deduction

## Target System

Natural deduction represents proofs as sequences or trees governed by introduction and elimination rules, often with temporary assumptions and discharge conditions.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | formula occurrence, assumption marker, rule annotation, proof line |
| Representational structure | proof tree or ordered derivation with nested subproofs |
| Interpretation | optional semantics for formulas; not required for purely syntactic derivation |
| Investigation | derive a target formula from specified premises |
| Reasoning calculus | selected natural-deduction rules and discharge conditions |
| Operation | assumption opening, rule application, assumption discharge, formula copying |

## Valid Case

Goal:

P → P

Derivation:

1. Assume P.
2. Infer P by reiteration.
3. Discharge the assumption and infer P → P by implication introduction.

FAR can represent the temporary assumption, nested subproof structure, discharge operation, and final proof trace. It also distinguishes the reasoning process from the persistent proof representation.

Result: PASS.

## Invalid Case

Attempt:

1. Assume P.
2. Derive Q without a rule or premise supporting Q.
3. Infer P → Q.

The subproof contains an unsupported step. FAR can represent the attempted trace but classify the step and resulting discharge as inadmissible under the supplied calculus.

Result: PASS.

## Scope-Violating Case

A formula derived inside a subproof depends on a temporary assumption. The formula is then used outside that subproof without discharging or otherwise accounting for the assumption.

The target proof structure records an open dependency that remains unavailable outside the subproof. FAR can represent this as a structural and admissibility failure rather than merely a temporal ordering problem.

Result: PASS.

## Structural Tests

- Assumption occurrence and assumption discharge are different operation types.
- Identical formula strings at different proof locations may have different dependency contexts.
- A proof tree's branch structure carries information not recoverable from an unordered set of formulas.
- Semantic truth is not required to determine formal derivability, though a semantics may be supplied for soundness analysis.

## Limitations

FAR does not generate natural-deduction introduction/elimination rules. It also does not decide whether a proof search strategy will terminate. These remain properties of the supplied target calculus and implementation.

## Final Outcome

CONDITIONAL PASS

Condition: the natural-deduction rule set, assumption discipline, and discharge conditions must be supplied explicitly.
