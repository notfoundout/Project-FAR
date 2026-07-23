# UPP-W14 Maximality Audit

## Registered identity

- Program: `POST-TUE-UPP-001`
- Workstream: `UPP-W14-MAXIMALITY`
- Target PR: `295`
- Successor: `UPP-W15-TERMINAL-THEOREM` at PR `296`

## Evidence reviewed

The audit checks the executable challenge ledger, the machine-readable theorem, the result artifact, all 31 proper-component-subset witnesses, five extension challenges, deterministic validation, and regression tests.

## Decision discipline

The model is three-valued. `Proved` requires a frozen and complete registered ledger with every in-class challenge embedding under all preservation requirements. `Refuted` requires a concrete registered in-class nonembedding or a valid lower-cost full reduction. `Unknown` remains unresolved and is never counted as support or defeat.

The maximality result is relative to frozen extension rules. It does not treat absence of counterexample as unrestricted proof. Open-world challenges, unregistered vocabularies, unresolved equivalence claims, and concealed machinery remain outside the result.

## Anti-smuggling review

The package rejects hidden decoders, external semantic repair, unregistered oracles, circular reconstruction, output-only matching, identity collapse, partial query coverage, failure/Unknown collapse, and cost transfer into omitted support machinery.

## Conclusion

The registered challenge space closes without a surviving counterexample, so relative maximality is supported under the frozen rules. Public evaluation remains unauthorized until the terminal theorem workstream discloses the exact theorem, assumptions, mechanization status, unresolved obligations, and nonclaims.
