# Deduction-First Proof Roadmap

## Purpose

This roadmap defines the primary deductive path for Project FAR. It permits favorable, unfavorable, bounded, and unresolved outcomes. Independent empirical replication is a parallel supporting track, not a premise of the representation theorem.

## Dependency graph

```text
source class and theorem scope
        ↓
formal semantics and premises
        ↓
faithful-representation definition and P8 split
        ↓
W0 source normalization
        ↓
W1 target allocation and direct axes
        ↓
W2 dynamics, history, revision, self-modification
        ↓
W3 recovery, semantics, coherence, machinery, composition
        ↓
W4 formal negative controls
        ↓
W5 theorem-or-obstruction assembly
        ↓
S_IRD extension
        ↓
lower bounds, necessity, minimality, equivalence, or impossibility
        ↓
mechanization
        ↓
independent proof review
```

## Stage D1 — Theorem target

**Status:** complete prospectively through `THM-TARGET-001` v1.0.

The target separates `S_core`, `S_IRD`, `A_FARA`, the witness signature, preservation obligations, P8 correspondence, and theorem families. Freezing the target does not prove it satisfiable.

## Stage D2 — Premises and semantics

**Status:** complete prospectively through premise ledger v1.6, `FAITHFUL-REP-001`, and `P8-ROLE-001`.

The premise ledger records W0-W3 progress without adding an axiom, changing source scope, changing the target interface, or promoting a theorem.

## Stage D3 — Faithful representation

**Status:** definition frozen; all finite construction and recovery conjuncts proved; global `Nontrivial` and theorem satisfiability unproved.

W0 proves source normalization. W1 proves direct-axis embeddings. W2 proves dynamics and history. W3 proves target-only recovery, semantic agreement, cross-axis coherence, complete machinery accounting, uniformity, composition, and typed witness assembly.

## Stage D3.5 — P8 role

**Status:** complete prospectively; selected mode `split`.

Finite P8-I construction and target-only recovery are proved. `Corr_8E` remains separate and unproved.

## Stage D4 — Construction and obstruction lemmas

**Status:** active, with only formal negative controls unresolved.

The frozen ledger contains 37 obligations: 24 construction, 10 obstruction, and 3 assembly.

Current execution state:

- proved construction lemmas: 24;
- established source-scope boundaries: 1;
- refuted obstruction hypotheses: 8;
- open obligations: 4;
- completed waves: W0 through W3;
- active wave: W4.

### W0 — Source normalization — complete

`SCORE-W0-PROOF-001` proves `LEM-SC-001` through `LEM-SC-004` and establishes `OBS-SC-001` as a source boundary.

### W1 — Target allocation and direct axes — complete

`SCORE-W1-PROOF-001` proves the registered direct-axis construction lemmas and refutes `OBS-SC-003` and `OBS-SC-006`.

### W2 — Dynamics, history, and revision — complete

`SCORE-W2-PROOF-001` proves deterministic and probabilistic dynamics, history, revision, and operational rule-version change; it refutes `OBS-SC-004` and `OBS-SC-005`.

### W3 — Global witness obligations — complete

`SCORE-W3-PROOF-001` proves `LEM-SC-017` through `LEM-SC-024` and refutes `OBS-SC-002`, `OBS-SC-007`, `OBS-SC-008`, and `OBS-SC-009`.

The result includes one fixed finite target interface, deterministic target-only recovery, semantic agreement, coherent shared identities, a complete acyclic machinery ledger, source-isomorphism equivariance, source-declared composition, and typed witness assembly.

### W4 — Formal negative controls — active

Resolve `OBS-SC-010` by proving that NC-01 through NC-10 fail for their registered structural reasons, or preserve any valid countermodel or hidden commitment.

A failed test instance is not enough. The result must quantify over each frozen control family and identify the exact violated clause.

### W5 — Assembly — open

`ASM-SC-001` through `ASM-SC-003` remain blocked by `OBS-SC-010`. Assembly may conclude a scoped theorem, formal countermodel, proper-subclass theorem, impossibility result, or explicit unresolved result.

**D4 exit condition:** `OBS-SC-010` is resolved without changing the frozen representation definition.

## Stage D5 — Scoped representation theorem

**Status:** blocked by four open obligations.

After W4, assemble `ASM-SC-001` through `ASM-SC-003` and derive the strongest justified result for `THM-CORE-COMMON-001`, `THM-CORE-REP-001`, or `THM-IMP-001`.

A partial lemma package cannot satisfy this stage.

## Stage D6 — S_IRD extension

Attempt extension only after the finite-core result. Infinite carriers, continuous dynamics, partial observability, open-ended histories, semantic change, non-finite-support stochasticity, and unresolved external correspondence remain separate obligations.

## Stage D7 — Primitive independence and lower bounds

After a stable representation result, define the reconstruction class and prove each retained commitment indispensable, derivable, replaceable, assumption-dependent, unnecessary, or unresolved.

## Stage D8 — Minimality and equivalence

Define a candidate universe, equivalence relation, and cost preorder before using “minimal.” Then establish lower bounds, equivalence classes, uniqueness, incomparable minima, no minimum, or impossibility.

## Stage D9 — Mechanization

Encode frozen definitions, assumptions, proofs, unresolved obligations, and theorem chains in a proof assistant or verified formal system. W0-W3 Python references remain bounded corroboration, not proof-assistant verification.

## Stage D10 — Independent proof review

Qualified reviewers should reconstruct the proofs, challenge scope and assumptions, inspect mechanized artifacts, and search for countermodels.

## Immediate next artifacts

1. Produce the W4 formal negative-control package for NC-01 through NC-10.
2. Preserve every valid failure, countermodel, hidden commitment, and nonclaim.
3. Do not change the frozen faithful predicate to force a pass.
4. Do not begin W5 assembly until `OBS-SC-010` is resolved.

## Current nonclaims

This roadmap does not establish:

- the formal negative-control family or global `Nontrivial`;
- `Faithful_split` satisfiability;
- a common-schema or representation theorem;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency or completeness;
- primitive necessity or minimality;
- universality, equivalence, uniqueness, or impossibility;
- proof-assistant verification or independent review of W0-W3.
