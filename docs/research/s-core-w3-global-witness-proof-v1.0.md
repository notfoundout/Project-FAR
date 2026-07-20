# S_core W3 Global-Witness Construction Proof v1.0

## Status

Human-checkable project-authored proof package for `LEM-SC-017` through `LEM-SC-024`.

It also refutes `OBS-SC-002`, `OBS-SC-007`, `OBS-SC-008`, and `OBS-SC-009` over their registered finite `S_core` scopes.

Proof identifier: `SCORE-W3-PROOF-001`.

This is internal mathematical work. It has not been checked by a proof assistant or independently reviewed. The accompanying executable implementation is bounded corroboration only.

## Governing artifacts

This proof is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/research/s-core-construction-obstruction-ledger-v1.0.md`;
- `docs/research/s-core-w0-normalization-proof-v1.0.md`;
- `docs/research/s-core-w1-direct-axis-proof-v1.0.md`;
- `docs/research/s-core-w2-dynamics-history-proof-v1.0.md`;
- `theory/definitions/definitions.md`;
- `frameworks/FARA/architecture.md`;
- `frameworks/FARA/primitives.md`.

The machine-readable result is `theory/evaluation/s-core-w3-global-witness-proof.json`.

## 1. Scope and dependency boundary

Fix an arbitrary admitted source object

\[
S=(P,J,C_S)\in S_{core}
\]

and its W0-normalized finite source contract. W0 supplies finite typed carriers, materiality closure, canonical reducts, applicability, source interpretation, value-equivalence records, and source-isomorphism transport. W1 supplies finite strong embeddings for P1, P2, P3, P4, P6, and P8-I. W2 supplies finite deterministic and finite-support probabilistic dynamics, material history and path, revision, retraction, and operational rule-version change.

W3 must construct one integrated theorem-facing package and prove the global witness obligations. It may use the accepted W0-W2 results, but it may not assume:

- a hidden interpreter or source oracle;
- source reaccess during recovery;
- a case database or case identifier branch;
- evaluator repair;
- unregistered metadata;
- the formal negative-control result `OBS-SC-010`;
- `Faithful_split` satisfiability;
- any W5 assembly result;
- FARA adequacy, universality, necessity, or minimality.

## 2. Fixed integrated target schema

Define one fixed integrated schema `FARA-WITNESS-1.0` with target

\[
A^*=(U,\Pi,R,Rep,S,I,Inv,C,\Sigma,\Theta,H,\Omega,Res,Prov).
\]

The schema is independent of the source case. It combines the accepted W1 incidence construction and W2 dynamics/history construction through tagged allocation and a shared-identity quotient.

### 2.1 Tagged allocation

For each material source entity `x` of source sort `s`, allocate one target object

\[
e_x=\langle entity,s,x\rangle.
\]

For each source sort, relation role, attribute role, cross-component role, value, argument position, component, interface, relation occurrence, attribute occurrence, transition, event, rule, and rule version, allocate a corresponding tagged target object. The tags are mathematical constructors, not lexical labels. Freshness and tag disjointness make allocation injective.

The executable reference uses deterministic digest tokens to name these abstract tagged objects. Collision freedom of a concrete digest is not a premise of this proof; the proof relies on abstract fresh tagged allocation.

### 2.2 Shared-identity quotient

If the same source entity occurs in multiple axes or in both a direct axis and dynamics/history, all occurrences use the same target object `e_x`. Distinct source identities are never merged. Relation and attribute occurrence objects remain separate from their arguments and from their representations.

Therefore the quotient identifies exactly repeated uses of one source identity and nothing else.

### 2.3 Object-representation separation

For every target object `u`, allocate a distinct representation `rep(u)` and add:

\[
represented\_by(u,rep(u)),\qquad denotes(rep(u),u).
\]

The object and representation carriers are disjoint. This preserves the canonical FARA distinction between what is represented and the representation that denotes it.

### 2.4 Integrated components

The target components have the following fixed roles:

- `U`, `Pi`, `R`, `Rep`, and `S` contain typed carriers, fixed incidence relations, and representations;
- `I` contains explicit interpretation records for material entities, source sorts, relation roles, attribute roles, and cross-component roles;
- `Inv` identifies the frozen theorem investigation and scope;
- `C`, `Sigma`, `Theta`, `H`, and `Omega` contain the W2 rule, state, transition, history, and status structures;
- `Res` contains source-declared components, interfaces, membership, interface links, and cross-component relations;
- `Prov` contains internal evidential and historical provenance;
- the witness contains `E`, `D`, `M`, `iota`, and `kappa`.

No new FARA primitive is added. Every helper object is derived target data and is declared in the machinery ledger.

## 3. `LEM-SC-017` — Distributed decomposition and interface construction

Suppose the source declares a decomposition

\[
S=S_1\oplus_B S_2
\]

or any finite family of components with finite declared interfaces.

For every source component `K`, allocate a target component object `comp(K)`. For every source interface `B`, allocate `int(B)`. Copy exactly:

- component membership;
- interface membership;
- interface-to-component incidence;
- cross-component relation occurrences and ordered arguments;
- component and interface participation in material histories and dynamics.

The component and interface maps are injective by tagged allocation. A source cross-component relation is true exactly when its explicit target occurrence with the corresponding role and ordered argument images exists. No whole-episode fact is attributed to a component unless the source membership or interface declaration supports it.

For an indecomposable source declaration, the same fixed constructor records one component and no nontrivial interface. No special source-case branch is required.

Therefore `LEM-SC-017` is proved.

## 4. `LEM-SC-018` — Admissible target-only recovery

### 4.1 Recovery interface

Define the fixed recovery family `RECOVER-FARA-1.0`. Its input is only:

1. the completed target `A*`;
2. the declared recovery descriptor `D`;
3. the declared machinery ledger `kappa`.

The recovery algorithm does not read `S`, `E`, `M`, an external narrative, a case identifier, a network resource, an evaluator response, or a source oracle.

### 4.2 Recovery procedure

The algorithm performs the following finite operations:

1. validate the fixed target schema and the complete machinery ledger;
2. enumerate target objects, representations, properties, and fixed relations;
3. reconstruct target-local carrier identities and sorts from `has_sort`;
4. reconstruct each direct-axis reduct from `axis_member`, `in_axis`, occurrence roles, ordered arguments, owners, and values;
5. reconstruct rules, versions, states, transitions, exact finite weights, statuses, and live-transition conditions from `C`, `Sigma`, `Theta`, and `Omega`;
6. reconstruct events, order, causality, provenance, revision, modification, ancestry, and path conditions from `H`;
7. reconstruct interpretations and source-declared equivalence records from `I` and `source_equivalent`;
8. reconstruct components, interfaces, membership, links, and cross-component relations from `Res`;
9. emit a canonical target-indexed recovered contract or a deterministic diagnostic.

The output identities are target-local object identities. Recovery does not need to reproduce lexical source names because `E` supplies the typed source-to-target correspondence used by the preservation predicates.

### 4.3 Termination

Every admitted target is finite. Every recovery stage is a bounded traversal, finite grouping, finite sort, finite graph validation, or finite exact-rational check. Therefore recovery terminates.

### 4.4 Purity and determinism

All choices are fixed by the schema and canonical ordering. The algorithm has no environment-dependent input. Hence recovery is deterministic and pure.

### 4.5 Correctness

For every W1 direct-axis occurrence, recovery selects exactly the copied role and ordered arguments. W1 preservation and reflection therefore imply that the recovered target-local reduct is isomorphic to the source reduct through the accepted correspondence maps.

For every W2 state, transition, kernel branch, event, history relation, revision, and modification, recovery reads the exact copied record. W2 preservation and reflection imply that the recovered dynamics and history are isomorphic to the source structures.

Thus the fixed recovery family reconstructs every applicable P1-P7 and P8-I reduct up to the frozen source correspondence and value equivalence, without source reaccess or hidden machinery.

Therefore `LEM-SC-018` is proved.

## 5. `LEM-SC-019` — Semantic agreement

Let `den_S(z)` be the frozen source denotation of a material entity, role, sort, or value-equivalence record. The constructor adds an interpretation record

\[
I(e_z)=val(den_S(z))
\]

for each material entity and the corresponding interpretation record for each encoded role and sort. Source-declared value-equivalence rules are copied exactly into explicit target records.

The constructor does not infer meaning from display labels, identifier spelling, or target naming. It does not strengthen certainty, modality, authority, normativity, evidence grade, or precision. Exact copied denotation satisfies the source equivalence by reflexivity; a nontrivial equivalence is used only when explicitly owned by the source contract.

Shared source identities reuse one semantic subject, so the same material item cannot receive conflicting denotations across axes. A conflict in the source contract is rejected during well-formedness validation rather than repaired by the target.

Therefore `LEM-SC-019` is proved.

## 6. `LEM-SC-020` — Cross-axis coherence

Define the global entity map

\[
E(x)=e_x.
\]

Every per-axis map is the restriction of `E` to that axis. Hence a source item shared by P1, P2, P3, P4, P6, P8-I, dynamics, or history has one target image.

The construction also reuses:

- one sort-code object for each source sort;
- one role-code object for each source role identity and role kind;
- one value object for each exact finite source value;
- one rule-version object at every state, transition, and modification reference;
- one event object across direct-axis location, history, provenance, and decomposition records.

Deliberate duplication is limited to declared representations and occurrence records. Each duplicate is typed, linked, and counted in `kappa`. Statuses, versions, denotations, and provenance records are therefore compatible across axes.

Consequently the per-axis and dynamic/history constructions form one coherent integrated target.

Therefore `LEM-SC-020` is proved.

## 7. `LEM-SC-021` — Complete machinery-ledger construction

Define `kappa*` as a finite directed dependency graph. Its nodes include:

- the integrated, W1, and W2 schemas;
- source validation;
- tagged allocation;
- direct-axis construction;
- dynamics/history construction;
- semantic interpretation construction;
- decomposition construction;
- target-only recovery;
- witness verification;
- component restriction;
- source-owned interpretation and value-equivalence bridges.

Every field of `A*` and every field of `W=(E,D,M,iota,kappa)` has exactly one declared producer node. Every algorithm, schema, semantic bridge, normalization rule, equivalence rule, composition rule, and cost-bearing helper used by construction, recovery, interpretation, or verification appears in the graph.

The graph is acyclic under the stage order

\[
validate < allocate < \{direct,dynamics,semantics,decomposition\} < recover < verify.
\]

External dependencies are empty. Flags for source oracle, case database, network access, evaluator repair, and undeclared executable machinery are false. Missing producers, unknown dependencies, or cycles make the witness inadmissible.

Therefore `LEM-SC-021` is proved.

## 8. `LEM-SC-022` — Uniformity and source-isomorphism equivariance

### 8.1 One finite definition

The constructor and recovery family have one versioned schema and one finite algorithmic definition. Their loops range over finite typed records. They do not branch on source case identifiers or lexical labels.

### 8.2 Effectiveness and termination

W0 provides an effective finite normalized input. Every W3 construction and recovery operation is finite and effective. Therefore the family terminates on all of `S_core`.

### 8.3 Equivariance

Let

\[
f:S\cong S'
\]

be a source isomorphism preserving source sorts, material relations, values under the declared equivalence, dynamics, history, interpretation, and decomposition.

Define the induced target map by:

\[
\hat f(e_x)=e_{f(x)}
\]

and analogously on source-indexed occurrences, components, interfaces, transitions, events, rules, and versions. Fixed axis codes, argument-position codes, schemas, and unchanged source values remain fixed. Role, sort, and value codes are transported by the corresponding source isomorphism.

Because every target fact is generated by one fixed local rule from a source fact, `hat f` preserves and reflects every target relation and component. It is bijective by source-isomorphism bijectivity and tagged allocation. Recovery commutes with `hat f` because it uses only the fixed target relations and canonical target-local identities.

Thus source-isomorphic inputs produce target-isomorphic outputs and recovered-isomorphic contracts.

Therefore `LEM-SC-022` is proved.

## 9. `LEM-SC-023` — Compositional accountability

For a declared component `K`, let `cl(K)` contain:

- members explicitly assigned to `K`;
- members of every interface linked to `K`;
- the local occurrence, dynamic, and history records whose material endpoints lie in that closure;
- explicit cross-component records incident on the closure.

The target restriction `A*|K` is the induced typed substructure on the images of `cl(K)` plus the fixed schema objects needed to interpret those records.

The constructor is local: it allocates an entity from that entity, an occurrence from that occurrence and its endpoints, a transition from that transition and referenced state/version objects, and a history record from that source history record. Therefore encoding the source restriction and restricting the whole target generate the same typed records up to the induced target isomorphism:

\[
Encode(S|K)\cong Encode(S)|K.
\]

Interfaces and cross-component relations remain explicit, so restriction does not erase interaction structure. Composed histories retain their source-declared cross-component event order and ancestry. No component receives unsupported whole-episode responsibility.

Therefore `LEM-SC-023` is proved.

## 10. `LEM-SC-024` — Well-formed witness assembly

Define

\[
W^*=(E^*,D^*,M^*,\iota^*,\kappa^*),
\]

where:

- `E*` is the total typed entity and occurrence correspondence;
- `D*` is `RECOVER-FARA-1.0`;
- `M*` contains the typed sort, role, value, axis, dynamics, history, component, and interface correspondences;
- `iota*` identifies the explicit interpretation component and source-owned semantic equivalence;
- `kappa*` is the complete finite machinery ledger.

By Sections 2-9:

- `A*` is a well-formed FARA target using the frozen interface;
- `E*` and `M*` are total and typed;
- `D*` is admissible, deterministic, terminating, and target-only;
- W1 and W2 embeddings plus W3 recovery establish every applicable complete P1-P7 and P8-I preservation predicate;
- semantic agreement holds;
- cross-axis coherence holds;
- uniformity and equivariance hold;
- compositional accountability holds;
- machinery accounting is complete.

Hence `W*` is a well-typed integrated witness satisfying all construction and recovery clauses registered before the formal negative-control requirement.

This proof does not mark `Faithful_split` proved because the registered formal negative-control family and the global `Nontrivial` conclusion remain `OBS-SC-010`, and the theorem-level assembly obligations remain W5.

Therefore `LEM-SC-024` is proved.

## 11. Obstruction results

### 11.1 `OBS-SC-002` — Hidden-interpreter necessity — refuted

`D*` recovers every admitted finite target using only `A*`, its fixed descriptor, and its declared finite machinery ledger. It does not use `S`, `E`, `M`, a source oracle, a case database, or evaluator repair. Therefore no admitted `S_core` object requires an unrestricted hidden interpreter within the registered class.

`OBS-SC-002` is refuted.

### 11.2 `OBS-SC-007` — Nonuniform-constructor obstruction — refuted

Sections 2 and 8 define one finite constructor and prove source-isomorphism equivariance. No source case identifiers or unbounded family of helper definitions is required.

`OBS-SC-007` is refuted.

### 11.3 `OBS-SC-008` — Composition-interface loss — refuted

Sections 3 and 9 construct explicit component, interface, membership, cross-relation, and history records and prove restriction commutation. Therefore every admitted finite source-declared decomposition has an accountable target image.

`OBS-SC-008` is refuted.

### 11.4 `OBS-SC-009` — Fixed-target-interface insufficiency — refuted

Section 10 assembles a well-formed witness for an arbitrary admitted finite source object using the frozen target interface and no new primitive. Therefore the registered finite `S_core` class contains no demonstrated source requiring an enlarged target interface for witness construction.

This refutation does not establish the final representation theorem because `OBS-SC-010` and W5 remain open.

`OBS-SC-009` is refuted.

## 12. Executable corroboration

The reference implementation `tools/s_core_w3_reference.py` implements the fixed integrated constructor, target-only recovery, semantic comparison, coherence checks, machinery validation, component views, and witness verification.

The test suite covers:

- complete baseline witness construction;
- target-only recovery after removing `E` and `M`;
- direct relation loss;
- undeclared occurrence injection;
- semantic mutation;
- shared-image collapse;
- source sort conflict;
- machinery cycles;
- missing machinery producers;
- interface loss;
- hidden external dependencies;
- display-label invariance;
- source-isomorphism equivariance;
- interface and cross-relation retention in component views;
- replacement of the fixed recovery algorithm.

These finite tests corroborate the construction. They do not prove the quantified mathematical result, exhaust all malformed targets, or constitute independent review.

## 13. Dependency audit

This proof uses only:

- frozen W0 source normalization and transport;
- accepted W1 direct-axis constructions;
- accepted W2 dynamics/history constructions;
- the frozen faithful-representation and P8 split definitions;
- finite source-owned interpretation and equivalence data;
- source-declared decomposition when applicable.

It does not use:

- `OBS-SC-010` or any assumption that the negative controls fail;
- `ASM-SC-001`, `ASM-SC-002`, or `ASM-SC-003`;
- `Faithful_split` as a premise;
- PB-001 sufficiency or completeness;
- actual-process correspondence;
- primitive necessity or minimality;
- proof-assistant verification or independent review.

No premise, source scope, target interface, preservation definition, P8 boundary, or lemma statement is changed.

## 14. Ledger and gate effects

After this package:

- all 24 construction lemmas are proved;
- 8 obstruction hypotheses are refuted;
- 1 source-scope boundary is established;
- 4 obligations remain open;
- W0 through W3 are complete;
- W4 is active with `OBS-SC-010`;
- W5 remains open with `ASM-SC-001` through `ASM-SC-003`.

The formal-theorem-target, premise-ledger-and-semantics, and faithful-representation-definition gates remain satisfied.

The scoped-representation-proof gate remains not satisfied because formal negative controls and theorem assembly remain open. Mechanized-proof-verification and independent-proof-review remain not satisfied.

## 15. Stronger nonclaims

This proof does not establish:

- the formal negative-control family `OBS-SC-010`;
- the global `Nontrivial` conjunct;
- `Faithful_split` satisfiability;
- any W5 assembly obligation;
- `THM-CORE-COMMON-001` or `THM-CORE-REP-001`;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- actual-process correspondence;
- a universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification;
- independent proof review.

## 16. Exact next work

Execute `OBS-SC-010` as a formal negative-control package covering NC-01 through NC-10. If it passes without exposing a countermodel or hidden commitment, execute W5 assembly and derive the strongest justified finite-core theorem or obstruction.
