# Repository Certification Index

## Purpose

This index is the canonical navigation hub for Repository Certification.

## Why?

Repository Certification spans governance, inventory, semantic certification, architecture certification, documentation standardization, compliance enforcement, independent audit, and certification status evidence. A single index prevents contributors from treating any report as an isolated or competing source of certification authority.

## Scope

This index covers certification artifacts that define, evaluate, enforce, and finalize repository certification. It does not change accepted mathematics or replace artifact-specific reports.

## Role in Project FAR

This document connects Repository Certification governance, audit baselines, corrective reports, enforcement tooling, independent review, and certification status.

## Dependencies

- [Repository Certification Standard](../governance/repository-certification-standard.md)
- [Repository Certification Inventory Audit](../audits/repository-certification-inventory-audit.md)
- [Semantic Certification Report](../audits/semantic-certification-report.md)
- [Canonical Vocabulary Index](../glossary/canonical-vocabulary-index.md)
- [Repository Architecture Certification Report](../audits/repository-architecture-certification-report.md)
- [Documentation Standardization Report](../audits/documentation-standardization-report.md)
- [Repository Domain Registry](../architecture/repository-domain-registry.md)
- [Repository Compliance Enforcement Report](../audits/repository-compliance-enforcement-report.md)
- [Independent Repository Certification Audit](../audits/independent-repository-certification-audit.md)
- [Repository Certification Status](repository-certification-status.md)

## Dependents

- Repository maintenance.
- Future release reviews.
- Long-term certification regression checks.

## Design Rationale

The index is navigational rather than evidentiary. Each artifact retains its own canonical content while this document records how the artifacts relate.

## Certification Artifact Registry

| Artifact | Purpose | Scope | Canonical status | Certification area | Dependencies | Dependents |
|---|---|---|---|---|---|---|
| [Repository Certification Standard](../governance/repository-certification-standard.md) | Defines certification governance, protected boundaries, criteria, and completion rules. | Repository Certification governance. | Canonical governance standard. | Standard | Research Execution Charter. | Repository maintenance and certification status. |
| [Repository Certification Inventory Audit](../audits/repository-certification-inventory-audit.md) | Records the repository inventory baseline, classifications, metrics, and findings. | Repository-wide inventory and classification baseline. | Canonical inventory baseline. | Inventory | Repository Certification Standard. | Semantic, architecture, documentation, style, accessibility, release, and certification audits. |
| [Semantic Certification Report](../audits/semantic-certification-report.md) | Records semantic, terminology, glossary, dependency-matrix, reachability, and canonical-home resolutions. | Semantic certification and terminology consistency. | Canonical semantic certification report. | Semantic certification | Repository Certification Standard and inventory audit. | Documentation, accessibility, and certification status. |
| [Canonical Vocabulary Index](../glossary/canonical-vocabulary-index.md) | Provides vocabulary discovery by reference to canonical definition locations. | Glossary/navigation layer only. | Canonical vocabulary index; not a definition source. | Semantic certification | Protected canonical definitions and semantic certification report. | Documentation, accessibility, and certification status. |
| [Repository Architecture Certification Report](../audits/repository-architecture-certification-report.md) | Records repository architecture policy, report-root policy, reference-document policy, navigation, and discoverability results. | Repository architecture and documentation placement policy. | Canonical architecture certification report. | Architecture certification | Inventory and semantic certification reports. | Documentation, release, and certification status. |
| [Documentation Standardization Report](../audits/documentation-standardization-report.md) | Records documentation structure, metadata, style, accessibility, and cross-document consistency results. | Major-document standardization and documentation navigation. | Canonical documentation standardization report. | Documentation standardization | Certification artifacts and repository domain registry. | Accessibility, release, cross-repository, and certification status. |
| [Repository Domain Registry](../architecture/repository-domain-registry.md) | Defines top-level repository domains, responsibilities, owners, roots, child domains, and allowed artifact classes. | Repository architectural registry. | Canonical domain registry. | Documentation standardization | Architecture certification report. | Repository architecture maintenance and certification status. |
| [Repository Certification Index](README.md) | Provides the canonical navigation hub for certification artifacts and certification continuity. | Repository Certification navigation. | Canonical certification index. | Documentation standardization; updated during enforcement | Certification artifacts. | Maintenance, certification status, and regression checks. |
| [Repository Compliance Enforcement Report](../audits/repository-compliance-enforcement-report.md) | Records compliance enforcement, automation coverage, regression prevention, and final finding dispositions. | Repository compliance enforcement. | Canonical compliance enforcement report. | Compliance enforcement | Certification artifacts, Certification Index, and Domain Registry. | Certification status and future regression checks. |
| [Independent Repository Certification Audit](../audits/independent-repository-certification-audit.md) | Independently verifies certification criteria, governance consistency, canonical source behavior, walkthrough discoverability, automation effectiveness, regression protection, and finding disposition. | Independent repository certification audit. | Canonical independent audit; not certification status. | Independent audit | Certification artifacts and certification automation. | Certification status. |
| [Repository Certification Status](repository-certification-status.md) | Records the repository certification decision, evidence matrix, integrity summary, automation summary, regression summary, residual exceptions, and maintenance readiness assessment. | Repository certification status. | Canonical repository certification status. | Certification status | Certification artifacts and validation results. | Future release reviews and maintenance. |

## Index Statistics

| Metric | Count |
|---|---:|
| Certification artifacts indexed | 11 |
| Certification areas represented | 8 |
| Governance artifacts | 1 |
| Audit/certification reports | 7 |
| Navigation/index artifacts | 3 |
| Protected mathematical artifacts changed by this index | 0 |

## Usage Rule

When certification or maintenance work needs context, start here, then follow the artifact-specific link. Do not copy canonical findings out of their source reports unless the copied text is explicitly marked as an excerpt or summary.
