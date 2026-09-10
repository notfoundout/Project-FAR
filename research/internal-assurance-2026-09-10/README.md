# Internal assurance repair audit — 2026-09-10

Status: Research / maintenance evidence. No EFR execution or external evaluation.

## Audited state

Default branch `6a5aa1af92d738f480ab07affc1f5aa9e66e9dec`, tree
`c7728dc05dddc3d84481733c3e27a98632a609ab` passed all 30 uncached release checks.
Targeted reproductions nevertheless confirmed the defects below. The review
reconciliation has 402 source findings, two previously resolved and 400 awaiting
verification. This audit does not claim to have adjudicated all 400.

| Original finding | Observation on audited main | Repair boundary |
| --- | --- | --- |
| `PR231:PRRT_kwDOTH_vCM6ScNF9` | Direct files do not match globstars; another matching check prevents fallback and the intended check is omitted. | Reuse existing zero-directory glob expansion in selection. |
| `PR231:PRRT_kwDOTH_vCM6ScNF3` | Real subprocess timeouts leave bytes in both engines' output fields; JSON serialization fails. | Base engine corrected; assured engine repair remains protected and unapplied. |
| `PR232:PRRT_kwDOTH_vCM6Sd90_` | A real `R099` test rename with an assertion replaced by `pass` is accepted. | Candidate disables rename detection in the Python-strength path. |
| `PR232:PRRT_kwDOTH_vCM6Sd91A` | Directory-fd-relative reads disappear, including annotated repository fds. | Candidate uses `strace -yy`, resolves annotations, and rejects unresolved successful accesses. |
| `PR369:PRRT_kwDOTH_vCM6Ttjrh` | Metadata accepts NaN/infinities and serialization emits non-JSON values. | Reject non-finite metadata/serialization; preserve valid canonical bytes. |
| `PR151:PRRT_kwDOTH_vCM6PxMgL` | An investigation and claim sharing `C1` produce no duplicate diagnostic. | Include the investigation in the identifier map. |
| `PR151:PRRT_kwDOTH_vCM6PxMgM` | Invalid runtime graph node/edge kinds pass validation. | Validate both enums with the existing `FAR-IR-004` diagnostic. |

The new tests in `tests/test_internal_assurance_regressions.py` and
`tests/mechanization/test_canonical_ir.py` fail on the baseline and pass after the
unprotected repairs. The complete mechanization directory passes 53 tests. No
FAR-CORE statement, frozen campaign, W1–W6 result, or EFR input changes. Record
canonical closure only against an actual protected promotion commit.

## Protected candidate

- [Baseline observations](protected-baseline.json)
- [Candidate observations](protected-candidate.json)
- [Exact candidate patch](protected-repair.patch)
- [Actual repin rejection](protected-repin-rejection.json)
- [Standalone reproducer](reproduce_protected_defects.py)

The candidate removes all three reproduced protected defects and passes the nine
existing trace regression tests. It is proposed code, not a complete tracing
correctness certificate. The patch changes no lock, waiver, workflow, or live
protection setting.

Reproduce the baseline in an explicit checkout:

```bash
python research/internal-assurance-2026-09-10/reproduce_protected_defects.py \
  --root . --expect defective
```

Apply the patch only in a separate disposable worktree, then run the reproducer
with that worktree as `--root` and `--expect repaired`, plus its existing
`tests.test_validation_trace_regression` suite. `observation_matches: true` means
the requested observation was reproduced; it is not an assurance verdict. Source
digests bind observations to exact bytes.

## Demonstrated governance blocker

Bootstrap rejects the corrected assured engine with `FAR-VAL-BOOT-001: assurance
file hash mismatch`. A separate local negative control refreshed the three pins;
the weakening gate then rejected all three transitions. That rejection is retained
above. The negative-control commit and refreshed lock are not proposed for merge.

The current control chain is:

1. `validation_bootstrap/assurance-lock.json` pins the three affected files.
2. `far_validation/weakening.py` requires the comparison-base
   `validation/test-weakening-waivers.json` to authorize the exact old/new digests.
3. Existing grants cover historical PR #436 transitions only.
4. The authorization file is itself pinned, with no grant for changing it.
   A candidate cannot authorize itself.

No currently authorized in-repository transition covers these repairs. Do not
evade this by splitting pins from code, renaming protected files, injecting
replacement functions, weakening checks, or bypassing branch protection. A
separately authorized governance repair must supply a legitimate trust-root
transition before protected corrections can ship. User approval of code alone
does not create the required machine-readable base grant.

## Closure boundary

Internal closure is **not established**. Protected defects remain live until their
fixes land through an authorized protected path; unaudited findings remain open.
The release suite passing is compatible with that state. External seals,
reviewers, participants, cases, utility, novelty, and independence remain outside
this maintenance work.
