# Repository Red-Team Audit — 2026-09-23

Status: **Research — adversarial audit; no theory mutation and no status promotion**

Target: `main@7fb4816e4aa53aed749b7008b46ba9393d3d29b2`; remediation in PR #538.

Reviewer: Claude Code session, an AI agent with repository write access. This is an I0 author-side record, not independent review.

## Purpose

Look for failures that the existing assurance surfaces do not already expose: soundness gaps in executable verifiers, evidence that cannot discriminate between hypotheses, and CI trust weaknesses. Findings already disclosed elsewhere are listed with their existing disclosure and are not re-counted as new.

## Verification performed

- `make health-fast`, `make test-fast`, `make docs-check`, `make links-check`, `make semantic-check`, `make research-check`, the W4/W5/W6 campaign checkers, the commercial package tests, and the test-weakening gate against `main`. Results for each commit are reported in PR #538.
- Lean 4.19.0 could not be downloaded in the audit environment (network policy 403). The `FAR-CORE v1.1 Formalization` workflow is green on the PR heads. `mechanization/lean/` contains no `sorry`, `admit`, or custom `axiom`.

## Findings and dispositions

### RT-1 — baseline `far-ir/2.0` success does not mean verified (fixed for current surfaces)

The frozen baseline verifier (`contract_v2.py`) recomputes factorization, collision, and quotient claims only for `CHECKED_FINITE_EXPLICIT` evidence (specification section 9, Stage 3). Take `research/results/pca-w4-domain-contracts/argumentation-repaired.json` with the registered W6 mutation applied. It yields `FACTORIZATION_FAILURE`, but changing only `report.evidence.status` to `DECLARED_UNCHECKED` makes the same colliding `PROVED` record return `success = True`.

Disposition: `contract_v2_strict.py` is now the authoritative verifier for every current surface, under the [current verification rule](../specification/far-ir-2.0-current-verification.md). It rejects such records with `DETERMINATE_OUTCOME_UNCHECKED`. The baseline stays byte-identical for `PCA-W6` and `EFR-001` v1.0 provenance. `verifier_authority.py` registers the only files permitted to use the baseline, and `tests/test_contract_v2_verifier_authority.py` fails on any other import, dynamic load, or CLI invocation. `LIM-047`.

### RT-2 — the commercial exact-sufficiency gate accepted contradicted records (new; fixed)

`far_decision_integrity.semantic_audit` loaded the baseline verifier for `far-ir/2.0`, so an unchecked `PROVED` factorization whose own tables collide was classified `SATISFIES` and could clear `--require-semantic-contract`. A regression test reproduced this (`SATISFIES`) before the fix. The bridge now loads `contract_v2_strict`, which rejects the record as `INVALID`, and binds the baseline as a shared artifact.

### RT-3 — the strict loader read the file twice (new; fixed)

The first remediation's `load_and_validate_strict` parsed the file once for the baseline and again for the strict rule, so the two rule sets could apply to different byte snapshots. It also crashed on non-UTF-8 input. The loader now reads and parses once and validates that single document. Snapshot-switching regression tests fail against the double-read code and pass against the fix.

### RT-4 — W6 cannot discriminate beyond implementation correctness (partly disclosed)

The registered mutation creates exactly the collision the verifier and oracle check, and the schema baseline cannot see table values, so 0/6 versus 6/6 was fixed by construction. `02-execution-and-results.md` already concedes the mutation targets the verifier's condition, and `LIM-043` records project authorship. The README now calls W6 a regression control.

### RT-5 — `EFR-HD1`/`EFR-U1`/`EFR-C1` had no active comparator (new; resolved prospectively)

The FAR arm received the verifier report and the standard arm received no machine output. For finite explicit tables that report states the answer. The [comparator amendment v2.0](../governance/external-falsification-and-replication-comparator-amendment-v2.0.md) makes the v1.0 tests `SUPERSEDED_NOT_EXECUTABLE`. It registers `EFR-HD2`/`EFR-U2`/`EFR-C2`, whose primary contrast is FAR against a frozen generic table-consistency checker, and binds the H1/A1 machine lane to the strict verifier. v1.0 and v1.1 objects are verified byte-identical. `LIM-048`.

