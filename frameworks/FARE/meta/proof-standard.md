# FARE Proof Standard

## Purpose

This document defines the minimum requirements for an accepted proof within the Formal Architecture of Reasoning Evaluation.

Every accepted proof shall satisfy every requirement defined herein.

---

# Acceptance Requirements

A proof shall:

- possess a unique identifier;
- possess a descriptive title;
- state its objective;
- identify every dependency;
- identify every canonical definition used;
- explicitly state its theorem;
- provide a complete derivation;
- identify every assumption;
- state its conclusion.

---

# Dependency Requirements

Every dependency shall:

- exist;
- be uniquely identifiable;
- be accepted;
- be relevant.

Unused dependencies shall be removed.

Hidden dependencies are prohibited.

---

# Definition Requirements

Every formal concept appearing in a proof shall reference its canonical definition.

Local redefinitions are prohibited.

---

# Inference Requirements

Every inference shall:

- follow an accepted inference rule;
- identify its supporting premises;
- preserve semantic consistency.

Invalid inference invalidates the proof.

---

# Assumption Requirements

Every assumption shall be explicitly identified.

Assumptions shall be classified as one of:

- Axiom
- Definition
- Accepted Theorem
- Temporary Assumption
- External Assumption

Hidden assumptions are prohibited.

---

# Conclusion Requirements

The conclusion shall follow from the preceding derivation.

No unsupported conclusion may appear.

---

# Traceability Requirements

Every theorem shall possess a finite dependency chain.

Every dependency shall be recursively traceable.

---

# Audit Requirements

Every accepted proof shall pass:

- Consistency Audit
- Dependency Audit
- Terminology Audit
- Traceability Audit

Additional audits may be required by future framework revisions.

---

# Revision Requirements

Any modification affecting:

- definitions;
- dependencies;
- inference;
- assumptions;
- conclusions;

requires re-auditing the proof.

---

# Invalid Proof Conditions

A proof is invalid if:

- an inference is invalid;
- a dependency is missing;
- terminology is inconsistent;
- a canonical definition is violated;
- hidden assumptions exist;
- circular dependency exists;
- the conclusion does not follow.

---

# Relationship to Meta-Theorems

This document specifies the operational acceptance criteria used by:

- M004 — Framework Consistency
- M005 — Investigation Soundness
- M006 — Proof Soundness

---

# Notes

This document governs proof acceptance.

It does not establish mathematical truth.

It specifies the structural and procedural requirements for accepting proofs within FARE.