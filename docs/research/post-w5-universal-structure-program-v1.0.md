# POST-W5-USD-001 v1.0 — Post-W5 Universal-Structure Program

## Status

Frozen prospectively and unexecuted.

This program begins after the bounded `S_core` representation theorem, its Lean mechanization, and the independent-review package freeze. It does not treat those results as evidence that a universal structure exists.

## Controlling separation

The representation track has established and mechanized a bounded statement:

> For every source object in `S_core`, there exists a target object in the frozen theorem-facing FARA class and a witness satisfying `Faithful_split`.

The universal-structure discovery track asks a different question:

> Does an independently defined reasoning scope instantiate a nontrivial kernel that is invariant under admissible representation changes, discriminates reasoning from relevant contrasts, survives ablation and alternative reconstruction, and admits a minimality or equivalence classification?

The first result does not logically imply the second.

## Program objective

The program is designed to force one of the admissible outcomes rather than to protect FARA:

- one universal kernel;
- a kernel only for a proper subclass;
- several translation-equivalent kernels;
- several incomparable kernels;
- only generic structured-system properties;
- no single nontrivial kernel;
- unresolved.

Negative, reduction, equivalence, and no-go results count as central results.

## Frozen hypotheses

### `USD-H-EXIST`

At least one nontrivial common kernel exists over the declared post-W5 reasoning scope.

### `USD-H-INV`

A successful kernel survives every transformation in the frozen admissible-representation class up to declared equivalence.

### `USD-H-DISC`

A successful kernel performs a reasoning-relevant role not discharged by the frozen contrast class or by `GREL-001` alone.

### `USD-H-NEC`

A successful kernel cannot be removed without loss, except through an explicitly equivalent reintroduction counted in the machinery ledger.

### `USD-H-MIN`

Successful kernels admit a minimality, equivalence, incomparability, or no-minimum classification under a frozen candidate universe and cost preorder.

### `USD-H-NO`

No single nontrivial universal kernel exists under the frozen assumptions.

`USD-H-EXIST` and `USD-H-NO` are competing terminal possibilities. Neither is privileged.

## Workstream 1 — Scope extension

`USD-W1-SCOPE-EXT` expands beyond `S_core` one feature family at a time:

1. infinite carriers;
2. continuous dynamics;
3. partial observability;
4. open-ended histories;
5. semantic change;
6. non-finite-support stochasticity;
7. actual-process correspondence.

Each extension unit must freeze its source contract, candidate-independent admission rule, observation boundary, preservation obligations, and counterexample policy before execution.

A feature family may terminate as:

- extension proved;
- proper-subclass result;
- countermodel;
- new assumption required;
- unresolved.

No broad `S_IRD` or universal claim may be inferred from success on one feature family.

## Workstream 2 — Alternative-vocabulary competition

`USD-W2-ALT-VOCAB` compares at least:

- one FARA-derived candidate;
- `GREL-001`;
- two independently motivated non-FARA candidates.

Every candidate must face the same frozen source objects, preservation contract, failure conditions, and machinery accounting. Candidate-specific repair is prohibited.

The decision dimensions are reported separately:

- coverage;
- preservation;
- constraint strength;
- reasoning discrimination;
- derived machinery;
- operations;
- semantic description length;
- equivalent reintroduction.

There is no scalar overall score. Dominance is Pareto-only: a candidate dominates another only when it is no worse on preservation, no greater on every registered cost coordinate, and strictly better on at least one registered coordinate.

## Workstream 3 — Representation invariance

`USD-W3-INVARIANCE` tests whether the commitment survives materially different encodings rather than merely preserving labels.

The minimum transformation classes are:

- renaming and reindexing;
- definitional expansion and contraction;
- relational reification;
- state-transition re-encoding;
- history factoring;
- semantic-interface replacement.

A candidate fails invariance when an admissible transformation preserves the frozen source contract but destroys the alleged kernel commitment.

## Workstream 4 — Global necessity and reconstruction

`USD-W4-NECESSITY` searches for:

- primitive ablation;
- commitment ablation;
- alternative-basis reconstruction;
- hidden machinery;
- equivalent reintroduction;
- minimal counterexamples.

Allowed classifications are:

- necessary in the declared reconstruction class;
- derivable;
- replaceable by an equivalent;
- architecture-dependent;
- scope-dependent;
- refuted;
- unresolved.

A removed primitive does not count as eliminated when the same commitment is restored through helper logic, metadata, an unrestricted interpreter, evaluator repair, or another uncounted mechanism.

## Workstream 5 — Minimality, equivalence, and no-go results

`USD-W5-MIN-EQUIV` begins only after freezing:

- the candidate universe;
- commitment equivalence;
- translation equivalence;
- the cost preorder;
- admissible helpers;
- tie and incomparability rules.

Valid results include:

- unique minimum;
- multiple equivalent minima;
- multiple incomparable minima;
- no minimum;
- no successful kernel;
- unresolved.

Global minimality is unavailable unless the declared candidate universe and lower-bound argument justify it.

## Workstream 6 — Independent challenge

`USD-W6-INDEPENDENCE` keeps four claims separate:

- independent proof review;
- R3 independent technical replication;
- R4 adversarial conceptual replication;
- R5 cross-context replication.

Internal isolated implementations remain R2 and may not be described as independent validation.

## Execution order

The primary order is:

`scope extension → alternative-vocabulary competition → representation invariance → necessity/reconstruction → minimality/equivalence/no-go`

Independent review and adversarial work may proceed in parallel, but they do not substitute for unresolved deductive obligations.

## First execution unit

The next decisive PR must freeze and execute exactly one `USD-W1-SCOPE-EXT` feature family. It must not batch all extension families into one favorable-case exercise.

The recommended first family is partial observability because it directly tests whether the current explicit-state construction survives a materially weaker access relation without smuggling hidden state into the target.

## Decision rules

The following rules are controlling:

- Unknown is not Pass.
- Bounded success is not universality.
- Representation is not necessity.
- Failure to find a counterexample is not proof.
- Candidate-specific scope selection is prohibited.
- Hidden interpreters and metadata smuggling are prohibited.
- Equivalent reintroduction counts against elimination.
- Tradeoffs are not wins.
- Material post-freeze changes create a new version.
- Negative and no-go results are terminal scientific results.

## Universal-claim release gate

A universal-structure claim requires all of the following at the exact claimed scope:

1. coverage resolved;
2. representation invariance resolved;
3. reasoning discrimination resolved;
4. reconstruction and necessity resolved;
5. full cost accounting complete;
6. minimality or equivalence classified;
7. blocking counterexamples resolved or converted into explicit scope limits;
8. claim scope identical to proof scope.

Independent verification additionally requires completed eligible external review with blocking objections resolved without retrospective alteration of the frozen package.

## Nonclaims

This program does not establish that:

- a universal structure exists;
- FARA is the universal structure;
- `S_core` contains all reasoning;
- the current candidate registry is exhaustive;
- any FARA primitive is globally necessary;
- FARA is minimal or unique;
- the W5 theorem advances USD by logical implication;
- independent review or independent replication has occurred.
