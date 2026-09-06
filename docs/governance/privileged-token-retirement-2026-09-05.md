# Privileged GitHub Token Retirement — 2026-09-05

Status: **Accepted** through protected promotion of cleanup PR #474.

The exact obsolete repository credential is irreversibly revoked. The encrypted secret entry remains because both available deletion identities received 403; it contains an invalid value, not a usable administrator credential. Both unsafe consumers are disabled, and the temporary retirement workflow is removed. No branch-protection setting was written or weakened. This acceptance is operational security evidence; it introduces no research-validity, novelty, human-utility, or FARO-readiness claim.

## Accepted execution and independent read-back

The canonical machine-readable evidence is [`privileged-token-retirement-v1.0.json`](../../theory/evaluation/privileged-token-retirement-v1.0.json). It retains the complete capture, retirement and recovery receipts, exact commits/trees, failed attempts, and review scope.

| Evidence | Exact result |
| --- | --- |
| Protected activation | PR #473 merged normally at `7369b9fdb662f4b9bb000b6a76ca85502001ad23`, tree `6cdb6a417ed0c3eaa6c233825625806830141e50` |
| [Retirement execution](https://github.com/notfoundout/Project-FAR/actions/runs/34013331226/job/101432788941) | Run `34013331226`, attempt 1, job `101432788941`: success; PAT DELETE 403, short-lived token DELETE 403, issuer revocation 202, exact-token authentication 401 |
| [Independent recovery execution](https://github.com/notfoundout/Project-FAR/actions/runs/34013331226/job/101432892529) | Attempt 2, job `101432892529`: success using GET only; the same fingerprint still receives 401; both consumers disabled and protection summary enforced |
| Full protection identity | SHA-256 `cb411e177001a318e1fda2ab47b6625718b11af1892e575e5dce32c45b050ae0`, identical in the earlier read-only capture and the complete pre-revocation policy receipt |
| Independent API read-back | Public workflow reads and a separate connector branch read confirmed both consumers `disabled_manually`, main protected, and `merge-authority` enforced for everyone with app `15368` |
| Residue | `secret_absent: false`, `credential_usable: false`; the current connector exposes no Secrets administration, and both available repository deletion identities were actually denied |

The post-revocation branch result is a protection **summary**, not another full Administration read. The complete policy was verified immediately before invalidation, with no policy-writing operation in the control. A new job independently reproduced the invalid-credential result. Its matching fingerprint binds it to the authorized captured value.

## Defect and first execution

PR #468 left a reusable administrator PAT available to manual workflows that check out and execute mutable repository code. Content pinning does not make that credential handoff safe. The consumers are `.github/workflows/canonical-branch-protection.yml` and `.github/workflows/configure-validation-protection.yml`. Their protected hashes prevent an ordinary rewrite/deletion under the current anti-weakening rules. Weakening main protection or bypassing its PR path is prohibited.

PR #470 merged through protected main at `84ec353e7225eeafb9f11aa5dc6663366fcf9a69`, tree `390cb63256eb3537713a7ce08397754f7e567062`, after full exact-head and proposed-merge assurance and review. The [first retirement run](https://github.com/notfoundout/Project-FAR/actions/runs/34011013760/job/101426734335) verified the complete live protection policy, disabled both consumers, and verified the unchanged full policy before attempting deletion. Deleting `FAR_GITHUB_ADMIN_TOKEN` returned **403: Resource not accessible by personal access token**. The run failed and is retained as failed; it is not a successful retirement receipt. Independent public API reads confirmed both workflow states as `disabled_manually` and main still protected with `merge-authority` enforced for everyone and bound to app 15368.

## Separately captured identity and activation

PR #471 merged through the protected path at `24584754b9f628a5eff978d72a2efd716ff62792`, tree `5b763bb7b28015277c033e47151c2c1fb08efcf9`. [Read-only capture run 34012449165](https://github.com/notfoundout/Project-FAR/actions/runs/34012449165/job/101430472911) succeeded with full protection unchanged and both consumers disabled. Its receipt identifies the current obsolete repository credential by SHA-256 `1f2ca3a191e6df475cdad46a7567f35bda8ae2622f9392ba5a11ada8c3a45afa`. It performed no mutation and explicitly reports `retirement_accepted: false`. The complete receipt is retained in `theory/evaluation/privileged-token-retirement-v1.0.json`.

Protected PR #472 authorized retirement of only that captured value. The inline pin and governed receipt matched; regression tests rejected a different synthetic value before API calls. This is evidence about the observed repository credential, not an invented assertion about an earlier unobserved token. Retirement was still pending at that activation stage.

PR #472 activated the pinned control at `86889da3066c4fb911220eac0f3baffc74d96df0`. [Run 34012873101](https://github.com/notfoundout/Project-FAR/actions/runs/34012873101/job/101431576186) matched the fingerprint and passed the initial full-policy check, then failed with 403 while redundantly disabling an already disabled consumer. It attempted no deletion or revocation. PR #473 changed the control to read each consumer first and request disabling only when needed; an active consumer that could not be disabled still failed before retirement. Both states were independently read again before proceeding. This preserved the failed attempt and made repeat execution idempotent.

## Executed procedure, retained for audit

The checkout-free, main-only one-shot was the execution boundary. It had no manual-dispatch trigger and no repository checkout. Its final source is retained in immutable commit `7369b9fdb662f4b9bb000b6a76ca85502001ad23`; the live repository removes it in cleanup. The executed procedure required:

0. Capture the current repository credential fingerprint and full unchanged protection using GET requests only. PR #471 had an empty activation fingerprint and therefore could not delete or revoke. Its protected read-only execution captured the current credential; PR #472 pinned that observed fingerprint and exact capture run. A replacement value must fail before any API call. The capture identifies the currently available obsolete repository credential; it does not invent identity evidence for an unobserved historical value.
1. Verify the complete governed main policy, read both exact consumers and disable only those not already disabled, verify their states, and require the full policy unchanged.
2. Attempt deletion of the exact repository secret with the PAT. If forbidden, attempt the same operation with the already available short-lived Actions token. A successful deletion is the final API operation on that path.
3. If both identities receive 403, print and flush a token-free checkpoint containing the full verified policy, its hash, disabled workflow states, and the two deletion denials.
4. Submit **only this obsolete PAT** to GitHub's unauthenticated `POST /credentials/revoke` endpoint. It accepts classic and fine-grained PATs; the request has no Authorization header and never includes the workflow token. The credential body is never logged.
5. Require a 202 revocation response **and** subsequent authenticated `GET /user` rejection with 401. A valid credential, queue response alone, unexpected response, or expired verification deadline cannot be accepted. Verification is bounded to 61 attempts with five-second intervals; a pending attempt may be recovered by rerunning the same governed control.
6. Read back both disabled workflow states and the enforced public main-protection summary after issuer rejection. Remove the one-shot in a protected cleanup PR, preserving exact execution and read-back receipts.

GitHub documents issuer revocation as irreversible: a revoked credential cannot be reactivated. This endpoint is intended for exposed credentials; here the owner has authorized retirement of the exact obsolete PAT exposed to repository-controlled workflows. No other credential is submitted. See the [GitHub revocation API](https://docs.github.com/en/rest/credentials/revoke?apiVersion=2022-11-28).

The full policy is verified before credential invalidation; the subsequent public summary is identified as a summary, not misrepresented as another full Administration read. The control never writes branch protection. A credentialless rerun verifies absent trusted-main secret injection and the disabled/enforced controls. A rerun with the invalidated secret value additionally requires issuer 401 and uses read-only operations; it cannot accept a still-valid PAT. The separately pinned one-way SHA-256 credential fingerprint authorizes the exact value before mutation and binds checkpoints and recovery to the same high-entropy value without disclosing it. The workflow flushes both the full-policy checkpoint and the 202 response checkpoint before polling, preserving that evidence if the final receipt is interrupted. Recovery acceptance must match the credential fingerprint across these receipts.

## Review, lifecycle, and retained metadata

Acceptance requires either confirmed repository-secret deletion or confirmed issuer revocation plus authentication rejection, unchanged/enforced protection evidence, disabled consumers, complete validation/review, independent live read-back, and protected removal of the one-shot. This recovery follows the authorized permanent-neutralization criterion; it does not relabel the failed deletion attempt as success.

Both repository deletion identities were denied, so the encrypted invalid value remains explicitly recorded as metadata. `secret_absent` remains **false**; issuer rejection and irreversible revocation supply the security result. Such a value is not a usable privileged credential and cannot be revived. It must never be replaced with a new long-lived administrator credential. Future protection changes require an ephemeral, externally controlled administrative credential and a separately reviewed procedure that does not execute mutable repository code.

Codex reviewed the research reconciliation, retirement/recovery logic, identity pin and activation in PRs #470–#472; their substantive findings were fixed before protected merge. The service then exhausted its review quota. PR #473's three-line idempotence change received a recorded [author-side review](https://github.com/notfoundout/Project-FAR/pull/473#pullrequestreview-5124232721) at its exact head, explicitly I0 and not independent review. Cleanup receives the same honestly scoped review. No required reviewer, approving-review threshold, protection rule or assurance check is changed. A quota notice is never counted as a passing review.

| Lifecycle stage | Provenance and acceptance boundary |
| --- | --- |
| Question | Can the observed reusable credential exposure be permanently removed without changing protection? |
| Execution | Actual main runs attempted deletion, captured identity separately, and exercised the pinned retirement control; all failed attempts remain above and in the machine record. |
| Observation | Both deletion identities returned 403; issuer revocation returned 202 and exact-token authentication returned 401; full policy digests matched and consumers were disabled. |
| Discovery | The available repository identities cannot delete the entry, but the issuer permanently invalidated its exact credential; no reusable reapplication workflow is needed. |
| Replication | A new read-only job repeated exact-fingerprint authentication rejection and live control checks; separate connector/public API reads agreed. Regression tests include replacement rejection, active-consumer failure, queue-only rejection, and lost-receipt recovery. |
| Acceptance | Only the observed issuer-revocation receipt and matching recovery are accepted; deletion remains explicitly unsuccessful. |
| Promotion | Protected normal cleanup PR #474, after complete canonical assurance on its exact head/tree and proposed merge tree and recorded review. The GitHub merge event is the promotion identity, avoiding a circular in-file final-commit hash. |
| Repository change | Remove the one-shot; retain exact receipts, invalid-metadata scope, disabled legacy consumers, unchanged protection, and the prohibition on credential recreation. |

The 2026-09-04 application receipt remains historical protection evidence. The earlier retirement failures remain failures; they are not relabelled as successful deletion or revocation.
