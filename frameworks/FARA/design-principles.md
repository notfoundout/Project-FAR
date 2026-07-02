# FARA Design Principles

## Purpose

This document centralizes the design principles governing the Foundational Architecture of Reasoning Analysis (FARA).

These principles guide the construction, revision, and evaluation of FARA documents.

They are not independent definitions. Canonical terminology remains maintained in:

`theory/definitions/definitions.md`

---

## Principle 1 — Canonical Terminology

FARA documents must use the canonical terminology established in:

`theory/definitions/definitions.md`

Framework documents may specify architectural roles, constraints, or examples, but they should not redefine canonical terms independently.

---

## Principle 2 — Representation/Object Separation

A representation is distinct from that which it represents.

No FARA document should collapse:

- representation and represented object;
- reasoning state and reasoning state representation;
- reasoning state representation and reasoning state record;
- transition signature and transformation execution;
- Ω and the admissibility classifications it records.

This distinction is foundational to FARA's architecture.

---

## Principle 3 — Rule/Execution/Result Separation

A rule specifies conditions.

An execution applies a rule.

A result is produced by an execution.

FARA must preserve the distinctions among:

- transformation rule;
- transformation execution;
- transformation result;
- resolution rule;
- resolution execution;
- resolution.

---

## Principle 4 — Reduction Over Expansion

Project FAR prefers reducing concepts to simpler concepts over expanding the primitive basis.

A concept should be treated as a candidate primitive only when no successful reduction has been established.

Candidate primitive status remains provisional.

---

## Principle 5 — Explicitness

Architectural entities should be explicitly representable.

Implicit reasoning, hidden criteria, unrecorded transformations, or unstated dependencies weaken auditability and should be avoided.

---

## Principle 6 — Auditability

FARA is designed to support reconstruction and evaluation of reasoning.

Reasoning artifacts should make explicit:

- representations involved;
- interpretations used;
- reasoning calculi applied;
- transformation executions recorded;
- admissibility classifications produced;
- resolution rules applied.

---

## Principle 7 — Calculus Independence

FARA does not prescribe a single reasoning calculus.

Different investigations may employ different reasoning calculi.

FARA specifies the architecture required to represent reasoning under a calculus, not the exclusive calculus that reasoning must use.

---

## Principle 8 — Interpretation Separation

Representational structure and semantic interpretation must remain distinct.

The same representational structure may receive different interpretations.

Semantic equivalence and structural equivalence should not be treated as interchangeable.

---

## Principle 9 — Scope Discipline

Claims of universality, minimality, completeness, expressive power, or equivalence must specify their scope.

Unscoped generality claims should be treated as incomplete.

---

## Principle 10 — Architecture/Operation Separation

FARA specifies architectural structure.

FARO should specify operations performed over that structure.

The boundary is:

```text
FARA: what exists architecturally
FARO: what happens operationally
```

Future work should preserve this distinction.

---

## Principle 11 — Traceability

Architectural decisions should be traceable to:

- canonical definitions;
- grounding investigations;
- artifact audits;
- reduction attempts;
- proof obligations;
- explicit methodological decisions.

Untraceable architectural changes should not be treated as stable.

---

## Principle 12 — Stability Through Evidence

FARA should evolve only when supported by explicit evidence.

Acceptable evidence includes:

- grounding investigations;
- formal proofs;
- counterexamples;
- artifact audits;
- demonstrated reductions;
- identification of hidden assumptions;
- improvements in expressive or explanatory power.

Architectural stability is earned through investigation rather than assumed by declaration.

---

## Maintenance Policy

This document should be updated whenever a new architectural principle is adopted or an existing principle is revised.

Any change to these principles should be justified by an audit, grounding investigation, or formal methodological decision.