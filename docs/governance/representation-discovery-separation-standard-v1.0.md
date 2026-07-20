# Representation–Discovery Separation Standard v1.0

## Status

Frozen governance standard effective on merge.

## Purpose

Project FAR maintains two logically separate research programs:

1. **Representation capacity and fidelity** — whether a declared target can encode, recover, and preserve a frozen source class.
2. **Universal-structure discovery** — whether any nontrivial, representation-independent structure is necessary for reasoning and survives alternative vocabularies, non-reasoning contrasts, ablation, and reconstruction.

Success in the first program does not constitute evidence for the second unless a separately registered bridge result is proved.

## Governing non-implications

The repository must enforce:

\[
\text{faithful representation} \not\Rightarrow \text{universal structure}
\]

\[
\text{common target schema} \not\Rightarrow \text{reasoning-specific structure}
\]

\[
\text{recurrence across examples} \not\Rightarrow \text{necessity}
\]

\[
\text{ablation failure in FARA} \not\Rightarrow \text{global necessity}
\]

\[
\text{finite } S_{core}\text{ result} \not\Rightarrow S_{IRD}\text{ universality}
\]

\[
\text{successful vocabulary} \not\Rightarrow \text{minimal vocabulary}
\]

These are dependency rules, not discretionary wording preferences.

## Track classification

### REP — Representation track

`THM-TARGET-001`, `FAITHFUL-REP-001`, `P8-ROLE-001`, and `SCORE-W0-PROOF-001` through `SCORE-W3-PROOF-001` belong to the REP track.

The strongest authorized W3 description is:

> A project-authored finite construction supplies one fixed FARA target schema, one target-only recovery family, and one integrated witness package for every frozen `S_core` source before formal negative controls and theorem assembly.

REP results may establish encoding capacity, preservation, reflection, recoverability, coherence, uniformity, composition, and machinery accounting. They do not establish reasoning-specificity, necessity, minimality, uniqueness, or universal structure.

### USD — Universal-structure discovery track

The USD track is governed by `THM-US-TARGET-001`. It tests architecture-neutral candidate invariants against:

- independently specified reasoning systems;
- independently specified non-reasoning and disputed systems;
- admissible representation changes;
- generic relational baselines;
- ablation;
- alternative reconstruction;
- equivalence and cost relations.

### ADJ — Adjudication track

The ADJ track compares REP constructions with generic and alternative architectures. It determines whether a FARA result is:

- strictly FARA-specific;
- a conservative extension;
- translation-equivalent to a generic baseline;
- more constrained but equally expressive;
- dominated by a simpler architecture;
- unresolved.

## Mandatory W3.5 bridge

After W3 and before W5 theorem assembly, the project must resolve the registered W3.5 specificity-and-discovery gate.

W4 formal negative controls may execute in parallel. W5 may not assemble or promote the finite-core result until W3.5 records:

1. the generic-baseline factorization result;
2. the FARA-specificity classification;
3. the reasoning/non-reasoning discrimination status;
4. the effect on all central claims;
5. any exposed hidden machinery, countermodel, equivalence, or simplification.

## Claim-state isolation

Every central claim must have an independent status. In particular:

- REP progress may update `CLM-REP-CAPACITY`;
- REP progress may not update `CLM-UNIVERSAL-STRUCTURE`;
- USD progress may not be inferred from REP obligation counts;
- minimality and necessity remain blocked until their own universes and proof obligations are frozen;
- generated dashboards may display the tracks together but may not aggregate them into one progress percentage.

## Proof-status discipline

Repository checks may verify artifact consistency and executable corroboration. They may not describe those checks as mathematical proof verification.

Internal written derivations remain project-authored proof packages until proof-assistant verification or independent reconstruction is separately recorded.

## Revision policy

Changing a frozen REP theorem does not silently change the USD target. Changing the USD scope, contrast class, invariance relation, reconstruction universe, or minimality preorder requires a versioned revision.

## Failure preservation

A result that FARA is equivalent to a generic baseline, not reasoning-specific, nonminimal, or nonuniversal is a valid Project FAR result and must be preserved without repair by definition change.
