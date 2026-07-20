# Generic Typed Relational Baseline v1.0

## Status

Frozen neutral comparison baseline.

Identifier: `GREL-001`.

## Purpose

`GREL-001` tests whether the W0–W3 construction succeeds because of specifically FARA commitments or because any sufficiently general finite typed relational representation can copy explicit source structure.

The baseline contains no reasoning-specific primitive and is not selected to fail.

## Baseline structure

A finite baseline package is:

\[
G=(T,U,V,A,R,\Sigma_G,E_G,D_G,K_G)
\]

where:

- `T` is a finite set of sort identifiers;
- `U` is a finite carrier of entities;
- `V` is a finite carrier of exact values;
- `A` is a finite set of typed attributes;
- `R` is a finite set of typed ordered n-ary relation occurrences;
- `Sigma_G` is a finite schema describing the preceding records;
- `E_G` is one canonical encoder from a frozen finite typed relational source contract;
- `D_G` is one canonical target-only decoder;
- `K_G` is a complete finite machinery ledger.

## Excluded reasoning-specific commitments

The baseline does not primitively contain:

- investigation;
- commitment;
- stake;
- ground;
- justification;
- admissibility;
- consequence;
- interpretation;
- evidence;
- provenance;
- reasoning calculus;
- reasoning state;
- reasoning trace.

Any such distinction may appear only as ordinary encoded data, typed relations, attributes, or values.

## Canonical encoder

`E_G`:

1. allocates one typed target entity for each source entity;
2. allocates one relation-occurrence record for each source relation fact;
3. preserves ordered arguments;
4. allocates exact value records;
5. records source sorts, attributes, dynamics, history, decomposition, interpretation declarations, and provenance as typed data;
6. uses no source-case identifier or case database;
7. is equivariant under source isomorphism.

## Canonical decoder

`D_G` receives only the completed baseline package, its descriptor, and `K_G`. It returns the canonical target-indexed typed relational reduct or a deterministic failure diagnostic.

## Factorization questions

W3.5 must determine:

1. whether the accepted W0–W3 FARA constructor factors through `GREL-001`;
2. whether the FARA target can be recovered from `GREL-001` by a fixed translation;
3. whether `GREL-001` can satisfy the same frozen preservation and recovery obligations;
4. which FARA category separations impose constraints not present in the baseline;
5. whether those constraints are reasoning-specific, audit-specific, semantic, or organizational;
6. whether either architecture dominates under a declared machinery and cost relation.

## Multidimensional result

W3.5 must report each dimension independently.

### Expressiveness

- `fara_stronger`
- `grel_stronger`
- `equivalent`
- `incomparable`
- `unresolved`

### Translation

- `bidirectional`
- `fara_to_grel_only`
- `grel_to_fara_only`
- `none`
- `failed_for_explicit_reason`
- `unresolved`

### Constraint strength

- `fara_stricter`
- `grel_stricter`
- `equivalent`
- `incomparable`
- `unresolved`

### Reasoning specificity

- `established`
- `not_established`
- `refuted`
- `unresolved`

### Cost relation

- `fara_dominates`
- `grel_dominates`
- `tradeoff`
- `equivalent`
- `incomparable`
- `unresolved`

### Overall interpretation

- `strict_fara_separation`
- `fara_constrained_equivalent`
- `translation_equivalent`
- `generic_baseline_strictly_simpler`
- `incomparable`
- `factorization_failed_for_explicit_reason`
- `unresolved`

No overall interpretation may replace the dimension-level record. Expressive equivalence may coexist with stronger FARA admissibility constraints, a cost tradeoff, and no demonstrated reasoning specificity.

No dimension establishes universality, necessity, or minimality by itself.

## Nonclaims

Freezing `GREL-001` does not establish that:

- it represents `S_core`;
- FARA factors through it;
- it is simpler under a frozen cost preorder;
- generic relational structure is the universal structure of reasoning;
- FARA adds no value;
- one comparison dimension determines another.
