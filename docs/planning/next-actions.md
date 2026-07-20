# Next Actions

## Navigation

- README Command Center: [README.md](../../README.md)
- Project Status: [docs/reports/project-status-generated.md](../reports/project-status-generated.md)
- Research Gaps: [docs/reports/research-gap-report.md](../reports/research-gap-report.md)
- Next Actions: [docs/planning/next-actions.md](next-actions.md)

Generated under the separated REP, ADJ, and USD program.

W0–W3 remain frozen project-authored REP packages. W4 and W3.5 are active in parallel. W5 is blocked until both resolve. Representation progress does not update the universal-structure claim.

## Ranked Next Actions

### STRATEGIC-001: Execute the W4 S_core formal negative controls

- Source: central research program
- Priority: high
- Why it matters: `OBS-SC-010` must determine whether NC-01 through NC-10 are rejected by the frozen clauses or expose a valid countermodel.
- Affected files:
  - [docs/research/s-core-construction-obstruction-ledger-v1.0.md](../research/s-core-construction-obstruction-ledger-v1.0.md)
  - [theory/evaluation/s-core-construction-obstruction-ledger.json](../../theory/evaluation/s-core-construction-obstruction-ledger.json)
  - [docs/methodology/negative-control-suite-v1.0.md](../methodology/negative-control-suite-v1.0.md)
- Expected outcome: a versioned W4 result without changing the frozen representation definition.
- Risk level: high
- Suggested branch name: `research/prove-s-core-w4-negative-controls`
- Suggested PR title: `Prove S_core W4 formal negative controls`

### STRATEGIC-002: Execute W3.5 baseline factorization and universal-discovery gate

- Source: central research program
- Priority: high
- Why it matters: W3 proves a complete finite FARA witness construction but not FARA-specificity, generic-baseline separation, reasoning-specificity, necessity, minimality, or universal structure.
- Affected files:
  - [docs/research/w3-5-specificity-and-discovery-gate-v1.0.md](../research/w3-5-specificity-and-discovery-gate-v1.0.md)
  - [theory/evaluation/w3-5-specificity-and-discovery-gate.json](../../theory/evaluation/w3-5-specificity-and-discovery-gate.json)
  - [docs/research/generic-relational-baseline-v1.0.md](../research/generic-relational-baseline-v1.0.md)
  - [theory/evaluation/universal-structure-candidate-registry.json](../../theory/evaluation/universal-structure-candidate-registry.json)
- Expected outcome: immutable factorization, specificity, contrast, ablation, reconstruction, cost, and claim-impact results.
- Risk level: high
- Suggested branch name: `research/execute-w3-5-specificity-discovery`
- Suggested PR title: `Execute W3.5 specificity and universal-discovery gate`

### STRATEGIC-003: Assemble the finite-core theorem or strongest obstruction

- Source: central research program
- Priority: blocked
- Why it matters: W5 remains blocked until both `OBS-SC-010` and `W3.5-SDG-001` resolve.
- Affected files:
  - [docs/research/s-core-construction-obstruction-ledger-v1.0.md](../research/s-core-construction-obstruction-ledger-v1.0.md)
  - [theory/evaluation/thm-target-001.json](../../theory/evaluation/thm-target-001.json)
  - [theory/evaluation/central-claim-registry.json](../../theory/evaluation/central-claim-registry.json)
- Expected outcome: a bounded REP theorem, equivalence, countermodel, proper-subclass result, impossibility result, or explicit unresolved result with specificity classification.
- Risk level: high
- Suggested branch name: `research/assemble-s-core-result`
- Suggested PR title: `Assemble S_core theorem or obstruction`

## Execution controls

- Preserve `THM-TARGET-001`, `THM-US-TARGET-001`, `FAITHFUL-REP-001`, `P8-ROLE-001`, W0–W3, all failures, and every nonclaim.
- Do not promote REP progress into USD, necessity, minimality, or uniqueness.
- Do not begin W5 while `OBS-SC-010` or `W3.5-SDG-001` remains unresolved.
- Run `make research-check` and `make health-fast`.
