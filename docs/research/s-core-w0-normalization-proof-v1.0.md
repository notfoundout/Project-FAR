# S_core W0 Normalization Kernel Proof v1.0

## Status

Human-checkable project-authored proof package for `LEM-SC-001` through `LEM-SC-004`, with `OBS-SC-001` resolved as a source-scope boundary.

Proof identifier: `SCORE-W0-PROOF-001`.

This result is internal proof work. It has not been independently reviewed or machine-checked in a proof assistant. The executable reference implementation and tests accompanying this document validate the registered algorithms on finite fixtures; they are not substitutes for the mathematical proof.

## Governing artifacts

This proof is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/thm-target-001.json`;
- `theory/evaluation/thm-target-001-premise-ledger.json`;
- `docs/research/independent-reasoning-definition-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/research/s-core-construction-obstruction-ledger-v1.0.md`.

The machine-readable result is `theory/evaluation/s-core-w0-normalization-proof.json`.

## 1. Scope and assumptions

Fix a well-formed theorem-facing source object

\[
(P,J,C_S)\in S_{core},\qquad C_S=(\tau_S,\mathsf{Mat},\mathsf{ValEq},\mathsf{App}).
\]

Only the material episode-restricted part of `C_S` is relevant. Define its **material universe** `U_C` as the disjoint typed union of:

- event positions in `J`;
- material source elements and material attribute values;
- material relation and attribute occurrences;
- transition, condition, rule, and rule-version records;
- history, dependency, revision, retraction, and supersession records;
- provenance and internal evidence-status records;
- interpretation and value-equivalence clauses needed to interpret the preceding items.

Under the frozen definition of `S_core`, `J` and every material carrier used by R1–R6 are finite; admissible dynamics are an explicit finite relation or finite-support kernel; and all material history, support, interpretation, and revision distinctions are explicit. Therefore `U_C` is finite.

Let `Ref_C(x,y)` mean that material item `x` directly refers to item `y` and requires it for interpretation. `Ref_C` includes argument incidence, attribute ownership, transition preconditions, rule-version references, support endpoints, provenance links, history ancestry, semantic bridges, and value-equivalence dependencies. Well-formedness requires both endpoints to belong to `U_C`.

Let `M_0` be the finite set of initially declared material items. Define materiality closure by

\[
M_{n+1}=M_n\cup\{y\in U_C\mid \exists x\in M_n\;Ref_C(x,y)\},
\]

and

\[
Cl_C(M_0)=\bigcup_{n\ge 0}M_n.
\]

For each axis `i` in `1,...,7,8I`, let `Tag_i` be the finite source-declared set of closed material items belonging to that axis. Attributes are represented as typed relation occurrences for this proof, so no separate case is required.

## 2. `LEM-SC-001` — Finite source-contract normalization

### Statement

Every `(P,J,C_S) in S_core` admits an effective finite normalized source contract preserving the source interpretation, materiality, value equivalence, applicability, R1–R6 truth, and every material dependency.

### Construction

Restrict `tau_S` to the finite material sub-signature `tau_C^mat` consisting of the sorts, relation symbols, attribute symbols, and interpretation symbols that occur in `U_C`. Unused symbols have no theorem-facing material occurrence and are omitted from the reduct, not declared semantically absent from the original presentation.

For each non-rigid finite carrier sort `s`, let its cardinality be `n_s` and let its canonical carrier be the initial segment

\[
[s]=\{(s,0),\ldots,(s,n_s-1)\}.
\]

Rigid semantic constants fixed by the source interpretation remain fixed. Every other material value is included in a typed finite carrier and renamed with that carrier.

Enumerate the finite nonempty set `B_C` of all sort-preserving bijections from the material carriers to their canonical initial segments. For each `b in B_C`, transport every material relation occurrence, attribute occurrence, reference edge, interpretation clause, `ValEq` clause, materiality declaration, and axis tag along `b`. Encode the transported finite structure using a fixed prefix-free ordering of sorts, symbols, tuples, and finite value records. Define

\[
Norm(C_S)=\min_{lex}\{Code(b\cdot C_S)\mid b\in B_C\}.
\]

The minimum exists because `B_C` is finite and nonempty and the codes are finite strings in a total lexicographic order. A witnessing bijection is retained as the normalization map.

### Preservation proof

Each candidate `b` is a typed source isomorphism on the material episode-restricted structure. It preserves and reflects all material relation and attribute facts by transport. Interpretation clauses and `ValEq` are transported rather than recomputed, so no semantic strengthening or weakening occurs. `Mat`, `Ref_C`, and the axis tags are transported pointwise. R1–R6 truth is invariant because the isomorphism preserves the complete episode structure and declared interpretation used to evaluate those clauses.

Consequently the selected canonical representative is isomorphic to the source material contract and preserves every theorem-facing distinction. The procedure is effective: all carriers and facts are finite, the finite bijection set can be enumerated, and finite codes can be compared. Efficiency is not claimed; only termination and uniform definability are required at W0.

Therefore `LEM-SC-001` is proved.

## 3. `LEM-SC-002` — Canonical reduct extraction

### Statement

From the normalized source contract, effectively extract the least finite typed reducts `S_1` through `S_7` and `S_8I`, including their materiality-closure dependencies.

### Construction

First compute `M=Cl_C(M_0)`. For each axis `i`, define the axis seed

\[
A_i=M\cap Tag_i.
\]

Define

\[
U_i=Cl_C(A_i)\cap M.
\]

The reduct `S_i` is the typed induced relational structure on `U_i`, containing every material relation or attribute occurrence whose occurrence-node and required endpoints lie in `U_i`, together with the restricted source interpretation and value-equivalence clauses required by those occurrences.

### Leastness and uniqueness

`U_i` contains `A_i` and is closed under `Ref_C`. Let `Y subseteq M` be any `Ref_C`-closed set containing `A_i`. By induction on path length, every node reachable from `A_i` lies in `Y`; hence `U_i subseteq Y`. Therefore `U_i` is the unique least closed carrier supporting the axis seed.

Because `M` is finite, every `U_i` and every induced fact set is finite. Breadth-first or depth-first reachability computes each `U_i`, and finite filtering computes each induced reduct. The construction applies uniformly to P1–P7 and the internal P8-I evidential-status reduct.

Therefore `LEM-SC-002` is proved.

## 4. `LEM-SC-003` — Materiality closure and applicability decidability

### Closure termination

The sequence `M_0 subseteq M_1 subseteq ...` is monotone and every `M_n` is a subset of finite `U_C`. Whenever `M_{n+1}` differs from `M_n`, at least one previously absent item is added. Therefore strict growth can occur at most `|U_C|-|M_0|` times. For some `k <= |U_C|`,

\[
M_k=M_{k+1}=Cl_C(M_0).
\]

Cycles in `Ref_C` do not threaten termination: reachability uses a visited set, and a finite directed cycle adds no new item after its members have been visited.

### Closure completeness

Induction on reference-path length shows that every item reachable from `M_0` belongs to `M`. Conversely, each item added at stage `n+1` is reachable by extending a path to an item in `M_n`. Thus the fixed point equals finite graph reachability and includes exactly the dependencies required by the frozen materiality rule.

### Applicability

For each axis,

\[
App_i(P,J)\iff A_i\ne\varnothing.
\]

Equivalently, the canonical axis reduct contains at least one material axis distinction or relation occurrence. Since `M` and `Tag_i` are finite explicit sets, emptiness is decidable. An `unknown` applicability value is therefore a malformed `S_core` contract, not a theorem result.

Therefore `LEM-SC-003` is proved.

## 5. `LEM-SC-004` — Source-isomorphism transport

### Source-isomorphism definition

A source isomorphism `f:C -> C'` is a family of sort-preserving bijections that preserves and reflects:

