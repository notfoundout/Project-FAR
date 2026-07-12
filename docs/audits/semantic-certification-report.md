# Semantic Certification Report

Status: semantic certification Semantic Certification
Protected Boundary: This report changes no primitives, canonical definitions, axioms, lemmas, propositions, theorems, accepted proof objects, accepted mathematical dependency metadata, accepted doctrine, or Foundation v1.0.

## Purpose
Resolve inventory semantic and terminology findings by assigning canonical homes, glossary references, semantic dependency structure, reachability status, and required dispositions.

## Why?
Repository certification requires one semantic purpose, one canonical name, one canonical definition location, and one canonical home per canonical concept before cleanup work proceeds.

## Scope
Semantic certification for repository governance, architecture, roadmap, dependency, planning, glossary, and vocabulary surfaces identified by inventory. This is not a theorem dependency audit and does not alter accepted mathematics.

## Role in Project FAR
This is the semantic certification canonical semantic certification report for the Repository Certification program.

## Dependencies
Depends on the Repository Certification Standard, inventory audit audit, canonical map, and canonical definitions document.

## Dependents
architecture certification documentation standardization, documentation standardization architecture/dependency audit, and later roadmap/release consistency work.

## Design Rationale
Findings are resolved by reference and classification rather than mathematical edits, preserving the protected boundary and one-canonical-source rule.

## Semantic Overlap Rule Applied
Semantic overlap is found only when one canonical concept may replace another in every valid interpretation without reducing expressive power. Dependency, derivability, composition, specialization, inheritance, and normal hierarchy are not treated as overlap.

## Semantic Certification Summary
- Canonical vocabulary entries: 96.
- Semantic dependency matrix rows: 96.
- Glossary entries resolving to exactly one canonical definition location: 96.
- Protected mathematical artifacts changed: 0.

## Disposition Counts
| Disposition | Count |
| --- | ---: |
| Canonical | 2 |
| Merge | 0 |
| Reference | 4 |
| Archive | 0 |
| Delete | 0 |
| Deferred | 2 |

## Semantic Overlap Resolutions
| ID | Subject | Semantic relation | Resolution | Disposition |
| --- | --- | --- | --- | --- |
| P3-SF-001 | Architecture descriptions | composition / normal hierarchy | docs/ARCHITECTURE.md is canonical repository architecture; `docs/architecture/` and framework/mechanization architecture docs are scoped references or specializations. | Reference |
| P3-SF-002 | Roadmap and planning descriptions | composition / specialization | docs/ROADMAP.md is canonical project roadmap; `docs/roadmap/`, `docs/planning/`, and release roadmaps are scoped plans or historical/release-specific references. | Reference |
| P3-SF-003 | Dependency descriptions | normal hierarchy | `theory/dependencies/dependency-registry.yaml` is canonical accepted theorem dependency metadata; generated graphs/reports and framework dependency graphs are supporting scoped views, not semantic overlap. | Reference |
| P3-SF-004 | Governance descriptions | composition | `docs/governance/repository-certification-standard.md` governs repository certification; `docs/governance/research-execution-charter.md` governs automated research execution; issue/PR templates are supporting process artifacts. | Canonical |
| P3-SF-005 | Planning descriptions | specialization | `docs/planning/` supports operational planning while `docs/ROADMAP.md` remains canonical project roadmap. | Reference |
| P3-SF-006 | Report roots | ambiguity | `docs/reports/` and `docs/audits/` are certification/report homes under docs; root `reports/` remains historical/supporting until architecture certification work resolves root report policy. | Deferred |
| P3-SF-007 | Document standard sections | derivability / accessibility | Missing standard sections are documentation-structure issues, not semantic overlap; later documentation standardization work should add explanatory preambles without changing canonical math. | Deferred |
| P3-SF-008 | Canonical definitions and glossary | dependency | `theory/definitions/definitions.md` remains the canonical definition source; the new vocabulary index is a glossary/reference layer. | Canonical |

## Canonical Home Report
| Concept Area | Canonical Home | Other Locations Disposition | Justification |
| --- | --- | --- | --- |
| Repository architecture | `docs/ARCHITECTURE.md` | Architecture subdirectory and framework/mechanization architecture documents are scoped references/specializations. | Avoids duplicate repository-wide architecture canon while preserving scoped architecture documents. |
| Project roadmap | `docs/ROADMAP.md` | `docs/roadmap/`, `docs/planning/`, and release roadmaps are references, scoped operational plans, or release-specific records. | Separates canonical roadmap from execution planning and release history. |
| Accepted theorem dependency metadata | `theory/dependencies/dependency-registry.yaml` | Generated reports, graphs, and framework dependency graphs are supporting or scoped. | Preserves protected dependency metadata as canonical. |
| Repository certification governance | `docs/governance/repository-certification-standard.md` | This report and the inventory audit reference it. | certification standard established this as the standard. |
| Automated research execution governance | `docs/governance/research-execution-charter.md` | AGENTS.md delegates to it. | Existing governance remains authoritative for automated work. |
| Canonical definitions | `theory/definitions/definitions.md` | Vocabulary index references it without redefining terms. | Preserves canonical mathematical definitions unchanged. |

## Glossary Consistency Report
| Check | Result | Disposition |
| --- | --- | --- |
| Every indexed canonical concept appears in the glossary index | 96 entries present | Canonical |
| Every glossary term points to exactly one canonical definition location | 96 of 96 | Canonical |
| Duplicate glossary entries | None present in the index | Canonical |
| Conflicting glossary entries | None present; entries are references only | Canonical |
| Orphan glossary entries | None present; each row has a canonical home | Canonical |
| Undefined terminology | Deferred where framework audits already identify graph terminology gaps | Deferred |

