# P8 Theorem-Role Decision Audit

## Scope

This audit records the freeze of `P8-ROLE-001` and its integration with `THM-TARGET-001` and `FAITHFUL-REP-001`.

## Decision checked

- selected mode: `split`;
- internal obligation: `Pres_8I`;
- external obligation: `Corr_8E`;
- formal faithful predicate: `Faithful_split`;
- application predicate: `ApplicableFaithful`.

## Boundary checks

- Internal provenance and evidence-status distinctions remain protected by the representation relation.
- Actual-process correspondence is not inferred from a theorem about a formal presentation.
- Failure of internal P8 defeats a representation witness.
- Failure of external P8 defeats or weakens an application claim, not the formal theorem automatically.
- Metadata carrying evidential distinctions is counted machinery.
- No experimental replication requirement is introduced as a premise of the formal theorem.

## Gate effects

- formal theorem target: satisfied;
- premise ledger and semantics: satisfied;
- faithful-representation definition: satisfied;
- scoped representation proof: not satisfied.

## Claim effects

No central theorem claim is promoted. No application correspondence is asserted. No theorem is machine checked or independently reviewed.

## Next artifact

Create the `S_core` construction and obstruction lemma ledger. Each admitted source feature must receive a uniform construction obligation or a registered obstruction/countermodel.
