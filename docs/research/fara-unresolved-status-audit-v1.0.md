# FARA `unresolved status` semantic audit v1.0

Status: **Research result — split outcome. H2 established at the type level; H4 returned for semantic content. No canonical surface modified.**
Investigation target: `OP-16` / `UQ-T20`
Kind: deductive usage and authority audit. No experiment, no software, no canonical edit.

## Stage 1 — Usage reconstruction

### 1.1 The decisive quantitative fact

Canonical FARA uses the term **exactly once**:

> `frameworks/FARA/admissibility-structure.md:111` — "Every candidate admitted for consideration should possess either an explicit admissibility classification or an explicitly represented unresolved status."

It occurs inside a section headed "An Admissibility Structure **should** satisfy the following properties" (`:107`). It is a desideratum, not a definition.

**Shared theory contains zero occurrences** of `unresolved`, `unknown`, `uncertain`, `indeterminate`, `undetermined`, or `unclassified`. The concept is entirely absent upstream of FARA.

### 1.2 Five lexically similar, semantically distinct concepts

| Concept | Subject | Layer | Canonical definition? |
|---|---|---|---|
| **FARA `unresolved status`** | a **candidate** in `Ω` | FARA | **None.** One normative use, undefined. |
| **FAR `Unresolved`** | an **investigation** closure | FAR (downstream) | **Yes** — `frameworks/FAR/workflow.md:136`: "no resolution is currently available under the stated method"; `investigation-validation.md:143`: "No resolution is currently available under the stated methodology." One of six closure statuses. |
| **FARO `uncertainty`** | an operational **output** | FARO (downstream) | Only in the terminology authority, `docs/glossary/canonical-terminology.md:36`: "Explicitly recorded lack of warranted determination; not automatically probability." FARO's own documents never define it. |
| **Charter `Unknown`** | an **artifact** epistemic status | governance | `docs/governance/research-execution-charter.md:197-203`, one of five artifact statuses. |
| **CRP `Unknown`** | a **preservation-dimension** value | methodology | `theory/evaluation/comparative-representation/protocol-v1.0.md:79`: "`Unknown` is epistemically **incomparable** with non-`Unknown` values"; ":99": "`Unknown` does not count as successful removal or survival." |

These are not merged. Subjects differ (candidate / investigation / output / artifact / dimension) and layers differ.

### 1.3 Two structural observations

1. **The only canonical definition of the word lives downstream, for a different subject.** FAR defines `Unresolved` for investigations. Under `docs/governance/framework-boundaries.md`, FAR must not supply FARA definitions, and a downstream need "is not itself a derivation" (`:17`). FAR's definition therefore **cannot** be imported upstream.
2. **Precedent exists for the terminology authority defining a term its owning framework does not define.** FARO `uncertainty` is defined only in `canonical-terminology.md`. This is the pattern that would apply here.

## Stage 2 — Behavioral constraints derivable from canonical FARA alone

Governing text: `:111`; `:84` (available classifications determined **entirely** by the calculus); `:41` (`Ω` is the representation of classifications of candidates); `:43` (records without determining); `:117-122` Traceability; `:142-146` Auditability; `theory/definitions/definitions.md:606` (a classification assigns admissibility status to a candidate).

| # | Question | Answer | Premises | Force |
|---|---|---|---|---|
| P1 | Is unresolved itself an admissibility classification? | **No**, on the non-redundancy reading: if it were, `:111`'s second disjunct would be subsumed by the first and the sentence vacuous. | `:111` | **Reading, not forced.** English "either…or" admits an inclusive sense. FARA's fastidious category separation favours non-redundancy, but this is coherence, not derivation. |
| P2 | Do Traceability and Auditability attach to unresolved? | **No, conditional on P1.** Both are scoped to "admissibility classification". | `:117`, `:142`, P1 | Derivable **given P1**. Consequence: an unresolved candidate carries no traceability or auditability obligation — an asymmetry canonical text neither states nor defends. |
| P3 | Is unresolved available regardless of the calculus? | **Yes, conditional on P1.** If it is not a classification, `:84` does not govern it. | `:84`, P1 | Derivable **given P1**. Under the contrary reading, a calculus may declare `S_K = {admissible, inadmissible}`, leaving `:111` unsatisfiable for candidates it cannot classify. Because `:111` is a "should", this is **tension, not contradiction**. |
| P4 | Does `:111` require a marker or semantic content? | **Marker only.** "Explicitly represented" requires presence in the representation, not a reason. | `:111` | Derivable. Nothing requires a reason. |
| P5 | May two candidates be unresolved for different reasons? | **Not prohibited** on the surfaces searched. | absence of prohibition; P2 | Permission by bounded absence, not a positive derivation. |
| P6 | May unresolved become substantive without the calculus changing? | **Not prohibited.** `:64` contemplates different structures from changed inputs; further reasoning may produce classifications. | `:64`, `:134-138` | Permission by bounded absence. |

