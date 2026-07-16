# FAR YAML Grammar 1.0

## Status

Normative concrete syntax for machine-readable `.far.yaml` objects. Semantic validity is additionally constrained by `theory/semantics/proof-step-semantics.md` and the FAR core definitions.

## Conventions

The notation below is EBNF over YAML data-model values, not character-level YAML tokens. `string+` means a nonempty string. `id` means a nonempty string unique within its collection. Lists preserve order.

```ebnf
far-object = investigation,
             [reasoning-system],
             representations,
             [relations],
             [interpretations],
             [rules],
             [transitions] ;

investigation = "investigation" : string+ ;

reasoning-system = "reasoning_system" : {
  "system" : string+,
  "far_primitives" : {
    "Investigation" : string+,
    "Representation" : string+,
    "Representational Structure" : string+,
    "Interpretation" : string+,
    "Reasoning Calculus" : string+
  },
  ["verdict" : verdict]
} ;

verdict = "fits FAR" | "extends FAR" | "falsifies FAR" | "draft" ;

representations = "representations" : [ representation, {representation} ] ;
representation = {
  "id" : id,
  "kind" : string+,
  ["content" : string],
  ["statement" : statement]
} ;

statement = string+ | {
  "kind" : statement-kind,
  "claim" : string+,
  ["subject" : string],
  ["predicate" : string],
  ["scope" : string]
} ;

relations = "relations" : [ {relation} ] ;
relation = {
  "id" : id,
  "type" : string+,
  "source" : representation-id,
  "target" : representation-id
} ;

interpretations = "interpretations" : [ {interpretation} ] ;
interpretation = {
  "representation" : representation-id,
  "meaning" : string+
} ;

rules = "rules" : [ {rule} ] ;
rule = {
  "id" : id,
  ["name" : string+],
  "inputs" : [ {representation-id} ],
  "output" : representation-id,
  ["condition" : string]
} ;

transitions = "transitions" : [ {transition} ] ;
transition = {
  "id" : id,
  "source" : string+,
  "rule" : rule-id,
  "target" : string+,
  ["status" : transition-status],
  "order" : integer
} ;

transition-status = "admissible" | "inadmissible" | "unresolved" | "draft" ;
```

## Static constraints

1. `representations` is required and nonempty.
2. Representation, relation, rule, and transition IDs are unique in their own namespaces.
3. Every representation has nonempty `content` or a valid `statement`.
4. Relation endpoints, interpretation targets, and rule inputs/outputs reference declared representations.
5. Transition rules reference declared rules.
6. Transition orders are unique integers.
7. Unknown top-level keys are rejected in strict mode.
8. Unknown keys inside normative records are rejected in strict mode.
9. Syntax does not assign meaning. Interpretations and rule conditions provide semantic commitments; executable reasoning must respect them.

## Canonical parser contract

`tools/parse_far.py` is the reference parser. A valid file must parse to a `FARObject`, pass strict grammar validation, and pass `FARObject.validate_well_formed()`. A parser that accepts a file violating these constraints is nonconforming.

## Invalid examples

The fixtures under `examples/far/invalid/` are normative negative cases and must be rejected by the reference parser.
