# Presenting FAR — Research Continuation Freeze v1

Status: **NONCANONICAL research-continuation freeze.**

This freeze fixes a noncanonical live-research baseline so that a later session
resumes from the reconstructed state instead of restarting. It is **not** a
theory freeze under
`docs/governance/evidence-replication-and-freeze-standard-v1.0.md`, and it
constitutes neither Acceptance nor Promotion. It confers no evidence class on
anything.

Any material change to the reconstructed theory state produces a successor
research-state version (`v2`, …). This record is never amended in place.

## Frozen identity

| Field | Value |
|---|---|
| Freeze date | 2026-08-14 |
| Repository | `notfoundout/Project-FAR` |
| Branch | `claude/far-live-theory-reconstruction-1l3dqm` |
| Repository commit | `de5f1b23dc53e2633c67d73d86d1899444c3b548` |
| Repository root tree | `bb3bcde2f65c3ca72f9b68624cf882ef9558fe48` |
| Canonical baseline | `origin/main` tip `4bc964fd5fc8597158e73b4f94ecb76df5652433` |

The frozen repository commit is the state the reconstruction was reconciled
against. Git's content-addressed tree SHA is itself the recursive digest; any
single-byte change anywhere is mechanically detectable via
`git diff --stat de5f1b23 <candidate>`.

## Frozen research inputs

| Artifact | Digest |
|---|---|
| `.far/inbox/presenting-project-far.md` (SHA-256) | `bb57422dd2d4de28e5f78a54e4d5c059c607690e65033f8b901a1ef2f821abce` |
| `.far/inbox/presenting-project-far.md` (git blob) | `428e8ec6d610aaaceab7dec35a38dc36d5952eec` |
| Live target/issue ledger (`live-theory-state.json`) | `6e8f7ffc8c9f6ba535ec8c8b1bda30e247c95ade793d7ebe450914d5a242b65e` |
| Calibration report (SHA-256) | `393936bc3ad8859e8212b0527065e458146f2a864b0dcd6d042a31ec4f16e002` |
| Calibration preregistration digest | `6e03129580bbd98bd5010819da3c5405a4e7e91c56f059b2af6066e833651374` |

The ledger digest is reproducible: `python tools/build_presenting_far_live_state.py`
rebuilds it deterministically from the reconstruction plus the recorded
NOT_RECOVERED search results.

## Frozen protocol versions

| Component | Version |
|---|---|
| Ledger schema | `far-adversarial-ledger/1` |
| Evidence schema | `far-adversarial-evidence/1` |
| Prompt/protocol | `far-adversarial-protocol/1` |
| Calibration | `far-adversarial-calibration/1` |

## Source identities

| Lane | Provider | Model | Configuration |
|---|---|---|---|
| Reconstruction lane | Claude Code noninteractive (`claude -p`) | `claude-opus-5` | all tools denied; cwd sandboxed outside the repository |
| Adversarial lane | OpenAI HTTP API | `gpt-5` (default) | **unavailable this run** — `LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED` |

## Recovered exact artifacts

Per `recovery-ledger.md`: the Turn 33 concession block is
`RECOVERED_PARTIALLY` as verbatim text truncated mid-sentence. Every other
Presenting FAR protocol identifier is `NOT_RECOVERED` or
`RECOVERED_PARTIALLY` at the level of a summary only.

## Live target ledger at freeze

| Target | Status | Authorized |
|---|---|---|
| `PFAR-S1` | `READY_UNDER_INTERNAL_PROTOCOL` | no — internally closed, do not restart |
| `PFAR-T1-T8` | `SOURCE_REQUIRED` | no |
| `PFAR-E0` | `SOURCE_REQUIRED` | no |
| `PFAR-RC1` | `REFUTED` | no |
| `PFAR-RC2` | `UNDERDETERMINED` | no |
| `PFAR-SRB2` | `SOURCE_REQUIRED` | no |
| `REPO-UPP-SR-001-W1` | `OPEN` | yes |
| `REPO-UPP-SR-001-W2` | `OPEN` | yes, blocked behind `SR-W1` |

14 issues are registered. 10 are terminal-defeated (1 withdrawn, 9 conceded);
the 5 RC2 repair obligations remain live under an unrecoverable resolution.

## Unresolved obligations at freeze

1. External recovery of `𝔈₀`, `T1`–`T8`, the frozen `S1` statement, `SR-B2 v2`,
   `NM-v1`, `K-P1`, `FDI-v1`, `CDE-v1`, `FDI1`–`FDI5`.
2. Whether the five Turn 17 `RC2` repairs were discharged (Turns 18–22 `GAP`).
3. The truncated final clause of Turn 33.
4. GPT credentials for the adversarial lane.
5. `CAL-DI3-S1` group 1 (the intra-sequent/frontier level distinction) was
   **missed** on the sandboxed calibration run.
6. Every canonical obligation listed in `repo-research-delta.md`, unchanged.

## Explicit nonclaims

- This freeze does not make any reconstructed content canonical.
- `READY_UNDER_INTERNAL_PROTOCOL` for `PFAR-S1` is not Acceptance.
- Claude and GPT surviving each other is not independent validation, not
  external replication, and not evidence of theory correctness.
- No canonical register, matrix, or status surface was modified.
