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

The source catalog cryptographically indexes six immutable source bundles containing 18 indexed source records under `theory/evaluation/rcs-corpus-sources/`.

- `theory/evaluation/rcs-concrete-source-catalog-v1.0.json` — SHA-256 `6b0249b64216585371a7a57362396201336064f5edce7849408c513f3168ea3f`
- `theory/evaluation/rcs-positive-corpus-v1.0.json` — SHA-256 `1a70c175601e199b6b0c412dadec2d48ac4fe94106b850a0a97b24cd352030dd`
- `theory/evaluation/rcs-contrast-corpus-v1.0.json` — SHA-256 `0f206b1f1bb8fa9ead5937d56f992513dd3d5887a92f85888e70f2591bb0f578`
- `theory/evaluation/rcs-disputed-corpus-v1.0.json` — SHA-256 `db04d13a5b8465a6debcf2483b9287fb58dc8b6ad0ac4a7a570aa70139097312`
- `theory/evaluation/w3-5-corpus-freeze-result-v1.0.json` — SHA-256 `d178e5a3e649c0f4926f7803480cc61eb297ab38baa28082a6cdfd1dc8635f2a`

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
