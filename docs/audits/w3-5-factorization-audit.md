# W3.5 GREL-FARA Factorization Audit

Audit target: `W35-GREL-FARA-FACTOR-001` over `RCS-CORPUS-001` using `GREL-001` and `SCORE-W3-PROOF-001`.

## Scope

The executable package covers all 18 frozen records: eight positive, eight contrast, and two disputed. It verifies exact GREL recovery of each candidate-neutral authoritative projection, fixed adapter stability, equality of direct and GREL-mediated FARA construction, target-only FARA recovery, and exact generic recovery of each finite FARA package.

The GREL-to-FARA translation explicitly uses the fixed FARA-oriented source adapter and the accepted FARA constructor. The result is therefore operational factorization, not primitive reduction.

## Adversarial checks

The tests detect corrupted value references, missing relations, hidden case-database or interpreter flags, candidate-metadata steering, collapsed dimensions, unsupported reduction claims, premature specificity or discrimination, and premature W5 authorization.

## Results

| Dimension | Result |
|---|---|
| Expressiveness | `equivalent` |
| Translation | `bidirectional` |
| Constraint strength | `fara_stricter` |
| Reasoning specificity | `not_established` |
| Cost relation | `tradeoff` |
| Overall interpretation | `fara_constrained_equivalent` |

GREL has the smaller generic architecture surface. FARA provides direct six-axis access and stronger mandatory category, history, provenance, coherence, admissibility, and recovery constraints. Neither architecture dominates under the declared multidimensional cost record.

## Gate conclusion

The evidence supports only `baseline-factorization-resolved`.

The following remain unsatisfied: FARA-specificity, reasoning/contrast execution, complete cost accounting, candidate ablation and reconstruction, claim-impact closure, universal-structure result, and W5 authorization.
