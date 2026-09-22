# FAR Investigation Validation

## Purpose

This document defines the minimum validation checklist for a completed FAR investigation.

It is methodological validation, not FARO auditing.

FARO may later operationalize or automate these checks, but the checks themselves belong to FAR.

---

## Contract-Discovery Intake Validation

When the supplied input is not itself an explicit validated downstream comparison-contract artifact, validation begins with the governed intake record.

Intake may be bypassed only when the supplied artifact itself is machine-readable, the applicable downstream schema and semantic validator accept it, and the investigation records the artifact's exact format/version, content hash, and validation result. A prose assertion that the contract is complete or that intake is not applicable fails this gate.

When intake applies, require all of the following:

- the record satisfies the published `far-intake/1.0` JSON Schema before semantic validation;
- the exact raw input is preserved and its SHA-256 recomputes;
- materially distinct claim parses and terms are explicit;
- every term's material/non-material classification has an auditable source/raw-input/inference basis and records the consequence of misclassification;
- parse, interpretation, and compatibility exclusions have an auditable source/raw-input/inference basis rather than an analyst-written reason alone;
- source-derived interpretations have source provenance;
- source synthesis and inference have explicit derivations;
- discovered parses and interpretations do not disappear without exclusion records;
- at least one claim parse remains active;
- known assumptions state what changes if they are false;
- every active material term and active claim parse has recorded search coverage;
- the bounded search protocol, evidence cutoff, stopping rule, timestamped saturation observations, and limitations are recorded;
- registered queries and sources appear in saturation provenance and the final saturation observation reports no new material parse or interpretation;
- source retrievals and saturation observations precede both the evidence cutoff and the freeze;
- the contract family covers every active material interpretation combination unless that exact combination has a valid compatibility exclusion;
- every retained zero-material parse contributes the singleton empty-assignment candidate;
- each candidate contract hash recomputes;
- every scalar or empty-container leaf of each candidate downstream contract has exactly one valid provenance trace to raw input, sources, selected interpretations, declared assumptions, or explicit inference;
- interpretation-based parameter provenance does not reference interpretations outside the candidate's selected assignments;
- `intake_sha256` binds the exact raw input and discovery object;
- `freeze_sha256` binds the intake hash and exact freeze timestamp;
- no evaluation predates the intake freeze;
- each evaluation binds both the exact frozen candidate contract hash and exact freeze identity;
- each non-`Unknown` evaluation has evidence references, while `Unknown` has an explanation;
- every frozen candidate is evaluated before a cross-contract aggregate is issued;
- any result-relevant frozen `Unknown` assumption blocks invariant terminal promotion;
- the cross-contract aggregate follows the fixed `far-intake/1.0` rule rather than an analyst-selected preferred contract.

A draft, incomplete, invalid, or unresolved-assumption intake cannot support an invariant non-`Unknown` cross-contract verdict.

Passing intake validation establishes bounded procedural conformance only. It does not establish open-world semantic completeness, source truth or authority, independent retrieval of source bytes, uniquely unbiased contract selection, or downstream contract adequacy.

## Contract-Relative Validation Gates

Before the existing checklist, validate the following whenever the investigation makes a representation claim:

- claim, domain, quantifiers, evidence cutoff, and nonclaims are frozen;
- the intake gate is satisfied, or bypass is proven by an exact supplied machine-readable downstream contract artifact with recorded format/version, content hash, and successful applicable schema/semantic validation;
- cases, tests/contexts, typed outcomes, observation semantics, and consequence-affecting parameters are explicit;
- admitted translations/equivalences, interpretation profiles, and interface frame are explicit;
- approximation or cost orders are present for any non-exact or non-information minimality claim;
- the representation mapping and charged auxiliary machinery are reconstructible;
- a decoder/factorization certificate, a collision witness, or `OPEN` is recorded;
- determinate absence and epistemic Unknown are not collapsed when observable;
- common content is profile/frame/target indexed;
- primitive/operator language is not inferred from spelling;
- the terminal report uses a typed outcome and exposes falsifiers and remaining boundaries.

Passing methodological validation does not itself prove factual premises, mathematical theorems, domain adequacy, or independent validation.

## Evidence-Closure Validation Gate — `FAR-EVIDENCE-CLOSURE-1.0`

Validate the post-evidence closure contract defined canonically in `workflow.md` before accepting either `Resolved` or `Provisionally resolved` as a completed FAR investigation.

A decisive atomic verdict is not evidence that the closure gate passed. Claim-level logical disposition and methodological closure must be recorded and validated separately.

Require all of the following:

