# Decision Log

## 2026-07-29 — Accept and promote the scoped FARA formal kernel

**Question:** Which coherent formal carrier architecture should govern canonical FARA within Project FAR v1.0 finite explicit auditable representational scope?

**Execution:** `FARA-CANONICAL-KERNEL-001` implemented and falsification-tested four candidates under eight mandatory architectural gates. `FARA-CANONICAL-KERNEL-REPLICATION-001` then used a separate Node.js implementation, three neutral scenarios, isolated execution, outcome-blind sequencing, Git-proven fixture ancestry, and fail-closed adjudication.

**Observation:** Identity-bearing many-sorted relational was the sole registered candidate passing all eight gates in both implementations. Pure extensional relations collapsed parallel occurrence identity. Typed hypergraph preserved the model but introduced universal graph scaffolding. Bare algebraic/state-transition omitted required nonoperational commitments and reconstructed exactly only with explicit sidecar machinery.

**Acceptance:** Accept `FARA-FORMAL-KERNEL-001` only for Project FAR v1.0 finite explicit auditable representational architecture. The accepted claim selects a formal carrier architecture; it does not reclassify the seven candidate primitives or establish their independence, necessity, minimality, or irreducibility.

**Promotion:** Promote `frameworks/FARA/formal-kernel.md` as the canonical formal-kernel source within the stated scope. Typed-hypergraph and algebraic/state-transition forms remain optional derived views. The immutable source and replication campaigns remain Research evidence.

**Repository change:** Synchronize FARA architecture/navigation, the canonical map, claim status, limitations, unresolved/open-problem registers, project status, and fail-closed promotion validation. Preserve the dependency direction foundations → shared theory → FARA → FAR → FARO.

**Claim boundary:** No global uniqueness, universality, primitive necessity/minimality, completeness, full-signature or unbounded adequacy, nonfinite continuous semantics, live-oracle semantics, embodied/environment-inclusive semantics, external-investigator independence, or superiority under every comparison criterion is established.

## 2026-07-26 — Stabilize the completed SWE-agent v2 evidence boundary

**Question:** How should the repository represent and protect the completed comparison after outcome reveal?

**Execution:** Compared frozen manifests, source and primary locks, reveal outcomes, generated reports, workflows, tests, and current navigation/status surfaces; ran deterministic verification and mutation-oriented repository checks.

**Observation:** The evidence agrees on four unresolved runs and `REVIEW_REQUIRED`, while the mutable execution-status page still described the pre-reveal phase. Execution remained dispatchable after completion, retryable internal failure was converted to outer success, and report verification could silently skip.

**Decision:** Preserve every frozen evidence artifact; update only mutable status/navigation surfaces; close mutation-capable stages after a final bundle exists; propagate internal failure; require committed reveal verification; and make the bounded claim machine-enforced. Historical provenance and dependency limitations remain registered rather than rewritten.

**Claim boundary:** This maintenance decision does not adjudicate equivalence, superiority, safety, readiness, general performance, or unresolved FAR/FARA/FARO theory.

## Purpose

This document records significant architectural and theoretical decisions made during the development of Project FAR.

Each entry records the decision, its rationale, and its impact on the framework.

The purpose of this log is to preserve design history, prevent repeated discussions of previously resolved issues, and document the evolution of the project.

---

# Decision 1

## Decision

Adopt `theory/definitions/definitions.md` as the canonical source for shared formal terminology.

---

## Rationale

Maintaining a single canonical source eliminates redundant definitions and ensures consistency throughout the repository.

---

## Impact

All architectural, methodological, operational, and documentation files now reference the canonical definitions instead of redefining terms.

---

# Decision 2

## Decision

Separate Project FAR into four primary components:

- FARA
- FAR
- FARO
- Theory

---

## Rationale

Each component has a distinct responsibility.

Separating them reduces redundancy and establishes a clear dependency structure.

---

## Impact

The repository now distinguishes architecture, methodology, operations, and formal theory.

---

# Decision 3

## Decision

Replace **Candidate Resolution** with **Candidate**.

---

## Rationale

The previous terminology introduced an unnecessary circular dependency.

A candidate exists before admissibility is evaluated or a resolution is selected.

---

## Impact

The dependency graph became acyclic and conceptually simpler.

---

# Decision 4

## Decision

Remove **Possibility Space** as a primitive architectural concept.

---

## Rationale

The concept was reducible to the collection of candidates admitted for consideration within an investigation.

Maintaining it as an independent concept added unnecessary complexity.

---

## Impact

The architecture was simplified without reducing expressive power.

---

# Decision 5

## Decision

Rename **Ω** to **Admissibility Structure (Ω)** on first reference.

---

## Rationale

The descriptive name communicates the purpose of Ω while preserving the symbolic notation.

---

## Impact

Repository terminology became clearer and more self-explanatory.

---

# Decision 6

## Decision

Introduce **Resolution Rules** as a concept distinct from the reasoning calculus.

