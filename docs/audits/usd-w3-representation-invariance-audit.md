# Audit — USD-W3 representation invariance

## Scope integrity

The tested source benchmark and preservation contract are inherited from USD-W2. Transformations are candidate-independent and do not add FARA-specific assumptions.

## Equivalence integrity

Commitment-equivalence preserves ontology, hidden state, admissibility, dependencies, revisions, and history. Output equality and label identity are explicitly insufficient.

## Execution integrity

Every registered admissible transformation was applied to both successful USD-W2 vocabularies. Preservation and cost ledgers were recomputed rather than copied. Negative controls were evaluated separately and rejected.

## Comparison integrity

No scalar score was introduced. Existing Pareto relations were required to remain stable under admissible transformations. FARA and LTS-PROV remain incomparable; no winner was manufactured.

## Classification integrity

The correct result is `bounded_invariance_supported`. A global invariance claim would exceed the tested transformations, vocabularies, and benchmark family.

## Claim boundary

This audit does not establish independent review, global invariance, necessity, minimality, uniqueness, universality, or actual-process correspondence.