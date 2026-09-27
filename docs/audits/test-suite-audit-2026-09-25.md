# Test-Suite and CI Assurance Audit

Status: **Repository infrastructure audit and remediation record; no theory, claim, or status change**

Date: 2026-09-25; re-evaluated and extended 2026-09-27 (see [Re-evaluation](#re-evaluation-2026-09-27))

Scope: `tests/`, `tools/check_*.py`, `validation/manifest.json`, `far_validation/`, the Makefile health targets, and `.github/workflows/`.

Independence: I0 author-side review by an AI agent. The audit is not independent review, and its measurements are internal.

## Question

Which tests and checks actually detect the failures they are meant to catch, which only prove that a checker ran or that bytes are unchanged, and what would make the suite detect more bugs per unit of cost?

## Baseline measurements on `main` at `7fb4816`

| Measure | Value | Method |
|---|---|---|
| Canonical tests | 1,955 in 234 files, 0 failures, 0 skips, about 76 s | Timed run of `tools/run_tests.py` |
| Workflows | 39 (11 on every PR to `main`, 17 path-filtered, 11 manual, scheduled, or push-only) | YAML parse |
| Checker scripts | 143 `tools/check_*.py`; 32 manifest checks, 5 protected | Inventory |
| Canonical-suite executions per PR | About 12 | Derived from workflow and manifest configuration, not measured in CI |
| Tests on frozen historical campaigns | About 1,225 of 1,955 (63%) | File-name family classification, approximate |
| Rule-deletion mutants detected | 93 of 283 (33%) across 15 checker/test pairs; 0/58 theory closure, 0/19 FAR-CORE v1.1 formalization, 0/12 semantic consistency | Each `errors.append` line replaced by `pass` in a disposable copy |
| `far_validation mutations` | 615 "mutations", score 1.0; 600 are four fixed texts applied to 150 files | Campaign output |
| Orphaned checkers | 14 invoked by nothing; 11 of them failing on `main` | Every checker executed |
| Adversarial canonical-data edits | 13 edits; 1 caught by nothing, 5 caught only by whole-file hash pins | Full suite plus checkers per edit |

## Findings and disposition

`Implemented` means committed on this branch. `Deferred` means it belongs to the security task (PR #538) or waits for it. On 2026-09-25 several items were prepared as patches under `test-suite-audit-2026-09-25/pending/`; the [re-evaluation](#re-evaluation-2026-09-27) applied, rejected, or deferred each of them and removed the directory.

| # | Finding | Disposition |
|---|---|---|
| 1 | Promoting `CLM-EXISTENCE`, `CLM-ECONOMY`, and `CLM-INDEPENDENCE` to `supported` passed all 1,955 tests and all 135 checks in `repo_health_check.py --full`. The registry's `stronger_status_requires_linked_artifacts` policy has no enforceable field. | Implemented: `tools/check_claim_status_ceiling.py`, wired into repository health, and (former patch 01) enforced by the protected `governance.research-gates` check. |
| 2 | The validator-assurance evidence is largely self-referential. The mutation campaign counts four fixed texts per checker. The oracle is a static AST-size heuristic and accepted 11 failing checkers. The formal model checks its own `simulate()`, which the engine never calls. | Implemented: exhaustive behavioral test of the real engine scheduler; (former patch 03) the campaign counts real rule-deletion mutants and reports the static texts separately, and the formal model is run against the real engine. The two changed files are protected and need owner signatures. Deferred: literal `lean-proof` evidence and in-job signing (RT-9/RT-10, implemented in PR #538). |
| 3 | Checker rules were untested; deleting the reversed-dependency rule passed the suite and the weakening detector. | Implemented: per-rule tests; 102/102 rule deletions now detected across the five registered governance checkers; `tools/checker_rule_mutation.py` and workflow `checker-rule-mutation.yml` enforce per-checker floors. |
| 4 | PCA W4/W6 pin living governance documents by whole-file hash, so any edit fails and a routine repin hides a buried promotion. | Implemented: `tools/check_governance_register_integrity.py`, a semantic guard that passes benign edits. The pins themselves live in PR #538-owned files and are unchanged. |
| 5 | Two protected checks are historical-campaign checkers that require the Makefile to repeat commands exactly three times. | Deferred (former patch 04, a single `define research-gates` block): a maintainability refactor with no detection gain that conflicts with PR #548's Makefile changes and PR #538/#548's PCA W6 supplement, and rewrites rules in the protected claim-boundaries and w5-authorization checkers. Its text is preserved in this pull request's history at `7806bb18`. |
| 6 | Eleven UPP checkers asserted the live queue tip, broke after the terminal migration, and ran nowhere. | Implemented: `tools/upp_queue_history.py`; all 15 UPP checkers pass and are run by tests; a reachability test requires every checker to be invoked and forbids checker/test mutual invocation. |
| 7 | 46 checkers validate with bare `assert`; under `python -O` a promoted frozen result passed. | Implemented: all 46 refuse to run under `-O` (the protected `check_s_core_w4.py` by former patch 01), enforced by test. |
| 8 | Redundant execution: repository health re-runs the canonical suite inside every manifest profile. | Implemented: `repo_health_check.py --skip-canonical-tests` (default off). Rejected: former patch 02, which used it in the manifest. `tests.canonical` does not set `expect_no_changes`; the `git status` guard inside repository health is the only check that the suite leaves tracked files unmodified. Skipping the suite there drops that guard, and running the guard concurrently with the suite reintroduces the write race that PR #548 fixed for the generators. |
| 9 | `repo_health_check.py` silently skipped listed tools that did not exist, and two of its tests never exercised the logic they are named for. | Implemented. |
| 10 | The commercial package loads `mechanization/far_mechanization/*.py` and the contract schemas at runtime, but its workflow triggered only on `commercial/**`. | Implemented: path filter extended. |
| 11 | The Lean placeholder pattern missed inline `by sorry` and attributed or modified `axiom` declarations. | Implemented: pattern strengthened; comments and strings are excluded; 0 placeholders on `main`. |
| 12 | `far_validation/model.py` treats `unresolved` as a successful terminal status, contrary to `unknown_is_not_pass`; the engine never emits it today. | Not changed. It is a policy decision in a locked file and needs owner review. |
| 13 | `repository-health.yml` duplicates work that the required `merge-authority` job already performs. | Not changed. Removing it breaks links in three generated reports and saves CI time without improving detection. |
| 14 | `validator-assurance.yml` and `exact-head-assurance.yml` are near copies, and a test locks them equal; Lean is installed separately in five workflows. | Deferred to the security task, which is replacing these workflow steps. |

A hypothesis that the validation cache could serve stale passes was falsified: `validation/runtime-dependencies.json` widens `tests.canonical` inputs to `**/*`, and a real theory change invalidated the cache.

## After remediation

"2026-09-27" is this branch with former patches 01 and 03 and the re-evaluation fixes, measured at `6cf2c7d9`. A dash means not re-measured.

| Measure | `main` | Branch, 2026-09-25 | Branch, 2026-09-27 |
|---|---|---|---|
| Canonical tests | 1,955 | 2,055 | 2,086, one explicit skip (finding 21), 73 s |
| Rule deletions detected, registered governance checkers | 0/89 on the three that existed | 102/102 | 102/102 (mutation campaign) |
| Adversarial edits caught by a semantic check | 7 of 13 (5 more only by byte pins, 1 by nothing) | 13 of 13 | — |
| Failing or unreached checkers | 11 failing, 14 unreached | 0 | — |
| Mutation-campaign entries that carry information | 15 of 615 | unchanged | 117 of 117, plus 608 static checks reported separately; 27 s |
| Adversarial probes caught | 20 of 25 applicable | — | 30 of 31; the remaining one (T4) is caught with PR #560 |
| `pr-full` profile | not run in this audit | 30/30 pass, 120 s | 30/30 pass under strict tracing (`--trace-dependencies --require-trace --require-signed-cache`), 628 s on a loaded local machine |

## Re-evaluation (2026-09-27)

The branch was merged with `main` at `95834dab` (#565) and re-audited against the owner-signed repin model, which replaced the base-waiver model after 2026-09-25.

### Former pending patches

| Patch | Decision |
|---|---|
| 01 claim ceiling in `governance.research-gates`; `-O` guard for `check_s_core_w4.py` | Applied. The protected check's manifest definition is unchanged. |
| 02 manifest runs the canonical suite once | Rejected; see finding 8. |
| 03 rule-deletion mutants; formal model against the real engine | Applied. Protected transitions: `far_validation/mutations.py`, `far_validation/formal_model.py`. `tools/checker_rule_mutation.py` is added to the assurance lock. |
| 03a owner waiver entries | Obsolete: waivers in `validation/test-weakening-waivers.json` no longer authorize protected repins. An owner signature over each exact transition does. |
| 04 single research-gates block | Deferred; see finding 5. |

### New findings

An adversarial probe, `tools/assurance_adversarial_probe.py`, applies each defect that the validation system claims to reject to a disposable clone. It then runs the one detector that should reject the defect, and counts a probe as `CAUGHT` only when the rejection reason matches the one fixed in the probe.

| # | Finding | Disposition |
|---|---|---|
| 15 | V1: `raise SystemExit(0)` before a checker's body (also an early `return`, or `self.skipTest` before a test's assertions) passed the weakening detector, because every strength metric is syntactic and unchanged. | Implemented: the detector counts statements made unreachable by an unconditional terminator in their block and rejects any increase. No file had such dead code, so no existing file is affected. A conditional early exit remains uncaught. |
| 16 | U5: moving a test module out of `test_*.py` discovery with `git mv` passed. Rename detection reported only the new path, which has no base version. | Implemented: `_changed_python` uses `--no-renames`, as `_changed_paths` does. The trade-off is that a legitimate rename of a test module is also reported as a deletion. |
| 17 | V3: pointing the protected `governance.claim-boundaries` check at another checker passed `validation_bootstrap/verify.py`, which compared only the flag, severity, and profiles. V4: the protected set lived in `bootstrap-lock.json`, which no assurance pin covered, so a check could be unprotected in the manifest and that lock together. | Implemented: `bootstrap-lock.json` pins a digest of each protected check's whole definition, `verify.py` rejects any difference, and `bootstrap-lock.json` is added to the assurance lock. Protected transition: `validation_bootstrap/verify.py`. |
| 18 | T4: the strict tracer did not see an undeclared write made through an atomic rename. | Fixed by PR #560's tracer (rename destinations are writes). It is caught on the combined tree below. |
| 19 | Tests inherited the host's global git configuration. In the authoring environment, whose configuration signs commits, tests that commit to temporary repositories failed. | Implemented: `tools/run_tests.py` points git at an empty global configuration and ignores the system one. The test includes a control. |
| 20 | `test_theory_dependency_audit` passed vacuously on a shallow clone. | Implemented: it skips with a stated reason. |
| 21 | The cross-interpreter hardening test probed the host's `/usr/bin/python3.x`. It executed interpreters that no check declares, and it skipped on the runner image. | Implemented: interpreters come from `FAR_CROSS_INTERPRETERS`. `python311-compatibility` still verifies the pins under a second version. |
| 22 | Thirteen read-only workflows ran with the default token permissions. `repository-health.yml` used the newest Python 3.x and an unpinned pyyaml. | Implemented: `permissions: contents: read`; Python 3.12 and `requirements.txt`. |
| 23 | `classify-merged-pr-review-findings.yml` and `far-swe-agent-v2-postprocess.yml` push only on `push` or `workflow_dispatch`, but they also hold workflow-wide `contents: write` on `pull_request`. | Implemented. The earlier "not changed" rested on the author already having push access, but the token is held by the code the pull request runs, not by its author. That code includes the pull request's tests, tools and dependencies. It could push as `github-actions[bot]` to any branch that branch protection does not cover. Both workflows now default to `contents: read`. The push to the audit branch moved to a `commit-generated` job, which runs only on `push` and runs no repository code. `far-swe-agent-v2-postprocess.yml` grants `contents: write` only to `evaluate-reveal`, which runs only on `workflow_dispatch`. `tests/test_workflow_token_permissions.py` fails on any job that can run for a pull request or merge-queue entry and holds a write token. A job passes only when every branch of its `if` requires a non-pull-request event. The test also requires every unlocked workflow to declare its permissions. Against the previous workflows it names `classify`, `contracts` and `verify-source`; against `main` it also names the 13 workflows from finding 22. The three locked workflows that declare none (`lean.yml`, `repo-health.yml`, `specification-export.yml`) get the repository default, which the job logs show as Contents, Metadata and Packages `read`. Changing that default is an owner setting, like branch protection. |
| 24 | `repository.health-full` runs `check_fara_canonical_kernel_replication.py`, which needs an implementation commit reachable only from a non-`main` branch and falls back to a network fetch. | Not changed. It passes on full clones. Deleting that branch would break the check. |
| 25 | `repo-health.yml` and `repository-health.yml` share the display name `Repository Health`, and `full-shadow` repeats work that `merge-authority` performs. | Not changed; recorded for CI maintenance. |
| 26 | The finding-11 placeholder scan, and PR #548's independent comment-aware rewrite of it, could each be blinded by a literal. Here a character literal `'"'` or a raw string ending in `\` opened a string that hid a later `sorry`; in PR #548, a string holding `/-` opened a comment that never closed. Neither scan matched `sorryAx`, which compiles with only a warning under Lean 4.19.0. | Implemented: one lexer (nested comments, strings, raw strings, character literals, interpolation kept as code, unterminated input left as code). It uses the union of both patterns plus `sorryAx`, and is byte-identical in this PR and PR #548. `tests/test_lean_placeholder_scan.py` has 11 cases failing under each previous scanner. |

### Adversarial probe results

Raw outputs: [`test-suite-audit-2026-09-25/probe-2026-09-27/`](test-suite-audit-2026-09-25/probe-2026-09-27/). The same probe code ran against four trees, with PR #560 head `1ebbbfbf` as the signed ref.

| Tree | Caught | Missed | Not run |
|---|---|---|---|
| `main` `95834dab` | 20 | V1, V3, V4, G1, T4 | U1–U6 (their target file does not exist on `main`) |
| This branch before the detector fixes, `7c8833e4` | 26 | U5, V1, V3, V4, T4 | none |
| This branch, `6cf2c7d9` (detectors identical to the final head) | 30 | T4 | none |
| This branch merged with PR #560, `d3f83662` | 26 | none | S1–S5: that tree already contains #560's signed ledger entries, so there is nothing appended to tamper with or replay. They are caught on the other trees. |

The expected reason for V1 was narrowed to `unreachable statement count increased` when the rule was added. The earlier alternatives (branch, failure-path, or structure decrease) cannot occur for an inserted early exit.

### Protected transitions and ordering

The protected transitions are `far_validation/mutations.py`, `far_validation/formal_model.py`, `far_validation/weakening.py`, and `validation_bootstrap/verify.py`. Each needs an owner-signed authorization bound to this pull request.

`weakening.py` is also changed by PR #560. The two versions merge without conflict, but the merged bytes differ from both. For that reason, signatures are requested only after PR #560 and PR #538 have merged and `main` has been merged into this branch.

## Unresolved

- The four protected transitions need owner signatures, in the order given above. Until they are signed, `merge-authority` and `protected-repin-gate` fail on this pull request, as intended.
- A conditional early exit in a test or checker is not detected (finding 15).
- A legitimate rename of a test module needs a base waiver (finding 16).
- Former patch 04 is deferred (finding 5). Findings 23–25 are recorded, not changed.
- The PCA W4/W6 whole-file pins on living documents remain as designed; replacing them is a decision for their owners.
- The governance promotion rule is a clause-level heuristic and can miss unusual phrasing.

## Claim and status impact

None. No claim, theorem, gate, or status changed. The new checkers pin current statuses as ceilings and forbid promotion without a reviewed change; they do not raise or lower any status.
