# Project FAR Status

The root [README Command Center](../README.md) is the canonical entry point for current repository status and generated planning reports.

- [`docs/maintenance/repository-health-checks.md`](maintenance/repository-health-checks.md) — Repository health-check commands and failure remediation.

## Current Status

Project FAR has completed the v0.4.0 external-validation milestone. The current baseline includes the v0.3.0 internal-validation milestone, the v0.3.1 repository-maturity maintenance release, preliminary external validation EV-001 through EV-029, frozen CRP v1.0 methodology, and a merged deterministic CRE-001 result.

The v0.4.0 release does not change FAR primitives, definitions, axioms, theorem statements, proof objects, parser behavior, reasoning-engine behavior, metadata schemas, or accepted doctrine.

| Framework | Role | Status |
|---|---|---|
| FARA | Representation | Stable |
| FAR | Methodology | Stable |
| FARO | Operations | Stable |
| FARE | Mathematics | Frozen, requirement-driven |
| FARM | Meta-framework coordination | Stable |

Active development now moves toward independent formal vocabulary semantics and the design of CRE-002. The merged deterministic CRE-001 result established, at CRE-001 scope only, vocabulary-native compilation, executable lowering, deterministic verification against the registered reference behavior, replayable lowering traces, mutation testing, adversarial compiler audit, and repository integration. T-001 and T-002 are conditionally established only at their recorded scope and assurance level; VI-002 and VI-003 remain active broader research investigations. Universal sufficiency, primitive-only sufficiency, necessity, minimality, independence, global primitive minimality, global primitive independence, superiority, a FAR proof, universal reasoning structure, and formally licensed vocabulary semantics are not established.

---

## Latest Release

### Project FAR v0.4.0 — External Validation and Comparative Methodology

Status: Current release baseline.

Release document: [`releases/project-far-v0.4.0.md`](releases/project-far-v0.4.0.md)

Prior maintenance release: [`releases/project-far-v0.3.1.md`](releases/project-far-v0.3.1.md)

Prior internal-validation release: [`releases/project-far-v0.3.0.md`](releases/project-far-v0.3.0.md)

---

## Completed Milestones

### Project FAR v0.4.0 External Validation and Comparative Methodology

Status: Complete.

v0.4.0 completes the historical external-validation milestone and additionally registers frozen CRP v1.0 plus the original CRE-001 preparation artifacts; the current repository baseline now also includes the later merged deterministic CRE-001 implementation result.

---

### Project FAR v0.3.1 Repository Maturity and Automation

Status: Complete after release publication.

v0.3.1 packages repository maturity work around the v0.3.0 baseline: README command center, dashboard generation, repository index, dashboard metrics, improved health diagnostics, GitHub Actions, release-readiness reporting, and repository automation documentation.

---

### Project FAR v0.3.0 Internal Validation

Status: Complete.

v0.3.0 evaluates primitive sufficiency across the internal corpus, expanded reasoning-system fixtures, and adversarial test suite. Current repository-grounded analysis finds no analyzed case requiring a sixth primitive, while keeping the conclusion provisional and subject to future falsification.

---

### Project FAR v0.2.0 Evidence Framework

Status: Complete.

v0.2.0 introduced the evidence-bearing infrastructure: machine-readable theory, structured proof objects, proof-step semantics, reasoning-engine traces, falsification harness, counterexample fixtures, and hard-case derived concepts.

---

### FARA — Representation

Status: Stable architecture layer.

FARA provides the representational architecture used by the rest of Project FAR. No separate FARA milestone file is currently present.

---

### FARE Mathematics v0.1

Status: Frozen.

FARE Mathematics v0.1 is requirement-driven. It shall not expand unless FAR, FARO, FARA, or FARM requires mathematical support.

Milestone: [`milestones/FAR-MILESTONE-001-FARE-v0.1-Frozen.md`](milestones/FAR-MILESTONE-001-FARE-v0.1-Frozen.md)

---

### FAR v1.0 Stable

Status: Stable.

Milestone: [`milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md`](milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md)

---

### FARO v1.0 Stable

Status: Stable.

Milestone: [`milestones/FAR-MILESTONE-004-FARO-v1.0-Stable.md`](milestones/FAR-MILESTONE-004-FARO-v1.0-Stable.md)

