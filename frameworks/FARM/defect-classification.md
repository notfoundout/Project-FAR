# FARM Defect Classification

## Purpose

This document defines how FARM classifies downstream defects before routing or change control.

---

## Defect

A defect is a recorded problem in a framework artifact, example, operation, proof, dependency, or governance record.

A defect is not automatically a mandate to change a stable layer.

---

## Defect Classes

### Definition Defect

A canonical definition is missing, circular, duplicated, ambiguous, or inconsistent.

### Architecture Defect

A framework architecture has missing, overlapping, or conflicting responsibilities.

### Methodology Defect

A procedure, workflow, or validation method is incomplete, ambiguous, or non-reconstructible.

### Operation Defect

A FARO operation or operation category has unclear inputs, outputs, failure modes, or boundaries.

### Mathematical Defect

A FARE definition, theorem, proof, or dependency is missing, invalid, or insufficient.

### Boundary Defect

A document or operation crosses framework boundaries improperly.

### Example Defect

A worked example fails to instantiate the relevant framework correctly.

### Governance Defect

A milestone, status, decision log, or canonical map entry is stale, conflicting, or incomplete.

---

## Classification Rule

Every defect should identify:

- defect class;
- affected artifact;
- evidence of defect;
- affected framework layer;
- severity;
- recommended routing target;
- proposed status.

---

## Statuses

A defect may be:

- accepted;
- rejected;
- deferred;
- unresolved;
- duplicate;
- superseded.

---

## Boundary Rule

Classifying a defect does not itself modify any framework layer.
