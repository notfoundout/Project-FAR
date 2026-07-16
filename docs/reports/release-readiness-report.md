# Release Readiness Report

This advisory report is the canonical Project FAR release checklist. It never publishes a GitHub Release and does not authorize theory changes.

## Repository Overview

| Metric | Current | Source |
|---|---:|---|
| Markdown files | 830 | [.](../..) |
| Theory files | 256 | [theory](../../theory) |
| Python tools | 50 | [tools](../../tools) |
| Reports | 185 | [docs/reports](.) |
| Registries | 10 | [theory](../../theory) |
| Proof objects | 15 | [theory/proof-objects](../../theory/proof-objects) |
| Examples | 43 | [examples](../../examples) |
| Maintenance documents | 5 | [docs/maintenance](../maintenance) |
| Releases | 17 | [docs/releases](../releases) |
| Internal evaluations | 23 | [theory/evaluation/evidence-registry.yaml](../../theory/evaluation/evidence-registry.yaml) |
| External evaluations | 29 | [theory/evaluation/external-validation-registry.yaml](../../theory/evaluation/external-validation-registry.yaml) |
| Adversarial fixtures | 14 | [theory/falsification/adversarial-test-suite.yaml](../../theory/falsification/adversarial-test-suite.yaml) |
| Counterexample fixtures | 1 | [tests](../../tests) |
| Candidate primitive failures | 0 | [theory/falsification/primitive-pressure-registry.yaml](../../theory/falsification/primitive-pressure-registry.yaml) |
| Conservative extensions | 35 | [theory/falsification/primitive-pressure-registry.yaml](../../theory/falsification/primitive-pressure-registry.yaml) |
| Fits FAR | 14 | [theory/evaluation/evidence-registry.yaml](../../theory/evaluation/evidence-registry.yaml) |
| Unresolved cases | 17 | [docs/reports/research-gap-report.md](research-gap-report.md) |
| Unresolved gaps | 160 | [docs/reports/research-gap-report.md](research-gap-report.md) |
| Documentation coverage | 830 | [docs](..) |
| Health-check availability | 1 | [tools/repo_health_check.py](../../tools/repo_health_check.py) |

## Validation Results

| Area | Status | Evidence |
|---|---|---|
| Repository Health | PASS | `make health-fast` |
| Internal Links | PASS | [tools/check_internal_links.py](../../tools/check_internal_links.py) |
| Generated Reports | PASS | [docs/reports/project-status-generated.md](project-status-generated.md) |
| README Synchronization | PASS | [README.md](../../README.md) |
| Release Consistency | PASS | [tools/check_release_consistency.py](../../tools/check_release_consistency.py) |
| Registry Validation | PASS | [tools/check_registry.py](../../tools/check_registry.py) |
| Critical Research Gaps | 0 | [docs/reports/research-gap-report.md](research-gap-report.md) |
| Candidate Primitive Failures | 0 | [theory/falsification/primitive-pressure-registry.yaml](../../theory/falsification/primitive-pressure-registry.yaml) |
| Documentation Completeness | 830 | [docs](..) |
| Planner Freshness | PASS | [docs/planning/next-actions.md](../planning/next-actions.md) |

## Documentation Status

- Markdown files: 830
- Reports: 185
- Maintenance documents: 5

## Planning Status

- Planner: [tools/self_advancement_plan.py](../../tools/self_advancement_plan.py)
- Next actions: [docs/planning/next-actions.md](../planning/next-actions.md)

## Outstanding Critical Issues

- Critical issues: 0

## Outstanding High Priority Issues

- High priority issues: 1

## Repository Alerts

| Category | Status | Source |
|---|---:|---|
| Critical Issues | 0 | [docs/reports/research-gap-report.md](research-gap-report.md) |
| High Priority Issues | 1 | [docs/reports/research-gap-report.md](research-gap-report.md) |
| Repository Health | PASS | [docs/maintenance/repository-health-checks.md](../maintenance/repository-health-checks.md) |
| Planner Status | CURRENT | [docs/planning/next-actions.md](../planning/next-actions.md) |
| CI Status | Manual workflows available | [.github/workflows/repository-health.yml](../../.github/workflows/repository-health.yml) |
| Release Readiness | READY WITH WARNINGS | [docs/reports/release-readiness-report.md](release-readiness-report.md) |

## Release Recommendation

READY WITH WARNINGS

## Next Required Actions

- Run `make health` before any human-approved release publication.
- Resolve critical issues before release.
- Review high priority issues when recommendation is READY WITH WARNINGS.

<details><summary>Health output excerpt</summary>

