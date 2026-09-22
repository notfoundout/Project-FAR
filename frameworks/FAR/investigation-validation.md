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

## Post-Evidence Closure Validation

Logical disposition and investigation closure are separate validation targets. A proof, counterexample, supported result, or other decisive atomic outcome may settle the frozen proposition without satisfying the conditions for a fully `Resolved` investigation.

Any investigation claiming `Resolved` must satisfy the [FAR Post-Evidence Closure Protocol v1.0](../../methodology/post-evidence-closure-protocol.md) and record all of the following:

- the exact logical disposition and evidence licensing it;
- a bounded search frame with scope, searched sources/spaces, stopping rule, and evidence cutoff;
- coverage of direct/primary evidence;
- coverage of strongest opposing/disconfirming evidence;
- coverage of measurement, classification, source-quality, or data-quality limits;
- denominator/base-rate/directness/construct-alignment analysis when applicable, or an explicit reason it is not applicable;
- material alternative explanations or rival hypotheses;
- narrower propositions that survive the atomic disposition;
- residual uncertainty;
- evidence that materially plausible interpretations and alternatives were tested; and
- a terminal saturation pass over the declared search frame that yielded zero new material findings.

Every mandatory evidence class must be either `covered` with traceable evidence or `not_applicable` with a reason. Empty findings inventories require an explicit basis for the none-found result. Labels such as `complete`, `checked`, `exhaustive`, `saturated`, or `none found` do not certify themselves.

If the terminal pass finds a new material source, interpretation, alternative, limitation, or surviving proposition, the investigation is not closure-complete. The finding must be incorporated and the closure analysis repeated before another terminal pass.

`Provisionally resolved` is valid when a defensible logical disposition exists but one or more closure dimensions remain incomplete, constrained, or unsaturated. The unfinished dimensions must be explicit. `Provisionally resolved` must not be used as evidence of full closure and does not satisfy a machine execution `PASS` governed by the closure protocol.

Passing this gate establishes bounded procedural saturation only. It does not establish open-world completeness, factual truth, external independence, or that no future evidence exists.

## Validation Standard

A FAR investigation is methodologically valid only if its required artifacts are explicit enough to support audit, reconstruction, and review.

Validation does not imply that the resolution is true, optimal, final, or uniquely correct.

Validation means the investigation was conducted and recorded according to FAR methodology.

---

## Optional Stage Policy

A workflow stage or post-evidence evidence class may be marked `Not applicable` only when the investigation record states why it is not applicable.

No required stage or closure obligation shall be silently omitted.

If a required stage or closure obligation is skipped without justification, the investigation is incomplete.

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

### 9. Resolution or Logical Disposition Recorded

- The resolution or atomic logical disposition is explicitly recorded when one is produced.
- The disposition is distinguishable from Ω, the resolution rule, resolution execution, and full investigation closure.
- If no resolution is produced, the closure status is recorded.
- When intake produced multiple frozen contracts, the record preserves all per-contract outcomes and the deterministic cross-contract aggregate.
- Any unresolved frozen assumption that constrains the terminal result remains explicit.

---

### 10. Post-Evidence Closure Recorded When `Resolved`

- The logical disposition carries evidence.
- The bounded search frame and stopping rule are explicit.
- Every mandatory evidence class is covered or explicitly not applicable with a reason.
- Strongest opposing evidence and material alternatives are recorded.
- Measurement/classification limits and applicable denominator/directness/construct issues are recorded.
- Surviving narrower propositions and residual uncertainty are recorded.
- Interpretive closure has evidence.
- The terminal saturation pass is evidenced and records zero new material findings.

A decisive Stage 9 result without these checks is not enough for `Resolved`.

---

### 11. Revision Records Preserved

If the investigation revisits an earlier stage, the record identifies:

- the stage revisited;
- the reason for revision;
- the artifact changed;
- the effect on later stages.

Any revision to frozen intake content records the invalidation of the prior freeze and downstream evaluations. Any new material finding during terminal saturation invalidates full closure until incorporated and rechecked.

---

### 12. Reconstructibility Preserved

- The investigation record contains enough information for another investigator to reconstruct the reasoning process.
- Missing artifacts are explicitly identified.
- Limitations and unresolved issues are recorded.

---

## Closure Statuses

A FAR investigation may close with one of the following statuses.

### Resolved

A logical disposition has been recorded under the stated resolution rule and the mandatory post-evidence closure gate has passed, including a zero-new-material-finding terminal saturation pass.

---

### Provisionally Resolved

A defensible logical disposition has been recorded, but one or more post-evidence closure dimensions remain incomplete, constrained, or unsaturated. Those dimensions must be named explicitly.

---

### Unresolved

No resolution is currently available under the stated methodology.

---

### Suspended

The investigation is paused pending additional representations, interpretations, criteria, evidence, or reasoning.

---

### Incomplete

Required methodological artifacts or closure obligations are missing.

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

They should not be recorded as resolved unless both a resolution rule has produced a disposition and the post-evidence closure gate has passed.

---

### Conflicting Resolutions

If conflicting resolutions are produced, the conflict must be recorded and either resolved by a stated rule or preserved as unresolved.

When the conflict is produced solely by different frozen contract interpretations, preserve it as contract sensitivity unless a pre-evaluation rule already licenses another aggregate.

---

## Validation Outcomes

A FAR investigation may be classified as:

### Valid

All required methodological artifacts and applicable closure obligations are present or explicitly marked not applicable with reasons.

---

### Provisionally Valid

The investigation is mostly reconstructible, but minor artifacts require clarification.

---

### Incomplete

Required methodological artifacts or closure obligations are missing.

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

It does not assert truth, correctness, soundness, open-world completeness, or finality of the investigation's resolution.
