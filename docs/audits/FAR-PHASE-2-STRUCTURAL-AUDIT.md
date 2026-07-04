# FAR Phase 2 — Structural Audit

## Status

Initial structural audit complete.

---

## Scope

This audit reviews FAR after the Phase 1 canonical cleanup branch changes.

Reviewed files:

- `frameworks/FAR/README.md`
- `frameworks/FAR/workflow.md`
- `frameworks/FAR/methodology.md`
- `frameworks/FAR/application.md`
- `frameworks/FAR/dependency-graph.md`
- `frameworks/FAR/design-principles.md`
- `frameworks/FAR/FAR-v1.0-criteria.md`
- `docs/CANONICAL_MAP.md`

The audit asks:

1. Is every stage of reasoning represented?
2. Are any responsibilities duplicated?
3. Are there missing interfaces between components?
4. Does FAR remain independent of any particular logic, mathematics, or epistemology?
5. Are FAR, FARA, FARO, and FARE cleanly separated?
6. Is the resulting structure ready for FAR v1.0 final review?

---

## Structural Summary

FAR currently has a clean three-document active structure:

```text
workflow.md      -> canonical procedural stage source
methodology.md   -> principles governing workflow use
application.md   -> domain-facing application guidance
```

Maintenance and governance are handled separately:

```text
dependency-graph.md
 design-principles.md
 FAR-v1.0-criteria.md
```

This separation is structurally sound.

---

## Finding 1 — Core document roles are now properly separated

`workflow.md` is explicitly the canonical source for the FAR stage sequence.

`methodology.md` now states that the canonical ordered stage sequence is maintained in `workflow.md` and no longer maintains an independent stage list.

`application.md` also delegates canonical workflow order to `workflow.md` and states that its requirements summarize but do not replace the workflow.

Assessment: pass.

The previous duplication problem has been mostly corrected.

---

## Finding 2 — FAR remains methodology-scoped

`methodology.md` states that FAR does not define the architecture of reasoning, applies the architecture supplied by FARA, and does not introduce new primitives.

`workflow.md` states that it organizes investigations into stages without prescribing the reasoning calculus used within those stages.

Assessment: pass.

FAR remains a methodology layer rather than an architecture layer.

---

## Finding 3 — FAR and FARA are cleanly separated

The updated FAR documents explicitly delegate architectural concepts to FARA and repository-wide definitions.

The workflow delegates transition signatures and the Admissibility Structure (Ω) to FARA.

The methodology delegates reasoning state, reasoning state representation, transition signature, Ω, resolution rule, resolution execution, and resolution.

Assessment: pass.

This preserves the intended dependency:

```text
FARA -> FAR
```

---

## Finding 4 — FAR and FARO boundary is stated but still underdeveloped

The FAR README says FARO is the future operational layer downstream of stable FAR.

The methodology says FARO should operationalize stable FAR methodology and not redefine workflow stages or introduce replacement primitives.

The application document says FARO should operationalize stable FAR applications after FAR reaches sufficient stability.

Assessment: partial pass.

The boundary is stated, but not yet operationally specified.

This is acceptable before FARO development, but FAR v1.0 should include a short boundary statement identifying what FARO may and may not do.

Recommended addition:

`frameworks/FAR/faro-boundary.md`

or a section in `design-principles.md` with explicit allowed and prohibited FARO roles.

---

## Finding 5 — Stage coverage is complete at the current level of abstraction

The canonical workflow covers:

1. investigation definition;
2. representational structure;
3. interpretation;
4. reasoning calculus;
5. initial reasoning state;
6. reasoning transformations;
7. admissibility structure;
8. resolution rule;
9. resolution record.

Assessment: pass with one caveat.

The workflow represents the major stages of a structured investigation. However, it does not yet explicitly distinguish candidate generation from candidate classification.

Currently candidates appear implicitly at the admissibility stage.

This may be acceptable if candidate generation is treated as part of reasoning, but the choice should be explicit.

Recommended review question:

