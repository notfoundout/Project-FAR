# Follow-Up Audit: Target-Category Protocol Hardening v1.3

Status: **Research**  
Audit ID: `TCD-HARDENING-AUDIT-001`  
Program ID: `TCD-CLEANROOM-001`  
Audit date: 2026-08-05

## Decision

The public protocol-control defects identified after PRs #432 and #433 are corrected and negative-tested. The experiment remains operationally uninstantiated and execution remains unauthorized.

## Corrected controls

1. **Exact freeze:** the covering array and report remain byte-identical; the public-control manifest locks every governed file by Git blob identity and CI verifies the working bytes against those identities.
2. **Prompt freeze:** `execution-prompts-v1.0.json` contains exact A1, A2, and B1 texts, IDs, and a normalization rule. The freeze verifier computes their normalized SHA-256 values, and every future run must record its prompt ID and computed digest.
3. **Stage A neutrality:** curator-known failures are excluded from A1 and disclosed only in a separately labeled A2 completeness arm after A1 freeze.
4. **Adjudication:** the fixed codebook defines splitting, equivalence, merging, recurrence, witness acceptance, disagreement, contamination, and status assignment.
5. **Costing:** the Stage B instrument defines units, canonicalization, measurement, `NA`/`Unknown`, replication, and coordinate-wise Pareto comparison. Unregistered scalar weights are prohibited.
6. **Source selection:** universes, queries, retrieval windows, ordering, stopping, complete pre-decision candidate logs, independent coding, deterministic matching, unfilled rows, and replacement chains must be frozen.
7. **Restricted commitments:** canonical paths, exact file hashes, canonical JSON, deterministic Merkle roots, symlink/hard-link rejection, reproduction, access logs, reveal, revocation, and restore are specified.
8. **Validation boundary:** validation is explicitly profile-known and source-identity-hidden; six public and six operational cases do not test synthetic holdout transfer or undisclosed profiles.
9. **Validation and challenge rules:** exact construction, freeze, execution, scoring, stopping, failure, and claim-impact rules are fixed before development exposure.
10. **Role separation:** required identities, conflicts, access classes, prohibited combinations, substitutions, revocation, and audit evidence are specified. Unassigned roles keep the gate closed.
11. **Sacrificial pilot:** three operations-only fixtures are permanently excluded from all study evidence and must test capture, commitments, sanitation, access denial, logging, revocation, restore, and mutation detection.
12. **Historical integrity:** the original `audit-manifest-v1.0.json` payload is preserved unchanged. The current audit authority is v1.1; history is not rewritten.

## Verification

The hardened package includes semantic sampling checks, exact repository-byte checks, prompt-registry checks, symlink rejection, deterministic restricted-package tests, and negative mutations for every implemented verification branch.

## Residual blockers

These are uninstantiated prerequisites, not unresolved public-protocol defects:

- named independent role assignments and signed conflict declarations;
- an access-controlled restricted store, credentials, backup, restore, revocation, and append-only audit log;
- successful execution and independent audit of the sacrificial pilot;
- frozen source universes, queries, candidate logs, codings, and deterministic matches;
- exact bytes for 24 real-source cases and 12 synthetic cases;
- accepted blind packets and leakage reviews;
- frozen validation and challenge packet contents and keys;
- any A1, A2, adjudication, B1, validation, or challenge result.

## Claim boundary

This audit establishes only that the public control package is internally specified, exact-byte governed, and negatively tested. It establishes no neutral requirement basis, RCCD adequacy, investigator independence, held-out success, universality, necessity, minimality, comparative superiority, or canonicality.

## Final disposition

> **Public protocol controls corrected and frozen; historical audit preserved; execution prompts and validation/challenge rules machine-verifiable; operational prerequisites absent; experiment not started and not authorized.**