- **EC-01 — Separate adjudication from closure.** The exact claim form, atomic decomposition, claim-level logical disposition, disposition time/evidence basis, and investigation closure status are distinct and reconstructible.
- **EC-02 — Bind decisive evidence to the exact proposition.** The decisive evidence states what it establishes or refutes and what nearby stronger, broader, causal, comparative, mechanistic, or frequency proposition it does not establish.
- **EC-03 — Enumerate evidence/search classes.** Every evidence/search class material to the frozen interpretation is registered. Each is executed or marked `NOT APPLICABLE` with a reason. Direct or mechanism-specific evidence is searched when aggregate evidence cannot identify the claimed mechanism or concrete implementation detail.
- **EC-04 — Check denominator and directness alignment.** The record tests whether evidence matches the relevant estimand, denominator, conditioning set, population, comparison class, mechanism, and level of directness. Any bridge from proxy/aggregate evidence to the interpreted proposition is explicit.
- **EC-05 — Check measurement and classification.** Material measurement, coding, classification, provenance, ascertainment, missingness, reporting, and state/version limitations are identified with their possible effect on interpretation, magnitude, or terminal boundary.
- **EC-06 — Seek both evidentiary directions after the initial disposition.** The record identifies the strongest support and strongest counterevidence still relevant to the frozen scope after the first decisive result.
- **EC-07 — Test alternative explanations and inference paths.** Material alternative explanations or inference paths are tested where the claim form permits them, including causal, historical, statistical, forensic, semantic, or logical alternatives that could change interpretation or verdict scope.
- **EC-08 — Preserve surviving propositions.** Narrower, adjacent, conditional, comparative, mechanism-specific, or subgroup propositions that remain live after the main adjudication are explicit; the parent verdict is not mechanically copied to them.
- **EC-09 — Record residual uncertainty.** Unresolved empirical, formal, interpretive, measurement, classification, source, or generalization questions are explicit. An empty residual-uncertainty record has an explicit basis.
- **EC-10 — Execute a terminal bounded saturation pass.** The terminal bounded saturation pass rechecks every registered applicable evidence/search class under the current evidence cutoff and search frame and produces no new material evidence, no new material claim decomposition, no new material alternative explanation, and no new residual uncertainty. Any new item invalidates the attempted closure and requires another investigation cycle.
- **EC-11 — Run the methodology audit.** The current methodology audit executes after EC-01 through EC-10 and explicitly checks for premature stopping caused by decisive evidence and for any newly exposed methodological failure.

The closure record must preserve the evidence cutoff, search frame, applicability decisions, inclusion/exclusion rules, stopping rule, terminal pass result, surviving propositions, residual uncertainty, and methodology-audit result.

Passing `FAR-EVIDENCE-CLOSURE-1.0` establishes bounded methodological closure only. It does not establish open-world source completeness, semantic completeness, universal generalization, factual truth of every premise, or independent replication.

A failed or unexecuted closure gate cannot be relabeled `Provisionally resolved` merely because the atomic verdict is strong. Preserve the atomic verdict at its exact scope and use `Unresolved`, `Suspended`, `Incomplete`, `Invalid`, or another applicable non-closure boundary until the gate is satisfied.

## Validation Standard

A FAR investigation is methodologically valid only if its required artifacts are explicit enough to support audit, reconstruction, and review.

Validation does not imply that the resolution is true, optimal, final, or uniquely correct.

Validation means the investigation was conducted and recorded according to FAR methodology.

For `Resolved` and `Provisionally resolved` investigations, methodological validity additionally requires `FAR-EVIDENCE-CLOSURE-1.0` to pass independently of the claim-level logical disposition.

---

## Optional Stage Policy

A workflow stage may be marked `Not applicable` only when the investigation record states why the stage is not applicable.

No stage shall be silently omitted.

If a stage is skipped without justification, the investigation is incomplete.

---

## Minimum Checklist

A completed FAR investigation should satisfy the following checks.

### 1. Investigation Defined

- The investigation is explicitly identified.
- The objective is stated.
- The relevant conditions or scope are stated.
- The governed intake record is referenced when contract discovery was required; when intake was bypassed, the exact supplied validated contract artifact, format/version, content hash, and validation result are referenced instead.

---

### 2. Representational Structure Specified

- The relevant representations are identified.
- The relations among representations are recorded or explicitly scoped.
- Missing representations are identified if relevant.

---

### 3. Interpretation Specified

- The interpretation assigned to representations is stated.
- Any changes in interpretation are explicitly recorded.
- Material interpretations frozen by intake are preserved or superseded only by an explicit revision that invalidates dependent evaluations.

---

### 4. Reasoning Calculus Identified

- The reasoning calculus is identified.
- The applicable rules, criteria, or procedures are stated.
- If the calculus is informal, its operative standards are made explicit.

---

### 5. Initial Reasoning State Recorded

- The initial reasoning state or reasoning state representation is recorded.
- Its relationship to the investigation is clear.

---

### 6. Reasoning Activity Recorded

- Reasoning transformations are recorded.
- Transition signatures or equivalent trace artifacts are present.
- Candidate generation is recorded as part of reasoning where candidates arise.

---

### 7. Admissibility Structure Materialized When Required

- Candidate admissibility is classified when relevant.
- Ω records classifications and provenance produced by the applicable calculus.
- Ω is not treated as the source or cause of admissibility criteria or consequences.
- If no candidates exist, Ω is marked empty or not applicable with an explicit reason.

---

### 8. Resolution Rule Applied When Applicable

