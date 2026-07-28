# FARA core formalization v1.0

Status: **Research — multiple non-equivalent coherent formalizations remain**

## Authority recovery and discrepancy

`FARA-VOC-001` leaves two exact obligations relevant here: “formalize canonical derivation and composition rules” and “resolve circular primitive definitions identified by W1.” Repository authority does not combine them into a designated workstream and supplies no W7 designation. The initiating prompt authorizes their combined execution and expects a canonical-core specification; this campaign is therefore named descriptively, not W7. Open-problem and unresolved-question registers remain indexes rather than execution authorization.

W0–W5 and the vocabulary-extension campaign remain authoritative for their original scopes. In particular, W1's seven outcomes remain unresolved; W2 remains bounded; W3 remains a reconstruction result; W4 remains a representation boundary; W5 invariance remains unresolved; and no vocabulary-extension classification is promoted.

## Exact target and result

The machine-readable specification freezes a finite many-sorted relational object language, disjoint typed carriers, symbol formation and typing, partial interpretation, finite rules and transitions, identity criteria, admissible models of carrier size at most two, structure-preserving maps, commitment-preserving isomorphism, bounded derivability, consistency, conservativity, extension, and fail-closed outputs. It separates object language, metalanguage, source entities, tokens, meanings, rules, executions, results, investigation context, and external dependencies.

The pre-formalization graph retains the exact W1 hazards. The selected post-formalization graph is a DAG: `Property` is a typed unary `Relation`; `Investigation` is an objective/conditions/calculus tuple; `SemanticContent`, `Execution`, and `Result` are derived. `Object`, `Relation`, `Representation`, `Interpretation`, and `ReasoningCalculus` have bounded paired-reduct countermodels. These are new model-relative results and do not overwrite W1 or establish global independence.

Three materially different foundations were executed: many-sorted relational structure, typed hypergraph, and algebraic state-transition structure. All can be made coherent with distinct native machinery and failure profiles. Therefore the terminal result is exactly **multiple non-equivalent coherent formalizations remain**. The chosen specification is an auxiliary test target, not the uniquely correct or canonical final ontology.

## Conservativity and non-vacuity

Making source and token carriers disjoint is a substantive, nonconservative choice relative to models permitted by the underformalized old prose. The unary-Relation definition of Property is conservative. Investigation and full-prose conservativity remain unresolved because the old identity conditions and model class are absent. No prior prose is rewritten.

The accounting rule charges primitive carriers/relations/maps/rules, definitional expansions, finite-set metalanguage, external services, opaque content, and hidden machinery separately. Universal containers, unrestricted payloads, semantic blobs, decoder smuggling, arbitrary higher-order predicates, whole-theory constants, result-defined equivalence, and unconstrained interpretations are rejected.

## Adversarial execution and self-review

Twelve finite families validate typing, formation, execution, recovery, and all six preservation dimensions. Oracle-dependent and continuous/embodied families remain `Unknown`. Incompatible ontologies retain external semantic alignment; partial-order history is not silently totalized. Successful and unresolved formalization counterexamples are retained in the proof object.

The self-review records substantive disjointness, finite-model selection bias, metalanguage support, possible benchmark overfitting, non-semantic portions of conservativity, and the danger of confusing formal elegance, representability, or bounded countermodels with truth, ontology, or global independence.

## Artifacts and validation

- Formal specification: `theory/formal/fara-core-formalization-v1.0.json`.
- Execution/proof object: `theory/evaluation/fara-core-formalization-proof-v1.0.json`.
- Sole deterministic report: `theory/evaluation/generated-fara-core-formalization-report.md`.
- Validator: `tools/check_fara_core_formalization.py`.
- Adversarial mutations: `tests/test_fara_core_formalization.py`.

Exact nonclaims and obligations are pinned in both machine-readable artifacts. Run `python tools/check_fara_core_formalization.py` and `python -m unittest tests.test_fara_core_formalization -v`.
