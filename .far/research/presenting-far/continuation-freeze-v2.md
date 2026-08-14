# Presenting FAR — Research Continuation Freeze v2

Status: **NONCANONICAL research-continuation freeze.** Successor to
`continuation-freeze-v1.md`, which is preserved unamended as the historical
record of the pre-audit state.

This freeze constitutes neither Acceptance nor Promotion and confers no evidence
class on anything.

## Why a successor version

The executor was audited at `9551f424c3a74571e313d27787f66e601ea0d722` and
repaired (see `executor-audit-repair-v1.md`). The repairs changed the ledger
schema and the meaning of several recorded states, so the v1 digests no longer
describe the current baseline. Per the v1 record's own rule, that produces a
successor version rather than an amendment.

**No reconstructed research content changed.** The transcript, the recovery
classification, and the Turn 33 findings are identical. What changed is how the
executor represents them:

- `DI3`'s defeat is now recorded with its actual lifecycle — Claude raised it,
  GPT rebutted, Claude withdrew — rather than GPT sustaining and Claude
  conceding, which misattributed standing.
- The Turn 33 corrections (intra-sequent/frontier, DF-02b weakening) moved from
  registered objections *against S1* to recorded supporting material on S1.
  They were corrections to Claude's defeated argument, not standing objections
  to the target.
- `PFAR-S1`'s READY is now marked `RECORDED_TRANSCRIPT_DISPOSITION`.
- Unrecovered artifacts became first-class blocking `Obligation` objects.
- `SR-W2`'s dependency on `SR-W1` became a typed edge requiring an established
  disposition.

## Frozen identity

| Field | Value |
|---|---|
| Freeze date | 2026-08-14 |
| Repository | `notfoundout/Project-FAR` |
| Branch | `claude/far-live-theory-reconstruction-1l3dqm` |
| Audited predecessor commit | `9551f424c3a74571e313d27787f66e601ea0d722` |
| Canonical baseline | `origin/main` tip `4bc964fd5fc8597158e73b4f94ecb76df5652433` |

## Frozen research inputs

| Artifact | Digest |
|---|---|
| `.far/inbox/presenting-project-far.md` (SHA-256) | `bb57422dd2d4de28e5f78a54e4d5c059c607690e65033f8b901a1ef2f821abce` |
| `.far/inbox/presenting-project-far.md` (git blob) | `428e8ec6d610aaaceab7dec35a38dc36d5952eec` |
| Live target/issue/obligation ledger | `91fa591145d29ebae5ebd9a79ae2f2ca3b10d7ddc1f6b1e87759503052388b35` |
| Calibration preregistration digest | `6e03129580bbd98bd5010819da3c5405a4e7e91c56f059b2af6066e833651374` (unchanged from v1) |

The ledger digest is reproducible with
`python tools/build_presenting_far_live_state.py`, and now excludes wall-clock
fields so it is stable across days.

## Frozen protocol versions

| Component | v1 | v2 |
|---|---|---|
| Ledger schema | `far-adversarial-ledger/1` | `far-adversarial-ledger/2` |
| Reducer | (unversioned) | `far-adversarial-reducer/2` |
| Evidence schema | `far-adversarial-evidence/1` | `far-adversarial-evidence/1` |
| Prompt/protocol | `far-adversarial-protocol/1` | `far-adversarial-protocol/2` |
| Calibration | `far-adversarial-calibration/1` | `far-adversarial-calibration/1` |

Replay refuses to reconstruct a run recorded under a different reducer, ledger
schema, or protocol version unless migration is requested explicitly.

## Campaign source

**Unregistered.** No `campaign.json` exists, so `run` refuses to start. This is
deliberate: the current `HEAD` is never adopted as a campaign source implicitly.

## Live target ledger at freeze

| Target | Status | Basis | Authorized |
|---|---|---|---|
| `PFAR-S1` | `READY_UNDER_INTERNAL_PROTOCOL` | recorded | no — internally closed, do not restart |
| `PFAR-T1-T8` | `SOURCE_REQUIRED` | recorded | no |
| `PFAR-E0` | `SOURCE_REQUIRED` | recorded | no |
| `PFAR-RC1` | `REFUTED` | recorded | no |
| `PFAR-RC2` | `UNDERDETERMINED` | recorded | no |
| `PFAR-SRB2` | `SOURCE_REQUIRED` | recorded | no |
| `REPO-UPP-SR-001-W1` | `OPEN` | derived | yes |
| `REPO-UPP-SR-001-W2` | `OPEN` | derived | yes, edge unsatisfied |

12 issues: 1 withdrawn (`DI3`), 6 upheld against `PFAR-RC1`, 5 live against
`PFAR-RC2`. 6 obligations, all unresolved and blocking.

## Unresolved obligations at freeze

1. External recovery of `𝔈₀`, `T1`–`T8`, the frozen `S1` statement, `SR-B2 v2`,
   `NM-v1`, `K-P1`, `FDI-v1`, `CDE-v1`, `FDI1`–`FDI5`.
2. Whether the five Turn 17 `RC2` repairs were discharged (Turns 18–22 `GAP`).
3. The truncated final clause of Turn 33.
4. GPT credentials for the adversarial lane.
5. `CAL-DI3-S1` group 1 was **missed** on the sandboxed calibration run. The
   case, its digest, and the miss are unchanged and test-pinned.
6. The effect of the Presenting FAR line on canonical `OP-01`/`OP-02`/`OP-03`
   is undetermined; see `repo-research-delta.md`.
7. Every canonical obligation listed in `repo-research-delta.md`, unchanged.

## Explicit nonclaims

- This freeze does not make any reconstructed content canonical.
- `READY_UNDER_INTERNAL_PROTOCOL` for `PFAR-S1` is not Acceptance, and it is a
  transcribed disposition rather than one this executor derived.
- Claude and GPT surviving each other is not independent validation, not
  external replication, and not evidence of theory correctness.
- Passing the repaired executor's own tests is not evidence about Project FAR
  theory. It is evidence about the executor.
- No canonical register, matrix, or status surface was modified.
