# Repository Domain Registry

Version: 1.0
Status: Frozen Canonical Registry

## Purpose

This registry defines the authoritative top-level repository domains for Project FAR.

## Why?

Architecture certification resolved repository architecture policy. Documentation standardization requires an architectural registry so documentation, tooling, audits, examples, reports, and future cleanup work use the same domain names, responsibilities, canonical roots, and allowed artifact classes.

## Scope

This registry covers top-level repository domains and major documentation child domains. It does not modify the content of any domain and does not change mathematical meaning.

Version 1.0 is frozen. Future domain-registry revisions require an explicit
new version rather than silent modification.

## Role in Project FAR

The registry is the canonical architectural reference for repository-domain ownership and allowed artifact placement.

## Dependencies

- [Repository Certification Standard](../governance/repository-certification-standard.md)
- [Repository Architecture Certification Report](../audits/repository-architecture-certification-report.md)
- [Repository Certification Inventory Audit](../audits/repository-certification-inventory-audit.md)

## Dependents

- Documentation Standardization Report.
- Repository Certification Status.
- Future repository maintenance, release consistency, and cross-repository consistency work.

## Design Rationale

The registry records observed repository domains rather than imposing a new structure. It chooses explicit responsibility statements over physical reorganization because architecture certification found policy ambiguity, not a protected-content requirement to move files.

## Domain Registry Statistics

| Metric | Count |
|---|---:|
| Top-level domains registered | 18 |
| Documentation child domains registered | 15 |
| Domains with one documented responsibility | 33 |
| Domains whose canonical root equals their filesystem root | 33 |
| Protected mathematical domains | 2 |

## Top-Level Repository Domains

| Name | Purpose | Responsibility | Canonical owner | Canonical root | Parent domain | Child domains | Allowed artifact classes |
|---|---|---|---|---|---|---|---|
| GitHub Automation | Host repository automation and templates. | CI workflows, issue templates, and GitHub integration. | Maintainers | `.github/` | Repository | `ISSUE_TEMPLATE`, `workflows` | Tooling, Test, Governance |
| Archive | Preserve superseded or historical material. | Historical storage that must not compete with canonical content. | Maintainers | `archive/` | Repository | `meta-theory`, `superseded` | Archive, Governance, Report |
| Assets | Store static support assets. | Non-canonical static assets for documentation or examples. | Documentation maintainers | `assets/` | Repository | None currently material | Example, Generated, Report |
| Conformance | Store FAR IR conformance fixtures. | Versioned valid/invalid/expected conformance material. | Mechanization maintainers | `conformance/` | Repository | `far-ir-1.0` | Test, Example, Mechanization |
| Documentation | Provide canonical navigation, governance, reports, and explanatory documentation. | Repository documentation and certification navigation. | Documentation maintainers | `docs/` | Repository | See documentation child-domain table. | Governance, Report, Specification, Release, Example |
| Examples | Demonstrate FAR and mechanization usage. | Human-readable and executable examples. | Documentation and mechanization maintainers | `examples/` | Repository | `far`, `mechanization` | Example, Test |
| Foundations | Preserve Foundation v1.0 and foundation discovery artifacts. | Protected foundation material. | Foundation maintainers | `foundations/` | Repository | `assumptions`, `discovery`, `investigations`, `meta`, `motivation`, `primitives`, `representations` | Foundation, Governance, Report |
| Frameworks | Host FAR-family framework-layer documentation. | FAR, FARA, FARE, FARM, and FARO framework material. | Framework maintainers | `frameworks/` | Repository | `FAR`, `FARA`, `FARE`, `FARM`, `FARO` | Theory, Specification, Governance, Report |
| JSON Schema Compatibility | Expose external JSON Schema packaging location. | Compatibility-facing schema material. | Mechanization maintainers | `jsonschema/` | Repository | None currently material | Specification, Generated, Mechanization |
| Mechanization | Implement mechanized FAR artifacts. | Code packages and mechanization support. | Mechanization maintainers | `mechanization/` | Repository | `far_mechanization`, `lean` | Mechanization, Tooling |
| Methodology | Store supporting methodology material. | Validation, falsification, proof, and comparison methodology support. | Methodology maintainers | `methodology/` | Repository | `comparison`, `falsification`, `proof-standard`, `validation` | Specification, Governance, Report |
| Papers | Store manuscript-oriented material. | Paper drafts and paper navigation. | Documentation maintainers | `papers/` | Repository | None currently material | Report, Example |
| Legacy Reports | Preserve legacy repository-level reports. | Transitional reference reports, not the active report root. | Documentation maintainers | `reports/` | Repository | None currently material | Report, Archive |
| Research | Store exploratory and provisional research. | Non-canonical investigations, notes, validation, and literature work. | Research maintainers | `research/` | Repository | `axiomatization`, `bibliography`, `comparisons`, `discovery`, `foundations`, `literature`, `methodology`, `notes`, `open-problems`, `proofs`, `validation` | Report, Specification, Theory, Example |
| Schemas | Store project schema definitions. | Canonical schema roots. | Mechanization maintainers | `schemas/` | Repository | None currently material | Specification, Mechanization |
| Tests | Store automated tests and fixtures. | Regression, fixture, counterexample, edge-case, mechanization, and simulation tests. | Tooling and mechanization maintainers | `tests/` | Repository | `counterexamples`, `edge-cases`, `fixtures`, `mechanization`, `regressions`, `simulations` | Test, Example |
| Theory | Preserve accepted mathematical theory artifacts. | Protected definitions, axioms, proofs, theorems, dependency metadata, verification, and examples. | Theory maintainers | `theory/` | Repository | `applications`, `audits`, `axioms`, `consistency`, `definitions`, `dependencies`, `derivations`, `evaluation`, `examples`, `falsification`, `formal-language`, `formal-semantics`, `language`, `lemmas`, `metadata`, `model-theory`, `notation`, `operators`, `proof-objects`, `proofs`, `semantics`, `tests`, `theorems`, `verification` | Theory, Test, Report, Specification |
| Tools | Store repository automation and validators. | Scripts, validators, planners, generators, and command-line maintenance tools. | Tooling maintainers | `tools/` | Repository | None currently material | Tooling, Test, Generated |

