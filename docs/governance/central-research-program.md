# Central Research Program

## Purpose

Project FAR exists to determine whether there is a universal and minimal structure underlying reasoning.

This program governs the primary research direction. Infrastructure, implementations, experiments, and applications support the central question but may not replace it.

It does not introduce a new primitive, accept a representation theorem, revise Foundation v1.0, or declare FAR correct.

## Governing standards and artifacts

The active program is controlled by:

- `docs/governance/deduction-first-research-standard.md`;
- `docs/governance/anti-self-validation-standard.md`;
- `docs/governance/anti-self-validation-deduction-clarification.md`;
- `docs/governance/evidence-replication-and-freeze-standard-v1.0.md`;
- `docs/research/thm-target-001-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/research/s-core-construction-obstruction-ledger-v1.0.md`;
- `docs/research/s-core-w0-normalization-proof-v1.0.md`;
- `docs/research/s-core-w1-direct-axis-proof-v1.0.md`;
- `docs/research/s-core-w2-dynamics-history-proof-v1.0.md`;
- `theory/evaluation/research-gates.json`.

The deduction-first standard controls proof dependencies. Anti-self-validation and replication standards separately control independent-confirmation claims.

## Central research question

> Does every reasoning process necessarily instantiate a common underlying structure, and if so, is that structure both universal and minimal?

This separates at least six obligations:

1. common-schema existence;
2. faithful representation within a formally justified source class;
3. necessity or derivability of retained commitments;
4. minimality within a declared candidate universe;
5. equivalence, uniqueness, or incomparability;
6. impossibility under stated assumptions.

These obligations may not be collapsed into one favorable conclusion.

## Research position

The existence of a universal reasoning structure is an open hypothesis. Project FAR does not assume that such a structure exists or that FAR or FARA is that structure.

A proof, countermodel, proper-subclass theorem, equivalence result, no-go theorem, or unresolved result is an admissible central outcome. No artifact is protected from criticism because it supports the current framework.

## Frozen boundaries

`THM-TARGET-001` v1.0 freezes:

- `S_core`, the first finite explicit source class;
- `S_IRD`, the broader extension target;
- the theorem-facing target class `A_FARA`;
- witness `W=(E,D,M,iota,kappa)`;
- P1–P7 and P8-I preservation obligations;
- the separate P8-E correspondence family;
- common-schema, representation, extension, necessity, minimality, equivalence, and impossibility theorem families.

`FAITHFUL-REP-001` freezes materiality, applicability, canonical reducts, strong typed correspondence, target-only recovery, P5 bisimulation, P7 history and path requirements, semantic agreement, coherence, uniformity, composition, machinery accounting, nontriviality, and `Faithful_split`.

`P8-ROLE-001` selects `split`: `Pres_8I` remains internal, while `Corr_8E` remains a separate actual-process correspondence obligation.

`SCORE-LEMMA-LEDGER-001` registers 24 construction, 10 obstruction, and 3 assembly obligations. Its statements and dependency graph remain frozen.

A material change to source scope, target interface, faithful predicate, P8 boundary, lemma statement, quantified obstruction, or theorem family requires a versioned revision.

## Accepted partial proof packages

### W0 — Source normalization

`SCORE-W0-PROOF-001` proves `LEM-SC-001` through `LEM-SC-004` and establishes `OBS-SC-001` as a source-scope boundary. Genuinely non-finite material closure is outside frozen `S_core`.

### W1 — Target allocation and direct axes

`SCORE-W1-PROOF-001` proves:

- `LEM-SC-005` target carrier allocation;
- `LEM-SC-006` P1 configuration construction;
- `LEM-SC-007` P2 commitment construction;
- `LEM-SC-008` P3 stake-and-alternative construction;
- `LEM-SC-009` P4 ground-and-justification construction;
- `LEM-SC-012` P6 consequence construction;
- `LEM-SC-014` P8-I internal evidential-status construction.

It refutes `OBS-SC-003` and `OBS-SC-006` over their registered finite scopes. It uses existing FARA categories and adds no primitive.

### W2 — Dynamics, history, revision, and self-modification

`SCORE-W2-PROOF-001` proves:

- `LEM-SC-010` deterministic dynamics construction;
- `LEM-SC-011` finite-support probabilistic dynamics construction;
- `LEM-SC-013` historical-and-path construction;
- `LEM-SC-015` nonmonotonic revision and retraction;
- `LEM-SC-016` self-modification and rule-version change.

It refutes:

- `OBS-SC-004` dynamics-bisimulation mismatch;
- `OBS-SC-005` history-and-path collapse.

The fixed `DYN-HISTORY-1.0` schema copies finite transition records, exact finite-support weights, state-indexed active rule versions, material event order, revision snapshots, rule modifications, ancestry, and path conditions. Accepted rule changes alter later live transitions; rejected changes do not. No new FARA primitive is added.

W1 and W2 prove finite target constructions and strong embeddings. They do not prove target-only recovery or any complete `Pres_i` predicate.

## Current active stage

Current ledger state:

