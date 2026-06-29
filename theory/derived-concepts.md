# Derived Concepts

## Purpose

This document records the concepts of Project FAR that are currently regarded as derived rather than primitive.

The objective is to determine whether each derived concept can be completely characterized in terms of the primitive architecture of FARA.

Successful derivations strengthen the claim that the primitive architecture is both minimal and sufficient while reducing the number of primitive concepts required by the framework.

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

A derived concept is considered established only if:

- its derivation is complete;
- its derivation is non-circular;
- every dependency has been explicitly identified;
- every dependency ultimately terminates at the primitive architecture;
- no hidden assumptions remain;
- no successful counterexample has been identified; and
- the derivation preserves the expressive power of Project FAR.

Until these conditions are satisfied, a derivation remains proposed rather than established.

---

# DC-REASONING-STATE

## Status

Proposed

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

Determine whether Reasoning State can be completely characterized using only the primitive architecture.

---

## Proposed Derivation

An Investigation specifies the bounded context within which reasoning occurs.

Representations constitute the explicit objects manipulated during reasoning.

The Representational Structure specifies the explicit relationships among those representations.

Interpretation assigns meaning to the representations and their relationships.

The Reasoning Calculus governs the admissible transformations of those representations.

Accordingly, the complete condition of a reasoning process at any point appears to be completely characterized by these primitive concepts.

No additional primitive concept has presently been identified.

Reasoning State is therefore proposed to be a derived concept.

---

## Proposed Derived Definition

A **Reasoning State** is the complete characterization of an Investigation at a particular condition of reasoning, consisting of its representations, their representational structure, their interpretation, and the governing reasoning calculus.

---

## Verification Status

Verification in progress.

Current verification has identified several questions requiring resolution, including:

- whether "stage" introduces a hidden assumption;
- whether "configuration" constitutes an independent concept;
- whether the proposed derivation preserves expressive power.

No successful counterexample has presently been identified.

---

## Formal Derivation

Pending.

---

## Notes

This derivation remains provisional until formal verification has been completed.

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

Project FAR has entered the formal derivation phase.

The current objective is to determine whether every non-primitive concept can be derived from the primitive architecture without reducing expressive power.

No derived concept has yet been formally established.
