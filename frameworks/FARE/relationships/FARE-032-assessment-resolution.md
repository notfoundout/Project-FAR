# FARE Discovery Investigation

## Identifier

FARE-032

---

# Title

Assessment Resolution

---

## Status

In Progress

---

# Purpose

Determine the necessary and sufficient conditions under which conflicting assessments may be resolved.

The objective is to establish the formal process governing conflict resolution within the Formal Architecture of Reasoning Evaluation.

---

# Motivation

Previous investigations established:

- dependency;
- support;
- conflict;
- refinement.

Conflict identifies incompatible assessments.

This investigation examines how such conflicts should be resolved.

---

# Central Question

How should conflicting assessments be resolved?

---

# Candidate 1

Majority Acceptance.

Question

Should the assessment supported by the greatest number of assessments be accepted?

Evaluation

The number of supporting assessments does not necessarily determine their quality.

Quantity alone is insufficient.

Result

Rejected.

---

# Candidate 2

Highest Confidence.

Question

Should the assessment possessing the greatest confidence be accepted?

Evaluation

Confidence is itself a derived assessment property.

Using confidence alone risks circular reasoning.

Result

Rejected.

---

# Candidate 3

Comparative Evaluation.

Question

Should conflicting assessments themselves become evaluation objects?

Evaluation

Each assessment may be evaluated according to previously established assessment properties, including:

- validity;
- justification;
- admissibility;
- completeness;
- robustness;
- consistency.

Current evidence supports this approach.

Result

Supported.

---

# Pattern Analysis

Conflict does not determine which assessment should be accepted.

Conflict merely identifies incompatibility.

Resolution requires additional evaluation.

---

# Emerging Hypothesis

Assessment resolution is the evaluation of conflicting assessments according to explicitly specified evaluative criteria in order to determine their subsequent status.

---

# Observation

Resolution does not necessarily produce:

- acceptance;
- rejection.

It may instead produce:

- suspension;
- refinement;
- further investigation;
- decomposition into independent assessments.

---

# Consequences

If accepted:

Assessment conflict becomes operationally useful.

Conflict no longer represents the end of reasoning.

Instead, it becomes an input to further evaluation.

---

# Relationship to Previous Investigations

Assessment Relationships

├── Dependency

├── Support

├── Conflict

├── Refinement

└── Resolution

Resolution governs the treatment of conflicting assessments.

---

# Remaining Questions

Future investigations should determine:

- whether resolution procedures admit formal proof;
- whether multiple resolutions may coexist;
- whether unresolved conflicts possess formal status;
- whether resolution always terminates.

---

# Current Status

The investigation remains active.

Current evidence supports treating assessment resolution as a separate evaluative process applied to conflicting assessments.