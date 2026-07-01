# Discovery Registry and Knowledge Graph Architecture

## Status

Proposed Architecture

## Purpose

This document codifies the long-term architecture for separating Project FAR's framework specification from its grounding discovery program.

It does not implement the registry.

It does not populate metadata.

It does not promote any theoretical result.

It defines the target architecture for making every concept, theorem, methodology rule, audit, decision, and framework component traceable from origin through validation to current authority.

## Core Separation

Project FAR shall distinguish two parallel products:

```text
Project FAR
  ├── Current Framework
  └── Discovery Program
```

The Current Framework is the usable version of FAR, FARA, FARO, and associated definitions.

The Discovery Program is the grounding research process that tests whether those concepts are derived, reduced, replaced, split, merged, rejected, or provisionally stabilized.

The Current Framework may be useful before it is fully grounded.

The Discovery Program determines what grounding status each framework element actually has.

## Authority Principle

Framework usefulness does not imply foundational grounding.

Discovery status does not automatically imply repository canonization.

Evaluation and governance remain separate.

A result may be strong under the Discovery Program while still awaiting a separate decision before becoming canonical repository doctrine.

## Discovery Program

The Discovery Program exists to derive, test, reduce, and audit the foundations of Project FAR.

Its valid research outcomes include:

- rejected;
- reduced;
- merged;
- split;
- replaced;
- residual candidate;
- provisionally stable;
- reopened;
- open.

Discovery does not use `accepted` as a primary research state.

Acceptance is a governance action.

Discovery records evidence, constraints, reductions, counterexamples, dependencies, and current stability.

## Framework Layer

The Framework Layer exists for users and implementation.

It records the current operational version of Project FAR.

Every major framework component should eventually link back to:

- the investigation that produced or justified it;
- its grounding status;
- its dependency chain;
- its known objections;
- its authority level;
- its last audit.

## Foundation Registry

Project FAR should eventually maintain a Foundation Registry.

Each concept should receive a record containing at minimum:

```yaml
artifact_id:
artifact_kind: concept
name:
current_status:
authority_level:
grounding_investigations:
reducibility_status:
necessity_status:
sufficiency_status:
replaceability_status:
dependencies:
counterexamples:
open_objections:
methodology_version:
last_audit:
```

The registry is the traceability source.

Definition files are human-readable views over registry-backed artifacts.

## Theorem Registry

Each theorem, lemma, conjecture, or proposition should eventually receive a record containing at minimum:

```yaml
artifact_id:
artifact_kind: theorem | lemma | conjecture | proposition
statement:
logical_status:
research_state:
authority_level:
scope:
assumptions:
definitions_used:
dependencies:
proof_refs:
counterexamples:
open_challenges:
methodology_version:
last_audit:
```

Theorem status and research state shall remain separate.

A theorem may be valid under assumptions while still being reopened for scope, dependency, or methodology reasons.

## Methodology Registry

Every methodology rule should eventually receive a record containing at minimum:

```yaml
artifact_id:
artifact_kind: methodology_rule
rule:
purpose:
problem_addressed:
enables:
evidence:
known_failures:
competing_rules:
affected_investigations:
authority_level:
last_audit:
```

Methodology rules must justify themselves.

They are not immune from reduction, replacement, or revision.

## Audit Registry

Each audit should record:

```yaml
artifact_id:
artifact_kind: audit
audited_artifact:
audit_question:
methodology_used:
findings:
recommendations:
affected_artifacts:
authority_implications:
follow_up_required:
```

Audits do not automatically revise artifacts.

They expose defects and recommend downstream actions.

## Knowledge Graph

The long-term repository model is an auditable knowledge graph.

Nodes are artifacts.

Edges are typed relations.

Examples of node kinds:

- concept;
- definition;
- question;
- investigation;
- proof;
- theorem;
- methodology rule;
- audit;
- ADR;
- framework component;
- repository decision.

Examples of edge kinds:

- depends_on;
- derived_from;
- reduced_to;
- replaced_by;
- refutes;
- supports;
- audits;
- implements;
- supersedes;
- constrains;
- evaluates;
- canonized_by;
- reopened_by.

No major artifact should remain outside the graph long term.

## Artifact Profiles

Every artifact should eventually be represented by an artifact profile rather than a single label.

Independent dimensions should remain separate.

At minimum, profiles should distinguish:

- artifact ontology;
- research state;
- logical status;
- repository role;
- authority level;
- dependency role;
- scope;
- methodology version;
- provenance.

Composite labels may be used for readability only if their component dimensions remain auditable.

## Authority Levels

Authority levels should be separate from research states and logical statuses.

Candidate authority levels:

- exploratory;
- research;
- provisionally stable;
- grounded;
- canonical;
- superseded;
- archived.

These labels require future governance definition before registry implementation.

## Current Implication

The current repository should not immediately rewrite every definition.

Instead, it should:

1. preserve the current framework as the usable specification;
2. build the Discovery Program;
3. audit framework artifacts;
4. record grounding status;
5. revise canonical theory only when investigations justify revision.

## Non-Goals

This architecture does not:

- prove any FAR theorem;
- derive FARA;
- implement metadata records;
- assign final authority levels;
- replace existing definitions;
- populate a registry;
- create CI validation.

Those are later implementation phases.

## Governing Claim

Project FAR should become a living, self-auditing knowledge graph in which every significant statement can answer:

- why it exists;
- what produced it;
- what assumptions it depends on;
- what evidence or proof supports it;
- what could invalidate it;
- what authority level it currently has;
- what changed since the last revision.
