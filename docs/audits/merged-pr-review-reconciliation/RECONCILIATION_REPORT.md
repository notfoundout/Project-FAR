# Merged-PR finding reconciliation

Audited main: `ff398005894827ef2dbf91a0195b98048a9deafd`
Frozen baseline Git blob: `69b72e0247b1c1604e03789a472559f8be9eeffb`

## Result

- Source findings: 402
- Residual findings: 379
- `cannot_verify`: 376
- `fixed_on_current_main`: 15
- `obsolete_after_later_changes`: 8
- `still_reproducible`: 3

Unaudited findings fail closed to `cannot_verify`; they are not claimed reproducible.
Unaudited experiment-blocking status remains `unknown`; no keyword heuristic is treated as authoritative.

## Residual counts

- By risk: `{"high": 121, "medium": 258}`
- By subsystem: `{"canonical-theory": 111, "ci-and-automation": 13, "commercial-validation": 15, "comparative-experiments": 26, "documentation-and-governance": 65, "external-validation": 35, "frameworks": 12, "mechanization": 4, "repository-metadata": 2, "research-records": 1, "test-infrastructure": 7, "validation-engine": 3, "validators-and-tooling": 85}`
- By experiment-blocking status: `{"true": 3, "unknown": 376}`

**121 unresolved P1 findings require verification or remediation.**
