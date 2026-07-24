# Project FAR Terminology Status

Date: 2026-07-23
Status: canonical convergence guidance

## Stable framework vocabulary

| Name | Full name | Canonical role | Current status | Product relationship |
|---|---|---|---|---|
| FAR | Foundational Analysis of Reasoning | Investigation methodology | Stable v1.0; requirement-driven changes only | Defines how external-validation investigations are conducted and closed |
| FARA | Foundational Architecture of Reasoning Analysis | Representational architecture | Stable; requirement-driven changes only | Supplies the objects and relations product artifacts compile into or reference |
| FARE | Formal Architecture of Reasoning Evaluation | Mathematical and formal evaluation support | Frozen v0.1; expand only for reviewed requirements | Supplies formal evaluation machinery when product requirements demand it |
| FARM | Foundational Analysis of Reasoning Meta-framework | Cross-framework coordination and change control | Stable v1.0 | Routes validated product defects to the correct framework without duplication |
| FARO | Operational layer | Operational procedures and execution | Active framework role | Owns operationalization of investigations and runtime procedures |

## Product vocabulary

| Name | Role | Status |
|---|---|---|
| FAR Verification Core | Reusable representation, validation, comparison, provenance, and evidence machinery | Strategic umbrella; maps to existing mechanization and commercial packages |
| FAR Release Assurance | Baseline-versus-candidate package comparison and release gating | Implemented on diverged research branch; requires clean integration into `main` |
| FAR Decision Integrity | Explicit decision packages, adjudication, regression, trace ingestion, instrumentation, reports, storage, and service layers | Implemented on diverged research branch; requires clean integration into `main` |
| FAR Evidence Engine | Commercial product concept for continuous evidence reconstruction | Product umbrella, not a replacement framework vocabulary |
| External Validation | Real-artifact correspondence testing | Immediate execution priority |

## Rules

1. Framework terms and product terms are not synonyms.
2. Product code must not silently redefine FAR, FARA, FARE, FARM, or FARO.
3. Product-discovered deficiencies may trigger framework changes only through explicit evidence and FARM coordination.
4. New application entities should live in application contracts unless a real case proves they belong in foundational `far-ir/1.0`.
5. Historical names should be archived only if a separate reviewed decision proves that their canonical responsibility has been transferred.

## Immediate mapping

- Candidate selection, preregistration, and investigation closure: FAR.
- Trace/event representation and claim/evidence structures: FARA plus mechanization contracts.
- Deterministic assessment and preservation rules: FARE where formal support is required; otherwise application-level adjudication.
- Operational acquisition, hashing, adapter execution, and reports: FARO/application runtime.
- Cross-layer defect routing: FARM.

No framework requires speculative modification before Candidate 001 is run. The external trace should expose concrete deficiencies first.
