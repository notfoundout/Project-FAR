# CRE-001: Reflective Discrete Rule-Transition System

Status: Registered; deterministic implementation complete at CRE-001 scope
Protocol: CRP-1.0
Scenario: CRE-001-SCENARIO-1.0
Vocabulary package: CRE-001-VOCABULARIES-1.0
Instructions: CRE-001-INSTRUCTIONS-1.0

## Experiment Purpose

CRE-001 records the first Comparative Representation Protocol v1.0 experiment package and the later merged deterministic implementation. The deterministic result tested how registered vocabularies can be compiled into vocabulary-native artifacts and lowered to executable models that match the registered reflective discrete rule-transition reference under explicit ambiguity policies.

## Scope

The experiment scope is limited to systems characterized by discrete states, explicit propositions, explicit rules, explicit transitions, self-modification, historical dependency preservation, and explicit termination conditions.

## Frozen Inputs

- Scenario package: `scenario/scenario-v1.0.md` and `scenario/scenario-v1.0.json`.
- Vocabulary packages: `vocabularies/vocabulary-A.md`, `vocabularies/vocabulary-B.md`, and `vocabularies/vocabulary-C.md`.
- Calibration package: `calibration/calibration-exercise-v1.0.md`.
- Evaluator instructions: `evaluator-instructions/evaluator-instructions-v1.0.md`.
- Submission templates: `submissions/mapping-submission-template.json` and `submissions/cir-submission-template.json`.
- Adjudication package: files under `adjudication/`.
- Provenance template: `provenance/provenance-record.template.json`.
- Pre-exposure checklist: `execution-checklist.md`.
- Package manifest: `package-manifest.json`.

## Historical Human-Comparison Execution Order

1. Verify protocol lock and package hashes.
2. Confirm evaluator eligibility and isolation.
3. Administer unrelated calibration; exclude only preregistered procedural failures.
4. Randomize evaluator assignments so each evaluator receives exactly one vocabulary.
5. Deliver the frozen scenario, assigned vocabulary package, evaluator instructions, and submission templates.
6. Collect mapping and CIR submissions.
7. Canonicalize and adjudicate according to CRP v1.0.
8. Perform ablation, aggregation, Pareto comparison, and decision-rule evaluation only after submissions exist.

## Required Artifacts

A completed execution requires eligibility records, calibration pass records, assignment records, provenance records, primary mapping submissions, CIR submissions, adjudication records, ablation submissions, aggregation worksheets, and an experiment summary.

## Deterministic Outputs

The merged deterministic implementation provides vocabulary-native compilation artifacts, executable lowerings, deterministic verifier reports, replayable lowering traces, mutation-test reports, an adversarial compiler audit, and repository integration for CRE-001. Historical human-comparison outputs such as evaluator mapping submissions, CIR records, adjudication records, and Pareto worksheets remain absent unless separately produced by a historical human-comparison experiment.

## Supported Deterministic Conclusions

CRE-001 establishes deterministic implementation at registered CRE-001 scope: vocabulary-native compilation, executable lowering, deterministic verification against the registered reference behavior, replayable lowering traces, mutation testing, adversarial compiler audit, and repository integration.

## Unsupported Conclusions

CRE-001 does not establish universal sufficiency, primitive-only sufficiency, necessity, minimality, independence, superiority, a FAR proof, universal reasoning structure, or formally licensed vocabulary semantics. Historical human-comparison conclusions also remain absent unless a separate human-comparison execution is performed and recorded.
