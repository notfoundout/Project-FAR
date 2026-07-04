# FAR

**Foundational Analysis of Reasoning**

---

## Purpose

This directory defines the methodology of the Foundational Analysis of Reasoning (FAR).

FAR provides a structured methodology for conducting investigations within the architectural framework established by the Foundational Architecture of Reasoning Analysis (FARA).

Unlike FARA, which defines the architecture of structured reasoning, FAR defines how that architecture is applied during an investigation.

FAR does not introduce new primitives.

---

## Current Status

FAR is undergoing Phase 2 structural stabilization.

The active objective is FAR v1.0 Stable.

FARO development should begin only after FAR reaches comparable stability.

---

## Canonical Source Rule

`workflow.md` is the canonical source for the ordered stages of a FAR investigation.

`methodology.md` describes the methodological principles governing that workflow.

`application.md` describes how the methodology is applied across domains.

---

## Candidate Generation Placement

Candidate generation is part of Stage 6 — Perform Reasoning.

Candidate admissibility classification occurs in Stage 7 through the Admissibility Structure (Ω).

Candidate generation is not a separate universal FAR workflow stage.

---

## Delegation to FARA

FAR uses architectural concepts defined by FARA, including:

- reasoning states;
- transition signatures;
- the Admissibility Structure (Ω);
- resolution rules;
- resolution executions;
- resolutions.

FAR specifies when and how these concepts are used during an investigation.

FAR does not redefine them.

---

## Contents

- `workflow.md` — Canonical source for the stages of a FAR investigation.
- `methodology.md` — Defines the principles governing FAR investigation practice.
- `application.md` — Describes how FAR is applied across domains.
- `dependency-graph.md` — Records FAR document and concept dependency order.
- `design-principles.md` — Records governing design principles for FAR.
- `faro-boundary.md` — Defines the boundary between FAR and future FARO.
- `example-standard.md` — Defines the required structure for canonical FAR examples.
- `investigation-validation.md` — Defines methodological validation checks for completed FAR investigations.
- `FAR-v1.0-criteria.md` — Defines the criteria required before FAR v1.0 Stable.

---

## Related Directories

- `frameworks/FARA/` — Foundational architecture.
- `frameworks/FARO/` — Future operational layer, downstream of stable FAR.
- `theory/` — Formal definitions, axioms, propositions, conjectures, theorems, and proofs.
- `examples/` — Complete worked investigations.
