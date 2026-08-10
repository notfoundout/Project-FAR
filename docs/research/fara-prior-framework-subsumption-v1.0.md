# FARA prior-framework subsumption investigation v1.0

Status: **Research result — `H6` at the tested scope, with a strong Stage-10-B component. Every kernel component is independently anticipated by prior work; no single independently motivated framework reconstructs the connecting architecture. No canonical surface modified.**
Investigation target: `OP-20` / `UQ-T23`
Kind: deductive prior-art and embedding analysis. No experiment, no software.

## 1. Exact canonical FARA target tested

The tested target is the **Accepted formal kernel** at its registered scope — Project FAR v1.0 finite, explicit, auditable representational architecture (`frameworks/FARA/formal-kernel.md`, `FARA-FORMAL-KERNEL-001`). FAR and FARO are excluded as downstream. Optional methodology is excluded.

| Component | Canonical source | Epistemic status | Kind |
|---|---|---|---|
| Seven candidate primitives (Object, Property, Relation, Representation, Interpretation, Investigation, Reasoning Calculus) | `primitives.md` | **Provisional candidates; all seven W1 outcomes unresolved** | unresolved — **not treated as established irreducibles** |
| 15 disjoint carriers | `formal-kernel.md` | Accepted at scope | defined |
| 15 typed relations | `formal-kernel.md` | Accepted at scope | defined |
| Admission constraints 1–11 | `formal-kernel.md` | Accepted at scope | derived constraints |
| Typed occurrence-sensitive identity | `formal-kernel.md` | Accepted at scope | defined |
| Kernel-equivalence = sort-preserving relational isomorphism | `formal-kernel.md` | Accepted at scope | defined |
| Ω admissibility architecture | `admissibility-structure.md` | mixed; `:111` under `ADR-002` | defined + open decision |
| Construct / Differentiate / Restrict | `canonical-terminology.md:21-23` | **shared theory, not FARA** | **excluded from target** |

**Target dependency graph.**

```
candidate primitives (unresolved)
        │  conceptual correspondence only — kernel does not reclassify them
        ▼
carriers ──► typed relations ──► admission constraints
                    │                     │
                    ▼                     ▼
        occurrence-sensitive identity ──► kernel-equivalence (Σ-isomorphism)
                    │
                    ▼
        Ω admissibility architecture (partly open, ADR-002)
```

Formally, the tested target is: **a finite many-sorted relational Σ-structure over a fixed 15-sort, 15-relation signature, satisfying 11 integrity constraints, taken up to Σ-isomorphism.**

## 2–3. Comparison relations and criteria

`R0` lexical · `R1` analogy · `R2` component anticipation · `R3` faithful representation · `R4` derivability · `R5` equivalence at scope · `R6` strict subsumption at scope. `R4` is not inferred from `R3`; `R5` is not inferred from informal mappings; `R6` is not inferred from greater generality.

**Triviality guard applied throughout (Stage 3).** Many-sorted first-order model theory and the relational data model trivially subsume the kernel — the kernel *is* a finite many-sorted relational structure and kernel-equivalence *is* Σ-isomorphism, by definition. This is `R6` in the letter and **theoretically uninformative**: a meta-language encoding arbitrary relational structures subsumes every relational structure. It is recorded and then set aside, exactly as Stage 3 requires.

## 4–6. Search space and serious candidates

Searched across formal logic, proof theory, type theory, category theory, institution theory, universal algebra, algebraic specification, transition systems, SOS, coalgebra, Kripke semantics, constraint systems, argumentation, belief revision, nonmonotonic reasoning, knowledge representation, provenance models, and event semantics. Candidates were prioritized by whether their **native** architecture plausibly covers several kernel components at once.

