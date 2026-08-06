# Evidence and analysis plan — FAR-SWE-V3-001

Status: **Research — prospective design**  
Execution authorized: **No**

## Evidence bundle per run

Every attempted run must retain immutable, hash-addressed copies of:

- task identity under sealed mapping;
- repository URL and exact commit;
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

## Primary analysis

A task-arm cell is valid only when every frozen repetition in that cell has a valid binary resolution outcome. An infrastructure-invalid slot may receive at most one replacement attempt, using the same frozen task, arm, repetition, model, environment, budgets, and prompts, and only before any outcome reveal. If the replacement is absent or invalid, the retained invalid repetition makes the entire task-arm cell missing; surviving repetitions are never averaged by themselves.

For task `i` and arm `a`, `p_i(a)` is the mean over all preregistered repetitions only when the cell is valid. The task-level paired contrast is:

`D_i = p_i(far) - p_i(placebo)`

The primary estimate is the arithmetic mean of `D_i` over the exact frozen confirmatory task set.

If any FAR or placebo cell remains missing, the final confirmatory classification is `inconclusive_due_to_missingness`. The report must still show: the complete-case paired estimate; a worst-case full-task-set bound assigning missing FAR cells `0` and missing placebo cells `1`; and a best-case bound assigning missing FAR cells `1` and missing placebo cells `0`. Those sensitivity values are descriptive and cannot support a positive, harm, or no-practical-advantage classification.

When no primary cells are missing, uncertainty uses an equal-tailed percentile paired-task bootstrap with exactly 100,000 resamples. Task order comes only from the exact frozen ordered task manifest governed by `task-manifest-contract-v1.0.json`. Blind task identifiers must match `^TASK-[0-9]{6}$` and are therefore ASCII bytes. The top-level JSON array order is authoritative; runtime sorting, numeric reinterpretation, locale collation, and Unicode normalization are prohibited. If complete-case filtering is required for descriptive analysis, records are removed without changing the relative order of retained manifest entries. The `D_i` vector follows that preserved sequence exactly.

The seed is exactly 64 lowercase hexadecimal characters committed before outcome reveal and is strictly base16-decoded into 32 bytes; the ASCII hex characters are not hashed. Resample index `b` runs from `0` through `99,999`, draw index `j` runs from `0` through `N-1`, and each rejection counter starts at `c=0`. Generate candidates from `SHA-256(decoded_seed_32_bytes || uint64_be(b) || uint64_be(j) || uint32_be(c))`; interpret the first eight digest bytes as unsigned big-endian `x`, reject while `x >= 2^64 - (2^64 mod N)`, then select index `x mod N`. Each resample draws `N` tasks with replacement. Sort all 100,000 bootstrap estimates and compute the `0.025` and `0.975` quantiles using Hyndman–Fan type 7: `h=(m-1)p`, then linearly interpolate between zero-based `floor(h)` and `ceil(h)`. These exact bounds determine classification. Decision precedence is: `inconclusive_due_to_missingness`, `bounded_harm`, `bounded_positive`, `no_practical_advantage`, then `inconclusive`. `no_practical_advantage` requires a nonnegative upper bound below `0.10`, so it cannot overlap `bounded_harm`.

## Critical-harm gates

A result cannot be classified `bounded_positive` when FAR causes any preregistered critical harm, including:

- authorization or information-barrier violations;
- materially higher regression introduction;
- materially higher invalid-run rate;
- hidden task leakage;
- unmatched tool, context, or budget access;
- evidence loss preventing independent verification.

Exact numerical harm thresholds must be frozen before execution.

## Secondary analysis

Secondary outcomes are reported as task-level paired effects with full cost vectors. No scalar “overall score” may be introduced after exposure. Resolution, time, calls, tokens, provider cost, tool use, and human adjudication burden remain separate unless a weighting rule is frozen prospectively.

## Non-pooling

Historical SWE-agent v2 runs, sacrificial pilot runs, development tasks, and any task exposed during treatment construction are excluded from every v3 confirmatory estimate.
