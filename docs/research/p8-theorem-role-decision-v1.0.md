# P8 Theorem-Role Decision v1.0

## Status

Frozen prospective decision for `THM-TARGET-001` v1.0.

Selected mode: **`split`**.

This artifact resolves the theorem-role parameter. It does not prove a representation theorem, establish application correspondence, validate any actual process model, or establish PB-001 necessity or minimality.

## Decision

P8 — evidential correspondence — is divided into two non-interchangeable obligations.

### P8-I — Internal evidential-status preservation

`P8-I` is internal to `Faithful_split`.

A faithful target representation must preserve and reflect every material distinction represented by the formal source episode concerning:

- observation versus inference;
- reported versus instrumented content;
- assumed versus derived content;
- source identity and provenance;
- confidence, uncertainty, qualification, and unresolved status;
- accepted, rejected, superseded, or withdrawn support;
- the evidence grade attached to a source commitment.

The target may not assign a stronger evidential status than the source presentation supports. Provenance or evidence-status distinctions stored in metadata count as target machinery and must appear in the machinery ledger.

### P8-E — External process-to-presentation correspondence

`P8-E` is not an internal representation coordinate.

A theorem about a formal source presentation does not by itself establish that the presentation faithfully describes a human, machine, institution, physical process, or hidden internal mechanism. Any such application claim requires a separate correspondence artifact identifying:

- the actual process and episode;
- the observation and instrumentation boundary;
- the mapping from process events or states to source-presentation components;
- unsupported or unobservable components;
- the applicable evidential grade;
- uncertainty, limitations, and possible alternative presentations.

Failure of `P8-E` blocks or weakens the application claim. It does not refute a theorem whose quantified subject is only the formal presentation.

## Formal effect

For a formal source episode `(P,J)`, target package `A`, and witness `W`:

```text
Faithful_split(P,J,A,W)
  := Faithful_internal(P,J,A,W)
     and Pres_8I(P,J,A,W)
```

where `Faithful_internal` contains the frozen P1-P7, typing, semantic-agreement, recovery, coherence, uniformity, compositionality, nontriviality, and machinery-accounting clauses.

For an application assertion that actual process `Z` is represented by `(P,J)` and then by `(A,W)`:

```text
ApplicableFaithful(Z,P,J,A,W,Corr)
  := Corr_8E(Z,P,J,Corr)
     and Faithful_split(P,J,A,W)
```

`Corr_8E` is a separate evidence relation. It is not inferred from `Faithful_split`, behavioral similarity, evaluator agreement, successful decoding, or the existence of a representation witness.

## Why `split` is selected

The `coordinate` option is rejected because it conflates two different relations: preservation inside a formal representation and evidence that a formal presentation corresponds to an actual process.

The `side_condition` option is rejected because it would place all provenance and evidence-status distinctions outside the representation theorem, permitting a target to erase or upgrade distinctions already explicit in the source presentation.

The `split` option preserves both requirements without making empirical application evidence a premise of a theorem about mathematical presentations.

## Consequences for theorem targets

- `THM-CORE-REP-001` now uses `Faithful_split`.
- `THM-IRD-EXT-001` now uses `Faithful_split`.
- `THM-P8-CORR-001` becomes the external correspondence theorem or contract family for `Corr_8E`.
- A proof over formal presentations may proceed without independent empirical replication.
- No actual-process application claim may rely on the formal theorem alone.

## Failure conditions

`P8-I` fails when a material internal provenance or evidence-status distinction is lost, collapsed, fabricated, or upgraded.

`P8-E` fails or remains unresolved when the process-to-presentation mapping is unsupported, under-observed, circular, dependent on invented hidden structure, or stronger than the available evidence grade.

A failure of `P8-I` defeats the representation witness. A failure of `P8-E` defeats or weakens the application claim but does not automatically defeat the formal representation theorem.

## Revision control

This decision is content-bearing. Changing from `split` to `coordinate` or `side_condition`, or materially changing the boundary between `P8-I` and `P8-E`, requires a versioned theorem-target revision unless definitional equivalence is proved.

## Nonclaims

This decision does not establish:

- that `Faithful_split` is satisfiable for every `S_core` object;
- that FARA faithfully represents `S_core`;
- that any actual system corresponds to an IRD-001 presentation;
- that PB-001 is sufficient, necessary, independent, minimal, or complete;
- universality, minimality, uniqueness, or impossibility;
- machine verification or independent proof review.