| Candidate | Native reconstruction, in its own vocabulary |
|---|---|
| **W3C PROV-DM** | Entity, Activity, Agent; `used`, `wasGeneratedBy`, `wasDerivedFrom`, `wasInformedBy`; qualified-influence pattern reifying a relation instance and attaching `hadRole`; Plan; acyclicity constraints in PROV-CONSTRAINTS. Independently motivated by data provenance on the web. |
| **Meseguer general logics (1989), extending Goguen–Burstall institutions (1984/92)** | Signature category; sentence functor; model functor; satisfaction relation invariant under signature morphism; entailment system; proof calculus assigning a proof space to each signature. Independently motivated by the proliferation of specification logics. |
| **Chen ER model (1976)** | Entity sets, relationship sets, relationship instances, roles, cardinality constraints. |
| **Sowa conceptual graphs (1984)** | Finite connected bipartite graph of concept nodes and conceptual-relation nodes; relation nodes are reified relation occurrences with typed arcs. |
| **Neo-Davidsonian event semantics (Davidson 1967; Parsons 1990)** | Event as the sole argument of a predicate; participants attached by thematic-role relations. |
| **Event structures (Nielsen–Plotkin–Winskel 1981)** | `(E, ≤, Con)`: identity-bearing events, causal partial order, consistency sets. |

## 7–9. FARA → candidate mappings, assumptions, recovery

### Strongest single adversary: **W3C PROV-DM**

| Kernel fragment | Image in PROV | Class |
|---|---|---|
| `Event`, event identity distinct under identical extension | `prov:Activity` | **native** |
| `input_state` / `output_state` | `prov:used` / `prov:generated` | **partial** — PROV relates Activity to *Entity*; FARA's `State` is a separate sort with exactly-one-in / exactly-one-out |
| `precedes` acyclic | `wasInformedBy` + PROV-CONSTRAINTS acyclicity | **native** |
| `Provenance`, `provenance_of`, ≥1 per Event | the whole of PROV | **native** |
| `RelationOccurrence`, `instance_of`, `participant(occ, Role, Object)` | qualified-influence pattern with `prov:hadRole` | **native** |
| `Rule`, `applies`, exactly one per Event | `prov:Plan` + qualified association | **partial** — PROV permits an activity with no plan |
| `ReasoningCalculus`, `contains_rule` | collections of Plans | **partial** |
| `Interpretation`, `Meaning`, `assigns(I, R, M)` | — | **absent** |
| `denotes(Representation, Object)` | — | **absent** |
| `Investigation`, `Objective`, `Condition` | — | **absent** (P-Plan extends PROV toward plans but not objectives/conditions) |

**Recovery test.** Given only the PROV-side representation plus declared translation rules, the event/occurrence/role/provenance/order fragment is recoverable up to Σ-isomorphism. **What collapses:** the `State` sort merges into `Entity` unless a typing predicate is added; and the entire semantic layer — `Interpretation`, `Meaning`, `assigns`, `denotes` — has no preimage at all. **PROV reaches `R3` on a proper fragment; it does not reach `R4` on the target.**

### Second adversary: **general logics / institutions**

Covers precisely what PROV lacks — `Interpretation`/`Meaning`/`assigns` via satisfaction, and `ReasoningCalculus`/`Rule` via proof calculus, with calculus-parameterization native (that is the point of an institution). But it has **no event, execution, occurrence, provenance, or trace layer**, and it sits at a different abstraction level: institutions index over signature *categories* and abstract over logical systems, whereas the FARA kernel is a concrete finite structure recording one investigation. Per Stage 6, literal derivation is impossible across that abstraction gap; the strongest legitimate relation is **`R2` component anticipation, plus `R1` analogy for the parameterization pattern.**

### Assumption-independence (Stage 8)

| Assumption needed to push PROV toward `R4` | Class |
|---|---|
| Add a distinguished `State` sort | introduced specifically to reproduce FARA — **weak** |
| Require exactly one Plan per Activity | a restriction not independently studied in PROV — **weak** |
| Add an interpretation/meaning layer | **forced reconstruction** — this is "assume the missing FARA structure" |

