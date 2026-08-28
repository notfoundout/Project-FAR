# Theorem and Proof-Status Register

Status: **Accepted current assurance register**

Current governing theory: `PROJECT-FAR-CORE-THEORY-1.1`.

| Claim family | Current status | Assurance and boundary |
|---|---|---|
| `FAR-CORE-001` exact factorization | **Proved** | Explicit narrative proof; internal deductive, not proof-assistant checked or independently reviewed. |
| `FAR-CORE-002` observational quotient | **Proved** | Explicit construction/universality proof; information minimality only. |
| `FAR-CORE-003` dynamic descent | **Proved** | Requires declared context/test closure. |
| `FAR-CORE-004` no contract-free minimum | **Proved negative; clarified in v1.1** | No single representation is simultaneously least-informative sufficient for every observation contract on a nontrivial domain. The identity representation may still be sufficient for all contracts on fixed `X`. |
| `FAR-CORE-005`–`008` invariance/transport/noninvariance | **Proved** | Explicit set-theoretic inclusions and reification/tagging constructions. |
| `FAR-CORE-009` finite-panel boundary | **Proved** | Requires a proper finite subset of an open domain. |
| `FAR-CORE-010` common theory/residue | **Proved; corrected in v1.1** | Exact `T_{L,J,I}` depends directly on language, interpretation profiles/models, and target class; the frame-subtracted residue additionally depends on `Γ`. |
| `FAR-CORE-011`–`013` parameter/typed-outcome/Ω results | **Proved** | Exact contracts; Ω result uses the current canonical definition. |
| `FAR-CORE-014` SSS classification | **Supported/derived; unchanged** | Depends on the merged PR #453 bounded proofs and stated decoder classes. |
| Historical `PROJECT-FAR-CORE-THEORY-1.0` | **Superseded as current authority; preserved** | Byte-identical v1.0 monograph retained at SHA-256 `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`. |
| Historical terminal UPP theorem | **Not established by frozen derivation** | Proposition not refuted; defects `XA-001`–`XA-005`; historical artifacts preserved. |
| `FARA-FORMAL-KERNEL-001` | Accepted bounded specification/engineering result | Finite explicit auditable v1 target; not a global primitive/minimality theorem. |
| Empirical and executable campaigns | Observations or bounded corroboration | Never proofs of the core or open-domain universality. |

The hostile W1 audit that triggered v1.1 is **not independent validation**. `PCA-W1-INDEPENDENT-REVIEW` remains open. Independent review and proof-assistant reconstruction remain open assurance dimensions under `POST-CLOSURE-001`; their absence limits assurance, not the surviving terminal kernel.

## Historical pre-closure entries

The following text preserves the earlier register at its evidence cutoff. Its broader unresolved labels are superseded where the current table gives a terminal disposition.

Status: **Accepted classification index; proof objects remain authoritative**