### RT-6 — v1.0 U1 analysis invalidates correctly run studies by chance (new; resolved for U2)

The frozen v1.0 U1 loop declares the whole test `INVALID_UNESTIMABLE_RESAMPLE` if any of 10,000 crossed resamples draws only zero-weight workers for an arm. Simulating that loop on correctly executed synthetic studies gave `INVALID` in 40/40 studies with 5 workers per site, 19/40 with 10, 8/40 with 20, and 3/40 with 40. U2 instead resolves such a resample against FAR (FAR rate 1, comparator and standard rate 0) and reports the count, so chance can only make a FAR-specific pass harder.

### RT-7 — core mathematics is correct but elementary (disclosed)

Already recorded by the [FAR core epistemic calibration audit](far-core-epistemic-calibration-v1.0.md): FAR-CORE-010 frame independence and FAR-CORE-013 hold by `rfl`, FAR-CORE-007/008 compare declared counts with `decide`, and FAR-CORE-001/002/004 are standard kernel-factorization and quotient facts. The README now points to that audit beside the terminal verdict.

### RT-8 — the W1 reviewer was one OpenAI Codex agent (disclosed)

Recorded by `LIM-035`. The README W1 paragraph now names the reviewer.

### RT-9 — validation signing material reaches candidate code (new; repaired pending owner-signed authorization)

- `validator-assurance.yml` `merge-authority` runs on `pull_request` with `FAR_VALIDATION_CACHE_SIGNING_KEY: ${{ secrets.FAR_VALIDATION_CACHE_SIGNING_KEY || github.token }}`.
- `exact-head-assurance.yml` sets that variable to the live `github.token` for every step, even though its checkout uses `persist-credentials: false` specifically to keep the token away from candidate code.
- `far_validation/assured_engine.py` forwards the variable into every check subprocess.

Because the whole job executes candidate code, subprocess filtering alone cannot protect a persistent key. The repair removes the secret and the token fallback and derives a masked `openssl rand -hex 32` key per job in both lanes. It also checks out with `persist-credentials: false`, because `merge-authority` previously left the job token in `.git/config` where candidate code could read it. `tests/test_ci_merge_gate_hardening.py` pins this.

The key no longer outlives its job, so forwarding it to check subprocesses exposes nothing that the job's own candidate code could not already read. `far_validation/assured_engine.py` is therefore left unchanged; changing it would cost one more protected transition and add no boundary. The certificate signed with this key binds evidence within one job. It is not a trust boundary against the candidate that runs in that job. Whether the persistent secret is still configured is Unknown; if it is, the owner should delete it. `LIM-049`.

### RT-10 — mutable Lean acquisition in protected workflows (new; repaired pending owner-signed authorization)

