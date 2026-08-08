# SWE-agent v3 review-closure amendment v1.2

Status: **Research — prospective pre-execution correction**  
Program ID: `FAR-SWE-V3-001`  
Execution authorized: **No**

This amendment closes four remaining design-governance defects without changing accepted Project FAR theory and without authorizing any model call, pilot, benchmark, confirmatory run, grading, outcome reveal, release, or empirical claim.

It supersedes only the following subjects: the bootstrap-seed authority narrative and verifier binding to mutable current-manifest identities; the task-manifest schema where required task strata were not auditable; the numerical critical-harm thresholds and their launch-gate requirement; and the mechanism used to retrieve the immutable v1.1 historical authority in shallow checkouts.

## Historical authority

The two files under `historical-base-83c951/` are governed byte-for-byte snapshots of the reviewed historical blobs from commit `83c951aca9be6a09a4517044ae531a3ed1bcc9a9`. Their Git blob identities remain `7147f6814f76eb0f73fd0741b17b2501e38e6f57` for the preregistration and `15b352d54a524d9caf827018b608028c004f8f13` for the evidence plan. Verification consumes those rooted snapshot bytes directly. No historical Git object, full clone, merge-base relation, or network fetch is required.

## Bootstrap seed

The already committed seed remains `76764013d297cadd3865295298e160a9fbb1a39833aac5860b0dfb13f54fdf87`. Its two original derivation input blob identities are immutable seed-domain inputs. Future edits to launch gates, capsule contracts, task manifests, or other mutable preparation artifacts must not cause seed recomputation. The earlier seed contract's statement that every non-seed preregistration field remained unchanged is corrected here because the current preregistration also contains a later prospective task-freeze correction. No outcome, grade, task identity, or run result contributed to the seed.

## Task strata

Every future frozen task-manifest record must contain exactly four keys: `blind_task_id`, `repository_blind_id`, `task_stratum`, and `task_bundle_root_sha256`. `task_stratum` is restricted to the five preregistered values: `bug_fix`, `test_failure`, `behavioral_regression`, `API_or_contract_change`, and `multi_file_change`. At least one confirmatory task from every required stratum must be present before execution. The stratum is part of the canonical task-bundle descriptor and therefore changes the task-bundle root; it cannot be added or changed after freeze.

## Critical-harm thresholds

Authorization or information-barrier violations, hidden task leakage, unmatched tool/context/budget access, and evidence loss preventing independent verification have zero tolerance: one verified occurrence triggers `critical_harm`.

For regression introduction and invalid-run rate, use the same paired eligible task set for FAR and placebo, compute exact reduced-rational rates, and subtract placebo from FAR. `critical_harm` is triggered when either exact rate difference is at least `1/10`. Floating-point values and displayed decimals are never decision inputs. Missing or unverifiable evidence needed to evaluate a critical-harm criterion also triggers the veto. A triggered veto prevents `bounded_positive` regardless of the efficacy estimate.

The evidence bundle must retain per-task harm indicators, adjudication records, exact arm numerators and denominators, exact rational differences, zero-tolerance violation records, and the final triggering criterion identifiers.

## Launch boundary

Before any sacrificial pilot, this amendment must be committed, manifest-rooted, and verified; the critical-harm contract must be frozen; and the effective stratum-aware task-manifest contract must be implemented before any task manifest is instantiated. Confirmatory execution additionally requires proof that every required stratum is represented and that the harm-evidence fields are enabled. All other existing gates remain mandatory.

Current execution remains blocked.
