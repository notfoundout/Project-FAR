# Predicate-Logic Quantifier Reasoning Validation

## Test Case

Premises:

1. `∀x (A(x) ∨ B(x))`
2. `¬B(c)`

Target conclusion:

3. `A(c)`

A representative derivation instantiates the universal premise at `c`, then applies disjunctive reasoning with `¬B(c)`.

## FAR Mapping

| FAR role | Target-system counterpart |
| --- | --- |
| Investigation | Determine whether `A(c)` follows from the quantified premises. |
| Representation | Quantified formula, negated atomic formula, instantiated disjunction, and conclusion. |
| Representational structure | Quantifier scope, variable binding, predicate application, and proof order. |
| Interpretation | Domain and extensions for `A` and `B`, when semantic validity is assessed. |
| Reasoning calculus | Universal instantiation and classical disjunctive inference. |
| Operation | Instantiation and elimination steps. |
| Admissibility | Satisfaction of substitution and inference-rule side conditions. |
| Reasoning state | Available premises and derived formulas. |
| Resolution | Derivation of `A(c)`. |

## Structural Test

The example pressure-tests the difference between a syntactically legal substitution and an arbitrary textual replacement. Quantifier reasoning requires explicit structural constraints governing free and bound variables. The licensed move cannot be characterized by bare change alone.

FAR's operation concept captures the performed step, while the applicable reasoning calculus supplies the conditions under which that step is admissible. The distinction prevents the framework from treating every symbol manipulation as reasoning.

## Pressure Findings

1. Admissibility is indispensable for distinguishing valid quantifier manipulation from variable capture or malformed substitution.
2. The same visible formula can receive different semantic content under different interpretations.
3. Object-language derivation and metalanguage justification are distinct representational layers. FAR can represent both, but the mapping must state which investigation each layer serves.

## Counterexample Search

No counterexample was found in which valid explicit quantifier reasoning lacked representational structure or calculus-relative admissibility. The object-language/metalanguage distinction remains a modeling responsibility.

## Result

**PASS WITH LIMITATION**

The frozen foundation covers the tested quantifier structure. The limitation is that FAR does not automatically identify the correct representational level when object-language and metalanguage reasoning are interleaved.
