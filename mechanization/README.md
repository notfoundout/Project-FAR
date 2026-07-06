# Mechanization

## Purpose

This directory contains proof-assistant and formal-methods prototypes for Project FAR.

The first scaffold targets Lean because it is well suited for formal definitions, structures, and theorem statements.

## Current Status

Initial scaffold only. The Lean file does not yet prove the full Project FAR theorem catalog.

## Goals

1. Encode primitive sorts.
2. Encode FAR representations.
3. Encode well-formedness predicates.
4. Encode model satisfaction.
5. Port T-003 as the first mechanized theorem.
6. Gradually replace narrative Markdown proofs with proof-assistant-checked statements.

## Boundary

The current repository verifier checks structural consistency. Mechanization is the next layer: checking logical derivations themselves.
