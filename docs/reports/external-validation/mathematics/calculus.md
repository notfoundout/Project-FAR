# External Validation: Differential Calculus

## Target System

Differential calculus studies limits, continuity, derivatives, and local rates of change under explicit domain and regularity assumptions.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | function, expression, limit statement, derivative, interval, proof line |
| Representational structure | dependency on variables, domain restrictions, limit nesting, equation chain |
| Interpretation | real-valued function over a specified domain |
| Investigation | establish a limit, derivative, continuity claim, or counterexample |
| Reasoning calculus | real-number axioms, limit definitions, derivative definitions, and proved rules |
| Operation | substitution, simplification, limit transformation, differentiation, comparison |

## Valid Case

Claim: The derivative of f(x) = x² is 2x.

Using the limit definition:

f'(x) = lim(h→0) [(x+h)² - x²]/h

= lim(h→0) [2xh + h²]/h

= lim(h→0) (2x + h)

= 2x.

FAR can represent the function, the investigation, each algebraic transformation, the condition h ≠ 0 during cancellation, and the final limit determination.

Result: PASS.

## Invalid Case

Claim: If lim(x→a) f(x) = L, then f(a) = L.

The claim is false without continuity or an equivalent condition. FAR can expose the missing premise and distinguish a limit statement from the function's value at the point.

Result: PASS.

## Malformed or Scope-Violating Case

A proof cancels h in a difference quotient and then substitutes h = 0 before the cancellation step has been justified on the punctured neighborhood.

FAR can distinguish the transformation domain from the final limit operation and identify the scope error.

Result: PASS.

## Limitations

FAR does not supply real analysis, epsilon-delta semantics, derivative rules, or convergence theorems. Those must come from the target calculus.

## Final Outcome

CONDITIONAL PASS

Condition: domains, regularity assumptions, limit semantics, and admissible algebraic or analytic rules must be explicit.
