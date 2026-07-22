# S_core W5 Theorem Assembly Proof v1.0

## Status

Bounded deductive proof package for the frozen finite explicit source class `S_core` and the frozen theorem-facing target class `A_FARA`.

This package proves the registered W5 assembly obligations `ASM-SC-001`, `ASM-SC-002`, and `ASM-SC-003` by composition of the already proved W0-W4 obligations. It does not establish representation of `S_IRD`, correspondence to actual processes, primitive necessity, minimality, uniqueness, reasoning specificity, or universal structure.

## Frozen dependencies

The proof imports without modification:

- `LEM-SC-001` through `LEM-SC-024`;
- the terminal obstruction adjudications `OBS-SC-001` through `OBS-SC-010`;
- `FAITHFUL-REP-001` with P8 mode `split`;
- the W3.5 result that FARA is not unique or reasoning-specific at the registered comparative scope.

No new premise, source restriction, target primitive, recovery oracle, hidden interpreter, or source-specific decoder is introduced.

## ASM-SC-001 — Common schema existence

For every `(P,J)` in `S_core`, `LEM-SC-005` allocates the fixed theorem-facing carrier interface, `LEM-SC-018` supplies admissible target-only recovery, `LEM-SC-021` supplies the complete machinery ledger, `LEM-SC-022` establishes one uniform source-isomorphism-equivariant constructor, and `LEM-SC-024` assembles a well-formed witness.

Therefore one fixed `A_FARA` interface schema and one uniform construction method assign an eligible target package and witness to every source object in `S_core`.

Hence `THM-CORE-COMMON-001` is proved at the frozen `S_core` scope.

## ASM-SC-002 — Finite-core faithful representation

Fix an arbitrary `(P,J)` in `S_core`. The W1-W3 lemmas provide typed strong embeddings and target-only recovery for every material preservation axis:

- configuration, commitment, stakes, alternatives, grounds, and consequences;
- deterministic and finite-support probabilistic admissible dynamics;
- material history, path, revision, retraction, supersession, and rule-version change;
- internal provenance and evidential status under P8 split mode;
- semantic agreement, cross-axis coherence, uniformity, composition, and complete machinery accounting.

`LEM-SC-024` combines these components into a witness `W=(E,D,M,iota,kappa)`. The W4 family proof establishes that the frozen nontriviality clauses are substantive by rejecting each applicable registered negative-control family; it does not add a new positive premise.

Consequently the assembled witness satisfies `Faithful_split(P,J,A,W)`. Since `(P,J)` was arbitrary,

`forall (P,J) in S_core, exists A in A_FARA, exists W, Faithful_split(P,J,A,W)`.

Hence `THM-CORE-REP-001` is proved at the frozen finite explicit scope.

## ASM-SC-003 — Theorem-family adjudication

From `ASM-SC-001` and `ASM-SC-002`:

- `THM-CORE-COMMON-001` is proved;
- `THM-CORE-REP-001` is proved;
- the `S_core` branch of `THM-IMP-001` is refuted under the frozen definitions because a finite, uniform, nontrivial witness exists for every in-scope source object.

The following remain open or blocked:

- `THM-IRD-EXT-001` for `S_IRD`;
- `THM-P8-CORR-001` for actual-process correspondence;
- primitive necessity or derivability;
- minimality;
- equivalence or uniqueness;
- universal structure and reasoning specificity.

## Proof character

This is a bounded deductive assembly over frozen definitions and previously established proof packages. Repository checkers provide executable reference corroboration. Proof-assistant mechanization and independent proof review remain separate unsatisfied gates.
