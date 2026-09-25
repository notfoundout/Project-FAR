# Test-Suite and CI Assurance Audit

Status: **Repository infrastructure audit and remediation record; no theory, claim, or status change**

Date: 2026-09-25

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

`Implemented` means committed on this branch. `Pending` means prepared as a patch under [`test-suite-audit-2026-09-25/pending/`](test-suite-audit-2026-09-25/pending/), because it touches a protected check, a file locked by `validation_bootstrap/assurance-lock.json`, or a file owned by the open security/bootstrap task (PR #538). `Deferred` means it belongs to that security task.

| # | Finding | Disposition |
|---|---|---|
| 1 | Promoting `CLM-EXISTENCE`, `CLM-ECONOMY`, and `CLM-INDEPENDENCE` to `supported` passed all 1,955 tests and all 135 checks in `repo_health_check.py --full`. The registry's `stronger_status_requires_linked_artifacts` policy has no enforceable field. | Implemented: `tools/check_claim_status_ceiling.py`, wired into repository health. Pending: patch 01 makes the protected `governance.research-gates` check enforce it. |
| 2 | The validator-assurance evidence is largely self-referential. The mutation campaign counts four fixed texts per checker. The oracle is a static AST-size heuristic and accepted 11 failing checkers. The formal model checks its own `simulate()`, which the engine never calls. | Implemented: exhaustive behavioral test of the real engine scheduler. Pending: patch 03 counts real rule-deletion mutants, reports the static texts separately, and binds the model to the engine; patch 03a holds the owner repin authorization it requires. Deferred: literal `lean-proof` evidence and in-job signing (RT-9/RT-10). |
| 3 | Checker rules were untested; deleting the reversed-dependency rule passed the suite and the weakening detector. | Implemented: per-rule tests; 102/102 rule deletions now detected across the five registered governance checkers; `tools/checker_rule_mutation.py` and workflow `checker-rule-mutation.yml` enforce per-checker floors. |
| 4 | PCA W4/W6 pin living governance documents by whole-file hash, so any edit fails and a routine repin hides a buried promotion. | Implemented: `tools/check_governance_register_integrity.py`, a semantic guard that passes benign edits. The pins themselves live in PR #538-owned files and are unchanged. |
| 5 | Two protected checks are historical-campaign checkers that require the Makefile to repeat commands exactly three times. | Pending: patch 04 replaces the three copies with one `define research-gates` block and replaces nine `count(...)==3` rules with a helper that checks every gate target runs the shared block. |
| 6 | Eleven UPP checkers asserted the live queue tip, broke after the terminal migration, and ran nowhere. | Implemented: `tools/upp_queue_history.py`; all 15 UPP checkers pass and are run by tests; a reachability test requires every checker to be invoked and forbids checker/test mutual invocation. |
| 7 | 46 checkers validate with bare `assert`; under `python -O` a promoted frozen result passed. | Implemented: 45 checkers refuse to run under `-O`, enforced by test. Pending: patch 01 guards the protected `check_s_core_w4.py`. |
| 8 | Redundant execution: repository health re-runs the canonical suite inside every manifest profile. | Implemented: `repo_health_check.py --skip-canonical-tests` (default off). Pending: patch 02 uses it in the manifest, so each profile runs the suite once; the patched health-fast profile measured 94 s. |
| 9 | `repo_health_check.py` silently skipped listed tools that did not exist, and two of its tests never exercised the logic they are named for. | Implemented. |
| 10 | The commercial package loads `mechanization/far_mechanization/*.py` and the contract schemas at runtime, but its workflow triggered only on `commercial/**`. | Implemented: path filter extended. |
| 11 | The Lean placeholder pattern missed inline `by sorry` and attributed or modified `axiom` declarations. | Implemented: pattern strengthened; comments and strings are excluded; 0 placeholders on `main`. |
| 12 | `far_validation/model.py` treats `unresolved` as a successful terminal status, contrary to `unknown_is_not_pass`; the engine never emits it today. | Not changed. It is a policy decision in a locked file and needs owner review. |
| 13 | `repository-health.yml` duplicates work that the required `merge-authority` job already performs. | Not changed. Removing it breaks links in three generated reports and saves CI time without improving detection. |
| 14 | `validator-assurance.yml` and `exact-head-assurance.yml` are near copies, and a test locks them equal; Lean is installed separately in five workflows. | Deferred to the security task, which is replacing these workflow steps. |

A hypothesis that the validation cache could serve stale passes was falsified: `validation/runtime-dependencies.json` widens `tests.canonical` inputs to `**/*`, and a real theory change invalidated the cache.

## After remediation

| Measure | `main` | This branch | Branch plus pending patches |
|---|---|---|---|
| Canonical tests | 1,955 | 2,055 | 2,070 |
| Rule deletions detected, registered governance checkers | 0/89 on the three that existed | 102/102 | 102/102 |
| Adversarial edits caught by a semantic check | 7 of 13 (5 more only by byte pins, 1 by nothing) | 13 of 13 | 13 of 13 |
| Failing or unreached checkers | 11 failing, 14 unreached | 0 | 0 |
| Mutation-campaign entries that carry information | 15 of 615 | unchanged | 117 of 117, plus 608 static checks reported separately |
| `pr-full` profile | not run in this audit | 30/30 pass, 120 s | 30/30 pass, 110 s |

## Pending integration

Apply in this order after the security/bootstrap task reconciles protected files:

1. [`03a-owner-repin-authorization.patch`](test-suite-audit-2026-09-25/pending/03a-owner-repin-authorization.patch) must land on `main` first through an owner action. It adds `REPIN-TSA-0001` and `REPIN-TSA-0002` to `validation/test-weakening-waivers.json`. That file is itself content-pinned, which is the RT-11 constraint recorded by PR #538.
2. [`01-protected-claim-ceiling-and-O-guard.patch`](test-suite-audit-2026-09-25/pending/01-protected-claim-ceiling-and-O-guard.patch)
3. [`02-manifest-single-suite-run.patch`](test-suite-audit-2026-09-25/pending/02-manifest-single-suite-run.patch)
4. [`03-validator-campaign-evidence.patch`](test-suite-audit-2026-09-25/pending/03-validator-campaign-evidence.patch)
5. [`04-makefile-single-gate-block.patch`](test-suite-audit-2026-09-25/pending/04-makefile-single-gate-block.patch), or [`04-makefile-single-gate-block.after-pr538.patch`](test-suite-audit-2026-09-25/pending/04-makefile-single-gate-block.after-pr538.patch) if PR #538 has merged. Both variants add a PCA W6 current-state supplement entry declaring the Makefile change.

Verification of the pending stack, performed in disposable worktrees:

- With the owner authorization on the comparison base, patches 01–03 pass `validation_bootstrap/verify.py` and `far_validation weakening`. Without it, the weakening gate rejects the two repins, as intended.
- The stack passes `far_validation validate --profile pr-full` (30/30) and the canonical suite (2,070 tests).
- On a merge of this branch with PR #538's head (`f1ae56c`), the stack applies in order with the post-#538 variant of patch 04 and the canonical suite passes (2,113 tests).

## Unresolved

- `make docs-check`, `make links-check`, `make research-check`, `make health-fast`, and a standalone weakening run on this branch were not executed as a batch in the authoring session because the execution environment denied that batch. The same checks ran through `far_validation validate --profile pr-full`, which includes repository health, hygiene, markdown, links, and the research checks.
- The PCA W4/W6 whole-file pins on living documents remain as designed; replacing them is a decision for their owners.
- The governance promotion rule is a clause-level heuristic and can miss unusual phrasing.

## Claim and status impact

None. No claim, theorem, gate, or status changed. The new checkers pin current statuses as ceilings and forbid promotion without a reviewed change; they do not raise or lower any status.
