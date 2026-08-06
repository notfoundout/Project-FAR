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

## Primary analysis

For task `i` and arm `a`, resolution probability is the mean of valid binary resolution outcomes over the frozen repetitions. The task-level paired contrast is:

`D_i = p_i(far) - p_i(placebo)`

The primary estimate is the arithmetic mean of `D_i` over the exact frozen confirmatory task set.

Uncertainty uses a paired task bootstrap with 100,000 resamples. The bootstrap seed must be committed before outcome reveal. Invalid runs are not silently dropped; the preregistered invalid-run rule must either rerun the same frozen slot for an infrastructure failure or retain the task-arm cell as missing and trigger the declared missingness sensitivity analysis.

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