## Documentation Child Domains

| Name | Purpose | Responsibility | Canonical owner | Canonical root | Parent domain | Child domains | Allowed artifact classes |
|---|---|---|---|---|---|---|---|
| Architecture Documentation | Host architecture support and ADRs. | Scoped architecture records that reference canonical repository architecture. | Documentation maintainers | `docs/architecture/` | `docs/` | `adr` | Specification, Governance, Report |
| Audit Reports | Host certification and audit reports. | Repository certification, consistency, and audit evidence. | Documentation maintainers | `docs/audits/` | `docs/` | None currently material | Report, Governance |
| Certification Index | Host certification navigation. | Repository Certification artifact navigation. | Documentation maintainers | `docs/certification/` | `docs/` | None currently material | Governance, Report |
| Doctrine | Host accepted doctrine documents. | Non-mathematical doctrine documentation. | Governance maintainers | `docs/doctrine/` | `docs/` | None currently material | Governance, Specification |
| Glossary | Host vocabulary and terminology navigation. | Glossary/reference layer by canonical source. | Documentation maintainers | `docs/glossary/` | `docs/` | None currently material | Governance, Specification |
| Governance | Host governance and execution charters. | Repository governance standards and rules. | Governance maintainers | `docs/governance/` | `docs/` | None currently material | Governance |
| Maintenance | Host maintainer procedures. | Health checks and maintenance guidance. | Tooling maintainers | `docs/maintenance/` | `docs/` | None currently material | Tooling, Governance |
| Mechanization Documentation | Host mechanization documentation. | Explanatory documentation for mechanization architecture and use. | Mechanization maintainers | `docs/mechanization/` | `docs/` | None currently material | Mechanization, Specification |
| Methodology Documentation | Host methodology documentation. | Documentation for project methodology. | Methodology maintainers | `docs/methodology/` | `docs/` | None currently material | Governance, Specification |
| Milestones | Host milestone records. | Milestone tracking and historical project state. | Documentation maintainers | `docs/milestones/` | `docs/` | None currently material | Report, Release |
| Planning | Host active planning views. | Next actions and planning navigation. | Maintainers | `docs/planning/` | `docs/` | None currently material | Governance, Report |
| Principles | Host principle explanations. | Human-readable principle documents. | Documentation maintainers | `docs/principles/` | `docs/` | None currently material | Governance, Specification |
| Releases | Host release documentation. | Release notes and release records. | Release maintainers | `docs/releases/` | `docs/` | None currently material | Release, Report |
| Active Reports | Host active project reports. | Validation, generated, health, release, external-validation, and appendix reports. | Documentation maintainers | `docs/reports/` | `docs/` | `appendices`, `external-validation` | Report, Generated |
| Roadmap Support | Host scoped roadmap support views. | Roadmap support material that references `docs/ROADMAP.md`. | Maintainers | `docs/roadmap/` | `docs/` | None currently material | Governance, Report |

## Placement Rule

Artifacts should be placed in the domain whose responsibility names their primary purpose. If an artifact appears to fit multiple domains, prefer the domain containing its canonical source and convert other occurrences into references.
