# FAR Investigation Benchmark — Blinded Adjudication Rubric v0.1

Status: PREPARED / must be frozen before output scoring

## Unitization

Adjudicators score normalized condition-blinded packets. Each packet is segmented into atomic factual propositions and material inferential steps by a blinded unitizer. Adjudicators may split or merge a unit only by recording a reason. Original text remains immutable.

A material inferential step is a conclusion whose removal or weakening could change the investigation's bottom-line resolution, confidence, causal explanation, or treatment of a material alternative.

A non-missing condition packet must yield at least one ratable material inferential step. If the blinded unitizer and raters cannot identify any ratable material inference, treat the case-condition packet as a scoring failure under the case-level missingness rule; do not define M1 as zero and do not divide by zero.

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

The reference-evidence panel assigns stable IDs to valid material evidence items and freezes the denominator before any condition execution.

For each frozen reference item, adjudicators assign:

- RECOVERED-CORRECTLY-CONNECTED;
- RECOVERED-WRONG-CONNECTION;
- NOT-RECOVERED.

`REFERENCE-ITEM-INVALID` is not an output-scoring option. Reference-item validity is resolved by the reference panel before S1.

M2 denominator is the frozen positive set of valid reference items for that case and is identical across conditions.  
M2 numerator includes only RECOVERED-CORRECTLY-CONNECTED.

An item is RECOVERED-CORRECTLY-CONNECTED only when the condition identifies the same substantive evidence represented by the frozen item and visibly connects it to the proposition, inference, material alternative, or uncertainty boundary for which the item was frozen as material. Exact wording is unnecessary; proposition-level correspondence is required. A citation to the source elsewhere in the packet, an unsupported paraphrase, or a link to a different proposition is RECOVERED-WRONG-CONNECTION or NOT-RECOVERED as applicable.

## Critical error classes

Use exactly one primary class per material defect: C1 unsupported factual assertion; C2 citation/evidence mismatch; C3 omitted material counterevidence; C4 hidden assumption; C5 invalid/over-strength inference; C6 interpretation/claim substitution; C7 provenance failure; C8 unresolved contradiction presented as resolved; C9 uncertainty suppression; C10 materially incomplete alternative set; C11 unreplayable evidence/computation; C12 other with mandatory justification.

## Secondary metrics

Contradiction discovery, alternative-hypothesis coverage, assumption explicitness, source-to-claim correspondence, calibrated Unknown use, falsification-condition quality, provenance completeness, and replay completeness are scored only from frozen operational definitions. They cannot alter M1/M2.

## Blinding

Condition names, FAR field names, distinctive headers, filenames, and machine-readable schema labels are removed or mapped to neutral labels. Content is not rewritten merely to conceal stylistic differences. Adjudicators record whether they believe they recognized a condition; guesses are analyzed only as a blinding diagnostic.

## Raters and disagreement

Two primary raters independently score every packet. They may not see one another's scores. Any M1 unit disagreement or M2 item disagreement goes to a third adjudicator. The third adjudicator receives the blinded packet and disputed unit/item, not the identities or prior votes of the first two raters.

The three evaluator records in the frozen campaign manifest must use distinct IDs and declare identity, provider/model when applicable, prior FAR exposure, conflicts, and lane. Raw ratings are immutable. Adjudicated ratings are stored separately.

## Missingness

A wholly missing condition output is assigned M1 = 1 and M2 = 0 for that case. A non-missing packet with no ratable material M1 unit is treated as a packet-level scoring failure, not as zero unsupported inference.

If packet corruption, inaccessible evidence, or a scoring failure prevents valid scoring for any condition, the affected case is non-ratable for that primary metric across all compared conditions; condition-specific deletion is forbidden. If more than 3 of 60 cases are non-ratable for either primary metric, the terminal benchmark status is INDETERMINATE. At 3 or fewer, use complete paired cases for that metric and run the frozen best/worst-case sensitivity analysis defined in `analysis-parameters-v0.1.json`.

The confirmatory SURVIVES disposition additionally requires the preregistered worst-case sensitivity result not to reverse either primary gate. If it does, the benchmark is INDETERMINATE rather than promoted from the complete-case analysis alone.

## Prohibitions

Adjudicators do not score writing quality, ideological agreement, preferred policy, persuasiveness, or whether they personally agree with the conclusion. They score evidence-to-claim and evidence-to-inference relations under this rubric.
