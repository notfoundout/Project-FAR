# Proof-Step Semantics 1.0

## Status

Normative for machine-readable proof objects.

## General judgment

A proof state is a finite ordered environment `Γ` mapping premise and prior-step identifiers to statements plus provenance. A proof step has the form:

`Γ ⊢ rule(inputs) ⇓ statement`

A step is valid only when every input identifier is already available, the rule-specific preconditions hold, the output statement is well formed, and the output is justified by the cited inputs under the rule below. Structural availability is necessary but not sufficient.

## Common requirements

Every step requires a unique `id`, a known `rule`, an ordered `inputs` list, a nonempty `statement`, and a nonempty `justification`. A step may cite premises and earlier steps only. No rule may introduce a stronger claim than its sources license. Rule names describe proof obligations; they are not evidence by themselves.

## Rule semantics

### `definition_unfolding`

Input: at least one statement whose provenance contains a registered definition, derived-concept definition, definitional base source, or an earlier valid unfolding.

Output: the source statement with one or more defined terms replaced by their registered definiens, preserving scope and variable binding.

Invalid: adding empirical or logical content absent from the definition; reversing a one-way definition; changing quantifier scope.

### `axiom_application`

Input: at least one premise whose provenance contains a declared axiom and any additional premises required by that axiom's antecedent.

Output: an instance of the axiom under a declared substitution.

Invalid: citing an axiom without satisfying its side conditions; producing a claim outside the axiom schema.

### `prior_theorem`, `prior_proposition`, `lemma_application`

Input: a source carrying the corresponding registered theorem, proposition, or lemma plus any premises required to instantiate it.

Output: the registered conclusion or a valid instance obtained by explicit substitution.

Invalid: using an undeclared dependency; strengthening the registered result; changing its scope or conditions.

### `modus_ponens`

Input: exactly or at least two available statements containing a conditional `P → Q` and a statement matching `P` under the same substitution.

Output: `Q` under that substitution.

Invalid: affirming the consequent, denying the antecedent, or using mismatched substitutions.

### `conjunction_intro`

Input: at least two available statements `P1 ... Pn`.

Output: their conjunction, preserving each conjunct without alteration.

Invalid: omitting a cited conjunct while claiming full conjunction, or adding an uncited conjunct.

### `universal_instantiation`

Input: a universally quantified statement `∀x∈D. P(x)` and a term `t` established or declared to be in `D` when a domain restriction exists.

Output: `P(t)` with capture-avoiding substitution.

Invalid: instantiating outside the domain or capturing variables.

### `registry_substitution`

Input: a statement containing a registered derived concept and provenance to the derived-concept registry or its governing theorem.

Output: a statement obtained by replacing the derived concept with its registered expansion, or the reverse only when the registry declares equivalence.

Invalid: substituting an unregistered concept or treating a directional reduction as biconditional.

### `semantic_preservation`

Input: a source statement, an interpretation or translation mapping, and an explicit preservation condition or cited preservation theorem.

Output: a statement whose truth conditions are equivalent under the declared mapping within the stated scope.

Invalid: claiming preservation from syntactic similarity alone; omitting the mapping; changing ontology, hidden state, admissibility, or historical commitments without proving commitment-equivalence.

## Output discipline

The proof-object conclusion must equal a step statement and align with the theorem's canonical Statement section. Warnings about weak lexical overlap do not establish semantic validity. A checker may reject clear rule violations mechanically; cases requiring theorem proving remain unresolved rather than silently accepted.

## Invalid examples

See `examples/proof-objects/invalid/` for executable negative fixtures. Each fixture must fail `tools/check_proof_object.py` for the stated reason.