---

## Rationale

Determining candidate admissibility and selecting a final resolution are logically distinct operations.

Separating them simplifies the architecture and clarifies the reasoning process.

---

## Impact

The workflow now distinguishes:

- Candidate classification
- Resolution selection

---

# Decision 7

## Decision

Replace **Fundamental Objects** with **Primitive Concepts**.

---

## Rationale

"Primitive" has a precise meaning within formal systems.

"Fundamental" is broader and may refer only to importance.

---

## Impact

Repository terminology now aligns with formal mathematical practice.

---

# Decision 8

## Decision

Organize the repository according to a directed dependency structure.

---

## Rationale

Every component should depend only upon lower-level components.

This minimizes circular dependencies and simplifies maintenance.

---

## Impact

The repository now follows the dependency order:

- Theory
- FARA
- FAR
- FARO
- Documentation

## 2026-07-26 — Canonical theory and protocol correction

**Question:** Could the active repository consistently distinguish upstream theory, downstream methods/evidence, and bounded claims?
**Execution:** Repository-wide authority, terminology, dependency, claim, procedure, theorem, protocol, navigation, and counterexample audit.
**Observation:** Authority was dispersed; independent procedures could be read as derived; strong claims and counterexample classes lacked one consolidated classification.
**Discovery/acceptance:** Preserve the dependency order foundations → shared theory → FARA → FAR → FARO; centralize terminology/status registers; keep unsupported global claims unresolved; freeze CRP v1.0 and record design-changing clarifications for v1.1.
**Repository change:** Added canonical specifications, audit/registers, navigation, and semantic checks. No frozen SWE-agent v2 evidence changed.

## 2026-07-26 — SWE-agent v2 forensic boundary

**Question:** Can the failed comparison support exact causal attribution from committed evidence?
**Execution:** Inventoried committed/frozen and hash-locked external artifacts; reconciled four identities/outcomes; reconstructed all required stages with explicit gaps; classified causes, alternatives, controls and falsifiers.
**Observation:** All applied patches failed the same target and all runs stopped at call-budget autosubmission, while exact trajectories and patch text remain external-only. The experiment contains one task, not two.
**Discovery/acceptance:** Preserve `no_observed_resolution_difference` and `REVIEW_REQUIRED`; accept patch failure, budget termination and diagnostic artifact loss as bounded facts; leave first agent mistakes and deepest patch causes Unknown.
**Repository change:** Add derived forensic records and fail-closed validation only. No v3 implementation, frozen rerun, held-out execution, or frozen evidence change is authorized.

## 2026-08-10 — Unresolved-questions identifier collision correction

**Question:** Did `docs/governance/unresolved-questions-register.md` assign one identifier to two distinct questions?
**Execution:** Enumerated `UQ-T` identifiers in the register; searched the non-archive repository, tooling, and machine-readable records for external references; used `git log -S` to establish which entry introduced the collision.
**Observation:** `UQ-T10` named two distinct questions. The representation-invariance entry entered in PR #419 (`6e63e28`); the `FARA-VOC-001` necessity entry entered later in PR #420 (`1665125`) and created the collision. Neither entry was referenced anywhere outside the register.
**Decision (not a discovery):** Reassign the later-introduced `FARA-VOC-001` entry to the next unused identifier `UQ-T14`. The earlier entry retains `UQ-T10`. This is an identifier-integrity correction determined by provenance, not by preference among the questions.
**Repository change:** Identifier only. No substantive wording, status, scope, or meaning changed; no external reference required updating; no question was opened, closed, merged, or reprioritized.

## 2026-08-10 — Set-valued admissibility representation in `Ω`

**Question:** Does FARA's per-candidate `Ω` admit a faithful representation of set-valued admissibility, or does multi-extension admissibility require retyping `Ω`?
**Execution:** Reused the existing `FAITHFUL-REP-001` faithfulness criterion rather than defining a new one. Surveyed set-valued admissibility across Dung argumentation, Reiter default logic, answer-set semantics, AGM partial meet, and maximal consistent subsets so the witness class is not Dung-specific. Constructed and tested four `C → Status` encodings before rejecting the hypothesis, then tested a conservative extension-indexed construction against six countermodel attacks.
**Observation:** Credulous, skeptical, and skeptical/credulous-trichotomy encodings each admit explicit finite collisions. More strongly, equivariance under source isomorphism forces `Ω` to be constant on sources with transitive automorphism groups, and four such frameworks on four candidates carry four distinct extension families against only three constant values, so no function `C → Status` can support admissible recovery.
**Discovery/acceptance:** Accept at Project FAR v1.0 finite explicit auditable scope only: retyping `Ω` is **not** required for set-valued admissibility. An extension-indexed family of unchanged canonical `Ω` structures is faithful and conservative, uses only existing primitives, and preserves the multiplicity, nonexistence, uncertainty, and underdetermination distinctions that a single-valued `Ω` destroys. Recorded as accommodation, not prediction; representational cost can be exponential and is charged, not hidden.
**Repository change:** Research record plus register updates only. `OP-13` resolved at finite scope; `OP-14`/`UQ-T18` opened for graded acceptability. The prior order-inversion observation is superseded as an artifact of forcing a single `Ω`. No evaluation record, frozen evidence, primitive classification, or software changed. The terminal UPP theorem and its frozen `E*` premise are untouched and unaffected.

