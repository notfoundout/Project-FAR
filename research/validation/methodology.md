# Validation Methodology

## Purpose

This document defines the methodology for validation investigations in Project FAR.

Validation investigations evaluate whether existing architectural, methodological, or theoretical claims survive structured attempts at failure.

This document does not introduce canonical terminology. Canonical terminology remains maintained in:

`theory/definitions/definitions.md`

---

## Validation Standard

A validation investigation should attempt to falsify or constrain the claim under investigation.

A validation investigation should not merely demonstrate that the framework can be made to work in a favorable case.

The preferred method is adversarial representation: choose cases likely to expose ambiguity, insufficiency, circularity, category collapse, or unproven assumptions.

---

## Required Sections

Each validation investigation should include:

- purpose;
- research question;
- hypothesis;
- attempted falsification;
- methodology;
- test cases;
- observations;
- results;
- architectural deficiencies found;
- required modifications;
- conclusion;
- research status.

---

## Success Criteria

A validation investigation succeeds when the tested claim survives the defined attempted falsification without requiring ad hoc modification.

Survival does not prove the claim.

It only provides evidence that the claim survived the tested conditions.

---

## Failure Criteria

A validation investigation fails when the tested claim requires:

- an undefined concept;
- an inconsistent dependency;
- a circular definition;
- category collapse;
- an ad hoc architectural extension;
- an ungrounded assumption;
- unexplained loss of information;
- failure to preserve explicitness or auditability.

Failure is an acceptable and valuable research result.

---

## Result Statuses

Validation results may be classified as:

- Accepted;
- Provisional;
- Failed;
- Archived;
- Unknown.

A failed validation should identify the precise reason for failure and the artifact affected.

---

## Maintenance Policy

This methodology should be revised when validation investigations expose weaknesses in the validation process itself.

Methodology changes should be justified by audit findings, failed validations, or explicit methodological investigations.
