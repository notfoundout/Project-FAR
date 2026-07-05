# FARO Auditing

## Purpose

This document defines auditing within FARO.

Auditing checks whether a FAR investigation record satisfies FAR validation requirements and operational audit criteria.

Auditing does not determine truth or replace FAR methodology.

---

## Operation Category

Primary category: Audit.

---

## Definition

An audit is the systematic examination of a recorded FAR investigation to determine whether it satisfies explicitly defined audit criteria.

The audit evaluates the investigation record and its artifacts rather than asserting that the resolution is true.

---

## Required Inputs

Typical audit inputs include:

- investigation record;
- FAR workflow artifacts;
- reasoning state records;
- transition signatures or trace artifacts;
- admissibility records where applicable;
- resolution rule and resolution or closure status;
- revision records where applicable.

---

## Audit Criteria

A FARO audit may check:

- explicitness;
- artifact completeness;
- workflow completion;
- optional-stage justification;
- revision-record adequacy;
- closure-status adequacy;
- traceability;
- reconstructibility;
- boundary compliance.

---

## Procedure

A typical audit:

1. identifies the investigation;
2. verifies required artifacts;
3. verifies workflow stage treatment;
4. checks optional-stage justifications;
5. checks reasoning trace artifacts;
6. checks admissibility records where applicable;
7. checks resolution rule and closure status;
8. records defects, omissions, inconsistencies, or insufficiencies;
9. produces an audit report.

---

## Outputs

An audit produces an explicit audit record or audit report.

The report should identify passed checks, failed checks, incomplete checks, and boundary notes.

---

## Failure Modes

An audit may return incomplete if required input artifacts are missing.

An audit may return invalid if the investigation cannot be reconstructed.

---

## Boundary Notes

Auditing operates downstream of FAR v1.0 Stable.

It does not redefine FAR validation requirements, FARA architecture, or FARE mathematics.