| Family | Status | Exact boundary |
|---|---|---|
| Definitions and framework “principles” | specification/assumption, not proof | Naming or stability does not establish necessity. |
| Legacy root-theory limits “theorem” | historical proof attempt | Filename is retained for provenance; no global theorem status follows. |
| FARA representation/minimality claims | conjecture or bounded evaluation | Global proof absent; counterexample search remains open. |
| FARA W1 primitive independence | completed fail-closed execution; no theorem | All seven candidate primitives are unresolved because no canonical formal theory, model class, scope/objective, or equivalence relation supports a derivation or countermodel. |
| T-/L-/P-series records | status declared in their validation reports | Assurance and premises must travel with each statement. |
| Terminal UPP theorem | bounded theorem claim with mixed assurance; registered derivation found defective by the 2026-08-13 internal cross-audit | Relative to frozen class/contract/closure/equivalence premises; composition is not one kernel-checked object. **2026-08-13:** the three-lane cross-audit adjudicated `FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED` for frozen source `f6645a77` — the terminal proposition is not refuted, but the frozen derivation does not establish it over its stated domain (`XA-001`–`XA-005`; W9 empty-dependency countermodel `CE-UPP-W9-001`, unpropagated W8/W11 side conditions, status-level composition). See `docs/audits/bounded-v1-three-lane-cross-audit-adjudication-v1.0.md`. Internal model-assisted evidence; not independent validation. |
| CRE/EV/SWE-agent results | empirical observations | Never theorems and never proofs of universality. |
| Construct/Differentiate/Restrict sufficiency or irreducibility | unresolved conjecture outside registered scope | Bounded reconstruction/ablation does not prove global minimality. |
| FARA-OPS-W2-001 | coordinate-separation-induced bounded result; executable corroboration | Joint sufficiency and individual irreducibility hold only because `finite_coordinate_trace_v1` assigns each operator exclusive control of one observable coordinate under componentwise equality. This does not establish canonical or global operator necessity. |
| FARA-ARCH-W3-001 | bounded representational existence result plus counterexample; executable validation | CTC reconstruction is established by construction only for `B_W3_closed_explicit`; uniqueness and internal-state-only lossless universality are refuted. No necessity, minimality, native-architecture, or open-world theorem follows. |
| THM-REP-001 / FARA-W4-PROOF-001 | bounded sufficient condition; executable corroboration, not proof-assistant verification | Finite explicit typed archives have an inverse under the frozen W4 contract; collision counterexamples establish failures outside it. No universal representation theorem follows. |
| THM-INV-001 / FARA-W5-PROOF-001 | unresolved global result with two bounded invariant witnesses; executable corroboration, not proof-assistant verification | Two finite admissible pairs agree. Every attempted negative pair is lossy, unrecoverable, unavailable, hidden-machinery dependent, or circular; therefore no admissible representation-sensitive counterexample and no representation-independence theorem is established. |

Any active canonical use of “theorem”, “lemma”, “proposition”, “proof”, or “derivation” must identify a statement/record and its status or link here/its proof record. Illustrations and semantic similarities are not derivations.

| THM-VOC-001 / FARA-VOC-PROOF-001 | bounded executable insufficiency/extension-pressure evidence | The seven candidate primitives do not expose several family-specific operational roles under the frozen interpretation; no universal insufficiency, minimality, necessity, or globally primitive extension follows. |
| FARA-CORE-PROOF-001 | bounded executable specification/consistency evidence; not a theorem | The selected finite many-sorted target has an acyclic dependency graph and bounded countermodels, while three non-equivalent coherent foundations remain. Original W1 adjudications remain unresolved. |
| FARA-FOUNDATION-COMP-PROOF-001 | bounded executable comparison evidence; not a theorem | Fifty-seven translations and reconstructions, three paired non-equivalence witnesses, 21 ablations, and direction-aware Pareto recomputation establish many-sorted relational → algebraic/state-transition while typed hypergraph remains incomparable with many-sorted relational. No global or canonical selection follows. |
| FARA-EXPANDED-BOUND-001 | bounded executable Research evidence; not a theorem | Every unary and binary relation interpretation on independent axes over carriers 0..4 was materially constructed and evaluated (66,098 executions). Thirty independently revalidated paired-reduct witnesses support only recorded target-specific bounds: 1..4 for Object, Property, Relation, Representation, and Interpretation; 0..4 for Investigation and Reasoning Calculus. No full-signature, unbounded, global, or independent-replication result follows. |

<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: start -->
- Mapping totals (Pass/Partial/Fail/Unknown): `{"algebraic-state-transition":{"Fail":4,"Partial":0,"Pass":12,"Unknown":3},"many-sorted-relational":{"Fail":3,"Partial":0,"Pass":13,"Unknown":3},"typed-hypergraph":{"Fail":0,"Partial":0,"Pass":16,"Unknown":3}}`
- Dominance edges: `[["many-sorted-relational","algebraic-state-transition"]]`
- Terminal result: **multiple foundations remain Pareto-incomparable**
- Nonclaims: `["canonical uniqueness","global superiority","universal representation","global minimality","primitive necessity","completeness","universality"]`
- Remaining obligations: `["independent replication","nonfinite continuous semantics","environment-inclusive embodied semantics","live-oracle semantics","neutral external benchmark corpus","complete old prose source-model class"]`
<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: end -->

The expanded campaign proof, trace summaries, cost accounting, immutable base identities, target-specific coverage, and mutation checks are machine validated. They do not create a theorem.
