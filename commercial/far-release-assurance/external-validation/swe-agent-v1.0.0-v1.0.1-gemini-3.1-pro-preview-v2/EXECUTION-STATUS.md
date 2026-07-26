# SWE-agent External Comparison v2 Execution Status

## Current state

- Case preregistered.
- Exact replacement model: `gemini-3.1-pro-preview`.
- Provider-access attestation: pending.
- Execution inputs: not yet frozen.
- Four-run matrix: defined but not started.
- Valid v2 comparison attempts recorded: zero.
- Provider-access probe attempts recorded: one unsuccessful probe.
- Benchmark outcomes accessed: no.
- Prior blocked case imported: no.

## Access-probe attempt 1

The first non-benchmark probe reached the exact provider endpoint and received an HTTP 200 response, but the visible response did not equal `FAR_ACCESS_OK`. No attestation was created, no freeze pull request was opened, and no comparison slot was touched.

The original probe capped total output at 16 tokens and omitted `thinkingLevel`. Gemini 3.1 Pro defaults to high thinking, so the probe could exhaust its output allowance before emitting visible text. The failed response payload was not persisted, so that specific finish reason cannot be proven retroactively.

The repaired probe freezes `thinkingLevel: low`, raises `maxOutputTokens` to 1024, excludes returned thought parts from the exact visible-text comparison, and persists sanitized failure diagnostics without raw response text, credentials, task data, or benchmark outcomes.

## Next authorized action

After the probe-repair pull request is green and merged, dispatch the v2 workflow with:

- stage: `access-probe`
- confirmation: `PROBE-FAR-GEMINI-3-1-PRO-PREVIEW`

A successful fixed non-benchmark response will generate a separate provider-access freeze pull request. Do not run `plan` or `execute` until that pull request is green and merged.

## Prohibited actions

- Do not modify or reset the earlier blocked case.
- Do not import its execution state.
- Do not substitute another model inside this case.
- Do not access benchmark outcomes before the primary comparison freeze.