The third is decisive and is labelled **forced reconstruction** under Stage 3. No `R4` is claimed for PROV.

## 10–11. Strongest adversary and the strongest counterargument

**Strongest reduction available:** PROV-DM reconstructs the event/occurrence/role/provenance/order fragment at `R3`, faithfully and recoverably, with no forced assumptions on that fragment. This is a substantial proper subset of the kernel — roughly nine of the fifteen relations.

**Strongest counterargument against treating that as subsumption:** the reduction is silent on the semantic layer. `denotes` and `assigns` carry FARA's representation/interpretation architecture, and PROV has no counterpart; supplying one is forced. Symmetrically, the framework that *does* own the semantic layer — general logics — has no trace layer and sits at the wrong abstraction level. **Neither adversary can be repaired into the other without importing the very structure at issue.**

Both are preserved. Neither is discarded.

## 12. Minimal remainder

After the strongest PROV reconstruction, the remainder is:

| Remainder | Classification | Independently necessary, or design choice? |
|---|---|---|
| `Interpretation` / `Meaning` / `assigns` / `denotes` | **theoretically substantive** relative to PROV — but independently anticipated by model-theoretic semantics and institutions, so **not novel** | necessary for a semantics-bearing architecture |
| `Investigation` / `Objective` / `Condition` / `occurs_in` | **representational** — a scoping and indexing device | design choice |
| The 11 admission constraints | **representational** — ordinary integrity constraints expressible in any host | design choice |
| The *conjunction* of semantic, trace, occurrence-identity, and provenance layers under one equivalence relation | **representational**, not shown substantive | design choice on current evidence |

Per Stage 9, none of this is labelled novel merely for being absent from PROV.

## 13–14. Single-framework and multi-framework results

**Single framework: no subsumption at the tested scope**, excluding the trivial model-theoretic case. Best result is `R3` on a proper fragment (PROV).

**Multi-framework:** the union of PROV + institutions/general logics + ER/conceptual-graph reification + event structures covers every kernel component. Classifying per Stage 10:

- Not **A** — no single prior synthesis combining semantics, trace, occurrence identity, and provenance was located.
- Partly **B** — the Semantic Web stack (RDF/OWL model-theoretic semantics + reification + PROV-O + rule languages + named graphs) is an independently established, naturally composed body covering most of the kernel. This is the strongest architectural-reduction evidence found, and it is genuinely non-trivial.
- Not **C** — the components were not retrospectively collected; each was located by its native coverage of multiple kernel fragments before FARA terminology was introduced.

**Verdict: `H6`, with a substantial Stage-10-B component, held jointly with `H3`.**

**Scope correction (recorded 2026-08-10).** `H3` and `H6` are **compatible findings, not mutually exclusive terminal outcomes**. PROV reconstructs a substantial proper fragment (`H3`) *and* the overall architecture still requires multiple prior frameworks (`H6`). Both are asserted together. `H4` and `H5` are not established. `H1` is refuted. `H2` is too weak — the anticipation is not merely componentwise, since PROV covers a connected multi-component fragment.

## 15. Components independently anticipated by prior work

**Scope correction (recorded 2026-08-10).** What follows is **component-level prior-art evidence only**. It does **not** establish prior anticipation of FARA's exact architecture, its dependency structure, the specific combination of components, or its equivalence relation. Stage-12 conclusion 2 is established; conclusion 3 is not.

Every tested component. Reified relation occurrences with roles (Chen 1976; Sowa 1984; Parsons 1990). Identity-bearing events under acyclic causal order (Nielsen–Plotkin–Winskel 1981). Provenance attached to executions (W3C PROV). Interpretation assigning meaning to representations (classical model theory). Calculus-parameterized reasoning with proof calculi (Goguen–Burstall 1984/92; Meseguer 1989). Many-sorted relational structure up to isomorphism (classical model theory; Codd 1970).

## 16–17. Distinctiveness and novelty