**Not derivable at all:** what unresolved *means* — whether the calculus has no answer, the evaluator lacks information, computation has not terminated, evidence is insufficient, or some disjunction. Canonical FARA contains no text bearing on this.

## Stage 3 — Distinction tests

| Case | Would canonical FARA label it unresolved? | Basis |
|---|---|---|
| **A** source-semantic uncertainty | **Undetermined.** Reduces to F or E depending on whether the source carries it as a value. | no canonical text |
| **B** evaluator ignorance | **Not derivable as FARA-unresolved.** `Ω` is calculus-relative (`:128-130`); evaluator epistemic state is not calculus content. Resembles FARO `uncertainty`. | cross-layer vocabulary, **suggestive only** |
| **C** incomplete evidence | **Not derivable.** Resembles FAR `Incomplete` and FARO `incompleteness`. | cross-layer vocabulary, **suggestive only** |
| **D** nontermination / not-yet-computed | **Not derivable.** Resembles FAR `Suspended`. P6 shows FARA does not forbid it either. | cross-layer vocabulary, **suggestive only** |
| **E** calculus genuinely leaves a candidate undecided | **Yes — core case.** No classification is available, so the `:111` fallback applies. | `:111`, `:84`, P1 |
| **F** source semantics contains an explicit "undecided" **value** | **No — must not be unresolved.** `:84` lets the calculus declare that value inside `S_K`, where it is a substantive classification. Labelling it unresolved would discard a declared source value. | `:84`, `:111`, P1 — **derivable given P1** |
| **G** no applicable classification | **Yes.** Variant of E. | `:111` |

The F/E separation is the one genuinely discriminating result: **an explicit "undecided" value is a classification, not unresolved.** B, C, and D are only *suggested* to belong elsewhere by other layers' vocabularies; that is not a FARA derivation and is not treated as one.

## Stage 4 — Type-level models

| Model | Verdict | Reason |
|---|---|---|
| **M1** `Ω_K : C → S_K`, unresolved ∈ `S_K` | **Disfavoured, not refuted** | Makes `:111` redundant (P1). Creates the `:84`/`:111` tension in P3. Inherits Traceability and Auditability, so reasons would have to be reconstructable — an obligation canonical text never states. Survives only because `:111` is a "should". |
| **M2** `Ω_K : C → S_K ∪ {⊥}`, `⊥ ∉ S_K` | **Best fit** | Satisfies `:111` non-redundantly; always available regardless of calculus; marker-only; imposes no traceability obligation; does not constrain `S_K`. Shape matches the CRP `Unknown` precedent, which is epistemically incomparable with the ordered values — though that precedent is methodology-layer and is **not** imported as authority. |
| **M3** `Ω_K : C →` the tagged sum of `Classified(S_K)` and `Unresolved` | **Collapses into M2** | Informationally isomorphic tagged sum. The explicit tagging is additional structure no canonical clause forces. Rejected as unforced ceremony, not as wrong. |
| **M4** `Unresolved(Reason)` | **Rejected as unforced** | P4 shows `:111` requires only a marker. FAR's own practice is evidence *against* embedding: `investigation-validation.md:171-173` records the **cause separately** — "The cause must be recorded" — rather than inside the status. |
| **M5** unresolved lives outside `Ω` at the package/trace layer | **Rejected** | `:111` sits under "An Admissibility Structure should satisfy the following properties" and requires the **candidate** to possess the explicitly represented status. A status wholly outside `Ω` could not be a property of `Ω`. Contradicts `:41` and `:111`. |

## Stage 5 — Ownership

