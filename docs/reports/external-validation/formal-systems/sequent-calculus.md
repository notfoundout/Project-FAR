# External Validation: Sequent Calculus

## Target System

Sequent calculus represents derivations using sequents such as Γ ⊢ Δ and rules that transform premise sequents into conclusion sequents. Structural rules and logical left/right rules govern admissibility.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | formula occurrence, context, sequent, inference-rule instance |
| Representational structure | derivation tree with antecedent/succedent positions |
| Interpretation | optional semantic relation supporting soundness analysis |
| Investigation | derive a target sequent or test admissibility |
| Reasoning calculus | selected sequent calculus, including structural and logical rules |
| Operation | context extension, exchange, contraction, weakening, cut, logical rule application |

## Valid Case

Identity sequent:

P ⊢ P

The identity rule directly licenses the sequent. FAR can represent the left/right positions, the rule instance, and the one-node derivation.

Result: PASS.

## Valid Multi-Step Case

From:

Γ ⊢ P

and:

Δ, P ⊢ Q

infer:

Γ, Δ ⊢ Q

under a calculus admitting Cut.

FAR can represent both premise sequents, the shared cut formula, context combination, and the cut operation. If the target calculus excludes Cut as primitive but admits cut elimination, the classification changes according to that supplied calculus.

Result: PASS.

## Invalid Case

Attempt to infer:

Γ ⊢ Q

from:

Γ ⊢ P

without any rule connecting P to Q.

The conclusion is not licensed merely because both are formulas. FAR records the attempted transition and rejects it under the supplied rule set.

Result: PASS.

## Structural Scope Case

In a linear or substructural sequent calculus, unrestricted contraction or weakening is attempted.

FAR can represent the attempted structural operation but must classify admissibility relative to the chosen calculus. The same operation may be valid in classical sequent calculus and invalid in a resource-sensitive calculus.

Result: PASS.

## Distinction Tests

- Formula identity does not erase antecedent/succedent position.
- Contexts are structured collections, not merely informal lists.
- Rule admissibility is calculus-relative.
- A derivation tree is a representation of the reasoning process, not the process itself.
- Cut elimination is a metatheoretic property and is not supplied by FAR.

## Limitations

FAR does not prove soundness, completeness, cut elimination, normalization, or decidability for a target sequent calculus. Those require independent metatheory. FAR can host and audit the explicit structures involved.

## Final Outcome

CONDITIONAL PASS

Condition: the exact sequent syntax, structural policy, and inference rules must be supplied.
