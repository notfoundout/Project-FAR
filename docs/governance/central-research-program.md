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

`SCORE-W0-PROOF-001` proves:

- `LEM-SC-001` finite source-contract normalization;
- `LEM-SC-002` canonical reduct extraction;
- `LEM-SC-003` materiality closure and applicability decidability;
- `LEM-SC-004` source-isomorphism transport.

It establishes `OBS-SC-001` as a source-scope boundary: genuinely non-finite material closure is outside frozen `S_core`.

### W1 — Target allocation and direct axes

`SCORE-W1-PROOF-001` proves:

- `LEM-SC-005` target carrier allocation;
- `LEM-SC-006` P1 configuration construction;
- `LEM-SC-007` P2 commitment construction;
- `LEM-SC-008` P3 stake-and-alternative construction;
- `LEM-SC-009` P4 ground-and-justification construction;
- `LEM-SC-012` P6 consequence construction;
- `LEM-SC-014` P8-I internal evidential-status construction.

It refutes the registered direct-axis impossibility hypotheses `OBS-SC-003` and `OBS-SC-006` by one fixed finite incidence construction.

The W1 construction uses existing FARA categories and adds no primitive. Source-specific roles, sorts, values, and denotations enter as explicit target data. Objects and representations remain distinct.

W1 proves direct-axis strong embeddings. It does not prove target-only recovery or any complete `Pres_i` predicate.

## Current active stage

Current ledger state:

- total obligations: 37;
- proved construction lemmas: 11;
- source-scope boundaries established: 1;
- refuted obstruction hypotheses: 2;
- open obligations: 23;
- completed waves: W0 and W1;
- active wave: W2.

The active obligations are:

- `LEM-SC-010` deterministic dynamics;
- `LEM-SC-011` finite-support probabilistic dynamics;
- `LEM-SC-013` history and path;
- `LEM-SC-015` nonmonotonic revision and retraction;
- `LEM-SC-016` self-modification and rule-version change.

`OBS-SC-004` and `OBS-SC-005` are executed as their dependencies close.

The scoped-representation-proof, mechanized-proof-verification, and independent-proof-review gates remain unsatisfied.

## W2 proof requirements

The W2 package must preserve and reflect operational behavior rather than merely store labels.

For deterministic dynamics it must establish finite labeled bisimulation, including preconditions, resources, actions, observations, rule identity, rule version, and admissibility.

For finite-support stochastic dynamics it must preserve exact source probabilities or source-declared weight equivalence and establish the registered probabilistic bisimulation.

For history it must provide an order embedding preserving and reflecting provenance, dependency ancestry, revision, retraction, supersession, activation, rejection, and material path conditions.

For nonmonotonic revision it must retain earlier and later commitment states rather than replacing history with current output.

For self-modification it must show that accepted, rejected, and superseded rule changes alter later admissible transitions at the exact source position.

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

A proof assistant can verify only the encoded theorem under its trusted assumptions. Executable W0 and W1 reference implementations are corroboration, not proof-assistant verification.

## Current nonclaims

The repository does not establish:

- admissible target-only recovery;
- any complete `Pres_i` predicate;
- `Faithful_split` satisfiability;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- actual-process correspondence;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review of W0 or W1.

## Immediate central task

Execute the W2 dynamics, history, revision, and self-modification proof-or-obstruction package. Independent empirical work remains parallel and nonblocking.
