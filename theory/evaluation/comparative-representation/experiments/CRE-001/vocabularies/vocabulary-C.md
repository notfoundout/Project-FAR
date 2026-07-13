# CRE-001 Vocabulary C Package

Status: Frozen evaluator-facing package
Vocabulary package identifier: CRE-001-VOCAB-C-1.0
Experiment: CRE-001
Protocol: CRP-1.0

## Vocabulary Definitions

Use only the following supplied categories as primitive vocabulary terms:

- **Representation**: an explicit represented item, proposition, rule, state element, transition record, or output record.
- **Representational Structure**: explicit structure over representations, including ordering, dependency, rule-status structure, transition structure, admissibility structure, or history structure.
- **Interpretation**: the policy or assignment that gives represented items their scenario meaning, truth condition, status meaning, or output meaning.
- **Investigation**: the bounded task or question that fixes what must be represented and preserved for the mapping.
- **Calculus**: the explicit rule-governed procedure, transition policy, admissibility standard, update rule, or stopping rule used to move between states or judge transitions.

## Evaluator Instructions

Map the frozen scenario into this vocabulary. Use the scenario as fixed; do not alter it, simplify it, or add unstated domain rules. You may introduce derived machinery only under the derived-machinery rules below.

## Permitted Derived-Machinery Rules

Every derived construct must record its declaration, formal role, supplied category under which it is introduced, preservation requirement served, necessity for the mapping, and provenance. Derived machinery may not alter the scenario or introduce unstated domain rules.

## Submission Instructions

Submit the mapping using the official CRE-001 mapping submission template and, where requested, the CIR submission template. Use only label `Vocabulary C`; do not discuss other vocabularies, expected outcomes, prior results, or protocol rationale.