> **SUPERSEDED IN PART — see the graded-admissibility entry below (same date).** The Observation above concludes that "no function `C → Status` can support admissible recovery." That conclusion is **withdrawn**: its equivariance pigeonhole assumed `card Status = 3`, which `frameworks/FARA/admissibility-structure.md:84` shows is not canonical. The three encoding-specific collisions survive; the general impossibility does not. The repair is reclassified from conservative extension to **semantic clarification**. This entry is retained unaltered as the historical record of the decision as taken.

## 2026-08-10 — Graded admissibility, and correction of the set-valued adjudication

**Question:** What is the weakest representation architecture capable of faithfully representing graded or ranking-based admissibility while conservatively preserving canonical `Ω`?
**Execution:** Fixed two structurally distinct source semantics before mapping: ordinal ranking-based semantics (Amgoud & Ben-Naim 2013, which produce a preorder and no extensions) and cardinal gradual semantics (h-categorizer). Reused `FAITHFUL-REP-001` unchanged. Attempted four `Ω`-only constructions before considering auxiliary grade, then tested the explicit `Ω : C → Status` plus `G : C → Grade` separation.
**Observation:** `frameworks/FARA/admissibility-structure.md:84` assigns the available admissibility classifications entirely to the reasoning calculus, so canonical FARA never fixes `Ω`'s codomain. A numeric status carries gradual semantics and a partially ordered status carries ranking semantics. A totally ordered status destroys incomparability. Under threshold-free semantics a three-valued `Ω` has no determinate content, so grade is constitutive rather than auxiliary.
**Discovery/acceptance:** Accept at Project FAR v1.0 finite explicit auditable scope only. The weakest justified outcome is **semantic clarification**: no change to canonical `Ω`, no codomain generalization, no retyping, and no new primitive. H1 was not eliminated, so canonical `Ω` is not altered. A defect is recorded: no canonical requirement was located that a calculus keep ties, incomparability, uncertainty, and unresolved mutually distinct.
**Correction (affects a committed result):** The preceding set-valued investigation refuted every function `C → Status` by an equivariance pigeonhole assuming `card Status = 3`. That premise is not canonical and the general impossibility claim is **withdrawn**. The verdict is unchanged in substance — no retyping, no new primitive, same representational cost — but the repair is reclassified from conservative extension to semantic clarification, and `CE-ADM-001` now refutes only the three-valued reading. Registers corrected accordingly.
**Repository change:** Research record plus register corrections and additions only. `OP-14` resolved; `OP-15`/`UQ-T19`/`LIM-028` opened. No evaluation record, frozen evidence, primitive classification, canonical definition, or software changed. The terminal UPP theorem and its frozen `E*` premise are untouched and unaffected. The README and `docs/project-status.md` phase conflict remains preserved as unresolved.

## 2026-08-10 — Admissibility classification-space authority audit

**Question:** What constraints, if any, must the classification space of a FARA reasoning calculus satisfy for `Ω` to preserve admissibility semantics faithfully, and at what architectural layer does that obligation belong?
**Execution:** Audited foundations, shared theory, FARA, the terminology authority, the vocabulary index, and the framework-boundary specification in dependency order for requirements on distinction preservation, reflection, ties, incomparability, uncertainty, unresolved status, information loss, explicit classification, and calculus-defined classification structures. Tested four independent collapses. Discriminated five architectural placements.
**Observation:** The located canonical requirements govern architectural category separation, totality of coverage, traceability, and auditability — none governs classification-space granularity. Three canonical texts converge on a deliberately permissive stance: `theory/definitions/definitions.md:344` permits mappings to discard, `:378` makes complete fidelity a demonstrable claim rather than a default, and `frameworks/FARA/admissibility-structure.md:84` delegates the classification space to the calculus. `admissibility-structure.md:204` holds admissibility preservation open as research.
**Discovery/acceptance:** Accept H5 — no additional normative requirement is justified. Placing a faithfulness obligation in shared theory would contradict `:344`; placing an admissibility preservation obligation in FARA would promote open research to canonical requirement. The weakest sufficient rule is `FAITHFUL-REP-001` §5.2 specialized to the admissibility axis, which is derivable and already stated, and which supplies distinction preservation only, not reflection.
**Correction:** `LIM-028` framed the missing requirement as a defect. The negative search result stands, but the framing was wrong: the absence is deliberate delegation. Reframed.
**Genuine defect located:** `unresolved status` carries normative force at `admissibility-structure.md:111` with no canonical definition, no terminology-authority owner, and no index entry, and must not be conflated with FARO `uncertainty` or the Charter artifact status `Unknown`. Recorded as `LIM-029`/`OP-16`/`UQ-T20`. A minimal revision is identified but **not applied**: Replication and Acceptance have not occurred, so the Charter lifecycle does not authorize a canonical text change.
**Repository change:** Research record plus register corrections and additions only. No canonical surface, evaluation record, frozen evidence, primitive classification, or software changed. `Ω`'s type and semantics are unchanged. Seven-primitive completeness, `UQ-T2`, and `OP-02` are unaffected in both directions. The terminal UPP theorem and its frozen `E*` premise are untouched. The README and `docs/project-status.md` phase conflict remains preserved as unresolved.

