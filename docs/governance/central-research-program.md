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
- `docs/research/s-core-w3-global-witness-proof-v1.0.md`;
- `theory/evaluation/research-gates.json`.

The deduction-first standard controls proof dependencies. Anti-self-validation and replication standards separately control independent-confirmation claims.

## Central research question

> Does every reasoning process necessarily instantiate a common underlying structure, and if so, is that structure both universal and minimal?

This separates common-schema existence, faithful representation, necessity or derivability, minimality, equivalence or uniqueness, and impossibility. These obligations may not be collapsed into one favorable conclusion.

## Frozen boundaries

`THM-TARGET-001` v1.0 freezes `S_core`, `S_IRD`, `A_FARA`, witness `W=(E,D,M,iota,kappa)`, P1-P7, P8-I, P8-E, and the theorem families.

`FAITHFUL-REP-001` freezes materiality, applicability, canonical reducts, target-only recovery, strong typed correspondence, P5 bisimulation, P7 history and path, semantic agreement, coherence, uniformity, composition, machinery accounting, nontriviality, and `Faithful_split`.

`P8-ROLE-001` selects `split`: `Pres_8I` is internal; `Corr_8E` remains a separate actual-process correspondence obligation.

`SCORE-LEMMA-LEDGER-001` freezes 24 construction, 10 obstruction, and 3 assembly obligations. A material change requires a versioned revision.

## Accepted partial proof packages

### W0 — Source normalization

`SCORE-W0-PROOF-001` proves `LEM-SC-001` through `LEM-SC-004` and establishes `OBS-SC-001` as a source boundary.

### W1 — Target allocation and direct axes

`SCORE-W1-PROOF-001` proves `LEM-SC-005` through `LEM-SC-009`, `LEM-SC-012`, and `LEM-SC-014`; it refutes `OBS-SC-003` and `OBS-SC-006`.

### W2 — Dynamics, history, revision, and rule versions

`SCORE-W2-PROOF-001` proves `LEM-SC-010`, `LEM-SC-011`, `LEM-SC-013`, `LEM-SC-015`, and `LEM-SC-016`; it refutes `OBS-SC-004` and `OBS-SC-005`.

### W3 — Global witness construction

`SCORE-W3-PROOF-001` proves:

- `LEM-SC-017` distributed decomposition and interface construction;
- `LEM-SC-018` deterministic terminating target-only recovery;
- `LEM-SC-019` semantic agreement;
- `LEM-SC-020` cross-axis coherence;
- `LEM-SC-021` complete machinery accounting;
- `LEM-SC-022` uniformity and source-isomorphism equivariance;
- `LEM-SC-023` compositional accountability;
- `LEM-SC-024` well-formed witness assembly.

It refutes `OBS-SC-002`, `OBS-SC-007`, `OBS-SC-008`, and `OBS-SC-009` over their registered finite scopes.

W3 uses the frozen FARA interface and adds no primitive. It proves all registered finite construction obligations. It does not prove the formal negative-control family, `Nontrivial`, `Faithful_split`, or a theorem.

## Current active stage

Current ledger state:

- total obligations: 37;
- proved construction lemmas: 24;
- source-scope boundaries established: 1;
- refuted obstruction hypotheses: 8;
- open obligations: 4;
- completed waves: W0 through W3;
- active wave: W4.

The active obligation is `OBS-SC-010`, the formal NC-01 through NC-10 family. W5 remains open with `ASM-SC-001` through `ASM-SC-003`.

The scoped-representation-proof, mechanized-proof-verification, and independent-proof-review gates remain unsatisfied.

## W4 proof requirements

Each negative control must be rejected by a frozen formal clause rather than by evaluator preference, source reaccess, case-specific repair, or a newly invented restriction. The package must:

- instantiate NC-01 through NC-10 against the completed W3 witness class;
- identify the exact violated preservation, recovery, semantics, coherence, uniformity, composition, or machinery clause;
- prove that the violation is structural for the registered control family;
- preserve any valid countermodel or hidden commitment;
- avoid modifying the frozen faithful predicate to force failure.

A successful W4 package may establish the global `Nontrivial` conjunct. It still does not itself assemble the theorem.

## Primary deductive method

1. preserve the frozen theorem, source, target, semantic, and P8 boundaries;
2. execute the lemma ledger in dependency order;
3. search concurrently for countermodels and obstructions;
4. resolve W4 formal negative controls;
5. assemble the strongest finite-core result in W5;
6. attempt extension to `S_IRD` only after the finite-core result;
7. address necessity, lower bounds, minimality, equivalence, uniqueness, or impossibility;
8. mechanize the largest sound fragment;
9. obtain independent proof review and adversarial counterexample search.

## Proof-status discipline

The following dimensions remain separate:

- project-authored human-checkable proof;
- bounded executable corroboration;
- proof-assistant verification;
- independent proof review.

No lower status may be reported as a higher one. Partial lemma packages do not satisfy the scoped-representation-proof gate. A result over `S_core` may not be reported as a result over `S_IRD`.

## Evidence hierarchy

For mathematical claims, machine-checked proof outranks complete human proof, which outranks partial lemmas and formal countermodels, bounded exhaustive results, executable conformance, experiments, and informal arguments. Lower-ranked evidence may challenge or motivate proof work but may not substitute for it.

## Counterexample policy

Potential counterexamples are primary research objects. Each must be classified as a formal countermodel, impossibility witness, representation failure, interpretation dispute, scope-boundary case, non-reasoning process, inconclusive case, or successful representation. Scope may not be changed after exposure without a versioned and independently defended revision.

## Supporting empirical work

PBTS-001 replication, comparative representation, boundary discovery, bounded model search, and implementation validation continue as parallel supporting tracks. They are not theorem premises.

## Current nonclaims

The repository does not establish:

- `OBS-SC-010` or the global `Nontrivial` conjunct;
- `Faithful_split` satisfiability;
- any W5 assembly obligation;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- actual-process correspondence;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review of W0-W3.

## Immediate central task

Execute the W4 formal negative-control package. W5 theorem assembly remains blocked until `OBS-SC-010` closes.
