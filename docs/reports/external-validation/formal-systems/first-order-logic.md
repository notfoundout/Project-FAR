# External Validation: First-Order Logic

## Target System

First-order logic extends propositional logic with predicates, individual variables, constants, functions, quantifiers, variable assignments, domains, and structures interpreting the non-logical vocabulary.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | term, atomic formula, quantified formula, premise, conclusion, assignment |
| Representational structure | syntax tree, variable-binding structure, derivation sequence, first-order structure |
| Interpretation | domain plus assignments to constants, functions, and predicates |
| Investigation | determine truth in a structure, validity, satisfiability, or derivability |
| Reasoning calculus | specified first-order proof rules and variable conditions |
| Operation | substitution, instantiation, generalization, evaluation, rule application |

## Valid Case

Premises:

1. ∀x (Human(x) → Mortal(x))
2. Human(s)

Conclusion:

Mortal(s)

Universal elimination yields Human(s) → Mortal(s); implication elimination then yields Mortal(s). FAR can represent the formula hierarchy, the supplied interpretation-independent derivation, the investigation, and the two admissible steps.

Result: PASS.

## Invalid Case

Premise:

∃x Human(x)

Conclusion:

∀x Human(x)

A structure with two objects, only one of which satisfies Human, makes the premise true and conclusion false. FAR can encode the countermodel and classify the inference as non-valid under first-order semantics.

Result: PASS.

## Malformed or Scope-Violating Case

Attempt:

From Human(a), infer ∀x Human(x), where `a` is not arbitrary but names a specific object introduced by a premise.

The generalization violates the target calculus's eigenvariable or arbitrariness condition. FAR can record the attempted operation but admissibility depends on the supplied first-order rule conditions.

Result: PASS.

## Distinction Tests

- Bound versus free variables are structural properties of formulas.
- Syntax does not determine denotation without a domain and interpretation.
- Truth in a structure differs from logical validity across all structures.
- A substitution operation differs from the written proof line recording its result.

## Limitations

FAR does not define first-order domains, variable assignments, quantifier semantics, or admissible generalization rules. The target system supplies them. The mapping therefore validates FAR as a host meta-framework for tested first-order reasoning, not as an independent first-order proof system.

## Final Outcome

CONDITIONAL PASS

Condition: the first-order signature, domain, interpretation, and proof calculus must be explicitly supplied.
