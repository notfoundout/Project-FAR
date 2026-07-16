# Proof-Step Rules

## Status

Proposed rule semantics for Project FAR proof objects.

---

## Purpose

This document defines the meaning of each proof-step rule used in `theory/proof-objects/*.proof.yaml`.

A proof object is not merely a list of prose claims. Each step must cite prior available inputs and use a rule whose input pattern licenses the step.

The checker currently enforces structural rule patterns. Later versions may enforce stronger logical transformations.

---

## General Requirements

Every proof step must contain:

- `id`: a unique step identifier;
- `rule`: one rule listed in this document;
- `inputs`: a list of previously available premise or step identifiers;
- `statement`: the proposition established by the step;
- `justification`: an explanation of why the rule licenses the statement.

A step may only cite inputs that occur before it.

A proof object may not cite theorem, proposition, or lemma sources unless those sources are declared dependencies of the theorem being proved.

---

# Rule 1 — `definition_unfolding`

## Meaning

`definition_unfolding` licenses a step that expands, applies, or restates the content of a definition, declared context source, or previously established definitional result.

## Required input pattern

At least one input must ultimately cite one of:

- a definition source, such as `DEF-015`;
- a definition alias, such as `D-REP`;
- an approved definitional base source, such as `FAR-model-theory`, `definition-policy`, or `derived-concept-registry`;
- a prior proof step already licensed by a definitional rule.

## Invalid use

It is invalid to use `definition_unfolding` to introduce an unsupported substantive theorem claim.

---

# Rule 2 — `axiom_application`

## Meaning

`axiom_application` licenses a step that applies one or more Project FAR axioms to the current object, process, representation, model, or transition under discussion.

## Required input pattern

At least one input must ultimately cite an axiom source:

- `A1`
- `A2`
- `A3`
- `A4`
- `A5`

## Invalid use

It is invalid to use `axiom_application` without an axiom-bearing input.

---

# Rule 3 — `prior_theorem`

## Meaning

`prior_theorem` licenses a step that applies an already established theorem to the current proof context.

## Required input pattern

At least one input must ultimately cite a theorem source of the form `T-###`.

The cited theorem must exist in theorem metadata and must be declared as a dependency of the theorem being proved, unless the theorem cited is the theorem currently being proved only as an object of discussion rather than as a supporting result.

## Invalid use

It is invalid to use `prior_theorem` to cite an undeclared theorem dependency.

---

# Rule 4 — `lemma_application`

## Meaning

`lemma_application` licenses a step that applies an established lemma to the current proof context.

## Required input pattern

At least one input must ultimately cite a lemma source of the form `L-###`.

The cited lemma must exist in lemma metadata and must be declared as a dependency of the theorem being proved.

## Invalid use

It is invalid to use `lemma_application` with no lemma-bearing input.

---

# Rule 5 — `conjunction_intro`

## Meaning

`conjunction_intro` licenses a step that combines two or more already established inputs into a single combined statement.

## Required input pattern

The step must have at least two inputs.

Each input must be available before the step.

## Invalid use

It is invalid to use `conjunction_intro` with fewer than two inputs.

---

# Rule 6 — `universal_instantiation`

## Meaning

`universal_instantiation` licenses a step that generalizes from an arbitrary object satisfying the stated scope conditions, or applies a universal statement to a particular arbitrary object.

Within current FAR proof objects, this rule is used for controlled arbitrary-object generalization.

## Required input pattern

The step must have at least one input establishing the arbitrary object, scope condition, or universal premise.

## Invalid use

It is invalid to use `universal_instantiation` without any input.

---

# Rule 7 — `semantic_preservation`

## Meaning

`semantic_preservation` licenses a step that preserves semantic content across mappings, transformations, reconstruction, or equivalence claims.

## Required input pattern

At least one input must ultimately cite one of:

- `T-004`;
- `DEF-031`;
- `DEF-033`;
- a prior step established by `semantic_preservation`;
- a premise whose statement explicitly concerns semantic preservation, semantic content, interpretation preservation, or semantic equivalence.

## Invalid use

It is invalid to use `semantic_preservation` for purely structural or syntactic claims without semantic content.

---

# Rule 8 — `registry_substitution`

## Meaning

`registry_substitution` licenses a step that replaces a registered derived concept with its registered derivation path or substitutes already-derived primitive constructions into a later derived construction.

## Required input pattern

At least one input must ultimately cite one of:

- `derived-concept-registry`;
- a registered derived concept of the form `D-###`;
- `T-006`;
- a prior step established by `registry_substitution`.

## Invalid use

It is invalid to use `registry_substitution` for concepts not listed in the derived-concept registry.

---

# Rule 9 — `modus_ponens`

## Meaning

`modus_ponens` licenses the inference from a conditional statement and its antecedent to the consequent.

## Required input pattern

The step must have at least two inputs:

1. an available conditional statement;
2. an available antecedent or statement satisfying the conditional's antecedent.

## Invalid use

It is invalid to use `modus_ponens` with fewer than two inputs.

---

## Enforcement Direction

The current checker enforces rule-specific source and input patterns.

Future proof checkers should enforce stronger content-level constraints, including:

- exact conditional matching for `modus_ponens`;
- exact definition lookup for `definition_unfolding`;
- theorem statement matching for `prior_theorem`;
- lemma statement matching for `lemma_application`;
- semantic-equivalence preservation conditions for `semantic_preservation`.