- The resolution rule is identified when a resolution is attempted.
- The resolution execution is distinguishable from the rule.
- If no resolution rule is applicable, the reason is recorded.

---

### 9. Resolution, Evidence Closure, or Closure Status Recorded

- The claim-level logical disposition is explicitly recorded when one is produced.
- The claim-level logical disposition is distinguishable from Ω, the resolution rule, the resolution execution, and the investigation closure status.
- If `Resolved` or `Provisionally resolved` closure is claimed, EC-01 through EC-11 are individually traceable to evidence or an allowed applicability determination.
- The evidence/search classes, denominator/directness checks, measurement/classification limits, strongest support, strongest counterevidence, alternative explanations, surviving narrower propositions, residual uncertainty, terminal bounded saturation pass, and methodology audit are preserved.
- If no resolution is produced, the closure status is recorded.
- When intake produced multiple frozen contracts, the record preserves all per-contract outcomes and the deterministic cross-contract aggregate.
- Any unresolved frozen assumption that constrains the terminal result remains explicit.

---

### 10. Revision Records Preserved

If the investigation revisits an earlier stage, the record identifies:

- the stage revisited;
- the reason for revision;
- the artifact changed;
- the effect on later stages.

Any revision to frozen intake content records the invalidation of the prior freeze and downstream evaluations.

Any terminal evidence-closure pass that discovers a new material item records which search/reasoning work was reopened and whether the earlier atomic disposition remains valid.

---

### 11. Reconstructibility Preserved

- The investigation record contains enough information for another investigator to reconstruct the reasoning process.
- Missing artifacts are explicitly identified.
- Limitations and unresolved issues are recorded.
- For a closed investigation, another investigator can reconstruct why the bounded search stopped without treating the stopping rule itself as proof of open-world completeness.

---

## Closure Statuses

A FAR investigation may close with one of the following statuses.

### Resolved

A resolution has been recorded under the stated resolution rule and `FAR-EVIDENCE-CLOSURE-1.0` has passed.

---

### Provisionally Resolved

A resolution has been recorded and `FAR-EVIDENCE-CLOSURE-1.0` has passed, but explicit limitations, uncertainty, or unresolved issues remain that constrain interpretation or generalization.

---

### Unresolved

No resolution is currently available under the stated methodology.

---

### Suspended

The investigation is paused pending additional representations, interpretations, criteria, evidence, reasoning, or closure-gate work.

---

### Incomplete

Required methodological artifacts or closure-gate obligations are missing.

---

### Invalid

The investigation cannot be reconstructed or violates core FAR methodology.

---

## Edge-Case Handling

### Decisive Atomic Verdict Before Evidence Closure

Record the atomic verdict at the moment its support or refutation condition is satisfied. Continue the bounded closure work required by `FAR-EVIDENCE-CLOSURE-1.0`.

If that work cannot be completed, preserve the atomic verdict and use a non-closure investigation status. Do not weaken the atomic verdict merely because closure remains incomplete, and do not upgrade the investigation to `Resolved` merely because the atomic verdict is decisive.

---

### No Admissible Candidates

If no candidates are admissible, the investigation may close as unresolved, suspended, or incomplete depending on the cause.

The cause must be recorded.

---

### Multiple Admissible Candidates

If multiple candidates are admissible, the resolution rule must specify how they are selected, ranked, combined, preserved, or left unresolved.

---

### Changing Interpretations

If interpretation changes during the investigation, the change must be recorded with its effect on later stages.

If the changed interpretation was part of a frozen intake, the intake must be refrozen and dependent evaluations rerun.

---

### Changing Reasoning Calculi

If the reasoning calculus changes, the investigation record must identify the change, justify the change, and record which stages are affected.

---

### Open-Ended Investigations

Open-ended investigations may close as suspended or provisionally resolved only under the rules above.

They should not be recorded as resolved unless a resolution rule has actually produced a resolution and the evidence-closure gate has passed.

---

### Conflicting Resolutions

If conflicting resolutions are produced, the conflict must be recorded and either resolved by a stated rule or preserved as unresolved.

When the conflict is produced solely by different frozen contract interpretations, preserve it as contract sensitivity unless a pre-evaluation rule already licenses another aggregate.

---

## Validation Outcomes

A FAR investigation may be classified as:

### Valid

All required methodological artifacts are present or explicitly marked not applicable, and any claimed `Resolved` or `Provisionally resolved` closure satisfies `FAR-EVIDENCE-CLOSURE-1.0`.

---

### Provisionally Valid

The investigation is mostly reconstructible, but minor artifacts require clarification. This label does not waive a missing evidence-closure gate for a claimed closed investigation.

---

### Incomplete

Required methodological artifacts are missing.

---

### Invalid

The investigation cannot be reconstructed or violates core FAR methodology.

---

## Boundary With FARO

This document defines methodological validation requirements.

FARO may later define operational procedures for applying, automating, comparing, or reporting these checks.

FARO shall not replace these validation requirements with independent criteria.

---

## Notes

Validation is structural and methodological.

It does not assert truth, correctness, soundness, or open-world completeness of the investigation's resolution.
