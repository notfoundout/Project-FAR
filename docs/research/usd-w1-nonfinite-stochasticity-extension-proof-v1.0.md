# USD-W1-NFS-001 — Non-finite-support stochasticity scope extension

## Status

Complete bounded extension proof for `S_stoch_eff`.

## Frozen question

Does the existing theorem-facing target class admit a uniform faithful representation of countable effectively presented stochastic reasoning systems with certified infinite-support tails, bounded computable probability and expectation queries, and effective positive-probability conditioning, without replacing the distribution by a finite support truncation or importing exact infinite-sum, null-event, or future-outcome oracles?

## Source class

`S_stoch_eff` contains source objects with countable effective carriers, computable point-mass or transition-kernel interfaces, certified tail bounds or summation moduli, bounded computable observables, finite stopping horizons, and conditioning events carrying certified positive probability and an effective denominator bound. Finite commitments, grounds, dependencies, revisions, and evidential annotations may depend on the represented stochastic state and update history.

Noncomputable kernels, uncertified uncountable integration, null-event conditioning, uncertified unbounded observables, unrestricted infinite-horizon convergence, and actual-process correspondence are outside the frozen source class.

## Construction

For every admitted source object, construct one target object containing:

1. effectively named state and outcome objects;
2. the point-mass or transition-kernel interface;
3. certified rational lower and upper approximants for finite cylinder probabilities;
4. certified rational approximants for bounded computable expectations;
5. explicit tail or summation-modulus certificates;
6. positive-probability conditioning records with numerator and denominator certificates;
7. separate belief, commitment, ground, dependency, revision, and evidential histories;
8. one uniform finite-query recovery interface.

The construction is intensional. It does not enumerate the entire support and does not identify a finite truncation with the source distribution. For every requested rational tolerance, the same total procedure returns a certified approximation whose residual tail is below that tolerance. Refinements are nested and compatible.

## Preservation argument

Probability mass is preserved extensionally through all certified finite queries: point masses, finite cylinders, and bounded expectation queries agree to arbitrary requested rational precision. The tail certificate proves that omitted support is bounded rather than erased. Positive-probability conditioning preserves the source update because numerator and denominator approximants converge effectively and the denominator certificate prevents division by an unresolved zero.

Commitments and revisions triggered by probabilistic thresholds retain the source probability certificate, grounds, dependencies, and update history. A finite truncation that changes the threshold result, loses residual mass, or changes a downstream revision fails the preservation contract.

## Obligation results

- `NFS-EXT-001`: proved — one total uniform constructor and recovery interface covers the admitted class.
- `NFS-EXT-002`: proved — probability mass and finite cylinder queries are preserved through certified approximants.
- `NFS-EXT-003`: proved — bounded computable expectations are preserved to arbitrary rational precision.
- `NFS-EXT-004`: proved — certified positive-probability conditioning and declared updates are preserved.
- `NFS-EXT-005`: proved — commitments, grounds, and dependencies remain distinct.
- `NFS-EXT-006`: proved — belief and revision history remains indexed and recoverable.
- `NFS-EXT-007`: proved — tail and summation refinements are coherent.
- `NFS-EXT-008`: proved — finite support truncation is never accepted as exact infinite-support coverage.
- `NFS-EXT-009`: proved — frozen negative controls are rejected and boundary cases remain excluded.

## Adversarial controls

`NFS-NEG-TRUNC-001` is rejected because it discards certified tail mass and can change probability thresholds, expectations, commitments, and revisions.

`NFS-NEG-ORACLE-001` is rejected because exact infinite summation and future random outcomes are undeclared machinery.

`NFS-BOUND-NULL-001` is excluded because the frozen source does not supply a regular conditional interface for a null or effectively unresolved zero-probability event.

`NFS-BOUND-NONCOMP-001` is excluded because no total effective approximation procedure exists in the declared presentation.

`NFS-BOUND-UNBOUNDED-001` is excluded because expectation recovery lacks a certified integrability or convergence modulus.

## Terminal classification

`proper_subclass_only`.

The proof extends faithful representation to `S_stoch_eff`. It does not establish all stochastic reasoning systems, arbitrary uncountable measures, noncomputable kernels, null-event conditioning, unrestricted unbounded observables, or unrestricted infinite horizons.

## Claim effect

This is a sixth bounded feature-family result for `THM-IRD-EXT-001`. It supplies no logical proof of universal existence, representation invariance, necessity, minimality, uniqueness, reasoning specificity, or actual-process correspondence.

## Nonclaims

This result does not establish that:

- all stochastic reasoning systems are represented;
- finite truncation is exact;
- every probability measure or conditional distribution is computable;
- arbitrary null-event conditioning is defined;
- FARA is necessary, minimal, unique, or universal;
- an actual process has been captured;
- this extension has been mechanized or independently reviewed.
