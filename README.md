# Project FAR

[![Release](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/tag/v0.4.0)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

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

The generated dashboard below remains the canonical status surface for the older bounded REP/ADJ/W3.5 program and must not be read as overriding the later UPP terminal adjudication.

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Repository Status

- Current project phase: W3.5 machinery/cost, claim-impact, and preserved-failure closure
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- W5 status: blocked by incomplete `W3.5-SDG-001`

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

## Top Priority Tasks

### STRATEGIC-004: Complete W3.5 closure

- Complete cross-package machinery/cost, claim-impact, and preserved-failure artifacts without promoting registered-scope results to universal claims.

### STRATEGIC-005: Assemble W5

- Remains blocked until every required W3.5 artifact is complete and the gate is evidence-backed resolved.

## Current Roadmap

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