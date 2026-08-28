# PCA-W1 Stage B — machine-ledger reconciliation

Status: **STAGE B RECORDED; EXTERNAL CORPUS STILL EMPTY**

The Stage-A reconstruction was committed before the first read of the machine ledger. This record compares rather than rewrites it.

## 1. Ledger integrity and direct premises

Pinned ledger:

`theory/terminal/project-far-core-theory-v1.1.json@14105775daf3c5713b134a728db2e1e53673af97`

The exact fetched bytes hash to:

`66372644e5a2fe65c93f7e893e41eae74211934f92827cadcfe28dd81290ab40`

This matches the review protocol.

The ledger declares these global premises:

1. set presentation;
2. explicit totalized semantics;
3. fixed-contract evaluation;
4. extensional exactness; and
5. declared invariance.

They narrow the core to exact, extensional, Set-based claims. They do not by themselves supply a decoder on unreachable codomain values, an effective/computable decoder, a metric for approximation, or the application definitions referenced by claims 013 and 014.

## 2. Reconciliation table

| Claim | Exact ledger claim/scope (compressed without changing substance) | Stage-A match | Reconciliation |
|---|---|---|---|
| FAR-CORE-001 | Exact sufficiency iff behavior factors through representation; any Set-based exact contract | Match | Retain image-level factorization proof. Whole-codomain total decoder remains a scope ambiguity unless totalization includes an extension premise. |
| FAR-CORE-002 | Observational quotient uniquely least-informative up to isomorphism; any Set-based exact contract; cardinal minimum when finite | Match with omitted qualifier | Stage A proved image-level uniqueness generally. Ledger only expressly adds cardinal minimum in finite cases; do not silently broaden that cardinal subclaim. |
| FAR-CORE-003 | Context closure makes observational equivalence action-compatible; declared action/test closure | Match | Stage A correctly treated closure as a sufficient hypothesis, not literal necessity in every accidental system. |
| FAR-CORE-004 | No one representation is simultaneously least-informative sufficient for every varying contract on a nontrivial domain; universal sufficiency not denied | Exact match | No change. |
| FAR-CORE-005 | Invariants are antitone in nested admitted transformation classes | Partial/general match | Stage A gave the broader relativity principle but did not state antitonicity explicitly. Exact theorem reconstructed below. |
| FAR-CORE-006 | Unconstrained encoding establishes host capacity, not native common structure; injective transport with decoder | **Material mismatch** | Stage A provisionally assigned a sufficiency-transport theorem. Replace only for post-reconciliation analysis with the exact non-entailment schema below; preserve mismatch as evidence. |
| FAR-CORE-007 | Primitive vocabulary count noninvariant; faithful reification/tagging | Match | Product/tag reification witness is within the ledger scope, subject to exact admitted regime. |
| FAR-CORE-008 | Finite operator count noninvariant; finite operator family with tagged tuples | Match | Dispatcher witness is within scope. |
| FAR-CORE-009 | Proper finite subset does not establish universality over an open domain | Match | Preserve coverage-theorem boundary. |
| FAR-CORE-010 | Exact common theory relative to `L,J,I`; residue additionally to `Γ`; fixed language/models/target | Exact match | No change; retain empty-index, translation, and residue-not-closed qualifications. |
| FAR-CORE-011 | Omitting consequence-affecting parameter refutes sufficiency; any exact contract | Match | “Consequence-affecting” must entail an attainable behavioral collision or equivalent no-decoder proof. |
| FAR-CORE-012 | Contracts distinguishing absence from Unknown require sufficient representations to preserve it | Match | Exact contract-conditional scope preserved. |
| FAR-CORE-013 | `Ω` is semantically eliminable derived materialized view; canonical FARA definition of `Ω` | Conditional match, application premise missing | Stage A proved the graph/projection theorem but the allowed v1.1 monograph and ledger do not state the canonical definition needed to instantiate it. |
| FAR-CORE-014 | Search-State Sufficiency is a bounded factorization instance, not universal; only PR #453's stated representation and decoder classes; ledger status supported/derived | Scope sharpened | Preserve this exact PR-#453-bounded scope. Do not promote to an open domain, universal architecture, theorem about other classes, or `PROVED` merely from the ledger label. |

## 3. Exact post-reconciliation reconstruction of FAR-CORE-005

Let `G⊆H` be nested admitted classes of transformations on a common universe of presentations. Let

`Inv(G)={P | P is preserved by every transformation in G}`.

Then

`Inv(H)⊆Inv(G)`.

**Proof.** If `P` is preserved by every member of `H`, it is preserved by every member of its subset `G`. Thus enlarging the transformation class can only remove (or retain), never add, invariants. Equality can occur; strict antitonicity is not claimed.

**Required typing.** The two classes must act on compatible objects and “preserved” must use the same predicate/transport semantics. For arbitrary unrelated classes, “nested” has no meaning. Empty and identity-only classes produce the expected vacuous boundary.

## 4. Exact post-reconciliation reconstruction of FAR-CORE-006

Let source sets/structures `S_i` admit injective encodings `e_i:S_i→H` into a host and decoders `d_i:e_i(S_i)→S_i` with `d_i∘e_i=id`. These hypotheses prove that `H` has enough set-level capacity to carry lossless codes for each source.

They do **not** entail that the sources share any specified native operation, relation, axiom, primitive vocabulary, or semantics. The same set encodings and decoders remain valid while the source structures are varied arbitrarily. For example, a two-element group and a two-element left-zero semigroup can use identical element codes in the same host; lossless coding does not make their binary operations the same or make the host operation a homomorphic image of both.

Therefore the valid conclusion is a non-entailment:

`injective encoding + decoder ⊬ native common structure`

unless added premises declare a common signature and require homomorphism, interpretation, definitional equivalence, or other structure-preserving transport.

**Scope objection carried forward.** “Native common structure” is not formally defined in the v1.1 monograph or ledger. The non-entailment is rigorous for every specified structural conclusion absent preservation premises, but a positive classification of what counts as native requires a signature/category/semantics. External prior-art search will test this boundary.

## 5. FAR-CORE-014 scope lock

The exact scope to carry into every subsequent table is:

> only the representation and decoder classes stated in PR #453; a bounded supported/derived Search-State Sufficiency factorization instance; not a universal architecture.

Before controlled unblinding, PR #453 itself remains unread. Accordingly:

- no assumption is made about the number of cases, fields, operators, empirical records, or decoder implementation;
- no repository check is treated as proof;
- no claim is made outside those stated classes; and
- the application claim cannot receive a proof verdict unless the exact factorization evidence is available in an allowed source.

## 6. Stage-B mismatch consequences

The one material blind-allocation error, FAR-CORE-006, does not contaminate the other reconstructions: the mistakenly reconstructed transport theorem is a useful lemma but is not the ledger claim. FAR-CORE-005 was directionally correct but less exact than the antitone set-inclusion theorem. FAR-CORE-013 and FAR-CORE-014 remain incompletely auditable because their operative application definitions/evidence are referenced but not present in the two governing target artifacts allowed before unblinding.

No Stage-D verdict is frozen here.