| Candidate owner | Verdict |
|---|---|
| shared theory | **Rejected.** Zero occurrences upstream. Adding it because FARA needs it is a downstream-motivated upstream change, which `framework-boundaries.md:17` says is not a derivation. |
| **FARA** | **Correct owner.** The term is a property of `Ω`, a FARA-owned component, and appears only in FARA. |
| FAR | **Rejected.** FAR's `Unresolved` is a different subject (investigation closure) and FAR is downstream. |
| FARO | **Rejected.** FARO `uncertainty` is a different subject and downstream; importing it upstream would require a derivation that does not exist. |
| governance / Charter | **Rejected.** A governance epistemic status must not silently become a FARA semantic status. |
| nowhere yet | **Partially correct — see Stage 6.** |

Recording surface, if a definition is authorized: `docs/glossary/canonical-terminology.md`, which already performs exactly this role for FARO `uncertainty`.

## Stage 6 — Surviving hypothesis and minimal definition

**The outcome splits, and the split is the result.**

- **Type level — H2 established** (weakly): unresolved is a framework-level meta-status indicating no substantive `S_K` classification is currently available. M2 is the only model that satisfies `:111` without redundancy or tension with `:84`.
- **Semantic level — H4 returned**: canonical evidence underdetermines *which* of cases A–G unresolved covers. One "should" clause, no definition, and no discriminating text cannot fix a meaning. H3 is rejected outright: no canonical clause requires unresolved to carry reason structure.

H2 is not adopted because it types cleanly. It is adopted because M1 generates a `:84`/`:111` tension and renders `:111` redundant, M4 and M5 contradict or exceed canonical text, and M3 reduces to M2. The residual weakness of P1 — a reading rather than a forced inference — is carried forward explicitly and is why H2 is recorded as *weakly* established.

### Minimal candidate definition — proposed, not applied

> **unresolved status** — An explicitly represented record that no admissibility classification from the applicable reasoning calculus is currently assigned to a candidate. It is not itself an admissibility classification and is not a member of the calculus-determined classification set. Owner: FARA. Class: framework-level meta-status.

**Falsification attempts, all survived:**

| Attack | Outcome |
|---|---|
| Conflates with FARO `uncertainty`? | No. It concerns classification availability, not warranted determination. |
| Conflates with Charter `Unknown`? | No. Different subject (candidate vs artifact) and layer. |
| Fixes `S_K`'s structure? | No. It places the status outside `S_K` and says nothing about `S_K`'s contents or order. |
| Adds a normative obligation? | No. It is descriptive; `:111` already carries the only obligation. |
| Converts methodological faithfulness into a canonical requirement? | No. It says nothing about preservation, reflection, or fidelity. |
| Forbids a calculus's own "undecided" value? | No — and it correctly separates that case: such a value lies in `S_K` and is a classification (Stage 3 case F). |
| Settles cases A–G? | **No, deliberately.** "Currently assigned" is neutral among no-answer, not-yet-computed, and genuinely-undecided. This residue is `H4` and must not be invented away. |

## Impact on `Ω` and FARA architecture

`Ω`'s type is unchanged: the definition describes what `:111` already requires, and under M2 the codomain `S_K ∪ {⊥}` is how the existing clause was already operating. `Ω`'s semantics are unchanged. FARA primitives are unchanged. No evidence is produced for or against seven-primitive completeness; `UQ-T2` and `OP-02` are unaffected. The terminal UPP theorem and its independently frozen `E*` premise are untouched.

One consequence is recorded rather than resolved: under P1/P2, unresolved candidates carry **no** traceability or auditability obligation, while classified candidates do. Canonical text neither states nor defends this asymmetry.

## Exact canonical surface that would change, if authorized

One row appended to the core inventory table of `docs/glossary/canonical-terminology.md`, using the definition above, with canonical detail pointing at `frameworks/FARA/admissibility-structure.md`. No change to `admissibility-structure.md` itself, to shared definitions, or to any framework document.

**Not applied.** The Charter lifecycle requires Question → Execution → Observation → Discovery → **Replication** → **Acceptance** → **Promotion** before canonical text changes. Replication and Acceptance have not occurred. The type-level result is additionally recorded as *weakly* established, which is not a basis for canonical promotion.

## Nonclaims

This investigation does not establish: that no further canonical usage exists anywhere in the repository, only that none was located on the surfaces searched; that the proposed definition is unique or complete; the semantic content of unresolved status; that FARA's traceability asymmetry is correct; any primitive, minimality, necessity, or completeness result. No canonical surface, evaluation record, frozen evidence, or software was modified.
