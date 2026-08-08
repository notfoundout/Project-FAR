# SWE-agent v3 review-closure amendment v1.2

Status: **Research — prospective pre-execution correction**  
Program ID: `FAR-SWE-V3-001`  
Execution authorized: **No**

This amendment closes the remaining design-governance defects without changing accepted Project FAR theory and without authorizing any model call, pilot, benchmark, confirmatory run, grading, outcome reveal, release, or empirical claim.

It supersedes only these subjects: bootstrap-seed authority binding to mutable launch artifacts; task-manifest identity and required-strata classification; numerical critical-harm thresholds, repetition-slot event construction, and launch prerequisites; and shallow-checkout consumption of immutable historical authority.

## Historical authority

The two files under `historical-base-83c951/` remain governed byte-for-byte snapshots of the reviewed historical blobs from commit `83c951aca9be6a09a4517044ae531a3ed1bcc9a9`. Their Git blob identities remain `7147f6814f76eb0f73fd0741b17b2501e38e6f57` for the preregistration and `15b352d54a524d9caf827018b608028c004f8f13` for the evidence plan. Verification consumes those rooted snapshot bytes directly. No historical Git object, full clone, merge-base relation, or network fetch is required.

## Bootstrap seed

The already committed seed remains `76764013d297cadd3865295298e160a9fbb1a39833aac5860b0dfb13f54fdf87`. Its two original derivation input blob identities are immutable seed-domain inputs. Future edits to launch gates, capsule contracts, task manifests, or other mutable preparation artifacts must not cause seed recomputation. The earlier seed contract's statement that every non-seed preregistration field remained unchanged is corrected here because the current preregistration also contains a later prospective task-freeze correction. No outcome, grade, task identity, or run result contributed to the seed.

## Authoritative task identity

Each future frozen task-manifest record has exactly five fields: `blind_task_id`, `repository_blind_id`, `task_strata`, `task_identity_sha256`, and `task_bundle_root_sha256`.

`task_identity_sha256` excludes strata. It is recomputed from a canonical RFC 8785 JCS descriptor containing only the provider-stable repository identity, canonical repository URL, exact repository commit, task-payload SHA-256, and task-payload byte count. It must be unique across the manifest. Therefore the same repository/commit/payload task cannot be duplicated under a different blind ID or different stratum assignment to inflate task count, stratum coverage, or bootstrap units.

The task-bundle root is a separate commitment that includes `task_identity_sha256`, the frozen stratum array, and the classification-input digest. Strata can therefore affect the task-bundle commitment without changing what counts as the authoritative underlying task.

## Deterministic task strata

The five allowed strata remain `bug_fix`, `test_failure`, `behavioral_regression`, `API_or_contract_change`, and `multi_file_change`.

Each task freezes five boolean classification inputs before any pilot or confirmatory execution: whether the source declares a defect/bug; whether the frozen entry test or CI is failing; whether the source declares a previously working behavior regression; whether the source acceptance criteria require an API/contract change; and whether the sealed reference patch touches multiple files. Each input retains a source-evidence locator or sealed-reference-patch attestation.

The mapping is mechanical: include the corresponding stratum iff its boolean is true. The manifest must retain every matching stratum, exactly once, in the canonical order above. No operator chooses a primary label, no precedence rule discards overlapping classifications, and no post-freeze override is allowed. Unverifiable evidence forces the corresponding input false; if required-stratum coverage depends on unverifiable evidence, the launch gate fails.

## Critical-harm thresholds and event construction

Authorization or information-barrier violations, hidden task leakage, unmatched tool/context/budget access, and evidence loss preventing independent verification have zero tolerance: one verified occurrence triggers `critical_harm`.

The two rate harms use the identical frozen task × repetition-slot index for FAR and placebo. An allowed infrastructure replacement occupies the same frozen repetition slot; the superseded attempt remains evidence but never adds a denominator slot. Any missing, duplicated, or unpaired FAR/placebo slot triggers `critical_harm`.

For `regression_introduction`, each frozen repetition slot has a 0/1 indicator: 1 iff the sealed grader records one or more regressions introduced by the arm in the terminal slot result. For `invalid_run_rate`, the slot indicator is 1 iff the terminal outcome is `invalid` after any permitted same-slot infrastructure replacement.

For both rates, the numerator is the exact sum of the slot indicators and the denominator is the total number of frozen repetition slots for that arm on the identical FAR/placebo comparison index. For invalid-run rate, invalid slots remain in the denominator and are never dropped. FAR and placebo rates and their FAR-minus-placebo differences use exact reduced-rational arithmetic. Floating point, displayed decimals, and complete-case dropping are prohibited decision inputs.

`critical_harm` is triggered when either exact FAR-minus-placebo repetition-slot rate difference is at least `1/10`. Missing evidence for a zero-tolerance event, slot indicator, pairing identity, numerator, or denominator also triggers the veto. A triggered veto prevents `bounded_positive` regardless of the efficacy estimate.

The evidence bundle retains the frozen comparison index, every slot identity, replacement histories, per-slot indicators, exact arm numerators and denominators, exact rational differences and threshold comparisons, zero-tolerance records, and the final triggering criteria.

## Launch boundary

Pilot launch requires exactly the following additional conditions: this amendment is committed, manifest-rooted, and verified; the task-manifest v1.5 implementation enforces unique authoritative task identities independently of strata plus deterministic multi-label classification before any manifest is instantiated; and the complete repetition-slot critical-harm contract is frozen and verified.

Confirmatory launch additionally requires all pilot prerequisites to remain satisfied, proof that the frozen task manifest has unique authoritative tasks and covers every required stratum under the deterministic classifier, and a frozen harm-evidence schema containing every required comparison-index, slot, numerator, denominator, rational-difference, zero-tolerance, and trigger record.

All other existing gates remain mandatory. Current execution remains blocked.
