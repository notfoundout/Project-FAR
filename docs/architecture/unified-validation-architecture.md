# Project FAR Unified Validation Architecture

Status: implementation foundation / shadow-validation phase

## Purpose

Project FAR now requires a validation system that is faster and easier to repair without weakening research evidence, claim boundaries, or independent corroboration. The unified platform replaces duplicated orchestration with one manifest-driven engine while preserving the legacy suite during a measured shadow period.

The governing standard is:

> No required check may be silently omitted; no cached result may be reused without an implementation-and-input identity; no scientific negative result may be misclassified as infrastructure failure; and no claim, evidence gate, or W5 authorization may advance through status text alone.

## Implemented foundation

The initial implementation provides:

- one JSON validation manifest with stable check IDs;
- protected bootstrap, gate, claim-boundary, and W5 checks;
- manifest schema and dependency-cycle validation;
- profile-based execution;
- dependency-aware scheduling;
- deterministic parallel execution of independent checks;
- changed-file selection with full-profile fallback when coverage is uncertain;
- explicit selection explanations;
- content-addressed local caching;
- cache invalidation by manifest, command, runtime, declared input, and dependency hashes;
- isolated generator execution in a copied repository;
- generated-drift detection without modifying the source checkout;
- root-failure blocking of dependent checks;
- stable failure codes;
- structured run records, certificates, and failure bundles under `.far/`;
- exact reproduction commands;
- local diagnosis and doctor commands;
- an independent bootstrap verifier that does not import the main engine;
- unified-validation unit and integration tests;
- shadow GitHub Actions execution alongside the existing canonical workflows.

## Command surface

```bash
python tools/far.py doctor
python tools/far.py validate --profile pr-fast
python tools/far.py validate --profile pr-full
python tools/far.py validate --profile full
python tools/far.py validate --profile release
python tools/far.py validate --changed origin/main --explain
python tools/far.py validate governance.w5-authorization --no-cache
python tools/far.py diagnose
```

The equivalent module form is:

```bash
python -m far_validation validate --profile pr-fast
```

## Manifest authority

`validation/manifest.json` is the single source of validation topology. Each check records:

- stable ID and title;
- command or builtin implementation;
- REP, ADJ, governance, or repository ownership;
- severity and failure code;
- profile membership;
- declared inputs;
- dependencies;
- timeout;
- cache eligibility;
- sandbox and no-drift requirements;
- protected status.

Makefiles and workflows may invoke profiles, but they must not define parallel canonical checker lists after migration completes.

## Protected checks

The bootstrap lock currently protects:

- `bootstrap.manifest`;
- `selection.completeness`;
- `governance.research-gates`;
- `governance.claim-boundaries`;
- `governance.w5-authorization`.

Each protected check must remain critical and present in `pr-fast`, `pr-full`, `full`, and `release`. Removing or weakening one causes the independent bootstrap verifier to fail before the main engine runs.

## Profiles

### `pr-fast`

Runs the canonical tests and critical governance, W5, repository-hygiene, and Markdown checks. This is the default developer profile.

### `pr-full`

Adds the complete research checker set, link validation, and isolated generator-idempotence checks.

### `full`

Currently mirrors the complete registered suite. Future phases add property, adversarial, determinism, and platform checks.

### `release`

Currently executes all registered checks. Future phases disable cache for critical evidence checks and require attestations, mutation completion, and quarantine-free certification.

### `validator-change`

Runs whenever the validation engine, manifest, bootstrap layer, result schemas, protected checks, or validation workflow changes. It is designed to become the strongest non-release profile.

## Selection safety

Changed-file mode maps changed paths to declared check inputs, then includes dependencies and downstream affected checks. Global invalidation paths trigger the entire requested profile.

When any changed path lacks declared coverage, the engine records incomplete selection context and falls back to the complete requested profile. It never treats incomplete dependency knowledge as permission to skip work.

## Caching safety

Cache identity includes:

- engine version and implementation digest;
- Python version;
- manifest digest;
- check command or builtin identity;
- timeout and sandbox behavior;
- declared input paths and SHA-256 digests;
- dependency result fingerprints.

Only successful cacheable checks are stored. Generators are deliberately not cached. Release trust-domain separation and random cache-hit verification remain scheduled work.

## Generator safety

Legacy generators do not yet expose universal `--check` modes. The engine therefore executes registered generators in an isolated repository copy, snapshots files before and after, and fails when generated output differs. The original checkout remains unchanged.

The long-term target remains explicit `--check` and `--write` modes for every generator.

## Failure model

Each failure reports:

- stable failure code;
- check ID and title;
- status;
- command;
- summary;
- stdout and stderr;
- generated-drift file list when applicable;
- exact focused reproduction command;
- dependency failures.

Dependent checks are marked `blocked_by_root_failure` instead of being reported as independent defects.

Failure bundles are written to:

```text
.far/failures/<failure-code>-<check-id>/
```

Run records and certificates are written under `.far/runs/` and `.far/artifacts/validation/`.

## Scientific result semantics

The result model supports positive, negative, unresolved, blocked, inapplicable, validation-failure, and infrastructure-error states. A correctly preserved negative research result is not itself a failed CI run.

The current legacy checker commands primarily return pass/fail exit codes. Domain-native terminal scientific statuses will be introduced as individual checkers are converted into importable validation functions.

## Trust boundary

The independent bootstrap verifier is intentionally small and standard-library only. It verifies protected check identity, severity, profile membership, and manifest consistency before the main engine is trusted.

Future trust hardening includes:

- engine and oracle change governance;
- undeclared file, environment, clock, subprocess, and network dependency tracing;
- cache trust domains;
- test deletion and weakening detection;
- expected-result change audits;
- merge-tree certificate binding;
- hostile acceptance campaigns;
- signed or attested release certificates.

## Migration policy

The legacy Makefile targets and existing workflows remain authoritative during shadow validation. The new system must demonstrate parity across passing commits, historical failures, and intentional mutations before replacing the old orchestration.

Migration phases:

1. establish the manifest, engine, bootstrap, diagnostics, and shadow workflow;
2. measure runtime and parity;
3. convert checkers into reusable functions;
4. add typed immutable repository context;
5. add semantic change classification and undeclared-dependency tracing;
6. add mutation, property, adversarial, and determinism profiles;
7. add merge-tree and release certificate enforcement;
8. retire duplicated legacy command lists only after parity is established.

## Nonclaims

This initial implementation does not yet claim:

- formal verification of the engine;
- complete runtime capability confinement;
- independent oracle verification for every legacy checker;
- cross-runner cache attestation;
- merge-queue enforcement;
- complete mutation coverage;
- proof that every historical test is nonredundant;
- zero possibility of implementation error.

It establishes the executable foundation needed to implement and verify those controls incrementally without a flag-day replacement.
