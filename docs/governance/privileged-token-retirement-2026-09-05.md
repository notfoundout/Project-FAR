# Privileged GitHub Token Retirement — 2026-09-05

## Artifact status

**Scheduled governance control; not yet accepted.**

This record becomes Accepted only after the retirement workflow has run from canonical `main`, the exact live controls and workflow states have been read back, the `FAR_GITHUB_ADMIN_TOKEN` Actions secret has been deleted, and a cleanup PR has removed the one-shot workflow.

## Defect

PR #468 left a long-lived administrator PAT available to manual workflows that check out and execute mutable repository code. Content pinning detects repository drift but does not make handing a reusable administrator credential to repository-controlled code safe. The two affected workflows are:

- `.github/workflows/canonical-branch-protection.yml`;
- `.github/workflows/configure-validation-protection.yml`.

Their protected hashes prevent a safe ordinary rewrite or deletion under the current anti-weakening rules. Weakening `main` protection or bypassing the protected PR path is prohibited.

## Permanent remediation

The one-shot `.github/workflows/retire-far-github-admin-token.yml` runs only when its exact file first reaches `main`. It has no `workflow_dispatch`, does not check out repository content, and executes only its inline reviewed retirement program. It must, in order:

1. use the existing credential for a fail-closed read-back of all governed `main` protection fields;
2. disable the two exact privileged workflows;
3. delete the exact repository Actions secret `FAR_GITHUB_ADMIN_TOKEN`;
4. read back both disabled workflow states, secret absence, and unchanged branch protection; and
5. emit a token-free JSON receipt.

The workflow does not configure or weaken protection. Any unexpected repository, branch, protection value, workflow state, or API response fails closed. After successful execution, a protected cleanup PR removes the one-shot and promotes this record with its run, final commit/tree, and independent live read-back.

Until those steps complete, this artifact makes no retirement claim. The 2026-09-04 protection-application receipt remains historical evidence for the applied policy, not evidence that the privileged credential is safe to retain.