## 2026-08-10 — `unresolved status` semantic audit

**Question:** What exactly is FARA's `unresolved status`, and which canonical layer owns its definition?
**Execution:** Reconstructed every authoritative use of unresolved, unknown, uncertainty, indeterminate, undetermined, unclassified, and admissibility status across foundations, shared theory, FARA, FAR, FARO, the terminology authority, governance, and CRP methodology. Derived behavioural constraints from canonical FARA alone. Tested seven distinction cases and five type-level models. Discriminated six candidate owners.
**Observation:** Canonical FARA uses the term exactly once, at `frameworks/FARA/admissibility-structure.md:111`, inside a "should" property list. Shared theory contains zero occurrences of the concept. Five lexically similar concepts are distinct by subject and layer: FARA unresolved status (a candidate), FAR `Unresolved` (an investigation closure, and the only canonically defined one, downstream), FARO `uncertainty` (an operational output), Charter `Unknown` (an artifact status), and CRP `Unknown` (a preservation-dimension value).
**Discovery/acceptance:** Split outcome. Owner is **FARA** — established; shared theory, FAR, FARO, and governance are each rejected. Type is a **framework-level meta-status outside the calculus-determined classification set** — **weakly** established, resting on a non-redundancy reading of `:111` that is a reading rather than a forced inference. Reason-carrying and package-layer models are rejected as unforced or contradicting `:111`. **Semantic content is returned as underdetermined (`H4`)**: canonical evidence does not fix whether unresolved covers no-answer, not-yet-computed, evaluator ignorance, or insufficient evidence, and it is not invented. One derivable distinction: a source semantics' explicit "undecided" value belongs in the classification set and is not unresolved.
**Repository change:** Research record plus register updates only. **No canonical surface modified.** A one-row terminology-authority change is drafted and falsification-tested but unapplied: Replication and Acceptance have not occurred, and a weakly established result is not a basis for canonical promotion. `OP-17`/`UQ-T21` opened on the traceability asymmetry between classified and unresolved candidates. `Ω`'s type and semantics, FARA primitives, seven-primitive completeness, `UQ-T2`, `OP-02`, and the terminal UPP theorem are all unaffected.

## 2026-08-10 — Unresolved-candidate obligation-scope audit

**Question:** What traceability and auditability obligations apply to a FARA candidate represented as unresolved, and is the apparent asymmetry architectural or terminological?
**Execution:** Reconstructed the grammatical and semantic scope of every canonical obligation clause bearing on classification, status, traceability, auditability, criteria, and grounds. Tested four interpretations, seven unresolved-cause countermodels, and six necessity questions. Downstream FAR, FARO, Charter, and `FAITHFUL-REP-001` material was used only as comparison evidence and supplied no premises.
**Observation:** Exactly one canonical clause reaches unresolved — the Explicitness property at `frameworks/FARA/admissibility-structure.md:111` — and it requires only a marker. Traceability (`:117`), `Ω` Auditability (`:144`), and Principle 6 (`design-principles.md:80-89`) are each worded in terms of "admissibility classification". Whether that wording covers the unresolved result turns on a lexical bridge from `:23` ("a classification is the explicit assignment of admissibility **status**") that fails to carry force because `status` is used in at least five distinct senses across canonical FARA without disambiguation.
**Discovery/acceptance:** Return `H5`. **The asymmetry is not established as architectural**: it holds under the narrow reading and dissolves under the broad reading, and canonical text supports both, so the ambiguity is preserved rather than resolved. Intent is not established either; `:204` marks the area as open research. Two derived results stand independently of the ambiguity: traceability requires **path-linking, not cause-recording**, and auditability of unresolved **causes** is not generally satisfiable, because an unknown cause cannot be reconstructed. An unresolved result can be auditable without being a substantive classification, by auditing the derivation rather than a nonexistent object — the form `transition-signatures.md:85` already uses.
**Established defect:** `status` is non-univocal across canonical FARA. *(Superseded the same day by the `OP-18` term audit below: the five-sense premise is refuted and `status` is univocal; the surviving defect is the compound `N status`, ambiguous at exactly one occurrence. The `H5` verdict and the path-linking and unknown-cause results of this entry do not depend on the withdrawn premise and stand.)* The repair site is identified as a single scope clarification, but **the repair content is not supplied**, because the direction of clarification is exactly the undetermined question. Recorded as `LIM-030`/`OP-18`/`UQ-T22`.
**Interaction with `OP-16`:** none. Preferring the in-`S_K` typing because it removes the asymmetry would infer upstream ontology from downstream convenience. One weak non-convenience consideration favours the meta-status typing and is not treated as strengthening it. `OP-16`'s result is left unchanged: typing weakly established, semantics underdetermined.
**Repository change:** Research record plus register updates only. **No canonical surface modified.** `Ω`'s type and semantics, FARA primitives, seven-primitive completeness, `UQ-T2`, `OP-02`, and the terminal UPP theorem are unaffected.

