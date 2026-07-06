# Project FAR v0.2.0 Theory Freeze

Status: Provisional v0.2.0 baseline freeze note.

## Purpose

This note freezes the Project FAR v0.2.0 theory and evidence baseline for future comparison. The freeze does not assert finality, irreducibility, or universal coverage. It identifies the v0.2.0 baseline that later work must evaluate against rather than silently overwrite.

## Frozen Primitive Baseline

For v0.2.0, the FAR primitive architecture is frozen as the five-principle baseline used by the release evidence corpus:

```text
P = { Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus }
```

These five primitives define the v0.2.0 baseline for evaluating machine-readable reasoning-system fixtures and candidate counterexamples.

## Frozen Metadata Baseline

The theorem/proposition/lemma/axiom/definition metadata present at v0.2.0 is frozen as the v0.2.0 metadata baseline.

Future metadata changes may extend, correct, or improve the corpus, but they must be evaluated against the v0.2.0 baseline and should identify whether they preserve, revise, or falsify v0.2.0 results.

## Frozen Evidence Corpus

The reasoning-system fixtures present at v0.2.0 are frozen as the baseline evidence corpus for this release. This includes the fixtures classified as `fits FAR`, `extends FAR`, and `candidate counterexample` by the v0.2.0 falsification harness.

The v0.2.0 baseline includes the analyzed candidate counterexamples for paradoxical reasoning, inconsistent calculus, and opaque intuition or oracle reasoning.

## Future Evaluation Requirements

Future changes must be evaluated against this baseline. In particular:

- changes to primitives must state whether they preserve, refine, reduce, extend, or falsify the v0.2.0 primitive baseline;
- changes to theorem, proposition, lemma, axiom, or definition metadata must state whether v0.2.0 metadata results remain valid;
- changes to reasoning-system fixtures or evaluator behavior must state whether v0.2.0 classifications are preserved or revised;
- new hard cases must be compared against the v0.2.0 candidate-counterexample analysis before being promoted as stronger evidence.

## v0.3.0 Boundary

v0.3.0 may extend the evidence corpus, add stronger checks, improve mechanization, and analyze additional hard cases. It should not silently rewrite v0.2.0 results.

If v0.3.0 evidence changes a v0.2.0 conclusion, that change should be recorded as a revision or falsification of the v0.2.0 baseline rather than as an unmarked replacement.
