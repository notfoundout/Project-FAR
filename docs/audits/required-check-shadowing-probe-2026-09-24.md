# Required-Check Shadowing Probe (2026-09-24)

Status: **Live evidence** (I1: author-side experiment on the real repository). This is not independent validation.

Machine-readable record: [`required-check-shadowing-probe-2026-09-24.json`](required-check-shadowing-probe-2026-09-24.json). It contains the trimmed API responses and the SHA-256 of each raw capture.

## Question

`main` requires the status check `merge-authority`, bound to the GitHub Actions App (id 15368). Can a pull request satisfy that requirement with a job it adds itself while it carries an unauthorized protected-artifact change?

## Method

The repository owner approved a throwaway PR, #540 on branch `probe/shadow-merge-authority`. It was never merged. It contained:

1. `.github/workflows/zz-shadow-probe.yml`: a `pull_request` workflow whose only job is named `merge-authority` and always succeeds.
2. An unauthorized protected repin: one line appended to `tests/test_validation_trace_regression.py`, with its assurance-lock pin moved. Locally, `python -m far_validation weakening --base 7fb4816` reports FAIL for it.

Check runs and pull-request state were read from the GitHub REST API at each stage.

## Results

| State | Head | `merge-authority` check runs (App id: conclusion) | `mergeable_state` |
|---|---|---|---|
| A: genuine job ran and failed; shadow succeeded | `3bf4b23f` | 15368: failure (genuine, run 35968015186); 15368: success (shadow, run 35968015198) | `blocked` |
| B: shadow re-run so its success is the newest run | `3bf4b23f` | 15368: success (shadow re-run); 15368: failure (genuine); 15368: success (shadow, first attempt) | `blocked` |
| C: candidate renames the genuine job in `validator-assurance.yml` | `0edca5d7` | 15368: success (shadow only); the renamed genuine job was skipped | **`unstable`**, i.e. mergeable; only non-required checks fail |

## Findings

1. **GitHub attaches every same-named check run from GitHub Actions to the head**, all with App id 15368. A required check bound to GitHub Actions cannot tell the trusted job from a candidate's job.
2. **When the genuine job reports a failure, a shadow success does not override it** (states A and B): the PR stays `blocked`. On this point the required-check logic failed closed.
3. **When the genuine job does not report the context, the shadow alone satisfies branch protection** (state C). A `pull_request` workflow's definition comes from the candidate, so a candidate can always arrange this. State C was mergeable while carrying an unauthorized protected repin. **This is a live bypass of `main`'s current protection** (red-team RT-10 / LIM-049). It stays open until the App-bound gate is bootstrapped.
4. GitHub Actions therefore cannot be the trusted `protected-repin-gate` principal, whatever the ordering semantics. The required check must be bound to a dedicated App's ID ([procedure](../governance/protected-repin-procedure.md)).

## Cleanup

- PR #540 was closed unmerged immediately after state C was recorded.
- The session's git relay refused to delete the remote branch. The branch was instead reset to a commit whose tree is byte-identical to `main` at `7fb4816` (tree `a8c8c2e2…`), so reopening or merging it changes nothing.
- The owner should delete `probe/shadow-merge-authority`.

## Limits

- The required-check configuration was re-read live after the probe, from the public branch summary (`GET /repos/notfoundout/Project-FAR/branches/main`). It showed `protection.required_status_checks.checks = [{context: merge-authority, app_id: 15368}]` with `enforcement_level: everyone`. The full protection object needs Administration read, which this session does not have. The owner exports it at bootstrap.
- `GET …/rulesets?includes_parents=true` and `GET …/rules/branches/main` both returned `[]`: no rulesets apply to `main`.
- The probe does not test the App-bound requirement. That requires the dedicated App, and it is covered by the mandatory post-bootstrap probes P1–P7.
