# KA-001 — Knowledge Architecture

## Status

Proposed Knowledge Architecture

## Phase

Phase IIA — Epistemic Architecture

## Purpose

Define the missing epistemic layer of Project FAR: the layer that records what the repository claims to know, what supports those claims, what challenges them, and what depends on them.

This document does not create canonical claims.

It defines a proposed architecture for representing claims, evidence, counterexamples, open questions, and support relations.

## Layer Separation

Project FAR should distinguish at least five layers:

```text
Reality
  ↓
Ontology
  ↓
Representation
  ↓
Knowledge
  ↓
Repository
```

The Knowledge Layer is distinct from ontology, representation, and repository storage.

A claim is not the same as the file that records it.

Evidence is not the same as the investigation that produced it.

A repository artifact is not the same as the epistemic object it contains.

## Knowledge Objects

Candidate knowledge object kinds include:

- Claim;
- Hypothesis;
- Conjecture;
- Theorem;
- Evidence;
- Counterexample;
- Open Question;
- Dependency;
- Support Relation;
- Refutation Relation;
- Challenge;
- Research Debt Item.

These are epistemic objects.

They are not automatically canonical theory.

## Claim Object

A claim object should eventually record:

```yaml
claim_id:
statement:
status:
authority_level:
origin:
supporting_investigations:
supporting_audits:
supporting_evidence:
counterexamples_considered:
open_challenges:
depends_on:
supports:
last_reviewed:
```

## Evidence Object

An evidence object should eventually record:

```yaml
evidence_id:
produced_by:
supports:
strength:
limitations:
replications:
contradictions:
last_reviewed:
```

## Counterexample Object

A counterexample object should eventually record:

```yaml
counterexample_id:
target_claim:
status:
resolution:
impact:
source:
last_reviewed:
```

## Knowledge Graph

The Knowledge Layer should eventually form a directed graph.

Example edges:

- supports;
- challenges;
- refutes;
- depends_on;
- derived_from;
- weakens;
- strengthens;
- reopens;
- supersedes.

This graph answers questions such as:

- What supports this claim?
- What depends on this claim?
- What evidence challenges it?
- What investigations produced it?
- What would be affected if it fails?

## Distinction from Repository Artifacts

A repository file records knowledge objects but is not identical to them.

Example:

```text
Claim
  ↓ recorded in
Markdown file
  ↓ versioned by
Git commit
```

The claim, file, and commit are distinct.

## Initial Non-Goals

This architecture does not:

- populate claim files;
- assign final claim statuses;
- canonize any knowledge object;
- replace investigations or audits;
- implement automated graph tooling.

## Immediate Next Step

Do not create a large claims registry immediately.

First create a small pilot set of claims only from already-supported Phase II findings, such as:

- Representation is distinct from represented entity;
- Rule is distinct from execution;
- Investigation process is distinct from investigation record;
- Model is distinct from theory;
- Category collapse is an observed candidate failure mode.

The pilot should test whether claim objects improve traceability before a full registry is authorized.