- total obligations: 37;
- proved construction lemmas: 16;
- source-scope boundaries established: 1;
- refuted obstruction hypotheses: 4;
- open obligations: 16;
- completed waves: W0, W1, and W2;
- active wave: W3.

The active obligations are:

- `LEM-SC-017` distributed decomposition and interface construction;
- `LEM-SC-018` admissible target-only recovery;
- `LEM-SC-019` semantic agreement;
- `LEM-SC-020` cross-axis coherence;
- `LEM-SC-021` complete machinery-ledger construction;
- `LEM-SC-022` uniformity and source-isomorphism equivariance;
- `LEM-SC-023` compositional accountability;
- `LEM-SC-024` well-formed witness assembly.

The scoped-representation-proof, mechanized-proof-verification, and independent-proof-review gates remain unsatisfied.

## W3 proof requirements

The W3 package must close the difference between successful per-axis constructions and one admissible faithful witness.

Recovery must:

- accept target data, registered witness metadata, and an axis query only;
- terminate deterministically on every finite theorem-facing package;
- use no source object, source identifier, evaluator repair, unrestricted interpreter, network resource, or case database;
- return exactly the recovered reduct or an explicit failure diagnostic.

Semantic agreement must use source-declared denotational equivalence and must not strengthen precision, certainty, modality, normativity, authority, or evidential grade.

Cross-axis coherence must reuse or explicitly link shared identities and prohibit contradictory commitment, version, provenance, or consequence data.

The machinery ledger must count every schema, algorithm, field, bridge, helper, metadata item, and dependency used by construction, recovery, interpretation, or verification.

Uniformity must establish one finite source-isomorphism-equivariant constructor family with no case-identifier branching or unbounded helper family.

Compositional accountability must preserve declared interfaces, cross-component relations, histories, and admissibility conditions, and restriction must commute with encoding up to the declared target equivalence.

Witness assembly must produce a well-formed `W=(E,D,M,iota,kappa)` without assuming `Faithful_split` or the theorem conclusion.

## Primary deductive method

1. preserve the frozen theorem, source, target, semantic, and P8 boundaries;
2. execute the lemma ledger in dependency order;
3. search concurrently for quantified countermodels and obstructions;
4. assemble the strongest finite-core result only after dependencies close;
5. attempt extension to `S_IRD` only after the finite-core result;
6. then address necessity, lower bounds, minimality, equivalence, uniqueness, or impossibility;
7. mechanize the largest sound fragment;
8. obtain independent proof review and adversarial counterexample search.

The canonical detailed sequence is `docs/planning/deduction-first-proof-roadmap.md`.

## Proof-status discipline

Every proof artifact must state its identifier, version, exact statement, quantified scope, assumptions, dependencies, result status, countermodels, machine-check status, independent-review status, consequences, and stronger nonclaims.

The following dimensions are separate:

- **project-authored human-checkable proof**: a complete written derivation registered internally;
- **bounded executable corroboration**: finite implementations and adversarial fixtures test the construction;
- **proof-assistant verification**: a formal encoding checked by a trusted kernel;
- **independent proof review**: qualified external reconstruction or challenge.

No lower status may be reported as a higher one. Partial lemma packages do not satisfy the scoped-representation-proof gate.

A proof over `S_core` may not be reported as a proof over `S_IRD`. A failed witness is not an impossibility theorem unless nonexistence is proved over the registered class.

## Evidence hierarchy

For mathematical claims:

1. machine-checked proof from frozen assumptions;
2. complete human-checkable proof;
3. partial proof, lemma, lower bound, or formal countermodel;
4. exhaustive result over a fully defined finite universe;
5. bounded executable conformance or model checking;
6. comparative experiment or independently replicated evaluation;
7. informal argument or intuition.

Lower-ranked evidence may motivate or challenge proof work but may not be described as logically equivalent to proof.

## Counterexample policy

Potential counterexamples are primary research objects. Each must be classified as a formal countermodel, impossibility witness, representation failure, interpretation dispute, scope-boundary case, non-reasoning process, inconclusive case, or successful representation.

A candidate may not be excluded by redefining reasoning after exposure. Scope restrictions must be versioned and defended independently.

## Supporting empirical work

PBTS-001 replication, comparative representation, boundary discovery, bounded model search, and implementation validation continue as parallel supporting tracks. They may expose ambiguity, implementation defects, hidden assumptions, or counterexamples.

They are not logical premises of the theorem. Independent replication gates only independent empirical-confirmation claims.

## Theory revision and mechanization

Protected theory may not be silently changed to rescue a proof. Any substantive change creates the applicable new version and preserves earlier failures.

A proof assistant can verify only the encoded theorem under its trusted assumptions. Executable W0, W1, and W2 reference implementations are corroboration, not proof-assistant verification.

## Current nonclaims

The repository does not establish:

- admissible target-only recovery;
- any complete `Pres_i` predicate;
- `Faithful_split` satisfiability;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- actual-process correspondence;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review of W0, W1, or W2.

## Immediate central task

Execute the W3 global-witness proof-or-obstruction package. Independent empirical work remains parallel and nonblocking.
