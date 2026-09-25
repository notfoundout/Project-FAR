# Protected-Artifact Repin Procedure

Status: **Operational procedure.** It binds only after every one of these holds:

- the one-time bootstrap is on protected `main`;
- the `protected-repin-gate` App runs from the owner's gate repository at the current `main` commit;
- branch protection requires `protected-repin-gate` **from that App's ID**;
- every probe in [Mandatory live probes](#mandatory-live-probes) has passed and been recorded.

This is the **AgePony profile** of the design. The owner signs on an iPhone with AgePony, using a Secure Enclave P-256 key that exists only for FAR. The gate App runs as a scheduled GitHub Actions workflow in a separate repository that only the owner controls. No computer, hardware security key, paid service or shell is needed for any owner step. How this differs from the FIDO-SSH design it replaces is recorded in the [threat model](../audits/owner-authorization-agepony-threat-model-2026-09-25.md).

Implementation:

| File | Role |
|---|---|
| [`far_validation/repin_signature.py`](../../far_validation/repin_signature.py) | Canonical payload, signature verification, preparation and bundling helpers |
| [`far_validation/repin.py`](../../far_validation/repin.py) | Evaluator over git objects |
| [`far_validation/repin_gate_app.py`](../../far_validation/repin_gate_app.py) | The GitHub App that publishes the check, and the protection audit |
| [`far_validation/repin_gate_workflow.yml`](../../far_validation/repin_gate_workflow.yml) | Workflow template for the owner's gate repository (never run in this repository) |
| `validation_bootstrap/repin-allowed-signers` | The pinned owner public key, written by `repin_signature.py pin-key` |
| `validation/protected-repin-consumptions.json` | Consumption ledger |

Tests: `tests/test_repin_signature.py`, `tests/test_protected_repin_ledger.py`, `tests/test_repin_gate_app.py`, `tests/test_protected_repin_authorization.py`, with `tests/repin_agepony_testkit.py`.

Live evidence: [required-check shadowing probe](../audits/required-check-shadowing-probe-2026-09-24.md).

## Defects this replaces

1. **Self-deadlock.** Repin authorizations lived in a protected file, so adding one was itself an unauthorized protected transition.
2. **Candidate-controlled enforcement.** The only required check, `merge-authority`, runs the candidate's own workflow file and code.
3. **Repository bytes as authority.** Any ledger a pull request can append lets PR A add an authorization and PR B use it.
4. **GitHub Actions as the check principal.** A check bound to GitHub Actions (App 15368) cannot tell the trusted job from a same-named job in a workflow the candidate adds; both come from App 15368. The live probe confirms this; see the evidence record. Only a check bound to a dedicated App's ID excludes other sources: "If the status is set by any other person or integration, merging won't be allowed."
5. **GitHub account identity as owner intent.** Agents may act through credentials of the owner's account. "The owner's account did it" therefore does not show that the owner authorized a repin.

## Trust chain

```
FAR-only AgePony Secure Enclave P-256 key on the owner's iPhone
  (non-exportable; never in the repository, GitHub secrets, agent workspaces or agent credentials)
  → exact canonical authorization file, inspected and then signed in AgePony
    (detached SSHSIG, namespace "agepony"; FAR's domain separation is inside the signed bytes)
  → trusted evaluator (main's repin*.py, byte-identical to the gate's pinned deployment; git objects only)
  → dedicated GitHub App, run by a scheduled workflow in the owner's separate gate repository
    (the App key exists only in that repository's main-only environment; never in this repository)
  → required check protected-repin-gate bound to that App ID (strict, enforce_admins)
  → protected transition + single-use consumption recorded in the ledger
```

Candidate code controls none of these links:

- A pull request can copy a valid authorization, but it cannot alter or manufacture one.
- It can add a workflow that posts a check named `protected-repin-gate`, but that check does not come from the required App. Its workflows cannot reach the App key, which is not in this repository.
- It can edit `repin.py` or the key file, but the App only ever uses main's versions. The edit is also a protected transition that needs a signature.

## What the App trusts, precisely

| The App trusts | How it is enforced |
|---|---|
| Its own deployment | The workflow checks out exactly `FAR_DEPLOYED_COMMIT` of this repository. The App refuses to run unless its three evaluator files are clean at that commit. |
| Main's evaluator | For every decision, it compares `far_validation/repin.py`, `repin_signature.py` and `repin_gate_app.py` on the current `main` tip with the deployed bytes. On any difference it posts FAILURE asking for a redeploy. It never loads code from the fetched repository. Until `main` carries these files at all (before the bootstrap merge), it posts nothing. |
| Main's pinned key | The deployment's `validation_bootstrap/repin-allowed-signers` must equal the file on the current `main` tip, otherwise it posts FAILURE. The candidate's copy of the key file is never read for verification. |
| The repository identity | Each cycle it checks that the configured name still resolves to the configured immutable repository id (`1283452680`); otherwise it posts nothing. |
| Nothing from the pull request | Pull request heads are fetched into a private bare mirror and read only through `ls-tree`/`cat-file`/`merge-base`: no checkout, no submodules, no hooks, no import, execution or sourcing. A test records every process a full cycle runs and allows only these, plus `openssl dgst` (JWT) and `ssh-keygen -Y verify`. |
| A minimal installation token | Each evaluation cycle requests a token restricted to `checks: write`, `contents: read`, `pull_requests: read`, `metadata: read`, for this repository only. The audit requests `administration: read`, `checks: write`, `metadata: read`. |
| Where it runs | In CI it runs only when the runner reports the configured gate repository's id (never this repository's id), `refs/heads/main`, and a `schedule` or `workflow_dispatch` event. These values are the runner describing itself: they catch a misplaced deployment. The security boundary is that the key exists only in the gate repository's `far-repin-gate` environment. The key file it writes is mode 600 and is deleted at the end of the cycle. |
| One decision per commit | Check runs attach to a commit, not to a pull request. When one head is open as several pull requests, the App decides it once, and it passes only if it passes as every one of them. Deciding per pull request would post conflicting conclusions on the same commit, and one pull request could briefly carry another's success. |
| No local state | Nothing persists between cycles. Whether a decision was already posted is read from the App's own newest completed check run on that head (its `external_id` is the decision key). A cold start re-posts nothing it already said and never suppresses a changed decision. |

