# FARM Dependency Graph

## Purpose

This document records FARM document-maintenance dependencies.

It does not introduce new primitives.

---

## Maintenance Order

```text
FARA
  -> FAR v1.0 Stable
  -> FARO v1.0 Stable
  -> FARE Mathematics v0.1
  -> FARM architecture.md
  -> FARM design-principles.md
  -> FARM requirement-routing.md
  -> FARM defect-classification.md
  -> FARM change-control.md
  -> FARM integration-record.md
  -> FARM-v1.0-criteria.md
```

---

## Dependency Roles

### Stable Framework Layers

FARA, FAR, FARO, and FARE provide the stable layers FARM coordinates around.

### FARM Architecture

Defines FARM's meta-framework role and boundaries.

### FARM Design Principles

Defines constraints governing FARM behavior.

### Requirement Routing

Defines how downstream requirements are routed to the correct stable layer.

### Defect Classification

Defines how defects are classified before any stable-layer change is proposed.

### Change Control

Defines gates for modifying stable layers.

### Integration Record

Defines the artifact used to record cross-framework decisions.

### FARM v1.0 Criteria

Defines the criteria required before FARM v1.0 Stable.

---

## Boundary Constraints

FARM shall not create circular authority where FARM can redefine the layers it governs.

Stable framework changes require explicit defect, inconsistency, or downstream requirement records.
