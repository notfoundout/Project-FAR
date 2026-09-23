# Expertise Applicability Protocol

Status: **Accepted — bounded internal methodology extension**  
Contract: `FAR-EXPERTISE-APPLICABILITY-1.0`

## Purpose

This protocol governs use of a source's expertise as evidence about whether that source is qualified to contribute to a specific proposition.

Expertise is proposition-relative and scope-bounded. Evidence of competence in one domain does not silently transfer to another domain, subdomain, claim type, population, geography, time period, or method.

The protocol does not establish the truth of the source's substantive claim. It controls only the separate question of expertise applicability.

## Trigger

Run this protocol whenever an investigation materially relies on a person's, institution's, model's, or source's claimed expertise, credentials, specialized competence, or domain authority as part of evidence appraisal.

If the investigation does not rely on expertise, record `NOT_APPLICABLE` with a reason rather than manufacturing an expertise assessment.

## Required separation

Keep these propositions distinct:

1. the source possesses competence within scope `S`;
2. scope `S` applies to claim `C`;
3. the source asserts `C`;
4. independent evidence supports `C`.

No one proposition entails another without an explicit bridge.

In particular:

`expertise(source, X)` does not imply `expertise(source, Y)`.

`expertise_applicable(source, C)` does not imply `true(C)`.

## Expertise assertion

An expertise assertion records at least:

- source identity;
- domain and optional subdomain;
- claim type;
- population scope;
- geographic scope;
- temporal scope;
- method scope;
- competence basis;
- provenance for that basis;
- assessment status;
- uncertainty and limitations;
- validity interval;
- assessor, method, and version.

`valid_from` and any non-null `valid_until` must be parseable timezone-aware date-times. `valid_until` may not precede `valid_from`. The validity interval bounds the expertise assessment itself; proposition-relative temporal applicability remains a separate comparison dimension and is not inferred from the interval.

Allowed assertion statuses are:

- `SUPPORTED`;
- `PARTIALLY_SUPPORTED`;
- `INSUFFICIENT_EVIDENCE`;
- `CONTRADICTED`;
- `INDETERMINATE`;
- `NOT_APPLICABLE`.

The status applies only to the recorded expertise assertion. It is not a claim-truth status.

## Proposition-relative applicability

Every material use of an expertise assertion requires a separate applicability record bound to the exact expertise-assertion revision and exact claim revision.

The applicability record therefore names both `expertise_assertion_id` and `expertise_assertion_version`, and both `claim_id` and `claim_version`. The copied expertise and claim scopes must correspond to those resolved revisions. A later revision that retains the same stable ID does not inherit an earlier applicability result.

The record compares at least:

- domain;
- subdomain;
- claim type;
- population;
- geography;
- time;
- method.

Each dimension is assessed as one of:

- `MATCH`;
- `PARTIAL`;
- `MISMATCH`;
- `UNKNOWN`;
- `NOT_APPLICABLE`.

A dimension marked `MATCH` with different recorded scope values requires an explicit bridge explaining why the difference preserves applicability. Mere adjacency, prestige, institutional affiliation, or broad field similarity is not a bridge.

`SUPPORTED` overall applicability requires every material dimension to match. A mismatch, partial match, or unknown dimension prevents fully supported applicability.

## Source-resolution binding

Standalone record validation proves only internal consistency. Before an applicability result is used, the parent investigation must resolve the referenced expertise assertion revision and claim revision and verify that the stored IDs, versions, and scopes match those source records.

`mechanization/far_mechanization/socratic_epistemic.py` exposes `validate_expertise_applicability_binding(...)` for this resolver-assisted check. The helper does not fetch source records itself; source resolution and provenance remain obligations of the parent FAR investigation.

A version mismatch or resolved-scope mismatch invalidates reuse of the applicability record until it is re-evaluated.

## Evidence use

An expertise-applicability assessment may affect source appraisal, interpretation confidence, search prioritization, or weighting under a separately declared evidence protocol.

It may not:

- replace direct evidence where direct evidence is required;
- convert testimony into proof by status alone;
- repair an invalid inference;
- expand the scope of the source's assertion;
- erase counterevidence;
- override the parent investigation's evidence contract or decision threshold.

## Revision

A material change in credentials, domain, method, claim scope, population, geography, time, validity interval, expertise-assertion version, claim version, or other applicability dimension requires a new version or new applicability record.

Earlier records remain reconstructible. A later broader expertise assessment does not retroactively validate an earlier use unless that relation is explicitly re-evaluated.

## Failure conditions

The protocol fails if:

- an expertise claim lacks a bounded scope;
- `valid_from` or non-null `valid_until` is not a parseable timezone-aware date-time;
- `valid_until` precedes `valid_from`;
- an applicability record omits the exact expertise-assertion or claim version;
- a resolved expertise assertion or claim does not match the ID, version, or scope recorded by the applicability assessment;
- competence is transferred to a materially different scope without an explicit applicability assessment;
- a `MATCH` is asserted across different scope values without an explicit bridge;
- an overall `SUPPORTED` applicability hides a `PARTIAL`, `MISMATCH`, or `UNKNOWN` material dimension;
- expertise applicability is treated as substantive truth;
- provenance for the competence basis or applicability judgment is missing;
- a changed scope, validity interval, expertise-assertion revision, or claim revision silently reuses an earlier applicability result.

## Machine-readable record

The accepted internal interchange contract is `socratic-epistemic-extensions/1.0` with record types `EXPERTISE_ASSERTION` and `EXPERTISE_APPLICABILITY`, governed by:

- `schemas/socratic-epistemic-extensions-v1.schema.json`;
- `mechanization/far_mechanization/socratic_epistemic.py`.

Schema conformance and single-record semantic validation establish record consistency only. Resolver-assisted binding validation establishes that an applicability record points to the resolved source revisions supplied by the parent investigation. None of these checks establishes that the source truly possesses expertise or that the source's substantive claim is true.

## Relationship to FAR

This protocol is an evidence-appraisal protocol used within the canonical FAR workflow. It does not add a workflow stage or reasoning primitive.

## Relationship to FARA

The records are expressible using existing identity-bearing representations, relations, states, and provenance. No new FARA primitive is claimed or required.

## Nonclaims

This protocol does not define a universal ontology of expertise, prove that expertise predicts correctness, rank professions, or supply a universal rule for translating competence between adjacent domains.
