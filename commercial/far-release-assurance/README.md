# FAR Release Assurance

FAR Release Assurance is a deterministic command-line gate for comparing disclosed, instrumented baseline and candidate AI-agent releases.

It validates release packages, inventories declared machinery, compares integrity-relevant changes, writes evidence-bound reports, and returns stable CI exit codes.

## Install

```bash
python -m pip install ./commercial/far-release-assurance
far-release --help
```

## Core commands

```bash
far-release validate release.json
far-release inventory release.json --output inventory.json
far-release compare --baseline baseline.json --candidate candidate.json --output comparison.json
far-release report --baseline baseline.json --candidate candidate.json --output-directory far-report
far-release gate --baseline baseline.json --candidate candidate.json --output-directory far-report
```

Gate exit codes are `0` for Pass, `20` for Review required, `30` for Blocked, `40` for Unknown, `10` for invalid release-package input, and `11` for an unsupported internal command path.

## Scope boundary

The tool evaluates disclosed and instrumented release packages. It does not establish hidden cognition, complete telemetry, complete causal truth, safety certification, legal compliance, or validation of Project FAR research hypotheses.
