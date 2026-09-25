# Owner Authorization on an iPhone: AgePony Profile — Threat Model (2026-09-25)

Status: **Design record with author-side test evidence.** It is not independent validation. Nothing here has run against the live repository yet: the live probes P0–P7 in the [procedure](../governance/protected-repin-procedure.md#mandatory-live-probes) are the acceptance gate.

## Constraint and decision

The owner has only an iPhone: no computer, no hardware security key, and $0 recurring cost. The FIDO-SSH design (B″) needs a computer, `ssh-keygen` and a FIDO key for the owner signer, and a separate always-on host for the gate App. Both were replaced:

| Layer | B″ (FIDO-SSH) | This profile |
|---|---|---|
| Owner signer | `sk-ssh-ed25519` on a FIDO key; touch + PIN, enforced and verified from signature flags | AgePony Secure Enclave `ecdsa-sha2-nistp256` identity on the iPhone |
| SSHSIG namespace | `far-repin-authorization@v1` (FAR-specific) | `agepony` (fixed by AgePony) |
| Domain separation | Namespace | Inside the signed bytes: `schema` `far-repin-authorization/3` plus `domain` `far-protected-repin-authorization`, with strict canonical encoding |
| Payload bindings | Repository id and name, PR, base SHA, path, old/new digest, nonce, issuance, expiry, reason | Unchanged |
| Evaluator (`repin.py`) | Git objects only, ledger, single use, lineage, no burning | Unchanged, except that it reports each transition's full digests |
| Digest source for the owner | Computed by the owner on their computer | Read from the gate App's check summary (App-authored, per head) |
| Gate host | Owner VPS with a systemd service | Scheduled GitHub Actions workflow in the owner's separate public gate repository |
| Gate state | `posted.json` on the host | None; decision key stored in the check run's `external_id` |
| Protection read-back | Owner's `gh api` exports | App-authored `protected-repin-audit` check with the full JSON |

The WebAuthn/iCloud-passkey design (B‴) is not the basis of this profile; see [B‴ as historical evidence](#b-as-historical-evidence).

## AgePony: what was verified in its source

Source: `github.com/norsehorse-dev/AgePonyiOS`, Apache-2.0, cloned on 2026-09-25 at release 3.1.0, commit `33731a8d875493a466fc0668d8d9e9aec55f0005` (2026-07-30).

| Claim | Evidence | Status |
|---|---|---|
| The Secure Enclave identity is generated inside the Enclave | `AgePony/Services/SecureEnclaveSigner.swift`: `SecureEnclave.P256.Signing.PrivateKey()` | Verified in source |
| Only a device-bound handle is stored | Same file: persists `key.dataRepresentation` (Enclave-wrapped) and the public wire blob | Verified in source |
| No private-key export for this type | `AgePony/Vault/VaultModels.swift` `privateDisplayString()`: the "reveal private key" path shows only "(Secure Enclave — the private key is generated in hardware and never leaves this device)". CryptoKit's `SecureEnclave.P256.Signing.PrivateKey` has no raw-key accessor | Verified in source |
| Signature format | `Sources/AgePonyCore/Signing/SSHSigner.swift` `assembleECDSAP256`: `string("ecdsa-sha2-nistp256") ‖ string(mpint r ‖ mpint s)`, minimal mpints; SHA-512 message hash; armor at 70 columns, LF, final LF | Verified in source; ported line for line in `tests/repin_agepony_testkit.py` |
| Fixed namespace | `SSHSig.defaultNamespace = "agepony"`; the UI passes no other | Verified in source |
| Public-key export | `publicDisplayString()`: `ecdsa-sha2-nistp256 <base64 wire blob> [comment]`, shown in the identity's *Public* block | Verified in source |
| Presence per signature | Not enforced by the Enclave: the key has no `SecAccessControl`. `SignFileView.startSign` asks for Face ID or passcode only while the **In-app biometric prompts** setting is on (default on). The vault master key is in the keychain with `biometryCurrentSet` or `devicePasscode`, `WhenUnlockedThisDeviceOnly`, and is re-fetched after the app returns from the background | Verified in source; **weaker than FIDO UP+UV** |
| Face ID re-enrollment | `KeychainStore.swift`: "Re-enrolling Face ID / Touch ID invalidates the entry" | Verified in source; a lost-key event for FAR |
| The App Store binary is built from this source | Not reproducible here | **Unknown** |
| Price | agepony.com states no cost, subscription or in-app purchase; the App Store page could not be fetched from this environment | Vendor statement, unverified |

AgePony's own test vector (`Tests/AgePonyCoreTests/SSHSigECDSATests.swift`, produced by `ssh-keygen -Y sign -n agepony`) is reused: it verifies as a signature, and FAR rejects it as an authorization.

## Reconciliation with the current release (2026-09-25)

The App Store serves AgePony **4.0.x** for iOS. The audit above covers 3.1.0.

| Question | Finding | Source |
|---|---|---|
| Is the iOS 4.0.x source published? | **No.** `git ls-remote github.com/norsehorse-dev/AgePonyiOS` shows one ref, `main` = `33731a8` ("AgePony 3.1.0", 2026-07-30), with no tags. The vendor's own plans refer to "iOS 4.0.0" and "iOS 4.x", so the store build is newer than any public source. | Repository refs; `AgePonyAndroid` `AgePony_5.0.0_Plan.md`, `AgePony_5.0.1_Plan.md` at `af84282` (2026-09-23) |
| Known, unfixed iOS security findings? | **Yes.** "The iOS-side audit findings are tracked in the private audit report, not here, until the iOS fixes ship" (September 2026 security audit). The Android findings in the same audit include Critical and High items; the iOS ones are undisclosed. | `AgePony_5.0.1_Plan.md` §6 |
| Detached-signature format | The vendor's cross-platform spec says it is **unchanged**: namespace `agepony`, SSHSIG over the file bytes. The new namespaces `agepony-sig-v2` and `agepony-bundle-v2` belong only to sealed-in signatures, which FAR rejects because its namespace is pinned. | `docs/SIGNATURE_FORMATS_v2.md` (Android repo) |
| Sealed-in v1 signatures | In AgePony before signature v2 (all iOS 4.x), a sign-then-encrypt signature is an SSHSIG under `agepony` over the payload, the same as a detached one. Sign-encrypting a FAR payload is therefore equivalent to signing it, and no new capability arises. | Same spec, "Why v2" |
| Planned changes that could touch the FAR key | Moving iOS Secure Enclave keys to the `age1tag1` recipient format "with a migration path for existing SE keys"; a duress PIN that wipes the vault ("iOS implements the same spec next release"; after the audit, duress means PIN-only). A wipe, or a migration that re-creates the identity, destroys the FAR key. | `AgePony_5.0.0_Plan.md` §2.5, `AgePony_4.0.0_Plan.md` §7 |
| Secure Enclave creation, access control, prompt setting, public-key display, vault behaviour in 4.0.x | **Unverified**: no source. | none |

**Consequence.** Source-to-App-Store equivalence remains unresolved, so this profile does **not** infer 4.0.x behaviour from the reviewed 3.1.0 source. Instead, permanent-key enrollment is gated by a black-box acceptance of the exact installed binary with a disposable key and a frozen corpus in `agepony-acceptance/`. `far_validation/repin_agepony_acceptance.py` verifies the six detached signatures over the exact bytes, the P-256/`nistp256` key and point, SSHSIG v1, namespace `agepony`, empty reserved field, `sha512`, minimal in-range ECDSA components, canonical armor, exact-message binding, non-FAR/canonical rejection, malformed-envelope rejection, and the expected `(r, n-s)` ECDSA twin. The owner separately observes the identity type, private-key export surface, and prompt-on/prompt-off behaviour on the phone. This does **not** prove source equivalence, Secure Enclave origin from the signature, or that a benign App Store build will never sign autonomously; those remain explicit trusted-ceremony limits. The initial bootstrap accepted AgePony **4.0.1 (1)** on 2026-09-25. Any AgePony version change requires the disposable-key acceptance again before `FAR repin` signs anything in that version.

## Why the gate runs in the owner's GitHub Actions

Options considered under the $0, iPhone-only and no-agent-accessible-key constraints:

1. **Owner-run VPS (B″ as specified).** It needs a paid host and a computer to administer: excluded.
2. **Free serverless platform** (for example a Workers-type service). The evaluator would need a JavaScript port, proven equivalent with shared vectors. It adds a third party that holds the App key and runs the gate code, and requires administering a second account from the phone.
3. **Scheduled workflow in a separate, owner-only public repository (chosen).** Actions minutes are free for public repositories. GitHub is already fully trusted: it hosts the repository and enforces branch protection. The unchanged Python evaluator runs byte-for-byte, so no port and no equivalence argument is needed. It is administered in Safari, and the key lives in an environment secret restricted to `main`.

The protected repository's own Actions was excluded. The live probe showed that a candidate controls workflows there, and agents hold write access to it.

## Threats, controls and tests

Test files: `S` = `tests/test_repin_signature.py`, `L` = `tests/test_protected_repin_ledger.py`, `A` = `tests/test_repin_gate_app.py`, `W` = `tests/test_protected_repin_authorization.py`.

| Threat | Control | Evidence |
|---|---|---|
| Wrong key / software-key substitution after enrollment | Exactly one pinned key; signer key in the SSHSIG must equal it; OpenSSH verifies under it | S `test_wrong_and_substituted_keys_are_rejected`; L `test_signature_under_an_untrusted_key_fails` |
| Software key enrolled instead of an Enclave key | **Not detectable** by FAR; the enrollment ceremony is owner-controlled | Documented limit |
| AgePony namespace confusion | Namespace must be exactly `agepony`, locally and in `ssh-keygen -n`; the pin is namespace-restricted | S `test_namespace_confusion_is_rejected`, `test_only_one_plain_p256_key_in_the_agepony_namespace_is_accepted` |
| Arbitrary AgePony-signed non-FAR files | Signed bytes must be the exact canonical payload with FAR `schema` and `domain` | S `test_arbitrary_agepony_signed_files_authorize_nothing`, `test_agepony_published_golden_vector_verifies_as_a_signature_but_authorizes_nothing`; P0 |
| Altered payload byte | Signature over exact bytes; canonical-only parsing | S `test_any_change_to_a_signed_payload_is_rejected` (every single-byte flip) |
| Cross-PR / repository / base / path / digest replay | Payload bindings checked by the evaluator | L `…for_another_pull_request…`, `…another_repository…`, `…another_repository_id…`, `…another_path…`, `…another_new_digest…`, `…foreign_base…`, `…stale_base_pin…`; A `test_end_to_end_decisions` |
| Reuse after merge; reuse after revert | Nonce single use against the base ledger | L `test_replay_after_use_fails`, `test_replay_after_revert_fails` |
| Signature malleability `(r, n-s)` | Nothing keyed on signature bytes; the payload nonce is single use | S `test_value_malleability_verifies_but_cannot_be_replayed`; L `test_malleated_signature_twin_is_valid_but_cannot_be_replayed`, `test_malleated_twin_replay_after_merge_and_after_revert_fails` |
| Malformed P-256 SSHSIG | Strict local parse: minimal positive mpints in `[1, n-1]`, no trailing data at three levels, empty reserved field, `sha512`, version 1, canonical armor; valid on-curve uncompressed pinned point | S `MalformedSignatureTests` (encodings OpenSSH 9.6 accepts and those it rejects), `test_key_blob_must_be_a_valid_uncompressed_p256_point` |
| Other algorithms (ed25519, FIDO, P-384, RSA, sha256) | P-256/sha512 only | S `test_other_signature_algorithms_under_the_same_name_are_rejected`, `test_sha256_message_hash_is_refused` |
| Key rotation | Rotation is a protected transition signed by the current key; the new key has no effect in the rotating PR; the gate fails closed until redeployed | L `test_key_rotation_…`, `test_rotated_key_has_no_effect_…`, `test_after_rotation_the_gate_must_be_redeployed_…` |
| Lost phone | Recovery bootstrap re-pins a new key; the old key's signatures are then rejected | L `test_lost_key_signatures_fail_after_a_recovery_repin` |
| Candidate replacement of the pinned key | The trusted key comes from the deployment and must equal main's; the candidate's key file is never used; changing it is itself a protected transition | L `test_candidate_replacing_the_pinned_key_cannot_authorize_itself`; A `test_deployment_key_not_matching_main_fails_closed` |
| Candidate shadow required check | Required check bound to the App ID; `check_protection` rejects any weaker binding | A `test_end_to_end_decisions` (PR 542), `ProtectionTests`; live P1, P2; shadowing probe record |
| Compromised candidate workflow | The App key is not in this repository; the gate reads candidate bytes only as git objects; the gate refuses to run from this repository's id | A `test_every_process_the_app_runs_is_read_only_object_access`, `test_ci_is_allowed_only_as_the_gate_repositorys_main_schedule_or_dispatch`, `test_actions_cycle_fails_closed_on_any_misconfiguration` |
| Compromised gate host (GitHub runner, gate repository, App key) | **Not preventable by FAR**: whoever holds the App key can post a passing check. Mitigations: key only in a `main`-only environment of an owner-only repository with no agent integration; no third-party actions; `GITHUB_TOKEN` has no permissions; key file mode 600, deleted after each cycle; revocation procedure | A `WorkflowTemplateTests`, `test_actions_cycle_uses_the_deployed_key_file_and_leaves_no_app_key_behind` |
| Gate absence or outage | No check means the required check is pending: blocked. Before the bootstrap merge the gate posts nothing | A `test_nothing_is_posted_before_main_carries_the_evaluator`, `test_modified_or_wrong_deployment_refuses_to_run`; live P2 |
| Free-host cold start, restart, statelessness | No local state; dedup key read from the App's own newest completed check run; another App's run never counts; a changed decision is always posted | A `test_cold_start_is_stateless_and_never_suppresses_a_changed_decision`, `test_only_the_apps_own_completed_runs_count_as_already_posted` |
| One commit opened as two pull requests (authorization bound to #N reused by #M on the same head) | One decision per head over every open PR on it; success only if it passes as each. This defect was inherited from B″ and found while building the simulation for this profile. Residual: until the next cycle after a duplicate PR is opened, the earlier decision stands. Merging then lands the exact commit the owner authorized, and its ids are consumed | A `test_a_head_open_as_two_pull_requests_is_decided_once_and_must_pass_as_both` |
| Evaluator drift between the gate and main | Deployed files must equal main's, otherwise FAILURE | A `test_deployed_evaluator_must_equal_mains_evaluator` |
| Agent prepares wrong digests for the owner to sign | The owner compares the file with the App's summary, which lists every transition in full for the current head | A `test_check_summary_publishes_every_transition_in_full_for_the_owner`; procedure step 4 |
| All earlier B″ attacks (self-repin, unsigned, username-only, forged, burning, ambiguity, append-only rewrite, two-PR escalation, path drop, symlink, protecting the ledger, working-tree bypass, rename of protected workflow, fabricated `merge-authority` success) | Unchanged evaluator and weakening gate | L and W suites, unchanged apart from the key type and `domain` |

## Comparison

| Property | FIDO-SSH B″ | WebAuthn B‴ | AgePony profile |
|---|---|---|---|
| Private key non-exportable | Yes (FIDO hardware) | **No**: iCloud Keychain syncs and escrows it | Yes (Secure Enclave), **per source and the owner's ceremony; not remotely verifiable** |
| Key bound to one device | Yes | No | Yes (same caveat) |
| Per-signature presence, hardware-enforced | Yes: touch | Yes: UP | **No**: app-level prompt, a setting |
| Per-signature user verification | Yes: PIN (UV) | Yes: UV (device passcode or biometric) | Passcode or Face ID via the app prompt and vault unlock; **not attested** |
| FAR verifies presence/UV from the signature | Yes (flags 0x05, checked locally) | Yes (authData flags) | **No**: no flags exist |
| FAR verifies hardware origin | No (no attestation used) | No (attestation `none`) | No |
| Recoverable by someone without the device | No | **Yes**: Apple account recovery (password + SMS + passcode) restores the passkey | No |
| Signer software trusted to sign only the shown bytes | `ssh-keygen` on the owner's computer | Browser + an authorizer page served from the App host | AgePony App Store build |
| Signatures per presence event | One per touch | One per assertion | Unlimited while the vault stays unlocked, if a malicious AgePony build acts on its own |
| FAR-specific namespace | Yes | RP ID + challenge domain | **No** (`agepony`); replaced by in-payload domain + canonical bytes |
| Domain confusion resistance | Namespace | Challenge prefix | Exact canonical payload with schema + domain; tested |
| Owner computes digests independently | Yes (own computer) | No | No: compares against the App's check summary (App-authored; trust = gate) |
| Payload bindings, single use, lineage | Yes | Yes | Yes (same evaluator) |
| Gate host outside candidate control | Owner VPS | Owner VPS | Owner's separate GitHub repository (GitHub-hosted runner) |
| Extra trusted parties beyond GitHub | VPS provider | VPS provider, DNS, a web CA | Apple (Secure Enclave, App Store distribution), AgePony developer |
| Recurring cost | VPS | VPS | $0 |
| Owner needs a computer | Yes | No | No |

## Remaining trust differences from B″ (explicit)

1. **Presence is not cryptographically attested.** B″ proved touch + PIN in every signature. Here FAR cannot tell whether a person approved a signature. What stands in for it is iOS device unlock, AgePony's vault unlock (Face ID or passcode) and the in-app prompt. This is unavoidable with plain ECDSA SSHSIG, and AgePony's Enclave key carries no per-use access control.
2. **Hardware binding is asserted, not proven.** Enrollment is an owner ceremony. A key generated in software and pasted by mistake, or by someone with access to the conversation, would be indistinguishable. P0 proves that the owner's AgePony holds the key they sent; it does not prove the key is Enclave-bound.
3. **The signing app is a larger trust base.** A malicious or compromised AgePony build (auto-updated from the App Store) could sign arbitrary FAR payloads whenever the vault is unlocked, without per-signature hardware consent. Under B″, a compromised computer could at most swap the payload of one touch-approved signature. Mitigation: every authorization appears in the public ledger and in the App's check summary, and the owner merges only PRs they review. Optional: disable automatic App Store updates.
4. **The namespace is shared.** Domain separation moved into the payload. It is complete for FAR (tested), but other AgePony verifiers would accept FAR payloads as ordinary AgePony-signed files. That is harmless, because the key is trusted nowhere else.
5. **Digest provenance.** The owner no longer recomputes digests on their own computer. They compare the file against the gate App's summary for the current head. Against an agent that prepares wrong digests, this protects exactly as B″'s recomputation did: the agent cannot author the App's check. It differs only when the gate itself is compromised, and a compromised gate already defeats B″ (it can post success regardless of signatures). So this is a change of mechanism, not a loss against any adversary the design resists.
6. **Gate host.** GitHub-hosted runners and the owner's gate repository replace an owner VPS. GitHub was already fully trusted. The new exposures are the gate repository's write access and any agent integration mistakenly granted on it; the runbook audits both.
7. **Loss events are broader.** Deleting AgePony, re-enrolling Face ID, or erasing the phone destroys the key. Recovery requires an owner recovery bootstrap, as for a lost FIDO key.
8. **No second key.** B″ also pinned a single key, but a FIDO key can be kept offline and apart from the phone. Here the key and the everyday phone are the same object, so theft of an unlocked phone with the passcode known is a signing compromise until the key is replaced.

**Assessment.** These differences mean the profile is **not** at least as strong as B″ on every property. It matches B″ on non-exportability (per source and ceremony), device binding, payload binding, domain separation for FAR, replay, malleability handling, canonical encoding, the trusted key source, gate semantics, fail-closed behaviour and statelessness. It is weaker on differences 1–3. Differences 4–6 change the mechanism without weakening resistance to any adversary the design resists. Difference 7 affects availability only. Difference 8 keeps B″'s structure (possession plus a secret: phone plus passcode, like FIDO key plus PIN) but carries more practical exposure, because the signer is the everyday phone. Differences 1–3 are **unavoidable** with plain SSHSIG from AgePony. No iPhone-only, $0 alternative without a hardware key was found that provides them: an own iOS app using App Attest or a Secure Enclave key with a per-use access control needs a paid Apple developer account or a Mac, and platform passkeys give attested presence only by being synced and escrowed (B‴). That search was not exhaustive; an overlooked free signer would reopen differences 1 and 2. It is materially stronger than B‴ on key custody and recovery exposure (no cloud-escrowed key) and on gate cost, and weaker than B‴ only in not attesting presence.

## B‴ as historical evidence

B‴ (WebAuthn with an iCloud Keychain passkey, commit `cb913a9c21262ef2772a6805a0d3c4ce14ab7cd6`, patch SHA-256 `6e0be71397e2a7dcd93c08220a3f58e89f61c0216e1cd3ff4c942b4fa65b3eb7`) was built and tested but not adopted. The passkey is synced and escrowed by Apple and recoverable through account recovery, it attests nothing (`none`, zero AAGUID), and it needed an authorizer page served from the App host plus DNS and a web CA. It is preserved outside the repository as development evidence only. No part of its WebAuthn machinery is used here.

## Unknowns to close by the live probes

- Everything in [the reconciliation](#reconciliation-with-the-current-release-2026-09-25) marked unverified. This is a precondition, not a probe: key generation waits for an audited release.

- Exact AgePony UI labels (for example the identity-type name) and whether Quick Look displays a `.json` file as text. The P0 rehearsal settles both before anything is pinned.
- Whether GitHub's branch-protection page in iOS Safari offers the App as the required check's source. The step-9 audit reads back the resulting `app_id`, so a wrong result is detected, not assumed.
- Real scheduling delay of the gate workflow. It affects latency only, never the decision.
