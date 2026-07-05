# FARO Operation Interface Standard

## Purpose

This document defines the required structure for FARO operation specifications.

Every canonical FARO operation should follow this interface unless a justified exception is recorded.

---

## Required Fields

### Operation Name

The operation's canonical name.

### Operation Category

The operation's primary category from `operation-taxonomy.md`.

### Purpose

The operational purpose of the operation.

### Required Inputs

Inputs required before the operation can run.

### Optional Inputs

Inputs that may refine or constrain the operation.

### Preconditions

Conditions that must hold before execution.

### Procedure

The ordered procedure performed by the operation.

### Outputs

Artifacts produced by the operation.

### Postconditions

Conditions that hold after successful execution.

### Failure Modes

Known ways the operation may fail, halt, return incomplete results, or require additional input.

### FAR Dependency

The FAR methodology, workflow, validation, or artifact standard the operation relies on.

### FARA Dependency

The FARA representation or architectural object the operation relies on.

### FARE Dependency

Any mathematical dependency, if required.

If no FARE dependency exists, the operation must state that none is required.

### Boundary Notes

A statement of what the operation does not redefine or modify.

---

## Output Rule

Every operation must produce an explicit output artifact, even when the output is a failure, incompleteness notice, or defect report.

---

## Failure Rule

Failure modes are part of the operation specification.

An operation that cannot report failure conditions is not yet canonical.