**Strongest justified statement about architectural distinctiveness:** at the tested scope, no single independently motivated prior framework was found that natively binds semantic interpretation, execution trace, occurrence identity, and provenance under one equivalence relation. That is a statement about the *conjunction*, and it is bounded by the search performed.

**Strongest justified statement about novelty: not established, in either direction.** This investigation performed formal subsumption analysis, not a historical search. Per Stage 12, conclusions 1–7 do not establish conclusion 8, and failure to establish 1–7 does not prove novelty. No novelty claim is licensed by this record.

## 18. Existing EV claims whose interpretation changes: **none**

Exhaustive audit of all twenty `theory/evaluation/external-systems/*.md` records and the evaluation methodology:

- **Direction tested:** all twenty test only *external system → FAR/FARA*. The methodology's nine questions are uniformly forward-directed ("Does the system fit FAR directly? Does it require a conservative extension? Does it suggest a sixth primitive?"). Zero reverse-direction content.
- **What that direction legitimately supports:** representational coverage at the tested scope, and the absence of an indicated sixth primitive. Nothing more.
- **Does any claim overreach?** **No.** Zero occurrences of novelty, originality, irreducibility, or unprecedentedness across all twenty records and the EV registry. The `conservative extension` classifications claim only that no sixth primitive is indicated — a forward-direction claim that forward evidence supports.
- **Reverse-direction evidence already in the repository:** none located.

**Correction to an earlier framing.** The prioritization report preceding this investigation described the evidence base as exhibiting a "blind spot" and being "confirmation-biased." The exhaustive audit does not support that characterization. The evidence is one-directional, but the claims drawn from it are correspondingly bounded, so **the asymmetry is a scope limitation, not a defect**. No registered claim is downgraded.

## 19–20. Dependencies and unaffected claims

**Dependencies actually demonstrated: none.** No propagation into `OP-01`, `OP-02`, `OP-03`, `OP-09`, `OP-12`, or the terminal UPP result is asserted, because no dependency was proved. Specifically:

- Component anticipation does not bear on primitive *necessity* or *minimality* — those are claims about reducibility among the seven candidates, and prior existence of a component says nothing about whether it is derivable from the other six.
- A broader host framework does not defeat a minimality claim formulated at the kernel level.
- **Subsumption does not imply falsity.** Nothing here falsifies any bounded result.

**Explicitly unaffected:** the terminal UPP theorem and its independently frozen premises; `FARA-FORMAL-KERNEL-001` and its Acceptance; the seven candidate primitives and their unresolved W1 status; every bounded W2–W5, VOC, CORE, FOUNDATION-COMP, and EXPANDED-BOUND result; all CRE and SWE-agent evidence; `UQ-T2`; `OP-02`.

## 21. Quality Gate disposition

**ACCEPT WITH RESTRICTED SCOPE** for the `H6` finding and the Stage-13 audit result. Scope: the Accepted formal kernel at its registered v1.0 finite explicit auditable scope, against the candidate set searched. **INSUFFICIENT EVIDENCE** for any novelty or non-novelty claim. No canonical surface modified.

## 22. Preserved negative and non-discriminating results

- The model-theoretic/relational-model subsumption is real but uninformative; recorded, then set aside under the Stage 3 triviality guard.
- The attempt to push PROV to `R4` failed at forced reconstruction of the semantic layer — preserved as a failed reduction.
- The attempt to use general logics as the single adversary failed on abstraction-level mismatch — preserved, with `R2`+`R1` recorded as the strongest legitimate weaker relation.
- The number of frameworks searched is **not** counted as evidence against subsumption.

## 23. Nonclaims

This investigation does not establish: that FARA is novel or non-novel; that no prior framework outside the searched space subsumes the kernel; that the remainder is theoretically substantive; any primitive necessity, minimality, independence, or completeness result; any change to the terminal theorem. No canonical surface, evaluation record, frozen evidence, or software was modified.
