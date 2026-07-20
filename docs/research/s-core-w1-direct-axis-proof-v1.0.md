# S_core W1 Direct-Axis Construction Proof v1.0

## Status

Human-checkable project-authored proof package for `LEM-SC-005`, `LEM-SC-006`, `LEM-SC-007`, `LEM-SC-008`, `LEM-SC-009`, `LEM-SC-012`, and `LEM-SC-014`.

It also refutes `OBS-SC-003` and `OBS-SC-006` over their registered direct-axis scopes.

Proof identifier: `SCORE-W1-PROOF-001`.

This result is internal proof work. It has not been independently reviewed or machine-checked in a proof assistant. The accompanying executable reference implementation tests the construction on finite fixtures; it is corroboration, not a substitute for the proof.

## Governing artifacts

This proof is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/research/s-core-construction-obstruction-ledger-v1.0.md`;
- `docs/research/s-core-w0-normalization-proof-v1.0.md`;
- `theory/definitions/definitions.md`;
- `frameworks/FARA/architecture.md`;
- `frameworks/FARA/primitives.md`.

The machine-readable result is `theory/evaluation/s-core-w1-direct-axis-proof.json`.

## 1. Scope and dependency boundary

Fix an arbitrary normalized theorem-facing source contract produced by W0 and one of its finite direct-axis reducts

\[
S_i=(X_i,V_i,\mathcal R_i,\mathcal A_i,\operatorname{den}_i),
\]

where

\[
i\in\{1,2,3,4,6,8I\}.
\]

Here:

- `X_i` is the finite disjoint union of material source-element carriers;
- `V_i` is the finite set of material attribute values;
- `R_i` is the finite family of typed material relation symbols and their true tuples;
- `A_i` is the finite family of material attribute symbols and their values;
- `den_i` is the source interpretation restricted to the reduct;
- source relation and attribute roles are canonical W0 identities, not lexical display labels.

The W0 proof establishes finiteness, effective extraction, applicability decidability, and source-isomorphism transport. W1 must construct target carriers and direct-axis strong embeddings. It does not prove admissible target-only recovery, global semantic agreement, cross-axis coherence, dynamics, history, complete machinery accounting, or `Faithful_split`.

## 2. Fixed target incidence schema

Define one finite target schema `DIR-INCIDENCE-1.0`. The schema is fixed across every source contract and every direct axis.

### 2.1 Target object kinds

The target object carrier `U` may contain objects of the following declared kinds:

- `encoded_element`;
- `encoded_value`;
- `sort_code`;
- `role_code`;
- `axis_code`;
- `position_code`;
- `relation_occurrence`;
- `attribute_occurrence`;
- `evidence_status_record`;
- `provenance_record`;
- `investigation_record`.

These are object kinds represented through target properties and typed relations. This proof does not assert that they are new FARA primitives. They are derived target data built from `Object`, `Property`, `Relation`, `Representation`, `Interpretation`, and `Investigation`.

### 2.2 Fixed target relations

The target relation component `R` uses the following finite relation schema:

- `represented_by(u,p)`;
- `denotes(p,u)`;
- `has_sort(u,s)`;
- `in_axis(u,a)`;
- `occurrence_role(q,r)`;
- `argument(q,j,u)`;
- `attribute_owner(q,u)`;
- `attribute_role(q,r)`;
- `attribute_value(q,v)`;
- `has_provenance(u,p)`;
- `has_evidence_status(u,e)`;
- `has_source_denotation(u,d)`;
- `source_equivalent(v,w,e)`.

The relation names are fixed schema identifiers. Source-specific relation roles, attribute roles, sorts, axes, positions, denotations, and values enter only as encoded target objects and facts.

### 2.3 Representations and category separation

For every allocated target object `u`, allocate a distinct representation object `rep(u)` in `Rep`. Add `represented_by(u,rep(u))` and `denotes(rep(u),u)`.

Thus:

- the represented target object is not its representation;
- relation occurrences are objects distinct from representations of those occurrences;
- the representational structure `S` is the finite structure on `Rep` induced by the target incidence facts;
- interpretation `I` assigns each representation the transported source denotation or the declared structural meaning of its target code;
- `Inv` records the theorem-facing investigation and axis;
- `C`, `Sigma`, `Theta`, `H`, `Omega`, and `Res` are present as declared typed components but carry no W1 obligation unless source data explicitly uses a corresponding direct-axis object;
- `Prov` stores the copied internal provenance and evidence-status records used by P8-I and any other direct axis.

This preserves the mandatory FARA distinction between an object and a representation. It does not collapse a source item into a bare target label.

## 3. Uniform allocation construction

Let `G_i` be the following construction on `S_i`.

### 3.1 Elements, sorts, and values

For each source element `x in X_i`, allocate a fresh target object `e_x` of kind `encoded_element`.

For each source sort `s`, allocate one target object `sort(s)` of kind `sort_code` and add

\[
has\_sort(e_x,sort(s))
\]

exactly when `x` has source sort `s`.

For each material source value `v in V_i`, allocate a target object `val(v)` of kind `encoded_value`. Exact source values are copied as finite data. When `ValEq` permits a nontrivial source equivalence, the permitted equivalence record is copied into `source_equivalent`; it is not inferred by the target.

All allocations use disjoint tagged namespaces. Therefore distinct source elements remain distinct, materially disjoint source sorts remain distinguishable, and target objects remain distinct from their representations.

### 3.2 Relation occurrences

For every true material source fact

\[
r(x_1,\ldots,x_n),
\]

allocate one fresh target object `q_(r,x)` of kind `relation_occurrence`, one target role-code object `role(r)`, and position-code objects `pos(1)` through `pos(n)`. Add

\[
occurrence\_role(q_{r,x},role(r))
\]

and

\[
argument(q_{r,x},pos(j),e_{x_j})
\]

for every argument position `j`.

No relation-occurrence object is allocated for a false source tuple.

For a source relation symbol `r` of arity `n`, define the declared derived target relation

\[
DR_r(y_1,\ldots,y_n)
\]

by the fixed formula

\[
\exists q\,[occurrence\_role(q,role(r))\land
\bigwedge_{j=1}^{n}argument(q,pos(j),y_j)].
\]

`rho_i(r)=DR_r`. The finite definition template is fixed; `role(r)` and `n` are encoded source data. This is not a source-specific executable decoder or a new target primitive.

### 3.3 Attribute occurrences

For every material source attribute fact

\[
a(x)=v,
\]

allocate a fresh target object `q_(a,x)` of kind `attribute_occurrence`, allocate or reuse `role(a)`, and add

\[
attribute\_owner(q_{a,x},e_x),
\]

\[
attribute\_role(q_{a,x},role(a)),
\]

\[
attribute\_value(q_{a,x},val(v)).
\]

Define the derived target attribute `DA_a` by the fixed formula selecting the unique encoded value linked through an attribute occurrence with role `role(a)`. Set `psi_i(v)=val(v)`.

### 3.4 Interpretation and provenance

For every source element, value, relation role, attribute role, provenance item, and internal evidence-status item, copy its restricted source denotation into `I` through the encoded target object. Source-specific meaning is data under `I`; lexical spelling is not used as a semantic rule.

Every copied provenance and evidence-status fact is placed in `Prov` and connected by explicit target relations. No target evidence grade, certainty, or proof status is generated by inference at W1.

### 3.5 Machinery fragment

The W1 construction records a finite `kappa_W1` fragment containing:

- schema identifier `DIR-INCIDENCE-1.0`;
- the object-kind declarations;
- the fixed relation schema;
- allocation rules;
- the `DR` and `DA` definition templates;
- namespace and disjointness rules;
- the source `ValEq` records actually used;
- target interpretation records;
- provenance and evidence-status fields;
- algorithm identifiers for the executable reference implementation.

`kappa_W1` is a partial machinery ledger for this construction. `LEM-SC-021`, which requires a complete global machinery ledger for the entire witness, remains unproved.

## 4. `LEM-SC-005` — Target carrier allocation

### Finiteness

Every source carrier, relation fact, attribute fact, role family, and value family in `S_i` is finite. The construction allocates finitely many target objects and one representation per target object. Therefore all W1 target components are finite.

### Typing and disjointness

Tagged namespaces and `has_sort` facts preserve source typing. Fresh allocation makes the element map injective. Object and representation namespaces are disjoint. Role codes, sort codes, occurrence nodes, and value nodes are explicitly distinguishable.

### FARA eligibility

The construction uses only FARA's canonical object, property, relation, representation, representational-structure, interpretation, investigation, and provenance-facing components. Derived incidence objects and derived relations are declared and counted. No hidden state or external interpreter is required to state the target structure.

Therefore `LEM-SC-005` is proved.

## 5. Generic strong-embedding theorem

Define

\[
\phi_i(x)=e_x,
\qquad
\psi_i(v)=val(v),
\qquad
\rho_i(r)=DR_r.
\]

### Totality and typing

The allocation rules define `phi_i` on every source element, `psi_i` on every material attribute value, and `rho_i` on every material source relation symbol. Sort facts and disjoint tagged namespaces preserve typing.

### Injectivity

Fresh target allocation gives

\[
x\neq y\Longrightarrow e_x\neq e_y.
\]

Materially disjoint sorts remain distinguishable even if their display labels coincide.

### Relation preservation

If `r(x_1,...,x_n)` is true in the source, the construction allocates its occurrence object with exactly the corresponding role and argument links. Hence

\[
DR_r(e_{x_1},\ldots,e_{x_n})
\]

is true.

### Relation reflection

If `DR_r(e_{x_1},...,e_{x_n})` is true, a target occurrence object with role `role(r)` and those exact ordered arguments exists. Such an occurrence is allocated only from a true source fact. Hence `r(x_1,...,x_n)` is true in the source.

Therefore

\[
r^{S_i}(x)\Longleftrightarrow DR_r^{T_i}(\phi_i(x)).
\]

### Attribute preservation

Every source attribute occurrence is copied exactly. Thus the target value is `psi_i(v)`. Exact equality satisfies the default `ValEq`; any declared source equivalence is copied without strengthening.

### Image accountability

Occurrence, role, sort, value, representation, provenance, and evidence-status objects outside the source-element image are all linked to that image by explicit target relations and declared in `kappa_W1`. No unlinked auxiliary object discharges a preservation obligation.

Consequently `Phi_i=(phi_i,psi_i,rho_i)` is a total typed strong embedding of every finite direct-axis reduct into the W1 target structure.

## 6. Axis constructions

### `LEM-SC-006` — Configuration construction

Apply the generic theorem to `S_1`. Participants, states, resources, locations, externalized components, incidence, availability, containment, ownership, participation, and state-at-location facts are represented by distinct element images and exact typed occurrences. Preservation and reflection follow from Section 5.

Therefore `LEM-SC-006` is proved.

### `LEM-SC-007` — Commitment construction

Apply the generic theorem to `S_2`. Commitment identity, holder, content reference, status, degree, location, retention, acceptance, rejection, suspension, comparison, and revision facts remain distinct target data. Exact role codes prevent acceptance, rejection, suspension, and retention from collapsing unless the source itself declares them equivalent.

Therefore `LEM-SC-007` is proved.

### `LEM-SC-008` — Stake-and-alternative construction

Apply the generic theorem to `S_3`. Stakes, questions, objectives, conflicts, alternatives, live status, mutual exclusion, ranking, availability, relevance, and source location are copied as typed elements, values, and relation occurrences. A selected alternative does not erase the represented alternative set.

Therefore `LEM-SC-008` is proved.

### `LEM-SC-009` — Ground-and-justification construction

Apply the generic theorem to `S_4`. Grounds, constraints, assumptions, observations, rules, models, prior commitments, and every material justificatory endpoint are copied. Support, defeat, qualification, constraint, selection, provenance, and source-specific roles use distinct canonical role-code objects. The derived relation associated with one role cannot create facts for another role.

Therefore `LEM-SC-009` is proved.

### `LEM-SC-012` — Consequence construction

Apply the generic theorem to `S_6`. Consequence identity, content, status, degree, producing transition or justification, downstream use, authorization, inquiry effect, policy effect, proof status, communication effect, and source-specific consequence roles are represented and reflected exactly.

Therefore `LEM-SC-012` is proved.

### `LEM-SC-014` — Internal evidential-status construction

Apply the generic theorem to `S_8I`. Observation versus inference, reported versus instrumented status, assumed versus derived status, provenance source, confidence, uncertainty, qualification, rejection, supersession, withdrawal, unresolved status, and evidence grade are copied into `Prov` and the incidence structure.

Because every status and grade is copied exactly, the target cannot license a stronger internal evidence-status fact through this construction. Any changed or added stronger status would be a spurious target relation or attribute and would violate reflection or attribute preservation.

Therefore `LEM-SC-014` is proved.

## 7. Isomorphism behavior

Let `f:S_i -> S'_i` be a source isomorphism transported by W0. Define the induced target map by

