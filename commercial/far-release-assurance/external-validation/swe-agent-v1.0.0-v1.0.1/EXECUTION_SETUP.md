# Credentialed execution setup

## What is already provisioned

The repository contains a manual GitHub Actions environment in `.github/workflows/far-swe-agent-execution.yml`.

It provides three explicit stages:

1. `resolve-image` — pulls the selected SWE-bench image and reports its immutable digest without using an API key or making a model call.
2. `preflight` — validates the committed digest, manifest, configuration hash, run matrix, and local tool availability.
3. `plan` — requires the Anthropic secret and the exact confirmation phrase `RUN-FAR-EXTERNAL-COMPARISON`, then writes the deterministic four-run plan. It does not reveal benchmark outcomes.

The workflow uses `ubuntu-24.04`, serializes runs through a concurrency lock, removes unused runner packages for disk capacity, masks the API key, uses read-only repository permissions, and uploads only non-secret execution artifacts.

## One account-bound prerequisite

Create an Anthropic API key from the Anthropic Console under the account that will pay for the experiment. The key must not be committed, pasted into issues, included in artifacts, or sent through chat.

Add it to GitHub as either:

- an environment secret named `ANTHROPIC_API_KEY` in the `far-swe-agent-execution` environment; or
- a repository Actions secret named `ANTHROPIC_API_KEY`.

Environment-scoped storage is preferred because it can require reviewer approval before the credential becomes available to a job.

## Required execution order

1. Merge the PR containing this workflow.
2. Open **Actions → FAR SWE-agent External Comparison → Run workflow**.
3. Run `resolve-image`.
4. Download the artifact and copy the reported `sha256:...` digest into `manifest.json`.
5. Change manifest status to `execution_inputs_frozen` in a new reviewed commit.
6. Run `preflight` and require success.
7. Ensure Anthropic billing can cover the frozen maximum of $100.
8. Run `plan` with confirmation `RUN-FAR-EXTERNAL-COMPARISON`.
9. Execute the four isolated release runs only from the frozen plan and preserve each raw trajectory separately.
10. Compile trajectories into FAR packages, write the primary comparison, and hash-freeze it before accessing benchmark outcome fields.

## Security boundary

The API key is never stored in source control. GitHub Actions injects it only into the credential-gated job. The workflow does not print the key and explicitly registers it for masking. Generated artifacts must not contain request headers, environment dumps, or raw secret values.

## Cost boundary

The frozen configuration limits each run to $25 and the experiment to $100 total. A failed or interrupted run still consumes provider charges already incurred. Do not rerun automatically; record the failure and make a separate, explicit decision.
