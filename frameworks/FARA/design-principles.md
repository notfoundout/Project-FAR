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

Framework documents may specify architectural roles, constraints, local formal carrier names, or examples, but they should not redefine canonical terms independently.

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

Project FAR minimizes schema commitments relative to a declared contract. The seven retained FARA roles are not global primitives. Reification, tagging, splitting, and combination must be considered before any scoped lower-bound claim.

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

## Principle 13 — Typed Identity and Kernel Equivalence

Within the scope of `FARA-FORMAL-KERNEL-001`, identity is typed and occurrence-sensitive.

- one identity token belongs to exactly one formal carrier sort;
- distinct transformation-execution Events remain distinct even when their extensional rule/state fields coincide;
- distinct RelationOccurrences remain distinct even when their type and participants coincide;
- literal identifier spelling is not semantic;
- equivalent renaming may not merge, split, create, or delete identities.

Canonical kernel-equivalence is **sort-preserving relational isomorphism**: one bijection per carrier sort that preserves and reflects every declared relation. Behavioral similarity, commitment equivalence, and lossy projection do not substitute for kernel-equivalence unless a separate scoped relation is explicitly declared.

This principle is bounded to the Accepted formal-kernel scope. It is not a claim that the same identity or equivalence criteria govern every possible reasoning architecture.

---

## Maintenance Policy

This document should be updated whenever a new architectural principle is adopted or an existing principle is revised.

Any change to these principles should be justified by an audit, grounding investigation, accepted promotion record, or formal methodological decision.

## Contract and factorization discipline

FARA conformance is structural. Exact adequacy requires a separate FAR factorization proof under a declared contract. A collision refutes sufficiency; absence of a decoder and collision remains OPEN. Audit-only distinctions and machinery costs must be disclosed.
