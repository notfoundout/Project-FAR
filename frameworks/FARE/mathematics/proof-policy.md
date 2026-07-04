# FARE Mathematics Proof Policy

## Purpose

This document governs proof construction within the FARE mathematics layer.

Its purpose is to preserve dependency order, prevent hidden assumptions, and distinguish definitions from results.

---

# Artifact Roles

## Definitions

Definitions introduce mathematical objects or terminology.

Definitions do not prove properties.

---

## Lemmas

Lemmas establish reusable intermediate results.

A lemma should support later propositions or theorems.

---

## Propositions

Propositions establish useful results of limited scope.

---

## Theorems

Theorems establish mathematical properties from accepted dependencies.

A theorem should not merely restate a definition.

Foundational theorems may record immediate definitional consequences when doing so clarifies dependency structure for later proofs.

---

## Corollaries

Corollaries follow directly from accepted theorems.

---

## Conjectures

Conjectures are proposed results not yet proven.

Conjectures shall never be cited as proof dependencies.

---

# Theorem Statuses

## Proposed

A statement suggested for investigation before a proof attempt is formalized.

---

## Draft

A theorem document exists, but the proof is incomplete, unreviewed, or currently unsupported by the definitions.

---

## Reviewed

The proof has undergone review but has not yet been accepted as part of the stable theorem library.

---

## Accepted

The theorem has a complete proof from accepted dependencies.

---

## Canonical

The theorem is accepted and used as a stable foundation for later mathematical development.

Canonical status should be rare.

---

# Dependency Rules

Every theorem shall explicitly list its dependencies.

Dependencies may reference only:

- earlier mathematical definitions;
- earlier accepted theorems;
- explicitly stated axioms or proof rules, if such objects exist.

A theorem shall not depend on:

- later theorems;
- draft theorems;
- conjectures;
- examples;
- archived legacy proofs.

Circular dependencies are prohibited.

---

# Required Theorem Sections

Every theorem document shall contain:

- Identifier;
- Title;
- Status;
- Objective;
- Dependencies;
- Statement;
- Proof;
- Corollaries;
- Consequences;
- Notes.

---

# Proof Requirements

Every proof shall:

- distinguish assumptions from conclusions;
- cite all dependencies explicitly;
- use only defined terminology;
- avoid hidden metric, topological, algebraic, or semantic assumptions;
- prove no statement stronger than its dependencies support.

If a statement cannot currently be proven, the theorem shall remain Draft and the proof section shall state `Proof pending.`

---

# Archival Rule

Historical or legacy proof documents may be retained for provenance.

Archived proofs are not active theorem dependencies.

They may not be cited by accepted or canonical theorems unless restored through formal review and renumbering.

---

# Notes

This policy governs mathematical proof development only.

It does not govern canonical framework definitions outside the mathematics layer.