- every material relation and attribute occurrence;
- the event partial order and finite-support weights;
- `M_0`, `Ref_C`, and every `Tag_i`;
- interpretation, provenance, evidence status, and `ValEq` clauses;
- rigid constants.

### Closure transport

For every `n`, prove by induction that

\[
f[M_n]=M'_n.
\]

The base case follows from preservation of `M_0`. For the step, preservation and reflection of `Ref_C` imply that the direct successors of `f[M_n]` are exactly the images of the direct successors of `M_n`. Taking unions gives the result. Hence

\[
f[Cl_C(M_0)]=Cl_{C'}(M'_0).
\]

The same argument starting from `A_i` yields

\[
f[U_i]=U'_i,
\]

so reduct extraction commutes with isomorphism and `f|U_i` is an isomorphism `S_i ~= S'_i` for every axis.

### Canonical normalization transport

Composition with `f^{-1}` is a bijection between the sort-preserving canonical-label bijections of `C` and those of `C'`. Corresponding transported structures have identical finite codes. Therefore the two finite code sets are equal and

\[
Norm(C)=Norm(C').
\]

Thus normalization is canonical on source-isomorphism classes, while the recorded witness maps provide the induced transport. No case identifier, source name, or lexical label controls the result.

Therefore `LEM-SC-004` is proved.

## 6. `OBS-SC-001` — Non-finite material-closure boundary

Assume `(P,J,C_S)` is a well-formed member of `S_core`. By Section 1, `U_C` is finite and `Ref_C subseteq U_C x U_C`. Section 4 proves that materiality closure stabilizes after finitely many additions. Therefore no admitted `S_core` object has non-finite or nonterminating mathematical materiality closure.

A purported source with an infinite material carrier, an infinite-support material kernel, an open-ended material history, or a reference to indefinitely many undeclared items violates the frozen `S_core` requirements and belongs, if anywhere, to `S_IRD`. A program that loops on a finite reference cycle without recording visited nodes has an implementation defect; it is not a countermodel to closure termination.

Accordingly `OBS-SC-001` is resolved as `scope_boundary_established`, not as a target obstruction and not as evidence for FARA.

## 7. Dependency closure

| Obligation | Result | Dependencies used |
|---|---|---|
| `LEM-SC-001` | proved | frozen `S_core` finiteness and explicitness clauses |
| `LEM-SC-002` | proved | `LEM-SC-001`; finite reachability and induced reduct construction |
| `LEM-SC-003` | proved | `LEM-SC-001`, `LEM-SC-002`; stabilization of monotone subsets of a finite set |
| `LEM-SC-004` | proved | `LEM-SC-001`–`003`; transport of finite relational structures |
| `OBS-SC-001` | scope boundary established | `LEM-SC-001`, `LEM-SC-003` |

No FARA target component, constructor, recovery procedure, or faithfulness assumption is used. W0 is source-side only.

## 8. Executable reference evidence

`tools/s_core_w0_reference.py` implements finite dependency closure, axis-reduct extraction, applicability, source renaming, and canonical-code comparison. `tests/test_s_core_w0_reference.py` checks closure completeness, cycle termination, applicability, reduct transport, canonical invariance, and rejection of undeclared dependencies against the registered fixtures.

These executions corroborate the definitions and protect the repository against implementation drift. They do not elevate this result to proof-assistant verification or independent review.

## 9. Result and next dependency

W0 is complete. The lemma ledger now has four proved construction obligations and one established source-scope boundary. The next dependency wave is W1:

- `LEM-SC-005` — target carrier allocation;
- `LEM-SC-006` — configuration construction;
- `LEM-SC-007` — commitment construction;
- `LEM-SC-008` — stake-and-alternative construction;
- `LEM-SC-009` — ground-and-justification construction;
- `LEM-SC-012` — consequence construction;
- `LEM-SC-014` — internal evidential-status construction.

## Nonclaims

This proof does not establish:

- any W1–W5 obligation;
- existence of a FARA target package or uniform FARA constructor;
- `Pres_1` through `Pres_8I` for a target witness;
- satisfiability of `Faithful_split`;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- correspondence between an actual process and an IRD presentation;
- universality, necessity, minimality, equivalence, uniqueness, or impossibility;
- proof-assistant verification or independent proof review.
