# Deduction-First Proof Roadmap

## Purpose

This roadmap defines the primary deductive path for Project FAR. It permits favorable, unfavorable, bounded, and unresolved outcomes.

Independent empirical replication is a parallel supporting track, not a premise of the representation theorem.

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
W4 remaining obstructions and negative controls
        ↓
W5 theorem-or-obstruction assembly
        ↓
lower bounds and necessity
        ↓
minimality, equivalence, uniqueness, or impossibility
        ↓
mechanization
        ↓
independent proof review
```

## Stage D1 — Theorem target

**Status:** complete prospectively through `THM-TARGET-001` v1.0.

The target separates `S_core`, `S_IRD`, `A_FARA`, the witness signature, preservation obligations, P8 correspondence, and the theorem families. Freezing the target does not prove it satisfiable.

## Stage D2 — Premises and semantics

**Status:** complete prospectively through premise ledger v1.5, `FAITHFUL-REP-001`, and `P8-ROLE-001`.

The premise ledger records W0 through W2 proof progress without adding an axiom, changing source scope, changing the target interface, or promoting a theorem.

No premise asserts FARA adequacy, PB-001 completeness, primitive necessity, or universal reasoning structure.

## Stage D3 — Faithful representation

**Status:** definition frozen; global satisfiability unproved.

The specification fixes materiality, applicability, canonical reducts, target-only recovery, total typed strong embeddings, relation preservation and reflection, P5 bisimulation, P7 history and path requirements, semantic agreement, coherence, uniformity, composition, machinery accounting, nontriviality, and `Faithful_split`.

W0 proves source-side normalization. W1 proves finite direct-axis target structures and strong embeddings. W2 proves finite deterministic and probabilistic dynamics, history, revision, and operational rule-version constructions. Recovery and complete `Pres_i` predicates remain unproved.

## Stage D3.5 — P8 role

**Status:** complete prospectively; selected mode `split`.

`Pres_8I` is internal to `Faithful_split`; `Corr_8E` remains a separate actual-process correspondence obligation.

W1 proves the direct-axis P8-I embedding and no-upgrade property. Admissible recovery and external correspondence remain unproved.

## Stage D4 — Construction and obstruction lemmas

**Status:** active.

The frozen ledger contains 37 obligations: 24 construction, 10 obstruction, and 3 assembly.

Current execution state:

- proved construction lemmas: 16;
- established source-scope boundaries: 1;
- refuted obstruction hypotheses: 4;
- open obligations: 16;
- completed waves: W0, W1, and W2;
- active wave: W3.

### W0 — Source normalization — complete

`SCORE-W0-PROOF-001` proves `LEM-SC-001` through `LEM-SC-004` and establishes `OBS-SC-001` as a source boundary.

### W1 — Target allocation and direct axes — complete

`SCORE-W1-PROOF-001` proves `LEM-SC-005` through `LEM-SC-009`, `LEM-SC-012`, and `LEM-SC-014`. It refutes `OBS-SC-003` and `OBS-SC-006` over their registered finite scopes.

### W2 — Dynamics, history, and revision — complete

`SCORE-W2-PROOF-001` proves:

- `LEM-SC-010` deterministic finite labeled bisimulation;
- `LEM-SC-011` finite-support probabilistic bisimulation;
- `LEM-SC-013` historical-and-path order embedding;
- `LEM-SC-015` nonmonotonic revision and retraction;
- `LEM-SC-016` self-modification and rule-version change.

It refutes `OBS-SC-004` and `OBS-SC-005` over their registered finite explicit scopes.

The fixed `DYN-HISTORY-1.0` construction copies complete material transition metadata, finite support and weights, history order, provenance, revision snapshots, active rule versions, accepted and rejected modifications, dependency ancestry, and path conditions. Rule change is operational rather than label-only.

### W3 — Global witness obligations — active

Resolve:

- `LEM-SC-017` distributed decomposition and interface construction;
- `LEM-SC-018` admissible target-only recovery;
- `LEM-SC-019` semantic agreement;
- `LEM-SC-020` cross-axis coherence;
- `LEM-SC-021` complete machinery-ledger construction;
- `LEM-SC-022` uniformity and source-isomorphism equivariance;
- `LEM-SC-023` compositional accountability;
- `LEM-SC-024` well-formed witness assembly.

Success requires one fixed target-only recovery family, source-declared semantic equivalence, compatible shared identities, complete helper accounting, no case database or hidden interpreter, source-isomorphism equivariance, declared interface preservation, and a well-typed witness.

### W4 — Remaining obstructions and negative controls — open

Resolve `OBS-SC-002`, `OBS-SC-007`, `OBS-SC-008`, `OBS-SC-009`, and `OBS-SC-010`, including NC-01 through NC-10.

A failed implementation is not a theorem-level obstruction without quantification over the registered class.

### W5 — Assembly — open

`ASM-SC-001` through `ASM-SC-003` remain blocked. Assembly may conclude a scoped theorem, formal countermodel, proper-subclass theorem, impossibility result, or explicit unresolved result.

**D4 exit condition:** every mandatory feature has an accepted construction or quantified negative result, and `ASM-SC-003` records the strongest justified outcome.

## Stage D5 — Scoped representation theorem

**Status:** blocked by 16 open obligations.

The first theorem attempts are `THM-CORE-COMMON-001`, `THM-CORE-REP-001`, and `THM-IMP-001`. `THM-IRD-EXT-001` remains blocked until the finite-core result is resolved.

A partial lemma package cannot satisfy this stage.

## Stage D6 — Primitive independence and lower bounds

After a stable representation result, define the reconstruction class and prove each retained commitment indispensable, derivable, replaceable, assumption-dependent, unnecessary, or unresolved.

Finite ablation failure alone is not a necessity proof.

## Stage D7 — Minimality and equivalence

Define a candidate universe, equivalence relation, and cost preorder before using “minimal.” Then establish local or global lower bounds, equivalence classes, uniqueness, incomparable minima, no minimum, or impossibility.

## Stage D8 — Mechanization

Encode frozen definitions, assumptions, proved lemmas, unresolved obligations, and theorem chains in a proof assistant or verified formal system.

Distinguish trusted kernel assumptions, Project FAR axioms, executable definitions, proved lemmas, and admitted obligations.

The W0, W1, and W2 Python references are bounded corroboration, not proof-assistant verification.

## Stage D9 — Independent proof review

Qualified reviewers should reconstruct the proofs, challenge scope and assumptions, search for countermodels, inspect mechanized artifacts, and test whether conclusions exceed the derivations.

W0, W1, and W2 are project-authored and not independently reviewed.

## Parallel empirical track

PBTS-001 replication, comparative experiments, boundary discovery, and application tests remain useful for finding ambiguity, counterexamples, or implementation defects. They may not substitute for D1–D8.

## Immediate next artifacts

1. Produce the W3 proof-or-obstruction package for `LEM-SC-017` through `LEM-SC-024`.
2. Register recovery-oracle, semantic-strengthening, identity-conflict, hidden-machinery, nonuniformity, and composition-interface adversarial fixtures.
3. Execute the remaining W4 obligations as W3 dependencies close.
4. Preserve every unresolved dependency and nonclaim.
5. Do not begin theorem assembly while a required obligation remains open.

## Current nonclaims

This roadmap does not establish:

- admissible target-only recovery;
- any complete `Pres_i` predicate;
- `Faithful_split` satisfiability;
- a common-schema or representation theorem;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency or completeness;
- primitive necessity or minimality;
- universality, equivalence, uniqueness, or impossibility;
- proof-assistant verification or independent review of W0, W1, or W2.
