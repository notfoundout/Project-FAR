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

The project separates three tracks:

- **REP:** finite representation capacity and fidelity;
- **ADJ:** generic-baseline factorization, FARA-specificity, contrast, ablation, reconstruction, and cost;
- **USD:** representation-independent universal-structure discovery.

`SCORE-W0-PROOF-001` through `SCORE-W4-PROOF-001` are project-authored bounded REP packages. W3 establishes all 24 finite construction lemmas, target-only recovery, semantic agreement, coherence, machinery accounting, uniformity, composition, and witness assembly. W4 establishes that every applicable registered NC-01 through NC-10 family violates at least one frozen faithful-representation clause for its registered reason.

These results do not establish complete `Faithful_split`, rejection of every invalid representation, FARA-specificity, a representation theorem, universal structure, necessity, or minimality.

`RCS-CORPUS-001` freezes 8 positive, 8 contrast, and 2 disputed candidate-independent formal instances with declared candidate-registry exposure. `W35-GREL-FARA-FACTOR-001` establishes bounded operational factorization: equivalent expressiveness, bidirectional translation, stricter FARA constraints, no established reasoning specificity, a cost tradeoff, and the interpretation `fara_constrained_equivalent`. The translation explicitly reuses the declared FARA-oriented adapter and accepted constructor, so this is not a primitive reduction. Candidate scoring and reasoning/contrast discrimination have not begun. `W3.5-SDG-001` remains the sole live blocker before W5.

Run `make research-check` to validate the frozen REP program, representation-discovery separation, W3.5 gates, universal target, corpus freeze, factorization result, and conservative claim boundaries.

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Repository Status

- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)
- Current project phase: W3.5 specificity, discrimination, candidate testing, reconstruction, and cost closure
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- Planner status: CURRENT ([planner](tools/self_advancement_plan.py))

## Track Status

| Track | Status | Current boundary |
|---|---|---|
| REP | W0-W4 complete | Bounded construction and registered controls; theorem unproved |
| ADJ | W3.5 in progress; corpus and factorization complete | 8 positive, 8 contrast, 2 disputed; specificity and execution pending |
| USD | Target frozen, unexecuted | No universal-structure candidate classified |
| W5 | Blocked | Requires complete evidence-backed `W3.5-SDG-001` |

No aggregate completion percentage is authorized across REP, ADJ, and USD.

## Factorization Result

- Expressiveness: `equivalent`.
- Translation: `bidirectional`.
- Constraint strength: `fara_stricter`.
- Reasoning specificity: `not_established`.
- Cost relation: `tradeoff`.
- Overall interpretation: `fara_constrained_equivalent`.
- Boundary: operational factorization only; the translation reuses the declared FARA-oriented adapter and accepted constructor, so no primitive reduction is claimed.

## Top Priority Tasks

### STRATEGIC-002: Execute reasoning/contrast discrimination and FARA specificity

- Test whether FARA constraints have a distinct reasoning-relevant role over the frozen corpus.

### STRATEGIC-003: Execute candidate ablation and reconstruction

- Test every candidate across the frozen corpus and alternative conceptual bases, counting equivalent reintroduction.

### STRATEGIC-004: Complete W3.5 cost and claim-impact audit

- Produce complete machinery accounting, preserved failures, and track-specific claim effects.

### STRATEGIC-005: Assemble W5

- Blocked until W3.5 resolves with complete immutable evidence.

## Universal-Structure Discovery

- Target: [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)
- Generic baseline: [GREL-001](docs/research/generic-relational-baseline-v1.0.md)
- Frozen concrete corpus: [RCS-CORPUS-001](docs/research/w3-5-concrete-corpus-freeze-v1.0.md)
- Factorization result: [W35-FACTOR-RESULT-001](docs/research/w3-5-grel-fara-factorization-v1.0.md)
- Candidate registry: [US-CANDIDATES-001](theory/evaluation/universal-structure-candidate-registry.json)
- Current candidate result: unresolved

## Repository Navigation

- [Project Status](docs/reports/project-status-generated.md)
- [Next Actions](docs/planning/next-actions.md)
- [GREL–FARA Factorization](docs/research/w3-5-grel-fara-factorization-v1.0.md)
- [W3.5 Gate](docs/research/w3-5-specificity-and-discovery-gate-v1.0.md)
- [Central Claim Registry](theory/evaluation/central-claim-registry.json)
- [Research Gates](theory/evaluation/research-gates.json)

## Current Roadmap

- REP: W0-W4 complete at bounded `S_core` scope.
- ADJ: corpus and factorization complete; execute specificity, discrimination, candidate testing, reconstruction, full cost, and claim impact.
- USD: keep every candidate unresolved until candidate-neutral execution.
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
