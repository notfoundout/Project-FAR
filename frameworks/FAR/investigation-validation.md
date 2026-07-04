# FAR Investigation Validation

## Purpose

This document defines the minimum validation checklist for a completed FAR investigation.

It is methodological validation, not FARO auditing.

FARO may later operationalize or automate these checks, but the checks themselves belong to FAR.

---

## Validation Standard

A FAR investigation is methodologically valid only if its required artifacts are explicit enough to support audit, reconstruction, and review.

Validation does not imply that the resolution is true, optimal, final, or uniquely correct.

Validation means the investigation was conducted and recorded according to FAR methodology.

---

## Optional Stage Policy

A workflow stage may be marked `Not applicable` only when the investigation record states why it is not applicable.

No stage shall be silently omitted.

If a stage is skipped without justification, the investigation is incomplete.

---

## Minimum Checklist

A completed FAR investigation should satisfy the following checks.

### 1. Investigation Defined

- The investigation is explicitly identified.
- The objective is stated.
- The relevant conditions or scope are stated.

---

### 2. Representational Structure Specified

- The relevant representations are identified.
- The relations among representations are recorded or explicitly scoped.
- Missing representations are identified if relevant.

---

### 3. Interpretation Specified

- The interpretation assigned to representations is stated.
- Any changes in interpretation are explicitly recorded.

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

### 7. Admissibility Structure Constructed When Required

- Candidate admissibility is classified when relevant.
- Ω records admissibility classifications.
- Ω is not treated as the source of admissibility criteria.
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

---

### 10. Revision Records Preserved

If the investigation revisits an earlier stage, the record identifies:

- the stage revisited;
- the reason for revision;
- the artifact changed;
- the effect on later stages.

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
