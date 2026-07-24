# Trace Candidate 001

Status: `RAW_ARTIFACT_PENDING`
Branch: `validation/trace-candidate-001`
Started: 2026-07-23

## Objective

Determine whether FAR can ingest and evaluate a real external software-agent trajectory without changing the protocol to fit the observed outcome.

## Current candidate

- Source family: SWE-bench / SWE-agent
- Initial artifact: `django__django-15044.traj`
- Submission: `20240402_sweagent_gpt4`
- Known public metadata: ten trajectory steps; benchmark label was exposed as unresolved in the dataset preview.

## Adjudication consequence

Because the resolved/unresolved label was visible before a candidate-specific freeze was committed, this artifact is eligible for:

- acquisition-chain validation;
- trace-ingestion work;
- evidence-sufficiency analysis;
- CIR compatibility testing;
- cost measurement.

It is not eligible as the strongest blind decisive case for proving incremental detection value.

A separate candidate with an uninspected outcome must be frozen before outcome access for that claim.

## Required next actions

1. Acquire the raw trajectory and associated task statement, generated patch, report, and test output.
2. Hash every raw artifact and complete `acquisition-chain.md`.
3. Run ingestion and classify each FAR-relevant field as observed, derived, inferred, declared, or unverifiable.
4. Select a second candidate without viewing its outcome.
5. Commit that candidate's `freeze.md` and `freeze.sha256` before opening outcome artifacts.

## Claim boundaries

A positive result on this software-engineering trace would support external trace compatibility and possibly incremental testing value. It would not establish fuzzy-policy handling, privacy-sensitive production feasibility, broad failure prevalence, willingness to pay, or production deployment validity.
