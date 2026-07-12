# Repository Architecture Certification Report

Version: 1.0
Status: Frozen Canonical Architecture Policy

## Purpose

This report records the repository architecture policy for Project FAR.

## Why?

The inventory identified broad directory responsibilities and duplicate architectural/report locations; semantic certification identified report-root policy and document-section normalization. This report resolves architecture, canonical-home, report-root, reference-document, navigation, and discoverability policy without changing accepted mathematics.

## Scope

This report governs repository organization, documentation navigation, report roots, canonical locations, and reference-document behavior. It does not govern mathematical content or theorem dependency metadata.

The report-root policy and reference-document policy recorded here are frozen
at version 1.0. Future policy revisions require an explicit new version rather
than silent modification.

## Role in Project FAR

This is the canonical repository architecture certification artifact.

## Dependencies

- [Repository Certification Standard](../governance/repository-certification-standard.md)
- [Repository Certification Inventory Audit](repository-certification-inventory-audit.md)
- [Semantic Certification Report](semantic-certification-report.md)
- [Canonical Vocabulary Index](../glossary/canonical-vocabulary-index.md)
- [Repository architecture](../ARCHITECTURE.md)
- [Canonical map](../CANONICAL_MAP.md)

## Dependents

- Repository Certification Status.
- Repository Certification Status.
- Future documentation, style, accessibility, release, and cross-repository consistency audits.

## Design Rationale

The repository architecture should reveal Project FAR's conceptual ownership without requiring historical knowledge. The architecture certification resolves policy and navigation first, avoids protected mathematical edits, and records deferred physical moves only when moving files would be cleanup rather than architectural certification.

## Protected Boundary Confirmation

Architecture certification did not modify primitives, canonical definitions, axioms, lemmas, propositions, theorems, accepted proof objects, accepted mathematical dependency metadata, accepted doctrine, or Foundation v1.0. Any future architecture change requiring such a modification is a Certification Failure and must be reclassified as Foundation Revision, Theory Revision, or Research Investigation.

## Architecture Certification Summary

| Item | Result |
|---|---|
| Total tracked artifacts after architecture certification | 992 |
| Top-level repository domains | 18 |
| Top-level domains with documented responsibility | 18 |
| Canonical report root | `docs/reports/` |
| Certification/audit report root | `docs/audits/` |
| Historical repository-assessment report root | `reports/` as transitional reference root |
| Files moved | 0 |
| Protected artifacts changed | 0 |
| New canonical architecture certification artifact | This report |

## Canonical Repository Architecture Map

Project FAR is organized by conceptual responsibility:

```text
Repository
├── Project command and automation
│   ├── README.md, metadata, package files, CI, and repository health entry points
│   └── tools/ and tests/ for validation and enforcement
├── Accepted foundation and theory
│   ├── foundations/ for Foundation v1.0 and foundation discovery records
│   └── theory/ for accepted mathematical theory artifacts and verification metadata
├── Framework and mechanization layers
│   ├── frameworks/ for FAR, FARA, FARE, FARM, and FARO framework documentation
│   ├── mechanization/ for implementation packages
│   ├── schemas/ and jsonschema/ for machine-readable schemas
│   └── conformance/ for schema and IR conformance fixtures
├── Documentation, governance, and reports
│   ├── docs/ for canonical repository documentation and navigation
│   ├── docs/governance/ for repository governance
│   ├── docs/audits/ for certification and audit reports
│   ├── docs/reports/ for canonical active validation, generated, release, and research reports
│   └── docs/glossary/ for vocabulary and terminology navigation
├── Examples and assets
│   ├── examples/ for runnable or explanatory examples
│   └── assets/ for supporting static assets
└── Non-canonical historical or exploratory material
    ├── research/ for exploratory investigations and provisional work
    ├── methodology/ for supporting methodology material
    ├── papers/ for manuscript material
    ├── archive/ for superseded historical material
    └── reports/ for legacy repository-assessment references pending later migration
```

## Directory Responsibility Report

Every listed directory has one primary responsibility. Nested directories inherit their parent domain unless a narrower responsibility is stated.

