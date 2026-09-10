# Repository Certification Status

## Purpose

This report records the current Repository Certification decision for Project FAR.

## Why?

Project FAR requires repository-level quality claims to fail closed when current evidence contradicts them. A successful validation run is not sufficient to certify the repository while a governed defect ledger contains unresolved certification-relevant failures.

## Scope

This report evaluates repository governance, documentation, architecture, navigation, automation, repository integrity, and certification evidence. It does not revise or reinterpret protected mathematical artifacts and does not perform external scientific work.

## Role in Project FAR

This is the repository-level certification status record. Its decision is constrained by the frozen Repository Certification Standard and by the current merged-review reconciliation ledger. It cannot independently waive unresolved failures.

## Dependencies

- [Repository Certification Standard](../governance/repository-certification-standard.md)
- [Repository Certification Index](README.md)
- [Canonical Map](../CANONICAL_MAP.md)
- [Merged-PR Review Reconciliation](../audits/merged-pr-review-reconciliation/README.md)
- `docs/audits/merged-pr-review-reconciliation/disposition-ledger.json`
- `tools/check_certification_compliance.py`

## Dependents

- Future release reviews.
- Repository maintenance.
- Long-term certification regression checks.

## Design Rationale

The frozen certification standard permits only `PROJECT FAR REPOSITORY CERTIFIED` or `PROJECT FAR REPOSITORY CERTIFICATION FAILED`. It requires every Certification Failure to be resolved before certification succeeds. Therefore unresolved current defects or unresolved verification obligations force the failed state; passing CI does not override that requirement.

## Protected Boundary Confirmation

This status correction modifies no primitive, canonical mathematical definition, axiom, lemma, proposition, theorem, accepted proof object, accepted mathematical dependency metadata, accepted doctrine, or frozen Foundation artifact.

## Certification Status Summary

| Status item | Result |
|---|---|
| Certification decision | Failed |
| Unresolved merged-review reconciliation findings | Nonzero; authoritative count is read from `disposition-ledger.json` |
| Proven currently reproducible protected-validator defects | 3 |
| Protected mathematical artifacts modified by this correction | 0 |
| Maintenance readiness | Not certifiable until the governing failure conditions are cleared |

## Current Failure Basis

The merged-review reconciliation ledger is a fail-closed current-state audit of findings that earlier review adjudication classified as incorrectly resolved. At the audited state it contains unresolved findings, including three defects freshly reproduced in protected validation code. The exact residual count is machine-readable in `disposition-ledger.json`; this document intentionally does not duplicate that changing number as a second authority.

The three protected-validator defects have prepared, tested candidate repairs under `research/internal-assurance-2026-09-10/`, but the repository's protected-transition mechanism rejects those bytes without an authorization that already exists on the protected comparison base. Prepared patches are not merged fixes and are not counted as closure.

The remaining reconciliation entries must receive evidence-backed current dispositions. An implicit/default `cannot_verify` state is an unresolved verification obligation, not evidence that a defect is absent.

## Certification Consequences

Until the reconciliation ledger contains no certification-blocking current defect or unresolved required verification obligation, repository-level prose must not claim that Project FAR is repository certified. Individual validators, workstreams, formal artifacts, or bounded assurance results may still pass within their exact scopes; those narrower results do not entail repository certification.

## Automation Requirement

`tools/check_certification_compliance.py` reads the authoritative reconciliation ledger and enforces the certification decision. A nonzero residual count requires this status document to state failure. A zero residual count is necessary but not by itself sufficient for certification: the frozen standard also requires every mandatory audit to pass, every improvement opportunity and deferral to be documented, protected boundaries to remain intact, repository claims to be verifiable, canonical concepts to be unique, repository artifacts to be justified, and final certification to be approved.

## Merge Readiness Assessment

This status correction is internally mergeable when its own validation passes, but the repository is not certified. The protected-validator repairs remain blocked by their legitimate protected-transition authorization requirement. That control is not weakened or bypassed here.

## Certification Decision

PROJECT FAR REPOSITORY CERTIFICATION FAILED
