# S_core W4 Formal Negative-Control Proof v1.0

## Status

Project-authored human-checkable proof package for `OBS-SC-010` and the frozen `NC-01` through `NC-10` families.

Proof identifier: `SCORE-W4-PROOF-001`.

This artifact is internal mathematical work. It has not been checked by a proof assistant or independently reviewed. The accompanying executable suite is bounded corroboration of canonical representatives, not a proof of the quantified family result.

## Governing artifacts

This proof is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/s-core-construction-obstruction-ledger-v1.0.md`;
- `docs/research/s-core-w3-global-witness-proof-v1.0.md`;
- `docs/methodology/negative-control-suite-v1.0.md`;
- `theory/evaluation/s-core-w4-negative-control-fixtures.json`.

No source scope, target interface, preservation predicate, recovery rule, machinery rule, or negative-control definition is changed.

## 1. Statement proved

Let \(S\in S_{core}\) be an admitted finite source contract, and let \(W\) be a candidate witness evaluated under frozen `FAITHFUL-REP-001`.

For each control family \(NC_j\), let its protected distinction be applicable when that distinction is material and nonempty in \(S\). Then:

\[
NC_j(S,W)\Longrightarrow \neg Faithful_{split}(S,W)
\]

for at least one frozen conjunct named in the registered negative-control mapping.

If a protected distinction is empty or inapplicable in the source contract, that control instance is `not_applicable`; it is not counted as a successful rejection. This prevents an empty-axis case from being treated as evidence of constraint.

The theorem is limited to the ten registered families and their frozen structural definitions. It does not quantify over every possible invalid representation.

## 2. Proof method

`Faithful_split` is a conjunction including applicable preservation and reflection, target-only admissible recovery, semantic agreement, cross-axis coherence, uniformity, compositional accountability, complete machinery accounting, and `Nontrivial`.

Each negative-control family was frozen before this execution and is defined by removing, collapsing, hiding, substituting, or relocating a protected distinction. The proof for a family identifies a frozen conjunct that the defining operation makes false. The conclusion follows by conjunction elimination: if one required conjunct is false, `Faithful_split` is false.

This is not the invalid argument that a control fails because it was named a negative control. The failure follows from an independently frozen operation and an independently frozen representation clause.

## 3. Family proofs

### NC-01 — Lookup-table substitution

The control preserves selected outputs while omitting transition structure, dependencies, or historical commitments.

For every applicable source with a material transition, dependency, or history record, the target cannot both omit that record and preserve and reflect it. At least one of `P4`, `P5`, or `P7` is therefore false.

Expected diagnostic: `process_and_commitment_structure_lost`.

### NC-02 — Dependency collapse

The control maps two source-distinct premises, rules, authorities, causal dependencies, support roles, or defeat roles to one undifferentiated relation.

Where the source declares the distinction material, relation reflection requires the distinct source relations to have distinct typed target correspondences. Collapsing them either destroys injectivity or causes one reflected relation to assert the wrong source role. `P4_relation_reflection` is false.

Expected diagnostic: `distinct_dependency_roles_collapsed`.

### NC-03 — History erasure

The control retains a final state but removes a material order, revision, rule modification, ancestry, or path condition.

For every applicable source with a nonempty protected history distinction, `P7` requires preservation and reflection of that distinction. The erased relation is absent from the recovered target contract, so `P7_order_or_revision_reflection` is false.

Expected diagnostic: `material_history_or_revision_erased`.

### NC-04 — Hidden rule modification

The control changes operational rule behavior in compiler behavior, runtime code, or an external override while leaving the declared target and machinery ledger unchanged.

The changed behavior is not determined by the completed target, fixed recovery descriptor, and declared finite machinery graph. It therefore violates target-only `AdmissibleRecovery` or `LedgerComplete`. Adding the override to the ledger would stop it from being hidden and would charge its machinery; it would not make the negative control pass for free.

Expected diagnostic: `undeclared_operational_machinery`.

### NC-05 — Label-only semantics

The control uses a vocabulary label as a substitute for the source-owned denotation or operational distinction.

`FAITHFUL-REP-001` states that lexical labels are insufficient and that semantic agreement is evaluated against declared source denotations and equivalences. A label-only record therefore violates `SemAgree` or lexical invariance.

Expected diagnostic: `semantic_claim_reduced_to_label`.

### NC-06 — Unrestricted interpreter

The control supplies an unrestricted external interpreter to reconstruct missing behavior without counting it as machinery.

A recovery result that depends on this interpreter is not produced solely by the admitted target, fixed descriptor, and declared ledger. `AdmissibleRecovery`, `Uniform`, or `LedgerComplete` is false. If the interpreter is fully declared and costed, it is no longer an uncharged control and must be assessed as part of the candidate machinery.

Expected diagnostic: `unrestricted_external_interpreter`.

### NC-07 — Hidden auxiliary state

The control removes a protected distinction from the declared witness and stores it elsewhere.

The recovered target either lacks the distinction, violating the applicable preservation/reflection clause, or relies on the hidden store, violating image accountability and `LedgerComplete`. Relocation cannot preserve the distinction while remaining uncounted.

Expected diagnostic: `protected_information_relocated_outside_witness`.

### NC-08 — Provenance deletion

The control preserves a conclusion while deleting material source, justification, revision, adjudication, or evidential provenance.

Where the source marks provenance material, the corresponding `P4`, `P7`, or `Pres_8I` reduct contains a relation or attribute that the target no longer reflects. At least one applicable conjunct is false.

Expected diagnostic: `material_provenance_deleted`.

### NC-09 — Output-equivalent process substitution

The control replaces the registered process with a materially different process that produces the same selected outputs.

`FAITHFUL-REP-001` does not define equivalence by output equality. Applicable `P5` bisimulation, `P7` path/history preservation, and dependency/consequence relations in `P4` and `P6` remain theorem obligations. A materially different process therefore fails at least one of those obligations even when terminal outputs match.

Expected diagnostic: `output_equivalence_without_process_equivalence`.

### NC-10 — Primitive smuggling

The control removes a tested function from its declared location and relocates the same work into metadata, derived machinery, compiler assumptions, verifier behavior, or hidden code.

The function remains a dependency of construction, interpretation, recovery, or verification. Omitting that dependency from the machinery graph violates `LedgerComplete`; recording it makes the reintroduction explicit and chargeable. This result detects smuggling but does not prove that any FARA primitive is globally necessary.

Expected diagnostic: `function_relocated_into_unaccounted_metadata`.

## 4. OBS-SC-010 result

The ten proofs establish:

\[
\forall j\in\{1,\ldots,10\},\quad
Applicable(NC_j,S)\land NC_j(S,W)
\Rightarrow \neg Faithful_{split}(S,W).
\]

Therefore `OBS-SC-010` is established for the registered finite `S_core` negative-control families.

The global `Nontrivial` conjunct is supported at exactly this registered scope: the frozen witness relation rejects all ten frozen invalid-family constructions for their registered structural reasons. This does not establish rejection of every malformed or deceptive representation.

## 5. Executable corroboration

`tools/s_core_w4_negative_controls.py` constructs one canonical representative of each family from the frozen W3 reference source and witness.

The suite preserves all ten controls, processes them through the W3 package validator and faithful witness verifier, and records:

- validation or verification rejection;
- the frozen diagnostic;
- the violated clauses;
- the detection mode;
- unexpected passes or wrong-reason failures.

`tests/test_s_core_w4_negative_controls.py` checks the baseline witness, all ten mutations, the complete distribution, frozen diagnostics, and baseline immutability.

The executable results corroborate the family proofs. They do not replace them.

## 6. Dependency and change audit

This proof uses:

- the frozen `S_core` source contract;
- W0 normalization and applicability;
- W1 direct-axis preservation and reflection;
- W2 dynamics, history, revision, and rule-version preservation;
- W3 target-only recovery, semantics, coherence, machinery, uniformity, composition, and witness assembly;
- the pre-existing negative-control definitions and mapping.

It does not:

- alter `Faithful_split`;
- add a FARA primitive;
- change `S_core` or `S_IRD`;
- assume W5 assembly;
- use W3.5 factorization or specificity as a premise;
- assume primitive necessity or minimality;
- use actual-process correspondence;
- treat executable fixtures as deductive proof.

## 7. Result boundary

This package establishes only the formal incompatibility of the ten registered control families with the frozen faithful-representation relation when their protected distinctions are applicable.

It does not establish:

- `Faithful_split` satisfiability until W5 assembly;
- `THM-CORE-COMMON-001` or `THM-CORE-REP-001`;
- FARA-specificity relative to `GREL-001`;
- reasoning specificity;
- extension from `S_core` to `S_IRD`;
- universality, necessity, minimality, equivalence, uniqueness, or impossibility;
- proof-assistant verification;
- independent proof review.

## 8. Next work

W4 is complete after this package. W5 remains mechanically blocked by `W3.5-SDG-001` and its required immutable factorization, corpus, specificity, cost, ablation, reconstruction, and claim-impact evidence.
