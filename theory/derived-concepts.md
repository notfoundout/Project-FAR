# Derived Concepts

## Purpose

This document records the concepts of Project FAR that are regarded as derived rather than primitive.

The objective is to demonstrate that each derived concept can be completely characterized in terms of the primitive architecture of FARA.

Successful derivations strengthen the claim that the primitive architecture is both minimal and sufficient.

---

# Primitive Architecture

The current candidate primitive concepts are:

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

Every derived concept should ultimately depend only upon these primitives.

---

# Derivation Standards

A derived concept is considered formally established only if:

- Its derivation is complete.
- Its derivation is non-circular.
- Every dependency is explicitly identified.
- Every dependency ultimately terminates at the primitive architecture.
- The derivation preserves the expressive power of Project FAR.

---

# DC-REASONING-STATE

## Status

**Proposed**

---

## Primitive Dependencies

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

---

## Derived Dependencies

None.

---

## Objective

Determine whether a Reasoning State can be completely characterized using only the primitive architecture.

---

## Proposed Derivation

An investigation specifies the context within which reasoning occurs.

Representations constitute the explicit information manipulated during the investigation.

The representational structure specifies how those representations are organized.

Interpretation assigns meaning to the representations.

The reasoning calculus governs the admissible transformations of the representations.

At any stage of an investigation, the complete configuration of representations, together with their organization, interpretation, and governing reasoning calculus, completely characterizes the current condition of the reasoning process.

Accordingly, no additional primitive concept appears necessary.

Reasoning State is therefore proposed to be a derived concept rather than a primitive concept.

---

## Proposed Derived Definition

A **Reasoning State** is the complete configuration of representations, their representational structure, their interpretation, and the governing reasoning calculus at a particular stage of an investigation.

---

## Verification Checklist

Before this derivation can be accepted, it must be shown that:

- No hidden primitive concepts have been introduced.
- The derivation is non-circular.
- The derivation preserves expressive power.
- No counterexamples require Reasoning State to remain primitive.

---

## Formal Derivation

Pending.

---

## Notes

This derivation is provisional.

Acceptance requires successful verification against the criteria above.

---

# Remaining Derived Concepts

The following concepts remain pending derivation.

- DC-TRANSITION-SIGNATURE
- DC-CANDIDATE
- DC-ADMISSIBILITY-STRUCTURE
- DC-RESOLUTION-RULE
- DC-RESOLUTION

---

# Research Status

Project FAR has begun the formal reduction of its architecture.

No derived concept has yet been formally established.

All proposed derivations remain subject to verification and possible rejection.