- `e_x -> e_(f(x))`;
- `val(v) -> val(f(v))` where values are transported;
- `role(r) -> role(f(r))`;
- relation and attribute occurrence objects to the occurrence generated from the transported fact;
- representations to representations of the mapped target objects.

The induced map preserves and reflects every fixed incidence relation. Thus the W1 constructor is equivariant under source isomorphism at the direct-axis level. This supports, but does not by itself prove, the global uniformity obligation `LEM-SC-022`.

## 8. Obstruction results

### `OBS-SC-003` — Relation-reflection collapse

`OBS-SC-003` asks whether an in-scope commitment, stake-and-alternative, or ground-and-justification reduct necessarily collapses material relations under the fixed target interface without unregistered machinery.

Sections 2–6 give one uniform declared construction for every finite `S_2`, `S_3`, and `S_4` reduct. Every source relation symbol is represented by a distinct role-code parameter to the fixed `DR` schema, and every true tuple has exactly one or more corresponding occurrence records while false tuples have none. Therefore relation preservation and reflection hold for arbitrary finite reducts in the registered scope.

Accordingly the existential impossibility proposed by `OBS-SC-003` is refuted. This does not rule out failures caused by later global coherence, semantics, recovery, or machinery-ledger obligations.

### `OBS-SC-006` — Evidential-status impossibility

