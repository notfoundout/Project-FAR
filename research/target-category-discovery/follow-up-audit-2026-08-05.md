# Follow-Up Audit: Target-Category Protocol Hardening v1.3

Status: **Research**  
Audit ID: `TCD-HARDENING-AUDIT-001`  
Program ID: `TCD-CLEANROOM-001`  
Audit date: 2026-08-05  
Execution status: **not authorized**

## 1. Audit question

Did protocol hardening v1.3 close the integrity, neutrality, adjudication, cost, source-selection, restricted-storage, validation-boundary, mutation-coverage, and role-separation defects identified after PRs #432 and #433?

## 2. Decision

**The identified protocol and repository-control defects are corrected at the public-control layer. The experiment remains operationally blocked.**

This distinction is mandatory:

- `control_corrected` means the governing rule, verifier, and negative test now exist;
- `operationally_instantiated` means real personnel, credentials, stores, sources, packets, and logs satisfy those rules.

The first is true. The second is false.

## 3. Corrected findings

### 3.1 Exact design and artifact freeze

The sampling verifier now enforces exact SHA-256 identities for the canonical covering array and pairwise report before semantic checks. `verify_program_freeze.py` verifies the exact bytes of every governed public control and test against `freeze-manifest-v1.0.json`.

A byte-only mutation that preserves CSV semantics is rejected. Manifest omission, reordering, duplication, invalid hashes, and governed-file mutation are separately tested.

Disposition: **corrected**.

### 3.2 Stage A curator priming

The primary A1 packet no longer contains curator-known failure scenarios. Those failures remain in a sealed curator ledger and may be disclosed only in a separate A2 completeness arm after A1 outputs are frozen. A2-only questions are labeled `curator_prompted` and excluded from primary convergence.

Disposition: **corrected**.

### 3.3 Adjudication discretion

`stage-a-adjudication-codebook-v1.0.md` fixes atomic splitting, equivalence, merge limits, objective linkage, recurrence, witness acceptance, singleton treatment, curator-prompted status, contamination, disagreement, two-adjudicator procedure, third-adjudicator limits, and required decision records.

Disposition: **corrected at protocol layer**. Operational adjudicators are not assigned.

### 3.4 Cost ambiguity

`stage-b-cost-instrument-v1.0.md` defines count, byte, time, memory, reviewer-burden, exception, hidden-state, interpreter, and ambiguity-policy coordinates; canonicalization; measurement replication; Unknown/NA handling; and coordinate-wise Pareto dominance. Unregistered scalar scores and post hoc weights are prohibited.

Disposition: **corrected at protocol layer**. No candidate has been measured.

### 3.5 Project-controlled source selection

`source-selection-and-replacement-protocol-v1.0.md` requires frozen source universes, exact queries/filters, retrieval windows, ordering, maximum inspection, stopping, complete pre-decision candidate logging, independent coding, deterministic matching, unfilled-row handling, and immutable replacement chains.

Disposition: **corrected at protocol layer**. Actual universes and queries are not instantiated.

### 3.6 Restricted-package reproducibility

`restricted-package-format-v1.0.md` and `restricted_package_commitment.py` define normalized relative paths, sorted entries, exact file hashes, canonical JSON, deterministic Merkle roots, symlink and hard-link rejection, path-collision detection, independent reproduction, and append-only access logging. ZIP identity is explicitly non-authoritative.

Disposition: **corrected and unit-tested**. No real restricted store exists.

### 3.7 Validation interpretation

`sampling-design-v1.2.md` explicitly classifies validation as profile-known and source-identity-hidden, with six public and six operational cases and no synthetic holdout. Claims of synthetic-class generalization, undisclosed-profile generalization, population representativeness, and universality are prohibited.

Disposition: **corrected**.

### 3.8 Mutation-test completeness

The sampling suite now tests exact byte identity, report identity, headers, row count, integer rows, blind IDs, target leakage, row order, ID uniqueness and mapping, allocation, level sets, missing pair coverage, validation source split, synthetic validation, report headers, report row count, duplicate report pairs, numeric mismatch, and incomplete coverage.

Freeze-manifest and restricted-package suites add omission, ordering, duplication, malformed hash, governed-file mutation, order independence, byte mutation, path mutation, symlink, hard-link, unsafe-path, and empty-package controls.

Disposition: **corrected for all implemented verification branches**.

### 3.9 Role separation

`role-access-conflict-matrix-v1.0.md` defines required roles, prohibited combinations, deny-by-default access classes, assignment evidence, signed conflict declarations, substitutes, revocation, and independent access-log audit.

Disposition: **corrected at protocol layer**. The matrix is intentionally `unassigned — execution blocked`.

### 3.10 Pre-study operational pilot

`sacrificial-operational-pilot-v1.0.md` defines three permanently excluded fixtures and tests capture, commitment reproduction, blind-packet sanitation, access denial, release, logging, revocation, restore, and negative mutations.

Disposition: **pilot specified but not executed** because the store, credentials, and role assignments do not exist.

## 4. Internal consistency audit

The hardened controls satisfy the following dependency order:

1. public controls and exact freeze;
2. operational role/store instantiation;
3. sacrificial pilot;
4. source-universe and query freeze;
5. candidate enumeration and deterministic matching;
6. source/synthetic byte freeze;
7. A1 packet sanitation and leakage audit;
8. A1 derivation;
9. A2 completeness arm;
10. fixed adjudication;
11. Stage B and frozen costing;
12. validation;
13. challenge;
14. architecture comparison.

No later stage is authorized to repair an earlier exposed stage in place.

## 5. Residual blockers

The following are not defects in v1.3; they are uninstantiated prerequisites:

- no independent role assignments or signed conflict declarations;
- no access-controlled restricted store;
- no pilot credentials, backup, or append-only audit log;
- no executed sacrificial pilot;
- no frozen source universes, queries, retrieval windows, or candidate logs;
- no selected or captured 36-case sources;
- no generated synthetic artifacts;
- no sanitized packets or leakage approvals;
- no derivation, adjudication, cost measurement, validation, or challenge result.

## 6. Claim boundary

This hardening establishes only that the public control package is internally specified, exact-byte frozen, and negative-tested.

It does not establish:

- a neutral requirement basis exists;
- the source-selection pools will be adequate;
- real role separation will be obtainable;
- the pilot will pass;
- RCCD is sufficient, necessary, minimal, or superior;
- the bounded class is independently optimal;
- held-out adequacy;
- external independence;
- universality or canonicality.

## 7. Final disposition

> **Protocol hardening v1.3 closes the identified public-control defects. Exact freeze and negative tests pass. Operational execution remains blocked until role/store instantiation and a successful sacrificial pilot.**
