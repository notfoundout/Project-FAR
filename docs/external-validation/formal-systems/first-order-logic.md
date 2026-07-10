# First-Order Logic Validation

## Test Case

Premises:

1. `∀x (Human(x) → Mortal(x))`
2. `Human(socrates)`

Target conclusion:

3. `Mortal(socrates)`

The derivation uses universal instantiation followed by modus ponens.

## FAR Mapping

| FAR role | Target-system counterpart |
| --- | --- |
| Investigation | Determine whether `Mortal(socrates)` follows from the premises. |
| Representation | Predicate formulas, variable symbols, constant symbols, and the derived formula. |
| Representational structure | First-order syntax, binding structure, term formation, formula formation, premise set, and derivation sequence. |
| Interpretation | A domain plus assignments to constants, predicates, and variables. |
| Reasoning calculus | Quantifier and propositional inference rules. |
| Operation | Universal instantiation and modus ponens applications. |
| Reasoning state | Current formulas and variable/term conditions. |
| Transition | Addition of instantiated and derived formulas. |
| Resolution | Derivation of `Mortal(socrates)`. |

## Structural Test

First-order reasoning requires more representational organization than propositional reasoning because variable binding, term structure, and quantifier scope affect admissibility. A sequence of visible symbols is insufficient without structural relations determining which quantifier binds which occurrence.

The interpretation role is explicit when evaluating model-theoretic satisfaction. A syntactic proof may proceed without selecting a particular model, but its semantic significance depends on a class of interpretations.

## Pressure Findings

1. Representational structure must include binding and scope, not merely a collection of formula strings.
2. Interpretation must distinguish object-language symbols from their denotations.
3. Calculus-relative side conditions, including restrictions on substitutions, are part of admissibility rather than bare operation.
4. FAR describes the structural roles but does not itself supply first-order substitution rules; those belong to the target calculus.

## Counterexample Search

No explicit first-order derivation was found that eliminates representation, structure, or calculus. Model-theoretic evaluation additionally requires interpretation. No foundation change was required.

## Result

**PASS WITH LIMITATION**

Foundation v1.0 covers the tested first-order proof structure. The limitation is that FAR remains calculus-neutral and therefore does not determine the target system's substitution and quantifier rules by itself.
