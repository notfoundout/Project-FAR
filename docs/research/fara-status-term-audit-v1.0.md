# FARA `status` term audit v1.0

Status: **Research result — `D4` succeeds for the word, `D2` survives for one occurrence. `H3` preserved for `unresolved status`. `LIM-030` corrected. No canonical surface modified.**
Investigation target: `OP-18` / `UQ-T22`
Kind: deductive lexical audit. No experiment, no software, no canonical edit.

**Headline answer.** The ambiguity surrounding `unresolved status` **cannot** be eliminated without a new design choice. The remainder of the non-univocity **can** be, by recording a definition recoverable from usage.

## Stage 1 — Exhaustive occurrence inventory

Canonical FARA is the twelve documents listed in `docs/CANONICAL_MAP.md`; `frameworks/FARA/research/` is not canonical. Every occurrence of `status`/`statuses` in those twelve is inventoried below. `classification`/`classifications`/`classified` occurrences were also enumerated in full; all are governed by `admissibility-structure.md:23` and none introduces a further sense of `status`.

### 1.1 Non-technical: document metadata and repository convention

| Occurrence | Form |
|---|---|
| `README.md:17`, `admissibility-structure.md:198`, `architecture.md:231`, `ontology.md:170`, `ontology.md:182`, `primitives.md:167`, `reasoning-states.md:174`, `semantics.md:87`, `transition-signatures.md:190` | section headings ("Current Status", "Research Status", "Version Status") |
| `README.md:106` | link text to `docs/project-status.md` |
| `formal-kernel.md:3` | "Status: **Accepted**" — the Charter artifact-status vocabulary used as document metadata. Governance concept in a FARA document, but as metadata, not as FARA semantics. **No layer violation.** |

These carry no FARA-technical content and are excluded from the sense partition.

### 1.2 Technical occurrences

| # | Exact phrase | Grammatical subject | Entity whose status is described | Governing definition | Sense |
|---|---|---|---|---|---|
| 1 | "admissibility status" | "An admissibility classification" | a candidate | `admissibility-structure.md:23`; `theory/definitions/definitions.md:606` | **A** |
| 2 | "Candidate status does not imply admissibility" | "Candidate status" | an object admitted for consideration | `admissibility-structure.md:80`; `definitions.md:576-578` | **B** |
| 3 | "an explicitly represented unresolved status" | "Every candidate" | a candidate | **none** | **B, categorization unstated** |
| 4 | "Candidate primitive status is provisional" | `architecture.md:82` | a candidate primitive | `primitives.md` | **B** |
| 5 | "Candidate primitive status is provisional" | `dependency-graph.md:97` | a candidate primitive | `primitives.md` | **B** |
| 6 | "Candidate primitive status remains provisional" | `design-principles.md:66` | a candidate primitive | `primitives.md` | **B** |
| 7 | "Candidate primitive status does not imply permanent irreducibility" | `ontology.md:46` | a candidate primitive | `primitives.md` | **B** |
| 8 | "Candidate primitive status is provisional" | `primitives.md:9` | a candidate primitive | this document | **B** |
| 9 | "Candidate primitive status is not evidence of irreducibility" | `primitives.md:27` | a candidate primitive | this document | **B** |
| 10 | "unique foundation status" | `architecture.md:239` | a formal foundation | none | **B** |
| 11 | "a concept moves between primitive and derived status" | `document-map.md:124` | a concept | `ontology.md` | **B** |
| 12 | "'Stable' is a maintenance status" | `README.md:115` | FARA as a repository artifact | none | **A** |

**Adjacent finding, recorded not pursued.** `candidate` is itself polysemous: a noun at occurrence 2 (an object admitted for consideration) and an adjective meaning *provisional* at occurrences 4–9. `transition-signatures.md:162` "candidate classifications" uses the noun sense (classifications *of candidates*). This is a separate polysemy in `candidate`, not in `status`.

## Stage 2 — Minimal sense partition

The five candidate senses in the brief do not survive. The evidence supports a **two-way grammatical partition** of the compound `N status`, not a five-way semantic partition of `status`.

