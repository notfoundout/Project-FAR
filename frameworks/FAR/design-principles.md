# FAR Design Principles

## Purpose

This document records the design principles governing the Foundational Analysis of Reasoning (FAR).

It is a maintenance artifact.

It does not introduce new definitions.

---

## Principle 1 — FAR Is Methodological

FAR defines how the architecture of reasoning is applied during an investigation.

FAR does not define the architecture itself.

Architectural concepts are supplied by FARA and canonical repository-wide definitions.

---

## Principle 2 — FAR Applies FARA Without Redefining It

FAR depends on FARA for architectural objects and distinctions.

FAR may specify when and how those objects are used during an investigation.

FAR shall not alter their definitions.

---

## Principle 3 — FAR Is Reasoning-Calculus Neutral

FAR does not prescribe a single reasoning calculus.

Different investigations may use different calculi, provided the chosen calculus is explicitly specified.

---

## Principle 4 — Workflow Stages Are Procedural Roles

FAR workflow stages organize investigation activity.

They are not new primitives.

They should be understood as methodological roles performed during an investigation.

---

## Principle 5 — Records Are Distinct From What They Record

FAR shall preserve the distinction between:

- an investigation and an investigation record;
- a reasoning state and a reasoning state representation;
- a reasoning process and a reasoning trace;
- a transition and a transition signature;
- a resolution execution and a resolution.

This prevents documentation artifacts from being confused with the reasoning objects or activities they record.

---

## Principle 6 — Explicit Delegation Prevents Drift

When FAR uses a concept defined outside FAR, it should explicitly delegate to the canonical source.

This applies especially to:

- transition signatures;
- the Admissibility Structure (Ω);
- reasoning states;
- resolution rules;
- resolutions.

---

## Principle 7 — Workflow Is Canonical for Stage Order

`workflow.md` is the canonical source for the FAR investigation stage sequence.

Other FAR documents may summarize the stages, but they shall not maintain independent competing stage definitions.

---

## Principle 8 — FARO Follows FAR Stability

FARO should operationalize FAR after FAR reaches sufficient stability.

FARO should not redefine FAR primitives, alter FAR methodology, or become a substitute for FAR.

---

## Principle 9 — Iteration Is Permitted

The FAR workflow is ordered but not strictly linear.

An investigation may revisit earlier stages when new representations, revised interpretations, modified criteria, or additional reasoning require further analysis.

---

## Principle 10 — Methodological Claims Remain Auditable

Every FAR methodological claim should be traceable to:

- a canonical definition;
- a FARA architectural component;
- the FAR workflow;
- a documented design principle;
- or an explicit audit finding.

Unsupported methodological expansion should remain provisional until reviewed.