## 2026-08-10 — `status` term audit

**Question:** What distinct senses of `status` occur in canonical FARA, which sense is recoverable at each occurrence, and can the ambiguity around `unresolved status` be eliminated without a new design choice?
**Execution:** Inventoried every occurrence of `status`/`statuses` and `classification`/`classifications`/`classified` across the twelve canonical FARA documents named in `docs/CANONICAL_MAP.md`, separating document metadata from technical prose. Assigned each technical occurrence its weakest context-supported sense, ran pairwise substitution tests, sought only lexical discriminators for the `unresolved status` question, and attempted a single abstract definition covering all technical uses.
**Observation:** Twelve technical occurrences and eleven metadata occurrences. The technical uses partition two ways by how the compound `N status` is built — naming the categorization (admissibility, maintenance) or naming the value (candidate, candidate primitive, unique foundation, primitive/derived, unresolved). Substitution shows primitive-status and foundation-status collapse under "epistemic status", and that candidate status is not admissibility status. `admissibility-structure.md:111` is the only technical occurrence with no governing definition and no stated categorization.
**Discovery/acceptance:** The single abstract definition — the standing of an entity under an explicitly specified categorization — covers every technical occurrence with inferential content, so `status` is **univocal** and the prior five-sense record is **refuted**. The residual defect is the compound construction, and it bites at exactly one occurrence. **`H3` is preserved for `unresolved status`**: canonical evidence is exhausted, the construction is neutral between the readings, and no authorial reconstruction is offered. The substitution failure at `:111` restates `OP-16`'s non-redundancy argument and is not independent corroboration.
**Answer to the posed question:** the ambiguity around `unresolved status` **cannot** be eliminated without a new design choice; the remainder of the non-univocity **can**, by recording a definition recovered from usage.
**Correction:** `LIM-030` is corrected from "at least five distinct senses" to one univocal word with an ambiguous compound construction at a single occurrence.
**Propagation:** `OP-16` and `OP-17` are **left unchanged**. `OP-18` explains why `OP-16` could only weakly establish its typing, but explanation is not evidence. `OP-17`'s `H5` is reinforced, not altered. Neither investigation is reopened.
**Repository change:** Research record plus register corrections and additions only. **No canonical surface modified.** A partial repair requiring no design choice is identified but unapplied: Replication and Acceptance have not occurred. `OP-19` opened on an adjacent `candidate` polysemy observed but not pursued.

## 2026-08-10 — Close the admissibility investigation branch as evidence-exhausted

**Question:** Should the `OP-15` → `OP-18` chain continue, or has canonical evidence been exhausted?
**Execution:** Four completed investigations converged independently on `frameworks/FARA/admissibility-structure.md:111`. Each established, by a different route, that canonical evidence underdetermines it: no classification-space requirement exists and the permissiveness is deliberate (`OP-15`); the typing is only weakly established and the semantics underdetermined (`OP-16`); the obligation asymmetry is interpretation-relative (`OP-17`); the term `status` is univocal and the residual ambiguity is irreducible without a design choice (`OP-18`).
**Observation:** The residue is not a discoverable fact. It is a choice between two coherent architectures that the canonical text does not decide.
**Decision:** Close `OP-15` through `OP-18` and `UQ-T19` through `UQ-T22` as **evidence-exhausted, not resolved**. Reclassify the residue from an unresolved research question to an architectural decision point, recorded as `ADR-002` using the existing ADR mechanism rather than a new artifact class. Both alternatives are preserved with their established consequences, and **neither is selected**. No further research audit downstream of `:111` is authorized; the next step there is an authorized decision, not an investigation.
**Repository change:** New `docs/architecture/adr/ADR-002-Unresolved-Admissibility-Status-Semantics.md` with status "Open — decision required"; closure notes in the open-problems and unresolved-questions registers. No canonical surface modified. `LIM-029` and `LIM-030` remain open as recorded boundaries.

## 2026-08-10 — Prior-framework subsumption investigation (`OP-20`)

