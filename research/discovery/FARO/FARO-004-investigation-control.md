# FARO Discovery Investigation

## Identifier

FARO-004

---

# Title

Investigation Control

---

## Status

In Progress

---

# Purpose

Determine whether the current definition of FARA specifies how an investigation progresses from one reasoning state to the next.

---

# Central Question

Does FARA determine how reasoning proceeds through an investigation?

---

# Dependencies

- FARO-001 — Operational Necessity of FARO
- FARO-002 — Inferential Evaluation
- FARO-003 — Operational Rule Selection

---

# Background

FARA defines investigations and reasoning states.

This investigation asks whether those definitions determine how an investigation advances.

---

# Test Case

Suppose an investigation begins with two representations.

R₁

R₂

Several reasoning operations are available.

Examples include:

- infer a new representation;
- reject a representation;
- request additional evidence;
- revise an interpretation;
- terminate the investigation.

---

# Step 1 — Initial State

Question:

Can FARA represent the initial reasoning state?

Result:

Yes.

---

# Step 2 — Available Operations

Question:

Can FARA represent possible reasoning operations?

Result:

Yes.

---

# Step 3 — Operational Choice

Question:

Does FARA determine which operation should be executed next?

Result:

Undetermined.

The current architecture identifies reasoning states but does not specify an operational policy governing transitions between them.

---

# Observation

Representing possible transitions is not equivalent to selecting one transition.

The distinction between possibility and execution appears to be architectural.

---

# Missing Capability 004

Operational control of investigation progression.

Status:

Unresolved.

---

# Competing Hypotheses

## H1

Investigation control is logically determined by FARA.

## H2

Investigation control requires an operational framework built upon FARA.

---

# Decision Criteria

If the current architectural definitions do not uniquely determine progression through an investigation, investigation control belongs outside the architectural layer.

---

# Current Conclusion

No conclusion has been reached.

Further investigations are required.