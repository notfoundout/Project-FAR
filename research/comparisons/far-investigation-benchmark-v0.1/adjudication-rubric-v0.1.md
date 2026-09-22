# FAR Investigation Benchmark — Blinded Adjudication Rubric v0.1

Status: PREPARED / must be frozen before output scoring

## Unitization

Adjudicators score normalized condition-blinded packets. Each packet is segmented into atomic factual propositions and material inferential steps by a blinded unitizer. Adjudicators may split or merge a unit only by recording a reason. Original text remains immutable.

A material inferential step is a conclusion whose removal or weakening could change the investigation's bottom-line resolution, confidence, causal explanation, or treatment of a material alternative.

## M1 unsupported inference

For every material inference, assign one:

- SUPPORTED: cited evidence plus explicit assumptions warrants the conclusion at the stated strength;
- UNSUPPORTED: evidence/assumptions do not warrant the conclusion at the stated strength;
- NOT-RATABLE: required evidence is inaccessible or the normalized packet is corrupt.

An inference is UNSUPPORTED when any necessary bridge is hidden, contradicted, materially weaker than the conclusion, or dependent on an uncited factual premise.

M1 denominator = SUPPORTED + UNSUPPORTED material inferences.
M1 numerator = UNSUPPORTED material inferences.
NOT-RATABLE units never silently disappear; they trigger the missingness rule.

## M2 evidence coverage

The reference-evidence panel assigns stable IDs to material evidence items before seeing condition outputs.

For each reference item, adjudicators assign:

- RECOVERED-CORRECTLY-CONNECTED;
- RECOVERED-WRONG-CONNECTION;
- NOT-RECOVERED;
- REFERENCE-ITEM-INVALID is **not** an output-scoring option. Reference-item validity is resolved and frozen by the reference-evidence panel before any condition packet is exposed.

M2 denominator is the frozen set of valid reference items for that case and is identical across conditions.
M2 numerator includes only RECOVERED-CORRECTLY-CONNECTED.

A citation to a source does not count if the system fails to connect the material evidence to the proposition for which it matters.

## Critical error classes

Use exactly one primary class per material defect: C1 unsupported factual assertion; C2 citation/evidence mismatch; C3 omitted material counterevidence; C4 hidden assumption; C5 invalid/over-strength inference; C6 interpretation/claim substitution; C7 provenance failure; C8 unresolved contradiction presented as resolved; C9 uncertainty suppression; C10 materially incomplete alternative set; C11 unreplayable evidence/computation; C12 other with mandatory justification.

## Secondary metrics

Contradiction discovery, alternative-hypothesis coverage, assumption explicitness, source-to-claim correspondence, calibrated Unknown use, falsification-condition quality, provenance completeness, and replay completeness are scored only from frozen operational definitions. They cannot alter M1/M2.

## Blinding

Condition names, FAR field names, distinctive headers, filenames, and machine-readable schema labels are removed or mapped to neutral labels. Content is not rewritten merely to conceal stylistic differences. Adjudicators record whether they believe they recognized a condition; guesses are analyzed only as a blinding diagnostic.

## Raters and disagreement

Two raters independently score every packet. They may not see one another's scores. Any M1 unit disagreement or M2 item disagreement goes to a third rater. The third rater receives the packet and disputed unit/item, not the identities or prior votes of the first two raters.

Raw ratings are immutable. Adjudicated ratings are stored separately.

## Missingness

A wholly missing condition output is assigned M1 = 1 and M2 = 0 for that case. If packet corruption or inaccessible evidence prevents valid scoring for any condition, the affected case is non-ratable for that primary metric across all compared conditions; condition-specific deletion is forbidden. If more than 3 of 60 cases are non-ratable for either primary metric, the terminal benchmark status is INDETERMINATE. At 3 or fewer, use complete paired cases for that metric, report the count/reasons, and report the preregistered worst-case sensitivity analysis. NOT-RATABLE units therefore never disappear from a denominator without a case-level integrity disposition.

## Prohibitions

Adjudicators do not score writing quality, ideological agreement, preferred policy, persuasiveness, or whether they personally agree with the conclusion. They score evidence-to-claim and evidence-to-inference relations under this rubric.
