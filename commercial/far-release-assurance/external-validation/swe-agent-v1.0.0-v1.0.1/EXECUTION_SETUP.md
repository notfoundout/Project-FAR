# Zero-cost execution setup

## What is already provisioned

The repository contains a manual GitHub Actions environment in `.github/workflows/far-swe-agent-execution.yml`.

It provides three explicit stages:

1. `resolve-image` — pulls the selected SWE-bench image and reports its immutable digest without using an API key or making a model call.
2. `preflight` — validates the committed digest, manifest, configuration hash, run matrix, and local tool availability.
3. `plan` — requires the Gemini secret and the exact confirmation phrase `RUN-FAR-FREE-TIER-COMPARISON`, then writes the deterministic four-run plan. It does not reveal benchmark outcomes or start model calls.

The workflow uses a standard `ubuntu-24.04` GitHub-hosted runner. Standard runners are free for public repositories. It serializes runs through a concurrency lock, removes unused runner packages for disk capacity, masks the API key, uses read-only repository permissions, and uploads only non-secret execution artifacts.

## Free account-bound prerequisite

Create a Gemini Developer API key in Google AI Studio. A new Gemini API project begins on the free tier and does not require a billing account for supported free-tier models. The key must not be committed, pasted into issues, included in artifacts, or sent through chat.

Add it to GitHub as either:

- an environment secret named `GEMINI_API_KEY` in the `far-swe-agent-execution` environment; or
- a repository Actions secret named `GEMINI_API_KEY`.

Environment-scoped storage is preferred because it can require reviewer approval before the credential becomes available to a job.

## Required execution order

1. Merge the PR containing this workflow.
2. Open **Actions → FAR SWE-agent External Comparison → Run workflow**.
3. Run `resolve-image`.
4. Download the artifact and copy the reported `sha256:...` digest into `manifest.json`.
5. Change manifest status to `execution_inputs_frozen` in a new reviewed commit.
6. Run `preflight` and require success.
7. Create and store the free `GEMINI_API_KEY` secret.
8. Run `plan` with confirmation `RUN-FAR-FREE-TIER-COMPARISON`.
9. Execute one frozen release run at a time. If Google returns a quota or rate-limit error, stop cleanly and resume the same run after the quota window resets. Never substitute another model.
10. Preserve each raw trajectory separately.
11. Compile trajectories into FAR packages, write the primary comparison, and hash-freeze it before accessing benchmark outcome fields.

## Free-tier limitations

The selected model is `gemini-2.5-pro`, accessed through LiteLLM as `gemini/gemini-2.5-pro`. Google lists free input and output tokens for this stable model, but free-tier quotas are limited and can change. Four complete SWE-agent runs may require multiple quota windows. Free-tier prompts and outputs may be used by Google to improve its products, so this path is only appropriate for the selected public SWE-bench task and must not be used with confidential customer artifacts.

## Security boundary

The API key is never stored in source control. GitHub Actions injects it only into the credential-gated job. The workflow does not print the key and explicitly registers it for masking. Generated artifacts must not contain request headers, environment dumps, or raw secret values.

## Cost boundary

The model configuration has zero monetary cost limits and a 30-call ceiling per run. The workflow uses free public-repository GitHub Actions capacity. The experiment must stop rather than fall back to a paid tier or another model. Zero cash cost does not imply unlimited quota, guaranteed availability, or identical backend behavior across quota windows.
