# USD-W1-OH-001 v1.0 — Open-Ended Histories Scope Extension

## Status

Complete bounded extension proof for `S_hist_eff`.

## Frozen question

Does the theorem-facing target class admit a uniform faithful representation of effectively presented histories with no declared terminal length, while preserving every finite prefix, dependency cone, revision, and rule-change record without importing a future-history oracle or treating one fixed horizon as total coverage?

## Source class

`S_hist_eff` contains finite or countably open-ended event histories with:

- effective event indices and a total uniform finite-prefix procedure;
- no frozen terminal length requirement;
- finite effectively recoverable dependency cones for every event and judgment;
- stable prefix embeddings preserving identity and order;
- finitely described commitments, grounds, dependencies, evidential states, revisions, and rule changes at each finite stage;
- finitely supported retroactive changes with explicit change certificates.

Non-effective indexing, future-complete oracle access, unrecoverable infinite-past dependencies, unbounded past rewrites without finite certificates, uncountable unnamed events, and actual-process correspondence are excluded.

## Construction

For every admitted source history and prefix length `n`, construct a target prefix containing:

1. stable names for the first `n` events;
2. event order and source-declared admissibility judgments;
3. explicit finite dependency cones;
4. distinct commitments, grounds, dependencies, revisions, evidential states, and rule-change records;
5. retained rejected and superseded alternatives when they are part of source history;
6. a compatible extension map from prefix `n` to every later prefix;
7. one recovery map shared across the entire source class.

The representation is the coherent directed family of all finite prefixes, not any one finite prefix and not a completed future trace. For `m <= n`, recovering the first `m` events from the `n`-prefix gives the same result as constructing the `m`-prefix directly. Therefore event identity, order, dependencies, and history commute with extension.

## Why open-endedness is preserved

No target prefix asserts that the source has terminated. Every admitted finite prefix exposes the same uniform next-extension interface. A later source event, revision, or rule change can be represented without rebuilding or renaming the preserved past. This distinguishes an open-ended representation from a large but fixed trace.

For every requested finite stage:

- source and target prefixes have the same events and order;
- each judgment has the same finite recoverable dependency cone;
- commitments, grounds, and dependencies remain distinct;
- revisions preserve the exact before-and-after state and their reasons;
- rejected and superseded records remain recoverable where the source retains them;
- extension remains available without reading future events.

## Obligation results

- `OH-EXT-001`: proved — one total uniform constructor handles every requested finite prefix.
- `OH-EXT-002`: proved — prefix construction and recovery commute with extension.
- `OH-EXT-003`: proved — event identity and order remain stable.
- `OH-EXT-004`: proved — finite dependency cones remain explicit and recoverable.
- `OH-EXT-005`: proved — commitments, grounds, and dependencies remain distinct.
- `OH-EXT-006`: proved — revisions and rule changes retain complete before-and-after history.
- `OH-EXT-007`: proved — no represented stage closes the extension interface.
- `OH-EXT-008`: proved — a fixed terminal horizon is not accepted as open-ended coverage.
- `OH-EXT-009`: proved — registered negative controls are rejected and boundary cases remain excluded.

## Adversarial controls

`OH-NEG-HORIZON-001` is rejected because the chosen horizon omits a later revision and changes downstream dependency history.

`OH-NEG-FUTURE-001` is rejected because present representation and admissibility may not depend on events unavailable at the represented stage.

`OH-BOUND-INFINITE-PAST-001` is excluded because no finite effective dependency certificate is available for the relevant judgment.

`OH-BOUND-GLOBAL-REWRITE-001` is excluded because an unbounded past rewrite cannot be represented through the frozen finite-change interface without adding undeclared machinery.

## Terminal classification

`proper_subclass_only`.

The proof extends faithful representation to `S_hist_eff`. It does not establish all infinite histories, non-effective histories, uncountable event domains, unrestricted infinite-past dependence, arbitrary global rewrites, `S_IRD`, or universal structure.

## Claim effect

This is a fourth bounded feature-family result for `THM-IRD-EXT-001`. It does not establish representation invariance, necessity, minimality, uniqueness, reasoning specificity, actual-process correspondence, or a universal kernel.

## Nonclaims

This result does not establish that:

- every infinite or open-ended history is represented;
- the complete future is available at any finite stage;
- a fixed large trace is equivalent to an open-ended history;
- FARA is necessary, minimal, unique, or universal;
- an actual process has been captured;
- this extension has been mechanized or independently reviewed.
