# Faithful Representation Specification v1.0

## Status

Frozen prospective definition for `THM-TARGET-001`.

This artifact completes the theorem-facing semantics of `Pres_1` through `Pres_7`, parameterizes the three admissible P8 modes, and defines `Faithful_{m_8}` for the frozen theorem target. It does not prove that any source object has a faithful FARA representation, select a P8 mode, establish PB-001 completeness, or establish universality, necessity, minimality, equivalence, uniqueness, or impossibility.

## Governing artifacts

This specification depends on:

- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/thm-target-001.json`;
- `theory/evaluation/thm-target-001-premise-ledger.json`;
- `docs/research/independent-reasoning-definition-v1.0.md`;
- `docs/research/preservation-basis-investigation-v1.0.md`;
- `docs/methodology/negative-control-suite-v1.0.md`;
- `theory/definitions/definitions.md`;
- `frameworks/FARA/architecture.md`;
- `frameworks/FARA/primitives.md`;
- `docs/governance/deduction-first-research-standard.md`.

The machine-readable registration is `theory/evaluation/faithful-representation-specification-v1.0.json`.

## 1. Scope and notation

Let `(P,J)` be a well-formed source episode in `S_core`, let `A` be a target package in `A_FARA`, and let

\[
W=(E,D,M,\iota,\kappa)
\]

be a proposed representation witness.

The source episode is evaluated under a frozen source contract

\[
C_S=(\tau_S,\mathsf{Mat},\mathsf{ValEq},\mathsf{App}),
\]

where:

- `tau_S` gives the source sorts and relation signatures;
- `Mat` identifies the source facts material to IRD-001 and PB-001;
- `ValEq` gives every permitted value-equivalence or approximation relation;
- `App` records whether each preservation axis is applicable.

`C_S` belongs to the source presentation and may not be chosen or weakened by the target mapping.

For each axis `i`, the specification constructs a finite typed source reduct `S_i(P,J,C_S)` and a recovered finite typed target reduct `T_i(A,W)`. The correspondence package recorded in `M` is

\[
\Phi_i=(\phi_i,\psi_i,\rho_i),
\]

where `phi_i` maps source elements, `psi_i` maps attribute values, and `rho_i` maps source relation symbols to target relation symbols or explicitly declared derived relations.

## 2. Source materiality contract

### 2.1 Material facts

A source element, attribute, or relation fact is material when changing it in an otherwise well-formed comparison presentation can change at least one of:

- whether R1–R6 hold;
- which commitments or alternatives are live;
- which grounds support, defeat, qualify, constrain, or select a commitment;
- which transitions are admissible or with what weight;
- which commitment consequence occurs or how it is used;
- which history, provenance, rule version, or dependency path is in force;
- which semantic or evidential claim is licensed.

For `S_core`, every material fact is explicit and finite.

### 2.2 Materiality closure

`Mat` must be closed under the following rule:

> If a registered material fact refers to an element, attribute, relation, condition, rule version, provenance item, or event position required to interpret that fact, the referred item is also material.

A source contract may exclude a source fact only by recording a materiality-exclusion certificate stating why every permitted variation of that fact leaves the registered IRD-001 and PB-001 commitments unchanged. The certificate is part of the source contract and may be challenged by a countermodel.

### 2.3 Axis applicability

`App_i(P,J)` is true exactly when `S_i` contains at least one material distinction or relation fact for axis `i`.

An inapplicable axis is recorded as `not_applicable`; it is not counted as a successful preservation result. For a theorem over `S_core`, inability to determine applicability is a source-contract defect, not an `unknown` preservation result.

## 3. Canonical source reducts

Each source reduct is the least finite typed relational structure containing the following material content and its closure dependencies.

### 3.1 `S_1` — Configuration reduct

`S_1` contains material process locations, states, participants, resources, externalized components, and their typed incidence, availability, containment, ownership, participation, and state-at-location relations.

### 3.2 `S_2` — Commitment reduct

`S_2` contains material commitments and the holder, content reference, status, degree or weight, time or event location, retention, acceptance, rejection, suspension, comparison, and revision relations applicable to them.

### 3.3 `S_3` — Stake-and-alternative reduct

`S_3` contains material stakes, questions, objectives, conflicts, alternatives, and the relations identifying which alternatives are live, mutually exclusive, ranked, available, or relevant to each stake at each source location.

### 3.4 `S_4` — Ground-and-justification reduct

`S_4` contains material grounds, constraints, assumptions, observations, rules, models, prior commitments, and the typed justificatory relations connecting them to stakes and commitments. Justificatory role is preserved as data: support, defeat, qualification, constraint, selection, provenance, or an explicitly declared source-specific role.

### 3.5 `S_5` — Admissibility-and-dynamics reduct

`S_5` contains material source configurations and admissible continuations, including transition preconditions, rule or procedure identity, rule version, resource conditions, action or observation dependence, probability or weight where present, and the distinction between permitted, forbidden, defeated, superseded, and unresolved continuations.

### 3.6 `S_6` — Consequence reduct

`S_6` contains material consequences and their content reference, status, degree, producing transition or justification, downstream use, action authorization, inquiry effect, policy effect, proof status, communication effect, or other source-declared consequence role.

### 3.7 `S_7` — Historical-and-path reduct

`S_7` contains material event positions, temporal or causal order, provenance, revision, retraction, supersession, rule activation and deactivation, accepted and rejected modifications, dependency ancestry, and every path condition for which different histories license different current or future states.

## 4. Admissible recovery

`D` is an admissible recovery family only when all of the following hold.

1. **Fixed interface:** `D` consists of versioned procedures `D_i` with one declared interface for the source class.
2. **Target-only input:** after construction, `D_i` receives only `A`, the witness metadata contained in `A` or `kappa`, and an axis query. It receives no source object, source identifier, external narrative, evaluator judgment, or unregistered state.
3. **Determinism:** for fixed declared inputs, `D_i` returns one recovered reduct or one explicit failure diagnostic.
4. **Termination on `S_core`:** every `D_i` terminates for finite theorem-facing packages produced for `S_core`.
5. **Purity:** recovery does not modify the target package or create facts that were absent from the declared target and ledger.
6. **Declared derivation:** every derived relation used by `D_i` has a finite definition in `kappa`.
7. **No hidden oracle:** no recovery procedure may call an unrestricted interpreter, source simulator, case database, human evaluator, network resource, or undeclared executable dependency.
8. **Version identity:** procedures counted as the same recovery family have the same code or formal definition identifier and version.

Failure of any clause makes the witness inadmissible before axis preservation is evaluated.

## 5. Strong typed correspondence

For each applicable axis `i`, `Phi_i` must satisfy all of the following.

### 5.1 Totality and typing

`phi_i` is total on the carrier of `S_i` and preserves source sorts through a declared sort map. `rho_i` is total on every material relation symbol. `psi_i` is total on every material attribute value.

### 5.2 Distinction preservation

For source elements `x` and `y` of the same material sort,

\[
x\neq y \Longrightarrow \phi_i(x)\neq\phi_i(y).
\]

Where two source sorts are materially disjoint, their target images must remain distinguishable by target type, explicit sort tags, or a declared disjointness relation.

### 5.3 Relation preservation and reflection

For every material `n`-ary source relation symbol `r` and every well-typed source tuple `x`,

\[
r^{S_i}(x)
\Longleftrightarrow
\rho_i(r)^{T_i}(\phi_i(x)).
\]

The forward direction prohibits loss. The reverse direction prohibits spurious material relations among the represented source elements.

### 5.4 Attribute preservation

For every material attribute `a` of source element or tuple `x`,

\[
\psi_i(a^{S_i}(x))
\equiv_{a,C_S}
a^{T_i}(\phi_i(x)).
\]

The equivalence relation `equiv_{a,C_S}` must be fixed in `ValEq` before target construction. Exact equality is the default. Approximation is permitted only when its tolerance, metric, and consequence for later admissibility are source-declared.

### 5.5 Image accountability

Target elements or relations outside the image may exist, but they may discharge a preservation obligation only when they are declared in `kappa`, semantically interpreted, and linked to the image by explicit target relations. Unlinked auxiliary content cannot repair a failed embedding.

### 5.6 Preservation predicate

For applicable axis `i`,

\[
Pres_i(P,J,A,W)
\]

holds exactly when admissible recovery produces `T_i` and `Phi_i` is a total typed strong embedding satisfying Sections 5.1–5.5. For an inapplicable axis, `Pres_i` is replaced by the recorded result `not_applicable`.

## 6. Axis-specific obligations

The strong-embedding definition is supplemented by the following axis-specific conditions.

### 6.1 `Pres_1`

The represented configuration must distinguish all material participants, states, resources, locations, and externalized components and reflect their material incidence and availability relations.

### 6.2 `Pres_2`

Commitment identity, holder, content, status, degree, and revision state must be preserved. Acceptance, rejection, suspension, retention, and graded commitment may not collapse unless the source contract declares them equivalent.

### 6.3 `Pres_3`

Stake identity and live-alternative structure must be preserved at the source locations where they apply. A final choice does not preserve the alternatives that were available or the question under which they were compared.

### 6.4 `Pres_4`

The target must preserve and reflect the endpoints and role of every material justificatory relation. Distinct support, defeat, qualification, constraint, selection, and provenance relations may not collapse into one generic edge unless the source contract proves the role distinction immaterial.

### 6.5 `Pres_5`

The recovered target dynamics must be bisimilar on the represented image to the material source dynamics under `Phi_5`:

- every material admissible source continuation has a corresponding target continuation;
- every target continuation over represented source configurations that is used to justify faithfulness reflects a material source continuation;
- preconditions, rule versions, resource conditions, action or observation dependence, and registered weights are preserved;
- self-modification changes later admissible transitions rather than appearing only as a label.

This is a finite labeled probabilistic bisimulation when source weights are present and an ordinary finite labeled bisimulation otherwise.

### 6.6 `Pres_6`

The target must preserve consequence identity, status, degree, producing basis, and downstream role. Equal text or equal external output is insufficient when the source consequences differ in commitment, authorization, proof, policy, or inquiry status.

### 6.7 `Pres_7`

`phi_7` must be an order embedding for material temporal or causal order:

\[
x\preceq_S y \Longleftrightarrow \phi_7(x)\preceq_T\phi_7(y).
\]

Revision, retraction, supersession, rule-version, provenance, and dependency-ancestry relations are preserved and reflected. A target current state cannot stand in for a source history when path differences change present or future admissibility.

## 7. Semantic agreement

Let `den_S` be the source interpretation fixed by `C_S`, and let `den_A` be the semantic interpretation supplied by target component `I`.

`SemAgree(P,J,A,W)` holds when:

1. every material source element and relation role has a declared target denotation through `iota`;
2. for every source item `x`, `den_S(x)` and `den_A(iota(x))` are equivalent under a source-declared semantic equivalence relation;
3. the same semantic relation is used consistently wherever `x` appears across axes;
4. the target does not strengthen precision, certainty, modality, normativity, authority, or evidential grade beyond the source;
5. lexical similarity is irrelevant unless the lexical content is itself a material source object;
6. every semantic bridge used in the proof is finite, declared, and included in `kappa`.

A target label such as “belief,” “rule,” “evidence,” or “conclusion” has no semantic force by itself.

## 8. Cross-axis coherence

`Coherent(P,J,A,W)` holds when the seven correspondence packages form one compatible representation rather than seven unrelated successful encodings.

For every source item appearing in more than one source reduct:

- its target images are identical, or are connected by an explicit identity, co-reference, version, or representation relation;
- the linked images have semantically compatible denotations;
- commitment status, source location, rule version, provenance, and consequence role do not conflict;
- a relation used in one axis cannot be contradicted by a relation used in another;
- any deliberate duplication is declared and counted in `kappa`.

Cross-axis incoherence is a faithfulness failure even when every axis considered separately admits an embedding.

## 9. P8 parameterized clauses

This specification defines the clause for each allowed `m_8` value but does not select a value.

### 9.1 `coordinate`

`P8_coordinate` is an eighth strong-embedding obligation over the internal provenance and evidence-status reduct. It preserves and reflects:

- observation stratum;
- evidence grade;
- observed, reported, instrumented, specified, inferred, and formally proved status;
- provenance source;
- correspondence scope;
- unresolved status.

It additionally requires that no target claim is stronger than the represented source evidence status.

### 9.2 `side_condition`

`P8_side_condition` treats process-to-presentation correspondence as external to the internal representation theorem. The internal theorem applies only to the mathematical presentation. Any application claim must separately identify:

- the actual process;
- the source presentation;
- the observation contract;
- the correspondence evidence;
- the maximum licensed claim.

The target may preserve source provenance annotations, but such preservation does not establish the external correspondence.

### 9.3 `split`

`P8_split` requires:

1. an internal strong embedding of provenance and evidence-status annotations; and
2. a separate external correspondence obligation between the actual process and the source presentation.

The internal representation theorem may be proved without proving the external correspondence theorem, but no application claim may omit the second obligation.

### 9.4 P8 blocker

`P8_{m_8}` is defined for all three modes. `THM-CORE-REP-001` remains blocked until one mode is selected by a versioned P8 decision artifact. Selection changes no clause in this specification; it chooses which already-frozen clause enters the theorem.

## 10. Uniform construction

A constructor family `F` is uniform over a source class `S` only when:

1. `F` has one identifier, version, finite definition, and input schema;
2. `F(P,J,C_S)` returns `A,W` without branching on a source case identifier or consulting a case-specific database;
3. source-specific content enters the output only as encoded target data or declared constructor parameters;
4. every helper algorithm is fixed across the source class and appears in `kappa`;
5. after construction, preservation can be checked without reaccessing the source except to compare the frozen source reducts with recovered target reducts;
6. `F` is equivariant under source isomorphism: isomorphic source presentations produce target packages and witnesses isomorphic under the induced renaming;
7. for `S_core`, `F` and every recovery procedure are effective and terminating.

Uniformity is a property of a constructor family, not of one isolated witness. A theorem using different hand-built constructors must either prove that they instantiate one finite uniform schema or weaken its claim.

## 11. Compositional accountability

`CompAccount(P,J,A,W)` is conditional on a declared source decomposition.

When the source contract declares

\[
(P,J)=P_1\oplus_B P_2
\]

over an interface `B`, the witness must record:

- the component encodings;
- the target representation of `B`;
- how component images are identified or linked;
- every material cross-component relation;
- how component histories and admissibility conditions compose;
- whether the composite target is equal or equivalent to the target produced by the global constructor.

Restriction to a component must commute with encoding up to the declared target equivalence. A construction may not preserve components while discarding material interaction structure.

No decomposition is required when the source contract declares the episode indecomposable.

## 12. Complete machinery ledger

`LedgerComplete(A,W)` holds when `kappa` is a finite dependency graph containing every item used to construct, recover, interpret, or verify the representation, including:

- target primitives and derived constructs;
- relation and attribute schemas;
- state variables and hidden state;
- constructor and recovery algorithms;
- semantic bridge clauses;
- metadata fields;
- external libraries or executable assumptions;
- normalization, canonicalization, and equivalence procedures;
- composition rules;
- cost-bearing helper structures.

Every symbol, procedure, data field, and dependency referenced by `E`, `D`, `M`, or `iota` must resolve to:

1. a source input;
2. a canonical target component; or
3. a node in `kappa`.

A missing dependency is hidden machinery and makes the witness inadmissible. Metadata is not free: when it carries a material distinction, it is part of the target representation and must be preserved, interpreted, and counted.

## 13. Formal nontriviality predicate

`Nontrivial(P,J,A,W)` is the conjunction of:

- admissible recovery;
- strong preservation and reflection rather than output agreement alone;
- lexical invariance under alpha-renaming of nonmaterial labels;
- no source oracle or case database;
- cross-axis coherence;
- complete machinery accounting;
- no evaluator-supplied repair;
- no unsupported evidential upgrade;
- compositional accountability where applicable.

The following mandatory controls fail for registered formal reasons:

| Control | Required failure |
|---|---|
| NC-01 lookup-table substitution | `Pres_4`, `Pres_5`, or `Pres_7` fails even if `Pres_6` passes |
| NC-02 dependency collapse | relation reflection in `Pres_4` fails |
| NC-03 history erasure | order or revision reflection in `Pres_7` fails |
| NC-04 hidden rule modification | admissible recovery or `LedgerComplete` fails |
| NC-05 label-only semantics | `SemAgree` or lexical invariance fails |
| NC-06 unrestricted interpreter | admissible recovery, uniformity, or `LedgerComplete` fails |
| NC-07 hidden auxiliary state | image accountability or `LedgerComplete` fails |
| NC-08 provenance deletion | `Pres_4`, `Pres_7`, or the selected P8 clause fails |
| NC-09 output-equivalent process substitution | `Pres_4`, `Pres_5`, `Pres_6`, or `Pres_7` fails |
| NC-10 primitive smuggling | `LedgerComplete` and machinery accounting fail |

A control rejected for a different unproved reason is unresolved for that diagnostic; it does not validate the expected clause.

## 14. Faithful representation

For fixed `m_8`, define:

\[
\begin{aligned}
Faithful_{m_8}(P,J,A,W) \iff {}&
WF_{S_{core}}(P,J,C_S) \\
&\land WF_{A_{FARA}}(A) \\
&\land WF_W(W) \\
&\land AdmissibleRecovery(A,W) \\
&\land \bigwedge_{i=1}^{7}\left(App_i\Rightarrow Pres_i(P,J,A,W)\right) \\
&\land P8_{m_8}(P,J,A,W) \\
&\land SemAgree(P,J,A,W) \\
&\land Coherent(P,J,A,W) \\
&\land Uniform(F,S_{core}) \\
&\land CompAccount(P,J,A,W) \\
&\land LedgerComplete(A,W) \\
&\land Nontrivial(P,J,A,W).
\end{aligned}
\]

`WF_W` requires all correspondence packages, declarations, versions, diagnostics, and ledger references to be present and well typed.

The `Uniform` conjunct refers to the constructor family under which `W` is produced. A single witness cannot establish class-level uniformity by itself.

## 15. Decision semantics

For the formal `S_core` theorem:

- `true` means every conjunct has a derivation from frozen definitions and premises;
- `false` means at least one conjunct has a formal failure witness;
- `not_applicable` is permitted only for a source-declared empty axis;
- `partial` is diagnostic only and does not satisfy the theorem;
- `unknown` blocks theorem acceptance and normally indicates an incomplete source contract, target definition, or proof.

A countermodel to `THM-CORE-REP-001` must establish that one in-scope source object has no `A,W` satisfying `Faithful_{m_8}` for the selected P8 mode. Failure of one attempted witness is only a representation-construction failure unless nonexistence is proved.

## 16. Gate effects

Upon merge:

- `formal-theorem-target` remains `satisfied`;
- `premise-ledger-and-semantics` becomes `satisfied`;
- `faithful-representation-definition` becomes `satisfied`;
- `scoped-representation-proof` remains `not_satisfied`;
- `THM-CORE-REP-001` remains blocked by P8 selection and then remains unproved;
- no necessity, minimality, mechanization, or independent-review gate changes.

## 17. Revision policy

This specification may be revised only through a new version when a change alters:

- a source reduct;
- the strong-embedding criterion;
- admissible recovery;
- semantic agreement;
- cross-axis coherence;
- uniformity;
- compositional accountability;
- machinery accounting;
- a P8 mode clause;
- the `Faithful_{m_8}` conjunction.

Clarification that does not alter accepted witnesses or countermodels may be recorded as an erratum. A change that repairs a failed theorem preserves the failed version and creates a new theorem dependency.

## Nonclaims

This specification does not establish:

- that `Faithful_{m_8}` is satisfiable for any source object;
- that one uniform FARA constructor exists;
- that FARA represents `S_core` or `S_IRD`;
- that PB-001 is sufficient, necessary, independent, or complete;
- which P8 mode is correct;
- that the ten negative controls exhaust invalid representation strategies;
- that any FARA primitive is necessary;
- that FARA is minimal, equivalent to alternatives, unique, or universal;
- that a theorem has been proved, mechanized, or independently reviewed.

## Next required artifact

Select and justify the theorem-facing P8 mode. After that decision is frozen, construct the `S_core` construction-and-obstruction lemma ledger.
