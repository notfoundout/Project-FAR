# Repository Certification Index

## Purpose

This index is the canonical navigation hub for the Repository Certification campaign.

## Why?

Repository Certification now spans governance, inventory, semantic certification, architecture certification, and documentation standardization artifacts. A single index prevents contributors from treating any one report as an isolated or competing source of certification authority.

## Scope

This index covers certification artifacts introduced during Prompts 1 through 5. It does not certify the repository, change accepted mathematics, or replace the final certification report.

## Role in Project FAR

This document connects Repository Certification governance, audit baselines, corrective reports, and readiness claims so later prompts can continue from the same branch and draft PR without recreating prior audits.

## Dependencies

- [Repository Certification Standard](../governance/repository-certification-standard.md)
- [Repository Certification Inventory Audit](../audits/repository-certification-inventory-audit.md)
- [Semantic Certification Report](../audits/semantic-certification-report.md)
- [Canonical Vocabulary Index](../glossary/canonical-vocabulary-index.md)
- [Repository Architecture Certification Report](../audits/repository-architecture-certification-report.md)
- [Documentation Standardization Report](../audits/documentation-standardization-report.md)
- [Repository Domain Registry](../architecture/repository-domain-registry.md)

## Dependents

- Prompt 6 style standardization.
- Prompt 7 accessibility layer.
- Prompt 8 final certification.
- Future repository-maintenance work that needs to find certification evidence.

## Design Rationale

The index is separate from the reports because it is navigational, not evidentiary. Each artifact retains its own canonical content while this document records how the artifacts relate.

## Certification Artifact Registry

| Artifact | Purpose | Scope | Canonical status | Prompt introduced | Dependencies | Dependents |
|---|---|---|---|---|---|---|
| [Repository Certification Standard](../governance/repository-certification-standard.md) | Defines certification governance, protected boundaries, criteria, and completion rules. | Repository Certification governance. | Canonical governance standard. | Prompt 1 | Research Execution Charter. | All certification prompts and final certification. |
| [Repository Certification Inventory Audit](../audits/repository-certification-inventory-audit.md) | Records the repository inventory baseline, classifications, metrics, and findings. | Repository-wide inventory and classification baseline. | Canonical Prompt 2 baseline. | Prompt 2 | Repository Certification Standard. | Semantic, architecture, documentation, style, accessibility, release, and final audits. |
| [Semantic Certification Report](../audits/semantic-certification-report.md) | Records semantic, terminology, glossary, dependency-matrix, reachability, and canonical-home resolutions. | Semantic certification and terminology consistency. | Canonical Prompt 3 report. | Prompt 3 | Prompt 1 standard and Prompt 2 inventory. | Documentation, style, accessibility, and final certification. |
| [Canonical Vocabulary Index](../glossary/canonical-vocabulary-index.md) | Provides vocabulary discovery by reference to canonical definition locations. | Glossary/navigation layer only. | Canonical vocabulary index; not a definition source. | Prompt 3 | Protected canonical definitions and semantic certification report. | Documentation, accessibility, and final certification. |
| [Repository Architecture Certification Report](../audits/repository-architecture-certification-report.md) | Records repository architecture policy, report-root policy, reference-document policy, navigation, and discoverability results. | Repository architecture and documentation placement policy. | Canonical Prompt 4 report. | Prompt 4 | Prompt 2 and Prompt 3 reports. | Documentation, style, accessibility, release, and final certification. |
| [Documentation Standardization Report](../audits/documentation-standardization-report.md) | Records Prompt 5 documentation structure, metadata, style, accessibility, and cross-document consistency results. | Major-document standardization and documentation navigation. | Canonical Prompt 5 report. | Prompt 5 | Prompts 1-4 artifacts and repository domain registry. | Style, accessibility, release, cross-repository, and final certification. |
| [Repository Domain Registry](../architecture/repository-domain-registry.md) | Defines top-level repository domains, responsibilities, owners, roots, child domains, and allowed artifact classes. | Repository architectural registry. | Canonical domain registry. | Prompt 5 | Prompt 4 architecture certification report. | Documentation, style, accessibility, repository architecture maintenance, and final certification. |

## Index Statistics

| Metric | Count |
|---|---:|
| Certification artifacts indexed | 7 |
| Prompts represented | 5 |
| Governance artifacts | 1 |
| Audit/certification reports | 4 |
| Navigation/index artifacts | 2 |
| Protected mathematical artifacts changed by this index | 0 |

## Usage Rule

When a later prompt needs certification context, start here, then follow the artifact-specific link. Do not copy canonical findings out of their source reports unless the copied text is explicitly marked as an excerpt or summary.
