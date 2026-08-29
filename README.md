# Project FAR

[![Release v1.0.0](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/latest)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a framework for representing, analyzing, and comparing structured, explicit, auditable reasoning under declared contracts.

## Latest release: v1.0.0

The latest published GitHub repository release is [v1.0.0](https://github.com/notfoundout/Project-FAR/releases/tag/v1.0.0). The executable package metadata currently declares a separate installable version. These are separate version surfaces: the GitHub release records the published repository release, while package metadata governs the installable software version.

The current governing theory is `PROJECT-FAR-CORE-THEORY-1.1`.

> **NONTRIVIAL CONTRACT-FREE MINIMAL ARCHITECTURE IS IMPOSSIBLE; CONTRACT-RELATIVE SUFFICIENCY AND A UNIQUE MINIMAL OBSERVATIONAL QUOTIENT ARE PROVED.**

For a fixed exact comparison contract, a representation is sufficient exactly when declared behavior factors through it. The contract induces a unique least-informative observational quotient up to isomorphism. No single representation is simultaneously least-informative sufficient for every observation contract on a nontrivial domain, although identity can be sufficient for all such contracts on fixed `X`.

The v1.1 correction also separates exact common theory from frame-relative residue: `T_{L,J,I}` is indexed by language, interpretation profiles/models, and target class; `T_{L,J,I} \ Cn_L(Γ)` is additionally indexed by frame. `Γ` alone does not change exact `T` when the interpreted models are fixed.

Project FAR therefore closes as a **contract-relative audit discipline**, not as a universal inventory of reasoning primitives.

## Assurance state

The corrected v1.1 theory survived the sealed `PCA-W1-INDEPENDENT-REVIEW` under its exact scopes: 14 `PROVED`, 0 `REFUTED`, 0 `OPEN`, 0 `UNDERDETERMINED`; no theorem correction was required. Novelty and priority were not established.

`PCA-W2-PROOF-ASSISTANT-FORMALIZATION` is complete: all 14 governed claims are `FORMALIZED` under pinned Lean 4.19.0, with zero partial obstructions and zero contradiction/reopen outcomes. FAR-CORE-014 includes the bounded unit-free MLL witness bridge, and exact transitive kernel assumptions are runtime-audited rather than inferred from CI success.

These are separate assurance dimensions. Independent review does not imply novelty; Lean formalization does not imply empirical utility, efficiency, open-domain universality, or product readiness.

Canonical links:

- [Corrected core theory v1.1](theory/theorems/Project-FAR-Theory-Closure-v1.1.md)
- [Machine-readable v1.1 claim ledger](theory/terminal/project-far-core-theory-v1.1.json)
- [v1.1 correction acceptance](docs/governance/project-far-theory-closure-acceptance-v1.1.md)
- [W1 independent-review promotion](docs/governance/pca-w1-independent-review-promotion-v1.0.md)
- [Machine assurance ledger](theory/evaluation/far-core-assurance-v1.0.json)
- [W2 formalization status](docs/governance/pca-w2-formalization-status-v1.0.md)
- [Canonical project status](docs/project-status.md)
- [Roadmap](docs/ROADMAP.md)
- [Historical v1.0 core theory](theory/theorems/Project-FAR-Theory-Closure-v1.0.md), preserved byte-for-byte at SHA-256 `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`

## Post-closure phase

The active program is `POST-CLOSURE-001`.

- `PCA-W0-REPOSITORY-CONFORMITY`: complete.
- `PCA-W1-INDEPENDENT-REVIEW`: complete.
- `PCA-W2-PROOF-ASSISTANT-FORMALIZATION`: complete, 14/14 formalized.
- `PCA-W3-CONTRACT-SCHEMA`: **next**.
- `PCA-W4-DOMAIN-CONTRACTS`: open.
- `PCA-W5-APPROXIMATION-AND-COST`: open.
- `PCA-W6-EMPIRICAL-AUDIT-UTILITY`: open.

Core theory reopens only for a reproducible contradiction to a stated premise, proof step, theorem, or derivation.

## W3 boundary

W3 must implement a versioned successor to `far-ir/1.0`; it must not silently reinterpret the existing interchange format. The successor contract must explicitly represent contract identity/version, source/case domain, required behavior, representation, decoder/factorization or collision evidence, observation contexts, typed outcomes including `Unknown`, observational equivalence/quotient evidence, admitted transformations/equivalences, interpretation profile, target/model class, frame, provenance/freeze metadata, and optional approximation/loss/cost declarations.

The existing Phase 3 `far-ir/1.0` mechanization remains a historical/current MVP for its stated interchange scope. It does not itself encode the complete W3 comparison contract, verify factorization, compute observational quotients, or establish application correspondence.

## Framework roles

The authoritative dependency order is **foundations → shared theory → FARA → FAR → FARO**.

- FARA: formal/schema representation layer; its former seven candidate primitives are schema/contract roles, not globally necessary primitives.
- FAR: contract-relative methodology and audit protocol.
- FARO: downstream execution, comparison, materialized views, audit, and reporting.
- FARE: requirement-driven mathematical support.
- FARM: governance/change coordination.

Construct, Differentiate, and Restrict are workflow verbs. Resolve and Ω are derived. No global primitive count or operator basis is claimed.

## Historical boundaries

The historical UPP proposition remains not refuted, but its frozen derivation is defective and the theorem is not established. Its artifacts are preserved as history and are not current theorem authority.

Historical bounded-program status remains historical only. PR #453 remains a noncanonical Research record at its exact bounded scope. Preserved SWE-agent, REP, ADJ, W3.5, CRE, FARA-kernel, comparative-representation, and external-system records likewise retain only their original scopes. The frozen SWE-agent v2 comparison observed 0/2 resolved runs for v1.0.0 and 0/2 for v1.0.1 on one task; that bounded observation does not establish equivalence, superiority, safety, readiness, or general performance. No finite execution establishes open-domain universality or commercial value.

## Certification and architecture navigation

- [Repository certification governance](docs/governance/repository-certification-standard.md)
- [Repository certification inventory baseline](docs/audits/repository-certification-inventory-audit.md)
- [Semantic certification baseline](docs/audits/semantic-certification-report.md)
- [Canonical vocabulary index](docs/glossary/canonical-vocabulary-index.md)
- [Repository architecture certification](docs/audits/repository-architecture-certification-report.md)
- [Documentation standardization report](docs/audits/documentation-standardization-report.md)
- [Repository domain registry](docs/architecture/repository-domain-registry.md)
- [Repository compliance enforcement report](docs/audits/repository-compliance-enforcement-report.md)
- [Independent repository certification audit](docs/audits/independent-repository-certification-audit.md)
- [Repository certification status](docs/certification/repository-certification-status.md)

## Validation

Theory-closure validation:

```bash
python tools/check_project_far_theory_closure.py
```

W2 formalization alignment:

```bash
python tools/check_far_core_v11_formalization.py
python -m unittest tests.test_far_core_v11_formalization
```

Repository command center:

```bash
make research-check
make health-fast
make health
make docs-check
```

CI/repository consistency is assurance evidence for the encoded artifacts; it is not a substitute for mathematical proof.

## Navigation

Start with [the canonical map](docs/CANONICAL_MAP.md), [project status](docs/project-status.md), [terminology authority](docs/glossary/canonical-terminology.md), [framework boundaries](docs/governance/framework-boundaries.md), [claim-status matrix](docs/governance/claim-status-matrix.md), [theorem/proof register](docs/governance/theorem-proof-status-register.md), [limitations](docs/governance/limitations-register.md), and [open problems](docs/governance/open-problems-register.md).

Repository navigation continues through the [documentation index](docs/README.md), [foundations](foundations/README.md), [shared theory](theory/README.md), [frameworks](frameworks/README.md), [methodology](methodology/README.md), and [papers](papers/README.md).
