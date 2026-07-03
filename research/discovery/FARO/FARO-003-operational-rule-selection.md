# FARO Discovery Investigation

## Identifier

FARO-003

---

# Title

Operational Rule Selection

---

## Status

In Progress

---

# Purpose

Determine whether FARA logically specifies how reasoning rules are selected during an investigation.

---

# Central Question

Does the current definition of FARA entail a procedure for selecting reasoning rules?

---

# Dependencies

- FARO-001 — Operational Necessity of FARO
- FARO-002 — Inferential Evaluation

---

# Background

FARA defines representations, interpretations, investigations, reasoning calculi, and related architectural concepts.

This investigation asks whether those definitions alone determine which reasoning rules are applied during reasoning.

---

# Test Case 001

Suppose an investigation contains the following argument.

Premise 1:

> If A then B.

Premise 2:

> A.

Conclusion:

> B.

---

# Step 1 — Representation

Question:

Can FARA represent the premises and conclusion?

Result:

Yes.

---

# Step 2 — Investigation

Question:

Can FARA represent that the argument belongs to a particular investigation?

Result:

Yes.

---

# Step 3 — Rule Selection

Question:

Does FARA determine that Modus Ponens is the rule that should be applied?

Result:

Undetermined.

Current definitions identify the existence of a reasoning calculus but do not specify how a calculus is selected or invoked.

---

# Observation

The architecture distinguishes the existence of reasoning rules from the execution of those rules.

No operational procedure has yet been identified.

---

# Missing Capability 003

Selection of an appropriate reasoning calculus for a given reasoning step.

Status:

Unresolved.

---

# Competing Hypotheses

## H1

Rule selection follows directly from the architectural definitions of FARA.

## H2

Rule selection requires an operational procedure outside the architectural definitions.

---

# Decision Criteria

If the current definitions of FARA do not uniquely determine rule selection, then rule selection is an operational responsibility rather than an architectural one.

---

# Current Conclusion

No conclusion has been reached.

Additional investigations are required.