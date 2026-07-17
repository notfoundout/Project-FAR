# GMA-001 — Bounded Global Minimality Assessment

## Status

Completed evidence synthesis. Scientific conclusion: **global minimality unresolved**.

## Question

Does the current five-primitive FAR vocabulary have the lowest commitment-distinct vocabulary cost among all vocabularies capable of preserving the required benchmark commitments?

Absolute global minimality cannot be established by a finite candidate set. GMA-001 therefore distinguishes:

- minimality within the current FAR vocabulary;
- minimality over the frozen AVC-001 search space;
- unrestricted global minimality.

## Evidence used

GMA-001 synthesizes, without re-scoring:

1. PIE-001, which attempted elimination, derivability, merger, substitution, and recovery for each FAR primitive;
2. AVC-001, which compared FAR with nine frozen alternative vocabularies on `CRE-001-REFERENCE-V1`;
3. the preregistered preservation, hidden-reintroduction, complexity, and Pareto rules.

## Results by claim level

| Claim | Result | Basis |
|---|---|---|
| Current-vocabulary deletion minimality | Unresolved | Direct elimination failed for all five primitives, but derivability and substitution remain incomplete. |
| Simple-merger resistance | Supported on CRE-001 | The two four-primitive merger candidates lost commitments or reconstructed the original distinctions. |
| Minimality over the ten AVC-001 candidates | Unresolved | No lower-cost candidate was established as admissible and dominating, but five lower-cost candidates retain unresolved judgments. |
| Unrestricted global minimality | Not established | The candidate space, benchmark space, and evaluator space are finite and incomplete. |
| Global minimality falsified | No | No admissible lower-cost vocabulary was shown to match or dominate FAR. |

## Primitive-count bounds

On the frozen CRE-001 comparison:

- FAR provides a resolved admissible representation with five commitment-distinct primitives;
- no three- or four-primitive competitor was established as an admissible equal-or-better replacement;
- several three-primitive competitors remain unresolved rather than defeated.

Accordingly, the current evidence supports only this interval:

> The minimum demonstrated sufficient primitive count is at most five and may be as low as three within the tested families.

This is an epistemic bound, not a theorem that three primitives are sufficient or that five are necessary.

## Why no stronger result follows

A global-minimality conclusion requires closure over the relevant alternative-vocabulary space. GMA-001 lacks that closure because:

- vocabularies below three primitives were not tested;
- only ten candidate vocabularies were frozen;
- only one benchmark was used;
- unresolved semantic and information-preservation judgments remain;
- candidate construction and evaluation were internal rather than blinded and independent.

Failure to find a dominating competitor is not evidence that no such competitor exists outside this search space.

## Decision

- bounded global-minimality assessment: **unresolved**;
- FAR global minimality: **not established**;
- FAR global minimality falsified: **no**;
- lower-cost admissible replacement found: **no**;
- unresolved lower-cost competitors retained: **yes**.

## Falsification condition

The current five-primitive minimality hypothesis is falsified as soon as one lower-cost vocabulary is demonstrated to:

1. preserve every required dimension;
2. avoid commitment-equivalent hidden reintroduction;
3. use fewer commitment-distinct primitives;
4. Pareto-dominate or equal FAR on representation cost.

## Next evidence required

The next assessment must expand the benchmark set with cases that independently vary:

- representation and interpretation;
- investigation and reasoning calculus;
- structure and represented elements;
- rule identity before and after modification;
- semantic content under operationally identical traces.

It must also execute blinded mappings for the unresolved three-primitive candidates and add explicitly frozen one- and two-primitive challenge vocabularies.

## Artifacts

- `search-space.json` — exact included and excluded search space;
- `tests/test_global_minimality_assessment.py` — deterministic evidence and claim-boundary checks.
