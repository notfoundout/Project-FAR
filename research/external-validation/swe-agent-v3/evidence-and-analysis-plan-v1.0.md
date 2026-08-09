# Evidence and analysis plan — FAR-SWE-V3-001

Status: **Research — prospective design**  
Execution authorized: **No**

## Evidence bundle per run

Every attempted run must retain immutable, hash-addressed copies of:

- task identity under sealed mapping, including the frozen task-manifest strata classification;
- frozen task-manifest Git blob identity and frozen sealed identity-ledger Git blob identity;
- retained task-population repository-prohibition audit report root;
- authoritative repository provider identity, canonical repository URL, exact commit, GitHub fork-source repository ID or null, and treatment-material audit result as reconstructed from the sealed identity ledger by the independent identity auditor;
- environment image digest and dependency lock;
- model provider, endpoint, model version, parameters, and provider request identifier;
- all system, agent, task, capsule, and tool instructions;
- capsule or placebo manifest and mount path;
- randomization position and repetition;
- stdout, stderr, ordered trajectory, commands, tool calls, model messages, timestamps, token usage, budget state, and cost;
- workspace status before and after the run;
- patch, prediction, changed-file inventory, internal exit status, outer exit status, and terminal reason;
- target, neighboring, regression, and hidden-grader results;
- grader version, grader logs, adjudication record, and final outcome;
- the critical-harm evaluation inputs and exact results required by `critical-harm-thresholds-v1.0.json`;
- bundle manifest and content-root digest.

Outer process success cannot override an inner execution failure. `budget_exhausted` is distinct from `resolved`. Missing required evidence makes the run `invalid`, never `resolved`.

## Pre-submission behavior contract

The agent must retain:

1. a reproduction attempt or explicit `reproduction_unavailable`;
2. a causal hypothesis;
3. at least one observation that discriminates that hypothesis from an alternative;
4. execution of the identified target test before submission, or explicit `target_test_unavailable`;
5. execution of the frozen neighboring-test set after a target pass;
6. a patch that modifies an intended repository path, unless the run terminates with an explicit no-patch failure.

These controls affect all arms equally and are part of the frozen agent configuration, not part of the FAR capsule.

## Placebo exposure matching

The FAR treatment count is the sole denominator for both UTF-8-byte and frozen-tokenizer-token exposure matching. FAR counts must be positive integers and placebo counts must be nonnegative integers. A metric passes only when the exact integer inequality `abs(placebo_count - far_treatment_count) * 100 <= far_treatment_count` holds. The boundary is inclusive. No floating-point conversion, percentage rounding, decimal rounding, or alternative denominator is permitted. File count, relative path shape, directory depth, read order, interaction turns, and tool permissions must match exactly.

## Task identity and population audit

`task-manifest-contract-v1.0.json` controls both the blinded ordered task manifest and a separate sealed identity ledger. The manifest contains only blind task ID, repository blind ID, unique task-bundle root, and frozen strata. The sealed ledger contains exactly one same-position record for each manifest entry and binds those blind fields to the authoritative GitHub repository ID, canonical audit URL, exact repository commit, task-payload digest/byte count, matching strata, GitHub fork-source repository ID or null, and a boolean treatment-material audit result.

Before any pilot or confirmatory execution, an independent identity auditor must verify the exact one-to-one ledger/manifest binding, recompute every task-bundle root from the canonical seven-key descriptor, resolve every GitHub repository ID and canonical `full_name` independently from `api.github.com`, enforce one blind repository ID and one canonical URL per authoritative provider/ID pair, and enforce one authoritative provider/ID pair per canonical URL. The auditor must reject repository ID `1283452680` (`notfoundout/Project-FAR`), reject any GitHub fork whose `source.id` is `1283452680`, and reject any candidate exact commit for which the independent audit finds Project FAR treatment material. Every retained `contains_project_far_treatment_material` value must therefore be boolean `false`; unavailable required prohibition evidence rejects the population.

The same preexecution audit must enforce at least 24 tasks, at least five provider-stable repositories, no repository contributing more than 20% of frozen tasks, and frozen manifest-wide coverage of all five preregistered strata. The exact manifest bytes, sealed-ledger bytes, both Git blob identities, independent validation report, and repository-prohibition audit report are committed before execution. The ledger remains sealed from the executing agent and capsule authors. The repository-prohibition audit report root is a required prospective launch binding.

## Primary analysis

A task-arm cell is valid only when every frozen repetition in that cell has a valid binary resolution outcome. An infrastructure-invalid slot may receive at most one replacement attempt, using the same frozen task, arm, repetition, model, environment, budgets, and prompts, and only before any outcome reveal. If the replacement is absent or invalid, the retained invalid repetition makes the entire task-arm cell missing; surviving repetitions are never averaged by themselves.

For task `i` and arm `a`, `p_i(a)` is the mean over all preregistered repetitions only when the cell is valid. The task-level paired contrast is:

`D_i = p_i(far) - p_i(placebo)`

The primary estimate is the arithmetic mean of `D_i` over the exact frozen confirmatory task set.

If any FAR or placebo cell remains missing, the final confirmatory classification is `inconclusive_due_to_missingness`. The report must still show: the complete-case paired estimate; a worst-case full-task-set bound assigning missing FAR cells `0` and missing placebo cells `1`; and a best-case bound assigning missing FAR cells `1` and missing placebo cells `0`. Those sensitivity values are descriptive and cannot support a positive, harm, or no-practical-advantage classification.

