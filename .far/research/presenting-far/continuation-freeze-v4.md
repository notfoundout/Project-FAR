# Presenting FAR — Research Continuation Freeze v4

Status: **NONCANONICAL research-continuation freeze.** Successor to v1, v2, and
v3, all preserved unamended. Constitutes neither Acceptance nor Promotion.

## Why a successor version

A material change to the recorded research state: a genuine
`AUTHORITY_CONFLICT` between current canonical authority surfaces was verified
and registered. v3's delta asserted that no such conflict existed; that
assertion was wrong and is withdrawn.

| Version | What changed |
|---|---|
| v1 | Original reconstruction. |
| v2 | Executor audit repair; ledger schema v1 → v2. No research content changed. |
| v3 | Recovery addendum ingested. |
| v4 | **This record.** `REPO-AUTHORITY-CONFLICT-001` registered; campaign source pinned. |

## The registered conflict

`README.md:14-16` and `docs/governance/central-research-program.md:19-21`
present `POST-TUE-UPP-001`'s terminal adjudication as a theorem proved with a
complete dependency audit. `docs/project-status.md:31-37`, dated 2026-08-13,
records that same derivation as `FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED` and
defective over part of its stated domain (`XA-001`–`XA-005`), and registers
`UPP-SR-001`/`OP-22` as the successor repair.

All three are current-authority surfaces, and `README.md` outranks
`project-status.md` in the navigation order `project-status.md` itself declares.
`FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED`, `bounded-v1`, `XA-001`,
`UPP-SR-001`, and `OP-22` each occur zero times in the two higher-ranked
surfaces.

Recorded, not resolved. Repair is a canonical documentation change requiring
separate governance authorization, and `AGENTS.md` §4 forbids choosing between
conflicting authorities. Registered as `REPO-AUTHORITY-CONFLICT-001`, status
`GOVERNANCE_DECISION_REQUIRED`, unauthorized.

The finding came from an independent parallel reconstruction of this same
investigation and was verified here directly against the files.

## Frozen identity

| Field | Value |
|---|---|
| Freeze date | 2026-08-14 |
| Repository | `notfoundout/Project-FAR` |
| Branch | `claude/far-live-theory-reconstruction-1l3dqm` (PR #452) |
| Predecessor freeze | `continuation-freeze-v3.md` (commit `3480a72b`) |
| Canonical baseline | `origin/main` tip `4bc964fd5fc8597158e73b4f94ecb76df5652433` |

## Frozen research inputs

| Artifact | Digest |
|---|---|
| `presenting-project-far.md` (SHA-256) | `bb57422dd2d4de28e5f78a54e4d5c059c607690e65033f8b901a1ef2f821abce` |
| `presenting-project-far-recovery-addendum-2026-08-14.md` (SHA-256) | `a65dc87ac20e68517313fb9d542dd3128350a7547b68e2ad7a10bf72a341d850` |
| Live ledger (v3 state, superseded) | `32b69eac2bbf574f2f499270b7fb75b8108ab2fd02351b37e3c38c607c48cacd` |
| Live ledger (**v4 state**) | `6fc00badad34a09a128e1329f6c674dfc082075671e3c8615694a11e45fb8b2f` |
| Calibration preregistration digest | `6e03129580bbd98bd5010819da3c5405a4e7e91c56f059b2af6066e833651374` (unchanged since v1) |

## Live target ledger at freeze

| Target | Status | Basis | Authorized |
|---|---|---|---|
| `PFAR-S1` | `READY_UNDER_INTERNAL_PROTOCOL` | recorded | no — internally closed, do not restart |
| `PFAR-S2` | `UNDERDETERMINED` | recorded | no |
| `PFAR-S6-S7` | `SOURCE_REQUIRED` | recorded | no |
| `PFAR-T1-T8` | `SOURCE_REQUIRED` | recorded | no |
| `PFAR-E0` | `SOURCE_REQUIRED` | recorded | no |
| `PFAR-RC1` | `REFUTED` | recorded | no |
| `PFAR-RC2` | `UNDERDETERMINED` | recorded | no |
| `PFAR-SRB2` | `SOURCE_REQUIRED` | recorded | no |
| `REPO-AUTHORITY-CONFLICT-001` | `GOVERNANCE_DECISION_REQUIRED` | derived | no |
| `REPO-UPP-SR-001-W1` | `OPEN` | derived | yes |
| `REPO-UPP-SR-001-W2` | `OPEN` | derived | yes, edge unsatisfied |

11 targets, 12 issues, 10 obligations. Issues unchanged since v2: 1 withdrawn
(`DI3`), 6 upheld against `PFAR-RC1`, 5 live against `PFAR-RC2`.

## Preserved dispositions

- `PFAR-S1` remains `READY_UNDER_INTERNAL_PROTOCOL` on a **recorded** basis.
  Not canonical Acceptance. Not restarted. Not re-derived.
- `DI3` remains `WITHDRAWN`, defeated by its owner after rebuttal. Attempting to
  re-sustain it raises `IssueReopenError`, verified this session.
- The six `PFAR-RC1` objections remain upheld; `PFAR-RC1` remains `REFUTED`.
- The five `PFAR-RC2` repair obligations remain live.

## Explicit nonclaims

- Registering an authority conflict does not resolve it and does not alter any
  canonical surface.
- Pinning a campaign source does not start a campaign.
- `READY_UNDER_INTERNAL_PROTOCOL` is not Acceptance.
- No canonical register, matrix, or status surface was modified.
