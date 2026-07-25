# Bounded compare and adjudication interface v1.0 scope

Tracking issue: #368
Parent program: #364
Original audit ID: 2

## Purpose

Define one stable interface that compares two FAR evidence packages and records a separate adjudication without presenting either stage as a truth oracle.

## Required separation

The implementation exposes two distinct operations:

1. `compare`: deterministic mechanical comparison of two validated evidence packages.
2. `adjudicate`: explicit attachment of a human, policy, or domain judgment to a frozen comparison.

An adjudication cannot rewrite the comparison, erase dissent, convert unknowns into facts, or conceal unsupported claims.

## Frozen v1.0 contract

Version 1.0 defines:

- canonical package references and SHA-256 identities;
- oriented, deterministic comparison and finding identifiers;
- explicit agreement, contradiction, left-only, right-only, and unresolved findings;
- closed claim-status and adjudication-disposition vocabularies;
- claim-boundary preservation;
- deterministic canonical JSON serialization;
- fail-closed validation with unknown-field rejection;
- immutable comparison hashes;
- content-derived adjudication identifiers;
- preserved dissent, limitations, and unresolved findings;
- explicit compatibility and migration rules.

## Implemented

- `mechanization/far_mechanization/compare_adjudication.py`;
- `far-evidence` CLI with `validate-package`, `compare`, and `adjudicate` commands;
- three versioned JSON schemas;
- canonical left/right examples and an exact golden comparison fixture;
- deterministic ordering, hashing, orientation, and CLI round-trip tests;
- malformed-input and adversarial tests;
- registered package and adjudication mutation campaigns;
- consumer and maintainer documentation;
- one interface only, separate from the general FAR document CLI.

## Prohibited claims

This interface does not establish truth, correctness, universality, independent certification, commercial readiness, enterprise readiness, or automatic normative resolution.

## Merge gate

The PR may merge only after the full observable repository CI surface is green. Passing establishes conformance to the bounded v1.0 contract only.
