# S_core Construction and Obstruction Lemma Ledger v1.0

## Status

Frozen proof-dependency ledger for `THM-TARGET-001`; W0 and W1 complete, W2 active.

Ledger identifier: `SCORE-LEMMA-LEDGER-001`.

This artifact preserves the frozen construction, obstruction, and assembly statements while recording their execution state. `SCORE-W0-PROOF-001` proves the source-normalization kernel and establishes one source-scope boundary. `SCORE-W1-PROOF-001` proves the target-carrier and direct-axis construction package and refutes two registered direct-axis impossibility hypotheses.

The ledger currently records 11 proved construction lemmas, 1 established source-scope boundary, 2 refuted obstruction hypotheses, and 23 open obligations. It does not establish admissible target-only recovery, any complete `Pres_i` predicate, `Faithful_split`, FARA adequacy, or a scoped representation theorem.

## Governing artifacts

The ledger is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/thm-target-001.json`;
- `theory/evaluation/thm-target-001-premise-ledger.json`;
- `docs/research/independent-reasoning-definition-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/governance/deduction-first-research-standard.md`.

Accepted execution packages:

- `docs/research/s-core-w0-normalization-proof-v1.0.md` and `theory/evaluation/s-core-w0-normalization-proof.json`;
- `docs/research/s-core-w1-direct-axis-proof-v1.0.md` and `theory/evaluation/s-core-w1-direct-axis-proof.json`.

The machine-readable ledger is `theory/evaluation/s-core-construction-obstruction-ledger.json`.

## 1. Purpose and result boundary

Stage D4 requires every material `S_core` feature to receive either:

1. a proved uniform construction lemma showing how the feature participates in a `Faithful_split` witness; or
2. a proved obstruction, countermodel, refutation, or scope-boundary result showing the strongest justified negative conclusion.

Registration is not proof. A terminal status requires a versioned evidence artifact and dependency audit. Failure of one attempted construction does not establish nonexistence.

W1 proves direct-axis target structures and strong embeddings. The frozen definition of `Pres_i` also requires admissible target-only recovery, which remains `LEM-SC-018`. Therefore this ledger does not report any complete `Pres_i` predicate as proved.

## 2. Obligation classes

- **Construction:** produces or preserves a component of a target package, correspondence, recovery, or global witness.
- **Obstruction:** proves a registered impossibility, refutes an impossibility hypothesis by a quantified construction, or establishes a source boundary.
- **Assembly:** combines accepted obligations into a common-schema result, arbitrary-episode witness, or strongest theorem-or-obstruction conclusion.

## 3. Dependency waves and execution

### W0 — Source normalization kernel — **complete**

- `LEM-SC-001` — finite source-contract normalization — **proved**.
- `LEM-SC-002` — canonical reduct extraction — **proved**.
- `LEM-SC-003` — materiality closure and applicability decidability — **proved**.
- `LEM-SC-004` — source-isomorphism transport — **proved**.
- `OBS-SC-001` — non-finite material-closure boundary — **scope boundary established**.

### W1 — Base carriers and direct axes — **complete**

- `LEM-SC-005` — target carrier allocation — **proved**.
- `LEM-SC-006` — configuration construction — **proved**.
- `LEM-SC-007` — commitment construction — **proved**.
- `LEM-SC-008` — stake-and-alternative construction — **proved**.
- `LEM-SC-009` — ground-and-justification construction — **proved**.
- `LEM-SC-012` — consequence construction — **proved**.
- `LEM-SC-014` — internal evidential-status construction — **proved**.
- `OBS-SC-003` — relation-reflection collapse — **refuted**.
- `OBS-SC-006` — evidential-status impossibility — **refuted**.

### W2 — Dynamics, history, and revision — **active**

- `LEM-SC-010` — deterministic dynamics construction — **registered unproved**.
- `LEM-SC-011` — finite-support probabilistic dynamics construction — **registered unproved**.
- `LEM-SC-013` — historical-and-path construction — **registered unproved**.
- `LEM-SC-015` — nonmonotonic revision and retraction — **registered unproved**.
- `LEM-SC-016` — self-modification and rule-version change — **registered unproved**.
- `OBS-SC-004` and `OBS-SC-005` become executable as their dependencies close.

### W3 — Global witness obligations — **open**

- `LEM-SC-017` through `LEM-SC-024`.

### W4 — Remaining obstruction and negative controls — **open**

- `OBS-SC-002`, `OBS-SC-004`, `OBS-SC-005`, and `OBS-SC-007` through `OBS-SC-010`.

### W5 — Theorem assembly — **open**

- `ASM-SC-001` through `ASM-SC-003`.

No W5 entry may be accepted while a dependency remains open, unknown, or supported only by examples.

## 4. Frozen construction statements

### `LEM-SC-001` — Finite source-contract normalization — **proved**

For every `(P,J,C_S) ∈ S_core`, construct a finite normalized source contract preserving the source interpretation, materiality predicate, value-equivalence relations, axis applicability, R1–R6 truth, and every material dependency. The normalization may not discard information later required by `Faithful_split`.

### `LEM-SC-002` — Canonical reduct extraction — **proved**

From the normalized source contract, effectively extract the least finite typed reducts `S_1` through `S_7` and the internal evidential-status reduct `S_8I`, including their materiality-closure dependencies.

### `LEM-SC-003` — Materiality closure and applicability decidability — **proved**

Prove that materiality closure terminates on `S_core`, that every registered material reference is included, and that every axis applicability judgment is decidable from the frozen source contract.

### `LEM-SC-004` — Source-isomorphism transport — **proved**

Prove that source isomorphisms transport normalized contracts, reducts, materiality, applicability, and later construction inputs without case identifiers or semantic strengthening.

### `LEM-SC-005` — Target carrier allocation — **proved**

Define one finite target-allocation schema that assigns typed target carriers, relation schemas, and witness references to every normalized source carrier while preserving material disjointness and leaving all helper machinery explicit in `kappa`.

### `LEM-SC-006` — Configuration construction — **proved**

Using `LEM-SC-005`, construct the P1 target reduct and correspondence package preserving and reflecting material participants, states, resources, locations, externalized components, incidence, containment, availability, ownership, and participation.

### `LEM-SC-007` — Commitment construction — **proved**

Construct the P2 target reduct and correspondence package preserving and reflecting commitment identity, holder, content, status, degree, location, retention, acceptance, rejection, suspension, comparison, and revision.

### `LEM-SC-008` — Stake-and-alternative construction — **proved**

Construct the P3 target reduct and correspondence package preserving and reflecting stakes, questions, objectives, conflicts, live alternatives, relevance, mutual exclusion, ranking, and availability.

### `LEM-SC-009` — Ground-and-justification construction — **proved**

Construct the P4 target reduct and correspondence package preserving and reflecting every material ground, constraint, assumption, observation, rule, model, prior commitment, and typed justificatory role, including support, defeat, qualification, constraint, selection, and provenance.

### `LEM-SC-010` — Deterministic dynamics construction — **registered unproved**

For deterministic finite source dynamics, construct a target transition system and correspondence satisfying the P5 finite labeled bisimulation, including preconditions, resource conditions, action or observation dependence, rule identity, rule version, and admissibility status.

### `LEM-SC-011` — Finite-support probabilistic dynamics construction — **registered unproved**

For finite-support stochastic source dynamics, construct a target transition system and weight correspondence satisfying the registered finite labeled probabilistic bisimulation without changing source probabilities or source-declared value equivalence.

### `LEM-SC-012` — Consequence construction — **proved**

Construct the P6 target reduct and correspondence preserving and reflecting consequence identity, content, status, degree, producing basis, downstream use, authorization, policy effect, inquiry effect, proof status, and communication role.

### `LEM-SC-013` — Historical-and-path construction — **registered unproved**

Construct the P7 target reduct and correspondence as an order embedding preserving and reflecting temporal or causal order, provenance, revision, retraction, supersession, dependency ancestry, rule activation, rejected modifications, and material path conditions.

### `LEM-SC-014` — Internal evidential-status construction — **proved**

Construct `Pres_8I`'s direct-axis target reduct and correspondence while preserving and reflecting observation versus inference, reported versus instrumented status, assumed versus derived status, provenance source, confidence, uncertainty, qualification, rejection, supersession, withdrawal, unresolved status, and evidence grade. Prove that no evidential upgrade is introduced. Full `Pres_8I` remains dependent on admissible recovery.

### `LEM-SC-015` — Nonmonotonic revision and retraction — **registered unproved**

Show that defeasible support, rejection, suspension, retraction, and supersession can be represented without collapsing earlier and later commitment states or treating current output as a substitute for revision history.

### `LEM-SC-016` — Self-modification and rule-version change — **registered unproved**

Show that accepted, rejected, and superseded rule modifications alter the represented later admissible dynamics at the exact source event position, preserving before/after rule versions and dependencies.

### `LEM-SC-017` — Distributed decomposition and interface construction — **registered unproved**

For a source-declared decomposition `(P,J)=P_1 ⊕_B P_2`, construct component images, the interface image, cross-component relations, and composed histories without attributing the whole episode to an unsupported component or erasing interaction structure.

### `LEM-SC-018` — Admissible target-only recovery — **registered unproved**

Define one versioned deterministic recovery family that terminates on all constructed finite targets, uses target and declared witness data only, produces the registered reducts or explicit diagnostics, and calls no source oracle, case database, evaluator, network resource, or undeclared executable dependency.

### `LEM-SC-019` — Semantic agreement — **registered unproved**

Prove that every material source item and relation role receives a target denotation equivalent under the frozen source semantics, consistently across axes, without lexical shortcuts or strengthening of precision, certainty, modality, normativity, authority, or evidence grade.

### `LEM-SC-020` — Cross-axis coherence — **registered unproved**

Prove that the per-axis images form one compatible representation: shared source items are identical or explicitly linked, semantic denotations agree, statuses and versions do not conflict, and deliberate duplication is declared and counted.

### `LEM-SC-021` — Complete machinery-ledger construction — **registered unproved**

Construct a finite acyclic dependency graph resolving every target primitive, derived construct, schema, state variable, algorithm, semantic bridge, metadata field, external dependency, normalization rule, equivalence rule, composition rule, and cost-bearing helper used by `E`, `D`, `M`, `iota`, or verification.

### `LEM-SC-022` — Uniformity and equivariance — **registered unproved**

Prove that the constructor family has one finite definition and input schema, does not branch on source case identifiers, is effective and terminating on `S_core`, and maps source-isomorphic inputs to target-isomorphic outputs under induced renaming.

### `LEM-SC-023` — Compositional accountability — **registered unproved**

Prove that encoding commutes with every source-declared decomposition up to the frozen target equivalence and preserves material interface, cross-component, historical, and admissibility relations.

### `LEM-SC-024` — Well-formed witness assembly — **registered unproved**

Combine the constructed target, recovery family, correspondence packages, semantic interpretation, and machinery ledger into a well-typed witness `W=(E,D,M,iota,kappa)` without assuming any unproved theorem-level conclusion.

## 5. Frozen obstruction statements

### `OBS-SC-001` — Non-finite material-closure boundary — **scope boundary established**

Determine whether any admitted `S_core` source contract can have nonterminating or non-finite materiality closure. The W0 proof shows that no admitted object can; genuinely non-finite closure lies outside `S_core`.

### `OBS-SC-002` — Hidden-interpreter necessity — **registered unproved**

Prove or refute that some in-scope source object can be recovered only by an unrestricted interpreter, source oracle, or case database. Acceptance requires quantification over the frozen admissible constructor and recovery class.

### `OBS-SC-003` — Relation-reflection collapse — **refuted**

Search for an in-scope source whose material justificatory, commitment, or alternative relations cannot all be preserved and reflected under the fixed target interface without collapse or unregistered machinery. The W1 generic incidence construction embeds every finite direct-axis reduct in this registered scope.

### `OBS-SC-004` — Dynamics-bisimulation mismatch — **registered unproved**

Search for deterministic or finite-support stochastic `S_core` dynamics for which no admissible target transition system satisfies the frozen P5 bisimulation requirements.

### `OBS-SC-005` — History-and-path collapse — **registered unproved**

Search for an in-scope source whose revision, provenance, dependency ancestry, or path-sensitive admissibility cannot be order-embedded and reflected by an admissible target witness.

### `OBS-SC-006` — Evidential-status impossibility — **refuted**

Search for an in-scope source whose internal evidence-status distinctions cannot be preserved without loss, fabrication, or upgrade under the direct-axis `Pres_8I` construction. W1 supplies an exact strong embedding for every finite `S_8I` reduct. `Corr_8E` remains separate.

### `OBS-SC-007` — Nonuniform-constructor obstruction — **registered unproved**

Determine whether successful witnesses necessarily require source-specific case branching, source identifiers, or an unbounded family of helper definitions, contradicting frozen uniformity.

### `OBS-SC-008` — Composition-interface loss — **registered unproved**

Search for a source-declared distributed decomposition whose material cross-component relations or composed dynamics cannot be recovered by any admissible compositional witness.

### `OBS-SC-009` — Fixed-target-interface insufficiency — **registered unproved**

Determine whether some `S_core` object requires a target commitment not expressible or derivable in the frozen `A_FARA` interface without adding an unregistered primitive or weakening faithfulness.

### `OBS-SC-010` — Formal negative-control family — **registered unproved**

For NC-01 through NC-10, prove the expected failure predicate or register the control as unresolved. Passing a control for an unexpected or unproved reason does not establish the expected obstruction.

## 6. Frozen assembly statements

### `ASM-SC-001` — Common target-schema assembly — **registered unproved**

From the accepted construction lemmas, derive one fixed finite target and witness schema eligible for every `S_core` input. This is the immediate dependency of `THM-CORE-COMMON-001`.

### `ASM-SC-002` — Arbitrary-episode faithful-witness assembly — **registered unproved**

For arbitrary `(P,J,C_S) ∈ S_core`, combine the accepted obligations into an `A,W` satisfying every conjunct of `Faithful_split`. This is the immediate dependency of `THM-CORE-REP-001`.

### `ASM-SC-003` — Finite-core theorem-or-obstruction closure — **registered unproved**

Conclude exactly one strongest justified outcome: the scoped representation theorem is proved; a quantified obstruction refutes it; a proper subclass theorem is proved; or named obligations remain unresolved. This entry may not convert unresolved obligations into a favorable theorem statement.

## 7. Coverage and status rules

The mandatory feature set remains finite source normalization, P1–P7, P8-I, target-only recovery, semantic agreement, coherence, uniformity, distributed composition, machinery accounting, formal negative controls, and theorem assembly.

Allowed statuses are `registered_unproved`, `proof_in_progress`, `proved`, `refuted`, `obstruction_established`, `scope_boundary_established`, `blocked`, `unknown`, and `superseded`.

A terminal status requires accepted evidence. Examples, successful compilers, evaluator agreement, or one failed mapping do not resolve an obligation.

## 8. Gate and claim effects

- formal-theorem-target remains satisfied;
- premise-ledger-and-semantics remains satisfied;
- faithful-representation-definition remains satisfied;
- scoped-representation-proof remains not satisfied;
- mechanized-proof-verification remains not satisfied;
- independent-proof-review remains not satisfied;
- no central claim is promoted.

W1 direct-axis results are partial lemma progress. No admissible recovery family or complete faithful witness has been established.

## 9. Revision policy

Changing an obligation statement, quantified scope, accepted dependencies, success criterion, or obstruction strength requires a new ledger version unless the change is a non-substantive clarification. Failed and superseded proof attempts remain preserved.

## Nonclaims

This ledger does not establish:

- any W2–W5 construction or assembly obligation;
- admissible target-only recovery or a complete `Pres_i` predicate;
- satisfiability of `Faithful_split`;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- correspondence between an actual process and an IRD presentation;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review.

## Next required proof package

Construct or obstruct the W2 dynamics, history, revision, and self-modification package: `LEM-SC-010`, `LEM-SC-011`, `LEM-SC-013`, `LEM-SC-015`, and `LEM-SC-016`. Execute `OBS-SC-004` and `OBS-SC-005` as their dependencies close.
