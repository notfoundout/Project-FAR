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

Its safe functionality is retained permanently in `.github/workflows/canonical-branch-protection.yml`. That workflow is manual-dispatch only, requires `FAR_GITHUB_ADMIN_TOKEN`, applies the governed protection policy, and immediately performs the independent fail-closed read-back. PR #468 also content-pins this permanent workflow in `validation_bootstrap/assurance-lock.json`, so future changes to its privileged execution path cannot silently bypass the protected-artifact repin controls.

The older `.github/workflows/configure-validation-protection.yml` remains an assurance-locked apply-only historical surface. It is not the canonical evidence-producing reapplication path because it does not perform read-back. The canonical reapplication path is `.github/workflows/canonical-branch-protection.yml`.

## Merge queue boundary

Native GitHub merge-queue activation remains unavailable while the repository is owned by a personal account. This is not a branch-protection failure. The validator workflow already handles `merge_group` events and becomes queue-ready after transfer to an eligible organization.

## Security notes

`FAR_GITHUB_ADMIN_TOKEN` is a GitHub Actions secret and is not stored in repository content or artifacts. It should remain repository-scoped, administration-only, and rotated or replaced before expiration if future protection reapplication is required.

## Final disposition

`CANONICAL_MAIN_PROTECTION = ENFORCED`

The previous repository-governance blocker is closed. W1-W6 scientific dispositions are unchanged.
