# SWE-agent External Comparison v2 Execution Status

## Current state

- Case preregistered.
- Exact replacement model: `gemini-3.1-pro-preview`.
- Provider-access attestation: pending.
- Execution inputs: not yet frozen.
- Four-run matrix: defined but not started.
- v2 attempts recorded: zero.
- Benchmark outcomes accessed: no.
- Prior blocked case imported: no.

## Next authorized action

After this setup is merged, dispatch the v2 workflow with:

- stage: `access-probe`
- confirmation: `PROBE-FAR-GEMINI-3-1-PRO-PREVIEW`

A successful fixed non-benchmark response will generate a separate provider-access freeze pull request. Do not run `plan` or `execute` until that pull request is green and merged.

## Prohibited actions

- Do not modify or reset the earlier blocked case.
- Do not import its execution state.
- Do not substitute another model inside this case.
- Do not access benchmark outcomes before the primary comparison freeze.
