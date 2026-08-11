# FARA unresolved-candidate obligation-scope audit v1.0

Status: **Research result — H5 returned. The asymmetry is not established as architectural; a terminological defect is established. Ambiguity preserved. No canonical surface modified.**
Investigation target: `OP-17` / `UQ-T21`
Kind: deductive clause audit. No experiment, no software, no canonical edit.

Preserved from `OP-16` and not strengthened: unresolved appears structurally distinct from an ordinary calculus-defined admissibility value, but only **weakly**; its semantic content remains **underdetermined**. Nothing below strengthens that typing.

## Stage 1 — Clause reconstruction

### 1.1 Exact grammatical scope of each obligation

| Clause | Subject | Obligation | Reaches unresolved? |
|---|---|---|---|
| **Explicitness** `admissibility-structure.md:111` | "Every **candidate** admitted for consideration" | possess "either an explicit admissibility classification **or** an explicitly represented unresolved status" | **Yes — the only clause that does.** Requires a marker; nothing more. |
| **Traceability** `:117-122` | "Every **admissibility classification**" | traceable to the candidate classified, the investigation, the calculus, and "the reasoning process or reasoning trace **that produced the classification**" | **Interpretation-dependent.** |
| **Auditability** `:144-146` | "An **Admissibility Structure**" | "permit reconstruction of **why each candidate received its admissibility classification**"; requires explicit links between classifications, traces, criteria, supporting representations | **Interpretation-dependent.** Package-level subject, per-candidate object, and the object **presupposes** a classification was received. |
| **Principle 6 — Auditability** `design-principles.md:80-89` | "Reasoning **artifacts**" | should make explicit, among others, "**admissibility classifications produced**" | **No.** An unresolved candidate produced none. |

The two Ω clauses do not share a subject: Traceability is per-classification, Auditability is package-level. That asymmetry exists **between the clauses themselves**, independently of unresolved.

### 1.2 The `status` non-univocity — the decisive finding — **SUPERSEDED; WITHDRAWN RESULT PRESERVED FOR PROVENANCE**

> **Superseded 2026-08-10 by the `OP-18` term audit** (`docs/research/fara-status-term-audit-v1.0.md`).
>
> **Original question.** Does the lexical bridge from `admissibility-structure.md:23` carry enough force to bring the unresolved result inside the scope of the traceability and auditability obligations?
>
> **Original argument.** The bridge fails because `status` is used in at least five distinct senses across canonical FARA — admissibility, candidate, unresolved, primitive, foundation — with no disambiguation.
>
> **Why it failed.** The five-sense premise is **refuted**. Substitution testing shows `primitive status` and `foundation status` both collapse under "epistemic status", and every technical occurrence is recoverable under one abstract definition. The word is univocal; the ambiguity lies in the compound construction `N status`, and it bites at exactly one occurrence, `admissibility-structure.md:111`.
>
> **Current adjudication.** The bridge still fails, but for a narrower reason: `:111` is the sole technical occurrence with no governing definition and no stated categorization, and the construction is neutral between the readings. `H3` is preserved as unresolved and the residue is an architectural decision point, `ADR-002`. The `H5` verdict of this investigation, and its independent results on path-linking and unknown-cause auditability, do **not** depend on the withdrawn premise and stand unchanged.

The original subsection is retained verbatim below.

`admissibility-structure.md:23` and `theory/definitions/definitions.md:606` define the key term:

> "An admissibility classification is the explicit assignment of **admissibility status** to a candidate."

`:111` calls unresolved a "**status**". This suggests a bridge: *classification = assignment of status; unresolved is a status; therefore assigning unresolved is a classification* — which would establish **I2** directly.

**The bridge fails.** `status` is not univocal in canonical FARA. Enumerated uses:

| Use | Location | Sense |
|---|---|---|
| `admissibility status` | `admissibility-structure.md:23` | what a classification assigns |
| `candidate status` | `admissibility-structure.md:82` | admission for consideration — "Candidate status does not imply admissibility" |
| `unresolved status` | `admissibility-structure.md:111` | the `:111` disjunct |
| `primitive status` | `architecture.md:82`, `design-principles.md:66` | epistemic standing of a primitive candidate |
| `foundation status` | `architecture.md:239` | epistemic standing of a foundation |