| Directory | Primary responsibility | Canonical status |
|---|---|---|
| `.github/` | CI, issue templates, and GitHub automation configuration. | Supporting |
| `archive/` | Historical superseded material that must not masquerade as current canonical content. | Archive |
| `assets/` | Static supporting assets used by documentation or examples. | Supporting |
| `conformance/` | FAR IR conformance fixtures and expected validation outcomes. | Supporting |
| `docs/` | Canonical repository documentation, navigation, governance, audits, and reports. | Canonical documentation root |
| `docs/architecture/` | Architecture decision records and scoped architecture support material. | Supporting reference |
| `docs/audits/` | Repository, certification, and consistency audit reports. | Canonical audit root |
| `docs/doctrine/` | Accepted doctrine documents that are not mathematical theorem artifacts. | Canonical doctrine root |
| `docs/glossary/` | Vocabulary, terminology, and glossary navigation by reference. | Canonical glossary root |
| `docs/governance/` | Repository governance and execution charters. | Canonical governance root |
| `docs/maintenance/` | Maintainer procedures and health-check instructions. | Supporting |
| `docs/mechanization/` | Documentation for mechanization architecture and use. | Supporting reference |
| `docs/methodology/` | Documentation of project methodology. | Supporting/reference |
| `docs/milestones/` | Milestone records. | Supporting |
| `docs/planning/` | Active planning and next-action documents. | Supporting planning root |
| `docs/principles/` | Project principles and explanatory principle documents. | Supporting/reference |
| `docs/releases/` | Release notes and release-specific documentation. | Canonical release root |
| `docs/reports/` | Canonical active report root for validation, generated, audit-output, release, and research reports. | Canonical report root |
| `docs/roadmap/` | Roadmap support views that reference `docs/ROADMAP.md`. | Supporting reference |
| `examples/` | Examples demonstrating FAR, mechanization, and related usage. | Supporting |
| `foundations/` | Foundation v1.0 and foundation discovery artifacts. | Protected canonical domain |
| `frameworks/` | Framework-layer documentation for FAR, FARA, FARE, FARM, and FARO. | Canonical framework root |
| `jsonschema/` | External JSON Schema packaging compatibility location. | Supporting/generated-facing |
| `mechanization/` | Mechanization implementation packages. | Canonical mechanization root |
| `methodology/` | Methodology support material and validation methods. | Supporting/reference |
| `papers/` | Manuscript and paper-oriented material. | Supporting |
| `reports/` | Legacy repository-level assessment reports; reference root, not the active canonical report root. | Transitional reference |
| `research/` | Exploratory and provisional research work. | Research/supporting |
| `schemas/` | Project schema definitions. | Canonical schema root |
| `tests/` | Automated test, fixture, regression, and simulation material. | Supporting test root |
| `theory/` | Accepted theory, definitions, axioms, theorems, proofs, verification, and dependency metadata. | Protected canonical domain |
| `tools/` | Repository tooling, validators, planners, generators, and automation scripts. | Supporting tooling root |

## Canonical Location Report

| Finding from inventory and semantic certification phases | Disposition | Canonical location | Non-canonical treatment |
|---|---|---|---|
| Duplicate architecture descriptions | Reference | `docs/ARCHITECTURE.md` and this architecture certification report for certification-specific architecture policy | Scoped architecture files remain references/specializations and must not redefine repository-wide architecture. |
| Duplicate roadmap locations | Reference | `docs/ROADMAP.md` | `docs/roadmap/`, `docs/planning/`, generated status, and release roadmaps are scoped planning/reference views. |
| Duplicate planning locations | Reference | `docs/planning/README.md` for planning navigation; `docs/ROADMAP.md` for project roadmap | Planning documents must link to roadmap/status sources rather than duplicate canonical roadmap claims. |
| Duplicate governance locations | Canonical | `docs/governance/` | Governance references elsewhere must point to `docs/governance/` and not restate rules except as excerpts or explanations. |
| Duplicate dependency descriptions | Reference | `theory/dependencies/dependency-registry.yaml` for accepted mathematical dependency metadata | Reports, graphs, and framework dependency maps are generated, scoped, or explanatory views. |
| Duplicate report locations | Reference | `docs/reports/` for active reports; `docs/audits/` for certification/audit reports | Root `reports/` is transitional legacy reference material. |

## Report Root Policy

1. `docs/reports/` is the canonical root for active Project FAR reports, including validation reports, generated status reports, release-readiness reports, health reports, external-validation reports, and appendices.
2. `docs/audits/` is the canonical root for repository-certification, architecture, semantic, inventory, framework-normalization, and similar audit reports.
3. `reports/` is a legacy transitional reference root for repository-level historical assessment documents. It may remain while historically valuable, but new active reports must not be added there.
4. `archive/` is the canonical root for superseded material that is no longer current and should not be treated as active guidance.
5. Generated report artifacts may live under `docs/reports/` only when the path is documented as generated or generated-facing.
6. Moving historical reports is deferred unless a later cleanup work determines that movement improves coherence without losing history or breaking references.

## Reference Document Policy

Reference documents may intentionally overlap in subject matter only when they satisfy all of the following:

