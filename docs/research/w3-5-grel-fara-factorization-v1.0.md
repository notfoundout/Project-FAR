# W3.5 GREL–FARA Factorization v1.0

## Status

Completed bounded factorization over the frozen finite corpus and the accepted finite W3 constructor.

Identifiers:

- experiment: `W35-GREL-FARA-FACTOR-001`;
- result: `W35-FACTOR-RESULT-001`;
- baseline: `GREL-001`;
- FARA constructor: `SCORE-W3-PROOF-001`;
- corpus: `RCS-CORPUS-001`.

This artifact resolves only the six registered baseline-factorization dimensions. It does not resolve FARA-specificity, reasoning/contrast discrimination, candidate invariants, ablation, reconstruction, full machinery cost, central claim impact, W3.5 as a whole, or W5 authorization.

## Question

The experiment asks whether the accepted finite FARA constructor succeeds because FARA has greater bounded representational capacity than a neutral finite typed relational baseline, or because generic finite relational structure can carry the same explicit source contract.

The frozen dimensions are reported independently:

1. expressiveness;
2. translation;
3. constraint strength;
4. reasoning specificity;
5. cost relation;
6. overall interpretation.

No scalar score replaces them.

## Frozen inputs

The experiment uses:

- the frozen `GREL-001` schema;
- the existing `SCORE-W3-PROOF-001` constructor and target-only recovery implementation;
- all six immutable source bundles in `RCS-CORPUS-001`;
- eight positive, eight contrast, and two disputed instances;
- only each record's formal system, candidate-neutral observations, and formalization boundary.

Admission decision, family, title, rationale, and candidate-exposure metadata are excluded from construction. Mutating those fields must not change the compiled source contract.

## Fixed candidate-neutral compiler

One compiler maps every source record into the same finite `S_core` source schema.

The compiler structurally records:

- observable states and their order;
- registered transition constraints;
- represented distinctions;
- the source task;
- the source commitment-or-alternative statement;
- grounds and dependencies;
- the source-declared result;
- uncertainty and revision status;
- provenance and correspondence limits;
- the complete authoritative payload as an audit carrier.

The complete payload is not sufficient by itself. The same information is also projected into the registered P1, P2, P3, P4, P6, and P8I axes and into explicit finite state, transition, and history records.

The compiler has no branch on positive, contrast, disputed, family, title, or expected factorization result.

## GREL construction

`encode_grel` is one recursive finite encoder for arbitrary JSON-shaped values.

It creates:

- three sorts: object, array, and scalar;
- one entity for every source node;
- exact value records for scalar values;
- typed literal attributes;
- ordered field and array-item relation occurrences;
- a fixed schema descriptor;
- one target-only deterministic decoder;
- a complete machinery declaration;
- no case database, hidden interpreter, network use, evaluator repair, or source oracle.

`decode_grel` exactly reconstructs the input from the completed GREL package alone.

## Factorization identity

Let:

- `E_G` be `encode_grel`;
- `D_G` be `decode_grel`;
- `E_F` be the accepted `construct_witness`;
- `P` be a frozen candidate-neutral authoritative source projection;
- `C_F` be the fixed declared FARA-oriented `compile_projection` adapter.

Define the direct FARA pipeline as `F = E_F ∘ C_F` and the GREL-to-FARA translation as `T_GF = E_F ∘ C_F ∘ D_G`.

For every registered projection `P`:

\[
D_G(E_G(P)) = P
\]

and therefore:

\[
T_{GF}(E_G(P))
= E_F(C_F(D_G(E_G(P))))
= E_F(C_F(P))
= F(P).
\]

The executable checker verifies exact projection recovery, adapter stability, and final FARA equality byte-for-byte for all 18 frozen instances.

This is an operational factorization. It is not a primitive reduction because `T_GF` explicitly reuses both the FARA-oriented source adapter and the accepted FARA constructor. Both are declared rather than hidden and neither is assigned to the neutral GREL baseline.

## Reverse translation

The same generic encoder accepts every finite FARA witness package as input. Its target-only decoder exactly recovers that package.