The two unprotected Lean workflows now run a commit-pinned, SHA-256-verified `elan-init.sh`, but that script still fetches the latest elan release and elan resolves the toolchain. The protected `lean.yml`, `validator-assurance.yml`, and `exact-head-assurance.yml` still pipe `elan/master/elan-init.sh` into `sh`. A CI measurement bound the direct release archive `lean-4.19.0-linux.tar.zst` to SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe` (343,842,845 bytes; the binary reports Lean 4.19.0, commit `6caaee842e94`). That digest was first one trust-on-first-use observation from GitHub's CDN. On 2026-09-27 a second download from a different network location returned the same 343,842,845 bytes and digest. Both observations come from the same CDN origin, so they are not independent.

The repair installs that archive directly in `lean.yml`, `validator-assurance.yml` and `exact-head-assurance.yml`, and in the two unprotected Lean workflows, `far-core-v11-formalization.yml` and `pca-w5.yml`. The digest is verified before extraction, and no installer script or toolchain resolver runs. Every Lean compile in those five workflows fails on a `declaration uses 'sorry'` warning. `pca-w5.yml` previously had no such check. The PCA-W5 current-state supplement declares its workflow change. Every action in those three workflows is pinned to the commit its tag named on 2026-09-27; these are the same commits recorded below, so behavior does not change. `LIM-049`.

### RT-11 — the anti-self-repin gate cannot authorize its own waiver file (new; superseded by owner-signed repins)

`far_validation.weakening` requires every change to a base-protected artifact to be pre-authorized by the comparison base's `validation/test-weakening-waivers.json`. That file is itself protected. Adding any authorization therefore changes a protected file whose own transition no base authorization covers.

Reproduced: a branch off `main` adding one authorization fails with “a candidate may not authorize its own protected-artifact repin”. The only existing authorization commit (`7e7904c1`, 2026-08-10) was a direct edit to `main` made before the gate existed (`f8edfced` arrived with PR #436). No protected transition was possible through the governed PR path.

Superseded: the protected-repin bootstrap (#551) replaced base-waiver authorization with owner-signed, single-use authorizations. They are appended to the unprotected `validation/protected-repin-consumptions.json` and judged by the App-bound `protected-repin-gate` (`docs/governance/protected-repin-procedure.md`). PR #560 makes the in-CI weakening check honor them. The deadlock no longer blocks a governed protected transition.

### RT-12 — assurance apparatus mostly verifies self-description (structural observation)

About 190k Markdown lines, 92k Python lines, 888 JSON files, 143 `check_*` tools, and about 2,600 SHA-256 pins, against about 3k Lean lines. Hash pins and prose-presence tests detect drift; they cannot detect an incorrect claim that its author re-hashes. No change is proposed here.

## Protected transition in this PR (owner-signed)

The files below are protected by `validation_bootstrap/assurance-lock.json`. Each changed pin is a protected transition that needs one owner-signed authorization bound to this PR. The `protected-repin-gate` App check lists the exact old and new digests for the current head. Per the owner's integration order, these authorizations are requested only after live probe P7 has passed.

| Path | Change |
|---|---|
| `.github/workflows/validator-assurance.yml` | RT-9 per-job ephemeral key and `persist-credentials: false`; RT-10 digest-bound Lean archive and commit-pinned actions. It also carries the root-of-trust audit's R14 (#548, `LIM-050`). `merge-authority` now runs after a failed dependency (`if: ${{ !cancelled() }}`) and fails unless the signed-cache chain succeeded, because GitHub counts a skipped required check as passing. `assurance-hash-audit` now fails on lock drift instead of only recording it. A `sorry` warning fails the Lean assurance step. |
| `.github/workflows/lean.yml` | Read-only token; digest-bound Lean archive; commit-pinned actions; `persist-credentials: false`. Every governed compile now fails on `declaration uses 'sorry'`, which `lean` reports only as a warning. |
| `.github/workflows/exact-head-assurance.yml` (mirror, not locked) | Identical key, checkout, Lean and pin changes, preserving the mirror contract in `tests/test_exact_head_assurance_workflow.py`. |
| `validation_bootstrap/assurance-lock.json` | Repins the two protected workflows. |

### RT-13 — a repository tool can drop the App-bound merge authority (new; repaired pending owner-signed authorization)

`tools/configure_validation_protection.py` wrote `main`'s protection with required checks exactly `[merge-authority]`. Since the bootstrap, the only merge authority is the App-bound `protected-repin-gate` required check, so running the tool would silently remove it. `tools/check_validation_protection.py` required the same stale set, so its read-back would have called the weakened state compliant.

The deployed gate's own protection audit had the matching gap. `far_validation/repin_protection_audit.py` accepted the absence of the gate context, a bootstrap-period rule that became permanent once the App check was bound. It could not notice the binding being removed.

The two legacy workflows are `disabled_manually` and their admin token is revoked, so this was not exploitable from CI. It was reachable from any local run with an owner token, or by re-enabling a workflow. The repair removes the dangerous path instead of relying on the workflows staying disabled:

- The configurator is an inert tombstone. It makes no API call and exits 2, and the disabled workflows that invoke it fail closed. A locked file cannot be removed through the repin gate.
- The read-back requires `--gate-app-id`. It fails unless `merge-authority` is bound to GitHub Actions (15368) and `protected-repin-gate` to the given App.
- The audit defaults to the bound-state check (`repin_gate_app.check_protection`). The bootstrap rule stays only behind an explicit `--bootstrap`, for a first bootstrap or an App rotation. It takes effect in the deployed gate after the owner redeploys at a `main` commit that contains it.

Tests: the read-back rejects the configurator's old policy and a gate bound to any other App; the configurator exits 2 without network code; the default audit rejects a dropped or re-bound gate. The new audit tests fail against the previous `repin_protection_audit.py`.

### RT-14 — candidate code could rewrite the locked validator's verdict in `merge-authority` (new; repaired pending owner-signed authorization)

`merge-authority` ran `python -m far_validation`, which puts the checkout first on `sys.path`. Two reproduced attacks followed:

- a top-level `json.py` that registers `atexit(os._exit(0))` made `far_validation weakening` print `Result: FAIL` and exit 0, so the step passed;
- an unchecked-hash `far_validation/__pycache__/__main__.<tag>.pyc` replaced the locked `__main__` even under `python -I`.

Separately, the job installed the candidate's `requirements.txt` and ran its tests before the bootstrap check, the weakening check, the oracle, the formal model, and the Lean proof. Candidate code that runs in a job can rewrite every later step through `GITHUB_PATH`, `GITHUB_ENV` or site-packages.

Repair, in both `merge-authority` and its exact-head mirror:

- The checks that need no candidate code now run first: `validation_bootstrap/verify.py`, the oracle, weakening, the formal model, and the Lean install plus `ValidationEngine.lean`. They run before any `pip install`, test or checker, so a failure there cannot be undone later.
- They run through `python -I -X pycache_prefix=… validation_bootstrap/run_isolated.py`. That launcher adds the checkout after the standard library and site-packages, and ignores committed bytecode.
- `verify.py` and the inline scripts use `python -I`. The assurance-lock workflow contract now requires the isolated forms.

`tests/test_ci_merge_gate_hardening.py` pins this. It checks the step order and isolation in both jobs, and it runs the launcher against a planted `json.py` and planted bytecode (with a control showing `python -m` is subverted).

Residual, inherent: steps that must run candidate code (the test suite, the checkers, the mutation campaign) and every step after them stay candidate-controlled. That is why `docs/governance/protected-repin-procedure.md` treats `merge-authority` as ordinary CI and the App-bound `protected-repin-gate` as the only merge authority. The bootstrap, weakening, oracle, formal-model, and Lean-proof verdicts are no longer part of that residual.

Not changed, with reasons:
- `far_validation/assured_engine.py`: see RT-9.
- `canonical-branch-protection.yml` and `configure-validation-protection.yml`: both are live-verified `disabled_manually`, and their admin token was retired (`theory/evaluation/privileged-token-retirement-v1.0.json`). Pinning their actions would buy no protection for two more signatures. The tool they run is now inert, and the read-back requires the App binding (RT-13), so re-enabling them cannot drop the gate.

`tests/test_ci_merge_gate_hardening.py` pins each repair. Ten reintroduced defects (dropped `!cancelled()`, inverted guard, hash audit exiting 0, secret as key, unmasked key, persisted credentials, piped `elan/master`, unchecked digest, removed `sorry` gate, tag-pinned action) were each caught by the intended test. Restoring the elan installer in the two unprotected workflows fails the archive and `sorry`-gate tests.

Action pins, resolved on 2026-09-23 and re-resolved unchanged on 2026-09-27: `actions/checkout` v4.4.0 `11d5960a326750d5838078e36cf38b85af677262`, `actions/setup-python` v5.6.0 `a26af69be951a213d495a4c3e4e4022e16d87065`, `actions/upload-artifact` v4.6.2 `ea165f8d65b6e75b540449e92b4886f43607fa02`, `actions/download-artifact` v4.3.0 `d3f86a106a0bac45b974a628896c90dbdf5c8093`. The SWE-agent workflows are sealed historical experiment evidence and are excluded.

## Nonclaims

This audit does not refute or promote any claim, theorem, campaign result, or status. It is not independent review. Absence of further findings is not evidence of their absence.
