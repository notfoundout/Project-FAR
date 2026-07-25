# Pinned SWE-agent CLI contract hotfix

The second live execution dispatch failed before any model call because the controller treated human-readable `run-batch --help` output as the authoritative CLI schema. At the frozen SWE-agent commits, valid `RunBatchConfig` fields such as `output_dir` and `num_workers` are not rendered as literal `--` options in that summary.

The corrected authority is the pinned parser itself:

1. construct one canonical command containing both frozen configuration files and all execution controls;
2. run that exact command with `--print_config`, which parses and materializes configuration without starting an agent or model call;
3. fail closed unless the parsed configuration preserves the frozen file instance source, exact instance and output paths, one worker, disabled progress/random delay, exception propagation, and no redo;
4. execute the exact previously validated command without rebuilding it.

No frozen task, release, model, model parameters, agent configuration, environment digest, repetition count, run order, evidence-freeze rule, or outcome boundary changes in this hotfix.
