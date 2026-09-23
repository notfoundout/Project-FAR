# FARO Reporting

## Purpose

This document defines reporting operations within FARO.

Reporting operations produce structured records of FARO execution, audit, comparison, disagreement analysis, operational evaluation, or derived epistemic-boundary materialization.

---

## Definition

A report is an explicit output artifact summarizing an operation, its inputs, its procedure, its findings, and its limitations.

---

## Report Types

FARO may produce:

- execution reports;
- audit reports;
- comparison reports;
- disagreement reports;
- operational evaluation reports;
- defect reports;
- incompleteness reports;
- epistemic-boundary views.

An epistemic-boundary view is governed by [`epistemic-boundary.md`](epistemic-boundary.md). It is a derived view over existing FAR closure artifacts. It does not replace the closure record or create new truth semantics.

---

## Minimum Report Sections

Every FARO report should identify:

- comparison contract or `NOT APPLICABLE`;
- exact/approximate objective and any loss or cost order;
- decoder/factorization, collision, or OPEN status;
- profile, frame, admitted transformations, and charged auxiliary machinery;
- report type;
- operation performed;
- input artifacts;
- operation category;
- procedure summary;
- findings;
- limitations;
- failure modes encountered;
- boundary notes;
- output status from `PROVED`, `REFUTED`, `OPEN`, `BLOCKED`, `UNDERDETERMINED`, `NOT APPLICABLE`, or `HISTORICAL/SUPERSEDED`.

When the report type is an epistemic-boundary view, comparison-specific fields that do not apply are explicitly `NOT APPLICABLE`; the view instead binds the parent investigation, claim version, evidence cutoff, search frame, canonical closure-record references, terminal boundary categories, assumptions, falsifiers, surviving propositions, residual uncertainty, limitations, and closure status required by `FARO-EPISTEMIC-BOUNDARY-1.0`.

---

## Boundary Rule

A FARO report records operational findings.

It does not redefine FAR methodology, FARA architecture, or FARE mathematics.

A report does not determine truth unless the relevant operation explicitly includes truth-evaluation criteria grounded in the investigation.

An epistemic-boundary view summarizes the parent FAR investigation's recorded justification boundary. FAR does not depend on that downstream materialization.
