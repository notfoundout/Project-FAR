# G2 Open-World Structural Lower Bound v1.0

## Question

Can the finite extension ledger used by the prior relative-maximality result be replaced by a theorem quantified over arbitrary candidate representation types and arbitrary candidate packages?

## Result under validation

The G2 theorem does not enumerate symbolic, graph, neural, distributed, probabilistic, hybrid, or future representation families. It quantifies over an arbitrary Lean type `Candidate` and every member of that type.

For any candidate satisfying the independently stated full-faithfulness contract, the theorem derives five representation-independent structural obligations:

1. recoverable commitment;
2. constrained evolution;
3. dependency structure;
4. semantic interpretation;
5. historical trace.

These are the theorem-facing RCCD obligations. The derivation is mediated by an explicit `IndependentLowerBoundBridge` whose inputs are the eight independently frozen preservation dimensions rather than RCCD vocabulary in target-class membership.

## Why this is not another finite search

The theorem contains no candidate registry, vocabulary list, closed challenge ledger, or exhaustion claim. New representational media are covered whenever they satisfy the same admissibility, machinery-closure, and full-faithfulness conditions.

Formally, the result has the shape:

```text
forall Candidate : Type,
forall candidate : Candidate,
Admissible(candidate) and
MachineryClosed(candidate) and
FullFaithfulness(candidate)
implies
RCCDRealized(candidate).
```

## Critical bridge boundary

The theorem does not obtain the five obligations merely by naming them. The bridge records the lower-bound arguments:

- information preservation, total registered queries, and failure/Unknown separation require recoverable commitments;
- operational and structural preservation require constrained evolution;
- dependency preservation requires dependency structure;
- semantic preservation requires semantic interpretation;
- historical preservation requires historical trace.

The scientific burden is therefore concentrated in the independence and adequacy of these bridge lemmas. Previous UPP work established their relative operational forms. This PR composes them into an arbitrary-candidate quantified theorem.

## Claim boundary

This establishes open-world structural maximality only over candidates for which admissibility, machinery closure, and the full independent faithfulness contract are warranted. It does not establish:

- facts about inaccessible cognition;
- unrestricted metaphysical universality;
- a unique ontology or implementation;
- that every physical or cognitive process belongs to the reasoning class;
- that finite testing proves universality.

The inaccessible-evidence and maximal-knowability question remains G3.