**Question:** Does any independently motivated prior framework subsume, derive, reduce, or establish a materially significant structural equivalence with FARA at a specified scope?
**Execution:** Froze the target as the Accepted formal kernel at its registered scope — a finite many-sorted relational structure over 15 sorts and 15 relations under 11 constraints, taken up to sort-preserving isomorphism — excluding FAR, FARO, and shared-theory operators. Defined `R0`–`R6` and fixed subsumption criteria before candidate evaluation. Reconstructed each serious candidate natively before introducing FARA terminology. Ran reverse mappings, recovery tests, and assumption-independence tests, then audited all twenty external-system records for direction and claim strength.
**Observation:** Every tested kernel component is independently anticipated by prior work. W3C PROV-DM reaches faithful representation on a connected nine-relation fragment with no forced assumptions, but has no semantic layer; Meseguer's general logics owns exactly that semantic and calculus-parameterization layer but has no trace layer and sits at a mismatched abstraction level. The two strongest adversaries are complementary and neither repairs into the other without importing the structure at issue. Many-sorted model theory subsumes the kernel definitionally but uninformatively.
**Discovery/acceptance:** Accept `H6` at the tested scope, with a substantial Stage-10-B component in the Semantic Web stack. `H1` refuted; `H3` holds for PROV on its fragment; `H4`/`H5` not established. **Novelty and non-novelty are both unestablished** — this was formal subsumption analysis, not a historical search.
**Correction:** The prioritization preceding this investigation characterized the external-validation evidence base as a "blind spot" and "confirmation-biased." The exhaustive audit does not support that. All twenty records are one-directional, but none claims novelty, originality, or irreducibility, so the claims drawn are correspondingly bounded. The asymmetry is a **scope limitation, not a defect**. No claim is downgraded.
**Dependencies:** none demonstrated. No propagation into `OP-01`, `OP-02`, `OP-03`, `OP-09`, `OP-12`, `UQ-T2`, or the terminal UPP result is asserted.
**Repository change:** Research record plus register updates only. No canonical surface, evaluation record, frozen evidence, or software modified. `UQ-T24` opened on whether a prior synthesis binds semantics, trace, occurrence identity, and provenance under one equivalence relation.

## 2026-08-10 — `LIM-016` refutation search (null, with a structural obstruction)

**Question:** Does there exist an independently defensible and semantically faithful primitive-layer formalization under which any one of the seven candidate primitives is derivable from the other six plus independently justified background structure?
**Execution:** Strictly one-directional. Recovered each primitive's canonical functional role from `theory/definitions/definitions.md` before formalizing; fixed the derivability criterion and the formalization-admissibility criterion before searching; constructed two materially different admissible families — many-sorted relational and single-sorted with typed predicates, the latter chosen because it is most favourable to finding a witness; attempted derivations for all seven; ran the hidden-primitive audit and recovery tests on every survivor.
**Observation:** Five of seven primitives are **non-testable** because their canonical definiens rests on unformalized terms, and Reasoning Calculus is additionally blocked by an open architectural decision (`ADR-002`) over `admissibility`. Object fails circularly. Relation's tupling construction is cleanly **rejected as relocation**. Property's reification construction — canonically licensed by `definitions.md:64` — and Representation's definable-predicate construction both fail the hidden-primitive audit in the same way.
**Discovery/acceptance:** **NULL.** No admissible derivation witness was found in the tested families. A family-independent obstruction is identified: eliminating a primitive in any relational formalization requires designating a relation symbol carrying that primitive's semantic content, and canonical text does not settle whether that is elimination or relocation. **`LIM-016` is therefore self-blocking** — testing derivability requires exactly the semantics whose absence constitutes it. The W2/W4/W5 auxiliary-model precedent does not transfer, because those models supplied dynamics rather than primitive meanings.
**Explicitly not concluded:** independence, irreducibility, minimality, completeness, or the absence of a fourth or fifth primitive. Absence of a witness is not evidence of independence. `W1`'s seven `unresolved` adjudications are unchanged.
**Correction:** the preceding prioritization ranked `LIM-016` first on the reasoning that a refutation-seeking formulation avoids the arbitrary-choice trap. That reasoning is **wrong** — the refutation direction is blocked by the same missing semantics, because the hidden-primitive audit cannot be discharged without them. `LIM-016`'s executability is downgraded in both directions.
**Impact:** `OP-02`, `OP-03`, `OP-09`, `OP-12`, and `UQ-T2` are unchanged, still unresolved, still blocked; a null carries no upgrade. No propagation to `OP-01`, universality, or the terminal UPP theorem.
**Repository change:** Research record plus register updates only. No canonical surface, evaluation record, frozen evidence, or software modified.

## 2026-08-10 — Externally grounded contract-frontier discovery

> **SUPERSEDED IN PART — read the correction first.** The paragraphs below record this decision **as originally taken**. Their Pareto, frontier, maximality, `H2`, `B`+`F`, canonical-quotient, and RCCD/FARA contract-relativity claims are **withdrawn or narrowed** by "Correction of the contract-frontier discovery record" (same date, below). Retained unaltered for provenance; **not the current adjudication**.

