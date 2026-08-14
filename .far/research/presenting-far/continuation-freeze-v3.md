# Presenting FAR — Research Continuation Freeze v3

Status: **NONCANONICAL research-continuation freeze.** Successor to
`continuation-freeze-v1.md` and `continuation-freeze-v2.md`, both preserved
unamended. Constitutes neither Acceptance nor Promotion and confers no evidence
class on anything.

## Version numbering note

The instruction for this successor asked for "a v2." `v2` was already taken:
`continuation-freeze-v2.md` records the executor audit repair from the previous
session, and amending it in place would violate the same append-only rule this
freeze exists to honour. This successor is therefore **v3**. The two prior
records stand unaltered.

| Version | What it froze |
|---|---|
| v1 | The original reconstruction from `presenting-project-far.md`. |
| v2 | The same research content re-expressed after the executor audit repair (ledger schema v1 → v2). No research content changed. |
| v3 | **This record.** Research content changed: the recovery addendum is ingested. |

## Why a successor version

`.far/inbox/presenting-project-far-recovery-addendum-2026-08-14.md` supplied
recovered conversation-state evidence absent from the first reconstruction. It
is a material change to the reconstructed research state, so it produces a
successor rather than an amendment.

## Frozen identity

| Field | Value |
|---|---|
| Freeze date | 2026-08-14 |
| Repository | `notfoundout/Project-FAR` |
| Branch | `claude/far-live-theory-reconstruction-1l3dqm` |
| Predecessor freeze | `continuation-freeze-v2.md` (executor repair, commit `5323fb48`) |
| Addendum ingest commit | `26db5d37` |
| Canonical baseline | `origin/main` tip `4bc964fd5fc8597158e73b4f94ecb76df5652433` |

## Frozen research inputs

| Artifact | Digest |
|---|---|
| `presenting-project-far.md` (SHA-256) | `bb57422dd2d4de28e5f78a54e4d5c059c607690e65033f8b901a1ef2f821abce` |
| `presenting-project-far.md` (git blob) | `428e8ec6d610aaaceab7dec35a38dc36d5952eec` |
| `presenting-project-far-recovery-addendum-2026-08-14.md` (SHA-256) | `a65dc87ac20e68517313fb9d542dd3128350a7547b68e2ad7a10bf72a341d850` |
| `presenting-project-far-recovery-addendum-2026-08-14.md` (git blob) | `bd115f5da7874dddd2a754f98040898cbb1b1d41` |
| Live ledger (v2 state, superseded) | `91fa591145d29ebae5ebd9a79ae2f2ca3b10d7ddc1f6b1e87759503052388b35` |
| Live ledger (**v3 state**) | `32b69eac2bbf574f2f499270b7fb75b8108ab2fd02351b37e3c38c607c48cacd` |
| Calibration preregistration digest | `6e03129580bbd98bd5010819da3c5405a4e7e91c56f059b2af6066e833651374` (unchanged since v1) |

Reproduce the ledger digest with
`python tools/build_presenting_far_live_state.py`.

## What changed from v2

Research content, for the first time since v1:

- `SR-B2 v2` upgraded from a bare fact to a recoverable finite search procedure.
- `NM-v1`, `K-P1`, `FDI-v1`, `CDE-v1`, `DI1`–`DI6` upgraded to
  `RECOVERED_PARTIALLY`.
- Turn 24's precondition-stop semantics recovered.
- Turn 34's adjudication route partially recovered.
- Two new targets: `PFAR-S2` and `PFAR-S6-S7`.
- Two source identifications at `SOURCE-IDENTIFICATION-HIGH`.
- v1's "no occurrence anywhere" claim corrected to repository-scope only.

Unchanged: the Turn 33 verbatim excerpt, `DI3`'s withdrawal, `PFAR-S1`'s
recorded READY, `PFAR-RC1`'s refutation, and the five live `PFAR-RC2` repairs.

## Frozen protocol versions

| Component | Version |
|---|---|
| Research state | `v3` |
| Ledger schema | `far-adversarial-ledger/2` |
| Reducer | `far-adversarial-reducer/2` |
| Evidence schema | `far-adversarial-evidence/1` |
| Prompt/protocol | `far-adversarial-protocol/2` |
| Calibration | `far-adversarial-calibration/1` |

## Campaign source

**Unregistered.** No `campaign.json` exists, so `run` refuses to start. The
current `HEAD` is never adopted as a campaign source implicitly.

## Live target ledger at freeze

| Target | Status | Basis | Blocking obligations | Authorized |
|---|---|---|---|---|
| `PFAR-S1` | `READY_UNDER_INTERNAL_PROTOCOL` | recorded | 3 | no — internally closed, do not restart |
| `PFAR-S2` | `UNDERDETERMINED` | recorded | 1 | no |
| `PFAR-S6-S7` | `SOURCE_REQUIRED` | recorded | 1 | no |
| `PFAR-T1-T8` | `SOURCE_REQUIRED` | recorded | 1 | no |
| `PFAR-E0` | `SOURCE_REQUIRED` | recorded | 1 | no |
| `PFAR-RC1` | `REFUTED` | recorded | 0 | no |
| `PFAR-RC2` | `UNDERDETERMINED` | recorded | 0 | no |
| `PFAR-SRB2` | `SOURCE_REQUIRED` | recorded | 2 | no |
| `REPO-UPP-SR-001-W1` | `OPEN` | derived | 1 | yes |
| `REPO-UPP-SR-001-W2` | `OPEN` | derived | 0 | yes, edge unsatisfied |

10 targets, 12 issues, 10 obligations. Issues unchanged from v2: 1 withdrawn
(`DI3`), 6 upheld against `PFAR-RC1`, 5 live against `PFAR-RC2`.

## Unresolved obligations at freeze

1. Exact `𝔈₀`, `T1`–`T8`, and frozen `S1` statement — still unavailable, and
   binding: Turn 24 makes a precondition stop the correct outcome when they are
   missing, so no substitute is permitted.
2. Exact `S2` statement and disposition; exact `S6`/`S7` and the transition.
3. Exact `SR-B2 v2` protocol text and its six fixed queries; exact `DI1`–`DI6`;
   exact `FDI1`–`FDI5` clause mapping; exact `CDE-v1`.
4. Whether the five Turn 17 `RC2` repairs were discharged (Turns 18–22 `GAP`).
5. The truncated final clause of Turn 33.
6. GPT credentials for the adversarial lane.
7. `CAL-DI3-S1` group 1 was **missed** on the sandboxed run. Unchanged and
   test-pinned.
8. The effect of the Presenting FAR line on canonical `OP-01`/`OP-02`/`OP-03`
   remains undetermined.
9. Every canonical obligation in `repo-research-delta.md`, unchanged.

## Explicit nonclaims

- No reconstructed content becomes canonical here.
- The addendum is not a verbatim transcript and nothing in it may be quoted as
  one.
- `READY_UNDER_INTERNAL_PROTOCOL` for `PFAR-S1` is not Acceptance, and remains
  a transcribed disposition rather than one this executor derived.
- Recovering more of the protocol does not authorize restarting Presenting FAR.
- Claude and GPT surviving each other is not independent validation.
- No canonical register, matrix, or status surface was modified.
