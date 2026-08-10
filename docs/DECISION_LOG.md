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
**Established defect:** `status` is non-univocal across canonical FARA. The repair site is identified as a single scope clarification, but **the repair content is not supplied**, because the direction of clarification is exactly the undetermined question. Recorded as `LIM-030`/`OP-18`/`UQ-T22`.
**Interaction with `OP-16`:** none. Preferring the in-`S_K` typing because it removes the asymmetry would infer upstream ontology from downstream convenience. One weak non-convenience consideration favours the meta-status typing and is not treated as strengthening it. `OP-16`'s result is left unchanged: typing weakly established, semantics underdetermined.
**Repository change:** Research record plus register updates only. **No canonical surface modified.** `Ω`'s type and semantics, FARA primitives, seven-primitive completeness, `UQ-T2`, `OP-02`, and the terminal UPP theorem are unaffected.
