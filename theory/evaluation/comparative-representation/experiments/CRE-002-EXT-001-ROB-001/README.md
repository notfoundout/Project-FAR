# CRE-002-EXT-001-ROB-001

## Status

Automated multi-implementation robustness track replacing the unexecuted human-team track `CRE-002-EXT-001-REP-001`.

## Purpose

Test whether the frozen CRE-002-EXT-001 scenario survives multiple separately implemented computational normalization paths rather than depending on one implementation path.

## Required architecture

1. Three compiler implementations execute in separate temporary working directories.
2. Each compiler receives only the frozen scenario input and its own process arguments.
3. No compiler receives or can read another compiler's generated artifact during compilation.
4. A separate verifier process receives frozen copies only after all compiler processes finish.
5. The verifier performs deterministic byte-level comparison after canonical serialization.
6. The verifier applies structural mutations and adversarial malformed cases and must reject every changed case.
7. A second complete run must reproduce the same canonical output and digest.

## Claim boundary

A passing result establishes **bounded multi-implementation robustness**: the frozen scenario survived three computational normalization paths, a separately invoked verifier, registered mutations, malformed inputs, and a deterministic rerun.

It is not independent external replication. One agent, researcher, repository, or organization controlling all implementations cannot establish independent human judgment, independent organizational incentives, or absence of shared specification-level mistakes.

## Execution

```bash
python tools/cre002_ext001_robustness.py --check
python -m unittest tests.test_cre002_ext001_rep001_team_registry
```

## Supported conclusion

Only this conclusion is licensed by a passing run:

> For the frozen CRE-002-EXT-001 scenario, three isolated internal implementations produced the same canonical result; a separately invoked verifier accepted the unmodified outputs, rejected the registered mutations and adversarial cases, and a full rerun reproduced the same digest.

No external-replication, universal-sufficiency, necessity, minimality, independence, superiority, FAR-proof, or universal-structure conclusion follows.
