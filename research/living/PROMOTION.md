# Governed living-research promotion

Status: **Research infrastructure; fail closed; no scientific authority is delegated to automation**

`FAR-LIVING-PROMOTION-001` consumes the permanent draft PR #490 only as untrusted Research data. It may package already-governed state into a separate protected PR. It may not decide scientific acceptance, promote metadata into evidence, or bypass the lifecycle.

## Immutable source and execution boundary

The only source inbox is open draft PR #490, `automation/living-research-inbox` into `main`. A transaction freezes the exact source head and exact protected-main base, fetches those refs explicitly, and executes only tools/configuration from protected `main`. Source-branch code is never executed.

A promotion branch is keyed by both exact commits:

`automation/living-promotion-<40-hex-source>-<40-hex-base>`

If either PR #490 or `main` moves before publication, the attempt fails. A new base produces a new branch rather than rewriting a stale promotion attempt.

## Research snapshots: review is not authorization

`review-dispositions-v1.0.json` is durable review/queue memory. Membership there is **not** snapshot authority.

A reviewed candidate is mechanically snapshot-eligible only when protected `snapshot-authorizations-v1.0.json` contains one exact authorization with:

- `candidate_id`;
- exact `candidate_sha256`;
- exact `source_key` and allowed review `disposition`;
- exact `review_basis` path and `review_basis_sha256`;
- `review_record_sha256`, the canonical hash of the complete protected review row;
- `authorization_status: ACCEPTED_FOR_MECHANICAL_SNAPSHOT`.

If that authorization is absent, the candidate remains unpromoted. Existing historical review rows are not retroactively upgraded merely by hashing their current candidate bytes.

A Research snapshot preserves `authority: Research` and lifecycle stage `DISCOVERED`; it changes no claim, theorem, novelty, EFR, external-validity, utility, or independence status.

## Canonical edit proposals

A canonical edit is stronger. The source proposal must be at `PROMOTION_PROPOSED`, and protected `promotion-authorizations-v1.0.json` must bind the exact:

- proposal SHA-256;
- candidate SHA-256;
- canonical operation-set SHA-256;
- Question, Execution, Observation, Discovery, Replication, and Acceptance artifact SHA-256 values;
- `authorization_status: ACCEPTED_FOR_MECHANICAL_PROMOTION`.

Proposal provenance uses exact path/hash pairs:

```json
{
  "provenance": {
    "question": {"path": "...", "sha256": "..."},
    "execution": {"path": "...", "sha256": "..."},
    "observation": {"path": "...", "sha256": "..."},
    "discovery": {"path": "...", "sha256": "..."},
    "replication": {"path": "...", "sha256": "..."},
    "acceptance": {"path": "...", "sha256": "..."}
  }
}
```

Each `write_file` operation binds the exact current-main preimage (`ABSENT` for a new file), exact payload hash, target path, and payload source path. Duplicate targets, cross-proposal collisions, unsafe paths, symlink paths, protected/control-plane paths, disallowed extensions, stale preimages, or payload hash mismatches fail closed.

## Project-changing studies

`PROJECT_CHANGE_REQUIRED` is a governed review disposition, not an automated relevance score. It may be recorded only after the ordinary research lifecycle has established that the accepted result requires a Project FAR correction.

A row with that disposition is incomplete unless it binds one exact `proposal_id`, leaves the metadata-only review queue, and has both an exact snapshot authorization and an exact `PROMOTION_PROPOSED` canonical-edit authorization. The permanent inbox must contain the bound candidate, the exact proposal, at least one `write_file` operation, and every referenced payload. `tools/check_living_project_change_obligations.py` fails closed on any missing component before promotion runs.

A successful explicit validation of the rolling inbox triggers the promotion workflow on protected `main`. Changes to the protected acceptance/authorization surfaces on `main` also trigger it. The scheduled pass remains a recovery path. The existing promotion transaction then independently revalidates hashes, provenance, preimages, targets, and the frozen source/base before opening the separate correction PR.

Automatic PR creation is required once the accepted package is complete. Automatic merge is not permitted; Exact Head Assurance and protected `merge-authority` remain controlling.

## Write boundary

Automatic canonical targets are limited by `promotion-policy-v1.0.json`. `.github/`, `tools/`, `tests/`, validation/bootstrap code, `docs/governance/`, all `research/living/` governance/control files, and `research/living/inbox/.rolling-pr-anchor.json` are never canonical payload targets. If accepted information requires such an implementation change, it uses the ordinary governed code path and the obligation remains explicit until that work lands.

This restriction prevents executable bytes from the unprotected living inbox from running inside a write-scoped promotion job. The protected authorization binds the scientific/canonical payload exactly; it does not turn the inbox into a trusted software supply chain.

The only non-plan files permitted to change during promotion are the explicitly declared deterministic reconciliation outputs in `trusted_generated_paths`.

## Transaction seal

Materialization installs a fail-closed pre-commit hook. The runner stages only planned targets plus actually changed trusted-generated paths—never `git add -A`. Immediately before commit the seal independently requires:

1. the source head still equals the frozen source SHA;
2. current protected `main` still equals the frozen base SHA;
3. every planned file is staged and byte-identical to its approved result;
4. no unplanned staged, deleted, unstaged, or untracked repository file remains;
5. all preimages still match the frozen base;
6. the rolling anchor is absent;
7. one manifest records the exact SHA-256 and authority class of every promoted file.

The promotion commit must be exactly one commit whose parent is the frozen base.

## Independent protected verification

`tools/check_living_promotion_head.py` is independent of the promoter. Canonical tests run it inside `merge-authority`. For pull-request events GitHub checks out a synthetic merge commit, so the verifier resolves and checks the exact `GITHUB_HEAD_REF` promotion commit instead of trusting synthetic `HEAD`.

The verifier is read-only: it does not fetch or mutate `.git`. It re-derives the promotion from the protected base and rejects stale bases, forged/missing manifests, extra files, multiple commits, unsealed bytes, unauthorized snapshots, altered review/review-basis bytes, unauthorized proposal operations, provenance drift, stale preimages, and governance/self-modifying targets.

Strict branch protection requires the `merge-authority` check to be current with `main`. A base advance therefore invalidates the promotion and requires a new source+base transaction.

## Publication boundary

The scheduled workflow is only a small wrapper around `tools/run_living_research_promotion.py`. The runner may create/recover the separate promotion PR and dispatch protected validation. It never merges, approves itself, changes branch protection, writes directly to `main`, or uses the permanent inbox PR as the merge vehicle.

If GitHub Actions lacks permission to create a PR, the exact branch is preserved and the run fails. No broader token or protection bypass is substituted.

## Core rule

No bytes become canonical merely because the automation considers them relevant. Promotion requires the exact bytes, exact protected authorization, exact provenance, exact base state, exact sealed diff, and exact protected validation to agree. Any uncertainty or mismatch produces **no promotion**.