This establishes a fixed FARA-to-GREL translation on the finite target image. Together with `T_GF`, translations exist in both directions on the declared finite image classes.

The result does not assert that every arbitrary GREL package is a valid FARA package. FARA admissibility remains stricter.

## Per-instance checks

Every registered positive, contrast, and disputed instance must pass:

- candidate-neutral compilation;
- exact GREL recovery of the candidate-neutral authoritative projection;
- fixed source-adapter stability after GREL recovery;
- direct FARA construction equals construction through GREL;
- existing FARA target-only recovery;
- exact generic representation and recovery of the FARA package;
- no case database;
- no hidden interpreter.

A single failure blocks the result.

## Dimension results

### Expressiveness: `equivalent`

On the registered finite image class, both architectures recover the same explicit source contract. GREL also exactly carries the finite FARA package as typed relational data.

This is bounded expressive equivalence, not universality or minimality.

### Translation: `bidirectional`

A fixed GREL-to-FARA translation and a fixed FARA-to-GREL translation exist on the declared finite image classes.

The GREL-to-FARA direction reintroduces the fixed FARA-oriented source adapter and the accepted FARA constructor and is therefore not a reduction proof.

### Constraint strength: `fara_stricter`

Arbitrary GREL packages need not enforce FARA's mandatory distinctions between:

- object and representation;
- reasoning state and state representation or record;
- transformation rule, execution, result, and signature;
- admissibility, classification, and Ω;
- resolution rule, execution, and resolution;
- history, provenance, coherence, and target-only recovery.

FARA admits a narrower class of well-formed targets even where bounded representational capacity is equivalent.

### Reasoning specificity: `not_established`

The same factorization succeeds for all eight positive systems, all eight contrasts, and both disputed cases.

Factorization therefore does not distinguish reasoning from nonreasoning within the frozen corpus. This does not refute possible reasoning-specific constraints; it leaves that question to the later discrimination and specificity investigations.

### Cost relation: `tradeoff`

GREL has the smaller fixed architecture surface:

- 10 baseline components;
- one generic tree encoder and decoder.

FARA has:

- 14 architecture fields;
- 5 witness fields;
- stronger validation and machinery obligations.

FARA nevertheless provides direct access to six preservation axes, whereas equivalent semantic access in GREL requires scanning or decoding generic relation and attribute records.

Each architecture is strictly lower on at least one declared cost dimension, so neither Pareto-dominates in this bounded experiment.

### Overall interpretation: `fara_constrained_equivalent`

Bounded representational capacity and fixed translation are equivalent on the registered image class, while FARA imposes stronger admissibility and audit constraints.

The result does not establish that those stronger constraints are reasoning-specific, necessary, minimal, or globally preferable.

## Gate effect

This package satisfies only `baseline-factorization-resolved`.

It leaves unsatisfied:

- `fara-specificity-resolved`;
- `reasoning-contrast-execution`;
- full cost accounting;
- candidate ablation and reconstruction;
- central claim-impact closure;
- universal-structure result;
- W5 authorization.

`W3.5-SDG-001` advances to `in_progress_factorization_complete`.

## Preserved failures and limitations

1. The GREL-to-FARA translator includes the accepted FARA constructor.
2. The corpus is finite, synthetic, public, and not a private holdout.
3. The factorization does not show that FARA primitives reduce to GREL primitives.
4. Factorization succeeds for contrast systems and therefore does not establish reasoning specificity.
5. The cost record is architectural and operation-count based, not a runtime benchmark.
6. No candidate universal invariant is scored.
7. No primitive necessity, minimality, uniqueness, or universality claim is updated.

## Reproduction

```bash
python tools/w3_5_factorization.py
python tools/w3_5_factorization.py --json
python tools/check_w3_5_factorization.py
python -m unittest tests.test_w3_5_factorization
make research-check
```

## Next authorized work

The next investigation is candidate-neutral reasoning/contrast execution and FARA-specificity analysis over the already frozen corpus, followed by candidate ablation, reconstruction, and complete machinery-cost accounting.
