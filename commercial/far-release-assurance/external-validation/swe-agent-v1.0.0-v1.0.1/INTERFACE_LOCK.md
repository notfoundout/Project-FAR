# Pinned SWE-bench interface lock

The environment-preparation controller is bound to SWE-bench commit `f7bbbb2ccdf479001d6467c9e34af59e44a840f9`.

At that revision, `TestSpec` exposes these script properties:

- `setup_env_script`
- `install_repo_script`
- `eval_script`

It does not expose `setup_repo_script`.

The workflow and controller verify this interface before any Docker build. A mismatch is a hard failure and requires an explicit harness-version update rather than an inferred compatibility workaround.
