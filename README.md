# Project FAR

[![Release v1.0.0](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/latest)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

## Latest release: v1.0.0

The latest published GitHub repository release is [v1.0.0](https://github.com/notfoundout/Project-FAR/releases/tag/v1.0.0). The executable package metadata currently declares version `0.6.0`. These are separate version surfaces: the release tag records the published repository release, while `pyproject.toml` is authoritative for the installable package version.

## Central result

The registered Universal Proof Program `POST-TUE-UPP-001` is complete. Its terminal adjudication is:

`strictly_weakened_relative_rccd_universality_theorem_proved_with_complete_dependency_audit_and_open_world_boundary`

The result is relative and operational. It applies only under the frozen target-class, admissibility, faithfulness, machinery-closure, and commitment-equivalence premises. The end-to-end semantic composition is executable and audited but is not one kernel-checked proof object, and maximality is limited to frozen extension rules and a finite registered challenge ledger.

Public evaluation is authorized only when the exact theorem, premises, mechanization status, open-world boundary, Unknown discipline, and nonclaims are disclosed together.

- [Terminal theorem disclosure](docs/research/upp-w15-terminal-theorem-v1.0.md)
- [Terminal theorem audit](docs/audits/upp-w15-terminal-theorem-audit.md)
- [Post-terminal public-evaluation program](docs/governance/post-terminal-public-evaluation-program-v1.0.md)
- [Central research program](docs/governance/central-research-program.md)

## Post-terminal phase

The deductive UPP queue is closed. The active phase is independent criticism, countermodel search, proof review, kernel-checked reconstruction, bounded replication, and application-correspondence testing. There is no `UPP-W16`; any stronger deductive claim requires a newly registered program.

The generated dashboard below is a historical status surface for the older bounded REP/ADJ/W3.5 program. It does not override the later UPP terminal adjudication or define the repository's current phase.

## Latest bounded external evaluation

The frozen SWE-agent v2 comparison observed **0/2 resolved runs for v1.0.0 and 0/2 for v1.0.1** on one task. The recorded observation is `no_observed_resolution_difference`, and the bounded decision remains `REVIEW_REQUIRED`. This does **not** demonstrate equivalence, superiority, safety, readiness, or general performance. See the [post-experiment audit](docs/audits/post-swe-agent-v2-stabilization-audit.md) and [reproducibility guide](docs/reproducibility/swe-agent-v2.md).

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Historical bounded-program status

- Historical bounded-program phase: W3.5 machinery/cost, claim-impact, and preserved-failure closure
- Repository health status at generation: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- Historical W5 status: blocked by incomplete `W3.5-SDG-001`

## Track Status

| Track | Status | Current boundary |
|---|---|---|
| REP | W0-W4 complete | Bounded construction and registered controls; theorem unproved |
| ADJ | Corpus, factorization, discrimination, specificity, and candidate execution complete | 8 positive, 8 contrast, 2 disputed; 648/648 candidate trials preserved |
| USD | Target frozen | Registered-scope candidate axes resolved; universal structure unresolved |
| W5 | Blocked | Requires complete evidence-backed `W3.5-SDG-001` |

## Registered ADJ Results

- Factorization interpretation: `fara_constrained_equivalent`.
- Reasoning discrimination: 8/8 positives reasoning-like; 8/8 contrasts nonreasoning-like; 2/2 disputed borderline.
- FARA-specificity classification: `fara_role_directness_without_unique_discriminative_capacity`.
- Candidate result: `registered_candidate_axes_resolved_at_frozen_internal_scope`.
- Structural necessity: unresolved 0; supported 7; refuted 5; partial 0.
- Candidate evidence: complete project-authored internal execution; not independent replication.

## Historical Priority Tasks

### STRATEGIC-004: Complete W3.5 closure

- Complete cross-package machinery/cost, claim-impact, and preserved-failure artifacts without promoting registered-scope results to universal claims.

### STRATEGIC-005: Assemble W5

- Remains blocked until every required W3.5 artifact is complete and the gate is evidence-backed resolved.

## Historical Roadmap

- REP: W0-W4 complete at bounded `S_core` scope.
- ADJ: close machinery/cost, claim-impact, and preserved-failure evidence.
- USD: universal structure remains unresolved.
- W5: blocked until W3.5 resolves with immutable evidence.

## Command Center

```bash
make research-check
make health-fast
make health
make docs-check
make plan
make dashboard
```

<!-- END GENERATED PROJECT FAR DASHBOARD -->

## Post-terminal validation

```bash
python tools/check_post_terminal_public_evaluation.py
```

## Certification and Architecture Navigation

- Repository certification governance: [docs/governance/repository-certification-standard.md](docs/governance/repository-certification-standard.md).
- Repository certification inventory baseline: [docs/audits/repository-certification-inventory-audit.md](docs/audits/repository-certification-inventory-audit.md).
- Semantic certification and terminology baseline: [docs/audits/semantic-certification-report.md](docs/audits/semantic-certification-report.md).
- Canonical vocabulary index: [docs/glossary/canonical-vocabulary-index.md](docs/glossary/canonical-vocabulary-index.md).
- Repository architecture certification and report-root policy: [docs/audits/repository-architecture-certification-report.md](docs/audits/repository-architecture-certification-report.md).
- Repository Certification Index: [docs/certification/README.md](docs/certification/README.md).
- Repository Domain Registry: [docs/architecture/repository-domain-registry.md](docs/architecture/repository-domain-registry.md).
- Documentation standardization report: [docs/audits/documentation-standardization-report.md](docs/audits/documentation-standardization-report.md).
- Repository compliance enforcement report: [docs/audits/repository-compliance-enforcement-report.md](docs/audits/repository-compliance-enforcement-report.md).
- Independent repository certification audit: [docs/audits/independent-repository-certification-audit.md](docs/audits/independent-repository-certification-audit.md).
- Repository certification status: [docs/certification/repository-certification-status.md](docs/certification/repository-certification-status.md).

## Mechanization MVP

Phase 3 mechanization provides an executable MVP for the `far-ir/1.0` interchange format. It includes a canonical Python IR, JSON/YAML parsing, deterministic normalization and serialization, graph construction and dependency validation, structured diagnostics, a CLI, and a versioned conformance suite.

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
far version
far validate examples/mechanization/minimal-investigation.json
far normalize examples/mechanization/minimal-investigation.json
far graph examples/mechanization/minimal-investigation.json
python -m mechanization.far_mechanization.conformance
```

The MVP does not by itself verify the terminal theorem or establish application correspondence.

## Canonical theory navigation

The authoritative dependency order is **foundations → shared theory → FARA → FAR → FARO**. Start with the [canonical map](docs/CANONICAL_MAP.md), [terminology authority](docs/glossary/canonical-terminology.md), [framework boundaries](docs/governance/framework-boundaries.md), [claim-status matrix](docs/governance/claim-status-matrix.md), [limitations](docs/governance/limitations-register.md), and [open problems](docs/governance/open-problems-register.md). Methodology, evidence, examples, papers, software, commercial material, and archive records are downstream; none proves universality or supplies theory prerequisites.

Repository navigation continues through the [documentation index](docs/README.md),
[foundations](foundations/README.md), [shared theory](theory/README.md),
[frameworks](frameworks/README.md), [methodology](methodology/README.md), and
[papers](papers/README.md) entry points.
