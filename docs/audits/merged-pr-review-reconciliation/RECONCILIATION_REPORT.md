# Merged-PR finding reconciliation

Audited main: `5ca27d5c40281771cf74aa29704c2a06868a16ae`

## Result

- Source findings: 402
- Residual findings: 400
- `cannot_verify`: 400
- `fixed_on_current_main`: 2

Unaudited findings fail closed to `cannot_verify`; they are not claimed reproducible.
Unaudited experiment-blocking status remains `unknown`; no keyword heuristic is treated as authoritative.

## Residual counts

- By risk: `{"high": 124, "medium": 276}`
- By subsystem: `{"canonical-theory": 111, "ci-and-automation": 13, "commercial-validation": 20, "comparative-experiments": 26, "documentation-and-governance": 69, "external-validation": 35, "frameworks": 13, "mechanization": 7, "repository-metadata": 6, "research-records": 4, "test-infrastructure": 7, "validation-engine": 4, "validators-and-tooling": 85}`
- By experiment-blocking status: `{"unknown": 400}`

**124 unresolved P1 findings require verification or remediation.**
