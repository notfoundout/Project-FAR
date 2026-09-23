# Repository Red-Team Audit — 2026-09-23

Status: **Research — adversarial audit; no theory mutation and no status promotion**

Target: `main@7fb4816e4aa53aed749b7008b46ba9393d3d29b2`

Reviewer: Claude Code session, an AI agent with repository write access. This is an I0 author-side record, not independent review.

## Purpose

Look for failures that the existing assurance surfaces do not already expose: soundness gaps in executable verifiers, evidence that cannot discriminate between hypotheses, and CI trust weaknesses. Findings already disclosed elsewhere are listed with their existing disclosure and are not re-counted as new.

## Verification performed

- `make health-fast`: pass. `make test-fast`: 1,955 tests, OK.
- Lean 4.19.0 could not be installed locally: the environment's network policy returned 403 for the toolchain download. The `FAR-CORE v1.1 Formalization` workflow is green on the target commit (run `35927334158`), and `mechanization/lean/` contains no `sorry`, `admit`, or custom `axiom`.

## Findings

### RT-1 — baseline `far-ir/2.0` success does not mean verified (new; executable reproduction)

The frozen baseline verifier (`contract_v2.py`) recomputes factorization, collision, and quotient claims only for `CHECKED_FINITE_EXPLICIT` evidence (specification section 9, Stage 3). Starting from `research/results/pca-w4-domain-contracts/argumentation-repaired.json`, the registered W6 mutation yields `FACTORIZATION_FAILURE`. Changing only `report.evidence.status` to `DECLARED_UNCHECKED` makes the same colliding record, still with outcome `PROVED`, return `success = True` with no diagnostics, while the W6 table-only oracle reports a material collision.

The W6 detection result therefore holds only for records whose author declares checked evidence. The baseline is git-blob pinned as the `PCA-W6` protocol base and frozen as the `EFR-001` baseline command, so it is not edited. The opt-in `mechanization/far_mechanization/contract_v2_strict.py` rejects any `PROVED`/`REFUTED` outcome without checked evidence (`DETERMINATE_OUTCOME_UNCHECKED`); `tests/test_far_contract_v2_strict.py` reproduces the gap and pins the fix. Recorded as `LIM-047`.

### RT-2 — W6 cannot discriminate beyond implementation correctness (partly disclosed)

`inject_registered_collision` copies one case's representation value onto another case with different behavior. The FAR lane is a decoder-table functionality check, the oracle tests the same pairwise pattern, and the schema baseline cannot inspect table values. The 0/6 versus 6/6 outcome was fixed by construction unless the code was defective. `02-execution-and-results.md` already states that the mutation targets the verifier's condition, and `LIM-043` records project authorship; the README now also states that this is a regression control, not a detection-power estimate.

### RT-3 — `EFR-HD1`/`EFR-U1` have no active comparator (new; design-level)

The FAR arm receives the verifier report; the standard arm receives no machine output. For complete finite explicit tables, material loss is a table collision, so the report effectively supplies the answer. A registered pass would not separate FAR-specific benefit from access to any determinate collision check. The v1.0 preregistration is frozen and is not edited here; a comparator arm requires a new program version and a complete new freeze before execution. Recorded as `LIM-048`.

### RT-4 — core mathematics is correct but elementary (disclosed)

Already recorded by the [FAR core epistemic calibration audit](far-core-epistemic-calibration-v1.0.md): FAR-CORE-010 frame independence and FAR-CORE-013 hold by `rfl`, FAR-CORE-007/008 compare declared counts with `decide`, and FAR-CORE-001/002/004 are standard kernel-factorization and quotient facts. The README now points to that audit beside the terminal verdict.

### RT-5 — the W1 reviewer was one OpenAI Codex agent (disclosed)

Recorded by `LIM-035` and the W1–W6 matrix. The README W1 paragraph now names the reviewer.

### RT-6 — persistent validation signing key reaches candidate code (new; security)

`validator-assurance.yml` `merge-authority` runs on `pull_request` with `FAR_VALIDATION_CACHE_SIGNING_KEY: ${{ secrets.FAR_VALIDATION_CACHE_SIGNING_KEY || github.token }}`, and `far_validation/assured_engine.py` `_subprocess_environment` forwards that variable to the checks it executes from the candidate tree. Code in a same-repository pull request can read a configured persistent key and forge HMAC attestations for later runs. Whether the secret is configured is Unknown. Both files are protected by `validation_bootstrap/assurance-lock.json`; changing them requires a repin authorization already merged into the comparison base. Recorded as `LIM-049`.

### RT-7 — unpinned Lean installer (new; supply chain; partly fixed)

Five workflows piped `elan/master/elan-init.sh` into `sh`. `far-core-v11-formalization.yml` and `pca-w5.yml` now download the installer from elan commit `0e36a07b9bbcc5381fa6250df109f9a4f94d7bac` and verify SHA-256 `a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53` (byte-identical to the script CI previously ran). That script still fetches the latest elan release binary, so the binary remains unpinned. `lean.yml`, `validator-assurance.yml`, and `exact-head-assurance.yml` (which must mirror `merge-authority`) are protected and unchanged. Actions are pinned by tag, not commit SHA. Recorded as `LIM-049`.

### RT-8 — assurance apparatus mostly verifies self-description (structural observation)

About 190k Markdown lines, 92k Python lines, 888 JSON files, 143 `check_*` tools, and about 2,600 SHA-256 pins, against about 3k Lean lines. Hash pins and prose-presence tests detect drift; they cannot detect an incorrect claim that its author re-hashes. No change is proposed here.

## Nonclaims

This audit does not refute or promote any claim, theorem, campaign result, or status. It is not independent review. Absence of further findings is not evidence of their absence.

## Remaining work

1. Merge a repin authorization for `validator-assurance.yml`, `exact-head-assurance.yml`, `lean.yml`, and `far_validation/assured_engine.py`, then remove the persistent-secret fallback from candidate-executing jobs, stop forwarding the signing key to check subprocesses, and pin the installer there.
2. Pin the elan binary and Lean toolchain archive by checksum once release digests can be obtained.
3. Before executing `EFR-001`, register a new program version with an active comparator arm.
