# Project FAR Core Theory v1.1 — Corrected Successor

## Contract-Relative Representation, Sufficiency, and Audit

**Status:** **GOVERNED CORRECTED SUCCESSOR**

**Date:** 2026-08-27

**Theory identity:** `PROJECT-FAR-CORE-THEORY-1.1`

**Supersedes as current authority:** `PROJECT-FAR-CORE-THEORY-1.0`

**Preserves without modification:** `theory/theorems/Project-FAR-Theory-Closure-v1.0.md`

**Preserved v1.0 SHA-256:** `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`

**Assurance:** internal deductive correction after a non-independent hostile audit; not independently reviewed.

**Terminal verdict — unchanged:**

> **NONTRIVIAL CONTRACT-FREE MINIMAL ARCHITECTURE IS IMPOSSIBLE; CONTRACT-RELATIVE SUFFICIENCY AND A UNIQUE MINIMAL OBSERVATIONAL QUOTIENT ARE PROVED.**

## 0. Version semantics

This document is a versioned correction to the accepted v1.0 monograph. The v1.0 bytes and hash are historical evidence and MUST NOT be rewritten. `PROJECT-FAR-CORE-THEORY-1.1` incorporates v1.0 except where this document explicitly replaces a statement, scope, proof sentence, or prior-art characterization.

No surviving terminal-kernel theorem is altered except the exact wording and dependency statement of `FAR-CORE-004` and `FAR-CORE-010`. `FAR-CORE-014` remains `SUPPORTED/DERIVED`. The factorization theorem, observational-quotient theorem, dynamic descent theorem, invariance/transport/noninvariance results, finite-panel boundary, omitted-parameter result, Unknown-separation result, Ω elimination, and SSS classification retain their v1.0 scopes and proofs.

The correction was triggered by a hostile W1 audit that did not satisfy evaluator-independence requirements. Its defects are therefore admissible internal counterevidence, but its existence does not upgrade assurance to independent review.

---

## 1. Correction to FAR-CORE-004

### 1.1 Replaced machine-readable claim

The v1.0 ledger wording

> `no contract-free least-informative representation is sufficient for every observation contract`

is ambiguous and admits a false reading. The identity representation is sufficient for every observation contract on a fixed set of cases because it never identifies distinct cases. What fails is **simultaneous least-informativeness/minimality**, not universal sufficiency.

The corrected claim is:

> **On every nontrivial domain, no single representation is simultaneously a least-informative sufficient representation for every observation contract.**

### 1.2 Exact proof

Let `X` be any set with at least two elements.

Choose two exact observation contracts on `X`:

- `C0`, whose behavior map `β0` is constant. Then `ker(β0)=X×X`, and the unique least-informative sufficient quotient has one equivalence class.
- `C1`, whose behavior map `β1` is injective. Then `ker(β1)=ΔX`, and the unique least-informative sufficient quotient has one class per element of `X`.

A representation that is least-informative for `C0` identifies every pair and therefore is not sufficient for `C1`. A representation least-informative for `C1` distinguishes every pair and therefore is not least-informative for `C0`.

Thus no one representation is least-informative sufficient for both contracts, hence none is least-informative sufficient for every observation contract on a nontrivial `X`. ∎

### 1.3 Clarifying nonclaim

This theorem does **not** say that no representation can be sufficient for every contract. The identity representation is universally sufficient at fixed `X`. It says the domain alone does not select one representation that is minimal for every possible observational objective.

This clarification strengthens the logical precision of the terminal negative result without changing it.

---

## 2. Correction to FAR-CORE-010

### 2.1 Exact common theory

Fix:

- a logical signature `L`;
- an indexed target class `I`;
- interpretation profiles `J=(J_i)_{i∈I}` producing interpreted `L`-models `M_i`.

Define the exact common theory

\[
\mathcal T_{L,J,I}=\bigcap_{i\in I}\operatorname{Th}_L(M_i).
\]

The exact common theory is indexed directly by **`L`, `J`, and `I`**. It is not directly indexed by the interface frame `Γ`.

### 2.2 Frame-relative substantive residue

When an interface frame `Γ` is used to remove constitutive typing or stipulated definitions, define the frame-subtracted residue

\[
\mathcal R_{L,J,I,\Gamma}
=
\mathcal T_{L,J,I}\setminus\operatorname{Cn}_L(\Gamma).
\]

The residue is indexed by **`L`, `J`, `I`, and `Γ`**.

### 2.3 Corrected dependence statement

Holding `L`, `J`, `I`, and therefore the interpreted models `M_i` fixed:

- changing `L`, `J`, or `I` can change `\mathcal T_{L,J,I}`;
- changing `Γ` alone cannot change `\mathcal T_{L,J,I}` because `Γ` does not occur in its definition;
- changing `Γ` can change `\mathcal R_{L,J,I,Γ}`;
- if a changed frame is also used to change an interpretation profile or target model, any resulting change in `\mathcal T` is mediated through the resulting change in `J`/`M`, not through `Γ` as an independent index.

### 2.4 Proof

`\mathcal T_{L,J,I}` is exactly the intersection of the `L`-theories of the models selected by `J` over `I`. First-order truth is invariant under `L`-isomorphism. Therefore the intersection depends on the signature, selected interpreted models/profiles, and target index set. No frame parameter appears in the intersection once those objects are fixed.

By contrast, `\mathcal R_{L,J,I,Γ}` explicitly subtracts `\operatorname{Cn}_L(Γ)`, so changing `Γ` can change the residue. ∎

