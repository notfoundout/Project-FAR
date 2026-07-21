# Validator Assurance Hardening

## Status

This package is the second-stage hardening layer for the unified Project FAR validation platform. It carries the unified validator from PR #231 onto `main` and adds executable controls for the seven assurance gaps previously left open.

## Assurance layers

### Runtime undeclared-dependency tracing

Every registered command check can execute under Linux `strace`. The trace records repository-local reads, writes, child executables, and network attempts. The result is compared against the check's declared inputs and outputs plus the frozen runtime policy.

A traced check fails with `FAR-VAL-TRACE-001` when it reads an undeclared repository path, writes outside an allowed output, launches an undeclared executable, or attempts network access under the deny policy. CI requires the trace backend; an unavailable backend is not treated as a pass.

The trace claim is bounded to operating-system-visible system calls made by the command process tree on the Linux runner. It does not claim visibility into hardware, kernel compromise, or activity outside the traced process tree.

### Independent oracle validation

`far_validation.oracle` independently parses every discovered legacy checker and every manifest command entrypoint using only the Python standard library. It checks:

- manifest coverage and stable failure-code registration;
- nontrivial control flow;
- visible failure paths;
- repository-artifact or subprocess observation;
- rejection of empty, trivial-success, no-failure-path, and syntax-corrupted hostile checker mutations.

This is an independent implementation oracle for checker structure and enforcement identity. It is not an independent scientific re-proof of every domain-specific proposition checked by those scripts.

### Automated weakening detection

`far_validation.weakening` compares changed tests and validators with an explicit Git base. It rejects deleted tests, removed test functions, reduced assertions or failure paths, new skips, major branch loss, and large unexplained AST contraction. Any exception requires a versioned waiver bound to the exact base commit and a nonempty justification.

### Signed cross-runner cache trust

Cache entries and validation certificates use canonical JSON plus HMAC-SHA256 envelopes. Trust is bound to a trust domain and key identifier. CI requires a signing key; unsigned, wrong-domain, wrong-key, and tampered entries are rejected.

The CI workflow proves cross-runner reuse by producing a signed HMAC cache on one runner, packaging its ephemeral verification key with the cache, generating a GitHub Sigstore artifact attestation for the exact bundle, verifying that attestation on a second runner, and then requiring signed cache hits. Persistent cache reuse across separate workflow runs may instead use a protected `FAR_VALIDATION_CACHE_SIGNING_KEY` shared by the authorized runners.

### Mutation and hostile-acceptance campaign

`far_validation.mutations` runs every registered mutation family against every discovered legacy checker and the shared assurance components. The campaign covers:

- four hostile source mutations per checker;
- cache payload, signature, domain, key, and kind tampering;
- certificate commit, tree, required-check, and unsigned-content tampering;
- undeclared read, write, executable, and network activity;
- synthetic test deletion and assertion weakening;
- exhaustive abstract state-space validation.

“Complete” means complete over the versioned mutation registry and every checker discovered by the frozen discovery rule. It does not mean every logically conceivable implementation fault has been enumerated.

### Formal verification

Two formal layers are included:

1. `mechanization/lean/ValidationEngine.lean` machine-checks dependency safety, blocking soundness, successful-run soundness, and exact commit/tree certificate binding.
2. `far_validation.formal_model` exhaustively enumerates every forward-edge dependency DAG through four checks, every Boolean check-outcome assignment, and hostile attestation mutations.

The Lean file proves the abstract assurance model. The Python model checker corroborates the executable state-machine design. This package does not claim a machine-checked refinement proof connecting every line of the Python implementation to the Lean model.

### Merge authority and merge queue

The `Validator Assurance` workflow runs on pull requests, pushes to `main`, workflow dispatch, and the GitHub `merge_group` event. The `merge-authority` job issues a signed certificate bound to the exact checked commit and Git tree and requires all five assurance evidence artifacts.

`tools/configure_validation_protection.py` configures strict branch protection requiring the `merge-authority` status check, an up-to-date branch, pull requests, conversation resolution, and no force pushes or branch deletion.

Native GitHub merge queues are unavailable while this public repository is owned by a personal account. The workflow is merge-group compatible and becomes queue-ready after transfer to an eligible organization; until then, strict required-check branch protection is the strongest enforceable GitHub control.

## Required secrets

- `FAR_VALIDATION_CACHE_SIGNING_KEY`: persistent HMAC secret for cross-runner cache and certificate trust.
- `FAR_GITHUB_ADMIN_TOKEN`: fine-grained administrator token used only by the manual branch-protection configuration workflow.

Neither secret is written to artifacts or logs.

## Commands

```bash
make validate-trace
make validate-oracle
make validate-weakening
make validate-mutations
make validate-formal
make validate-assurance
```

## Claim boundary

This package substantially closes the registered assurance gaps. It does not establish literal impossibility of validator defects, immunity to compromised runners or secrets, independent scientific validation of Project FAR's research claims, or a full refinement proof of the Python engine.
