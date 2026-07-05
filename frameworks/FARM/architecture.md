# FARM Architecture

## Purpose

This document defines the minimum architecture of FARM.

FARM is the meta-framework coordination layer of Project FAR.

It coordinates post-v1.0 requirements across stable framework layers without redefining those layers.

---

## Architectural Position

FARM is downstream of stable framework components.

```text
FARA -> FAR -> FARO -> FARM
```

FARA defines representational architecture.

FAR defines methodology.

FARO defines operations.

FARE provides frozen requirement-driven mathematical support.

FARM coordinates cross-framework requirements, defects, change control, and integration records.

---

## Core Responsibilities

FARM may:

- classify downstream defects;
- route requirements to the correct framework layer;
- record integration decisions;
- govern post-v1.0 change control;
- preserve stable-layer boundaries;
- manage feedback from worked examples.

---

## Prohibited Responsibilities

FARM shall not:

- redefine FARA architecture;
- redefine FAR methodology;
- redefine FARO operations;
- expand FARE mathematics without a reviewed requirement;
- perform FARO audits;
- replace project milestones or project status documents;
- become a catch-all governance layer.

---

## Minimum Architecture

FARM consists of:

- requirement routing;
- defect classification;
- change control;
- integration records;
- dependency governance;
- FARM v1.0 criteria.

---

## Boundary Rule

FARM can recommend changes to stable layers only by recording a concrete defect, inconsistency, or downstream requirement.

It cannot directly alter the meaning of any stable framework layer.