No canonical text asserts that "unresolved status" is an **admissibility** status. With `status` used in five senses and no disambiguation, the lexical bridge carries no force — but it is also not refuted. **Both I1 and I2 survive.**

### 1.3 Two different auditability formulations inside FARA

`transition-signatures.md:85` audits a **derivation**: "Another investigator should be capable of reconstructing the represented transformation **execution** from the transition signature and its referenced reasoning state representations."

`admissibility-structure.md:144` audits a **reason for an assignment**, and presupposes the assignment occurred.

The transition-signature form takes an event that happened as its object; the Ω form takes a *why* whose subject may not exist. **H4's proposed object — the derivation/path rather than a nonexistent classification — is therefore not novel: it is the form FARA already uses elsewhere.**

## Stage 2 — Competing interpretations

| | Reading | Status |
|---|---|---|
| **I1** | "admissibility classification" means only a substantive member of `S_K` | **Coherent.** Obligations are then **vacuous** for unresolved candidates — a coverage gap, not a violation. |
| **I2** | "admissibility classification" includes the explicit unresolved result | **Coherent.** Supported by the `status` bridge, weakened by non-univocity (§1.2). |
| **I3** | obligations attach to the structure as a whole and so indirectly cover unresolved | **Partially correct and independently true**: the Auditability subject *is* the Admissibility Structure. But its object is still per-candidate and still presupposes receipt, so I3 does not by itself settle coverage. |
| **I4** | canonical FARA intentionally imposes weaker obligations on unresolved | **Not established.** No canonical text states or defends any such intent, and `:204` lists "completeness of admissibility classification" as **open research**, indicating an unfinished area rather than a designed one. |

## Stage 3 — Minimal countermodels

Three objects are kept separate throughout: (i) traceability of the path that produced unresolved, (ii) auditability of that path, (iii) auditability of a substantive classification. A missing classification is **not** treated as an auditable object; canonical text does not support that.

| Case | Path traceable? | Path auditable? | Substantive-classification auditability |
|---|---|---|---|
| **A** insufficient evidence | Yes — link to the evidence state | Yes | Vacuous under I1; presupposition failure under I2 unless the unresolved result counts |
| **B** conflicting criteria | Yes — link to the conflicting criteria | Yes | same |
| **C** nontermination | **Partially.** No process *produced* a result; only "did not terminate" is recordable | Weakly | same |
| **D** missing required input | Yes — link to the missing input | Yes | same |
| **E** calculus-defined inability to decide | If the calculus **declares** an inability *value*, that value lies in `S_K` and is a substantive classification, not unresolved (`OP-16` Stage 3 case F). If the calculus merely fails to yield, this is case G-adjacent | — | — |
| **F** evaluator failure | **Layer-uncertain.** `Ω` is calculus-relative (`:128-130`); evaluator state is not calculus content. `OP-16` returned `H4` on exactly this and it is not resolved here | — | — |
| **G** unknown cause | Only the fact of non-classification is recordable | **The decisive countermodel — see below** | — |

**Case G breaks strong auditability.** If the auditability obligation extended to unresolved and demanded reconstruction of the actual cause, case G would make it **unsatisfiable**: one cannot reconstruct a cause that is unknown. I2 therefore forks:

- **I2-weak** — only the *absence* must be recorded. This collapses into `:111`'s existing marker requirement plus a note, adding nothing.
- **I2-strong** — actual causes must be reconstructable. Refuted by case G.

Neither fork yields a new obligation worth stating. This is an independent reason why no normative change is justified, additional to the ambiguity.

## Stage 4 — Necessity analysis

| # | Question | Answer | Premises |
|---|---|---|---|
| 1 | Is explicit unresolved marking sufficient for FARA's current canonical goals? | **Yes.** Principle 6 enumerates what artifacts must make explicit; "admissibility classifications produced" is among them, and an unresolved candidate produced none. `:111` supplies the marker. | `design-principles.md:80-89`; `:111` |
| 2 | Is reason provenance required for reproducibility? | **No.** FARA states no reproducibility property for `Ω`. The only FARA reproducibility clause is `transition-signatures.md:93-99`, which concerns equivalence relations for transformations, not `Ω`. | absence over the surfaces searched; `transition-signatures.md:93` |
| 3 | Is reason provenance required for auditability? | **Interpretation-dependent, and self-defeating under I2-strong.** Vacuous under I1; refuted by case G under I2-strong. | `:144`; case G |
| 4 | Does traceability logically imply recording the **cause** of unresolved? | **No.** Traceability's four targets are the candidate, the investigation, the calculus, and the producing process — none is a cause. Even read broadly it requires **path-linking**, not cause-recording. | `:117-122` |
| 5 | Does auditability logically imply reconstructing why classification did not occur? | **Only under I2**, and then only in the weak form that survives case G. | `:144`; case G |
| 6 | Can an unresolved result be auditable without being a substantive classification? | **Yes.** Audit the derivation/path rather than a nonexistent object. This is the form `transition-signatures.md:85` already uses. | `transition-signatures.md:85` |

