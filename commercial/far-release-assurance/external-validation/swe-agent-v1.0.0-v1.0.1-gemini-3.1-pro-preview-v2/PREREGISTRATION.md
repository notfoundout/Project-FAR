# SWE-agent External Comparison v2 Preregistration

## Case identity

`SWE-agent v1.0.0 versus v1.0.1 / Gemini 3.1 Pro Preview / v2`

Case ID:

`swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2`

## Why this case exists

The earlier frozen case used `gemini-2.5-pro`. Three attempts were preserved, and the final attempt established that the exact endpoint was unavailable to the API project. The corrected controller classified that condition as terminal `provider_model_unavailable`.

That earlier case remains `BLOCKED`. It is not reset, repaired by substitution, or counted as a comparative result.

This v2 case is a new experiment. Google’s official Gemini API deprecation documentation identifies `gemini-3.1-pro-preview` as the recommended replacement for `gemini-2.5-pro`.

## Fixed before provider access

The following are preregistered before the access probe:

- SWE-agent baseline: v1.0.0 at commit `8ed382c`;
- SWE-agent candidate: v1.0.1 at commit `6aff215`;
- task: `scikit-learn__scikit-learn-14125`;
- immutable environment image and digest;
- model: `gemini-3.1-pro-preview`;
- temperature, top-p, call limit, retry policy, tools, templates, and demonstrations;
- two repetitions per release;
- baseline-baseline-candidate-candidate ordering;
- outcome-blind boundary;
- four fresh run slots with no imported state from the blocked case.

## Provider-access gate

The case is not execution-frozen at repository setup time.

A fixed non-benchmark request must first receive the exact response `FAR_ACCESS_OK` from the exact `gemini-3.1-pro-preview` endpoint. The probe:

- does not read or send the benchmark task;
- does not access benchmark outcomes;
- does not persist the API key;
- records only sanitized access evidence and hashes;
- creates a reviewable freeze pull request rather than changing `main` directly.

Execution is prohibited until that freeze pull request passes the repository’s required checks and is merged.

## Execution boundary

Planning and preserved-state reconciliation do not require or read `GEMINI_API_KEY`. The secret is injected only for:

1. the exact provider-access probe; or
2. an actual frozen model execution after all earlier gates pass.

## Cost boundary

Provider billing may apply. The `0.0` values preserved in the SWE-agent configuration and controller plan are compatibility values, not a representation that execution is free. A project-level provider spend cap should be configured before execution.

## Claim boundary

Results from the blocked Gemini 2.5 Pro case and this Gemini 3.1 Pro Preview case may not be pooled. A model change creates a new case and a new four-run matrix.

This case can provide one bounded external version-to-version comparison. It cannot establish universal accuracy, safety, compliance, commercial readiness, enterprise readiness, or general superiority.
