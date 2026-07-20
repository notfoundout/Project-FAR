# S_core W1 Direct-Axis Proof Audit

## Audit target

This audit covers:

- `docs/research/s-core-w1-direct-axis-proof-v1.0.md`;
- `theory/evaluation/s-core-w1-direct-axis-proof.json`;
- `tools/s_core_w1_reference.py`;
- `tests/test_s_core_w1_reference.py`;
- `theory/evaluation/s-core-w1-reference-fixtures.json`;
- integration with `SCORE-LEMMA-LEDGER-001`, `THM-TARGET-001`, `FAITHFUL-REP-001`, P8-ROLE-001, governance, planning, and repository health checks.

## Audit question

Does the package prove the registered W1 carrier and direct-axis construction obligations over every finite W0-normalized direct-axis reduct without silently assuming recovery, global semantics, coherence, dynamics, or the representation theorem?

## Result

**Pass as project-authored human-checkable proof, pending proof-assistant verification and independent review.**

The proof uses one fixed finite incidence schema, `DIR-INCIDENCE-1.0`, for all direct axes. Source-specific sorts, roles, values, and denotations enter as target data rather than new schemas or case-specific code.

## Dependency audit

The package uses:

- W0 finiteness and canonical reduct extraction;
- W0 source-isomorphism transport;
- the frozen FARA target interface;
- canonical FARA category separations;
- the frozen strong-embedding semantics of `FAITHFUL-REP-001`;
- the split P8 decision for internal evidential status.

It does not use:

- any W2 dynamics or history lemma;
- admissible target-only recovery;
- global semantic agreement;
- cross-axis coherence as an assumption;
- a complete global machinery ledger;
- theorem-level FARA adequacy.

## Construction audit

For each source element, value, relation occurrence, and attribute occurrence, the constructor allocates explicit target objects. Every target object receives a distinct representation. The target therefore preserves the mandatory distinctions between:

- object and representation;
- represented relation occurrence and its representation;
- source role identity and lexical display label;
- source element identity and target helper objects.

The fixed target schema contains explicit sort, role, axis, position, occurrence, argument, attribute, provenance, evidence-status, and denotation records. All helper objects are linked to represented source images and declared in the W1 machinery fragment.

## Strong-embedding audit

The source-element map is total, typed, and injective. A source relation fact is represented by an occurrence object with one role code and ordered argument links. The derived target relation is true exactly when such an occurrence exists.

Therefore:

- every true source tuple produces a target tuple;
- every target tuple over represented source elements comes from a true source tuple;
- source relation roles remain distinct even when their display labels are similar;
- relation and attribute symbol namespaces remain distinct;
- exact attribute copying satisfies the default source value equivalence.

## Axis audit

The generic theorem specializes to:

- P1 configuration;
- P2 commitments;
- P3 stakes and alternatives;
- P4 grounds and justificatory roles;
- P6 consequences;
- P8-I internal provenance and evidential status.

The proof therefore resolves:

- `LEM-SC-005`;
- `LEM-SC-006`;
- `LEM-SC-007`;
- `LEM-SC-008`;
- `LEM-SC-009`;
- `LEM-SC-012`;
- `LEM-SC-014`.

## Obstruction audit

The same quantified construction refutes:

- `OBS-SC-003`, because arbitrary finite P2, P3, and P4 relation structures admit preservation-and-reflection embeddings without relation collapse;
- `OBS-SC-006`, because arbitrary finite P8-I reducts admit exact embeddings without evidence-status loss, fabrication, or upgrade.

These refutations are limited to the registered direct-axis scopes. They do not preclude later failures of recovery, semantics, coherence, dynamics, composition, or complete machinery accounting.

## Executable audit

The executable reference and fixtures test:

- baseline construction for all direct axes;
- object/representation separation;
- injectivity and sort preservation;
- shared target images for shared source items;
- independent relation and attribute namespaces;
- spurious-relation rejection;
- collapsed-image rejection;
- support/defeat noncollapse;
- live-alternative retention;
- consequence-role retention;
- evidential-upgrade rejection;
- display-label alpha-renaming invariance;
- malformed shared-sort rejection.

These tests are bounded corroboration and regression protection. They are not proof-assistant verification.

## Ledger effect

After registration:

- total obligations: 37;
- proved construction obligations: 11;
- established target obstructions: 0;
- established source-scope boundaries: 1;
- refuted obstruction hypotheses: 2;
- open obligations: 23;
- completed waves: W0 and W1;
- active wave: W2.

## Gate effects

- formal-theorem-target: remains satisfied;
- premise-ledger-and-semantics: remains satisfied;
- faithful-representation-definition: remains satisfied;
- scoped-representation-proof: remains not satisfied;
- mechanized-proof-verification: remains not satisfied;
- independent-proof-review: remains not satisfied.

No central claim is promoted.

## Exact next work

Execute the W2 package:

- `LEM-SC-010` deterministic dynamics;
- `LEM-SC-011` finite-support probabilistic dynamics;
- `LEM-SC-013` history and path;
- `LEM-SC-015` nonmonotonic revision and retraction;
- `LEM-SC-016` self-modification and rule-version change;
- `OBS-SC-004` and `OBS-SC-005` when their dependencies close.
