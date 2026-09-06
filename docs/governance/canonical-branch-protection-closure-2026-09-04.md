# Canonical Branch Protection Closure — 2026-09-04

## Artifact status

**Accepted governance record.**

Acceptance basis: successful live application and fail-closed read-back on GitHub run `33894912212`; independent GitHub branch metadata reporting `main` protected; and promotion through PR #468 under the newly enforced `merge-authority` and conversation-resolution controls. Repository merge of PR #468 is the promotion event for this record.

## Scope

This record closes the repository-control-plane gap identified after PCA-W6. It changes repository governance only. It does not modify, reinterpret, or upgrade any W1-W6 scientific artifact or theorem result.

## Canonical target

Repository: `notfoundout/Project-FAR`

Branch: `main`

Protection was applied from canonical `main` commit `78578e2ebd805b52b2abc67c1453526359c83a82` after PR #467 merged.

## Execution

The one-shot bootstrap workflow invoked the already-governed tools:

- `tools/configure_validation_protection.py`
- `tools/check_validation_protection.py`

The apply step completed successfully using the repository-scoped `FAR_GITHUB_ADMIN_TOKEN` Actions secret. The independent read-back completed successfully immediately afterward.

Successful bootstrap workflow run: `33894912212`, rerun attempt after administrator-token provisioning.

## Read-back result

The fail-closed verifier returned:

```json
{
  "branch": "main",
  "control_plane_enforced": true,
  "errors": [],
  "owner_type": "User",
  "repository": "notfoundout/Project-FAR",
  "required_check": "merge-authority",
  "visibility": "public"
}
```

GitHub branch metadata independently reported:

- `protected: true`
- protection enabled
- required status check: `merge-authority`
- enforcement level: `everyone`
- strict up-to-date checking enabled by the configurator/read-back contract

The governed configurator/read-back contract additionally requires pull requests, conversation resolution, no force pushes, and no branch deletion. The successful read-back is the authoritative runtime evidence that those required settings matched the encoded policy at the time of closure.

## Permanent reapplication control

The temporary `.github/workflows/bootstrap-canonical-protection.yml` workflow existed only to cross the initial unprotected-to-protected boundary and is removed by PR #468.

PR #468 retained the functionality in `.github/workflows/canonical-branch-protection.yml`, but the later security review found that a content pin does not make it safe to expose a reusable administrator PAT to checked-out mutable repository code. The 2026-09-04 application and read-back remain valid historical protection evidence. The reapplication design is superseded by the separately governed 2026-09-05 privileged-token retirement; see `privileged-token-retirement-2026-09-05.md`.

The older `.github/workflows/configure-validation-protection.yml` and the PR #468 workflow remain assurance-locked repository artifacts. Both live workflows are now disabled and their exact credential is irreversibly revoked, with no protection weakening. Neither is a current authorized reapplication path.

## Merge queue boundary

Native GitHub merge-queue activation remains unavailable while the repository is owned by a personal account. This is not a branch-protection failure. The validator workflow already handles `merge_group` events and becomes queue-ready after transfer to an eligible organization.

## Security notes

`FAR_GITHUB_ADMIN_TOKEN` was not stored in repository content or artifacts, but retaining it as a reusable Actions secret is no longer authorized. Its verified irreversible issuer revocation and both disabled consumers are recorded in `privileged-token-retirement-2026-09-05.md`. Both available secret-deletion identities returned403, so the encrypted invalid entry remains explicitly recorded; no usable credential or authorized reapplication path remains.

## Final disposition

`CANONICAL_MAIN_PROTECTION = ENFORCED`

The previous repository-governance blocker is closed. W1-W6 scientific dispositions are unchanged.
