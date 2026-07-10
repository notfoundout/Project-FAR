# Phase 2 Campaign 1 Results — Formal Systems

## Executive Summary

Campaign 1 tested Project FAR Foundation v1.0 against classical propositional logic, first-order logic, predicate-logic quantifier reasoning, natural deduction, and sequent calculus.

All five target systems were structurally representable through the frozen FAR roles without changing the foundation. No target produced a counterexample involving explicit reasoning without representations, organization, investigation-relative scope, or calculus-relative admissibility.

The campaign found limitations rather than failures:

- syntactic derivation does not always require a selected semantic interpretation, although semantic evaluation does;
- object-language and metalanguage reasoning must be explicitly separated;
- reasoning traces may be branching, nested, or graph-structured rather than linear;
- FAR does not supply the specific rules of a target calculus and must not be mistaken for doing so.

Final result:

**FORMAL SYSTEMS CAMPAIGN PASS WITH LIMITATIONS**

## Case Results

| Target system | Result | Primary pressure point |
| --- | --- | --- |
| Classical propositional logic | PASS | Syntax/semantics separation and rule/application distinction |
| First-order logic | PASS WITH LIMITATION | Binding, substitution conditions, and calculus neutrality |
| Predicate quantifier reasoning | PASS WITH LIMITATION | Admissibility and object-language/metalanguage separation |
| Natural deduction | PASS | Nested assumptions, discharge, and structured proof states |
| Sequent calculus | PASS WITH LIMITATION | Branching proof states and non-linear traces |

## Cross-System Findings

### 1. Representation is consistently required

Every tested system manipulates explicit formula, sequent, context, assumption, or proof-node representations. None provided a case of explicit formal reasoning with no distinguishable representational objects.

### 2. Representational structure does substantive work

Structure is not decorative. It determines:

- connective scope;
- quantifier binding;
- antecedent/succedent position;
- active assumptions;
- proof-tree dependency;
- permissible substitution;
- derivation order.

A collection of formula strings without these relations does not preserve the tested reasoning systems.

### 3. Interpretation is role-dependent

Pure syntactic derivations can be conducted without fixing a particular valuation or model. Interpretation becomes necessary when the investigation concerns truth, satisfaction, semantic consequence, soundness, or completeness.

This does not falsify FAR's interpretation role. It shows that the role must be understood relative to the investigation and that syntactic and semantic investigations are distinct.

### 4. Calculus supplies admissibility

No tested system licensed inference by bare transformation alone. Valid moves were determined by rule schemas and side conditions. This supports the frozen distinction between operation and admissibility under a reasoning calculus.

### 5. Reasoning state is structurally richer than a formula set

Natural deduction and sequent calculus show that proof state may include:

- active assumptions;
- open goals;
- context position;
- nested subproofs;
- multiple branches;
- dependency relations.

Future implementations must therefore avoid defining reasoning state as only an unordered set of representations.

### 6. Traces need not be linear

A simple sequence is adequate for some derivations but insufficient for nested or branching proofs. FAR can accommodate this through representational structure, but implementation schemas should support trees or directed acyclic graphs.

## Falsification Review

The campaign explicitly searched for:

- representation-free formal reasoning;
- structure-free formal reasoning;
- rule-free admissible inference;
- unscoped formal investigation;
- a target-system primitive that cannot be represented through FAR;
- contradiction between frozen FAR roles and established proof structures.

No such counterexample was found in the five tested cases.

This is limited evidence. The sample is small, selected, and non-mechanized. It supports compatibility, not universality.

## Foundation Impact

No Foundation v1.0 change is recommended.

No axiom, definition, lemma, proposition, theorem, proof, or dependency should be altered as a result of Campaign 1.

## Implementation Requirements Discovered

A future FAR reference implementation should support:

1. typed representation objects;
2. explicit syntax trees and binding relations;
3. investigation-relative interpretation layers;
4. target-calculus rule registries;
5. rule side conditions;
6. nested and branching reasoning states;
7. graph-structured proof traces;
8. separation of rule specifications from rule applications;
9. separation of object-language and metalanguage artifacts;
10. audit records that preserve both derivation order and dependency structure.

These are implementation requirements, not additions to the frozen foundation.

## Remaining Questions

1. Does the same mapping remain stable for intuitionistic, relevant, paraconsistent, modal, temporal, and linear logics?
2. Can a proof assistant encode the mappings without adding hidden structural assumptions?
3. How should FAR distinguish a semantic investigation from a purely syntactic one in machine-readable metadata?
4. Should reasoning trace be implemented as a general directed graph with linear traces as a special case?
5. Can adversarial formal systems expose a target-calculus component that falls outside the frozen roles?

## Campaign Status

**FORMAL SYSTEMS CAMPAIGN PASS WITH LIMITATIONS**

Campaign 2 may begin after this draft PR is reviewed and accepted. The next recommended campaign is mathematics, but non-classical logics should remain a separate later stress campaign rather than being treated as already covered by this result.
