# FARO Epistemic Boundary

Status: **Provisional — candidate FARO reporting operation**  
Contract: `FARO-EPISTEMIC-BOUNDARY-1.0`

## Operation Name

Epistemic Boundary Materialization

## Operation Category

Primary category: Reporting.

Secondary category: Operational Evaluation, only when the operation checks whether required boundary inputs are present.

## Comparison Contract

`NOT APPLICABLE` for ordinary boundary materialization. This operation does not make an adequacy, preservation, common-content, invariance, minimality, or comparative superiority claim.

If a later use compares two boundary representations for information preservation, that comparison requires its own versioned comparison contract under the FARO operation-interface standard.

## Purpose

Produce one compact, machine-readable terminal view of the exact boundary of justification already recorded by a FAR investigation.

The operation consolidates existing FAR closure information. It does not create new truth values, alter the claim disposition, or replace the canonical evidence-closure record.

## Required Inputs

- investigation identity;
- exact claim identity and version;
- evidence cutoff;
- search frame;
- canonical closure-record references;
- claim-level logical disposition and its basis;
- conditional results and their assumptions where present;
- supported but unestablished propositions where present;
- explicit `Unknown` items and reasons;
- matters explicitly outside the investigation scope when recorded;
- non-identifiability findings where recorded;
- explicit nonclaims;
- falsifiers;
- surviving propositions;
- residual uncertainty;
- limitations;
- assumptions;
- closure status;
- provenance.

## Optional Inputs

- source-specific expertise applicability records;
- elenchus session references;
- disagreement-analysis records;
- later correction or supersession references.

These optional inputs may explain the boundary but do not change the underlying FAR closure semantics.

## Preconditions

1. The parent FAR investigation and claim are identifiable.
2. The boundary is bound to the same evidence cutoff and search frame as the referenced closure record.
3. Every summarized item is traceable to an underlying FAR artifact.
4. The operation does not invent content to fill an empty category.

## Procedure

1. Bind the investigation, claim version, evidence cutoff, search frame, and closure-record references.
2. Materialize exactly what the underlying investigation establishes at the recorded scope.
3. Materialize conditional results together with the assumptions or conditions on which they depend.
4. Materialize propositions supported by evidence but not established at a stronger status.
5. Preserve explicit unknowns with reasons.
6. Preserve matters recorded as outside the investigation scope under `not_investigated`.
7. Preserve questions the frozen evidence cannot discriminate under `not_identifiable_from_current_evidence`.
8. Preserve explicit nonclaims, falsifiers, surviving propositions, residual uncertainty, limitations, and assumptions.
9. Record the FAR investigation closure status unchanged.
10. Validate the resulting object and preserve provenance back to the underlying closure artifacts.

## Outputs

One `EPISTEMIC_BOUNDARY` record conforming to `socratic-epistemic-extensions/1.0`.

The terminal categories are:

- `established`;
- `conditionally_established`;
- `supported_not_established`;
- `unknown`;
- `not_investigated`;
- `not_identifiable_from_current_evidence`;
- `explicit_nonclaims`.

These are reporting categories. They do not replace existing FAR/FARA/FARO status vocabularies outside this operation.

## Postconditions

- every populated boundary statement is traceable;
- conditional claims name their conditions;
- unknown, not-investigated, and non-identifiable entries state why they occupy that category;
- the same scoped statement is not silently placed in incompatible categories;
- the object points to the canonical closure record rather than masquerading as one.

## Failure Modes

- missing or inconsistent parent claim identity;
- missing closure-record reference;
- evidence cutoff or search-frame mismatch;
- a boundary statement with no underlying basis reference;
- a conditional result with no condition reference;
- an unknown/non-investigated/non-identifiable entry without a reason;
- the same scoped statement placed in incompatible categories;
- attempted promotion of `not_investigated` into evidence of absence;
- attempted promotion of non-identifiability into falsity;
- attempted replacement of canonical evidence-closure artifacts by the derived view.

A failed materialization produces an incompleteness or defect report rather than a fabricated boundary.

## FAR Dependency

The operation depends on the canonical FAR workflow, investigation validation, and `FAR-EVIDENCE-CLOSURE-1.0` for the semantics it summarizes.

## FARA Dependency

The operation uses existing identity-bearing representations and relations. It does not add a FARA primitive.

## FARE Dependency

None required for the reporting operation itself.

## Boundary Notes

The epistemic boundary is a derived FARO view. It does not prove source completeness, semantic completeness, factual truth, external replication, or exhaustive knowledge of all possible unknowns.
