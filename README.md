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

These results do not establish complete `Faithful_split`, rejection of every invalid representation, a representation theorem, universal structure, necessity, or minimality.

`RCS-CORPUS-001` freezes 8 positive, 8 contrast, and 2 disputed candidate-independent formal instances with declared candidate-registry exposure. Bounded GREL-FARA factorization establishes equivalent expressiveness, bidirectional translation, stricter FARA constraints, no factorization-level reasoning-specificity result, and a cost tradeoff. A project-authored seven-criterion discriminator classifies all 8 positives as reasoning-like, all 8 contrasts as nonreasoning-like, and preserves both disputed cases as borderline. Because the same criterion inputs exist in the candidate-neutral source and survive exact GREL recovery, unique FARA discriminative capacity is refuted at this registered scope. Candidate ablation and reconstruction are not complete: the current artifact preserves preliminary internal observations but 0 of the required 648 atomic candidate × case × representation trials. Structural commitment necessity remains unresolved for all 12 registered candidates. `W3.5-SDG-001` remains the sole live blocker before W5.

Run `make research-check` to validate the frozen REP program, representation-discovery separation, W3.5 gates, corpus freeze, factorization, registered discrimination, qualified specificity result, candidate evidence boundary, universal target, and conservative claim boundaries.

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Repository Status

- Current project phase: W3.5 candidate evidence-complete re-execution
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- W5 status: blocked by incomplete `W3.5-SDG-001`

## Track Status

| Track | Status | Current boundary |
|---|---|---|
| REP | W0-W4 complete | Bounded construction and registered controls; theorem unproved |
| ADJ | Corpus, factorization, discrimination, and specificity complete; candidate execution incomplete | 8 positive, 8 contrast, 2 disputed; 0/648 candidate trials preserved |
| USD | Target frozen | Structural indispensability unresolved for all 12 candidates |
| W5 | Blocked | Requires complete evidence-backed `W3.5-SDG-001` |

## Registered ADJ Results

- Factorization interpretation: `fara_constrained_equivalent`.
- Reasoning discrimination: 8/8 positives reasoning-like; 8/8 contrasts nonreasoning-like; 2/2 disputed borderline.
- FARA-specificity classification: `fara_role_directness_without_unique_discriminative_capacity`.
- Candidate result: `candidate_structural_indispensability_unresolved_reexecution_required`.
- Structural necessity: unresolved 12; supported 0; refuted 0; partial 0.
- Candidate evidence: preliminary internal adjudication; atomic ablation/reconstruction evidence missing.

## Top Priority Tasks

### STRATEGIC-003: Execute candidate ablation and reconstruction

- Preserve all 648 candidate × case × representation trials with explicit ablation, reconstruction, equivalence, equivalent-reintroduction, and machinery-cost records.

### STRATEGIC-004: Complete W3.5 closure

- Complete cost, claim-impact, and preserved-failure artifacts only after candidate execution is evidence-complete.

## Current Roadmap

- REP: W0-W4 complete at bounded `S_core` scope.
- ADJ: execute evidence-complete candidate testing; do not promote preliminary observations.
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
