# Phase 2 Campaign 1 — Formal Systems

## Purpose

This campaign externally pressure-tests the frozen Project FAR Foundation v1.0 against five established formal reasoning systems:

1. classical propositional logic;
2. first-order logic;
3. predicate-logic quantifier reasoning;
4. natural deduction;
5. sequent calculus.

The campaign does not revise the foundation. It asks whether each target system can be represented through the frozen FAR vocabulary without omitting a structurally necessary component or importing an unacknowledged primitive.

## Evaluation Standard

Each case study tests whether the target system exhibits identifiable counterparts for:

- investigation;
- representation;
- representational structure;
- interpretation;
- reasoning calculus;
- operations participating functionally in reasoning;
- admissibility constraints;
- reasoning states or state representations;
- transition records or proof traces;
- resolution or derivation outcome.

A case passes structural coverage when all components required by the target system can be mapped without contradiction. A pass does not establish that FAR is uniquely correct, complete for all systems, or superior to the target formalism.

## Falsification Conditions

The campaign would count against Foundation v1.0 if any target system demonstrated one of the following:

- explicit reasoning without representations;
- reasoning representations with no organization;
- semantic evaluation with no interpretation;
- a scoped proof or derivation with no investigation-relative objective;
- admissible inferential change with no rule or calculus;
- a required reasoning component that cannot be expressed through FAR without changing frozen definitions;
- a contradiction generated solely by applying FAR's frozen concepts to the target system.

## Method

For each target system:

1. define a representative reasoning task;
2. map the formal objects into FAR roles;
3. reconstruct a short derivation or proof process;
4. test each frozen primitive role;
5. identify any mismatch, excess structure, or hidden assumption;
6. classify the result.

## Result Scale

- **PASS** — FAR covers the tested structure without contradiction or required foundation change.
- **PASS WITH LIMITATION** — FAR covers the structure, but a limitation or underdetermined mapping remains.
- **FAIL** — the target system demonstrates a structural counterexample or requires a foundation change.
- **INCONCLUSIVE** — available analysis does not determine the result.

## Campaign Boundary

This campaign tests structural applicability only. It does not claim:

- soundness of every target calculus;
- completeness of every target calculus;
- equivalence between FAR and the target system;
- mechanized verification;
- empirical universality.

## Campaign Result

The five case studies yield five structural passes, with limitations concerning semantic optionality, proof-object granularity, and the distinction between object-language and metalanguage.

Final campaign status:

**FORMAL SYSTEMS CAMPAIGN PASS WITH LIMITATIONS**
