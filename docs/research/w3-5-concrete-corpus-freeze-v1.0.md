# W3.5 Concrete Reasoning and Contrast Corpus Freeze v1.0

## Status

Frozen candidate-independent corpus package. Candidate scoring and W3.5 execution have not begun.

Identifiers: `RCS-CORPUS-001`, `W35-CORPUS-FREEZE-RESULT-001`.

## Purpose

This package satisfies only the concrete-corpus freeze required by `RCS-001` and `W3.5-SDG-001`. It fixes nonempty positive, contrast, and disputed registries before any GREL–FARA factorization, candidate-invariant scoring, ablation, or reconstruction result is exposed to admission.

## Corpus composition

| Class | Count | Families represented |
|---|---:|---|
| Positive | 8 | deductive proof, probabilistic inference, defeasible reasoning, planning, diagnosis, legal/policy reasoning, self-modifying machine reasoning, partially observed reasoning |
| Contrast | 8 | passive database, event log, ordinary workflow, arbitrary labeled transition system, lookup table, traffic controller, cellular automaton, random finite-state machine |
| Disputed | 2 | reinforcement-learning policy execution, constraint propagation without search |

The disputed cases are preserved rather than forced into a favorable binary classification.

## Candidate independence

Every admission decision was made from the frozen behavioral specification and source/observation contract. Admission rationales do not use FARA compatibility, GREL comparison, candidate-invariant presence or absence, or the expected W3.5 conclusion. The candidate registry preexisted this freeze, so the package is not described as evaluator-blind or a private holdout. Every record declares `candidate_exposure_status: candidate_registry_preexisted_admission_rationale_independent_no_scores_or_results_exposed`; no candidate scores or W3.5 results were exposed before admission.

## Observation boundary

Each source record fixes:

- observable or formal states;
- transitions and constraints;
- represented distinctions;
- declared semantics;
- history and path dependence;
- objectives or tasks;
- grounds or dependencies;
- commitment-like or alternative-like structure;
- uncertainty and revision;
- provenance and correspondence limits.

Only the enumerated finite system is admitted. Unrecorded implementation behavior, operator intent, hardware timing, and external context are excluded.

## Frozen artifacts

The source catalog cryptographically indexes 18 separate immutable source records under `theory/evaluation/rcs-corpus-sources/`.

- `theory/evaluation/rcs-concrete-source-catalog-v1.0.json` — SHA-256 `73470eb64cb777dfd8e4314667f128a4966e743b726895186f8fc44360e7c50d`
- `theory/evaluation/rcs-positive-corpus-v1.0.json` — SHA-256 `b190d22b0890c609aaa093b81927f61b1a26f696468f8c09c024ec1a4531e96a`
- `theory/evaluation/rcs-contrast-corpus-v1.0.json` — SHA-256 `579db283bf513f99c78f8a40424a0de7027d9e7e9b65222db702d008e963ff7a`
- `theory/evaluation/rcs-disputed-corpus-v1.0.json` — SHA-256 `676441742f4bb4b9f564df7fecbd0e28c8f1cec54baec6141f1462c7f56f913c`
- `theory/evaluation/w3-5-corpus-freeze-result-v1.0.json` — SHA-256 `30d2d0331d4a0aebc833283bafe2a1fd88d36080b63726a8ba9b0f1d0c56e28e`

## Decision effect

The `reasoning-contrast-corpus-frozen` research gate may move to `satisfied` with the linked evidence above. `W3.5-SDG-001` remains in progress. The following remain unresolved or not executed:

- GREL–FARA factorization;
- FARA specificity;
- reasoning/contrast discrimination;
- candidate ablation and reconstruction;
- machinery and cost accounting;
- W3.5 claim-impact closure;
- W5 theorem assembly.

## Nonclaims

This freeze is not a private holdout and does not establish statistical representativeness, empirical prevalence, FARA-specificity, universal structure, necessity, minimality, uniqueness, W3.5 resolution, or W5 authorization.
