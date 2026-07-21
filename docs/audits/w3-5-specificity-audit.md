# W3.5 Reasoning Discrimination and Specificity Audit

## Audited package

- `W35-REASONING-LICENSING-001`
- `W35-SCOPE-RESULT-001`
- `W35-SPEC-RESULT-001`
- runtime implementation `tools/w3_5_specificity.py`
- independent repository checker `tools/check_w3_5_specificity.py`
- hostile regression suite `tests/test_w3_5_specificity.py`

## Scope audit

The runtime covers exactly 18 frozen records:

- 8 positive;
- 8 contrast;
- 2 disputed.

Scoring excludes admission class, family, title, rationale, candidate-exposure metadata, and expected-result fields. Labels are joined only after every criterion vector and decision is computed.

## Semantic-coding audit

The licensing registry is explicitly marked:

- project-authored;
- non-blind at the semantic-coding level;
- not independent external evaluation;
- not a private holdout.

No claim of evaluator independence is permitted.

## Result audit

The frozen result requires:

- all eight positives to be `reasoning_like`;
- all eight contrasts to be `nonreasoning_like`;
- both disputed records to remain `borderline`;
- no statistical inference;
- no promotion of the registered result into a universal definition.

## Specificity audit

The same criterion inputs exist in the candidate-neutral source projection and survive exact GREL recovery. FARA provides direct role access and stronger schema constraints but not unique registered-scope discriminative capacity.

The audit therefore accepts:

- bounded discrimination: established;
- FARA role directness: supported;
- FARA uniqueness at registered scope: refuted;
- general FARA specificity: not established;
- primitive necessity: not established.

## Hostile checks

The test suite rejects:

- admission labels inside the licensing registry;
- missing criteria;
- blind or independent-evaluation inflation;
- FARA uniqueness promotion;
- primitive-necessity or general-specificity promotion;
- disputed cases entering the primary metric;
- candidate-registry promotion;
- status-only W5 authorization;
- missing gate evidence.

## Gate audit

Only these gates advance:

- `reasoning-contrast-execution` to evidence-backed `satisfied`;
- `fara-specificity-resolved` to evidence-backed `satisfied`.

Candidate, cost, claim-impact, universal-structure, and W5 states remain blocked or unexecuted.

## Conclusion

The package is internally reproducible and mechanically guarded. It establishes a bounded role-conjunctive separation on the frozen synthetic corpus and simultaneously records the negative specificity result: the discriminator is not unique to FARA at this scope.

It is not independent replication, a universal theorem, or W3.5 closure.
