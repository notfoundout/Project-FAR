# External Validation: Predicate and Quantifier Reasoning

## Target Focus

This case isolates quantifier-scope, substitution, and dependency phenomena that are often obscured when first-order logic is treated only as a general system.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | quantified sentence, open formula, witness term, variable condition |
| Representational structure | quantifier nesting, binding graph, dependency ordering |
| Interpretation | domain and predicate extension |
| Investigation | determine whether a quantified conclusion follows |
| Reasoning calculus | quantifier introduction/elimination rules with side conditions |
| Operation | witness introduction, instantiation, substitution, scope comparison |

## Valid Case

Premise:

∀x ∃y Loves(x,y)

Conclusion:

For an arbitrary object `a`, ∃y Loves(a,y).

Universal elimination supports the conclusion for arbitrary `a`. FAR preserves the dependency between the selected arbitrary object and the existential claim without treating the witness as globally fixed.

Result: PASS.

## Invalid Scope-Swap Case

Premise:

∀x ∃y Loves(x,y)

Conclusion:

∃y ∀x Loves(x,y)

The conclusion requires one common object loved by every object, while the premise permits a different witness for each `x`. FAR's representational-structure requirement can encode the different quantifier nesting and expose that the two formulas are not structurally interchangeable.

Result: PASS.

## Invalid Witness Reuse Case

Premises:

1. ∃x F(x)
2. ∃x G(x)

Conclusion:

∃x (F(x) ∧ G(x))

The existential witnesses need not be identical. FAR can represent two witness-introduction operations and preserve their independence under the target calculus.

Result: PASS.

## Malformed Substitution Case

Attempt to substitute a term containing a variable into a formula in a way that captures that variable.

The resulting expression may be syntactically formed as a token string but is not an admissible capture-avoiding substitution. FAR can distinguish the recorded transformation from its admissibility under the quantifier calculus.

Result: PASS.

## Limitations

FAR does not itself provide capture-avoidance rules, eigenvariable conditions, or quantifier semantics. Its contribution is to force those constraints, dependencies, and scope relations to be explicit.

## Final Outcome

CONDITIONAL PASS

Condition: quantifier rules and side conditions must be supplied by the target calculus.
