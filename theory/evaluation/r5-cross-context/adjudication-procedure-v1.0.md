# Normalization, mapping, and adjudication

**FROZEN.** Roles B and C follow this exactly. It replaces, and must not reuse, the withdrawn global Pareto rubric.

---

## 1. Why the withdrawn rubric is not reused

The comparison used in the prior internal analysis scored candidates on seven dimensions and derived dominance from them. That construction was withdrawn: no dimension carried an externally justified preference orientation, so dominance was undefined, and the claimed dominance was contradicted by the analysis's own table.

**Consequence for this protocol:** no project-supplied dimension set is applied to Role A's answer. The comparison privileges the respondent's own declared criteria, and records neutral structural relations separately without ranking them.

---

## 2. Primary comparison — the respondent's own criteria

Role A field `comparison_H` is the respondent's own account of how competing answers may be compared, if they offered one. Role B applies **that** criterion, not any other.

| `comparison_H` content | Procedure |
|---|---|
| A coherent comparison criterion is given | Apply it as stated to both formulations. Report the result **and** the fact that the criterion is the respondent's. |
| The respondent states that no comparison is justified | Record outcome `O8` as *supported by this respondent*. Do **not** substitute a project criterion to force a comparison. |
| `comparison_H` is unsettled | No primary comparison is available. Report §3 relations only. Do **not** supply a criterion. |
| The criterion is given but incoherent on inspection | Record the incoherence with the exact reason. No primary comparison. Do not repair it. |

Applying a project-supplied criterion where the respondent supplied one, or supplying one where they did not, **invalidates the adjudication**.

---

## 3. Neutral structural relations — recorded separately, never ranked

For each element of Role A's formulation against each element of the project's, Role B records exactly one:

| Relation | Meaning |
|---|---|
| `exact_clause_recovery` | The same requirement, recognisably, in either vocabulary. |
| `implies_forward` | Role A's requirement entails the project's. |
| `implies_backward` | The project's entails Role A's. |
| `overlap_without_implication` | Shared content, neither entails the other. |
| `contradiction` | They cannot both hold. |
| `domain_mismatch` | Stated over different system classes; not comparable as stated. |
| `assumption_mismatch` | Rest on assumptions that are not jointly satisfiable. |
| `no_meaningful_comparison` | No relation can be stated without inventing content. |

**These are descriptive. They are never converted into "better" or "worse" without a justified preference relation, and no such relation is supplied by this package.**

**One-directional failure rule.** `implies_forward` failing does **not** establish `implies_backward` failing, and neither direction failing alone establishes incomparability. Incomparability requires both directions tested and a criterion under which incomparability is defined. A single failed embedding direction establishes exactly one failed embedding direction.

---

## 4. Anti-reconstruction classification

Every apparent match is classified. Only the first two carry strong evidential weight without further argument.

| Class | Definition |
|---|---|
| **EXPLICIT RECOVERY** | Role A stated it. Quote the exact text. |
| **LOGICAL CONSEQUENCE** | Follows from what Role A stated, by an argument Role B writes out in full, using no premise Role A did not supply. |
| **NATURAL REFORMULATION** | Same content in different words, where a competent reader of Role A alone would accept the rewording. Weight: moderate; argue it. |
| **OPTIONAL ENCODING** | Expressible in Role A's terms, but Role A did not require it. Weight: low. Not recovery. |
| **FORCED RECONSTRUCTION** | Requires an auxiliary definition, assumption, or structure **absent** from Role A. Weight: **none**. Records a failure of recovery, not a recovery. |

**The mapper may not introduce auxiliary definitions absent from Role A in order to produce agreement.** Any mapping that needs one is `FORCED RECONSTRUCTION` by definition. Every failed mapping is preserved with its reason; failed mappings are evidence and are never discarded.

**Machinery charging.** If Role A's formulation requires a decoder, interpreter, schedule, lookup, or side-channel to reproduce a project requirement, that machinery is recorded and charged against the mapping. Whether Role A independently imposed a comparable charging rule is recorded separately as `S3`.

---

## 5. Anonymization

Where practical, Role C receives the two normalized formulations with origin labels stripped and order randomized, and records its outcome classification before origins are disclosed. Where anonymization is impractical — for example when one formulation is recognisable from its vocabulary — this is recorded as an anonymization failure on the run, and the outcome carries that limitation.

---

## 6. Outcome assignment

Role C assigns one primary outcome from the frozen registry `O1`–`O12`, plus any secondary outcomes that also hold, and cites the specific §3 relations and §4 classes supporting each.

**No outcome is scored as supporting the programme by default.** `O1` requires `EXPLICIT RECOVERY` or `LOGICAL CONSEQUENCE` on every element of the project formulation, at contamination level `C0` or `C1`, or it is `O2` at best.

**The asymmetry rule from the contamination questionnaire applies:** contamination degrades evidence of agreement and does not degrade evidence of divergence.

---

## 7. What a completed run can and cannot establish

| Can establish | Cannot establish |
|---|---|
| That one independently constituted party did or did not arrive at a comparable formulation | That the project formulation is correct, natural, or uniquely selected |
| That specific requirements were or were not independently recovered | Universality, from any number of positive runs |
| That a specific falsification condition was or was not met | That no dominating formulation exists outside what was elicited |
| That the elicited answer is or is not stable across two framings | That the answer is framing-independent in general |
| Divergence, counterexamples, and alien formulations at full weight | A comparison relation over formulations, which this package does not supply and does not attempt to derive |
