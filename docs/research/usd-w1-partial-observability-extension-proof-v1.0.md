# USD-W1 Partial-Observability Extension Proof v1.0

## Status

Complete bounded deductive result for the frozen source class `S_po_fin`.

## Claim

For every admitted finite explicit partially observable reasoning presentation in `S_po_fin`, there exists a target object in the frozen theorem-facing FARA class and a witness preserving the registered partial-observability commitments without giving the represented policy access to the true latent state.

Formally, for every source presentation `P` satisfying `USD-W1-PO-SCOPE-001`, there exist `A` and `W` such that `A` uses the fixed `A_FARA` interface and `W` satisfies the frozen preservation obligations for latent-state distinction, observation indistinguishability, information state, policy measurability, transition/observation update, commitments, grounds, dependencies, history, revision, and internal evidential status.

## Frozen source class

`S_po_fin` requires finite nonempty latent and observation carriers, an explicit total observation relation or finite-support kernel, an explicit initial information state, finite action and transition interfaces, policies measurable with respect to observation history, explicit commitments and dependencies, and a declared source interpretation.

The represented agent is permitted to access only observation history and the information state derived from it. The proof author may inspect the complete frozen source object to construct and verify the representation, but the target policy interface may not query the true latent state.

## Uniform construction

Given a source presentation:

1. represent each latent state as a target state object;
2. represent each observation as a target observation object;
3. encode the observation relation or finite-support kernel explicitly;
4. represent each information state as the set, or finite-support distribution, of latent states compatible with the observation history;
5. encode admissible actions as constraints indexed by observation history and information state rather than true state;
6. encode transition and observation updates as separate linked relations;
7. preserve commitment, ground, dependency, consequence, revision, and provenance records at each information state;
8. preserve the difference between analyst-visible latent truth and agent-available evidential status.

The construction is uniform because its schema depends only on the frozen interface and source fields. It does not introduce a source-specific interpreter, oracle, target primitive, or evaluator repair rule.

## Obligations

### `PO-EXT-001` — Total uniform constructor

Every admitted source contains all finite carriers and explicit relations needed by the construction. Therefore the constructor is defined for every object in `S_po_fin`.

### `PO-EXT-002` — Observation indistinguishability

Latent states that produce the same observation history remain distinct target states but belong to the same represented information state. No commitment or action may distinguish them unless the source observation history does.

### `PO-EXT-003` — Information-state preservation

The target information state is extensionally equal to the source-compatible latent-state set, or to the source finite-support belief when probabilities are supplied.

### `PO-EXT-004` — Policy measurability

Target action constraints are functions of represented observation history and information state. They do not receive a latent-state argument.

### `PO-EXT-005` — Transition and observation update

Each source transition followed by an observation update has a corresponding target transition followed by the linked observation and information-state update. Reflection holds because target updates not licensed by the source relations are inadmissible.

### `PO-EXT-006` — Commitments, grounds, and dependencies

Commitments and their grounds are indexed to the source information available at the corresponding observation history. Analyst knowledge of the latent state cannot upgrade the represented agent's entitlement.

### `PO-EXT-007` — History and revision

Observation histories, information-state histories, latent histories, commitment revisions, and dependency changes remain separately recoverable. Matching current observations do not erase distinct paths.

### `PO-EXT-008` — No true-state leakage

A target representation that selects actions by unobserved latent state violates policy measurability and is rejected. Encoding the latent state in metadata presented to the policy is equivalent leakage and is also rejected.

### `PO-EXT-009` — Negative controls

`PO-NEG-LEAK-001` is rejected because the policy uses inaccessible true state. `PO-NEG-COLLAPSE-001` is rejected because it merges information states with different admissible actions, destroying operational preservation.

## Result

The frozen finite explicit partial-observability subclass is faithfully representable without a new target primitive. The terminal workstream outcome is `proper_subclass_only`, because the result excludes infinite or continuous observation structures, non-finite-support kernels, open-ended histories, semantic change, and actual-process correspondence.

## Claim boundaries

This proof does not establish representation of all partially observable reasoning, representation of `S_IRD`, a universal reasoning kernel, representation invariance across alternative vocabularies, primitive necessity, minimality, uniqueness, actual-process correspondence, mechanized verification, or independent review.
