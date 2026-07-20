# Central Research Program

## Purpose

Project FAR exists to determine whether there is a universal and minimal structure underlying reasoning.

This program governs the primary research direction. Infrastructure, implementations, experiments, and applications support the central question but may not replace it.

The project does not assume that a universal structure exists, that FARA is that structure, or that faithful representation establishes reasoning-specific structure.

## Governing standards and artifacts

The active program is controlled by:

- `docs/governance/deduction-first-research-standard.md`;
- `docs/governance/anti-self-validation-standard.md`;
- `docs/governance/anti-self-validation-deduction-clarification.md`;
- `docs/governance/evidence-replication-and-freeze-standard-v1.0.md`;
- `docs/governance/representation-discovery-separation-standard-v1.0.md`;
- `docs/research/thm-target-001-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/research/s-core-construction-obstruction-ledger-v1.0.md`;
- `docs/research/s-core-w0-normalization-proof-v1.0.md`;
- `docs/research/s-core-w1-direct-axis-proof-v1.0.md`;
- `docs/research/s-core-w2-dynamics-history-proof-v1.0.md`;
- `docs/research/s-core-w3-global-witness-proof-v1.0.md`;
- `docs/research/generic-relational-baseline-v1.0.md`;
- `docs/research/reasoning-and-contrast-scope-v1.0.md`;
- `docs/research/universal-structure-discovery-target-v1.0.md`;
- `docs/research/w3-5-specificity-and-discovery-gate-v1.0.md`;
- `theory/evaluation/research-gates.json`.

## Central research question

> Does every reasoning process necessarily instantiate a common underlying structure, and if so, is that structure both universal and minimal?

This separates finite representation capacity, faithful representation, representation-independent common structure, reasoning-specificity, necessity, minimality, equivalence, uniqueness, and impossibility. These obligations may not be collapsed.

## Three-track program

### REP — Representation capacity and fidelity

`THM-TARGET-001`, `FAITHFUL-REP-001`, `P8-ROLE-001`, and W0 through W3 belong to the representation track.

The REP track asks whether one fixed target architecture can encode, recover, and preserve a frozen source class under declared constraints.

W0 through W3 establish project-authored finite construction results. They do not establish that the target structure is reasoning-specific, necessary, minimal, unique, or universal.

### USD — Universal-structure discovery

`THM-US-TARGET-001` governs the architecture-neutral discovery track.

The unknown kernel `K*` is not identified in advance with FARA, PB-001, or the current primitive list.

USD requires independently admitted reasoning systems, independently admitted contrast systems, representation invariance, ablation, alternative reconstruction, and explicit equivalence and cost relations.

### ADJ — Adjudication and specificity

The adjudication track compares FARA with `GREL-001` and later alternative architectures.

It determines whether the FARA construction is strict, constrained-equivalent, translation-equivalent, a conservative extension, dominated, incomparable, or unresolved.

## Frozen representation boundaries

`THM-TARGET-001` v1.0 freezes `S_core`, `S_IRD`, `A_FARA`, witness `W=(E,D,M,iota,kappa)`, P1–P7, P8-I, P8-E, and the finite representation theorem families.

`FAITHFUL-REP-001` freezes materiality, applicability, canonical reducts, target-only recovery, strong typed correspondence, P5 bisimulation, P7 history and path, semantic agreement, coherence, uniformity, composition, machinery accounting, nontriviality, and `Faithful_split`.

`P8-ROLE-001` selects `split`: `Pres_8I` is internal; `Corr_8E` remains separate.

`SCORE-LEMMA-LEDGER-001` freezes 24 construction, 10 obstruction, and 3 assembly obligations.

## Accepted project-authored REP packages

### W0 — Source normalization

`SCORE-W0-PROOF-001` proves `LEM-SC-001` through `LEM-SC-004` and establishes `OBS-SC-001` as a source boundary.

### W1 — Direct axes

`SCORE-W1-PROOF-001` proves the direct-axis construction lemmas and refutes `OBS-SC-003` and `OBS-SC-006`.

### W2 — Dynamics and history