`OBS-SC-006` asks whether some in-scope internal evidence-status reduct cannot be preserved without loss, fabrication, or upgrade.

Section 6 constructs an exact copy strong embedding for arbitrary finite `S_8I` reducts. Exact copying preserves every status and grade, reflection prevents fabricated represented-image statuses, and no-upgrade follows because the target value equals the source value under the source contract.

Accordingly the registered direct-axis evidential-status impossibility is refuted. External process-to-presentation correspondence `Corr_8E` remains entirely separate and unproved.

## 9. Dependency closure

| Obligation | Result | Dependencies used |
|---|---|---|
| `LEM-SC-005` | proved | `LEM-SC-002`, `LEM-SC-004`; fixed finite incidence schema |
| `LEM-SC-006` | proved | `LEM-SC-005`; generic strong-embedding theorem on `S_1` |
| `LEM-SC-007` | proved | `LEM-SC-005`; generic strong-embedding theorem on `S_2` |
| `LEM-SC-008` | proved | `LEM-SC-005`; generic strong-embedding theorem on `S_3` |
| `LEM-SC-009` | proved | `LEM-SC-005`; generic strong-embedding theorem on `S_4` |
| `LEM-SC-012` | proved | `LEM-SC-005`, `LEM-SC-007`, `LEM-SC-009`; generic theorem on `S_6` |
| `LEM-SC-014` | proved | `LEM-SC-005`, `LEM-SC-007`, `LEM-SC-009`; exact `S_8I` embedding |
| `OBS-SC-003` | refuted | `LEM-SC-007`, `LEM-SC-008`, `LEM-SC-009` |
| `OBS-SC-006` | refuted | `LEM-SC-014` |

