# Project FAR

[![Release](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/tag/v0.4.0)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

This root README is the canonical command center for repository status, health, evidence, planning, and navigation.

## Central Research Program

Project FAR's primary objective is to determine whether every reasoning process necessarily instantiates a common underlying structure and, if so, whether that structure is universal and minimal.

The project does not assume that a universal structure exists or that FAR is that structure.

**[Read the Central Research Program](docs/governance/central-research-program.md)**

## Current Research State

The project now separates three tracks:

- **REP:** finite representation capacity and fidelity;
- **ADJ:** generic-baseline factorization, FARA-specificity, contrast, ablation, reconstruction, and cost;
- **USD:** representation-independent universal-structure discovery.

`SCORE-W0-PROOF-001` through `SCORE-W3-PROOF-001` remain project-authored REP packages. W3 establishes all 24 finite construction lemmas, target-only recovery, semantic agreement, cross-axis coherence, complete machinery accounting, uniformity, composition, and typed witness assembly.

W3 does not establish `OBS-SC-010`, `Nontrivial`, `Faithful_split`, a representation theorem, FARA-specificity, universal structure, necessity, or minimality.

W4 formal negative controls and W3.5 specificity/discovery are active in parallel. W5 is blocked until both resolve.

Run `make research-check` to validate the frozen REP program, the representation–discovery separation, W3.5 gates, universal target, and conservative claim boundaries.

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Repository Status

- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)
- Current project phase: W4 formal negative controls and W3.5 specificity/discovery in parallel
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- Planner status: CURRENT ([planner](tools/self_advancement_plan.py))

## Track Status

| Track | Status | Current boundary |
|---|---|---|
| REP | W4 active | W0–W3 finite construction packages; theorem unproved |
| ADJ | W3.5 frozen, not executed | Generic baseline, specificity, contrast, ablation, reconstruction |
| USD | Target frozen, unexecuted | No universal-structure candidate classified |
| W5 | Blocked | Requires `OBS-SC-010` and `W3.5-SDG-001` |

No aggregate completion percentage is authorized across REP, ADJ, and USD.

## REP Progress Summary

| Formal metric | Current |
|---|---:|
| Registered obligations | 37 |
| Proved construction lemmas | 24 |
| Source boundaries established | 1 |
| Obstruction hypotheses refuted | 8 |
| Open obligations | 4 |
| Completed waves | W0, W1, W2, W3 |
| Active wave | W4 |

## Top Priority Tasks

### STRATEGIC-001: Execute W4 formal negative controls

- Resolve `OBS-SC-010` and NC-01 through NC-10 without changing the frozen representation predicate.

### STRATEGIC-002: Execute W3.5 specificity and universal-discovery gate

- Resolve `GREL-001` factorization, FARA-specificity, reasoning/contrast discrimination, candidate ablation, alternative reconstruction, machinery cost, and claim impact.

### STRATEGIC-003: Assemble W5

- Blocked until W4 and W3.5 resolve.

## Universal-Structure Discovery

- Target: [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)
- Generic baseline: [GREL-001](docs/research/generic-relational-baseline-v1.0.md)
- Reasoning and contrast scope: [RCS-001](docs/research/reasoning-and-contrast-scope-v1.0.md)
- Candidate registry: [US-CANDIDATES-001](theory/evaluation/universal-structure-candidate-registry.json)
- Current result: unresolved

## Repository Navigation

- [Project Status](docs/reports/project-status-generated.md)
- [Next Actions](docs/planning/next-actions.md)
- [Representation–Discovery Separation Standard](docs/governance/representation-discovery-separation-standard-v1.0.md)
- [Deduction-First Proof Roadmap](docs/planning/deduction-first-proof-roadmap.md)
- [Architecture-Neutral Research Roadmap](docs/planning/architecture-neutral-research-roadmap.md)
- [THM-TARGET-001](docs/research/thm-target-001-v1.0.md)
- [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)
- [Generic Relational Baseline](docs/research/generic-relational-baseline-v1.0.md)
- [Reasoning and Contrast Scope](docs/research/reasoning-and-contrast-scope-v1.0.md)
- [W3.5 Gate](docs/research/w3-5-specificity-and-discovery-gate-v1.0.md)
- [S_core W3 Proof](docs/research/s-core-w3-global-witness-proof-v1.0.md)
- [Central Claim Registry](theory/evaluation/central-claim-registry.json)
- [Research Gates](theory/evaluation/research-gates.json)

## Current Roadmap

- REP: execute W4.
- ADJ: execute W3.5.
- USD: execute candidate-neutral reasoning/contrast and invariant tests.
- W5: blocked until W4 and W3.5 resolve.

## Command Center

```bash
make research-check
make health-fast
make health
make docs-check
make plan
make dashboard
```

## Typical Workflow

1. Run `make research-check` and `make health-fast`.
2. Work only on an authorized REP, ADJ, or USD obligation.
3. Preserve countermodels, equivalences, reductions, failures, assumptions, and nonclaims.
4. Do not promote representation progress into universal-structure status.
5. Run full health before merge.

<!-- END GENERATED PROJECT FAR DASHBOARD -->

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

The MVP intentionally defers proof verification, automated reasoning, operation execution, REST APIs, persistent storage, web interfaces, plugin systems, production hardening, and independent external implementation.