Should FAR include a distinct stage for candidate generation, or should candidate generation remain part of Stage 6 reasoning?

No change is required yet, but this should be resolved before FAR v1.0 Stable.

---

## Finding 6 — Methodological interfaces are mostly present

FAR now has clear interfaces:

- definitions and FARA supply terminology and architecture;
- workflow supplies procedural sequence;
- methodology supplies principles;
- application supplies domain-facing usage guidance;
- dependency graph supplies maintenance order;
- design principles supply constraints;
- v1.0 criteria supply freeze conditions.

Assessment: pass.

The architecture now has enough maintenance structure to support final stabilization.

---

## Finding 7 — Missing artifact interface for examples

Application points to complete worked investigations in `examples/`, but FAR does not define what counts as a valid FAR example.

Assessment: gap.

Recommended addition before FAR v1.0:

`frameworks/FAR/example-standard.md`

Minimum requirements:

- identify the investigation;
- identify the representational structure;
- identify the interpretation;
- identify the reasoning calculus;
- record reasoning states;
- record transition signatures;
- construct Ω where applicable;
- apply a resolution rule;
- record the resolution;
- preserve auditability.

This would prevent examples from drifting into informal essays.

---

## Finding 8 — Validation interface is missing

FAR says investigations should be auditable and reproducible, but it does not yet define a minimal validation checklist for completed FAR investigations.

Assessment: gap.

Recommended addition before FAR v1.0:

`frameworks/FAR/investigation-validation.md`

Minimum validation checks:

- all stages represented or explicitly marked not applicable;
- every transition signature recorded;
- reasoning calculus specified;
- interpretation specified;
- Ω constructed when candidate admissibility is required;
- resolution rule applied explicitly;
- final resolution recorded;
- enough artifacts exist to reconstruct the investigation.

This is methodological validation, not FARO auditing.

FARO may later operationalize or automate these checks.

---

## Finding 9 — The dependency graph is directionally sound but slightly underspecified

The dependency graph gives this order:

```text
theory/definitions/definitions.md
  -> frameworks/FARA/
  -> frameworks/FAR/workflow.md
  -> frameworks/FAR/methodology.md
  -> frameworks/FAR/application.md
```

Assessment: acceptable but debatable.

There is a structural tension:

- `workflow.md` is the canonical procedural stage source.
- `methodology.md` defines principles governing workflow use.

Either order can be defended:

- workflow before methodology if stages are the primary procedural artifact;
- methodology before workflow if principles generate the workflow.

Current choice is acceptable because `workflow.md` is explicitly the canonical stage source.

Recommended note:

Add a sentence stating that this order is document-maintenance order, not conceptual priority.

---

## Finding 10 — No structural dependence on FARE mathematics is currently needed

FAR v1.0 cleanup does not require new FARE definitions or theorems.

Assessment: pass.

FARE remains frozen correctly.

Future FARE expansion should occur only if FAR requires mathematical justification for a specific claim.

---

## Structural Verdict

FAR is now structurally coherent enough to proceed toward final stabilization.

However, FAR should not yet be declared v1.0 Stable.

Before final freeze, the following gaps should be addressed:

1. candidate generation placement;
2. FARO boundary statement;
3. example standard;
4. investigation validation checklist;
5. dependency graph clarification that document order is maintenance order, not conceptual priority.

---

## Required Changes Before FAR v1.0 Stable

1. Decide whether candidate generation is a distinct workflow stage or part of Stage 6.
2. Add a FARO boundary statement.
3. Add `frameworks/FAR/example-standard.md`.
4. Add `frameworks/FAR/investigation-validation.md`.
5. Clarify dependency-graph ordering.
6. Update `FAR-v1.0-criteria.md` to include examples and validation.
7. Update `README.md` navigation after adding the new documents.

---

## Recommended Next PR

Open a focused FAR Phase 2 cleanup PR implementing:

- example standard;
- investigation validation checklist;
- FARO boundary clarification;
- dependency graph clarification;
- v1.0 criteria expansion.

Do not modify FARE.

Do not begin FARO yet.
