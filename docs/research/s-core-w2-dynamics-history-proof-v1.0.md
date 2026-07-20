# S_core W2 Dynamics, History, Revision, and Self-Modification Proof v1.0

## Status

Human-checkable project-authored proof package for `LEM-SC-010`, `LEM-SC-011`, `LEM-SC-013`, `LEM-SC-015`, and `LEM-SC-016`.

It also refutes `OBS-SC-004` and `OBS-SC-005` over their registered finite W2 scopes.

Proof identifier: `SCORE-W2-PROOF-001`.

This result is internal proof work. It has not been independently reviewed or machine-checked in a proof assistant. The accompanying executable reference implementation tests the construction on finite fixtures; it is corroboration, not a substitute for the proof.

## Governing artifacts

This proof is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/research/s-core-construction-obstruction-ledger-v1.0.md`;
- `docs/research/s-core-w0-normalization-proof-v1.0.md`;
- `docs/research/s-core-w1-direct-axis-proof-v1.0.md`;
- `theory/definitions/definitions.md`;
- `frameworks/FARA/architecture.md`;
- `frameworks/FARA/primitives.md`.

The machine-readable result is `theory/evaluation/s-core-w2-dynamics-history-proof.json`.

## 1. Scope and dependency boundary

Fix an arbitrary W0-normalized theorem-facing source contract in `S_core`, its finite P5 and P7 reducts, and the W1 target allocation for every source item already represented on a direct axis.

Write the material source dynamics as

\[
\mathcal D_S=(Q,T,src,tgt,lab,stat,rv,pre,res,act,obs,K,w,Active),
\]

where:

- `Q` is the finite set of material source configurations;
- `T` is the finite set of material transition records;
- `src,tgt:T->Q` give transition endpoints;
- `lab` gives the material action, observation, procedure, or transition label;
- `stat` distinguishes permitted, forbidden, defeated, superseded, and unresolved continuations;
- `rv` gives the governing rule version when one applies;
- `pre`, `res`, `act`, and `obs` give material preconditions, resource conditions, action dependence, and observation dependence;
- `K` assigns a finite kernel identifier where the source transition belongs to a probabilistic continuation family;
- `w` gives the exact source-declared finite-support weight where present;
- `Active(q)` is the finite set of rule versions active at configuration `q`.

A source transition is **live** exactly when its source status is `permitted` and its governing rule version, if any, belongs to `Active(src(t))`. This definition is not chosen by the target. It is the explicit source operational contract restricted by W0.

For each finite-support probabilistic kernel `(q,k)`, the source supplies a finite distribution

\[
\mu_{q,k}:Q\to[0,1]
\]

whose nonzero values are the weights of the live transitions in that kernel and whose total weight is one under the source arithmetic or source-declared value equivalence.

Write the material source history as

\[
\mathcal H_S=(E,\preceq_S,\leadsto_S,evState,evTrans,Prov,Rev,Mod,Anc,Path),
\]

where `E` is the finite event carrier, `preceq_S` is the material temporal or causal order required by P7, `leadsto_S` is the material causal relation, and the remaining finite relations record provenance, revision, retraction, supersession, rule activation and deactivation, accepted and rejected modifications, dependency ancestry, and path conditions.

W2 proves finite target constructions for these source reducts. It does not prove admissible target-only recovery, global semantic agreement, complete cross-axis coherence, complete machinery accounting, distributed composition, uniformity of the complete witness family, or `Faithful_split`.

## 2. Fixed W2 target schema

Define one target extension schema `DYN-HISTORY-1.0`. The schema is fixed across every source contract in `S_core`.

### 2.1 Reuse of W1 images

When a source configuration, rule, commitment, ground, consequence, or other source item already has a W1 image `e_x`, W2 reuses that image. New W2 records use disjoint tagged namespaces. Therefore W2 does not replace the W1 representation or create a second source-specific target ontology.

This local reuse does not by itself prove the complete cross-axis coherence obligation `LEM-SC-020`; that obligation concerns the assembled witness and remains W3 work.

### 2.2 Target components

The W2 extension uses the existing theorem-facing FARA components as follows:

- `Sigma` stores finite target configuration records;
- `Theta` stores finite target transition records;
- `C` stores represented rules, rule versions, and the state-indexed active-version relation;
- `Omega` stores the copied admissibility status of every represented continuation;
- `H` stores event records and all material history, revision, provenance, ancestry, and path relations;
- `U`, `Pi`, `Rep`, `S`, and `I` represent and interpret the preceding records;
- `Prov` carries copied provenance records;
- `kappa_W2` declares the schema and the fixed operational definitions used in this proof.

No new FARA primitive is introduced. Configuration records, transition records, event records, rule-version records, and history relations are derived target data represented through the frozen object, property, relation, representation, interpretation, calculus, state, transition, history, admissibility, and provenance-facing components.

### 2.3 Configuration allocation

For every `q in Q`, reuse or allocate an injective target configuration image `sigma_q`. Store in `Sigma` exactly the material source snapshot at `q`, including:

- commitment and consequence status needed by P5 or P7;
- resource values needed by transition conditions;
- the set `Active(q)` of active rule versions;
- every additional finite state variable material to the source continuation relation.

The stored snapshot is source data. W2 does not infer a stronger state than the source supplies.

### 2.4 Transition allocation

For every `t in T`, allocate one target transition record `theta_t` and copy exactly:

\[
(src(t),tgt(t),lab(t),stat(t),rv(t),pre(t),res(t),act(t),obs(t),K(t),w(t)).
\]

The endpoint fields refer to `sigma_{src(t)}` and `sigma_{tgt(t)}`. Rule-version fields refer to represented rule-version objects. No target transition record is allocated without a source transition record.

Define the target live transition relation by the fixed formula

\[
Live_T(\sigma_q,\ell,\sigma_{q'})
\]

iff there exists `theta_t` such that:

1. `src(theta_t)=sigma_q`;
2. `tgt(theta_t)=sigma_{q'}`;
3. `lab(theta_t)=ell`;
4. `stat(theta_t)=permitted`; and
5. the copied governing rule version is absent or belongs to the copied active-version set of `sigma_q`.

Preconditions, resources, action dependence, observation dependence, rule identity, rule version, kernel identity, and weight remain explicit fields of the same transition record and are included in transition-label comparison for the preservation predicate.

This definition makes rule-version change operational. Merely attaching a “modified” label without changing the active-version relation cannot change `Live_T` and therefore cannot satisfy the construction.

### 2.5 Probabilistic kernels

For each source kernel `(q,k)`, define the target finite-support kernel by

\[
\nu_{\sigma_q,k}(\sigma_{q'})=\mu_{q,k}(q').
\]

The target copies exact source weights. When the frozen source contract permits a nontrivial weight equivalence, the same declared equivalence is copied; W2 does not choose a new tolerance.

### 2.6 History allocation

For every source event `e in E`, allocate one target event image `h_e`. Copy exactly:

- the source event-to-state relation;
- the source event-to-transition relation;
- every material pair in `preceq_S`;
- every material causal pair in `leadsto_S`;
- provenance records;
- revision, retraction, and supersession records;
- accepted and rejected rule-modification records;
- rule activation and deactivation facts;
- dependency-ancestry pairs;
- path-condition records.

The source material order relation is copied as the relation used by P7, rather than reconstructed from display order or file order. Thus target order does not gain or lose a material pair through an unstated closure convention.

### 2.7 W2 machinery fragment

`kappa_W2` records:

- schema identifier `DYN-HISTORY-1.0`;
- configuration, transition, event, rule, and rule-version record schemas;
- the fixed live-transition definition;
- the finite-support kernel definition;
- state-snapshot and active-version fields;
- exact history relation schemas;
- revision and modification validation rules;
- source value-equivalence records actually used;
- executable-reference identifiers.

This is a partial machinery fragment. `LEM-SC-021`, which requires the complete machinery ledger for the assembled witness, remains unproved.

## 3. `LEM-SC-010` — Deterministic dynamics construction

Assume the applicable source P5 reduct is deterministic under its declared material transition key. Let

\[
B=\{(q,\sigma_q)\mid q\in Q\}.
\]

The state map is total and injective by W1 allocation and W2 reuse.

### Forward condition

If the source has a live transition

\[
q\xrightarrow{\lambda}q',
\]

then the construction allocated `theta_t` with the exact endpoints, label, status, governing rule version, conditions, and dependencies. The rule version is active at `q` because the source transition is live. Therefore

\[
\sigma_q\xrightarrow{\lambda}_T\sigma_{q'}.
\]

### Reflection condition

If the target has a live transition

\[
\sigma_q\xrightarrow{\lambda}_T\sigma_{q'},
\]

then the fixed target definition witnesses a copied transition record `theta_t`. Such a record exists only for a source transition record. Its permitted status and active governing version imply that the corresponding source transition is live. Hence

\[
q\xrightarrow{\lambda}q'.
\]

All material preconditions, rule versions, resource conditions, action dependence, and observation dependence are fields of the same record and are compared exactly. Therefore no transition with altered operational metadata can satisfy the reflected label.

The target live transition graph on the represented image is isomorphic to the material source live transition graph. An isomorphism is a bisimulation. Determinism is preserved because the target has exactly the copied live transitions and no additional live transition on the represented image.

Therefore `LEM-SC-010` is proved.

## 4. `LEM-SC-011` — Finite-support probabilistic dynamics construction

Fix a source kernel `(q,k)`. Its support is finite by the frozen `S_core` definition. The target kernel has support

\[
\{\sigma_{q'}\mid q'\in supp(\mu_{q,k})\}
\]

and copies the corresponding source weight.

For every subset `A` of source configurations,

\[
\mu_{q,k}(A)=\nu_{\sigma_q,k}(\phi[A]),
\]

because `phi(q')=sigma_{q'}` is injective and each support weight is copied exactly. The same equality holds under a source-declared weight equivalence when exact equality is not the frozen source default.

The forward condition follows because every positive-weight source branch has a copied target branch. The reflection condition follows because every target branch and weight comes from one source transition record. Rule-version activation, preconditions, resource conditions, and action or observation dependence are preserved by the same record identity.

Thus `B` is a finite labeled probabilistic bisimulation on the represented image.

Therefore `LEM-SC-011` is proved.

## 5. `LEM-SC-013` — Historical-and-path construction

Define

\[
\phi_7(e)=h_e.
\]

Fresh allocation makes `phi_7` injective.

For source events `e,f`, the construction copies a target order fact exactly when the material source order fact exists. Therefore

\[
e\preceq_S f\Longleftrightarrow h_e\preceq_T h_f.
\]

Hence `phi_7` is an order embedding.

The same copy-and-reflect argument applies to causal order, provenance, revision, retraction, supersession, rule activation and deactivation, accepted and rejected modifications, dependency ancestry, and every registered path condition. Target event-state and event-transition links connect the history to the represented configurations and transitions rather than leaving history as an unrelated log.

If two source histories differ in any material pair, revision record, active rule version, ancestry fact, or path condition, their target histories differ in the corresponding copied fact. A current target state alone cannot replace the source history because the history carrier and path relations are separately represented and required by the recovered P7 reduct.

Therefore `LEM-SC-013` is proved.

## 6. `LEM-SC-015` — Nonmonotonic revision and retraction

For each material revision record, W2 copies:

- subject identity;
- revision kind;
- before and after configurations;
- before and after status or value;
- basis or defeater;
- event position;
- provenance and dependency links.

The target configuration snapshots at the before and after states copy the corresponding source status. No monotonicity condition is imposed. A retracted commitment may be absent or explicitly retracted in the later source snapshot, and the target later snapshot has the same state.

A target revision record is accepted only when its before value agrees with the represented before configuration and its after value agrees with the represented after configuration. Thus a decorative revision label that leaves the target state unchanged fails the construction whenever the source state changed.

Because revision, retraction, and supersession kinds are distinct copied values and their endpoints are reflected, none can collapse into another unless the frozen source contract declares the distinction immaterial.

Therefore `LEM-SC-015` is proved.

## 7. `LEM-SC-016` — Self-modification and rule-version change

For each source modification record, W2 copies:

- the proposed change;
- accepted or rejected decision;
- before and after configurations;
- deactivated rule versions;
- activated rule versions;
- event position, basis, provenance, and dependency ancestry.

For an accepted modification, the target after-state active-version set equals the target before-state set minus the copied deactivations plus the copied activations. For a rejected modification, the active-version set is unchanged.

The target live transition definition consults the active-version set at the source configuration. Therefore:

- a transition governed by a deactivated version is not live after deactivation unless a distinct source record permits it under another active version;
- a transition governed by a newly activated version can become live only at states where that version is active;
- a rejected proposal does not alter later live transitions merely because a proposal record exists.

The operational transition relation therefore changes when and only when the copied source operational contract changes. Rule modification is not represented solely as a label or historical annotation.

Therefore `LEM-SC-016` is proved.

## 8. Obstruction results

### `OBS-SC-004` — Dynamics-bisimulation mismatch

The registered obstruction asks whether some admitted finite deterministic or finite-support probabilistic P5 reduct necessarily fails to admit a bisimilar target under the fixed target interface.

Sections 3 and 4 construct, for an arbitrary admitted W2 source reduct, a target live transition system isomorphic to the deterministic source graph or measure-isomorphic to each finite probabilistic kernel. Hence no object in the registered finite W2 scope forces a dynamics-bisimulation mismatch.

`OBS-SC-004` is therefore **refuted** over its registered `S_core` scope.

This does not establish admissible recovery, semantic agreement, global coherence, or theorem assembly.

### `OBS-SC-005` — History-and-path collapse

The registered obstruction asks whether an admitted finite material history necessarily loses order, revision, path, or rule-version distinctions under the fixed target interface.

Section 5 gives an injective event map preserving and reflecting every material order and history relation; Sections 6 and 7 make revision and rule-version changes agree with represented state snapshots and later live transitions. Hence no object in the registered finite W2 scope forces history or path collapse.

`OBS-SC-005` is therefore **refuted** over its registered `S_core` scope.

This does not prove that all hidden or non-finite histories belong to `S_core`; those remain outside this finite explicit result.

## 9. Dependency audit

| Obligation | Result | Dependencies used |
|---|---|---|
| `LEM-SC-010` | proved | `LEM-SC-005` through `LEM-SC-009`; frozen P5 semantics |
| `LEM-SC-011` | proved | `LEM-SC-005` through `LEM-SC-009`; finite-support source kernel |
| `LEM-SC-013` | proved | `LEM-SC-005` through `LEM-SC-012`; W2 transition construction; frozen P7 semantics |
| `LEM-SC-015` | proved | `LEM-SC-007`, `LEM-SC-009`, `LEM-SC-012`, `LEM-SC-013` |
| `LEM-SC-016` | proved | `LEM-SC-009` through `LEM-SC-015`; explicit active rule versions |
| `OBS-SC-004` | refuted | `LEM-SC-010`, `LEM-SC-011` |
| `OBS-SC-005` | refuted | `LEM-SC-013`, `LEM-SC-015`, `LEM-SC-016` |

No W3 recovery, semantic-agreement, coherence, machinery-completeness, uniformity, composition, or witness-assembly lemma is assumed. No FARA adequacy theorem, PB-001 completeness claim, or actual-process correspondence claim is used.

## 10. Executable reference evidence

`tools/s_core_w2_reference.py` implements:

- exact finite state and transition allocation;
- state-indexed active rule versions;
- deterministic live-transition reflection;
- finite exact probabilistic kernels;
- complete transition-metadata comparison;
- event, order, causal, provenance, revision, modification, ancestry, and path copying;
- revision snapshot validation;
- accepted and rejected modification validation.

`tests/test_s_core_w2_reference.py` checks:

- exact deterministic transition reflection;
- exclusion of superseded continuations from the live relation;
- exact finite-support weights;
- rejection of probability-mass drift;
- rejection of inactive-version live transitions;
- order reflection against removed and spurious pairs;
- operational revision-state change;
- operational self-modification;
- rejected-modification invariance;
- path-condition retention;
- rule-version history retention.

These executions corroborate the construction and protect against implementation drift. They are not proof-assistant verification or independent proof review.

## 11. Result and next dependency

W2 is complete. The lemma ledger now records:

- 16 proved construction obligations;
- 4 refuted obstruction hypotheses;
- 1 established source-scope boundary;
- 16 open obligations;
- completed waves W0, W1, and W2;
- active wave W3.

The next dependency wave is W3:

- `LEM-SC-017` — distributed decomposition and interface construction;
- `LEM-SC-018` — admissible target-only recovery;
- `LEM-SC-019` — semantic agreement;
- `LEM-SC-020` — cross-axis coherence;
- `LEM-SC-021` — complete machinery-ledger construction;
- `LEM-SC-022` — uniformity and source-isomorphism equivariance;
- `LEM-SC-023` — compositional accountability;
- `LEM-SC-024` — well-formed witness assembly.

## Nonclaims

This proof does not establish:

- any W3 or W5 construction or assembly obligation;
- the remaining W4 obstruction or negative-control obligations;
- admissible target-only recovery;
- semantic agreement for the assembled target;
- complete cross-axis coherence;
- a complete machinery ledger;
- distributed composition or compositional accountability;
- uniformity of the complete constructor family;
- any complete `Pres_i` predicate;
- `Faithful_split` satisfiability;
- a complete uniform FARA witness constructor;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- correspondence between an actual process and an IRD presentation;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review.
