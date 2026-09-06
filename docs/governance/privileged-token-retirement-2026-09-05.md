# Privileged GitHub Token Retirement — 2026-09-05

Status: **Neutralization pending after observed secret-deletion permission denial; not yet Accepted**

## Defect and first execution

PR #468 left a reusable administrator PAT available to manual workflows that check out and execute mutable repository code. Content pinning does not make that credential handoff safe. The consumers are `.github/workflows/canonical-branch-protection.yml` and `.github/workflows/configure-validation-protection.yml`. Their protected hashes prevent an ordinary rewrite/deletion under the current anti-weakening rules. Weakening main protection or bypassing its PR path is prohibited.

PR #470 merged through protected main at `84ec353e7225eeafb9f11aa5dc6663366fcf9a69`, tree `390cb63256eb3537713a7ce08397754f7e567062`, after full exact-head and proposed-merge assurance and review. The [first retirement run](https://github.com/notfoundout/Project-FAR/actions/runs/34011013760/job/101426734335) verified the complete live protection policy, disabled both consumers, and verified the unchanged full policy before attempting deletion. Deleting `FAR_GITHUB_ADMIN_TOKEN` returned **403: Resource not accessible by personal access token**. The run failed and is retained as failed; it is not a successful retirement receipt. Independent public API reads confirmed both workflow states as `disabled_manually` and main still protected with `merge-authority` enforced for everyone and bound to app 15368.

## Separately captured identity and activation

PR #471 merged through the protected path at `24584754b9f628a5eff978d72a2efd716ff62792`, tree `5b763bb7b28015277c033e47151c2c1fb08efcf9`. [Read-only capture run 34012449165](https://github.com/notfoundout/Project-FAR/actions/runs/34012449165/job/101430472911) succeeded with full protection unchanged and both consumers disabled. Its receipt identifies the current obsolete repository credential by SHA-256 `1f2ca3a191e6df475cdad46a7567f35bda8ae2622f9392ba5a11ada8c3a45afa`. It performed no mutation and explicitly reports `retirement_accepted: false`. The complete receipt is retained in `theory/evaluation/privileged-token-retirement-v1.0.json`.

Protected promotion of this activation revision authorizes retirement of only that captured value. The inline pin and governed receipt must match; any different value fails before API calls. This is evidence about the current repository credential, not an invented assertion about an earlier unobserved token. Retirement remains pending until the activated main run supplies the required deletion or issuer-revocation evidence.

## Governed completion procedure

The checkout-free, main-only one-shot remains the execution boundary. It has no manual-dispatch trigger and no repository checkout. Its reviewed inline program must:

0. Capture the current repository credential fingerprint and full unchanged protection using GET requests only. PR #471 had an empty activation fingerprint and therefore could not delete or revoke. Its protected read-only execution captured the current credential; this activation revision pins that observed fingerprint and exact capture run. A replacement value must fail before any API call. The capture identifies the currently available obsolete repository credential; it does not invent identity evidence for an unobserved historical value.
1. Verify the complete governed main policy, disable both exact consumers, verify their states, and require the full policy unchanged.
2. Attempt deletion of the exact repository secret with the PAT. If forbidden, attempt the same operation with the already available short-lived Actions token. A successful deletion is the final API operation on that path.
3. If both identities receive 403, print and flush a token-free checkpoint containing the full verified policy, its hash, disabled workflow states, and the two deletion denials.
4. Submit **only this obsolete PAT** to GitHub's unauthenticated `POST /credentials/revoke` endpoint. It accepts classic and fine-grained PATs; the request has no Authorization header and never includes the workflow token. The credential body is never logged.
5. Require a 202 revocation response **and** subsequent authenticated `GET /user` rejection with 401. A valid credential, queue response alone, unexpected response, or expired verification deadline cannot be accepted. Verification is bounded to 61 attempts with five-second intervals; a pending attempt may be recovered by rerunning the same governed control.
6. Read back both disabled workflow states and the enforced public main-protection summary after issuer rejection. Remove the one-shot in a protected cleanup PR, preserving exact execution and read-back receipts.

GitHub documents issuer revocation as irreversible: a revoked credential cannot be reactivated. This endpoint is intended for exposed credentials; here the owner has authorized retirement of the exact obsolete PAT exposed to repository-controlled workflows. No other credential is submitted. See the [GitHub revocation API](https://docs.github.com/en/rest/credentials/revoke?apiVersion=2022-11-28).

The full policy is verified before credential invalidation; the subsequent public summary is identified as a summary, not misrepresented as another full Administration read. The control never writes branch protection. A credentialless rerun verifies absent trusted-main secret injection and the disabled/enforced controls. A rerun with the invalidated secret value additionally requires issuer 401 and uses read-only operations; it cannot accept a still-valid PAT. The separately pinned one-way SHA-256 credential fingerprint authorizes the exact value before mutation and binds checkpoints and recovery to the same high-entropy value without disclosing it. The workflow flushes both the full-policy checkpoint and the 202 response checkpoint before polling, preserving that evidence if the final receipt is interrupted. Recovery acceptance must match the credential fingerprint across these receipts.

## Acceptance and retained metadata

Acceptance requires either confirmed repository-secret deletion or confirmed issuer revocation plus authentication rejection, unchanged/enforced protection evidence, disabled consumers, complete validation/review, independent live read-back, and protected removal of the one-shot. This recovery follows the authorized permanent-neutralization criterion; it does not relabel the failed deletion attempt as success.

If repository tooling cannot delete the secret entry, its encrypted invalid value may remain as explicitly recorded metadata. `secret_absent` must then remain **false**; issuer rejection and irreversible revocation supply the security result. Such a value is not a usable privileged credential and cannot be revived. It must never be replaced with a new long-lived administrator credential. The current repository connector does not expose Secrets administration, and the actual PAT deletion denial is retained above; the workflow tests the remaining available short-lived identity before using revocation.

The present artifact makes no completed-retirement claim. The 2026-09-04 application receipt remains historical protection evidence, and the first retirement run supplies the observed deletion denial and disabled-workflow transition.