---

### FARM v1.0 Stable

Status: Stable.

Milestone: [`milestones/FARM-v1.0-Stable.md`](milestones/FARM-v1.0-Stable.md)

Stable components:

- FARM architecture;
- FARM dependency graph;
- FARM design principles;
- FARM requirement routing;
- FARM defect classification;
- FARM change control;
- FARM integration record;
- FARM v1.0 criteria;
- FARM Phase 1 through Phase 4 audit records.

---

## Active Focus

### Post-CRE-001 Deterministic Reconciliation

The active target is freezing independent formal semantics for each official vocabulary, then designing and preregistering CRE-002 as a prospective study. CRE-001's deterministic implementation is complete at its stated scope: the official vocabularies were compiled into vocabulary-native artifacts, lowered to executable models, deterministically verified against the registered reference behavior, replayed through lowering traces, mutation-tested, adversarially audited, and integrated into the repository. This does not establish universal sufficiency, primitive-only sufficiency, necessity, minimality, independence, superiority, a FAR proof, universal reasoning structure, or formally licensed vocabulary semantics.

---

## Development Order

The current project order is:

1. FARA stable representational architecture recognized.
2. FAR / FARO / FARM stable layers maintained.
3. v0.3.0 internal validation baseline preserved.
4. v0.3.1 repository maturity baseline published.
5. v0.4.0 external validation completes and preserves EV-001 through EV-029 as preliminary evidence.
6. CRP v1.0 is frozen and CRE-001 was registered.
7. Deterministic CRE-001 implementation is merged for the registered CRE-001 scope, with vocabulary-native compilation, executable lowering, deterministic verification, replayable traces, mutation testing, adversarial compiler audit, and repository integration.

---

## Canonical Maturity Dimensions

This lowercase path, `docs/project-status.md`, is the canonical case-stable project-level status document. Generated status summaries, release-readiness reports, framework README files, milestone records, theorem catalogs, validation investigations, and open-question lists remain subordinate or domain-specific status sources.

| Dimension | Current maturity | Notes |
|---|---|---|
| Repository maturity | Mature for documentation, governance, repository-health automation, preliminary external-system evaluation records, and comparative-study preparation. | This does not imply research completion. |
| Framework maturity | FARA, FAR, FARO, and FARM are stable framework layers; FARE Mathematics v0.1 is frozen and requirement-driven. | Framework stability does not imply universality or comparative superiority. |
| Implementation maturity | Prototype/mechanization support is limited to IR loading, validation, graph construction, trace inspection, selected transition summaries, and structural proof-object validation. | General semantic inference and general calculus execution remain unsupported. |
| Proof-assurance maturity | Canonical theorem records are established only at their stated scope and assurance level. Current proof objects are structurally checked, not machine-verified formal proofs. | Assurance metadata is authoritative in `theory/metadata/theorems.yaml`. |
| Empirical-validation maturity | EV-001 through EV-029 are preliminary external-system evaluations, not independent validation. CRE-001 deterministic comparison is complete at registered CRE-001 scope, but formally licensed vocabulary semantics and prospective independent replication are not established. | Independent validation requires isolated prospective execution under a preregistered protocol. |
| Release maturity | v0.4.0 is the current release baseline. | Release maturity does not strengthen theorem or validation claims. |

## Preserved Unique Notes from Prior Status File

- Status and maturity labels in this document describe project maturity only. They do not assign Charter artifact status.
- Current research remains focused on preserving preliminary v0.4.0 external-system evaluation evidence, maintaining the merged deterministic CRE-001 result at its limited scope, freezing independent formal vocabulary semantics, and preparing CRE-002 prospectively.
- Central research questions remain open: common reasoning structure, universality, primitive and assumption necessity, architectural and semantic minimality, counterexample construction, boundary identification, competing simpler structures, expressive power, alternative formulations, and unresolved uncertainty.
- Current priorities are freezing independent formal semantics for each official vocabulary, designing and preregistering CRE-002, executing CRE-002 prospectively, analyzing prospective evidence, and pursuing independent replication while keeping certification, compatibility mapping, deterministic comparison, prospective comparative evaluation, and independent external review distinct.
