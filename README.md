# Project FAR

[![Release v1.0.0](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/latest)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

## Latest release: v1.0.0

The latest published GitHub repository release is [v1.0.0](https://github.com/notfoundout/Project-FAR/releases/tag/v1.0.0). The executable package metadata currently declares version `0.6.0`. These are separate version surfaces: the release tag records the published repository release, while `pyproject.toml` is authoritative for the installable package version.

## Central result

Project FAR's governing result is `PROJECT-FAR-CORE-THEORY-1.1`:

> **NONTRIVIAL CONTRACT-FREE MINIMAL ARCHITECTURE IS IMPOSSIBLE; CONTRACT-RELATIVE SUFFICIENCY AND A UNIQUE MINIMAL OBSERVATIONAL QUOTIENT ARE PROVED.**

For a fixed exact comparison contract, a representation is sufficient exactly when declared behavior factors through it. The contract induces a unique least-informative observational quotient up to isomorphism. No single representation is simultaneously least-informative sufficient for every observation contract on a nontrivial domain, although the identity representation can be sufficient for all such contracts on fixed `X`.

The v1.1 correction also separates exact common theory from frame-relative residue: `T_{L,J,I}` is indexed by the language, interpretation profiles/models, and target class; the substantive residue `T_{L,J,I} \ Cn_L(Γ)` is additionally indexed by the frame. `Γ` alone does not change exact `T` when the interpreted models are fixed.

Project FAR therefore closes as a **contract and audit discipline**, not as a universal inventory of reasoning primitives. The result is Accepted as internal deductive work corrected after a non-independent hostile audit. It has **not** been independently reviewed.

- [Canonical corrected core theory v1.1](theory/theorems/Project-FAR-Theory-Closure-v1.1.md)
- [Machine-readable v1.1 claim ledger](theory/terminal/project-far-core-theory-v1.1.json)
- [v1.1 correction acceptance](docs/governance/project-far-theory-closure-acceptance-v1.1.md)
- [v1.1 correction audit](docs/audits/project-far-core-theory-v1.1-correction-audit.md)
- [Permanent v1.1 regression fixtures](theory/evaluation/project-far-core-theory-v1.1-regressions.json)
- [Historical v1.0 core theory](theory/theorems/Project-FAR-Theory-Closure-v1.0.md) — preserved byte-for-byte at SHA-256 `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`

The historical UPP proposition remains not refuted, but its frozen derivation is defective and the theorem is not established. Its exact terminal string and artifacts remain preserved as history; they are not current theorem authority.

## Post-closure phase

The active program is `POST-CLOSURE-001`. The canonical next workstream remains `PCA-W1-INDEPENDENT-REVIEW`, now against `PROJECT-FAR-CORE-THEORY-1.1`. The hostile audit that produced the v1.1 repair is explicitly not counted as independent review.

Core theory reopens only for a reproducible contradiction to a stated premise, proof step, theorem, or derivation. Subsequent work includes independent review, proof-assistant formalization, a contract/conformance schema, domain-specific contracts, approximation/cost extensions, and empirical audit-utility studies.

## Scoped FARA formal kernel

`FARA-FORMAL-KERNEL-001` is Accepted for **Project FAR v1.0 finite, explicit, auditable representational architecture**. The canonical formal foundation at that scope is an [identity-bearing many-sorted relational kernel](frameworks/FARA/formal-kernel.md) with typed occurrence-sensitive identity and sort-preserving relational isomorphism as model equivalence.

The decision follows an executable source campaign and a separate clean-room Node.js replication over neutral scenarios. It does not establish global uniqueness, universality, primitive necessity/minimality, completeness, nonfinite/oracle/embodied coverage, or external-investigator independence. The seven named fields remain available as schema roles; no global primitive inventory is claimed.

- [Acceptance record](docs/governance/fara-formal-kernel-acceptance-v1.0.md)
- [Promotion record](docs/governance/fara-formal-kernel-promotion-v1.0.md)
- [Limitation LIM-025](docs/governance/limitations-register.md)

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

## Theory-closure validation

```bash
python tools/check_project_far_theory_closure.py
```

The validator now checks both the immutable historical v1.0 hash and the corrected v1.1 authority/regression chain. The former post-terminal UPP validator remains only to verify that the superseded program and its historical controls are preserved consistently.

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

The MVP does not encode a complete comparison contract, verify factorization, compute the observational quotient, or establish application correspondence. Successor requirements are specified in [Contract-Relative FAR IR v1.1 Requirements](docs/mechanization/contract-relative-far-ir-v1.1-requirements.md).

## Canonical theory navigation

The authoritative dependency order is **foundations → shared theory → FARA → FAR → FARO**. Start with the [canonical map](docs/CANONICAL_MAP.md), [terminology authority](docs/glossary/canonical-terminology.md), [framework boundaries](docs/governance/framework-boundaries.md), [claim-status matrix](docs/governance/claim-status-matrix.md), [limitations](docs/governance/limitations-register.md), and [open problems](docs/governance/open-problems-register.md). Methodology, evidence, examples, papers, software, commercial material, and archive records are downstream; none proves universality or supplies theory prerequisites.

Repository navigation continues through the [documentation index](docs/README.md), [foundations](foundations/README.md), [shared theory](theory/README.md), [frameworks](frameworks/README.md), [methodology](methodology/README.md), and [papers](papers/README.md) entry points.