## 10. What is and is not established

W1 establishes finite target allocation and direct-axis strong embeddings. It does not yet establish the full predicates `Pres_i`, because the frozen definition of `Pres_i` additionally requires admissible target-only recovery. That dependency is registered as `LEM-SC-018`.

W1 also does not prove:

- deterministic or probabilistic dynamics;
- history or path preservation;
- nonmonotonic revision or self-modification;
- one admissible recovery family;
- global semantic agreement;
- cross-axis coherence;
- complete machinery accounting for the full witness;
- global uniformity and compositional accountability;
- a well-formed witness or common-schema theorem.

## 11. Executable reference evidence

`tools/s_core_w1_reference.py` implements the fixed incidence allocation, derived relation and attribute recovery, direct-axis verification, and internal evidence-status no-upgrade checks. `tests/test_s_core_w1_reference.py` checks:

- object/representation separation;
- injection and sort preservation;
- relation preservation and reflection;
- attribute preservation;
- support/defeat role noncollapse;
- live-alternative preservation;
- consequence-role preservation;
- evidential-status exactness and upgrade rejection;
- alpha-renaming independence;
- rejection of spurious target relations and collapsed images.

These executions corroborate the construction and protect against implementation drift. They do not constitute proof-assistant verification or independent review.

## 12. Result and next dependency

The lemma ledger now records eleven proved construction lemmas, one established source-scope boundary, two refuted obstruction hypotheses, and twenty-three open obligations. W0 and W1 are complete. W2 is active:

- `LEM-SC-010` — deterministic dynamics construction;
- `LEM-SC-011` — finite-support probabilistic dynamics construction;
- `LEM-SC-013` — historical-and-path construction;
- `LEM-SC-015` — nonmonotonic revision and retraction;
- `LEM-SC-016` — self-modification and rule-version change.

## Nonclaims

This proof does not establish:

- a complete target package and witness for any arbitrary `S_core` episode;
- admissible target-only recovery or any complete `Pres_i` predicate;
- `Faithful_split` satisfiability;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- actual-process correspondence;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review.
