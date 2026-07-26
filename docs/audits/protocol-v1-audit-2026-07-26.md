# Comparative Representation Protocol v1.0 Audit — 2026-07-26

Status: **Accepted clarification audit; CRP v1.0 remains frozen**

CRP v1.0 consistently distinguishes `H_{S,exists}`, `H_{S,rep}`, `H_{C,G}`, and `H_{C,R}`; `H_S` is umbrella-only. It fixes three primary mappings, two adjudicators plus a blinded third for unresolved disagreement, competence/independence/calibration gates, `P=(p_s,p_m,p_o,p_d,p_i,p_h)`, `A_used`, `A_required`, `D`, `O`, `L`, supplied `V`, `R=(D,O,L)`, `G_s`, CIR, commitment/operational equivalence, history/rule/operational treatment, preregistration, and decision-theoretic (non-inferential) interpretation. `Unknown` is incomparable and blocks affected sufficiency/dominance decisions.

## Ambiguities repairable without design change

The terminology authority now fixes exact field spelling and prevents “translation,” “valid,” “dominance,” or “sufficiency” from silently gaining an unregistered meaning. The derivation matrix classifies every protocol component as methodology rather than theory. Implementers must preserve mapping-level records, apply the published canonicalization order, count clauses by the published segmentation rules, and never substitute a consensus CIR for primary `G_s` or complexity.

## Proposed v1.1 changes (not applied to v1.0)

1. Publish executable pseudocode for conservative `P_V`, every tie case, material-better evaluation, and median handling.
2. Define independence conflict disclosures and competence thresholds as machine-readable predicates.
3. Add explicit adjudication rules for semantic-clause segmentation disagreements and missing historical information.
4. Define whether evaluator withdrawal/replacement changes the denominator or forces `Unknown`.
5. Version a complete worked fixture covering every Pass/Partial/Fail/Unknown and dominance-blocking branch.
6. Separate the overloaded abbreviation “CIR” from any future cost/impact ratio.

These would affect implementation compatibility or registered decisions and therefore require CRP 1.1 preregistration, not silent v1.0 edits.
