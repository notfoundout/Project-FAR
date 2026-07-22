# USD-W1 Infinite-Carriers Extension Proof v1.0

## Status

Complete bounded deductive extension for `S_inf_eff`.

## Frozen source class

`S_inf_eff` contains countably infinite reasoning systems whose carrier, transition, admissibility, observation, commitment, ground, dependency, and finite-prefix relations have one uniform effective presentation. Admission is independent of FARA and of any proposed universal kernel.

Uncountable carriers, non-effective countable presentations, undeclared oracles, noncomputable transition or admissibility relations, semantic change, and actual-process correspondence are outside this version.

## Construction

Let a source object provide an effective enumeration `e : N -> X`, a computable admissibility relation, a computable transition schema, and finite-support commitment and dependency data at each generated stage.

Construct a target object by:

1. representing each generated source state `e(n)` as an indexed target state object;
2. representing admissibility and transition by one target transition schema parameterized by the source index;
3. representing commitments, grounds, and dependencies at each stage without completing or truncating the infinite carrier;
4. representing history as a directed family of finite prefixes;
5. requiring the embedding maps between prefixes to commute with transition, commitment, dependency, and revision structure;
6. using one uniform recovery map for every finite prefix.

No new target primitive is introduced. Effective enumeration and prefix coherence are derived machinery and are counted explicitly.

## Obligations

### `INF-EXT-001` — Uniform effective constructor

The same constructor consumes the declared effective source interface for every member of `S_inf_eff`. It does not inspect case identity or use source-specific repair.

### `INF-EXT-002` — Finite-prefix faithfulness

For every natural-number bound `n`, the target prefix through `n` faithfully represents the corresponding source prefix. Recovery commutes with prefix inclusion.

### `INF-EXT-003` — Transition and admissibility preservation

A source transition or admissibility judgment holds at a generated stage exactly when its represented target judgment holds at that stage.

### `INF-EXT-004` — Commitment, ground, and dependency preservation

Every finite-support commitment active in a source prefix retains its semantics, grounds, and dependency edges in the corresponding target prefix.

### `INF-EXT-005` — History and revision coherence

Later prefixes extend earlier prefixes without rewriting prior source history. Revisions remain distinct from ordinary transitions and preserve their exact dependency points.

### `INF-EXT-006` — No finite truncation disguised as totality

A construction that chooses a fixed finite cutoff fails. The proof requires a coherent representation for every finite prefix under one unbounded constructor.

### `INF-EXT-007` — No oracle or decoder smuggling

The constructor and recovery map may use only the frozen effective interface. An undeclared oracle, unrestricted interpreter, or source-specific decoder is a failure.

### `INF-EXT-008` — Registered controls

The natural-number, infinite-tree, and unbounded-prefix fixtures pass. The truncation and oracle controls are rejected. The noncomputable fixture remains an explicit scope boundary rather than being silently repaired.

## Result

For every source object in `S_inf_eff`, there exists a target object in the frozen theorem-facing FARA class and a coherent family of witnesses satisfying the registered preservation obligations on every finite prefix.

The terminal classification is `proper_subclass_only`.

This establishes neither completed-infinite semantics for arbitrary systems nor representation of all infinite carriers. It does not establish `S_IRD` representation, universal structure, necessity, minimality, uniqueness, actual-process correspondence, mechanized verification, or independent review.