**Question:** Across independently developed theories of reasoning, information, semantics, representation, computation, and system equivalence, which preservation contracts `(C,Q,E,T)` are independently motivated strongly enough to define serious alternatives for the Project FAR universality question, and what Pareto relation holds among them?
**Execution:** Reconstructed all existing Project FAR contract machinery first and marked every component as independently motivated, project-authored-but-derived, methodological choice, frozen premise, unresolved, or externally unvalidated. Then searched primary literature and reconstructed six external frameworks **natively, before applying any Project FAR term**: Blackwell comparison of experiments, van Glabbeek's linear time–branching time spectrum, Goguen–Burstall institutions with Meseguer general logics, Cousot abstract interpretation, Myhill–Nerode and Kalman minimal realization, Rutten universal coalgebra, and De Nicola–Hennessy testing with Milner/Plotkin contextual equivalence. Extracted seven candidate contracts under a rule rejecting any candidate whose crucial clause exists solely to reproduce `P*`/`E*`, RCCD, FARA, or the terminal theorem. Admitted seven comparison dimensions, each justified by at least one external source treating it as a first-class axis. Placed `C*`/`P*`/`E*` only after the external candidates and dimensions were fixed.
**Observation:** Three of the seven dimensions — preservation strength, recovery strength, observational discrimination — are **anti-monotone** with source coverage, so any coverage-monotone total order is maximized at the degenerate bare-set contract, whose forced architecture is trivial. Four external contracts are pairwise Pareto-incomparable maximal elements, and `C*`/`P*`/`E*` is incomparable with each. Every `P*` component is independently anticipated outside the project; the conjunction is not recovered by any framework located. Every surviving contract forces a *different* canonical object, and only `P*`/`E*` forces RCCD — but each forced object is the canonical quotient of its own declared observations, so the cross-contract invariant is the construction pattern rather than the architecture. Reconstructing `P*` inside institutions or coalgebra failed at forced reconstruction, the identical failure `OP-20` recorded when pushing PROV-DM toward `R4`.
**Discovery/acceptance:** Accept `H2` held jointly with `H5`, terminal classification `B`+`F`. `H1`, `H3`, and `H6` rejected; `H4` rejected as the sole verdict because componentwise anticipation is strictly more informative than bare incomparability. **RCCD is contract-relative, established. FARA is contract-relative and realization-plural.** Both statements report the reach that `G2`, `IKD-W9`, and `TUE-W4` already declare; **no registered claim is downgraded.** The `H2` placement is explicitly weaker than the `H5` finding, because the dimension set was chosen with knowledge of the contract's profile while `H5` does not depend on it.
**Reframing, not a claim change:** contract selection is a known unsolved problem in at least three mature independent fields — concurrency theory has not converged on which observations are "reasonable," the Blackwell order is deliberately partial with most experiments unrankable, and universal coalgebra is parametric in the observation functor by design. Project FAR's inability to independently justify `C*`/`P*`/`E*` is therefore **not a project defect**, and `FAR-CANONICAL-UNIVERSALITY-DECISION-001`'s `not_derivable` verdict is not a gap awaiting closure — results conditioned on a declared contract and presented over a frontier are the normal terminal form for this class of question. The verdict itself is unchanged.
**Bridge consequence:** bridge witnesses are ranked by ability to change the frontier. `maximal_knowability` is highest — it is the contract-comparison question in Lean, with a concrete test now available. `quotient_minimality` is second, and Nerode's coarsest-congruence argument supplies the external witness template. `definitional_completeness` and `conservative_extensibility` currently **fail** the can-change-the-frontier test and should not be built before the frontier moves.
**Established deficit:** no party outside Project FAR has ever chosen or evaluated a preservation contract for the universality question. Recorded as `LIM-031`. This campaign is **weaker than `USD-W6`'s `internal_robustness_only`** — single path, no mutation controls, no external reviewer — and must not be cited as independence. R5 cross-context replication is the direct instrument and has **no frozen package**.
**Repository change:** Research record plus register additions only. `OP-21`, `UQ-T25`, `UQ-T26`, and `LIM-031` opened; claim-status rows added. **No canonical surface, evaluation record, frozen evidence, primitive classification, or software modified.** `Ω`'s type and semantics, the seven candidate primitives, completed `LIM-016`, `ADR-002`, `UQ-T2`, `OP-02`, `FARA-FORMAL-KERNEL-001`, and the terminal UPP theorem with its frozen `E*` premise are all unaffected. The README and `docs/project-status.md` phase conflict remains preserved as unresolved.