## Authorization format

The owner signs the exact bytes of one canonical JSON file. Canonical means:

- sorted keys;
- `,` and `:` separators with no whitespace;
- ASCII only, with every non-ASCII character `\u`-escaped;
- integers only for numbers;
- no trailing newline;
- exactly these fields.

Any other spelling of the same JSON (whitespace, key order, escaped ASCII, `538.0`, a BOM, a trailing newline) is rejected, so a signature can never be moved onto different bytes with the same meaning.

| Field | Meaning |
|---|---|
| `schema` | `far-repin-authorization/3` |
| `domain` | `far-protected-repin-authorization` (FAR's domain separation; see below) |
| `id` | 128-bit random nonce (32 lowercase hex), single use |
| `repository`, `repository_id` | `notfoundout/Project-FAR` and its immutable GitHub id `1283452680` |
| `path` | Protected path, or `validation_bootstrap/assurance-lock.json#contract` for the lock's non-file sections |
| `old_sha256`, `new_sha256` | Exact pin before and after |
| `target_pr` | The pull request that may consume it |
| `base_sha` | The `main` commit the authorization was prepared against |
| `reason` | 20–500 printable characters |
| `issued_at`, `expires_at` | UTC `YYYY-MM-DDTHH:MM:SSZ`, at most 30 days apart |

The signature is the `.sig` file AgePony writes: an OpenSSH SSHSIG with

- namespace `agepony` (AgePony's fixed namespace; FAR cannot choose it);
- key type `ecdsa-sha2-nistp256` only;
- message hash `sha512` only;
- principal `far-repin-owner` in the allowed-signers file.

A ledger entry is `{"payload": "<canonical string>", "signature": "<armored SSHSIG in canonical armor>"}`.

**Domain separation.** Every AgePony signature uses the namespace `agepony`, so the namespace cannot distinguish a FAR authorization from anything else the key signs. FAR therefore puts its domain inside the signed bytes: a signature authorizes nothing unless the signed file is, byte for byte, the canonical encoding of an object with exactly the fields above, `schema` `far-repin-authorization/3` and `domain` `far-protected-repin-authorization`. A photo, a note, a pretty-printed or older-schema JSON, or a payload for another domain is rejected even when the pinned key signed it. The key must still be used for FAR only (see [Owner key](#owner-key-agepony)); the payload rule is what makes a mistake harmless.

### What the evaluator requires

A protected transition passes only when exactly one appended entry, and no more, does all of the following:

1. It verifies under the trusted key.
   - OpenSSH `ssh-keygen -Y verify` checks the curve arithmetic.
   - The verifier itself also requires, because OpenSSH 9.6 does not: the exact pinned signer key; the `agepony` namespace; an empty reserved field; hash `sha512`; `r` and `s` as minimal positive mpints in `[1, n-1]` with nothing trailing; and the canonical armor (70-column base64, LF line ends, final LF). The pinned key must be a valid uncompressed point on P-256.
   - ECDSA is malleable: `(r, n-s)` verifies whenever `(r, s)` does. Secure Enclave signatures are not documented to be low-S normalized, so neither form is refused. Nothing is keyed on signature bytes; single use is enforced on the payload `id`, so a malleated twin authorizes nothing new.
2. It binds the transition exactly: repository name and id, path, old pin, new pin, and pull request.
3. Its `base_sha` is an ancestor of the comparison base, and the path was pinned to `old_sha256` at that commit.
4. The evaluation time falls inside its validity window.
5. Its `id` appears nowhere in the base ledger. This prevents replay after use and after a revert.

There are also ledger-wide rules:

- Every appended entry must match exactly one transition, so an authorization cannot be burned.
- The ledger is append-only.
- Protected paths must be regular files. A symlink whose target text hashes to the pin is rejected.
- Removing a path from the lock is not a supported transition.

Everything else fails closed.

## How to repin a protected artifact (owner, iPhone only)

Anyone may prepare the pull request and the authorization files; only the owner signs. The channel that carries files to and from the phone is untrusted: what protects the owner is steps 3–4.

1. **The pull request exists.** An agent or contributor opens PR `N` with the protected change. Within a few minutes the gate posts `protected-repin-gate` **failure** on its head. The summary lists every protected transition in full:
   ```
   Protected transitions in this head. An authorization must name exactly these values (repository_id 1283452680, target_pr N):
   - path: <path>
     old_sha256: <64 hex>
     new_sha256: <64 hex>
   ```
   Open it in the GitHub app or Safari: PR `N` → *Checks* → `protected-repin-gate`. The check must show the gate App's name, not *GitHub Actions*.
2. **Receive the files.** The preparer runs `repin_signature.py prepare` once per listed transition, then sends you the resulting `.json` files (chat attachment or a link). Save each to *Files → On My iPhone → FAR*.
3. **Review the change itself.** Read the PR diff in the GitHub app. A signature approves the content whose digest it names, so approve only what you have reviewed.
4. **Inspect each file before signing.** Open it in *Files* (Quick Look shows the text) and compare, against the gate's summary for the **current** head of PR `N`:
   - `path`;
   - `old_sha256` and `new_sha256`: at least the first 16 and the last 16 hex characters of each;
   - `target_pr` is `N`, `repository_id` is `1283452680`, `repository` is `notfoundout/Project-FAR`;
   - `schema` is `far-repin-authorization/3` and `domain` is `far-protected-repin-authorization`;
   - `issued_at` is about now and `expires_at` is at most 30 days later;
   - `reason` says what you are approving.

   If anything differs, or the file looks wrapped or reformatted, do not sign it.
5. **Sign in AgePony.** *Sign* → choose the file → identity **FAR repin** (Secure Enclave) → confirm with Face ID or your passcode. AgePony writes `<file>.json.sig`. Save it next to the file.
6. **Return the signatures.** Send each `.sig` back through any channel. The preparer runs `repin_signature.py bundle`, which verifies each signature against the pinned key before appending it, then pushes. Re-wrapped armor from transit is normalized; a signature that does not verify is refused.
7. **Merge only when `protected-repin-gate` from the App passes** on the current head, and its summary lists the authorization ids used.

Each authorization is valid for 14 days by default (30 at most). If `main` moves and the pin changes, or the authorization expires, sign a new file. Never edit an old one: any edit invalidates its signature.

## Owner key (AgePony)

AgePony is open source (Apache-2.0, `github.com/norsehorse-dev/AgePonyiOS`). This profile was written against release 3.1.0 (commit `33731a8d875493a466fc0668d8d9e9aec55f0005`), whose source shows:

- the Secure Enclave identity is created with `SecureEnclave.P256.Signing.PrivateKey()`;
- the vault keeps only the key's Enclave-wrapped `dataRepresentation`, which cannot be used on any other device;
- revealing the private key shows only a placeholder for this identity type, and CryptoKit offers no way to read an Enclave key;
- signing produces an `ecdsa-sha2-nistp256` SSHSIG over the file's SHA-512 in namespace `agepony`.

FAR cannot check any of this remotely. See [What FAR can and cannot verify](#what-far-can-and-cannot-verify).

**Installed-binary acceptance gate.** Source review and installed-binary acceptance are separate evidence. Before the permanent key is created, the owner uses a disposable Secure Enclave P-256 identity to sign the frozen six-file corpus in `agepony-acceptance/`; the agent runs `far_validation/repin_agepony_acceptance.py` over the returned detached signatures and records the exact AgePony version plus the phone observations (identity type, no private-key export, prompts on/off). A PASS permits a permanent key to be created in that exact version despite unresolved source-to-App-Store equivalence; it does not convert that unresolved provenance into a verified claim. Any later AgePony version is a **STOP** for signing with `FAR repin` until the disposable-key acceptance is repeated for that version. The 2026-09-25 bootstrap accepted AgePony **4.0.1 (1)**; details and residual trust are recorded in the [threat model](../audits/owner-authorization-agepony-threat-model-2026-09-25.md#reconciliation-with-the-current-release-2026-09-25).

1. **Generate the key.** In AgePony: *Identities* → *+* → generate a new identity of type **Secure Enclave (P-256)**, named `FAR repin`.
   - Use it for nothing else. Never sign any other file with it; that is harmless to FAR, but it keeps a FAR signature unambiguous.
   - In AgePony *Settings*, keep **In-app biometric prompts** on, so every signature asks for Face ID or your passcode.
2. **Copy the public key.** Open the identity → *Public*. The line reads `ecdsa-sha2-nistp256 AAAA…`; copy it exactly and send it. It is public.
3. **Permanent-key binding.** The disposable-key acceptance includes P0: a non-FAR enrollment proof that must verify as a signature and authorize nothing. The permanent `FAR repin` key signs nothing during enrollment. After pinning, live probe P5 is the cryptographic end-to-end proof that this pinned key is the key the owner controls in AgePony; until P5, compare the copied public key and reported fingerprint exactly.
4. **Pinning.** `repin_signature.py pin-key <file with the copied line>` writes the single line `far-repin-owner namespaces="agepony" ecdsa-sha2-nistp256 <key>` to `validation_bootstrap/repin-allowed-signers` and moves that file's pin. It prints the key's `SHA256:` fingerprint, which AgePony shows for your identity when it verifies one of your signatures.
5. **Rotation** (normal case, current key available): open a PR that repins `validation_bootstrap/repin-allowed-signers` to the new key and authorize it with the **current** key.
   - The new key has no effect within that PR.
   - After merge, the gate fails closed until `FAR_DEPLOYED_COMMIT` is moved to the new `main` commit.

**Do not**, while the key is pinned:

- delete AgePony: the vault holding the Enclave key handle is deleted with it;
- re-enroll Face ID (reset it or add an appearance): AgePony's vault key is bound to the current biometric set, and AgePony documents that re-enrolling invalidates it;
- erase or replace the phone without first rotating the key;
- set an AgePony duress PIN (its wipe deletes the vault), or run any identity or key-migration flow on `FAR repin`.

Each of these is a lost-key event: see [Disaster recovery](#disaster-recovery).

### What FAR can and cannot verify

| Property | Verifiable by FAR? | What it rests on |
|---|---|---|
| The signer holds the private key for the pinned public key | **Yes**, cryptographically, on every authorization | ECDSA P-256 |
| The key was generated in, and cannot leave, a Secure Enclave | **No.** Plain ECDSA SSHSIG carries no attestation, and a software P-256 key produces byte-identical signatures | The enrollment ceremony: you generate the identity as *Secure Enclave* in AgePony and copy its key yourself |
| A person approved each signature (presence, Face ID or passcode) | **No.** Unlike a FIDO signature, there are no user-presence or verification flags | AgePony's in-app prompt (a setting) and the iOS keychain protection of AgePony's vault. The Enclave key itself has no per-use access control in AgePony 3.1.0 |
| The key signs only FAR payloads | **No**, and not required | The payload rule makes any other signed file worthless to FAR |
| The App Store build matches the reviewed source | **No** | Apple's distribution and the AgePony developer; the build is not reproducible from source here |

Enrollment is therefore an owner-controlled trust ceremony. After it, FAR enforces possession of that exact key and nothing weaker.

## The gate App

### Registration (owner, GitHub in Safari)

Go to *Settings → Developer settings → GitHub Apps → New GitHub App*.

- Name: e.g. `far-protected-repin-gate`.
- Homepage URL: the repository URL.
- Webhook: **inactive**. The App polls; no inbound endpoint exists.
- Repository permissions, and nothing else:
  - *Checks: Read and write*;
  - *Contents: Read-only*;
  - *Pull requests: Read-only*;
  - *Administration: Read-only* (only for the protection audit);
  - *Metadata: Read-only* (mandatory).
- Organization and account permissions: none.
- Where it can be installed: *Only on this account*. Install it on `notfoundout/Project-FAR` only.
- Private key: generate it. The `.pem` downloads to *Files*. Put its contents into the gate repository's environment secret (below), then delete the file and empty *Recently Deleted*. Never paste it into a chat, an agent, a note, this repository or any other repository.

### Gate repository (owner, GitHub in Safari)

The gate runs in a **separate public repository owned by you**, for example `notfoundout/far-repin-gate`. Public-repository Actions minutes are free. The logs show only decisions (PR number, head, success), which are public in this repository anyway.

1. **Create it** with a README, and do not add collaborators.
2. **Keep agents out of it.** In *Settings → Applications*, every agent integration (the Claude GitHub App, Codex, others) must be set to *Only select repositories*, and none may include the gate repository. An agent with write access to the gate repository could change its workflow and read the App key.
3. **Actions settings.** In *Settings → Actions → General*:
   - allow only actions and reusable workflows from your own account (the workflow uses none);
   - set *Workflow permissions* to *Read repository contents*;
   - require approval for all outside collaborators.
4. **Environment.** In *Settings → Environments*, create `far-repin-gate`:
   - *Deployment branches and tags*: selected branches, `main` only;
   - environment secret `FAR_APP_PRIVATE_KEY` = the full `.pem` text, including the `-----BEGIN` and `-----END` lines.
5. **Workflow.** Create `.github/workflows/protected-repin-gate.yml` with the exact contents of [`far_validation/repin_gate_workflow.yml`](../../far_validation/repin_gate_workflow.yml) at the deployed commit, then replace the three `REPLACE_…` values:
   - `FAR_DEPLOYED_COMMIT`: the 40-hex `main` commit;
   - `FAR_APP_ID`: the App's id (App settings page);
   - `FAR_GATE_REPOSITORY_ID`: the `id` shown at `https://api.github.com/repos/<you>/far-repin-gate`.

   Commit to `main`.
6. **Redeploy** whenever the evaluator files or the pinned key change on `main`: edit `FAR_DEPLOYED_COMMIT` to the new `main` commit. Until then the App posts FAILURE, by design.

The workflow runs every 5 minutes. GitHub may delay scheduled runs; *Actions → protected-repin-gate → Run workflow* runs it at once (mode `evaluate`, or `audit` to record main's protection).

GitHub disables scheduled workflows in a public repository after 60 days without repository activity. Merges then wait (fail closed) until you re-enable the workflow; editing the README once in a while prevents it.

### Branch protection on `main`

`main` must end up with:

- required status check `protected-repin-gate` with **source = the App** (`app_id` = the App's ID);
- strict (*Require branches to be up to date*);
- *Do not allow bypassing the above settings* on (`enforce_admins`);
- force pushes and deletions off;
- every other existing protection setting unchanged.

`merge-authority` (App 15368) may remain required as an ordinary CI signal. It is never a security authority.

The **protection audit** (`Run workflow` with mode `audit`) posts an App-authored check `protected-repin-audit` on `main`'s tip. It contains the live protection, rulesets and branch rules as JSON, plus `check-protection`'s verdict. That record replaces command-line exports: the owner can read it on the phone, and anyone can diff two audits.

## One-time bootstrap

The frozen, step-by-step owner runbook is kept with the bootstrap record. It is iPhone-only. In summary, in this order:

1. **Credential audit.** No credential reachable by an agent may hold repository **Administration**. Agent integrations must also be excluded from the gate repository.
2. **Ruleset audit.** As of 2026-09-25, both unauthenticated views were empty: `rulesets?includes_parents=true` = `[]` and `rules/branches/main` = `[]`. Rulesets are preserved unchanged in every case.
3. **Disposable-key installed-binary acceptance (P0), then create and pin the permanent owner key.**
4. **Create and install the App, create the gate repository and its workflow** at the bootstrap PR's head commit.
5. **Audit protection** (mode `audit`). This is the "before" record.
6. **Owner merge with only `enforce_admins` relaxed, restored immediately:**
   - untick *Do not allow bypassing the above settings*, save;
   - merge the reviewed bootstrap PR at its reported head;
   - re-tick it, save;
   - run the audit again. It must equal the "before" record.
7. **Redeploy the gate** at the merge commit.
8. **Require `protected-repin-gate` from the App.** In the branch protection rule, add the check and pick the App as its source. Nothing else is changed.
9. **Audit again.** The verdict must be PASS, and the only difference from the "before" record must be the added App-bound check.
10. **Run P1–P7.** Real protected transitions, including #538's, and their signatures come only after all probes pass.

## Mandatory live probes

Run these on throwaway PRs after the bootstrap and before any real protected transition, including #538. Record each result in the audit record: PR number, head SHA, every check run with its App ID and conclusion, and `mergeable_state`. Close every probe PR unmerged, except where a merge is part of the probe. Any deviation means the bootstrap has failed.

| # | Probe | Required result |
|---|---|---|
| P0 | Before the permanent key exists: a disposable Secure Enclave P-256 identity signs the frozen acceptance corpus, including a non-FAR enrollment file; prompt-on/off and export behaviour are observed on the phone. | `repin_agepony_acceptance.py` reports PASS for all six exact-byte signatures and rejects the non-FAR enrollment file as an authorization; the disposable identity is then deleted |
| P1 | Candidate workflow emits a successful job `protected-repin-gate`, plus an unsigned protected repin, so the App posts FAILURE. Re-run the shadow job so it completes last. | `blocked` |
| P2 | The same shadow job while the App emits nothing: disable the gate workflow in the gate repository. | `blocked`; the Actions result is not accepted in place of the App-bound check |
| P3 | Ordinary PR with no protected change. | App SUCCESS; the requirement is satisfied |
| P4 | Unsigned protected transition. | App FAILURE listing the transition in full; `blocked` |
| P5 | Exactly signed protected transition: the owner inspects and signs, in AgePony, a trivial repin of a protected test file for that PR. | App SUCCESS. This also proves the pinned key is the owner's AgePony key: exactly one key can be pinned, and it accepted the owner's signature |
| P6 | The P5 signature copied into another PR with the same transition. | App FAILURE (bound to another pull request) |
| P7 | Merge the P5 PR, then open a PR that appends the same entry again. | App FAILURE (already consumed) |

## Disaster recovery

Recovery never uses an undocumented bypass. Each path below is an **owner recovery bootstrap**, performed with the same seriousness as the initial bootstrap:

1. The owner acts personally, not through an agent.
2. Branch protection is relaxed only for the duration of one reviewed commit.
3. Protection is restored immediately and verified with the audit.
4. P1–P7 are re-run where the gate or key changed.
5. A dated record in `docs/audits/` states the cause, the exact commit landed, and the probe results.

| Event | Response |
|---|---|
| Phone lost, erased, replaced, or AgePony deleted; Face ID re-enrolled; AgePony vault wiped (for example by a duress PIN) or the identity migrated (the key becomes unusable) | No repin can be authorized. Nobody without the phone can sign: the Enclave key never left it, and an iCloud backup restores only a wrapped handle that no other device can use. If the installed AgePony version is not already accepted, repeat the disposable-key installed-binary acceptance first. Generate a new `FAR repin` identity on the phone you have and land a commit that only `pin-key`s it via an owner recovery bootstrap. Redeploy the gate, then run P1–P7; P5 proves the new permanent-key binding. Unused signatures from the old key die with the key change. |
| Phone stolen, or used by someone else, while unlocked or with the passcode known | They can sign whatever they like until the key is replaced. Immediately suspend the App installation, which blocks all merges (fail closed). Then replace the key as above from a new identity. Review every authorization in the ledger since the loss. |
| App private key compromised | Anyone holding it can post a passing check. Immediately revoke the key under *App settings → Private keys* and suspend the installation, which blocks all merges (fail closed). Investigate merges since the suspected compromise. Check runs already posted with the stolen key stay attached to their head SHAs, and a forged summary can imitate a real one. Do not merge any PR open during the compromise until it has a **new head commit** evaluated after the new key is in place. Generate a new key, replace the environment secret, run P1–P7, and record it. |
| Gate repository compromised (for example an agent obtained write access) | Treat it as App key compromise. |
| Gate not running (workflow disabled, schedule paused after 60 days, GitHub Actions outage) | Merges wait (fail closed). Re-enable or re-run the workflow. |
| App deleted | The required check can never be satisfied again (fail closed). Register a new App (same permissions) and install it. Then, as an owner recovery bootstrap, change the required check's source to the new App. Run P1–P7 and record it. |
| Pinned public key must be replaced | If the current key is available, follow the rotation procedure (a signed protected transition; no bootstrap). If it is not, treat it as key loss above. |
| Repository renamed or transferred | Authorizations bind the immutable `repository_id`, so they stay valid across a rename. The App refuses to run while its configured name no longer matches that id; update `FAR_REPOSITORY` after confirming the id. A new repository (new id) needs a fresh bootstrap. |

## Trust boundary and limits

- **Repository administration.** Any credential with admin rights on this repository can edit branch protection and bypass everything here. That includes a classic PAT with `repo` scope, and any App or fine-grained token with *Administration: write*. The chain assumes no credential available to agents has admin rights on this repository. At bootstrap, GitHub reported `permissions.admin: true` for the account one agent session acts through, so the credential audit (bootstrap step 1) is mandatory.
- **The gate repository and the App key.** Anyone who controls the gate repository's workflow, its environment secret, or the App key can post a passing check. Protect them as carefully as the phone.
- **What the owner signs.** A signature authorizes exactly the digests in the file. Compare them with the App's check summary (step 4); a file an agent prepared is only a suggestion to check.
- **The phone and AgePony.** Whoever can unlock the phone and open AgePony can sign. The App Store build of AgePony is trusted to sign only the file you chose; a malicious build could sign other payloads while the vault is unlocked. The pinned key cannot be proven to be Secure Enclave-bound.
- **Denial of service, not bypass.** A candidate can make its own PR unmergeable. It can post a failing status of the same name (a required status and check of one name must both pass), or put a status on the test merge commit so GitHub requires checks there. It cannot make a PR mergeable.
- **Availability.** If the gate is not running, merges wait. This fails closed.
- **Advisory copies.** `python -m far_validation weakening` and `python3 far_validation/repin.py` run the same evaluator in CI or locally. They are useful feedback, not authority.
