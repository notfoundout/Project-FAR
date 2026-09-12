# FAR Investigation Validation

## Purpose

This document defines the minimum validation checklist for a completed FAR investigation.

It is methodological validation, not FARO auditing.

FARO may later operationalize or automate these checks, but the checks themselves belong to FAR.

---

## Contract-Discovery Intake Validation

When the supplied input did not already determine every result-relevant comparison parameter, validation begins with the governed intake record.

Require all of the following:

- the record satisfies the published `far-intake/1.0` JSON Schema before semantic validation;
- the exact raw input is preserved and its SHA-256 recomputes;
- materially distinct claim parses and material terms are explicit;
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
- `intake_sha256` binds the exact raw input and discovery object;
- `freeze_sha256` binds the intake hash and exact freeze timestamp;
- no evaluation predates the intake freeze;
- each evaluation binds both the exact frozen candidate contract hash and exact freeze identity;
- each non-`Unknown` evaluation has evidence references, while `Unknown` has an explanation;
- every frozen candidate is evaluated before a cross-contract aggregate is issued;
- any result-relevant frozen `Unknown` assumption blocks invariant terminal promotion;
- the cross-contract aggregate follows the fixed `far-intake/1.0` rule rather than an analyst-selected preferred contract.

A draft, incomplete, invalid, or unresolved-assumption intake cannot support an invariant non-`Unknown` cross-contract verdict.

Passing intake validation establishes bounded procedural conformance only. It does not establish open-world semantic completeness, source truth or authority, independent retrieval of source bytes, or downstream contract adequacy.

## Contract-Relative Validation Gates

Before the existing checklist, validate the following whenever the investigation makes a representation claim:

- claim, domain, quantifiers, evidence cutoff, and nonclaims are frozen;
- the intake gate is either satisfied or explicitly not applicable because the supplied input already determines the governing contract;
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

## Validation Standard

A FAR investigation is methodologically valid only if its required artifacts are explicit enough to support audit, reconstruction, and review.

Validation does not imply that the resolution is true, optimal, final, or uniquely correct.

Validation means the investigation was conducted and recorded according to FAR methodology.

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
- The governed intake record is referenced when the input required contract discovery, or the reason it was not applicable is explicit.

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

### 9. Resolution or Closure Status Recorded

- The resolution is explicitly recorded when one is produced.
- The resolution is distinguishable from Ω, the resolution rule, and the resolution execution.
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

---

### 11. Reconstructibility Preserved

- The investigation record contains enough information for another investigator to reconstruct the reasoning process.
- Missing artifacts are explicitly identified.
- Limitations and unresolved issues are recorded.

---

## Closure Statuses

A FAR investigation may close with one of the following statuses.

### Resolved

A resolution has been recorded under the stated resolution rule.

---

### Provisionally Resolved

A resolution has been recorded, but limitations, uncertainty, or unresolved issues remain.

---

### Unresolved

No resolution is currently available under the stated methodology.

---

### Suspended

The investigation is paused pending additional representations, interpretations, criteria, evidence, or reasoning.

---

### Incomplete

Required methodological artifacts are missing.

---

### Invalid

The investigation cannot be reconstructed or violates core FAR methodology.

---

## Edge-Case Handling

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

Open-ended investigations may close as suspended or provisionally resolved.

They should not be recorded as resolved unless a resolution rule has actually produced a resolution.

---

### Conflicting Resolutions

If conflicting resolutions are produced, the conflict must be recorded and either resolved by a stated rule or preserved as unresolved.

When the conflict is produced solely by different frozen contract interpretations, preserve it as contract sensitivity unless a pre-evaluation rule already licenses another aggregate.

---

## Validation Outcomes

A FAR investigation may be classified as:

### Valid

All required methodological artifacts are present or explicitly marked not applicable.

---

### Provisionally Valid

The investigation is mostly reconstructible, but minor artifacts require clarification.

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

It does not assert truth, correctness, soundness, or completeness of the investigation's resolution.