- **Sense A — categorization-naming.** `N` names the categorization; the value is left unstated. Occurrences 1, 12. Discriminator: `N` is a dimension along which entities are assessed (*admissibility*, *maintenance*), and a separate value fills it — `:23` has the classification *assign* the status; `README.md:115` supplies "Stable" as the value.
- **Sense B — value-naming.** `N` names the value; the categorization is contextually supplied or unstated. Occurrences 2–11. Discriminator: `N` is itself a standing an entity can hold (*candidate*, *candidate primitive*, *unique foundation*, *primitive*, *derived*, *unresolved*), and the sentence predicates something of holding it.

**`S4` and `S5` collapse.** Occurrences 4–9 (primitive) and 10 (foundation) are both Sense B and both denote epistemic standing within the primitive-basis/foundation programme. Substituting "epistemic status" preserves meaning in both (Stage 3). They are not distinct senses.

**`S2` collapses into the same class.** "Candidate status" (occurrence 2) is Sense B, parallel in construction to "candidate primitive status" despite using a different sense of `candidate`.

**`S1` and `S3` sit in different grammatical classes** — A and B respectively — but this is a difference in how the compound is built, **not** evidence about whether unresolved belongs to the admissibility categorization. See Stage 4.

## Stage 3 — Substitutability tests

| Substitution | Result | Reading |
|---|---|---|
| occurrence 2 → "admissibility status": *"Admissibility status does not imply admissibility"* | **Fails** — becomes near-tautologous and loses the intended contrast between being admitted for consideration and being admissible | Confirms A ≠ B; confirms `candidate status` is not `admissibility status` |
| occurrence 3 → "admissibility status": *"either an explicit admissibility classification or an explicitly represented admissibility status"* | **Fails** — `:23` makes a classification *the assignment of* an admissibility status, so the disjunction becomes redundant | **Not independent evidence.** This is exactly `OP-16`'s non-redundancy argument restated. It corroborates nothing new and must not be counted twice. |
| occurrences 4–9 → "epistemic status" | **Succeeds** | Meaning preserved |
| occurrence 10 → "epistemic status" | **Succeeds** | Meaning preserved; confirms collapse with 4–9 |
| occurrence 1 → "candidate status" | **Fails** — `:23` would then define a classification as assigning candidacy | Confirms A ≠ B |

Successful substitution is not treated as proof of identity; occurrences 4–10 additionally share a governing treatment in `primitives.md`/`ontology.md`, which supports the collapse independently of the substitution.

## Stage 4 — The `unresolved status` discriminator

Only evidence capable of discriminating the hypotheses lexically was admitted. Downstream consequences, typing preferences, awkwardness, and `OP-17` results were excluded.

| Evidence sought | Found? |
|---|---|
| A canonical occurrence listing `unresolved` alongside admissible/inadmissible as calculus values | **No.** `:111` is the only occurrence of the term in canonical FARA. |
| A canonical text naming a non-admissibility categorization for unresolved | **No.** |
| A governing definition for occurrence 3 | **No.** It is the only technical occurrence in the inventory with no governing definition. |
| A grammatical discriminator | **No.** Sense B leaves the categorization unstated by construction. If unresolved's categorization is admissibility, `H1` holds and "unresolved status" is simply the value-naming form of "admissibility status". If it is some other categorization, `H2` holds. The construction is neutral between these. |
| The mixed pairing in `:111` ("admissibility **classification**" vs "unresolved **status**") | **Weak and non-probative.** A tight parallel would pair classification with classification or status with status. The mixed pairing may indicate a kind difference or may be stylistic. `:23` already relates classification and status as act and value, so the mixing is not anomalous. |

**`H3` is preserved.** Canonical evidence is exhausted and does not determine whether `H1` or `H2` is intended. No authorial reconstruction is offered.

## Stage 5 — Defect characterization, and correction of `LIM-030`

**`D4` was attempted seriously and largely succeeds.** Strongest common definition recoverable from usage:

> **status** — the standing of an entity under an explicitly specified categorization.

Tested against every technical occurrence:

