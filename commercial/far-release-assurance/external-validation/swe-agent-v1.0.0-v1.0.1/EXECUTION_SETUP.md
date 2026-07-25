# Frozen SWE-agent execution setup

## Implemented workflow

The manual workflow at `.github/workflows/far-swe-agent-execution.yml` exposes four explicit stages:

1. `prepare-environment` builds the pinned SWE-bench task environment, publishes it to GHCR, and writes the immutable registry lock.
2. `preflight` validates the frozen manifest, environment lock, task record, agent configuration, and local image without making a model call.
3. `plan` requires `RUN-FAR-FREE-TIER-COMPARISON` and writes the deterministic four-run execution plan without revealing benchmark outcomes.
4. `execute` requires `EXECUTE-FAR-FROZEN-NEXT-RUN`, restores the latest execution artifact, validates the restored state, and executes at most one frozen run.

Every stage runs the case validator and regression suite before stage-specific work. The workflow uses a concurrency lock, masks the Gemini key, removes checkout credentials, strips `GITHUB_TOKEN` and `GH_TOKEN` from the model process, and uploads only the case execution-output directory.

The repository is private. GitHub-hosted runner and package usage are governed by the account's current GitHub plan and quotas; this document makes no claim that Actions or GHCR usage is free.

## Credential prerequisite

Store the Gemini Developer API key as `GEMINI_API_KEY` in the `far-swe-agent-execution` environment or as a repository Actions secret. Do not commit it, paste it into issues, include it in artifacts, or transmit it through chat.

The key is injected only into the credential-gated workflow job. The workflow masks it, and the execution controller redacts the exact secret from captured stdout and stderr before writing logs.

## Required execution order

The environment image and execution inputs are already frozen for this case. Do not rerun `prepare-environment` unless an independently accepted change explicitly replaces the frozen environment and updates every bound hash.

1. Run `preflight` and require success.
2. Run `plan` with `RUN-FAR-FREE-TIER-COMPARISON`.
3. Run `execute` with `EXECUTE-FAR-FROZEN-NEXT-RUN`.
4. Repeat the same `execute` stage until all four frozen slots are complete.
5. If the controller records `failed_retryable`, preserve the uploaded artifact and rerun the same stage only after provider access is available. Do not substitute another model, task, release, environment, or configuration.
6. If the controller records `failed_terminal`, stop the matrix. Later slots must not execute until the terminal defect is resolved through an auditable repository change.
7. After all four runs are internally validated, compile the evidence packages, freeze the primary comparison, independently verify the freeze, and only then reveal benchmark outcomes through the separate post-execution workflow.

## Restored-state validation and retries

A restored run is not trusted merely because its prior state says `complete`. Before selecting the next slot, the validated controller checks the preserved outer return code, `run_batch_exit_statuses.yaml`, target-instance prediction, and patch content.

If preserved evidence disproves completion, the controller writes `run-record-correction.json`, appends the correction to execution state, removes completion-only metadata, and reclassifies the same slot. The original run record and raw evidence remain preserved.

Before a retry, the controller moves the previous attempt's instance, invocation, logs, run record, correction record, SWE-agent output, and copied trajectory into an attempt archive. The new attempt therefore cannot inherit stale status or prediction files while prior evidence remains auditable.

Transient 429, quota, timeout, or 5xx messages do not override a final internally successful run with return code zero and a non-empty target patch. They control classification only when the final status, return code, or prediction evidence is unsuccessful.

## Model and cost boundary

The frozen model is `gemini-2.5-pro`, accessed through LiteLLM as `gemini/gemini-2.5-pro`, with zero monetary model-cost limits and a 30-call ceiling per run. Provider quotas, availability, pricing, and data-use terms can change. The workflow must stop rather than fall back to a paid tier or another model.

This case uses a public SWE-bench task. It must not be reused for confidential customer artifacts without a separately accepted security and privacy design.
