# FARM Integration Record

## Purpose

This document defines the integration record used by FARM.

An integration record preserves cross-framework decisions, requirements, defects, routing decisions, and change-control outcomes.

---

## Integration Record

An integration record is an explicit artifact documenting a cross-framework issue and its handling.

---

## Required Fields

An integration record should include:

- record identifier;
- source artifact;
- source context;
- affected framework layers;
- defect classification if any;
- requirement routing if any;
- change request if any;
- decision;
- rationale;
- downstream effects;
- status.

---

## Statuses

An integration record may be:

- open;
- under review;
- accepted;
- rejected;
- deferred;
- resolved;
- superseded.

---

## Use Cases

Integration records should be used when:

- a worked example exposes a framework gap;
- a FARO operation exposes a FAR requirement;
- a FAR investigation exposes a FARA representational issue;
- an operational requirement exposes a FARE mathematical need;
- a stable-layer change may affect another layer.

---

## Boundary Rule

An integration record records cross-framework handling.

It does not itself alter any framework artifact.
