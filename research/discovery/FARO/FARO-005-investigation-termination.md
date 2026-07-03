# FARO Discovery Investigation

## Identifier

FARO-005

---

# Title

Investigation Termination

---

## Status

In Progress

---

# Purpose

Determine whether the current definition of FARA logically specifies when an investigation should terminate.

---

# Central Question

Does FARA determine when reasoning has reached completion?

---

# Dependencies

- FARO-001 — Operational Necessity of FARO
- FARO-002 — Inferential Evaluation
- FARO-003 — Operational Rule Selection
- FARO-004 — Investigation Control

---

# Background

FARA defines investigations, reasoning states, transitions, admissibility structures, and resolutions.

This investigation asks whether those definitions alone determine when an investigation should end.

---

# Test Case

Consider an investigation with three admissible candidate conclusions.

Additional evidence could continue to be collected indefinitely.

---

# Step 1 — Representation

Question:

Can FARA represent the investigation?

Result:

Yes.

---

# Step 2 — Candidate Resolutions

Question:

Can FARA represent multiple admissible candidate resolutions?

Result:

Yes.

---

# Step 3 — Continuation

Question:

Can FARA represent additional reasoning after an admissible resolution has been identified?

Result:

Yes.

---

# Step 4 — Termination Decision

Question:

Do the current definitions of FARA determine whether reasoning should terminate or continue?

Result:

Undetermined.

The architecture specifies the existence of investigations and resolutions.

It does not specify an operational criterion for terminating reasoning.

---

# Observation

Representing a resolution is not equivalent to deciding that reasoning is complete.

Termination appears to require an operational decision rather than an architectural definition.

---

# Missing Capability 005

A formal termination criterion governing the completion of investigations.

Status:

Unresolved.

---

# Competing Hypotheses

## H1

Investigation termination follows directly from the architectural definitions of FARA.

## H2

Investigation termination requires an operational procedure beyond the architectural definitions.

---

# Decision Criteria

If FARA does not uniquely determine when an investigation terminates, termination is an operational responsibility rather than an architectural one.

---

# Current Conclusion

No conclusion has been reached.

Additional investigations are required.

---

# Emerging Pattern

The previous investigations have identified unresolved questions concerning:

- inferential evaluation;
- reasoning rule selection;
- investigation control;
- investigation termination.

Each unresolved question concerns the execution of reasoning rather than the representation of reasoning.

This pattern will be evaluated after additional investigations to determine whether it justifies a distinct operational framework.