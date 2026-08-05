# Sacrificial Operational Pilot v1.0

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Evidence status: **operations-only; permanently excluded from the 36 cases and six challenges**

## 1. Purpose

Test the machinery of capture, hashing, deterministic restricted commitment, packet sanitation, access control, release, revocation, restore, and audit logging before any eligible study source is selected.

## 2. Fixtures

Use three synthetic fixtures created solely for this pilot:

- `SP-001`: mutable-text capture with a deliberate later source change;
- `SP-002`: multi-file package including Unicode path normalization and ordering checks;
- `SP-003`: blind-packet sanitation fixture containing target-bearing decoys and curator-known failures.

Fixture content, generator, and expected outcomes are frozen in the pilot package. None may later enter development, validation, challenge, comparison, or claim evidence.

## 3. Required operations

1. capture exact fixture bytes;
2. build canonical restricted commitment;
3. reproduce commitment independently;
4. create a blind A1 packet excluding curator-known failures;
5. run lexical, structural, inferential, and unequal-detail leakage checks;
6. release only the accepted packet to an isolated workspace;
7. demonstrate denied access to restricted identities;
8. log every access and reveal;
9. revoke the workspace credential;
10. restore the package from backup and reproduce the root;
11. mutate one byte, one path, one manifest entry, and one role grant and confirm detection.

## 4. Pass rule

All required operations and negative controls pass; two independently produced package roots match; no restricted identity is visible to the A1 workspace; revocation and restore succeed; every event is present in the append-only log.

Any failure blocks the 36-case source freeze. A correction requires pilot v1.1 and retains the failed v1.0 record.

## 5. Current status

Protocol registered. Pilot not executed because restricted storage, role assignments, and credentials are not yet instantiated.