```text
- WARNING: step s5 lemma_application has weak semantic overlap with L-004 metadata statement
- WARNING: step s6 lemma_application has weak semantic overlap with L-005 metadata statement
PASS proof object theory/proof-objects/T-002.proof.yaml

==> proof object theory/proof-objects/T-003.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-003.proof.yaml
PROOF OBJECT CHECK PASSED
- WARNING: step s2 axiom_application has weak semantic overlap with A1 metadata statement
- WARNING: step s3 axiom_application has weak semantic overlap with A1 metadata statement
- WARNING: step s3 axiom_application has weak semantic overlap with A2 metadata statement
- WARNING: step s4 axiom_application has weak semantic overlap with A4 metadata statement
- WARNING: step s4 axiom_application has weak semantic overlap with A1 metadata statement
- WARNING: step s4 axiom_application has weak semantic overlap with A3 metadata statement
PASS proof object theory/proof-objects/T-003.proof.yaml

==> proof object theory/proof-objects/T-004.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-004.proof.yaml
PROOF OBJECT CHECK PASSED
PASS proof object theory/proof-objects/T-004.proof.yaml

==> proof object theory/proof-objects/T-005.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-005.proof.yaml
PROOF OBJECT CHECK PASSED
- WARNING: step s1 prior_theorem has weak semantic overlap with T-005 metadata statement
- WARNING: step s1 prior_theorem has weak semantic overlap with T-003 metadata statement
PASS proof object theory/proof-objects/T-005.proof.yaml

==> proof object theory/proof-objects/T-006.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-006.proof.yaml
PROOF OBJECT CHECK PASSED
PASS proof object theory/proof-objects/T-006.proof.yaml

==> proof object theory/proof-objects/T-007.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-007.proof.yaml
PROOF OBJECT CHECK PASSED
- WARNING: step s1 prior_theorem has weak semantic overlap with T-007 metadata statement
- WARNING: step s1 prior_theorem has weak semantic overlap with T-003 metadata statement
- WARNING: step s3 prior_theorem has weak semantic overlap with T-006 metadata statement
PASS proof object theory/proof-objects/T-007.proof.yaml

==> proof object theory/proof-objects/T-008.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-008.proof.yaml
PROOF OBJECT CHECK PASSED
- WARNING: step s1 prior_theorem has weak semantic overlap with T-008 metadata statement
- WARNING: step s3 prior_theorem has weak semantic overlap with T-004 metadata statement
PASS proof object theory/proof-objects/T-008.proof.yaml

==> proof object theory/proof-objects/T-009.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-009.proof.yaml
PROOF OBJECT CHECK PASSED
- WARNING: step s2 lemma_application has weak semantic overlap with L-007 metadata statement
PASS proof object theory/proof-objects/T-009.proof.yaml

==> proof object theory/proof-objects/T-010.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-010.proof.yaml
PROOF OBJECT CHECK PASSED
- WARNING: step s1 prior_theorem has weak semantic overlap with T-010 metadata statement
- WARNING: step s1 prior_theorem has weak semantic overlap with T-003 metadata statement
- WARNING: step s4 prior_theorem has weak semantic overlap with T-004 metadata statement
- WARNING: step s5 prior_proposition has weak semantic overlap with P-007 metadata statement
PASS proof object theory/proof-objects/T-010.proof.yaml

==> proof object theory/proof-objects/T-011.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-011.proof.yaml
PROOF OBJECT CHECK PASSED
- WARNING: step s2 prior_theorem has weak semantic overlap with T-011 metadata statement
- WARNING: step s2 prior_theorem has weak semantic overlap with T-006 metadata statement
PASS proof object theory/proof-objects/T-011.proof.yaml

==> proof object theory/proof-objects/T-012.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-012.proof.yaml
PROOF OBJECT CHECK PASSED
PASS proof object theory/proof-objects/T-012.proof.yaml

==> proof object theory/proof-objects/T-013.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-013.proof.yaml
PROOF OBJECT CHECK PASSED
PASS proof object theory/proof-objects/T-013.proof.yaml

==> proof object theory/proof-objects/T-014.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-014.proof.yaml
PROOF OBJECT CHECK PASSED
PASS proof object theory/proof-objects/T-014.proof.yaml

==> proof object theory/proof-objects/T-015.proof.yaml: /root/.pyenv/versions/3.14.4/bin/python tools/check_proof_object.py theory/proof-objects/T-015.proof.yaml
PROOF OBJECT CHECK PASSED
- WARNING: step s2 prior_theorem has weak semantic overlap with T-015 metadata statement
- WARNING: step s2 prior_theorem has weak semantic overlap with T-003 metadata statement
PASS proof object theory/proof-objects/T-015.proof.yaml

Repository health summary:
passed: 106 warnings: 0 failures: 0
```

</details>
