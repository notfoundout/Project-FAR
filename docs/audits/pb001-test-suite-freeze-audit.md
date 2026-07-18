# PB-001 Test-Suite Freeze Audit

## Scope

This audit records the controls applied while freezing PBTS-001.

## Dependency audit

PBTS-001 depends only on the frozen reasoning domain, IRD-001, and PB-001. It does not depend on FARA, FARO, FAR-IR, candidate compilers, or candidate-specific evaluators.

## Coverage audit

The suite requires:

- exactly one primary discriminating pair for each P1-P8 axis;
- one ablation challenge for every axis;
- at least two cases for every D1-D16 target class;
- all ten mandatory IRD-001 countermodels;
- hidden-recovery review;
- adversarial addition search.

Coverage is a prerequisite for interpretation, not proof of adequacy.

## Anti-confirmation audit

All execution gates are false. No responses, scores, results, or favorable classifications are included. The suite allows redundancy, incompleteness, class-specific bases, no finite basis, IRD revision, observability blockage, and insufficient evidence.

## Hidden-recovery audit

The frozen protocol checks aliases, metadata, compiler state, verifier assumptions, runtime interpreters, evaluator repair, external operator knowledge, exception policies, and unavailable trace information.

## Observability audit

The suite may not infer stronger preservation than the declared O0-O4 access supports. P8 explicitly tests correspondence claims.

## Separation audit

The suite freeze is separate from execution and interpretation. Post-exposure changes require a new version. Representation-theorem work remains blocked until execution results satisfy or explicitly fail the advance gate.

## Nonclaims

This audit does not establish PB-001 sufficiency, necessity, independence, minimality, completeness, FARA compliance, universality, superiority, or independent replication.