When no primary cells are missing, uncertainty uses an equal-tailed percentile paired-task bootstrap with exactly 100,000 resamples. Task order comes only from the exact frozen ordered task manifest governed by `task-manifest-contract-v1.0.json`; its sealed identity ledger independently binds every blind manifest position to one authoritative task/repository descriptor. Blind task identifiers must match `^TASK-[0-9]{6}$` and are therefore ASCII bytes. Task-bundle roots must be unique. Every task record also carries a nonempty canonical-order subset of the five preregistered strata, and the frozen manifest-wide union must cover all five before execution. The top-level JSON array order is authoritative; runtime sorting, numeric reinterpretation, locale collation, and Unicode normalization are prohibited. If complete-case filtering is required for descriptive analysis, records are removed without changing the relative order of retained manifest entries. The `D_i` vector follows that preserved sequence exactly.

The bootstrap seed is the exact 64-lowercase-hex value frozen in `bootstrap-seed-commitment-contract-v1.0.json`. It is independently committed and integrity-rooted before any pilot or confirmatory execution and before any run, grading, or outcome generation. It is immutable after commitment and is not derived from the current capsule, execution gate, task manifest, sealed identity ledger, or any other mutable launch artifact. Selecting, replacing, or trying alternative seeds after commitment is prohibited. The seed is strictly base16-decoded into 32 bytes; the ASCII hex characters are not hashed. Resample index `b` runs from `0` through `99,999`, draw index `j` runs from `0` through `N-1`, and each rejection counter starts at `c=0`. Generate candidates from `SHA-256(decoded_seed_32_bytes || uint64_be(b) || uint64_be(j) || uint32_be(c))`; interpret the first eight digest bytes as unsigned big-endian `x`, reject while `x >= 2^64 - (2^64 mod N)`, then select index `x mod N`. Each resample draws `N` tasks with replacement. Sort all 100,000 bootstrap estimates and compute the `0.025` and `0.975` quantiles using Hyndman–Fan type 7: `h=(m-1)p`, then linearly interpolate between zero-based `floor(h)` and `ceil(h)`. These exact bounds determine classification. Decision precedence is: `inconclusive_due_to_missingness`, `bounded_harm`, `bounded_positive`, `no_practical_advantage`, then `inconclusive`. `no_practical_advantage` requires a nonnegative upper bound below `0.10`, so it cannot overlap `bounded_harm`.

## Critical-harm gates

`critical-harm-thresholds-v1.0.json` is the sole threshold authority for the critical-harm condition used by `bounded_positive`. Its exact bytes and Git blob identity must be committed, integrity-rooted, and independently verified before any pilot or confirmatory execution, and the execution gate `critical_harm_thresholds_frozen_and_verified` must be true in the separately authorized launch commit. It is false in this design-only package.

The contract is zero-tolerance for authorization/information-barrier violations, hidden-task leakage, unmatched execution access, and evidence loss preventing independent reconstruction. For auditability, each zero-tolerance harm records the number of affected frozen repetition slots, the exact total frozen-slot denominator, the reduced rational incidence rate, the zero-occurrence threshold, and the triggered boolean. The trigger itself is strictly `slot_numerator > 0`; the denominator cannot excuse a violation.

`regression_introduction_rate` counts a frozen slot only when every frozen regression test used by the harm rule passes in the pristine frozen repository/environment control immediately before that slot and at least one of those same tests fails against the submitted workspace. There is no causal-attribution override, operator waiver, or post-hoc exclusion. `invalid_run_rate` counts frozen slots whose retained terminal outcome remains invalid after the single permitted same-slot infrastructure replacement process is exhausted or inapplicable. For both rate harms, the arm denominator is the exact preregistered frozen repetition-slot count before execution; resolved, unresolved, invalid, and replacement-eligible slots remain in the denominator and same-slot replacement never adds a denominator slot. All arithmetic is exact reduced rational arithmetic. Either rate harm triggers when the exact FAR-minus-placebo rate contrast is greater than or equal to `1/10`.

For every zero-tolerance harm, retained evidence must include harm ID, slot numerator, slot denominator, reduced rational incidence rate, exact threshold, trigger rule, and triggered boolean. For each rate harm, retained evidence must include FAR numerator and denominator, FAR reduced rational rate, placebo numerator and denominator, placebo reduced rational rate, reduced rational contrast, exact threshold, and triggered boolean. All harm records also retain the frozen design commit, frozen task-manifest Git blob identity, frozen sealed identity-ledger Git blob identity, grader version, and evidence-bundle content root. No `bounded_positive` classification is permitted if any exact harm rule triggers.

Changing a threshold, numerator predicate, denominator rule, comparison rule, evidence requirement, or harm set after any pilot or confirmatory exposure creates a new experiment version and cannot retroactively govern existing runs.

## Pre-execution launch binding

`execution-gate-v1.0.json` requires a separate prospective pilot or confirmatory launch record committed before execution. That record must bind every execution-critical identity listed in `launch_record_required_bindings`, including the frozen design commit and manifest, task manifest, sealed identity ledger, repository-prohibition audit report root, bootstrap-seed commitment, critical-harm contract, treatment and placebo roots, model identity, prompts/configuration, environment/dependencies, budgets/stopping rules, assignment seed, grader contract, evidence-store configuration, protection reference, and manual authorization record. A true gate without the complete launch record cannot authorize execution.

## Secondary analysis

Secondary outcomes are reported as task-level paired effects with full cost vectors. No scalar “overall score” may be introduced after exposure. Resolution, time, calls, tokens, provider cost, tool use, and human adjudication burden remain separate unless a weighting rule is frozen prospectively.

## Non-pooling

Historical SWE-agent v2 runs, sacrificial pilot runs, development tasks, and any task exposed during treatment construction are excluded from every v3 confirmatory estimate.
