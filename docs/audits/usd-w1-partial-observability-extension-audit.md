# USD-W1 Partial-Observability Extension Audit

## Scope

This audit checks `USD-W1-PO-SCOPE-001`, `USD-W1-PO-RESULT-001`, the proof artifact, and the registered fixtures against `POST-W5-USD-001`.

## Findings

- The admission rule is candidate-independent and does not define partially observable reasoning through FARA.
- Agent access is restricted to observation history and derived information state.
- The target constructor does not add a primitive or permit a source-specific decoder.
- Latent state, observation, information state, policy, history, commitment, dependency, revision, and evidential status are separately preserved.
- Both registered negative controls are rejected for their frozen reasons.
- The result is correctly classified as `proper_subclass_only`, not as full partial-observability or `S_IRD` coverage.
- The result has no logical effect on universal structure, necessity, minimality, uniqueness, or actual-process correspondence.
- Mechanization and independent review remain open.

## Adverse interpretation check

The strongest valid statement is that the fixed FARA target can faithfully represent the frozen finite explicit partial-observability subclass without leaking latent state to the represented policy. The artifacts do not support the statement that FARA represents all partially observable reasoning or that the represented distinctions are universal.

## Conclusion

Pass for the registered bounded extension claim. Broader extension and USD claims remain unresolved.
