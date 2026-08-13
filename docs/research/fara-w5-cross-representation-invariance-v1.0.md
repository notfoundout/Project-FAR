# FARA W5 cross-representation invariance v1.1

Status: **Unresolved; bounded invariance established for two executable admissible pairs**

Execution object: `FARA-INV-W5-001`  
Proof object: `FARA-W5-PROOF-001`  
Claim: `CLM-INV-W5-001`  
Theorem-status record: `THM-INV-001`  
Limitation: `LIM-020`

## Corrected adjudication

The frozen invariance contract requires both representations to recover commitment-equivalent sources and preserve structural, semantic, operational, dependency, information, and historical commitments. The original W5 draft incorrectly treated lossy or unrecoverable pairs as counterexamples to invariance.

That inference is invalid. A pair that fails recovery or any preservation dimension is inadmissible for testing whether the same source yields different conclusions under two faithful representations.

The corrected terminal result is:

> Two executable, exactly recoverable, all-six-preserving pairs establish bounded invariance. No admissible same-source pair with different conclusions was produced. Representation independence remains unresolved.

## Executable evidence

The validator now constructs a concrete six-component source for every fixture, encodes it through each declared family, runs the family-specific recovery path, compares recovered commitments against the source, computes the preservation vector, determines admissibility, and computes the frozen conclusion only when exact recovery succeeds.

The two admissible pairs are:

- `W5-FIX-001`: labeled state-transition system ↔ table-driven model.
- `W5-FIX-002`: typed relational structure ↔ table-driven model.

Both recover the complete source, pass all six dimensions, and produce the same deterministic adjudication.

The nonmonotonic, paraconsistent, causal, semantic-change, identity, provenance, and distributed pairs are retained as representation-boundary witnesses. They are not invariance counterexamples because at least one representation loses a material source commitment.

Oracle, continuous, and embodied fixtures remain unresolved because no finite source-independent recovery execution is available under the frozen machinery policy.

## Failed counterexample attempts

- `CE-W5-001`: rejected because the compared pair loses information.
- `CE-W5-002`: a useful collapse witness, but not a same-source invariance counterexample.
- `CE-W5-003`: rejected because total-order linearization loses partial-order history.
- `CE-W5-004`: rejected because agreement requires forbidden decoder-held semantics.
- `CE-W5-005`: rejected because conclusion-defined equivalence is circular.

## Claim boundaries

Established:

- multiple materially different encodings for the registered fixtures;
- exact recovery and bounded invariance for two finite pairs;
- executable detection of lossy, unavailable, and hidden-machinery cases.

Unresolved:

- representation independence across all registered families;
- any admissible same-source different-conclusion counterexample;
- oracle-dependent, continuous, embodied, and open-world invariance;
- universal invariance.

Explicit nonclaims include that lossy pairs refute invariance, reconstruction implies invariance, simulation implies semantic equivalence, or finite coverage proves representation independence.

## Reproduction

Run:

```bash
python tools/check_fara_w5_invariance.py
python -m unittest tests.test_fara_w5_invariance -v
```

The validator fails closed on declaration/execution drift, recovery contradictions, lossy-pair promotion, conclusion contradictions, family or dimension omission, circular equivalence, hidden decoder machinery, changed obligations, duplicate identifier ownership, and stale generated reports.