### 2.5 Permanent countermodel to the v1.0 overstatement

Choose any non-logically-valid sentence `φ` that belongs to `\mathcal T_{L,J,I}`. Hold `L`, `J`, `I`, and all `M_i` fixed. Let

\[
\Gamma_0=\varnothing,
\qquad
\Gamma_1=\{\varphi\}.
\]

Then the exact common theory is identical under both frames:

\[
\mathcal T_{L,J,I}^{(\Gamma_0)}
=
\mathcal T_{L,J,I}^{(\Gamma_1)}
=
\mathcal T_{L,J,I}.
\]

But `φ` remains in the residue under `Γ0` and is removed under `Γ1`:

\[
\varphi\in
\mathcal T_{L,J,I}\setminus\operatorname{Cn}_L(\Gamma_0),
\qquad
\varphi\notin
\mathcal T_{L,J,I}\setminus\operatorname{Cn}_L(\Gamma_1).
\]

This refutes the v1.0 sentence that changing `Γ` *by itself* can change the exact common theory while preserving the intended result that the substantive residue is frame-relative.

### 2.6 Corrected claim

> **Exact common theory is relative to the comparison language, interpretation profiles/models, and target class; the frame-subtracted substantive residue is additionally relative to the interface frame.**

---

## 3. Prior-art correction: Blackwell comparison

The v1.0 sentence that Blackwell comparison implies there is “no loss-independent ranking of information structures” was too broad.

Under the classical comparison-of-experiments setup, Blackwell's order supplies a decision-problem-uniform **partial order**: under the standard finite formulation, one experiment is at least as informative as another for every decision problem exactly when the latter can be obtained by garbling the former. The comparison is therefore not tied to one selected loss function.

The correct Project FAR boundary is:

1. Blackwell comparison is strong prior art for contract- or decision-class-relative comparison of representations/information structures.
2. The order presupposes a fixed experiment/state setup and an admitted comparison class; restrictions or extensions of the decision/problem model can induce other informativeness orders.
3. Project FAR does not claim novelty for the abstract pattern “informativeness/adequacy characterized relative to a declared observational or decision interface.”
4. Project FAR's contribution claim, if any is made downstream, must be limited to its explicit synthesis, audit discipline, cross-domain contract schema, collision test, and governance/application machinery—not the underlying Blackwell, sufficiency, quotient, automata, abstraction, or process-equivalence mathematics.

Primary prior-art anchor:

- David Blackwell, “Equivalent Comparisons of Experiments,” *The Annals of Mathematical Statistics* 24(2), 1953, 265–272. DOI: `10.1214/aoms/1177729032`.

Corroborating modern statements used in this correction audit include DOI `10.3390/e19100527` and the standard-Borel comparison discussion at `10.48550/arxiv.2005.06673`.

---

## 4. Claim ledger after correction

| Claim | v1.1 status | Change from v1.0 |
|---|---|---|
| `FAR-CORE-001` | PROVED | none |
| `FAR-CORE-002` | PROVED | none |
| `FAR-CORE-003` | PROVED | none |
| `FAR-CORE-004` | PROVED, clarified | universal sufficiency distinguished from simultaneous minimality |
| `FAR-CORE-005` | PROVED | none |
| `FAR-CORE-006` | PROVED | none |
| `FAR-CORE-007` | PROVED | none |
| `FAR-CORE-008` | PROVED | none |
| `FAR-CORE-009` | PROVED | none |
| `FAR-CORE-010` | PROVED, corrected | `Γ` removed as direct index of exact theory; retained for residue |
| `FAR-CORE-011` | PROVED | none |
| `FAR-CORE-012` | PROVED | none |
| `FAR-CORE-013` | PROVED | none |
| `FAR-CORE-014` | SUPPORTED/DERIVED | explicitly unchanged |

No claim is upgraded to independent assurance.

---

## 5. Terminal kernel after correction

The surviving terminal kernel is unchanged:

1. For a fixed exact contract, exact sufficiency is factorization of declared behavior through the representation.
2. Every fixed exact contract induces a canonical least-informative observational quotient, unique up to isomorphism.
3. Dynamic/compositional adequacy requires the declared test/context family to contain the relevant continuations.
4. A nontrivial domain admits incompatible contract-relative minima; there is no single contract-free representation that is simultaneously least-informative sufficient for all observation contracts.
5. Representation-independent content depends on the admitted re-representation class.
6. Encoding capacity does not prove native common structure.
7. Primitive and finite operator counts are noninvariant under admitted faithful re-presentation.
8. Finite panels do not prove open-domain universality.
9. Exact common theory is indexed by `L,J,I`; frame-subtracted substantive residue is additionally indexed by `Γ`.
10. Consequence-affecting omitted parameters refute sufficiency.
11. Determinate absence and epistemic Unknown must remain distinct whenever a contract distinguishes them.
12. Canonical FARA Ω is a derived materialized view.
13. SSS remains a bounded supported factorization instance.

The terminal verdict therefore survives W1 correction.

---

## 6. Assurance and next action

The W1 audit that exposed these defects had prior exposure and is not counted as independent validation. `PCA-W1-INDEPENDENT-REVIEW` therefore remains open and is still the next assurance workstream, now against `PROJECT-FAR-CORE-THEORY-1.1`.

Any isolated reviewer must receive the corrected successor rather than the superseded v1.0 claim wording, while the v1.0 artifact and W1 defect record remain available as provenance. A new contradiction reopens only the minimum affected claims.