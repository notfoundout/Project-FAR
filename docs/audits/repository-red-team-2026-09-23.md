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

### RT-9 — validation signing material reaches candidate code (new; NOT yet fixed)

- `validator-assurance.yml` `merge-authority` runs on `pull_request` with `FAR_VALIDATION_CACHE_SIGNING_KEY: ${{ secrets.FAR_VALIDATION_CACHE_SIGNING_KEY || github.token }}`.
- `exact-head-assurance.yml` sets that variable to the live `github.token` for every step, even though its checkout uses `persist-credentials: false` specifically to keep the token away from candidate code.
- `far_validation/assured_engine.py` forwards the variable into every check subprocess.

Because the whole job executes candidate code, subprocess filtering alone cannot protect a persistent key. The prepared replacement removes the secret and the token fallback, derives a masked `openssl rand -hex 32` key per job, stops forwarding the key to check subprocesses, and adds a regression test. It is not applied (see *Blocked protected transition*). Whether the persistent secret is configured is Unknown. `LIM-049`.

### RT-10 — mutable Lean acquisition in protected workflows (new; partly fixed)

The two unprotected Lean workflows now run a commit-pinned, SHA-256-verified `elan-init.sh`, but that script still fetches the latest elan release and elan resolves the toolchain. The protected `lean.yml`, `validator-assurance.yml`, and `exact-head-assurance.yml` still pipe `elan/master/elan-init.sh` into `sh`. A CI measurement bound the direct release archive `lean-4.19.0-linux.tar.zst` to SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe` (343,842,845 bytes; the binary reports Lean 4.19.0, commit `6caaee842e94`). That digest is one trust-on-first-use observation from GitHub's CDN; the audit environment could not fetch the asset to cross-check it. The direct, digest-bound install and commit-SHA action pins are not applied. `LIM-049`.

### RT-11 — the anti-self-repin gate cannot authorize its own waiver file (new; governance deadlock)

`far_validation.weakening` requires every change to a base-protected artifact to be pre-authorized by the comparison base's `validation/test-weakening-waivers.json`. That file is itself protected. Adding any authorization therefore changes a protected file whose own transition no base authorization covers.

Reproduced: a branch off `main` adding one authorization fails with “a candidate may not authorize its own protected-artifact repin”. The only existing authorization commit (`7e7904c1`, 2026-08-10) was a direct edit to `main` made before the gate existed (`f8edfced` arrived with PR #436). No protected transition is possible through the governed PR path; it needs an owner action outside the gate.

### RT-12 — assurance apparatus mostly verifies self-description (structural observation)

About 190k Markdown lines, 92k Python lines, 888 JSON files, 143 `check_*` tools, and about 2,600 SHA-256 pins, against about 3k Lean lines. Hash pins and prose-presence tests detect drift; they cannot detect an incorrect claim that its author re-hashes. No change is proposed here.

## Blocked protected transition

Every file below is protected by `validation_bootstrap/assurance-lock.json`, or must mirror a protected file. Changing them requires, first, a repin authorization for each exact old→new SHA-256 transition, merged into `main`. Per RT-11 that includes an authorization for the waiver file's own transition, which only the owner can land outside the gate.

| Path | Intended change |
|---|---|
| `far_validation/assured_engine.py` | stop forwarding `FAR_VALIDATION_CACHE_SIGNING_KEY` to check subprocesses |
| `.github/workflows/validator-assurance.yml` | remove the secret/`github.token` key; per-job ephemeral key step; digest-bound direct Lean install; action SHA pins |
| `.github/workflows/exact-head-assurance.yml` (mirror, not locked) | identical key, Lean, and pin changes, preserving the mirror contract |
| `.github/workflows/lean.yml` | digest-bound direct Lean install; action SHA pins |
| `.github/workflows/canonical-branch-protection.yml`, `.github/workflows/configure-validation-protection.yml` | action SHA pins (these jobs hold the admin token) |
| `validation_bootstrap/assurance-lock.json` | repin each changed protected file to its authorized digest |

Action pins resolved on 2026-09-23 to the commits the existing tags point at (no behavior change): `actions/checkout` v4.4.0 `11d5960a326750d5838078e36cf38b85af677262`, `actions/setup-python` v5.6.0 `a26af69be951a213d495a4c3e4e4022e16d87065`, `actions/upload-artifact` v4.6.2 `ea165f8d65b6e75b540449e92b4886f43607fa02`, `actions/download-artifact` v4.3.0 `d3f86a106a0bac45b974a628896c90dbdf5c8093`, `peter-evans/create-pull-request` v6.1.0 `c5a7806660adbe173f04e3e038b0ccdcd758773c`. The SWE-agent workflows are sealed historical experiment evidence and are excluded.

## Nonclaims

This audit does not refute or promote any claim, theorem, campaign result, or status. It is not independent review. Absence of further findings is not evidence of their absence.
