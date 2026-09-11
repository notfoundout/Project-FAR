# Merged-PR finding reconciliation

Audited main: `8d6f5ae10acd373461e4eeaf4b4ec5817c77b2ad`
Frozen baseline Git blob: `69b72e0247b1c1604e03789a472559f8be9eeffb`

## Result

- Source findings: 402
- Residual findings: 392
- `cannot_verify`: 389
- `fixed_on_current_main`: 2
- `obsolete_after_later_changes`: 8
- `still_reproducible`: 3

Unaudited findings fail closed to `cannot_verify`; they are not claimed reproducible.
Unaudited experiment-blocking status remains `unknown`; no keyword heuristic is treated as authoritative.

## Residual counts

- By risk: `{"high": 123, "medium": 269}`
- By subsystem: `{"canonical-theory": 111, "ci-and-automation": 13, "commercial-validation": 20, "comparative-experiments": 26, "documentation-and-governance": 65, "external-validation": 35, "frameworks": 13, "mechanization": 7, "repository-metadata": 2, "research-records": 4, "test-infrastructure": 7, "validation-engine": 4, "validators-and-tooling": 85}`
- By experiment-blocking status: `{"true": 3, "unknown": 389}`

**123 unresolved P1 findings require verification or remediation.**
