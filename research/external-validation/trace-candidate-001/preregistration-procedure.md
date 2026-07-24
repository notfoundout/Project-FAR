# Trace Candidate 001 — Preregistration Procedure

Status: `PROCEDURE_REGISTERED`; candidate-specific freeze not yet executed.
Registered: 2026-07-23 (America/New_York)

## Purpose

Prevent outcome-aware reinterpretation by making the candidate-specific commitments, operationalizations, evidence requirements, comparison baseline, and scoring rules externally checkable before FAR reads the benchmark verdict or evaluates the trace.

## Required order

1. Acquire and hash the raw task statement and trace artifacts.
2. Separate task-description artifacts from outcome artifacts.
3. Read only the task statement, declared agent policy/configuration, and permitted pre-outcome metadata.
4. Create `freeze.md` containing:
   - candidate identifier and pinned source version;
   - allowed pre-freeze inputs;
   - forbidden outcome inputs not yet inspected;
   - candidate commitments;
   - rule classifications;
   - operationalizations;
   - alternative reasonable operationalizations;
   - minimum evidence required for each commitment;
   - FAR mappings and expected Unknown conditions;
   - comparison baseline;
   - scoring and adjudication rules;
   - explicit nonclaims.
5. Compute the SHA-256 digest of the exact UTF-8 bytes of `freeze.md`.
6. Record the digest in `freeze.sha256`.
7. Commit both files to Git before inspecting the benchmark verdict, test output, generated patch outcome, or resolved/unresolved label.
8. Record the freeze commit SHA in `run-record.md`.
9. Only then inspect outcome artifacts and run FAR.

## Integrity rule

Any post-freeze change to a commitment, operationalization, evidence requirement, or scoring rule requires:

- a new versioned freeze file;
- a new digest;
- an explicit explanation of why the change was necessary;
- separate reporting of results under the original and revised freeze where technically possible.

The original freeze must never be overwritten or deleted.

## Candidate status

The public dataset preview already displayed that the initial candidate `django__django-15044.traj` is marked unresolved. Therefore that outcome label is already contaminated for strict blind adjudication. The candidate may still be used for ingestion and evidence-sufficiency work, but it cannot serve as the strongest preregistered incremental-detection case unless a different outcome component remains genuinely uninspected.

For the decisive case, select a candidate whose benchmark outcome has not been viewed before the freeze is committed.