- They point to the canonical source.
- They identify their limited scope.
- They do not redefine canonical content.
- They do not introduce competing terminology.
- They do not duplicate canonical information except for short orientation summaries.
- They state whether their role is explanatory, scoped, generated, historical, or transitional.

Violation of this policy is an Improvement Opportunity unless it creates conflicting canonical claims, in which case it is a Certification Failure.

## Repository Navigation Report

Navigation was updated so a new contributor can discover Foundation, Theory, Mechanization, Governance, Roadmap, Glossary, Certification, reports, and architecture from `README.md`, `docs/README.md`, and `docs/CANONICAL_MAP.md` without repository search.

| Entry point | Navigation responsibility | architecture certification result |
|---|---|---|
| `README.md` | Canonical command center. | Added certification and architecture navigation. |
| `docs/README.md` | Documentation index. | Added architecture certification report. |
| `docs/CANONICAL_MAP.md` | Canonical concept-location map. | Added architecture certification canonical architecture/report policy entry. |
| `docs/ARCHITECTURE.md` | Repository-wide architecture. | Remains canonical architecture description; this report references it. |
| `docs/glossary/canonical-vocabulary-index.md` | Vocabulary discovery. | Remains reachable from documentation index and canonical map. |

## Repository Discoverability Report

| Domain | Primary route from root README | Discoverability result |
|---|---|---|
| Foundation | `README.md` to `foundations/README.md` | Preserved |
| Theory | `README.md` to `theory/README.md` | Preserved |
| Mechanization | `README.md` to `mechanization/` and documentation links | Improved through architecture/certification navigation |
| Governance | `README.md` to `docs/governance/` and `docs/CANONICAL_MAP.md` | Improved |
| Roadmap | `README.md` to `docs/ROADMAP.md` | Preserved |
| Glossary | `README.md` and `docs/README.md` to `docs/glossary/canonical-vocabulary-index.md` | Improved |
| Certification | `README.md`, `docs/README.md`, and `docs/CANONICAL_MAP.md` to certification reports | Improved |
| Reports | `README.md` and this policy distinguish `docs/reports/`, `docs/audits/`, and `reports/` | Improved |

## Artifact Placement Audit

| Placement issue | Disposition | Action in architecture certification |
|---|---|---|
| Active reports split across `docs/reports/`, `docs/audits/`, and `reports/` | Reference | Policy resolves roots; no file move required for certification. |
| Architecture support files under `docs/architecture/` while repository architecture lives at `docs/ARCHITECTURE.md` | Reference | Scoped architecture support remains reference material. |
| Roadmap/planning material split across `docs/ROADMAP.md`, `docs/roadmap/`, and `docs/planning/` | Reference | Canonical roadmap retained; scoped planning remains reference material. |
| Generated reports beside active reports | Reference | Allowed only when generated-facing role is documented. |
| Examples separate from implementation | Canonical | `examples/` remains canonical example root; implementation stays in `mechanization/`. |

## Repository Minimality Decisions

No directory was deleted or physically reorganized in architecture certification because the unresolved architectural problem was ambiguous canonical policy, not proven duplicate content requiring removal. The minimal certification action is to document canonical roots and reference behavior, then defer physical moves to cleanup works only when evidence shows movement improves coherence without losing history.

## Concept Reachability Preservation

architecture certification did not rename or move canonical concepts. Reachability from README, documentation index, canonical map, architecture documentation, and glossary is preserved. Certification and architecture-policy reachability is improved by adding direct links from root and documentation navigation.

## Certification Findings Update

| Finding | Class | Disposition | Status after architecture certification |
|---|---|---|---|
| Report-root ambiguity | Certification Failure | Reference | Resolved by report-root policy. |
| Duplicate architecture descriptions | Improvement Opportunity | Reference | Resolved by canonical architecture/reference policy. |
| Duplicate roadmap/planning descriptions | Improvement Opportunity | Reference | Resolved by canonical roadmap/planning reference policy. |
| Duplicate governance descriptions | Improvement Opportunity | Canonical | Resolved: `docs/governance/` is canonical governance root. |
| Duplicate dependency descriptions | Improvement Opportunity | Reference | Resolved: accepted mathematical dependency metadata remains in `theory/dependencies/dependency-registry.yaml`. |
| Root `reports/` legacy location | Improvement Opportunity | Reference | Resolved as transitional reference root; later movement may be considered. |
| Missing standard document sections in existing documents | Improvement Opportunity | Deferred | Remains deferred to documentation standardization documentation standardization. |

## documentation standardization Completion Status

architecture certification is complete when this report, repository navigation, and canonical map updates are committed and validation passes or records only pre-existing warnings. documentation standardization is ready to proceed after review because repository architecture policy is resolved without protected mathematical changes.