## Concept Reachability Report
| Entry Point | Reachability Role | Result |
| --- | --- | --- |
| Root README | Repository entry point reaches docs and theory navigation. | Reference |
| Theory index | Reaches canonical theory concepts and definitions. | Reference |
| Glossary | `docs/glossary/canonical-vocabulary-index.md` points to one canonical definition location per concept. | Canonical |
| Architecture | `docs/ARCHITECTURE.md` remains the canonical repository architecture home. | Canonical |
| Navigation | `docs/CANONICAL_MAP.md` now includes the vocabulary index and semantic certification semantic report. | Canonical |

## Terminology Standardization Report
- Preferred capitalization is the canonical name listed in the vocabulary index.
- Acronyms remain limited to established project/mechanization abbreviations: FAR, FARA, FARE, FARO, CLI, IR, JSON, YAML, and PR.
- Explanatory documents may use aliases only when the canonical term is identified.
- Canonical mathematical definitions are not simplified or rewritten; accessibility is provided by reference and explanatory glossary entries.
- CLI, schema, tooling, documentation, and report terminology should reference the vocabulary index when naming shared concepts.

## Semantic Dependency Matrix
| Canonical Concept | Parent Concepts | Child Concepts | Required Concepts | Derived Concepts | Independent Concepts | Adjacent Concepts |
| --- | --- | --- | --- | --- | --- | --- |
| Object | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Property | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Relation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Structure | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Component | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| System | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Class | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Domain | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Model | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Framework | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Theory | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Architecture | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Project FAR; Canonical Vocabulary Index |
| Ontology | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Syntax | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Semantics | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Scope | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Universal | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Universal Architecture | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Minimal | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Candidate Primitive | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Established Primitive | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Derived Concept | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Reduction | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Independence | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Equivalence | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Expressive Power | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Represented Object | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representational Structure | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Interpretation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Semantic Content | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Structural Equivalence | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Semantic Equivalence | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representation Mapping | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representation Transformation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representation Invariance | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representation Fidelity | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representation Completeness | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representation Consistency | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Representational Independence | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Investigation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Investigation State | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Investigation Record | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Reasoning | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Reasoning Process | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Reasoning Calculus | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| State | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Reasoning State | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Reasoning State Representation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Reasoning State Record | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Transformation Rule | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Transformation Execution | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Transformation Result | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Transition Signature | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Reasoning Trace | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Candidate | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Criterion | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Classification | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Admissibility | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Admissibility Classification | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Admissibility Structure (Ω) | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Resolution Rule | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Resolution Execution | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Resolution | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Definition | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Principle | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Axiom | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Proposition | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Conjecture | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Lemma | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Theorem | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Corollary | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Proof | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Refutation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Claim | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Claim Type | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Evidence | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Observation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Assumption | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Hypothesis | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Explanation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Prediction | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Counterexample | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Artifact | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Audit | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Grounding Investigation | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Knowledge Object | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Traceability | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Revision | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Project FAR | None | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Repository Certification Standard | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Repository Certification Inventory Audit | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |
| Architecture | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Project FAR; Canonical Vocabulary Index |
| Roadmap | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Project FAR; Canonical Vocabulary Index |
| Dependency Registry | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Project FAR; Canonical Vocabulary Index |
| Research Execution Charter | Project FAR | None recorded in semantic certification matrix | Canonical definition location; Repository Certification Standard | None asserted by this audit | Independent status not asserted; evaluate in protected theory context if mathematical | Architecture; Roadmap; Dependency Registry |

## Updated Certification Findings
| ID | Finding | Class | Required Disposition |
| --- | --- | --- | --- |
| P3-SF-001 | Architecture descriptions: docs/ARCHITECTURE.md is canonical repository architecture; `docs/architecture/` and framework/mechanization architecture docs are scoped references or specializations. | Improvement Opportunity | Reference |
| P3-SF-002 | Roadmap and planning descriptions: docs/ROADMAP.md is canonical project roadmap; `docs/roadmap/`, `docs/planning/`, and release roadmaps are scoped plans or historical/release-specific references. | Improvement Opportunity | Reference |
| P3-SF-003 | Dependency descriptions: `theory/dependencies/dependency-registry.yaml` is canonical accepted theorem dependency metadata; generated graphs/reports and framework dependency graphs are supporting scoped views, not semantic overlap. | Improvement Opportunity | Reference |
| P3-SF-004 | Governance descriptions: `docs/governance/repository-certification-standard.md` governs repository certification; `docs/governance/research-execution-charter.md` governs automated research execution; issue/PR templates are supporting process artifacts. | Improvement Opportunity | Canonical |
| P3-SF-005 | Planning descriptions: `docs/planning/` supports operational planning while `docs/ROADMAP.md` remains canonical project roadmap. | Improvement Opportunity | Reference |
| P3-SF-006 | Report roots: `docs/reports/` and `docs/audits/` are certification/report homes under docs; root `reports/` remains historical/supporting until architecture certification work resolves root report policy. | Improvement Opportunity | Deferred |
| P3-SF-007 | Document standard sections: Missing standard sections are documentation-structure issues, not semantic overlap; later documentation standardization work should add explanatory preambles without changing canonical math. | Improvement Opportunity | Deferred |
| P3-SF-008 | Canonical definitions and glossary: `theory/definitions/definitions.md` remains the canonical definition source; the new vocabulary index is a glossary/reference layer. | Improvement Opportunity | Canonical |
