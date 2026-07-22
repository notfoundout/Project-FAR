# USD-W1-CD-001 v1.0 — Continuous-Dynamics Scope Extension

## Status

Complete bounded extension proof for `S_cd_lip_eff`.

## Frozen question

Does the existing theorem-facing target class admit a uniform faithful representation of effectively presented finite-dimensional continuous reasoning systems with unique computable Lipschitz flows, without replacing continuous semantics by a fixed finite time grid or importing exact-real and future-trajectory oracles?

## Source class

`S_cd_lip_eff` contains source objects with:

- a finite-dimensional compact rational-box state domain;
- a declared compact real-time horizon;
- an effectively evaluable vector field with an explicit computable global Lipschitz bound;
- optional piecewise-rational controls;
- finitely many effectively decidable guards with isolated crossings and declared reset maps;
- finite commitments, grounds, dependencies, revisions, and evidential annotations indexed to trajectories and event history.

Nonunique, Zeno, infinite-dimensional, noncomputable, unrestricted-horizon, and actual-process cases are outside this frozen source class.

## Construction

For each admitted source object, construct one target object containing:

1. effectively named continuous state objects;
2. the vector-field, guard, reset, and control interfaces as declared operational constraints;
3. certified rational enclosures for state values at requested rational times and tolerances;
4. one uniform refinement operation that tightens those enclosures;
5. explicit time order and event order;
6. separate commitment, ground, dependency, revision, and evidential-status histories;
7. one uniform recovery interface shared across the source class.

The construction does not materialize the full continuum. It represents the continuous object intensionally through its frozen effective presentation and a coherent family of certified finite observations. This is not a finite truncation: every rational query time and positive rational tolerance is handled by the same total refinement procedure, and compatible refinements commute.

## Why the flow is preserved

The explicit Lipschitz bound gives uniqueness and effective stability over the frozen compact domain. Certified integration/refinement procedures therefore produce nested enclosures whose diameter can be made smaller than any requested positive rational tolerance. The family identifies one trajectory extensionally through all certified observations rather than identifying it with one numerical mesh.

For any requested finite observation:

- source and target state enclosures agree to the requested tolerance;
- temporal ordering is unchanged;
- admissibility and transition judgments derived from the frozen interfaces are preserved;
- isolated guard crossings are bracketed and ordered;
- declared reset effects are preserved;
- commitment and revision events retain their grounds and dependency history.

## Event preservation

The scope admits only effectively decidable guard families with isolated crossings. Certified bracketing can therefore refine around each crossing without assuming an exact-real equality oracle. The represented event history records the guard, crossing interval, reset, downstream commitments, and dependency effects. A fixed grid that misses a crossing fails the preservation contract.

## Obligation results

- `CD-EXT-001`: proved — the constructor and recovery interface are uniform and total on `S_cd_lip_eff`.
- `CD-EXT-002`: proved — flow semantics are preserved through coherent certified observations.
- `CD-EXT-003`: proved — real-time order and event order are preserved.
- `CD-EXT-004`: proved — isolated guard and declared reset semantics are preserved.
- `CD-EXT-005`: proved — commitments, grounds, and dependencies remain distinct.
- `CD-EXT-006`: proved — history and revision effects remain time-indexed and recoverable.
- `CD-EXT-007`: proved — refinements are nested and compatible.
- `CD-EXT-008`: proved — no fixed discretization is accepted as exact continuous coverage.
- `CD-EXT-009`: proved — all frozen negative controls are rejected or retained as scope boundaries.

## Adversarial controls

`CD-NEG-GRID-001` is rejected because a finite grid misses an intervening guard crossing and therefore changes event, revision, and dependency history.

`CD-NEG-ORACLE-001` is rejected because exact-real equality and future-trajectory access are undeclared machinery.

`CD-BOUND-NONUNIQ-001` is excluded because the source presentation does not identify one flow. Adding a selection rule after failure would change the frozen source class.

`CD-BOUND-ZENO-001` is excluded because finite-time event accumulation violates the isolated finite-event contract.

## Terminal classification

`proper_subclass_only`.

The proof extends faithful representation to `S_cd_lip_eff`. It does not establish all continuous dynamics, all differential equations, infinite-dimensional systems, noncomputable presentations, nonunique flows, Zeno systems, unrestricted horizons, `S_IRD`, or universal structure.

## Claim effect

This is a third bounded feature-family result for `THM-IRD-EXT-001`. It supplies no logical proof of universal existence, representation invariance, necessity, minimality, uniqueness, reasoning specificity, or actual-process correspondence.

## Nonclaims

This result does not establish that:

- all continuous reasoning systems are represented;
- a numerical approximation is identical to an exact physical trajectory;
- every differential equation has a unique computable solution;
- FARA is necessary, minimal, unique, or universal;
- an actual process has been captured;
- this extension has been mechanized or independently reviewed.
