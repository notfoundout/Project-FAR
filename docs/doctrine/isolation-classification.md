# Isolation Classification Doctrine

Status: Accepted Methodology

## Purpose

Evaluator independence matters because validation evidence is stronger when the evaluator's conclusions are not shaped by the repository reasoning that the evaluation is meant to test. Isolation classification records how much confidence Project FAR can place in the independence of the validation process.

Isolation classification measures confidence in evaluator independence only. It does not measure mathematical correctness, proof validity, semantic adequacy, acceptance status, or the truth of any Project FAR artifact.

## Isolation Class I0 — No Isolation

Definition: the evaluator works in the same working context as the repository artifact under review.

Repository reasoning may influence conclusions because the evaluator may inspect, recall, or rely on repository arguments while forming the evaluation. I0 work is suitable for exploratory work only. It is not independent validation.

## Isolation Class I1 — Claimed Isolation

Definition: the evaluator works in a separate evaluation context and receives only explicitly supplied inputs.

Repository access is prohibited by instruction. The execution environment cannot independently verify that such access was technically impossible.

I1 is the current Project FAR validation standard. Evidence produced under I1 constitutes independent research evidence while acknowledging the limitations of the environment.

## Isolation Class I2 — Verified Isolation

Definition: the execution environment technically prevents repository access beyond explicitly supplied inputs.

Examples include:

- sandboxed evaluation;
- audited environments;
- reproducible isolated execution;
- restricted repositories.

Evidence produced under I2 constitutes verified independent validation.

## Isolation Class I3 — External Independent Validation

Definition: independent researchers or external evaluation systems reproduce the result without relying upon Project FAR repository reasoning.

Project FAR does not control the evaluation. I3 is the highest available level of evaluator independence.

## Interpretation

Isolation classification does not measure correctness.

A mathematically correct proof may originate from any isolation class. A highly isolated evaluation may still be incorrect.

Isolation classification supplements logical evaluation. It never replaces logical evaluation.

## Evidence Priority

When multiple evaluations exist for one artifact, prefer the highest successfully completed isolation class.

Lower isolation classes remain valid research evidence. They do not supersede stronger independently obtained evidence.

## Required Reporting

Every future validation report must include an `Isolation Classification` section.

That section must include:

- Isolation Class;
- Evaluation method;
- Technical limitations;
- Whether repository access was prohibited by instruction or prevented technically.

Canonical example:

```markdown
## Isolation Classification

- Isolation Class: I1 — Claimed Isolation.
- Evaluation method: blind evaluator in a separate evaluation context using only explicitly supplied artifact text and accepted prior inputs.
- Technical limitations: the execution environment records the separate context but does not independently prove that repository access was technically impossible.
- Repository access: prohibited by instruction; not technically prevented by the environment.
```

Future validations should adopt this doctrine beginning with L-002. Previous validation reports must not be rewritten or retroactively relabeled solely to apply this doctrine.

## Future Development

Project FAR should continually seek higher isolation classes whenever practical.

Improving isolation strengthens validation methodology without changing Project FAR mathematics.