Finding 4 is the clean discriminator: **traceability and auditability come apart for unresolved candidates.** Traceability is satisfiable (path-linking) in cases A, B, D and partially C; auditability of causes is not generally satisfiable (case G). Downstream layers were used only as comparison and supplied no premises.

## Stage 5 — Architectural options

| | Verdict |
|---|---|
| **H1** current asymmetry intentional and justified | **Rejected as unestablished.** No canonical text states or defends intent; `:204` marks the area as open research. |
| **H2** broad reading already covers it; semantic clarification only | **Available, not established.** Depends on the `status` bridge that §1.2 shows carries no force. |
| **H3** traceability extends, substantive-classification auditability does not | **Best-motivated content**, from finding 4 and case G — but it is a *proposal*, not something canonical text establishes. |
| **H4** both extend, object being the derivation/path | **Coherent**, with in-FARA precedent (§1.3). The auditability half still meets case G. |
| **H5** evidence insufficient to establish any normative change | **Accepted.** |

**H5 is returned** because I1 and I2 are both coherent readings of the same text, the standing instruction is to preserve ambiguity rather than select the cleaner design, and Stage 3 shows that neither fork of I2 yields an obligation worth adding.

## Stage 6 — Interaction with `OP-16`

Under `M1` (unresolved ∈ `S_K`) the obligations attach automatically and no asymmetry arises. Under `M2` (meta-status outside `S_K`) they do not.

**This provides no evidence about intended typing.** Preferring `M1` because it removes an awkward asymmetry would be exactly the prohibited inference from downstream convenience to upstream ontology.

One **non-convenience** consideration exists and is recorded at its true weight. Traceability requires linking to "the reasoning process or reasoning trace **that produced the classification**." In cases C and D nothing *produced* a result — the process failed to yield. Under `M1`, traceability would require pointing to a producing process that may not exist. This weakly favours `M2`. It is a single wording-level consideration against a clause whose own scope is disputed, so it is **not** treated as strengthening `M2`.

**`OP-16`'s result is left unchanged**: typing weakly established, semantics underdetermined.

## Stage 7 — Minimal revision test

**One canonical defect is established**, and it is terminological rather than architectural:

> `status` is used in at least five distinct senses across canonical FARA — admissibility status, candidate status, unresolved status, primitive status, foundation status — with no disambiguation. This non-univocity is precisely what makes the scope of the Traceability and Auditability obligations undecidable.

This defect is demonstrable and is **not** interpretation-relative, unlike the asymmetry itself.

**Repair site identified; repair content not supplied.** The smallest repair is a single scope clarification stating whether "admissibility classification", as used in the Traceability and Auditability properties, includes the explicit unresolved result — preferred over duplicated clauses or a new obligation. **Which way it should be clarified is exactly the undetermined question**, and this investigation supplies no evidence to settle it. Supplying content would select a design, which the standing instruction forbids.

No definition of unresolved's semantic meaning is proposed: `OP-17` supplied no evidence resolving `OP-16`'s `H4` underdetermination.

## Quality Gate disposition

**No canonical change justified.** The asymmetry is not established as architectural; the terminological defect is established but its repair requires a decision no current evidence supports.

## Nonclaims

This investigation does not establish: that the asymmetry is real (it exists only under `I1`); that it is intentional; that any obligation should be extended; the semantic content of unresolved status; that no further canonical usage exists beyond the surfaces searched. `Ω`'s type and semantics, FARA primitives, seven-primitive completeness, `UQ-T2`, `OP-02`, and the terminal UPP theorem are all unaffected. No canonical surface, evaluation record, frozen evidence, or software was modified.
