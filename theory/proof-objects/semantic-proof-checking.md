# Semantic Proof Checking

Status: Provisional

## Structural validation

Structural validation verifies YAML shape, required proof-object fields, unique identifiers, available inputs, known rules, step statements, justifications, and conclusion matching.

## Rule-pattern validation

Rule-pattern validation checks reliable rule-specific input patterns, such as theorem-bearing inputs for `prior_theorem`, lemma-bearing inputs for `lemma_application`, axiom-bearing inputs for `axiom_application`, definitional sources for `definition_unfolding`, and minimum input counts for conjunction and modus ponens.

## Semantic validation

Semantic validation compares proof-step claims with structured statements and semantic vocabulary when available. Current semantic comparison is intentionally soft where exact matching is not reliable; weak overlap is reported as a warning rather than a hard failure.

## Current limitations

The current checker is not a theorem prover. It does not decide arbitrary natural-language equivalence, construct missing derivations, or certify Lean-level proof terms.

## Future exact proof checking

Future exact checking requires more formal statement objects, explicit term syntax, formal rule semantics, and a mechanized backend capable of certifying derivability.
