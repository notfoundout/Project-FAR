# FARA W4 representation boundary result v1.0

Status: **Research result — bounded sufficient condition, registered failures, global question unresolved**
Execution object: `FARA-REP-W4-001`
Proof object: `FARA-W4-PROOF-001`
Theorem record: `THM-REP-001` (bounded; executable corroboration)
Claim record: `CLM-REP-W4-001`

## Authority recovery and dependency boundary

Canonical repository authority asks in UQ-T7 whether changing rules, continuous dynamics, embodied coupling, incompatible ontologies, and nonclassical consequence can be represented without material expressive loss. The requested W4 list is broader: it also names semantic change, probability, causal/counterfactual structure, oracle access, quotient/merge, deletion/relaxation, and provenance-sensitive history. W4 executes those items as registered extensions; it does not rewrite UQ-T7.

No canonical general representation contract for this question was found. The preservation basis supplies structural, semantic, operational, dependency, information, and historical dimensions. W4 therefore freezes the auxiliary contract below and makes no claim that it is canonical FARA semantics. W1 remains a completed fail-closed execution with all primitive-independence outcomes unresolved. W2 remains only coordinate-separation-induced bounded minimality in `finite_coordinate_trace_v1`. W3 is not consumed.

## Frozen representation contract

- **Source:** a declared tuple `S=(X,R,Sem,Step,Obs,Hist,Ext)` with explicit identities and observation interface.
- **Target:** `finite_tagged_archive_v1`, a finite typed JSON tree. It is data, not an interpreter, oracle, environment, learned model, or proof assistant.
- **Encoding:** serialize every finite explicit component injectively, retaining type tags, stable identities, exact reduced rationals, versioned rules/semantics, total transition tables, dependency edges, and ordered history.
- **Recovery:** deterministically parse the archive. Unsupported, omitted, ambiguous, and nonfinite content produces a registered failure or `Unknown`; it is never guessed.
- **Admissible machinery:** a JSON parser, type-tag dispatcher, reduced-rational arithmetic, and finite table lookup.
- **Equivalence:** commitment equality of recovered declared components up to declared identifier renaming; behavioral equality of every trace at the full declared observation interface.
- **Lossless decision:** all six preservation dimensions must be `Pass`, recovery must be exact, auxiliary machinery must not hide source content, and equivalence must not narrow the interface.
- **Scope:** finite explicit carriers, versions, tables, rational quantities, dependencies, and histories.
- **Excluded:** arbitrary exact real state without finite presentation, tacit content without an explicit identity criterion, absent live facts, undeclared semantic/ontology alignment, and sampled substitutes for unbounded histories.

## Claims kept separate

Representability asserts only that an admissible encoding exists. Losslessness adds complete preservation and machinery closure. Recoverability requires the declared inverse. Behavioral equivalence compares full-interface traces. Semantic equivalence compares interpretations and commitments. Historical/dependency preservation compares ordered provenance and dependency edges. Operational simulation merely reproduces outputs. Bidirectional translation requires admissible preservation in both directions. None is used as proof of another.

## Results

The machine record gives every exact witness, preservation vector, information change, recovery status, hidden machinery disclosure, interface narrowing, and eight independently reported claim outcomes. Positive exact witnesses cover versioned rule replacement, versioned semantic interpretation, nonmonotonic retraction with justifications, exact finite rational probability, and deletion/relaxation with retained tombstones and versions.

The deterministic case table is published in the [generated W4 summary](../../theory/evaluation/generated-fara-w4-representation-summary.md).

Adversarial cases establish bounded failures: incompatible ontology identity collapse prevents recovery; classical explosion changes paraconsistent consequence; observational distributions collapse distinct causal models; finite prefixes collapse arbitrary exact real states; an embodied replay hides the body/environment; oracle syntax omits future answers; quotient merge loses pre-merge identity; final-state projection loses provenance; and a decoder-held rule policy encodes the answer as hidden machinery.

`Unknown` remains material in the continuous, embodied/tacit, and historical dimensions where semantic identity or dependency cannot be adjudicated. Narrowed behavioral agreement is explicitly recorded in the ontology, causal, continuous, quotient, and provenance cases and does not become semantic equivalence.

## Strongest justified result

For sources inside the frozen finite explicit scope, the typed serialization is injective up to declared identifier renaming, its parser is an inverse, and replay of total finite transition tables preserves all finite traces at the full interface. This is a bounded sufficient condition for faithful representation under the auxiliary contract.

One necessary condition is independently established: if inequivalent sources collide under an encoding, no deterministic recovery map can recover both. Exact recovery therefore requires injectivity modulo the declared commitment equivalence. Full behavioral equivalence also requires every distinction exposed by the declared observation interface.

This does **not** prove a universal lossless representation theorem, a canonical target, W1 independence, W2 global minimality, semantic identity across undeclared interpretations, or faithful representation of arbitrary infinite, continuous, embodied, open-world, or oracle-dependent systems. Finite exhaustive checks corroborate only the registered bounded model.

## Assurance and reproduction

`python tools/check_fara_w4_representation.py` validates contract completeness, all preservation vectors, encoding/recovery consistency, hidden machinery disclosure, interface/equivalence drift, omitted loss, unsupported promotion, identifier ownership, report freshness, and an exhaustive 64-source finite injectivity/recovery fixture. The regression tests adversarially mutate each fail-closed control.

This is executable corroboration, not proof-assistant verification. No Lean or other kernel-checked proof of `THM-REP-001` was produced.
