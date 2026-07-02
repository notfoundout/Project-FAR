# GP-007A — Investigation Split Artifact Test

## Status

Active Grounding Test

## Parent Investigation

`GP-007-investigation.md`

## Test Objective

Test whether the GP-007 investigation split improves analysis of existing discovery artifacts without adding unnecessary complexity.

The split under test is:

```text
Investigation Process ≠ Investigation Record ≠ Investigation Target ≠ Investigation Outcome
```

## Artifact Families Tested

- FI artifacts
- GP artifacts
- AA artifacts
- CP artifacts
- DGA artifacts

This test does not revise canonical definitions.

---

# Test 1 — FI Artifacts

FI artifacts are foundational investigations.

## Split Application

An FI file is not the investigation itself.

It is the repository record of an investigation process.

The investigation target may be a question, relation, concept, or methodological defect.

The outcome may be unresolved, split, reduced, provisionally stable, or reopened.

## Result

The split improves precision.

It prevents treating an FI document as though it were identical to the inquiry it records.

---

# Test 2 — GP Artifacts

GP artifacts are grounding investigations.

## Split Application

A GP file records an active grounding process.

Its target is usually a concept.

Its outcome is not necessarily a definition.

Possible outcomes include:

- rejected;
- reduced;
- split;
- merged;
- residual candidate;
- downstream test required.

## Result

The split improves precision.

It prevents the project from assuming that every grounding pass must produce a canonical rewrite.

---

# Test 3 — AA Artifacts

AA artifacts are artifact audits.

## Split Application

An AA file is an investigation record whose target is a repository artifact.

Its method is audit.

Its outcome is a set of findings and recommendations, not a direct revision.

## Result

The split is useful.

It preserves the distinction between evaluation and repository action.

---

# Test 4 — CP Artifacts

CP artifacts are compression investigations.

## Split Application

A CP artifact targets methodological, conceptual, or repository redundancy.

Its outcome may be deletion, derivation, merger, replacement, or retention.

A CP artifact is therefore not simply a theory artifact.

It is an investigation record concerning minimization of independent commitments.

## Result

The split improves classification.

It prevents compression work from being confused with ordinary theory development.

---

# Test 5 — DGA Artifacts

DGA artifacts are dependency graph audits.

## Split Application

A DGA file records an investigation into dependencies among artifacts or concepts.

Its target is a dependency graph or dependency hypothesis.

Its outcome is graph confirmation, revision, split, or rejection.

## Result

The split improves precision.

It prevents dependency graphs from being treated as canonical theory merely because they are documented.

---

# Consolidated Result

The GP-007 investigation split survived its first artifact-family test.

It improved analysis across FI, GP, AA, CP, and DGA artifacts.

The split clarified that:

- a repository file is a record, not the investigation itself;
- a target is not always an object;
- an outcome is not always a definition or theorem;
- an audit evaluates but does not directly revise;
- an investigation may produce negative, partial, or structural results.

## Current Status of Investigation

`Investigation` should remain ungrounded until the following are investigated:

- investigation question;
- investigation target;
- investigation method;
- investigation process;
- investigation record;
- investigation outcome;
- investigation state;
- reopening conditions.

## Methodology Result

The split is useful.

It exposed real artifact-role conflations without requiring expansion of the repository architecture.

This provides evidence that Phase II grounding improves repository precision by distinguishing process, record, target, and outcome.
