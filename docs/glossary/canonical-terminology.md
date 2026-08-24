# Canonical Terminology Authority

Status: **Accepted terminology authority**
Authority rule: this file owns names, meanings, framework ownership, and epistemic class. Longer formal definitions remain at the linked canonical location; no downstream example, protocol, paper, validation record, or archive item may redefine them.

## Core inventory

| Canonical term | Meaning (bounded) | Owner | Class / status | Canonical detail |
|---|---|---|---|---|
| entity | Neutral protocol word for an explicitly represented item; in canonical theory use **object** unless a protocol schema requires `entity`. | shared theory | alias, not a new primitive | [`definitions.md#object`](../../theory/definitions/definitions.md#object) |
| object | Anything explicitly distinguishable; no independent-existence commitment follows. | shared theory / FARA schema | schema role; not a global primitive | [`definitions.md#object`](../../theory/definitions/definitions.md#object) |
| property | A represented characteristic an object may possess. | FARA | schema role; derived as a unary relation in the accepted kernel | [`definitions.md#property`](../../theory/definitions/definitions.md#property) |
| relation | An explicitly specified association among objects. | FARA | schema role; not a global primitive | [`definitions.md#relation`](../../theory/definitions/definitions.md#relation) |
| attribute | A schema-level property/value field; not a distinct theoretical primitive. | methodology | derived alias | this table |
| trace / reasoning trace | Ordered state/transition record sufficient for the declared reconstruction purpose. | FARA | derived; sufficiency scope-dependent | [`definitions.md#reasoning-trace`](../../theory/definitions/definitions.md#reasoning-trace) |
| state | Explicit characterization of a system at a specified analytical point. | shared theory | derived specification | [`definitions.md#state`](../../theory/definitions/definitions.md#state) |
| state transition | Application/occurrence relating source and target states under a rule or signature. | FARA | derived | [`transition-signatures.md`](../../frameworks/FARA/transition-signatures.md) |
| admissibility | Satisfaction of declared criteria in a declared context. | FARA | derived; not truth | [`definitions.md#admissibility`](../../theory/definitions/definitions.md#admissibility) |
| admissibility space | The candidates and declared criteria/classifications considered by an admissibility structure; not a new primitive. | FARA | derived alias | [`admissibility-structure.md`](../../frameworks/FARA/admissibility-structure.md) |
| valid state transition | A transition permitted by the governing calculus and declared admissibility conditions; “valid” is calculus-relative. | FARA | derived | this table |
| Construct | Introduce an explicit representation or structure. | FAR | workflow verb; not a primitive operator | [`workflow.md`](../../frameworks/FAR/workflow.md) |
| Differentiate | Record an explicit distinction relevant to the declared contract. | FAR | workflow verb; not a primitive operator | [`workflow.md`](../../frameworks/FAR/workflow.md) |
| Restrict | Apply an explicit constraint under a declared contract. | FAR | workflow verb; not a primitive operator | [`workflow.md`](../../frameworks/FAR/workflow.md) |
| Resolve | Apply a declared resolution rule to classified candidates. | FARA/FAR interface | derived procedure; not a primitive operator | [`definitions.md#resolution-execution`](../../theory/definitions/definitions.md#resolution-execution) |
| fourth/fifth operator | Historical global-basis search label. Operator count is not invariant without a fixed language, equivalence, and cost contract. | historical research | closed as an ill-posed global search | [`Project-FAR-Theory-Closure-v1.0.md#theorem-8--operator-count-noninvariance`](../../theory/theorems/Project-FAR-Theory-Closure-v1.0.md#theorem-8--operator-count-noninvariance) |
| mapping | Explicit correspondences from source representation components to target components. | shared theory | derived | [`definitions.md#representation-mapping`](../../theory/definitions/definitions.md#representation-mapping) |
| local comparison contract | Cases, tests/contexts, typed outcomes, and an observation relation; cross-system forms also fix language, profiles, frame, transformations, and any loss/cost order. | shared theory | governing parameter | [`definitions.md#local-comparison-contract`](../../theory/definitions/definitions.md#local-comparison-contract) |
| behavior map | Complete tuple of declared test outcomes for a case. | shared theory | derived from a contract | [`definitions.md#behavior-map`](../../theory/definitions/definitions.md#behavior-map) |
| factorization audit | Decoder construction plus collision search for exact sufficiency. | FAR | theory-constrained methodology | [`definitions.md#factorization-audit`](../../theory/definitions/definitions.md#factorization-audit) |
| representation collision | Same representation, different declared behavior. | shared theory / FAR | exact refutation witness | [`definitions.md#representation-collision`](../../theory/definitions/definitions.md#representation-collision) |
| observational equivalence | Equality under every declared test. | shared theory | contract-relative equivalence | [`definitions.md#observational-equivalence`](../../theory/definitions/definitions.md#observational-equivalence) |
| observational quotient | Cases modulo observational equivalence; unique least-informative exact representation up to isomorphism. | shared theory | proved contract-relative construction | [`definitions.md#observational-quotient`](../../theory/definitions/definitions.md#observational-quotient) |
| translation | A mapping that produces a target representation; preservation must be reported, never presumed. | methodology | derived | this table |
| representation | An explicitly distinguishable item used to denote, describe, encode, or refer under an interpretation. | shared theory / FARA | contract and schema role; not a global primitive | [`definitions.md#representation`](../../theory/definitions/definitions.md#representation) |
| interpretation | The assignment of meaning to a representation under a declared context or profile. | shared theory / FARA | contract parameter; not intrinsic to the representation | [`definitions.md#interpretation`](../../theory/definitions/definitions.md#interpretation) |
| investigation | The declared domain in which representations, interpretations, reasoning, and evidence are organized. | FARA | schema role; not a global primitive | [`definitions.md#investigation`](../../theory/definitions/definitions.md#investigation) |
| reasoning calculus | The declared rules, semantics, and consequence parameters governing a reasoning process. | FARA | contract parameter when consequence-affecting; schema role otherwise | [`definitions.md#reasoning-calculus`](../../theory/definitions/definitions.md#reasoning-calculus) |
| Admissibility Structure (Ω) | A representation of calculus-produced candidate classifications and provenance. | FARA | derived materialized view; not a cause or primitive | [`admissibility-structure.md`](../../frameworks/FARA/admissibility-structure.md) |
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
| representational sufficiency | Exact declared behavior factors through the representation; approximate forms require an added loss/order contract. | shared theory / FAR | contract-relative theorem or OPEN/REFUTED assessment | [`definitions.md#exact-representation-sufficiency`](../../theory/definitions/definitions.md#exact-representation-sufficiency) |
| universality | Coverage of every member of an explicitly specified domain under a declared contract. | shared theory | claim dimension; finite panels never establish an open domain alone | [`definitions.md#universal`](../../theory/definitions/definitions.md#universal) |
| minimality | Least information or cost under a stated contract, objective, equivalence, and order. | shared theory | contract-relative; no contract-free nontrivial minimum | [`definitions.md#minimal`](../../theory/definitions/definitions.md#minimal) |

## Retired language

“Meta-Theory” and “Accepted Root Theory” are historical labels only. Active prose must use **shared theory** and **foundations**, respectively, or explicitly mark a quotation/path as historical. Archive files retain original wording for provenance and are non-authoritative.

Capitalization is retained for the historical workflow labels **Construct**, **Differentiate**, and **Restrict**; it does not confer primitive status. Protocol field spelling is exact: `A_used`, `A_required`, `D`, `O`, `L`, `P`, `R`, `G_s`, and `CIR`.
