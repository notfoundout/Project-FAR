# Bounded compare and adjudication interface v1.0 scope

Tracking issue: #368
Parent program: #364
Original audit ID: 2

## Purpose

Define one stable interface that compares two FAR evidence packages and records a separate adjudication without presenting either stage as a truth oracle.

## Required separation

The implementation must expose two distinct operations:

1. `compare`: deterministic mechanical comparison of two validated evidence packages.
2. `adjudicate`: explicit attachment of a human, policy, or domain judgment to a frozen comparison.

An adjudication must never rewrite the comparison, erase dissent, convert unknowns into facts, or conceal unsupported claims.

## Frozen v1.0 contract targets

The version 1.0 contract must define:

- canonical package references and SHA-256 identities;
- deterministic comparison identifiers;
- explicit matched, differing, missing, contradicted, unknown, stale, and unsupported fields;
- claim-boundary preservation;
- deterministic JSON serialization;
- fail-closed schema validation;
- immutable comparison records;
- separately signed or hashed adjudication records;
- preserved dissent and unresolved findings;
- compatibility and migration rules.

## Required implementation

Before merge, this PR must include:

- implementation module and command-line interface;
- versioned schemas;
- canonical examples and golden fixtures;
- deterministic round-trip tests;
- malformed-input and adversarial tests;
- mutation coverage for boundary weakening;
- documentation for consumers and maintainers;
- repository integration without introducing a second competing interface.

## Prohibited claims

This interface does not establish truth, correctness, universality, independent certification, commercial readiness, enterprise readiness, or automatic normative resolution.

## Merge gate

The PR may merge only after the full observable repository CI surface is green and the final diff demonstrates that comparison and adjudication remain separately auditable and fail closed.
