# Mechanization

## Purpose

This directory contains proof-assistant and formal-methods prototypes for Project FAR.

The first scaffold targets Lean because it is well suited for formal definitions, structures, and theorem statements.

## Current Status

The repository contains an executable `far-ir/1.0` storage/graph MVP and partial Lean scaffolding. Neither verifies the Project FAR Core Theory or certifies representation sufficiency.

## Current goals

1. Preserve `far-ir/1.0` compatibility without silently changing its meaning.
2. Formalize `FAR-CORE-001` through `FAR-CORE-004` first.
3. Implement the versioned contract/factorization requirements in `docs/mechanization/contract-relative-far-ir-v1.1-requirements.md`.
4. Add positive decoder and negative collision fixtures.
5. Distinguish determinate absence from epistemic Unknown when the contract requires it.
6. Report exactly which definitions and theorems are proof-assistant checked.

## Boundary

The current repository verifier checks structural and claim-state consistency. `far-ir/1.0` does not encode the complete comparison contract, decoder/factorization certificate, observational quotient, or cost order required to verify the core claims. Mechanization may raise assurance but is not a premise of theory closure.
