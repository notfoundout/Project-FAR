# FAR Methodology

## Purpose

This document defines the methodology of the Foundational Analysis of Reasoning (FAR).

FAR provides a structured process for conducting investigations within the architectural framework established by FARA.

It defines how the architectural components are applied during an investigation.

---

## Objective

The objective of FAR is to conduct investigations that are:

- Structured
- Explicit
- Auditable
- Reconstructible

The methodology is independent of any particular reasoning calculus or application domain.

---

## FAR Methodology

A FAR investigation proceeds through the following stages.

1. Define the investigation.
2. Establish the representational structure.
3. Specify the interpretation.
4. Select the reasoning calculus.
5. Construct the initial reasoning state.
6. Apply explicit transformations represented by transition signatures.
7. Construct the Admissibility Structure (Ω).
8. Apply the applicable resolution rule.
9. Record the resolution.

Each stage is described in greater detail elsewhere within this directory.

---

## Principles

Every FAR investigation should satisfy the following principles.

### Explicitness

Every assumption, representation, transformation, and conclusion should be explicitly represented.

---

### Auditability

The complete investigation should be reconstructible from its recorded reasoning states and transition signatures.

---

### Neutrality

The methodology does not prescribe which reasoning calculus should be used.

Different investigations may employ different reasoning calculi.

---

### Reproducibility

Equivalent investigators following the same methodology should be capable of reproducing equivalent investigations.

---

## Relationship to FARA

FARA defines the architectural components used during an investigation.

FAR defines the methodology for applying those components.

The methodology depends upon the architecture but does not modify it.

---

## Current Status

The FAR methodology remains under development.

Current work includes:

- refinement of investigation procedures,
- formalization of workflows,
- and validation across diverse reasoning domains.