| Occurrence | Covered? |
|---|---|
| 1 (admissibility status) | Yes — categorization *admissibility*, value assigned by the classification |
| 2 (candidate status) | Yes — categorization *role in the investigation*, value *candidate* |
| 4–11 | Yes — categorization *epistemic/ontological standing*, values *candidate primitive*, *unique foundation*, *primitive*, *derived* |
| 12 (maintenance status) | Yes — categorization *maintenance*, value *Stable* |
| **3 (unresolved status)** | **Covered in form, but the occurrence violates the definition's own "explicitly specified categorization" clause.** |

**The definition is not vacuous.** It has inferential content: every technical status attribution must identify both the entity and the categorization. That content is precisely what isolates occurrence 3.

**Refined verdict, correcting `LIM-030`.** The prior record stated that canonical FARA uses `status` in "at least five distinct senses". **That was wrong.** The word is univocal under one abstract definition. What is genuinely ambiguous is the *compound construction* `N status`, which is systematically ambiguous between categorization-naming and value-naming — and this bites at exactly **one** occurrence, `admissibility-structure.md:111`, where the categorization is unstated and no governing definition exists.

- **`D1` rejected** — occurrence 3 is genuinely ambiguous.
- **`D2` survives, narrowly** — for the construction, at one occurrence.
- **`D3` rejected** — no occurrence has two incompatible senses *imposed*; occurrence 3 has two readings *available*, neither imposed.
- **`D4` largely holds** — for the word itself.

## Stage 6 — Repair options

| Repair | Assessment |
|---|---|
| **R1** qualified terminology only | Would require stating occurrence 3's categorization — the design choice that cannot be made. |
| **R2** abstract generic `status` plus qualified subtypes | **Partially available without any design choice.** The abstract definition in Stage 5 is *recovered from usage*, not invented, and can be recorded without resolving occurrence 3. |
| **R3** eliminate generic `status` from technical prose | Disproportionate: eleven of twelve technical occurrences are unambiguous under the recovered definition. |
| **R4** clarify only the ambiguous occurrence | Same blocker as R1. |

**Minimal repair justified by evidence: partial `R2`.** Record the recovered abstract definition, which reduces the defect from "five senses across canonical FARA" to "one occurrence with an unstated categorization", and **leave occurrence 3 unresolved**. No definition of `unresolved`'s semantics is proposed; the word `status` is clarified without touching it.

Even this repair is **not applied**: it changes a canonical surface, and Replication and Acceptance have not occurred.

## Stage 7 — Blocked-question propagation

Revisited only for dependency status; neither investigation is reopened.

| Question | Effect of `OP-18` |
|---|---|
| **`OP-16` / `UQ-T20`** (`M1` vs `M2` typing; semantic content) | **Leaves unchanged.** The only substitution bearing on it reproduces `OP-16`'s own non-redundancy argument and is not independent corroboration. No new discriminating evidence. `OP-18` does, however, *explain* why `OP-16` could only weakly establish its typing: occurrence 3 is the sole technical status occurrence lacking a governing definition and a stated categorization. Explanation is not evidence, and the typing remains weakly established with semantics underdetermined. |
| **`OP-17` / `UQ-T21`** (obligation scope) | **Leaves unchanged; confirms.** The ambiguity blocking `OP-17` is now precisely located and shown to be irreducible without a design choice. `OP-17`'s `H5` stands, and its conclusion that the asymmetry is interpretation-relative is reinforced rather than altered. |

Neither question is resolved. `OP-18` narrows and explains the blockage without removing it.

## Quality Gate disposition

**No canonical change applied.** The partial `R2` repair is justified in principle and requires no design choice, but the Charter lifecycle requires Replication and Acceptance before canonical text changes.

## Nonclaims

This investigation does not establish: the semantic content of `unresolved status`; which of `H1`/`H2` is intended; that no further occurrences exist outside the twelve canonical FARA documents; that the recovered definition is unique or complete; any typing, primitive, minimality, or completeness result. `Ω`'s type and semantics, FARA primitives, seven-primitive completeness, `UQ-T2`, `OP-02`, and the terminal UPP theorem are unaffected. No canonical surface, evaluation record, frozen evidence, or software was modified.
