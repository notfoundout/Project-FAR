# Candidate 002 findings

## Identity and ordering

- Candidate: `scikit-learn__scikit-learn-14125.traj`
- Eligible population: 2,240 trajectories
- Deterministic selection index: 1,609
- Outcome fields read during the primary stage: no
- Primary result frozen before reveal: yes
- Blind stage ordering preserved: yes

## Primary FAR result

FAR returned `unverifiable` before benchmark outcome reveal.

Findings:

- `declared-unknowns`
- `trace-incomplete`

The ordinary SWE-agent trajectory did not establish complete event capture or semantic completeness. Under the preregistered absence rule, missing evidence therefore remained unverifiable rather than being treated as evidence that an action, dependency, or failure did not occur.

## Revealed benchmark result

After the primary result and hashes were frozen, the benchmark fields were revealed:

- `resolved`: `false`
- `exit_status`: `submitted`

The blind FAR result was conservative and compatible with the unresolved benchmark outcome, but it did not independently identify the benchmark failure mode. One candidate cannot establish general detection performance.

## Evidence hashes

- Source dataset: `ed6c7d9a0f39fcfbb890eedd72bdf0ccfe295ac7a1f17b468f787515bdbe201e`
- Trajectory: `ae28baae1a167dcd0ba5f50012775453a10c31748964e67d90e0f1aab3e16714`
- Submission: `3d2bf97fac268401a00e5437a61596ebc2aa7f07a1ffbd878eefb66d933e3bdf`
- Decision package: `64c765229d6c772e4ccbe74ff45b03374d1721bff5702992389bada0a35a5f9d`
- Adjudication: `2d5f900e58aef1b01790d9a889ac8a6a9cfb40391e01b5e39c39aa6910d8968a`
- Primary freeze before reveal: `870fedae9d76eab1835550fbb349e988216440eed1a926f0187f8ddec169c8e8`

## Conclusion

Candidate 002 validates that Project FAR can preserve a blind stage boundary, ingest an ordinary external trace, produce deterministic auditable outputs, and refuse unsupported certainty. It does not yet establish broad external failure-detection accuracy or universal operational adequacy.
