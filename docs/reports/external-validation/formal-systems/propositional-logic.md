# External Validation: Classical Propositional Logic

## Target System

Classical propositional logic uses propositional variables, truth-functional connectives, well-formed formulas, valuations, and derivation rules or truth tables.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | propositional variable, formula, valuation entry, proof line |
| Representational structure | formula parse tree, proof sequence, valuation table |
| Interpretation | valuation assigning truth values to propositional variables and formulas |
| Investigation | determine validity, satisfiability, contradiction, or derivability |
| Reasoning calculus | selected classical truth-table or proof-rule system |
| Operation | formula construction, valuation, rule application, comparison, determination |

## Valid Case

Premises:

1. P → Q
2. P

Conclusion:

Q

Under a classical natural-deduction calculus, modus ponens permits Q. FAR can represent the premises and conclusion, bind them to one investigation, record the governing calculus, and distinguish the rule application from the proof trace documenting it.

Result: PASS.

## Invalid Case

Premises:

1. P → Q
2. Q

Conclusion:

P

This is affirming the consequent. A truth valuation with P false and Q true satisfies both premises while falsifying the conclusion. FAR can represent the attempted inference and classify it as inadmissible under the supplied classical calculus.

Result: PASS.

## Malformed Case

Expression:

P ∧ → Q

The expression is not a well-formed formula under the supplied syntax. FAR can represent the token sequence, but it cannot treat the sequence as an admissible formula unless the target calculus admits it.

Result: PASS.

## Distinction Tests

- Syntax versus semantics: the same formula structure may receive different truth values under different valuations.
- Process versus trace: the act of evaluating or deriving is distinct from the recorded table or proof sequence.
- Validity versus truth: validity concerns preservation across admissible valuations, not the actual truth of premises.

## Limitations

FAR does not supply classical truth tables or modus ponens by itself. Those belong to the target reasoning calculus. FAR therefore provides a meta-structure for making the reasoning explicit, not a replacement for propositional logic.

## Final Outcome

CONDITIONAL PASS

Condition: the classical propositional syntax, semantics, and admissible rules must be supplied explicitly as the target calculus and interpretation.
