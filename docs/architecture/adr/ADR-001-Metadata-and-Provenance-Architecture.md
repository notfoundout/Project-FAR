# ADR-001

## Title

Metadata and Provenance Architecture

## Status

Proposed

## Date

2026-07-01

## Context

Project FAR completed a repository review cycle that produced a Repository Assessment, Repository History, and Master Findings Matrix. That cycle identified unresolved metadata and provenance findings that require an architecture before implementation.

FAR-NF-009 exists because many repository artifacts lack explicit Charter-status metadata. The Repository Assessment records metadata maturity as incomplete and identifies missing explicit Charter-status metadata, multiple non-Charter status vocabularies, incomplete provenance-chain metadata, and insufficient separation between canonical location, repository role, maturity, and Charter status.

FAR-NF-011 exists because provenance-chain metadata is incomplete. Repository history records FAR-NF-011 as deferred after Cycle 1 because full execution requires provenance records that cannot be reconstructed without objective evidence or authority.

Metadata redesign became necessary because repository review showed that path, repository role, canonical location, Charter status, maturity, provenance, review history, promotion history, and archive history are distinct properties. They cannot be safely represented by one implicit convention without ambiguity.

Cycle 1 also established that research findings and human-review findings remained unchanged, while repository corrections resolved only bounded R1-R3 issues. Therefore, the metadata and provenance architecture must support future implementation without resolving research obligations, assigning Charter status, modifying theory, or changing research conclusions.

## Problem Statement

Project FAR requires a repository-wide metadata and provenance architecture capable of representing artifact identity, repository role, canonical designation, Charter status, maturity, dependency traceability, provenance, promotion history, archive history, review history, and execution history without conflating those dimensions.

The architectural problem is to design the smallest complete metadata system that supports auditability and traceability while avoiding theory changes, research-resolution changes, repository-wide metadata population, and duplication of Git functionality.

## Requirements

The metadata and provenance architecture shall support:

- stable artifact identity;
- current repository path;
- repository role;
- canonical designation;
- canonical scope where applicable;
- Charter status;
- maturity;
- dependency traceability;
- provenance references;
- finding references;
- review-cycle references;
- execution-cycle references;
- promotion history;
- demotion history;
- archive history;
- supersession history;
- replacement history;
- investigation origin;
- machine readability;
- human readability;
- auditability;
- minimality;
- status/category separation.

The architecture shall not:

- assign Charter status to artifacts;
- populate metadata;
- modify canonical theoretical content;
- resolve research obligations;
- decide primitive classifications;
- duplicate Git diffs;
- store theoretical truth values;
- infer unavailable provenance;
- infer human intent.

## Alternatives Considered

### 1. Inline Metadata Only

#### Advantages

- Keeps metadata near the artifact.
- Supports human readability when opening a file.
- Allows artifacts to carry their own identity.

#### Disadvantages

- Requires editing artifacts whenever mutable metadata changes.
- Risks touching canonical theory or research artifacts for repository-only metadata changes.
- Makes repository-wide metadata validation harder.
- Scales poorly for review history, promotion history, and provenance chains.
- Encourages conflation of artifact content with repository metadata.

#### Decision

Rejected as the sole architecture.

#### Justification

Inline metadata is justified for stable identity and registry linkage, but mutable metadata should not require editing theoretical or research content.

### 2. Central Registry Only

#### Advantages

- Centralizes repository-wide metadata.
- Supports machine readability.
- Avoids editing theory files for metadata updates.
- Supports validation of status, provenance, and dependency references.

#### Disadvantages

- Artifacts do not self-identify if moved or copied outside registry context.
- Registry/path drift is possible if artifact identity exists only outside the artifact.
- Human readers opening a file may not know its registry identity.

#### Decision

Rejected as the sole architecture.

#### Justification

A registry is necessary, but registry-only identity is weaker than a hybrid model because durable identity should survive path changes and direct artifact inspection.

### 3. Hybrid Architecture

#### Advantages

