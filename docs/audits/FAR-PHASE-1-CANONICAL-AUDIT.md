# FAR Phase 1 — Canonical Audit

## Status

Initial audit complete.

---

## Scope

This audit reviews the canonical FAR documents currently listed in the canonical map:

- `frameworks/FAR/README.md`
- `frameworks/FAR/methodology.md`
- `frameworks/FAR/workflow.md`
- `frameworks/FAR/application.md`

It evaluates whether FAR currently satisfies the Phase 1 canonical requirements:

1. every technical term is canonically defined or explicitly delegated;
2. every FAR concept has a single responsibility;
3. FAR does not redefine FARA or repository-wide terminology;
4. FAR has no obvious circular definitions;
5. FAR has a clear dependency relation to FARA;
6. FAR is ready to be stabilized before FARO development.

---

## Canonical Sources Reviewed

### Repository-wide Definitions

Canonical terminology is maintained in:

`theory/definitions/definitions.md`

This file defines the major terms used by FAR, including:

- investigation;
- representation;
- representational structure;
- interpretation;
- reasoning calculus;
- reasoning state;
- transition signature;
- candidate;
- admissibility;
- admissibility structure;
- resolution rule;
- resolution execution;
- resolution.

### FARA Architecture

FAR depends on FARA for the architecture of structured reasoning.

Relevant FARA documents include:

- `frameworks/FARA/architecture.md`
- `frameworks/FARA/dependency-graph.md`

FARA currently states that it specifies what exists architecturally, while FARO should specify operations performed over that architecture.

FAR should therefore remain methodological rather than architectural or operational.

### FAR Documents

The FAR directory currently contains:

- `README.md`
- `methodology.md`
- `workflow.md`
- `application.md`

---

## Findings

### Finding 1 — FAR is currently methodology-scoped

FAR is consistently described as methodology rather than architecture.

`frameworks/FAR/README.md` states that FAR defines the methodology of the Foundational Analysis of Reasoning and explains how FARA is applied during investigations.

`frameworks/FAR/methodology.md` repeats this relation by stating that FAR provides a structured process for conducting investigations within the architecture established by FARA.

Assessment: pass.

No major conceptual conflict is present here.

---

### Finding 2 — FAR depends correctly on FARA

FAR repeatedly states that it depends on FARA and does not modify it.

This is consistent with FARA's own separation between architecture and downstream application.

Assessment: pass.

FAR should preserve this dependency direction:

```text
FARA -> FAR -> FARO
```

FAR should not define new primitives or alter FARA's architectural categories.

---

### Finding 3 — The workflow duplicates the methodology list

`methodology.md` lists the nine stages of a FAR investigation.

`workflow.md` defines the same nine stages in greater detail.

`application.md` repeats the same nine stages again.

Assessment: revision needed.

This is not a logical contradiction, but it creates maintenance risk. If a stage changes in one document, the other documents can drift.

Recommended correction:

- `workflow.md` should be the canonical source for the FAR stage sequence.
- `methodology.md` should describe methodological principles and point to `workflow.md` for the stage list.
- `application.md` should avoid repeating the full stage list unless explicitly marked as a non-canonical summary.

---

### Finding 4 — FAR has no dedicated canonical dependency graph

FARA has a dependency graph.

FARE mathematics now has a proof policy and theorem index.

FAR does not yet have an equivalent dependency maintenance artifact.

Assessment: gap.

Recommended addition:

`frameworks/FAR/dependency-graph.md`

This file should specify:

```text
theory/definitions/definitions.md
  -> frameworks/FARA/
  -> frameworks/FAR/workflow.md
  -> frameworks/FAR/methodology.md
  -> frameworks/FAR/application.md
```

The exact ordering may be revised, but FAR needs an explicit maintenance artifact to prevent circularity and document drift.

---

### Finding 5 — FAR has no design-principles document

FARA has a design-principles document.

FAR does not currently have a FAR-specific equivalent.

Assessment: gap.

Recommended addition:

`frameworks/FAR/design-principles.md`

Minimum principles:

- FAR is methodological, not architectural.
- FAR applies FARA without redefining FARA.
- FAR remains reasoning-calculus neutral.
- FAR workflow stages are procedural roles, not new primitives.
- FAR records reasoning activity without collapsing records into the reasoning objects recorded.
- FARO should operationalize FAR only after FAR is stable.

---

### Finding 6 — The term “transition signature” is used correctly but should be explicitly delegated

FAR uses transition signatures in the methodology and workflow.

Transition signatures are canonically defined outside FAR.

Assessment: minor revision needed.

Recommended correction:

Add an explicit note in FAR methodology or README:

> Transition signatures are defined by FARA and used by FAR as documentation artifacts during a reasoning process. FAR does not redefine transition signatures.

---

### Finding 7 — The term “Admissibility Structure (Ω)” is used correctly but should be explicitly delegated

FAR uses the Admissibility Structure in its workflow.

The canonical definition is outside FAR.

Assessment: minor revision needed.

Recommended correction:

Add an explicit delegation note:

> The Admissibility Structure (Ω) is defined by FARA. FAR specifies when it is constructed during an investigation, not what it is architecturally.

---

### Finding 8 — FAR has no explicit freeze target

The project status document now says the next milestone is FAR v1.0 Stable.

The FAR directory itself does not yet define what it must satisfy to reach that milestone.

Assessment: gap.

Recommended addition:

`frameworks/FAR/FAR-v1.0-criteria.md`

Minimum criteria:

- canonical workflow source identified;
- no duplicated stage definitions;
- all technical terms delegated to canonical definitions or FARA;
- dependency graph added;
- methodology, workflow, and application documents synchronized;
- no FAR document introduces new primitives;
- FARO dependency boundary stated.

---

## Term Audit

| Term | Used in FAR | Canonical Source | Status |
|---|---:|---|---|
| Investigation | Yes | `theory/definitions/definitions.md` | Defined |
| Representational Structure | Yes | `theory/definitions/definitions.md` | Defined |
| Interpretation | Yes | `theory/definitions/definitions.md` | Defined |
| Reasoning Calculus | Yes | `theory/definitions/definitions.md` | Defined |
| Reasoning State | Yes | `theory/definitions/definitions.md` | Defined |
| Transition Signature | Yes | `theory/definitions/definitions.md`; FARA transition document | Defined, delegation should be explicit |
| Admissibility Structure (Ω) | Yes | `theory/definitions/definitions.md`; FARA admissibility document | Defined, delegation should be explicit |
| Resolution Rule | Yes | `theory/definitions/definitions.md` | Defined |
| Resolution | Yes | `theory/definitions/definitions.md` | Defined |
| Application | Yes | FAR document role | Acceptable as document title, not a new technical primitive |
| Workflow | Yes | FAR document role | Needs canonical status as stage-source |
| Methodology | Yes | FAR document role | Needs separation from workflow list |

---

## Structural Assessment

### Strengths

- FAR's role is clear: methodology for applying FARA.
- FAR remains reasoning-calculus neutral.
- FAR does not obviously redefine major FARA concepts.
- FAR's three documents are short and repairable.
- Workflow stages are coherent and align with repository-wide definitions.

### Weaknesses

- Stage list is duplicated across three documents.
- FAR lacks its own dependency graph.
- FAR lacks its own design principles.
- FAR lacks explicit v1.0 completion criteria.
- FAR uses FARA concepts without always explicitly delegating their definitions.

---

## Required Changes Before FAR v1.0 Stable

1. Add `frameworks/FAR/dependency-graph.md`.
2. Add `frameworks/FAR/design-principles.md`.
3. Add `frameworks/FAR/FAR-v1.0-criteria.md`.
4. Make `workflow.md` the canonical source for FAR stages.
5. Revise `methodology.md` so it does not duplicate the full stage definitions unnecessarily.
6. Revise `application.md` so it references workflow rather than maintaining an independent stage list.
7. Add explicit delegation notes for transition signatures and Ω.
8. Update `frameworks/FAR/README.md` to include the new maintenance documents.

---

## Verdict

FAR is structurally coherent but not yet stable.

The current material is suitable as a draft methodology layer, but it should not be declared FAR v1.0 Stable until the duplication and dependency-maintenance gaps are corrected.

The next action should be a focused FAR cleanup PR implementing the required changes above.
