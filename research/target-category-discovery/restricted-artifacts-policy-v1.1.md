# Restricted Artifacts Policy v1.1

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Supersedes: unversioned policy recorded with protocol v1.2

## 1. Excluded material

Exact source registries, candidate logs, captured bytes, source-to-row mappings, packet edit logs, curator failure ledgers, validation identities, challenge packets, role identities, credentials, and access logs are excluded from derivator-readable repository paths.

## 2. Store requirements

The custodian store must provide deny-by-default permissions, encryption at rest and in transit, append-only access logging, version retention, backup/restore, revocation, and separate credentials for each role.

## 3. Commitment

Restricted content is committed only through `restricted-package-format-v1.0.md`. Aggregate ZIP hashes are insufficient. The public record exposes only package version, file count, canonical-manifest digest, Merkle root, declaration ID, and reveal conditions.

## 4. Reveal

A1 receives accepted blind packets only. A2 receives the curator ledger only after A1 freeze. Stage B receives frozen Stage A outputs and approved disclosed facts. Validation and challenge material remain sealed until their registered gates.

## 5. Gate

No restricted package is considered frozen until independent reproduction, restore, access-denial, revocation, and log-integrity tests pass in the sacrificial pilot.
