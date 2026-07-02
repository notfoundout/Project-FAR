# Discovery Artifact Profile Model

## Status

Research Architecture

## Purpose

This document defines the candidate artifact profile model for the Discovery Program.

The model exists to prevent Project FAR from collapsing independent dimensions such as artifact type, research state, logical status, repository role, authority level, and dependency role into one label.

## Core Rule

An artifact shall not be described by a single status label when multiple independent dimensions are relevant.

If two dimensions can vary independently, they shall be represented independently unless a dependency between them has been established.

## Artifact Profile

A complete artifact profile should eventually include:

```yaml
artifact_id:
title:
artifact_kind:
repository_path:
repository_role:
research_state:
logical_status:
authority_level:
scope:
target_object:
relation_type:
methodology_version:
dependencies:
dependents:
provenance_refs:
investigation_refs:
audit_refs:
open_objections:
revision_triggers:
last_reviewed:
```

## Dimension Meanings

### artifact_kind

What kind of artifact this is.

Examples:

- concept;
- definition;
- question;
- conjecture;
- lemma;
- theorem;
- proof;
- investigation;
- methodology rule;
- audit;
- architecture decision;
- framework component.

### repository_role

What role the artifact plays in the repository.

Examples:

- canonical theory;
- research;
- report;
- methodology;
- architecture;
- archive.

### research_state

Where the artifact sits in investigation.

Examples:

- observation;
- question;
- candidate;
- active investigation;
- residual candidate;
- provisionally stable;
- reopened;
- rejected;
- reduced;
- split;
- merged.

### logical_status

Whether the artifact has a logical truth or proof status.

Examples:

- not applicable;
- unproven;
- conjectural;
- proven under assumptions;
- refuted;
- inconsistent;
- undefined.

Definitions, questions, methodology rules, and repository decisions may have `not applicable` logical status.

### authority_level

The governance status of the artifact.

Examples:

- exploratory;
- research;
- provisionally stable;
- grounded;
- canonical;
- superseded;
- archived.

Authority level is not identical to truth, proof, or research maturity.

### relation_type

The relation asserted or studied by the artifact.

Examples:

- necessity;
- sufficiency;
- reduction;
- equivalence;
- dependence;
- replacement;
- contradiction;
- support;
- derivation;
- evaluation.

## Typed Relational Claims

Claims should be expanded into explicit relational form.

Example:

```yaml
claim: Distinction is necessary for explicit reasoning.
relation_type: necessity
candidate_condition: distinction
target_object: explicit reasoning process
scope: explicit inspectable reasoning systems
assumptions: []
methodology_version:
```

Unexpanded claims shall be treated as incomplete for foundational purposes.

## Current Use

This model is not yet implemented as registry metadata.

It should be used manually during artifact audits until the registry architecture is authorized and implemented.