`SCORE-W2-PROOF-001` proves deterministic and probabilistic dynamics, history, revision, and operational rule-version change; it refutes `OBS-SC-004` and `OBS-SC-005`.

### W3 — Global witness construction

`SCORE-W3-PROOF-001` proves distributed decomposition, target-only recovery, semantic agreement, cross-axis coherence, complete machinery accounting, uniformity, source-isomorphism equivariance, compositional accountability, and well-formed witness assembly.

It refutes `OBS-SC-002`, `OBS-SC-007`, `OBS-SC-008`, and `OBS-SC-009` over their registered finite scopes.

W3 uses the frozen FARA interface and adds no primitive. It proves all registered finite construction obligations. It does not prove the formal negative-control family, `Nontrivial`, `Faithful_split`, a representation theorem, or any USD theorem.

## Current program state

### REP ledger

- total obligations: 37;
- proved construction lemmas: 24;
- source boundary established: 1;
- refuted obstruction hypotheses: 8;
- open obligations: 4;
- completed waves: W0 through W3;
- active wave: W4.

`OBS-SC-010` and NC-01 through NC-10 remain active.

### W3.5 bridge

`W3.5-SDG-001` is frozen and not executed.

W3.5 must resolve generic-baseline factorization, FARA-specificity, reasoning/non-reasoning discrimination, candidate-invariant ablation and reconstruction, machinery and cost accounting, and central-claim impact.

W4 may execute in parallel. W5 is blocked until both W4 and W3.5 resolve.

### USD state

`THM-US-TARGET-001`, `GREL-001`, `RCS-001`, and `US-CANDIDATES-001` are frozen prospectively.

No candidate invariant has been classified. No universal-structure theorem has been proved or refuted.

## W4 requirements

Each negative control must be rejected by a frozen formal clause rather than evaluator preference, source reaccess, case-specific repair, or a newly invented restriction.

The package must preserve any valid countermodel or hidden commitment and may not modify the frozen faithful predicate to force failure.

## W3.5 requirements

The factorization and specificity program must permit the result that FARA is equivalent to or dominated by a generic typed relational baseline.

Positive and contrast membership may not depend on FARA compatibility or candidate presence.

Representation counts and REP obligation closure may not update USD, necessity, minimality, or uniqueness claims.

## W5 authorization

W5 may begin only when:

1. `OBS-SC-010` is resolved;
2. `W3.5-SDG-001` is resolved;
3. the assembly package states whether the finite result is FARA-specific, generic, equivalent, incomparable, or unresolved;
4. all claim impacts remain track-specific.

## Primary method

1. preserve frozen source, target, semantic, P8, and track boundaries;
2. execute W4 and W3.5 in parallel;
3. search for countermodels, generic factorizations, and alternative reconstructions;
4. assemble the strongest finite REP result only after both gates close;
5. execute the USD positive/contrast and candidate-invariant program;
6. attempt extension to `S_IRD` only under explicit additional obligations;
7. address lower bounds, necessity, minimality, equivalence, uniqueness, or no-go results;
8. mechanize the largest sound fragments;
9. obtain independent proof review and adversarial counterexample search.

## Proof-status discipline

Project-authored human-checkable proof, bounded executable corroboration, proof-assistant verification, independent proof review, empirical replication, and application correspondence remain separate.

Repository consistency checks do not constitute mathematical proof verification.

## Counterexample policy

Potential counterexamples, equivalences, reductions, generic factorizations, and no-single-kernel results are primary research objects.

A result may not be repaired by redefining reasoning, narrowing the contrast class, changing a candidate after exposure, or omitting equivalent reintroduction costs.

## Current nonclaims

The repository does not establish:

- `OBS-SC-010` or the global `Nontrivial` conjunct;
- `W3.5-SDG-001`;
- `Faithful_split` satisfiability;
- any W5 assembly obligation;
- FARA adequacy for `S_core` or `S_IRD`;
- FARA-specificity relative to `GREL-001`;
- a representation-independent universal kernel;
- any candidate invariant’s necessity;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- actual-process correspondence;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review of W0–W3.

## Immediate central work

Execute W4 and W3.5 in parallel. Do not begin W5 assembly until both are resolved.
