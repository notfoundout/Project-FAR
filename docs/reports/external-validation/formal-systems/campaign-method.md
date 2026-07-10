# Formal Systems External Validation Campaign Method

## Purpose

This campaign tests whether the frozen Project FAR Foundation v1.0 can represent and evaluate reasoning in five established formal systems without altering the foundation:

- classical propositional logic;
- first-order logic;
- predicate-logic quantifier reasoning;
- natural deduction;
- sequent calculus.

This is external validation, not internal theorem validation. The campaign asks whether FAR can faithfully model each target system, identify its required reasoning components, preserve its distinctions, and expose where FAR adds no explanatory value or fails.

## Frozen Baseline

The campaign treats Foundation v1.0 as fixed. No axiom, definition, lemma, proposition, theorem, proof object, or dependency declaration may be changed in this branch.

## Evaluation Questions

Each case study answers:

1. What are the target system's representations?
2. What representational structure organizes them?
3. What interpretations assign semantic content?
4. What investigation scopes the reasoning task?
5. What reasoning calculus governs admissible steps?
6. What operations occur?
7. Can FAR reconstruct a valid target-system derivation?
8. Can FAR distinguish valid, invalid, malformed, and out-of-scope reasoning?
9. Does FAR preserve syntax/semantics and process/trace distinctions?
10. What is not established by the mapping?

## Test Pattern

Each system is tested with:

- one valid derivation;
- one invalid or non-derivable inference;
- one malformed or scope-violating case;
- one limitation analysis.

## Outcome Classes

- PASS: FAR represents the target case without contradiction or loss relevant to the investigation.
- CONDITIONAL PASS: FAR succeeds only after explicit target-calculus assumptions are supplied.
- FAIL: FAR cannot represent or distinguish a required feature without changing the frozen foundation.
- INCONCLUSIVE: available evidence does not decide the question.

## Non-Claims

A PASS does not prove FAR is complete for the entire target logic, logically equivalent to it, or superior to it. It shows only that the tested target-system cases can be represented and evaluated under the frozen FAR foundation.

## Isolation

This campaign is not blind validation. It is an explicit comparative mapping performed against known target systems. No independence class is claimed beyond ordinary documented analysis.
