# S_core Construction and Obstruction Lemma Ledger v1.0

## Status

Frozen prospective proof-dependency ledger for `THM-TARGET-001`.

Ledger identifier: `SCORE-LEMMA-LEDGER-001`.

This artifact decomposes the finite-core proof program into explicit construction, obstruction, and assembly obligations. It does not prove any listed lemma, establish a representation witness, establish FARA adequacy, or satisfy the scoped-representation-proof gate.

## Governing artifacts

The ledger is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/thm-target-001.json`;
- `theory/evaluation/thm-target-001-premise-ledger.json`;
- `docs/research/independent-reasoning-definition-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/governance/deduction-first-research-standard.md`.

The machine-readable registration is `theory/evaluation/s-core-construction-obstruction-ledger.json`.

## 1. Purpose and result boundary

Stage D4 requires every material `S_core` feature to receive either:

1. a proved uniform construction lemma showing how the feature participates in a `Faithful_split` witness; or
2. a proved obstruction, countermodel, or scope-boundary result showing why the required construction cannot be obtained under the frozen assumptions.

Registration in this ledger is not proof. A ledger entry may move from `registered_unproved` only when its proof, refutation, or obstruction artifact is versioned, dependency-complete, and accepted under repository proof governance.

Failure of one attempted construction does not establish nonexistence. An obstruction entry must quantify over the stated constructor or witness class and prove the registered impossibility statement.

## 2. Obligation classes

The ledger uses three classes.

### Construction obligations

A construction lemma produces or preserves a component of the target package, witness, recovered reduct, correspondence map, or global faithfulness condition.

### Obstruction obligations

An obstruction lemma proves that a stated construction class cannot satisfy a frozen obligation, or that a candidate source object lies outside the frozen finite-core scope. Obstructions must distinguish:

- failure of one attempted witness;
- failure of one constructor family;
- failure of the fixed `A_FARA` target interface;
- failure of the theorem over all admissible targets in the frozen class;
- source-scope failure.

### Assembly obligations

An assembly lemma combines previously proved obligations into a common-schema result, a `Faithful_split` witness result, or the strongest justified theorem-or-obstruction conclusion.

## 3. Dependency waves

The dependency order is mandatory.

### Wave W0 — Source normalization kernel

- `LEM-SC-001` — finite source-contract normalization;
- `LEM-SC-002` — canonical P1–P7 and P8-I reduct extraction;
- `LEM-SC-003` — materiality closure and applicability decidability;
- `LEM-SC-004` — source-isomorphism transport.

These obligations determine whether the finite theorem inputs are explicit, finite, stable under renaming, and suitable for effective construction.

### Wave W1 — Base carriers and direct axes

- `LEM-SC-005` — target carrier allocation;
- `LEM-SC-006` — configuration construction (`Pres_1`);
- `LEM-SC-007` — commitment construction (`Pres_2`);
- `LEM-SC-008` — stake-and-alternative construction (`Pres_3`);
- `LEM-SC-009` — ground-and-justification construction (`Pres_4`);
- `LEM-SC-012` — consequence construction (`Pres_6`);
- `LEM-SC-014` — internal evidential-status construction (`Pres_8I`).

### Wave W2 — Dynamics, history, and revision

- `LEM-SC-010` — deterministic dynamics construction;
- `LEM-SC-011` — finite-support probabilistic dynamics construction;
- `LEM-SC-013` — historical-and-path construction (`Pres_7`);
- `LEM-SC-015` — nonmonotonic revision and retraction;
- `LEM-SC-016` — self-modification and rule-version change.

### Wave W3 — Global witness obligations

- `LEM-SC-017` — distributed decomposition and interface construction;
- `LEM-SC-018` — admissible target-only recovery;
- `LEM-SC-019` — semantic agreement;
- `LEM-SC-020` — cross-axis coherence;
- `LEM-SC-021` — complete machinery-ledger construction;
- `LEM-SC-022` — uniformity and source-isomorphism equivariance;
- `LEM-SC-023` — compositional accountability;
- `LEM-SC-024` — well-formed witness assembly.

### Wave W4 — Obstruction and negative-control program

- `OBS-SC-001` through `OBS-SC-010`.

Obstruction work may begin as soon as its dependencies are defined. It does not need to wait for a favorable construction.

### Wave W5 — Theorem assembly

- `ASM-SC-001` — common target-schema assembly;
- `ASM-SC-002` — arbitrary-episode `Faithful_split` assembly;
- `ASM-SC-003` — finite-core theorem-or-obstruction closure.

No W5 entry may be accepted while a dependency is `registered_unproved`, `unknown`, or merely supported by examples.

## 4. Construction lemma statements

### `LEM-SC-001` — Finite source-contract normalization

For every `(P,J,C_S) ∈ S_core`, construct a finite normalized source contract preserving the source interpretation, materiality predicate, value-equivalence relations, axis applicability, R1–R6 truth, and every material dependency.

The normalization may not discard information later required by `Faithful_split`.

### `LEM-SC-002` — Canonical reduct extraction

From the normalized source contract, effectively extract the least finite typed reducts `S_1` through `S_7` and the internal evidential-status reduct `S_8I`, including their materiality-closure dependencies.

### `LEM-SC-003` — Materiality closure and applicability decidability

Prove that materiality closure terminates on `S_core`, that every registered material reference is included, and that every axis applicability judgment is decidable from the frozen source contract.

### `LEM-SC-004` — Source-isomorphism transport

Prove that source isomorphisms transport normalized contracts, reducts, materiality, applicability, and later construction inputs without case identifiers or semantic strengthening.

### `LEM-SC-005` — Target carrier allocation

Define one finite target-allocation schema that assigns typed target carriers, relation schemas, and witness references to every normalized source carrier while preserving material disjointness and leaving all helper machinery explicit in `kappa`.

### `LEM-SC-006` — Configuration construction

Using `LEM-SC-005`, construct the P1 target reduct and correspondence package preserving and reflecting material participants, states, resources, locations, externalized components, incidence, containment, availability, ownership, and participation.

### `LEM-SC-007` — Commitment construction

Construct the P2 target reduct and correspondence package preserving and reflecting commitment identity, holder, content, status, degree, location, retention, acceptance, rejection, suspension, comparison, and revision.

### `LEM-SC-008` — Stake-and-alternative construction

Construct the P3 target reduct and correspondence package preserving and reflecting stakes, questions, objectives, conflicts, live alternatives, relevance, mutual exclusion, ranking, and availability.

### `LEM-SC-009` — Ground-and-justification construction

Construct the P4 target reduct and correspondence package preserving and reflecting every material ground, constraint, assumption, observation, rule, model, prior commitment, and typed justificatory role, including support, defeat, qualification, constraint, selection, and provenance.

### `LEM-SC-010` — Deterministic dynamics construction

For deterministic finite source dynamics, construct a target transition system and correspondence satisfying the P5 finite labeled bisimulation, including preconditions, resource conditions, action or observation dependence, rule identity, rule version, and admissibility status.

### `LEM-SC-011` — Finite-support probabilistic dynamics construction

For finite-support stochastic source dynamics, construct a target transition system and weight correspondence satisfying the registered finite labeled probabilistic bisimulation without changing source probabilities or source-declared value equivalence.

### `LEM-SC-012` — Consequence construction

Construct the P6 target reduct and correspondence preserving and reflecting consequence identity, content, status, degree, producing basis, downstream use, authorization, policy effect, inquiry effect, proof status, and communication role.

### `LEM-SC-013` — Historical-and-path construction

Construct the P7 target reduct and correspondence as an order embedding preserving and reflecting temporal or causal order, provenance, revision, retraction, supersession, dependency ancestry, rule activation, rejected modifications, and material path conditions.

### `LEM-SC-014` — Internal evidential-status construction

Construct `Pres_8I` while preserving and reflecting observation versus inference, reported versus instrumented status, assumed versus derived status, provenance source, confidence, uncertainty, qualification, rejection, supersession, withdrawal, unresolved status, and evidence grade. Prove that no evidential upgrade is introduced.

### `LEM-SC-015` — Nonmonotonic revision and retraction

Show that defeasible support, rejection, suspension, retraction, and supersession can be represented without collapsing earlier and later commitment states or treating current output as a substitute for revision history.

### `LEM-SC-016` — Self-modification and rule-version change

Show that accepted, rejected, and superseded rule modifications alter the represented later admissible dynamics at the exact source event position, preserving before/after rule versions and dependencies.

### `LEM-SC-017` — Distributed decomposition and interface construction

For a source-declared decomposition `(P,J)=P_1 ⊕_B P_2`, construct component images, the interface image, cross-component relations, and composed histories without attributing the whole episode to an unsupported component or erasing interaction structure.

### `LEM-SC-018` — Admissible target-only recovery

Define one versioned deterministic recovery family that terminates on all constructed finite targets, uses target and declared witness data only, produces the registered reducts or explicit diagnostics, and calls no source oracle, case database, evaluator, network resource, or undeclared executable dependency.

### `LEM-SC-019` — Semantic agreement

Prove that every material source item and relation role receives a target denotation equivalent under the frozen source semantics, consistently across axes, without lexical shortcuts or strengthening of precision, certainty, modality, normativity, authority, or evidence grade.

### `LEM-SC-020` — Cross-axis coherence

Prove that the per-axis images form one compatible representation: shared source items are identical or explicitly linked, semantic denotations agree, statuses and versions do not conflict, and deliberate duplication is declared and counted.

### `LEM-SC-021` — Complete machinery-ledger construction

Construct a finite acyclic dependency graph resolving every target primitive, derived construct, schema, state variable, algorithm, semantic bridge, metadata field, external dependency, normalization rule, equivalence rule, composition rule, and cost-bearing helper used by `E`, `D`, `M`, `iota`, or verification.

### `LEM-SC-022` — Uniformity and equivariance

Prove that the constructor family has one finite definition and input schema, does not branch on source case identifiers, is effective and terminating on `S_core`, and maps source-isomorphic inputs to target-isomorphic outputs under induced renaming.

### `LEM-SC-023` — Compositional accountability

Prove that encoding commutes with every source-declared decomposition up to the frozen target equivalence and preserves material interface, cross-component, historical, and admissibility relations.

### `LEM-SC-024` — Well-formed witness assembly

Combine the constructed target, recovery family, correspondence packages, semantic interpretation, and machinery ledger into a well-typed witness `W=(E,D,M,iota,kappa)` without assuming any unproved theorem-level conclusion.

## 5. Obstruction lemma statements

### `OBS-SC-001` — Non-finite material-closure boundary

Determine whether any admitted `S_core` source contract can have nonterminating or non-finite materiality closure. A proved example is a source-scope defect or countermodel to the frozen `S_core` requirements, not automatically a target failure.

### `OBS-SC-002` — Hidden-interpreter necessity

Prove or refute that some in-scope source object can be recovered only by an unrestricted interpreter, source oracle, or case database. Acceptance requires quantification over the frozen admissible constructor and recovery class.

### `OBS-SC-003` — Relation-reflection collapse

Search for an in-scope source whose material justificatory, commitment, or alternative relations cannot all be preserved and reflected under the fixed target interface without collapse or unregistered machinery.

### `OBS-SC-004` — Dynamics-bisimulation mismatch

Search for deterministic or finite-support stochastic `S_core` dynamics for which no admissible target transition system satisfies the frozen P5 bisimulation requirements.

### `OBS-SC-005` — History-and-path collapse

Search for an in-scope source whose revision, provenance, dependency ancestry, or path-sensitive admissibility cannot be order-embedded and reflected by an admissible target witness.

### `OBS-SC-006` — Evidential-status impossibility

Search for an in-scope source whose internal evidence-status distinctions cannot be preserved without loss, fabrication, or upgrade under `Pres_8I`.

### `OBS-SC-007` — Nonuniform-constructor obstruction

Determine whether successful witnesses necessarily require source-specific case branching, source identifiers, or an unbounded family of helper definitions, contradicting frozen uniformity.

### `OBS-SC-008` — Composition-interface loss

Search for a source-declared distributed decomposition whose material cross-component relations or composed dynamics cannot be recovered by any admissible compositional witness.

### `OBS-SC-009` — Fixed-target-interface insufficiency

Determine whether some `S_core` object requires a target commitment not expressible or derivable in the frozen `A_FARA` interface without adding an unregistered primitive or weakening faithfulness.

### `OBS-SC-010` — Formal negative-control family

For NC-01 through NC-10, prove the expected failure predicate or register the control as unresolved. Passing a control for an unexpected or unproved reason does not establish the expected obstruction.

## 6. Assembly lemma statements

### `ASM-SC-001` — Common target-schema assembly

From the accepted construction lemmas, derive one fixed finite target and witness schema eligible for every `S_core` input. This is the immediate dependency of `THM-CORE-COMMON-001`.

### `ASM-SC-002` — Arbitrary-episode faithful-witness assembly

For arbitrary `(P,J,C_S) ∈ S_core`, combine the accepted obligations into an `A,W` satisfying every conjunct of `Faithful_split`. This is the immediate dependency of `THM-CORE-REP-001`.

### `ASM-SC-003` — Finite-core theorem-or-obstruction closure

Conclude exactly one strongest justified outcome:

- the scoped representation theorem is proved;
- a quantified obstruction or countermodel refutes it;
- a proper subclass theorem is proved with the excluded cases identified;
- the theorem remains unresolved because named ledger obligations remain open.

This entry may not convert unresolved obligations into a favorable theorem statement.

## 7. Coverage rule

The mandatory feature set is:

- finite source normalization;
- configuration;
- commitments;
- stakes and alternatives;
- grounds and justificatory roles;
- deterministic dynamics;
- finite-support probabilistic dynamics;
- consequences;
- history and path dependence;
- nonmonotonic revision;
- self-modification and rule versions;
- internal evidential status;
- target-only recovery;
- semantic agreement;
- cross-axis coherence;
- uniformity and equivariance;
- distributed composition;
- machinery accounting;
- formal negative controls;
- theorem assembly.

A feature is resolved only when a cited accepted artifact proves a construction lemma or establishes a quantified obstruction with the exact registered scope. Examples, successful compilers, evaluator agreement, or one failed mapping do not resolve a feature.

## 8. Status transitions

Allowed obligation statuses are:

- `registered_unproved`;
- `proof_in_progress`;
- `proved`;
- `refuted`;
- `obstruction_established`;
- `scope_boundary_established`;
- `blocked`;
- `unknown`;
- `superseded`.

A status other than `registered_unproved`, `proof_in_progress`, `blocked`, or `unknown` requires an evidence artifact and dependency audit.

The ledger itself is frozen and complete as a dependency decomposition. Its execution status is `registered_unexecuted`.

## 9. Gate and claim effects

Upon merge:

- the formal-theorem-target gate remains satisfied;
- the premise-ledger-and-semantics gate remains satisfied;
- the faithful-representation-definition gate remains satisfied;
- the scoped-representation-proof gate remains not satisfied;
- no lower-bound, minimality, mechanization, independent-review, or empirical-replication gate changes;
- no central claim is promoted.

The ledger is evidence that proof dependencies have been registered, not evidence that the dependencies hold.

## 10. Revision policy

Changing an obligation's statement, quantified scope, accepted dependencies, success criterion, or obstruction strength requires a new ledger version unless the change is a non-substantive clarification. Failed and superseded proof attempts remain preserved.

A lemma that reveals a defect in `THM-TARGET-001`, `FAITHFUL-REP-001`, P8-ROLE-001, or `S_core` triggers the applicable versioned revision rather than silent repair.

## Nonclaims

This ledger does not establish:

- any listed lemma;
- existence of a uniform constructor;
- satisfiability of `Faithful_split` for any or every `S_core` object;
- FARA adequacy;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- correspondence between an actual process and an IRD presentation;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- machine verification or independent proof review.

## Next required proof package

Prove or refute the W0 source-normalization kernel: `LEM-SC-001` through `LEM-SC-004`. No target-construction theorem should be accepted before those source-side obligations are resolved.