# S_core W0 Proof Audit

## Scope

This audit records the internal acceptance boundary for `SCORE-W0-PROOF-001` and its integration with `SCORE-LEMMA-LEDGER-001`.

## Results audited

- `LEM-SC-001`: proved by finite typed canonicalization;
- `LEM-SC-002`: proved by least finite reference closure and induced reduct extraction;
- `LEM-SC-003`: proved by stabilization of monotone subsets of a finite material universe and finite nonemptiness testing;
- `LEM-SC-004`: proved by transport of closure, reducts, and canonical codes under source isomorphism;
- `OBS-SC-001`: resolved as `scope_boundary_established` because non-finite material closure violates the frozen `S_core` source requirements.

## Premise audit

The proof uses only:

- frozen `S_core` finiteness and explicitness conditions;
- the frozen source materiality-closure rule;
- finite graph reachability;
- finite induced relational structures;
- sort-preserving isomorphism transport;
- existence of a minimum in a finite nonempty totally ordered code set.

It does not use:

- a FARA target constructor;
- FARA adequacy;
- `Faithful_split` satisfiability;
- PB-001 completeness;
- actual-process correspondence;
- evaluator agreement or empirical replication.

## Hidden-assumption checks

- Unused symbols in a potentially broader source signature are omitted only from the theorem-facing material reduct; they are not asserted nonexistent.
- Semantic constants are fixed when rigid; non-rigid material values are typed carrier items and are transported.
- Cyclic references terminate under set reachability and do not create infinitely many material items.
- Canonicalization enumerates all sort-preserving bijections and therefore does not depend on source labels or case identifiers.
- Efficiency is not claimed. The result establishes finite effectiveness and termination.
- `OBS-SC-001` is not misreported as evidence that FARA succeeds; it is a source-scope classification.

## Executable corroboration

The reference implementation and fixtures check:

- closure completeness;
- closure termination with cycles;
- exact axis applicability;
- source-renaming invariance;
- reduct transport under renaming;
- closure of reduct dependencies;
- rejection of undeclared references;
- rejection of sort-changing renamings.

These checks are bounded executable corroboration. They do not constitute proof-assistant verification.

## Ledger effects

- proved construction obligations: 4;
- established source-scope boundaries: 1;
- open obligations: 32;
- completed wave: W0;
- active wave: W1.

The scoped-representation-proof gate remains not satisfied because no target construction or `Faithful_split` witness has been established.

## Claim effects

No central claim is promoted. In particular, the result establishes only the finite source-normalization kernel required for later target construction.

## Review status

- project-authored human-checkable proof: complete;
- bounded executable reference checks: complete;
- proof-assistant verification: not started;
- independent proof review: not started.

## Next artifact

Construct or obstruct the W1 base-carrier and direct-axis package: `LEM-SC-005`, `006`, `007`, `008`, `009`, `012`, and `014`.
