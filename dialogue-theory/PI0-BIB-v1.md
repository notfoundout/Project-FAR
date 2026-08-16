# PI0-BIB-v1 — prospective, outcome-independent $\Pi_0$ bibliography

**Status: SEALED PROPOSAL, NOT YET OPERATIVE.** This is a separately versioned successor
object. The frozen $\Pi_0$ of $\mathfrak{E}_{0a}$ is **not modified**; its own verdict is
preserved separately in §4.

**Sealing rule.** This file was written and hashed **before any $W^\ast$ candidate existed** —
indeed before $U_0$ was constituted — and therefore could not have been selected against a
comparison outcome. Its hash is recorded in `STATE.json` under `pi0_bib_v1_sha256`. Any later
edit produces a different hash and a different version.

---

## 1. Correction to the frozen count — DF-08

Revisions 1–2 of these artifacts stated that frozen $\Pi_0$ is "a composite of **thirteen**
bodies". **That was an error of mine.** The frozen text (`TR-11:3287`, restating `TR-11:2210`)
is a semicolon-delimited list of **twelve** labels:

1. institutions and institution-independent model theory
2. MMT / theory morphisms
3. FCA / Chu / Barwise–Seligman
4. categorical logic and doctrines
5. Markov and CD categories
6. effectus theory
7. restriction categories
8. abstract interpretation and Galois connections
9. Pearl's causal hierarchy
10. substructural and monoidal resource theory
11. universal algebra and coalgebra
12. rewriting logic

**DF-08 — $\Pi_0$ individuation is underdetermined by the frozen text.** Six of the twelve
labels are internally composite (1, 3, 5, 8, 10, 11). The frozen text fixes neither how many
bodies each label denotes nor which document certifies each. Since $\Pi_c$ renderings must be
certificate-carrying (`TR-11:2212`), **frozen $\Pi_0$ is not executable as an exact corpus**.
This is a defect of the frozen object, recorded and preserved, not repaired.

**Individuation adopted here: one body per frozen label — twelve bodies.** This is the least
invasive reading: it changes no frozen text and introduces no boundary the frozen text does not
draw. Where a label is composite, the assignment must **cover** every named component.

**The continuation packet's proposed split** of "FCA/Chu/Barwise–Seligman" into two bodies to
reach thirteen is **not adopted**. Its motivation was to reconcile a count of thirteen — a count
that originated in my own error, not in the frozen text. With the count corrected to twelve, no
split is required, and splitting would draw a boundary inside a frozen label on no frozen
authority. The packet's *documents* are adopted; its *re-individuation* is not. Both of the
packet's documents for label 3 are retained, jointly covering that one composite body.

## 2. Selection rule, fixed before assignment

One canonical or field-defining primary-author work per frozen label; full text obtainable;
published on or before the evidence cutoff **2026-08-15**; selected without access to any
$W^\ast$ candidate, any $U_0$ item, or any comparison outcome. Where a label is composite, the
assignment covers each named component, using more than one document only where no single
primary-author work covers the label.

## 3. The bibliography

| # | Frozen $\Pi_0$ label | Assigned primary document(s) | Supplied? |
|---:|---|---|---|
| 1 | institutions and institution-independent model theory | Goguen & Burstall, *Institutions: Abstract Model Theory for Specification and Programming* | ✗ |
| 2 | MMT / theory morphisms | Rabe & Kohlhase, *A Scalable Module System* | ✗ |
| 3 | FCA / Chu / Barwise–Seligman | Wille, *Why Can Concept Lattices Support Knowledge Discovery in Databases?* **and** Gupta, *Chu Spaces: A Model of Concurrency* | ✗ |
| 4 | categorical logic and doctrines | Lawvere, *Adjointness in Foundations* (TAC reprint) | ✗ |
| 5 | Markov and CD categories | Fritz, *A Synthetic Approach to Markov Kernels, Conditional Independence and Theorems on Sufficient Statistics* | ✗ |
| 6 | effectus theory | Cho, Jacobs, Westerbaan & Westerbaan, *An Introduction to Effectus Theory* | ✗ |
| 7 | restriction categories | Cockett & Lack, *Restriction Categories I: Categories of Partial Maps* | ✗ |
| 8 | abstract interpretation and Galois connections | **Cousot & Cousot, *Abstract Interpretation Frameworks*, JLC 2(4):511–547, 1992** | ✅ `SS-CC92`, hashed, already inspected for S7 |
| 9 | Pearl's causal hierarchy | **Pearl, *The Seven Tools of Causal Inference, with Reflections on Machine Learning*, UCLA TR R-481, Feb 2019, DOI 10.1145/3241036** | ✅ `SS-P19`, hashed |
| 10 | substructural and monoidal resource theory | Coecke, Fritz & Spekkens, *A Mathematical Theory of Resources* | ✗ |
| 11 | universal algebra and coalgebra | Jacobs & Rutten, *A Tutorial on (Co)Algebras and (Co)Induction* | ✗ |
| 12 | rewriting logic | Meseguer, *Twenty Years of Rewriting Logic* | ✗ |

**Supplied: 2 of 12 labels (13 of the listed documents, 2 held). Missing: 10 labels, 11
documents.**

`SS-P19` is deliberately distinct from S5's SCM source: it states the three-level hierarchy
(Association / Intervention / Counterfactual) directly, which is what label 9 names. It is
**not** substituted for S5, and S5's source is **not** substituted for it.

## 4. Disposition of frozen $\Pi_0$, preserved separately

$$\boxed{\text{Frozen }\Pi_0\text{: \textbf{UNEXECUTABLE} — individuation and per-label certification not fixed by the frozen text (DF-08).}}$$

$$\boxed{\texttt{PI0-BIB-v1}\text{: \textbf{SEALED, NOT OPERATIVE} — 10 of 12 labels unsupplied.}}$$

The frozen verdict is not overwritten by the successor. Under both, the novelty verdict for
everything is **UNRESOLVED, never positive** (`TR-11:2214`).

## 5. What may and may not be inferred from this file

- **May not:** that any $\Pi_0$ body subsumes, or fails to subsume, any content. No translation
  certificate has been produced. Bibliographic presence is not a subsumption verdict, and
  bibliographic absence is not novelty.
- **May not:** that $\Pi_0$ is now executable. Ten labels have no supplied document.
- **May:** that the exact attachment set required to make $\Pi_0$ operative is now fixed,
  outcome-independently, and sealed against later tuning.
