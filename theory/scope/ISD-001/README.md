# ISD-001 — Independent Scope Definition

## Status

Completed bounded scope definition. Scientific conclusion: **current demonstrated scope is narrow and explicit**.

## Purpose

ISD-001 separates what Project FAR has actually demonstrated from what it is designed or hypothesized to represent.

A design intention is not evidence of scope. A discussed example is not evidence of scope. A partially representable class is not included merely because some visible artifacts can be encoded.

## Current demonstrated scope

Project FAR currently has demonstrated representational scope for:

1. finite, explicit, rule-governed state-transition reasoning;
2. explicit rule modification where the modification point and later operational consequences are preserved;
3. finite machine-checkable reasoning traces generated from repository artifacts.

The strongest evidence is the deterministic CRE-001 reference system and its preservation artifacts.

## Inclusion rule

A reasoning-system class enters demonstrated scope only when:

- a representative benchmark is frozen before evaluation;
- source artifacts and observability limits are explicit;
- structural, semantic, operational, dependency, information, and historical preservation are all resolved;
- no required commitment is silently reconstructed through undeclared machinery;
- the result is reproducible from repository artifacts.

## Unresolved investigated classes

The following remain outside demonstrated scope:

- large-language-model reasoning;
- agentic AI reasoning;
- human expert reasoning;
- analogical reasoning.

Legal reasoning is classified as a conservative extension rather than core-only demonstrated scope because it requires explicit machinery for jurisdiction, authority hierarchy, defeasibility, standards, and time-indexed sources.

These classifications do not mean FAR cannot represent these domains. They mean the repository does not yet contain evidence sufficient to claim complete preserved representation of the class.

## Explicit exclusions

ISD-001 does not support claims that FAR currently covers:

- all human reasoning;
- all AI reasoning;
- inaccessible private internal states inferred only from behavior;
- continuous or unbounded processes lacking a finite preserved artifact;
- universal necessity;
- global minimality;
- unique optimality;
- universality.

## Scope expansion procedure

A later PR may expand demonstrated scope only by adding a frozen benchmark, explicit observability statement, preservation evaluation, unresolved-dimension handling, and domain-extension accounting.

Where the expanded class is used as evidence for necessity or universality, the PR must also compare alternative vocabularies rather than evaluate FAR alone.

## Decision

The current scope statement is deliberately narrower than Project FAR's research ambition.

The correct claim is:

> Project FAR has demonstrated preserved representation for a bounded family of finite, explicit, inspectable rule-governed reasoning systems, including systems that modify active rules and preserve the operational consequences of those modifications.

It has not yet demonstrated universal coverage of reasoning.

## Artifacts

- `scope-registry.json` — machine-readable included, unresolved, and excluded classes;
- `tests/test_independent_scope_definition.py` — deterministic scope and claim-boundary checks.
