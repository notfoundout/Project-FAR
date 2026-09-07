# Canonical Terminology Authority

Status: **Accepted terminology authority**
Authority rule: this file owns names, meanings, framework ownership, and epistemic class. Longer formal definitions remain at the linked canonical location; no downstream example, protocol, paper, validation record, or archive item may redefine them.

## Core inventory

| Canonical term | Meaning (bounded) | Owner | Class / status | Canonical detail |
|---|---|---|---|---|
| entity | Neutral protocol word for an explicitly represented item; in canonical theory use **object** unless a protocol schema requires `entity`. | shared theory | alias, not a new primitive | [`definitions.md#object`](../../theory/definitions/definitions.md#object) |
| object | Anything explicitly distinguishable; no independent-existence commitment follows. | shared theory | candidate primitive | [`definitions.md#object`](../../theory/definitions/definitions.md#object) |
| property | A represented characteristic an object may possess. | FARA | candidate primitive | [`definitions.md#property`](../../theory/definitions/definitions.md#property) |
| relation | An explicitly specified association among objects. | FARA | candidate primitive | [`definitions.md#relation`](../../theory/definitions/definitions.md#relation) |
| attribute | A schema-level property/value field; not a distinct theoretical primitive. | methodology | derived alias | this table |
| trace / reasoning trace | Ordered state/transition record sufficient for the declared reconstruction purpose. | FARA | derived; sufficiency scope-dependent | [`definitions.md#reasoning-trace`](../../theory/definitions/definitions.md#reasoning-trace) |
| state | Explicit characterization of a system at a specified analytical point. | shared theory | derived specification | [`definitions.md#state`](../../theory/definitions/definitions.md#state) |
| state transition | Application/occurrence relating source and target states under a rule or signature. | FARA | derived | [`transition-signatures.md`](../../frameworks/FARA/transition-signatures.md) |
| admissibility | Satisfaction of declared criteria in a declared context. | FARA | derived; not truth | [`definitions.md#admissibility`](../../theory/definitions/definitions.md#admissibility) |
| admissibility space | The candidates and declared criteria/classifications considered by an admissibility structure; not a new primitive. | FARA | derived alias | [`admissibility-structure.md`](../../frameworks/FARA/admissibility-structure.md) |
| valid state transition | A transition permitted by the governing calculus and declared admissibility conditions; “valid” is calculus-relative. | FARA | derived | this table |
| Construct | Introduce an explicit representation or structure. | shared theory | candidate operator; global irreducibility unresolved | this table |
| Differentiate | Record an explicit distinction relevant to the declared scope. | shared theory | candidate operator; global irreducibility unresolved | this table |
| Restrict | Limit admissible objects, relations, states, or transitions by an explicit constraint. | shared theory | candidate operator; global irreducibility unresolved | this table |
| Resolve | Apply a declared resolution rule to admissible candidates; not established as an irreducible operator. | FARA/FAR interface | derived/procedural; primitive status rejected pending new evidence | [`definitions.md#resolution-execution`](../../theory/definitions/definitions.md#resolution-execution) |
| fourth/fifth operator | Placeholder for a demonstrated irreducible operation beyond the registered candidates. | research | unresolved; none accepted | [`open-problems-register.md`](../governance/open-problems-register.md) |
| mapping | Explicit correspondences from source representation components to target components. | shared theory | derived | [`definitions.md#representation-mapping`](../../theory/definitions/definitions.md#representation-mapping) |
| translation | A mapping that produces a target representation; preservation must be reported, never presumed. | methodology | derived | this table |
| representation | An explicitly distinguishable item used to denote, describe, encode, or refer under an interpretation. | FARA | candidate primitive | [`definitions.md#representation`](../../theory/definitions/definitions.md#representation) |
| framework | Organized specification for a stated objective; framework status implies no fundamentality. | shared theory | derived | [`definitions.md#framework`](../../theory/definitions/definitions.md#framework) |
| vocabulary | Declared set of supplied representational categories and formation permissions. | CRP methodology | methodological input | [`protocol-v1.0.md`](../../theory/evaluation/comparative-representation/protocol-v1.0.md) |
| claim | Proposition advanced with a stated scope and epistemic status. | shared theory | derived | [`definitions.md#claim`](../../theory/definitions/definitions.md#claim) |
| distinction | Explicit recorded difference; capitalized **Differentiate** names the candidate operator, while “distinction” names its result. | shared theory | derived result | this table |
| constraint | Explicit condition limiting admissibility or permitted transition. | shared theory | derived | this table |
| resolution | Recorded result of applying a resolution rule; not synonymous with truth or proof. | FARA | derived | [`definitions.md#resolution`](../../theory/definitions/definitions.md#resolution) |
| failure | Non-satisfaction of declared criteria or inability to complete a declared operation; a valid outcome. | methodology | methodological status | this table |
| uncertainty | Explicitly recorded lack of warranted determination; not automatically probability. | FARO | operational output | this table |
| incompleteness | A declared required component or determination is absent. | FARO | operational output | this table |
| fail report | Structured record of criteria, evidence, failure point, uncertainty, and preserved artifacts. | FARO | independent governance/method choice | [`reporting.md`](../../frameworks/FARO/reporting.md) |
| property selection | Declared choice of properties relevant to an investigation. | FAR | independent methodological choice | [`workflow.md`](../../frameworks/FAR/workflow.md) |
| framework selection | Declared choice of representational/methodological framework and scope. | FAR | independent methodological choice | [`methodology.md`](../../frameworks/FAR/methodology.md) |
| evaluator mapping | One evaluator's mapping under a registered protocol. | CRP methodology | empirical artifact | [`protocol-v1.0.md`](../../theory/evaluation/comparative-representation/protocol-v1.0.md) |
| preservation | Retention of a declared property under a mapping, relative to a criterion. | methodology | evaluated relation | this table |
| expressive loss | Failure to preserve a required representable distinction, commitment, behavior, dependency, or history. | methodology | evaluated outcome | this table |
| operational effect | Difference in permitted transitions, updates, admissibility, termination, or observable outputs. | CRP methodology | evaluated outcome | [`protocol-v1.0.md`](../../theory/evaluation/comparative-representation/protocol-v1.0.md) |
| dependency preservation | Retention of declared support/prerequisite relations. | CRP methodology | preservation dimension | same as above |
| historical preservation | Retention of declared history-sensitive information/effects. | CRP methodology | preservation dimension | same as above |
| comparison | Evaluation of artifacts under one declared relation and common criteria. | FARO | independent operation | [`comparison.md`](../../frameworks/FARO/comparison.md) |
| dominance | No-worse relation with at least one strictly/materially better registered dimension. | methodology | protocol-relative | this table |
| commitment equivalence | No materially different commitments in the categories enumerated by CRP v1.0. | CRP methodology | adjudicated relation | [`protocol-v1.0.md`](../../theory/evaluation/comparative-representation/protocol-v1.0.md) |
| canonicalization | Registered normalization that removes presentation variance without erasing operational or commitment differences. | methodology | independent design choice | same as above |
| CIR | Canonical Intermediate Representation required by CRP v1.0. | CRP methodology | protocol artifact, not canonical theory | same as above |
| Pareto dominance | Componentwise no-worse comparison plus a registered material improvement; `Unknown` blocks affected comparisons. | CRP methodology | decision rule | same as above |
| representational sufficiency | Preservation of all required dimensions for a stated case and criteria. | methodology | empirical, bounded conclusion | this table |
| universality | Coverage of every member of an explicitly specified domain. | shared theory | claim dimension; unbounded FAR universality unresolved | [`definitions.md#universal`](../../theory/definitions/definitions.md#universal) |
| minimality | No component removable without loss relative to a stated objective/scope. | shared theory | claim dimension; global FARA minimality unresolved | [`definitions.md#minimal`](../../theory/definitions/definitions.md#minimal) |

## Retired language

“Meta-Theory” and “Accepted Root Theory” are historical labels only. Active prose must use **shared theory** and **foundations**, respectively, or explicitly mark a quotation/path as historical. Archive files retain original wording for provenance and are non-authoritative.

Capitalization is semantic only for the candidate operator names **Construct**, **Differentiate**, and **Restrict**. Protocol field spelling is exact: `A_used`, `A_required`, `D`, `O`, `L`, `P`, `R`, `G_s`, and `CIR`.
