# FAR Example Standard

## Purpose

This document defines the minimum structure required for a canonical FAR example.

Examples illustrate FAR methodology.

Examples do not introduce definitions, alter workflow stages, or prove mathematical claims.

---

## Standard

A canonical FAR example shall be structured enough for another investigator to reconstruct the investigation.

The example may be brief or extensive, but it must preserve the required methodological artifacts.

---

## Required Sections

Every canonical FAR example should include the following sections unless a section is explicitly marked not applicable.

### 1. Investigation

Identify the investigation and its objective.

The investigation should state what is being examined and under what conditions.

---

### 2. Representational Structure

Identify the representations used in the investigation and the relevant relations among them.

---

### 3. Interpretation

Specify the interpretation assigned to the representations.

If interpretation changes during the investigation, the change should be recorded explicitly.

---

### 4. Reasoning Calculus

Identify the reasoning calculus or rule system governing the investigation.

If the reasoning calculus is informal, the example must still state the operative rules or criteria.

---

### 5. Initial Reasoning State

Record the initial reasoning state or its representation.

---

### 6. Reasoning and Candidate Generation

Record reasoning activity through explicit transformations, transition signatures, or equivalent trace artifacts.

Candidate generation is treated as part of this stage.

Candidates generated during reasoning should be identified before admissibility classification.

---

### 7. Admissibility Structure (Ω)

Construct Ω when the investigation involves candidate admissibility or selection.

Ω should record admissibility classifications rather than determine them.

If Ω is not applicable, explain why.

---

### 8. Resolution Rule

Identify the rule used to select the resolution from admissible candidates.

If no resolution rule is applicable, explain why.

---

### 9. Resolution or Closure Status

Record the resolution produced by the investigation.

The resolution should be distinguishable from the rule and execution that produced it.

If no resolution is produced, record the closure status.

Allowed closure statuses include:

- `Resolved`;
- `Provisionally resolved`;
- `Unresolved`;
- `Suspended`;
- `Incomplete`;
- `Invalid`.

---

### 10. Revision Records

If the investigation revisits any earlier stage, record:

- the stage revisited;
- the reason for revision;
- the artifact changed;
- the effect on later stages.

---

### 11. Audit Notes

Record any limitations, assumptions, unresolved issues, missing artifacts, or reproducibility concerns.

---

## Optional Stage Rule

A section may be marked `Not applicable` only when the example states why it is not applicable.

No required section should be silently omitted.

---

## Candidate Generation Rule

Candidate generation is not a separate universal workflow stage.

It belongs within Stage 6 — Perform Reasoning.

Stage 7 classifies candidates through the Admissibility Structure (Ω).

This preserves the generality of FAR across investigations where candidates emerge continuously rather than in a discrete phase.

---

## Edge-Case Requirements

Examples involving edge cases should explicitly record the relevant condition.

This includes:

- no admissible candidates;
- multiple admissible candidates;
- changing interpretations;
- changing reasoning calculi;
- unresolved investigations;
- suspended investigations;
- incomplete records;
- conflicting resolutions.

---

## Prohibited Example Behavior

Examples shall not:

- introduce new primitives;
- redefine FAR workflow stages;
- redefine FARA architectural concepts;
- treat narrative explanation as a substitute for required methodological artifacts;
- collapse reasoning records into the reasoning objects recorded;
- use FARO-style operational evaluation before FARO is formally developed.

---

## Notes

Examples may motivate future revisions, but revisions must occur through the canonical definition, methodology, or audit process.
