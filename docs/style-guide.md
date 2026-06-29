# Project FAR Style Guide

## Purpose

This document defines the writing standards used throughout Project FAR.

The objective is to produce a repository that is internally consistent, non-redundant, and suitable for long-term development.

---

# Principle 1 — One Concept, One Definition

Every technical concept should have exactly one canonical definition.

Examples include:

- Representation
- Interpretation
- Reasoning State
- Investigation
- Ω
- Resolution

Canonical definitions belong in:

theory/definitions.md

Other documents should reference those definitions rather than restating them.

---

# Principle 2 — One Question Per Document

Every document should answer one primary question.

For example:

overview.md

"What is Project FAR?"

mission.md

"Why does Project FAR exist?"

scope.md

"What reasoning lies within the project's scope?"

No document should attempt to answer every question.

---

# Principle 3 — Definitions Before Conclusions

Every argument should proceed in the following order.

Definitions

↓

Assumptions

↓

Representations

↓

Reasoning

↓

Conclusions

Definitions should never be modified after conclusions have been reached.

---

# Principle 4 — Separate Stable Theory From Active Research

Stable material belongs in:

- theory/
- fara/
- far/
- faro/

Exploratory material belongs in:

- research/

Experimental ideas should not appear in the formal theory until sufficiently developed.

---

# Principle 5 — Explicit Status

Every important claim should identify its current status.

Possible statuses include:

Definition

Axiom

Proposition

Conjecture

Lemma

Theorem

Proof Sketch

Open Problem

No claim should appear without indicating its status.

---

# Principle 6 — Avoid Redundancy

Information should appear once.

Later documents should reference earlier documents instead of repeating them.

Repeated explanations should be replaced with references whenever practical.

---

# Principle 7 — Progressive Detail

Higher-level documents should summarize.

Lower-level documents should provide detail.

For example:

README.md

↓

overview.md

↓

architecture.md

↓

definitions.md

↓

proofs.md

Readers should move from general concepts toward increasing formal precision.

---

# Principle 8 — Revision History

Major conceptual changes should be recorded in:

CHANGELOG.md

Design decisions should be recorded in:

research/decision-log.md

Research progress should be recorded in:

research/journal.md

The repository should preserve both the current theory and its historical development.

---

# Principle 9 — Falsifiability

Every substantial claim should identify the conditions under which it would be considered false.

Counterexamples should be documented rather than discarded.

---

# Principle 10 — Minimality

Every document should justify its existence.

Every section should justify its inclusion.

Every concept should justify its necessity.

The organization of the repository should reflect the same minimality principle that guides the development of Project FAR itself.
