# FAR Intermediate Representation (FIR)

Status: Provisional

## Purpose

FAR Intermediate Representation (FIR) is the minimal machine-readable layer between accepted Project FAR prose artifacts and executable checking tools. Its purpose is not to replace Markdown theory, YAML proof objects, or later mechanized files. Its purpose is to expose enough stable structure for parsers, checkers, reasoning engines, and future Lean translations to compare what an artifact says with what a proof step claims to use.

FIR is intentionally partial in v0.2.0. It records semantic anchors without asserting that Project FAR already has a complete theorem-prover semantics.

## Syntax objects

A FIR syntax object records the surface form of an artifact fragment:

- `id`: stable identifier, such as `T-004`, `L-006`, `DEF-031`, or a proof-step id.
- `kind`: syntactic category, such as theorem, proposition, lemma, definition, axiom, premise, proof step, or dependency.
- `source`: canonical file or source label.
- `text`: the human-readable expression being represented.
- `aliases`: optional equivalent identifiers used by current artifacts.

Syntax objects preserve traceability to Markdown and YAML. They do not by themselves establish meaning.

## Semantic objects

A FIR semantic object records the structured claim associated with a syntax object. The initial v0.2.0 shape is deliberately small:

- `kind`: theorem, proposition, lemma, definition, axiom, or proof-step claim.
- `subject`: the main object or relation discussed.
- `predicate`: the asserted property, relation, or definitional role.
- `scope`: the domain in which the assertion is intended to apply.
- `claim`: a concise natural-language claim used as the comparison anchor.

Semantic objects are comparison targets for the checker. They are not yet complete formal formulas.

## Statement objects

A FIR statement object is the machine-readable statement attached to a theorem, proposition, lemma, definition, or axiom metadata record. It should be minimal, stable, and falsifiable against the corresponding canonical prose. Practical fields are:

```yaml
statement:
  kind: theorem
  subject: Semantic Preservation Theorem
  predicate: holds
  scope: interpretation-preserving representation mappings
  claim: Semantic Preservation Theorem holds within interpretation-preserving representation mappings.
```

A statement object gives the checker a semantic comparison anchor while preserving the Markdown statement as the canonical human-readable formulation.

## Proof-step objects

A FIR proof-step object records:

- `id`: local proof-step identifier.
- `rule`: declared inference rule.
- `inputs`: premise or prior-step identifiers.
- `statement`: the asserted result of the step.
- `justification`: human-readable reason for the step.
- derived lineage: source identifiers inherited from inputs.
- rule lineage: proof rules inherited from inputs.

The checker uses proof-step objects to verify source availability, rule-specific input requirements, and soft alignment with cited semantic statements when those statements exist.

## Dependency objects

A FIR dependency object records that one artifact may rely on another. Minimal fields are:

- dependent artifact id.
- dependency id or approved source label.
- dependency kind, when known.
- status of the dependency.
- source file or registry location.

Dependency objects connect theorem metadata, proof-object premises, derived-concept registry entries, and approved contextual sources.

## Relation to repository artifacts

- Markdown remains the canonical human-readable theory and proof location.
- YAML proof objects provide executable proof-step structure.
- Metadata YAML files provide artifact registries and v0.2.0 statement objects.
- The parser may emit FIR syntax objects from FAR YAML examples and later Markdown extracts.
- The checker consumes FIR-like metadata and proof-step objects to validate rule use and semantic anchors.
- The reasoning engine can use FIR objects as normalized inputs without treating prose formatting as semantics.
- Future Lean files may be generated from, or cross-referenced against, FIR objects after the statement objects become formal enough to support translation.
