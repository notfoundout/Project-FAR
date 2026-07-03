# FARE Discovery Investigation

## Identifier

FARE-025

---

# Title

Robustness

---

## Status

In Progress

---

# Purpose

Determine the necessary and sufficient conditions under which an assessment is robust.

The objective is to establish robustness as a formal assessment property within the Formal Architecture of Reasoning Evaluation.

---

# Motivation

Previous investigations established:

- validity;
- justification;
- admissibility;
- completeness.

An assessment may satisfy all of these while remaining highly sensitive to small changes in its evaluative context.

This investigation examines that distinction.

---

# Central Question

What makes an assessment robust?

---

# Candidate 1

Confidence.

Question

Is robustness identical to confidence?

Evaluation

Confidence reflects belief in an assessment.

Robustness concerns the stability of the assessment under change.

The concepts are distinct.

Result

Rejected.

---

# Candidate 2

Reliability.

Question

Is robustness identical to reliability?

Evaluation

Reliability evaluates repeated execution of an evaluation process.

Robustness evaluates the stability of an assessment when relevant aspects of the evaluation vary.

The concepts are distinct.

Result

Rejected.

---

# Candidate 3

Stability Under Variation.

Question

Is an assessment robust when reasonable variations in evaluative conditions do not materially alter the assessment?

Evaluation

Current evidence supports this hypothesis.

Robustness appears to characterize resilience rather than correctness.

Result

Supported.

---

# Pattern Analysis

Every investigated robust assessment possesses:

- clearly defined evaluation conditions;
- limited sensitivity to reasonable variation;
- stability of the resulting assessment.

Assessments whose outcomes change dramatically under minor relevant variations appear non-robust.

---

# Emerging Hypothesis

Robustness is the property of an assessment that preserves materially equivalent outcomes under reasonable variations in evaluative conditions.

---

# Observation

Robustness depends upon:

- evaluation conditions;
- relevance;
- condition equivalence.

It therefore builds upon previous investigations within FARE.

---

# Consequences

If accepted:

Project FAR distinguishes:

- validity;
- justification;
- admissibility;
- completeness;
- robustness.

Each evaluates a different property of an assessment.

---

# Relationship to Previous Investigations

Assessment

├── Validity

├── Justification

├── Admissibility

├── Completeness

└── Robustness

Robustness evaluates the stability of an assessment under reasonable variation.

---

# Remaining Questions

Future investigations should determine:

- what constitutes a reasonable variation;
- whether robustness admits quantitative measurement;
- whether robustness depends upon evaluation objectives;
- whether robustness contributes directly to confidence.

---

# Current Status

The investigation remains active.

Current evidence supports treating robustness as the stability of an assessment under reasonable evaluative variation.