- Separates stable identity from mutable metadata.
- Allows artifacts to carry minimal identity while mutable metadata remains in a registry.
- Avoids unnecessary edits to theory and research content when metadata changes.
- Supports machine-readable validation.
- Supports human traceability.
- Supports provenance and review-cycle linkage.

#### Disadvantages

- Requires maintaining both inline identity and registry entries.
- Requires validation to prevent drift between artifact headers and registry records.
- Requires human authority before registry location and status vocabularies are finalized.

#### Decision

Accepted as the proposed architecture.

#### Justification

The hybrid architecture is the smallest complete model that supports durable identity, centralized metadata, provenance traceability, human readability, machine readability, and minimal theory disturbance.

### 4. Git-Only

#### Advantages

- Already records commits, diffs, file history, authorship, and timestamps.
- Requires no additional repository structure.
- Avoids duplicate storage of raw change history.

#### Disadvantages

- Does not encode Charter status.
- Does not encode repository role.
- Does not encode canonical designation.
- Does not encode maturity.
- Does not encode semantic provenance events such as promotion, demotion, archival, supersession, replacement, review cycle, or investigation origin.
- Does not directly connect findings to artifacts and review cycles.

#### Decision

Rejected.

#### Justification

Git is necessary but insufficient. The provenance model should reference Git commits rather than duplicate them, but Git alone cannot represent the required repository semantics.

### 5. Report-Only

#### Advantages

- Human-readable.
- Already aligned with repository assessment and execution history.
- Suitable for executive summaries and lifecycle narratives.

#### Disadvantages

- Narrative reports are not sufficiently machine-readable as the authoritative metadata store.
- Reports summarize state but should not define canonical theory or resolve research obligations.
- Reports are not ideal for enforcing artifact-level uniqueness, status, dependency, and provenance constraints.

#### Decision

Rejected.

#### Justification

Reports remain necessary for assessment and history, but metadata implementation requires a registry designed for validation and traceability.

## Decision

Adopt a proposed hybrid metadata and provenance architecture.

The architecture consists of:

1. minimal inline artifact identity;
2. a central artifact metadata registry;
3. a provenance event log;
4. a review-cycle index.

This ADR records the architectural decision only. It does not implement the architecture, create a registry, populate metadata, assign Charter status, or modify canonical theory.

## Architectural Principles

### Separation of Identity

Artifact identity shall be stable and independent of current path, title, maturity, status, or canonical designation.

### Separation of Repository Role

Repository role shall describe what function an artifact serves in the repository. It shall not determine Charter status or theoretical authority by itself.

### Separation of Charter Status

Charter status shall be recorded independently from repository role, path, maturity, and canonical designation.

### Separation of Canonical Designation

Canonical designation shall identify whether an artifact is canonical for a defined scope. It shall not by itself resolve theoretical truth or research obligations.

### Separation of Maturity

Maturity shall describe development or review maturity. It shall not assign Charter status.

### Separation of Provenance

Provenance shall record semantic repository events and references to commits, findings, reviews, and cycles. It shall not duplicate Git diffs.

## Metadata Model

The approved minimal artifact metadata model is:

```yaml
artifact_id:
path:
repository_role:
charter_status:
maturity:
canonical_designation:
canonical_scope:
dependencies:
provenance_ref:
review_refs:
```

### Field Meanings

- `artifact_id` — stable artifact identifier independent of path.
- `path` — current repository path.
- `repository_role` — repository function of the artifact.
- `charter_status` — Charter-status value or authorized status value.
- `maturity` — maturity value independent of Charter status.
- `canonical_designation` — canonical, non-canonical, historical, auxiliary, or unknown designation.
- `canonical_scope` — scope for which the artifact is canonical, where applicable.
- `dependencies` — declared artifact dependencies or an empty list.
- `provenance_ref` — reference to provenance event records.
- `review_refs` — references to review or execution cycles.

Fields derivable from path, Git, or artifact content shall not be stored as primary metadata.

## Provenance Model

The approved minimal provenance event model is:

```yaml
event_id:
event_type:
artifact_id:
finding_ids:
source_cycle:
commit:
review:
date:
summary:
```

### Event Types

The provenance model shall support these event types:

- `created`
- `modified`
- `promoted`
- `demoted`
- `archived`
- `superseded`
- `replaced`
- `reviewed`
- `executed`
- `investigation-origin`

### Provenance Rule

Git stores file history and diffs. Provenance stores semantic repository-event meaning and references the relevant Git commit.

## Registry Model

A central registry is recommended.

The registry shall contain artifact metadata records, provenance records, and review-cycle records.

### Single Large Registry Files

#### Advantages

- Simple to locate.
- Easy to inspect in one place.
- Easy to validate as a complete registry.
- Suitable for small initial adoption.

#### Disadvantages

- Large files may become difficult to review.
- Concurrent edits may conflict.
- Artifact-level changes are less isolated.

### One-Record-Per-File Registry

#### Advantages

- Isolates artifact records.
- Reduces merge conflicts.
- Supports artifact-level review.
- Scales better as repository size grows.

#### Disadvantages

- Requires directory organization.
- Requires tooling or convention to validate completeness.
- Harder to inspect the entire registry without aggregation.

### Registry Decision

Recommend one-record-per-file registry for artifact metadata, with index files for provenance and review cycles.

### Registry Justification

One-record-per-file artifact metadata is objectively superior for long-term maintainability because Project FAR has many artifacts and requires artifact-level metadata, provenance, and review history. Isolating artifact records reduces conflict risk and makes each metadata update reviewable without changing unrelated records.

Provenance and review-cycle records may be grouped by cycle or event log because they are naturally chronological and event-oriented.

Recommended conceptual layout:

```text
metadata/
  artifacts/
    <artifact-id>.yml
  provenance/
    <cycle-or-event>.yml
  reviews/
    <review-id>.yml
  indexes/
    artifacts.yml
    findings.yml
```

This is a recommendation only. It does not create the layout.

## Consequences

### Positive Consequences

- Separates artifact identity from mutable metadata.
- Prevents Charter status from being inferred from path or maturity.
- Prevents maturity from being confused with canonical status.
- Supports traceability from finding to investigation to artifact to commit to review to promotion or current artifact.
- Avoids duplicating Git diffs.
- Supports machine-readable validation.
- Preserves human-readable review history.
- Reduces need to edit canonical theory or research artifacts for metadata updates.

### Negative Consequences

- Requires a new registry system before metadata can be populated.
- Requires authority decisions before implementation.
- Requires validation to prevent registry drift.
- Requires conventions for artifact IDs and registry file naming.
- Requires maintenance discipline across future repository cycles.

### Migration Implications

- Registry location must be authorized before implementation.
- Artifact ID policy must be authorized before population.
- Charter-status vocabulary must be finalized or explicitly bounded before population.
- Historical provenance gaps must be represented without inference.
- Metadata population must proceed separately from this ADR.

### Maintenance Implications

- Future repository changes should reference artifact IDs and provenance events.
- Future execution cycles should update provenance and review-cycle records.
- Registry validation should check unique artifact IDs, valid paths, valid status values, valid provenance references, and valid review references.

### Audit Implications

- Audit can verify whether every artifact has a registry record.
- Audit can verify whether every provenance reference resolves.
- Audit can verify whether every finding-driven change links to a finding and commit.
- Audit can distinguish repository metadata from theory content and research conclusions.

## Deferred Decisions

The following decisions remain deferred pending human authority:

- final registry location;
- final artifact ID format;
- whether every artifact must carry inline identity metadata;
- final Charter-status vocabulary;
- whether Candidate, Canonical, Deprecated, Archived, and Superseded are statuses, lifecycle states, maturity values, or canonical-designation values;
- controlled maturity vocabulary;
- dependency declaration requirements by artifact class;
- handling of missing historical provenance;
- review-cycle authority for metadata changes;
- promotion authority;
- archive and supersession authority;
- whether registry validation is manual, scripted, or CI-enforced.

## References

- Repository Assessment: `reports/repository-assessment.md`
- Repository History: `reports/repository-history.md`
- Master Findings Matrix: summarized in `reports/repository-assessment.md`
- Metadata and Provenance Architecture: architectural design input for this ADR
