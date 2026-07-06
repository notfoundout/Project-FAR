# Semantic Proof-Checking Roadmap

Status: Provisional

## Current structural validation

Structural validation checks that a proof object is well-formed YAML with required top-level fields, unique premise and step identifiers, available inputs, known rule names, step statements, justifications, and a conclusion that appears as a proof-step statement.

This level verifies shape and local references. It does not verify that a rule was semantically appropriate.

## Rule-pattern validation

Rule-pattern validation checks that each declared rule has the minimum reliable input pattern currently known to Project FAR. Examples include requiring theorem-bearing inputs for `prior_theorem`, lemma-bearing inputs for `lemma_application`, axiom-bearing inputs for `axiom_application`, definition-bearing or approved definitional inputs for `definition_unfolding`, and at least two inputs for conjunction introduction.

This level is stricter than structural validation because it rejects proof steps whose declared rule cannot be supported by the lineage of their inputs.

## Semantic validation

Semantic validation compares what a proof step claims against the machine-readable statements and semantic vocabulary of its cited inputs. In v0.2.0 this is intentionally soft where exact formal matching is not reliable. The checker may warn when a step has weak overlap with an available metadata statement, while reserving hard failures for reliable constraints such as missing required source kinds.

Semantic validation is successful when the checker can establish that:

- the cited source has the expected artifact kind;
- the input lineage supplies the concepts required by the declared rule;
- the proof-step statement is compatible with the cited metadata statement when a statement object is present;
- conditional rules such as `modus_ponens` have both conditional-like and antecedent-like inputs;
- semantic-preservation and registry-substitution steps cite the relevant semantic or registry sources.

## Limits of the current checker

The current checker is not a theorem prover. It does not parse arbitrary natural language into formal logic, does not decide equivalence of all Project FAR statements, does not construct missing intermediate steps, and does not certify Lean-level derivability.

Its role is to move from rule labels toward reproducible semantic evidence while avoiding false hard failures where the repository lacks formal statements.

## v0.2.0 success condition

For v0.2.0, successful semantic checking means all current `T-001` through `T-015` proof objects pass stricter source-kind and rule-specific validation, metadata records expose minimal statement objects, and semantic mismatches that cannot yet be decided exactly are reported as soft warnings rather than accepted silently or rejected unsafely.
