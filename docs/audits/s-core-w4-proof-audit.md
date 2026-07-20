# S_core W4 Proof Audit

## Audit target

- Proof: `SCORE-W4-PROOF-001`
- Obligation: `OBS-SC-010`
- Scope: frozen finite `S_core`
- Control families: `NC-01` through `NC-10`

## Definition preservation

The W4 package does not alter:

- `THM-TARGET-001`;
- `FAITHFUL-REP-001`;
- the P8 split;
- `S_core` or `S_IRD`;
- the FARA target interface;
- W0 through W3 statements or proofs;
- any negative-control family definition.

The family result is derived from the controls and faithful-representation clauses frozen before W4 execution.

## Proof authority

The family-level mathematical argument in `docs/research/s-core-w4-negative-control-proof-v1.0.md` is the proof authority.

The executable implementation and fixtures provide bounded corroboration only. Ten passing mutation tests alone would not prove the quantified result, because each mutation is only one representative of its control family.

## Applicability discipline

Every control has a protected distinction and an explicit applicability condition. A source with no material instance of that distinction is classified `not_applicable`; it is not treated as a successful rejection.

This prevents vacuous evidence from:

- empty history axes;
- provenance-free sources;
- sources with only one dependency role;
- sources whose process commitments are explicitly declared output-only.

## Registered rejection reasons

The proof maps the ten families to clauses already present in `FAITHFUL-REP-001`:

| Control | Frozen rejection basis |
|---|---|
| NC-01 | P4, P5, or P7 process/dependency/history loss |
| NC-02 | P4 relation reflection |
| NC-03 | P7 order, revision, or path reflection |
| NC-04 | admissible recovery or complete machinery accounting |
| NC-05 | semantic agreement and lexical invariance |
| NC-06 | admissible recovery, uniformity, or machinery accounting |
| NC-07 | image accountability or machinery accounting |
| NC-08 | P4, P7, or Pres_8I provenance preservation |
| NC-09 | P4-P7 process equivalence beyond terminal output |
| NC-10 | complete machinery accounting and anti-reintroduction |

No control is rejected merely because it is labeled a negative control.

## Executable audit

The reference suite:

- begins from the accepted W3 reference witness;
- processes all controls through the W3 package validator and witness verifier;
- preserves the baseline package without mutation;
- records the full ten-control distribution;
- preserves unexpected passes, wrong-reason failures, and implementation defects as possible outcomes;
- does not repair a control after execution.

The fixture manifest records ten expected rejections and zero unexpected passes for the canonical representatives.

## Result boundary

The justified conclusion is:

> The frozen faithful-representation relation rejects each applicable registered NC-01 through NC-10 family for at least one registered structural reason over `S_core`.

This establishes the registered W4 nontriviality obligation. It does not establish:

- rejection of all invalid representations;
- satisfiability of the complete faithful predicate;
- the finite-core representation theorem;
- FARA-specificity relative to `GREL-001`;
- primitive necessity;
- minimality, uniqueness, or universality;
- extension to `S_IRD`;
- machine-checked or independently reviewed proof.

## Residual risks

1. The family proofs depend on the correctness and independence of the frozen source-materiality and applicability declarations.
2. Opaque semantic substitutions may require human semantic adjudication even when the structural verifier detects the canonical representative.
3. Hidden runtime dependencies outside the registered execution envelope remain an implementation-audit risk.
4. `NC-10` establishes anti-smuggling accountability, not a lower bound proving that a named primitive is indispensable.
5. The result may be generic to strong representation contracts rather than specific to FARA; W3.5 must determine that relationship.

## Audit conclusion

`SCORE-W4-PROOF-001` is internally coherent with the frozen W0-W3 program and supports marking `OBS-SC-010` `obstruction_established` at its registered scope.

W5 must remain blocked until the separate evidence-backed `W3.5-SDG-001` campaign resolves.