> **SUPERSEDED IN PART — see "Correction of the contract-frontier discovery record" (same date, below).** The Observation, Discovery/acceptance, and Reframing paragraphs above assert a Pareto relation over contracts, four pairwise-incomparable maximal elements, terminal classification `B`+`F`, that every contract forces a different canonical object and yields a canonical quotient, that RCCD and FARA are contract-relative, and three state-of-the-art claims. **All of these are withdrawn or narrowed.** The comparison was constructed without assigning any dimension a justified preference orientation, which leaves dominance undefined. Surviving: `H5`, `H1` not established, the six native reconstructions, every candidate rejection, the proved bare-set barrier and the refutation of coverage-only optimization, the restricted field-specific orders, and `LIM-031`. Corrected terminal classification is `E`+`F`. This entry is retained unaltered as the historical record of the decision as taken.

## 2026-08-10 — Correction of the contract-frontier discovery record

**Question:** Does the `OP-21` contract-frontier result survive an internal re-audit of its comparison argument?
**Execution:** Re-derived the Pareto construction from first principles. For each of the seven comparison dimensions, asked what raw property it measures, whether larger or smaller is normatively preferred, and whether that preference is externally justified by the cited tradition. Re-tested every claimed maximal element for a non-domination proof. Re-audited each Stage-5 "forced canonical object" row against what the cited native theory actually proves. Re-evaluated `H1`–`H7` independently of one another. Re-derived the consequences of a `maximal_knowability` non-embedding. Reclassified the source list by kind.
**Observation:** The record constructed a Pareto dominance relation **without assigning any dimension a preference orientation**, which leaves dominance undefined. The defect is visible on the record's own profile table: the degenerate bare-set boundary scores maximal on coverage and transformation invariance and minimal on structural assumptions, so the claim that every serious contract dominates it "at no cost on any admitted dimension" is false. Examining each dimension against its source tradition, **none carries an externally justified global preference direction** — van Glabbeek orders semantics by discriminating power without ranking them, Blackwell's order is decision-relative, and effectivity and structural prerequisites trade applicability against strength. All seven are tradeoff axes. Of the seven Stage-5 rows, one is an unconditional theorem, one is conditional on regularity, three are conditional theorems, and three are **not established** — Blackwell does not construct a minimal sufficient statistic, full abstraction is a property proved of a proposed model rather than yielded by a contract, and "the institution itself" is a category error.
**Discovery/acceptance:** Corrected in place, nothing deleted, every withdrawn claim retained at its original site under a marker. **Withdrawn:** every global Pareto, frontier, dominance, and maximality claim; `H2` as established; the rejection of `H3`, `H4`, and `H6`; terminal classification `B`; three Stage-5 rows and the claim that every contract yields a canonical quotient; "RCCD is contract-relative" and "FARA is contract-relative" as global claims; the `maximal_knowability` frontier consequences; and the three state-of-the-art claims. **Corrected dispositions:** `H5` supported; `H1` not established; `H2` not established; `H3` and `H4` **unresolved** — `H4`'s prior rejection rested on the invalid ground that a competing hypothesis was "more informative", and a proposition is not falsified by another carrying more information; `H6` **split**, supported globally and refuted within field-specific scopes. **Terminal classification `B`+`F` → `E`+`F`.** **Surviving unchanged:** `H5`; `H1` not established; the six native reconstructions; every candidate rejection including the forced-reconstruction failures; the proved bare-set barrier and the conclusion that coverage maximization alone does not select a useful reasoning contract; the existence of restricted field-specific orders at their own scopes; and `LIM-031`, which the correction strengthens.
**Bridge consequence:** a proof that the testing scope does not embed into `C*` establishes **one failed directed reduction under one embedding notion** — not the converse direction, not incomparability, not maximality, not `H4`, not "≥2 maximal frontier elements", and nothing about an unexamined dominating contract. Being internally authored it cannot address `LIM-031`. `maximal_knowability` is **downgraded from highest to low**; `quotient_minimality` becomes the highest-standing bridge, because its falsification power does not depend on any contract comparison.
**Claim-scope corrections:** RCCD is established **only conditionally** under the proved `P*`/`E*` result; contract-invariance across the serious contract space is **neither established nor refuted**. The same discipline applies to FARA, whose realization-plurality inside `CEC-RCCD-001` stands independently on `IKD-W8` while global contract-relativity is withdrawn. State-of-the-art claims are narrowed to *several mature external traditions also leave observational choices parameterized*, *this limitation is not unique to Project FAR*, and *`not_derivable` is terminal for the currently available internally authored evidence class; genuine external contract selection or replication could change the warrant* — removing an incoherence that had implied external replication both could not change the conclusion and was the missing evidence.
**Repository change:** Research record corrected in place plus register corrections. **No canonical surface, evaluation record, frozen evidence, primitive classification, or software modified.** `ADR-002`, completed `LIM-016`, `UQ-T2`, `OP-02`, `FARA-FORMAL-KERNEL-001`, `G2`, `IKD-W9`, `TUE-W4`, and the terminal UPP theorem with its frozen `E*` premise are all unaffected; no registered claim is downgraded.
