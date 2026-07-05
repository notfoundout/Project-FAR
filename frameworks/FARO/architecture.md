# FARO Architecture

## Purpose

This document defines the high-level operational architecture of FARO.

FARO operationalizes FAR v1.0 Stable over FARA representations and FAR investigation artifacts.

This document does not redefine FAR, FARA, or FARE.

---

## Architectural Position

FARO is downstream of both FARA and FAR.

```text
FARA -> FAR v1.0 Stable -> FARO
```

FARA defines representational architecture.

FAR defines investigation methodology.

FARO defines operations performed over explicit reasoning artifacts produced or governed by FAR and FARA.

---

## Operational Scope

FARO may define operations for:

- executing FAR investigations;
- auditing investigation records;
- comparing investigations;
- analyzing disagreement;
- producing reports;
- operationally evaluating investigation artifacts;
- detecting missing or defective artifacts;
- supporting repeatable review procedures.

---

## Core Operational Layers

### Execution Layer

Supports the conduct of FAR investigations without replacing FAR methodology.

### Audit Layer

Checks investigation artifacts against FAR validation requirements.

### Comparison Layer

Identifies similarities and differences between investigations or reasoning artifacts.

### Disagreement Analysis Layer

Locates and explains sources of divergence between investigations.

### Reporting Layer

Produces structured outputs describing operations, findings, defects, comparisons, or disagreements.

### Operational Evaluation Layer

Assesses operational qualities of investigation artifacts using FAR-grounded criteria.

---

## Operation Requirement

Every FARO operation shall specify:

- its category;
- required inputs;
- produced outputs;
- preconditions;
- postconditions;
- failure modes;
- FAR dependency;
- FARA dependency;
- boundary notes.

The canonical operation format is defined in `operation-interface-standard.md`.

---

## Boundary Rule

FARO may operationalize stable FAR.

FARO shall not redefine stable FAR methodology, FARA architecture, or FARE mathematics.

Operational convenience is not sufficient reason to alter canonical framework structure.
