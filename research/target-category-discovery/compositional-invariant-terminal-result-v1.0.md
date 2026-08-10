# Compositional Invariant Exploratory Research Note v1.0

Status: **Research — exploratory, unregistered derivation**  
Result ID: `TCD-COMPOSITIONAL-INVARIANT-001`  
Repository base: `d1fc8053e1459a7829f6f24b8d187f7887375cf0`

The filename version matches this note’s declared v1.0 identity. The `terminal-result` label is only the artifact type name; this document remains exploratory Research and does not establish a theorem.

## 1. Research question

Within the independently stated class of all small categories, with all functors admitted as recodings, what finitary arrow-valued operations on a fixed finite input graph are invariant under every functor? Do not assume RCCD components.

The original word “broadest” is not itself a mathematical criterion. It requires a comparison order over candidate classes and recoding policies. No such common order has been established.

## 2. Structural setup

A system considered by the exploratory argument has:

- a set of objects and a set of arrows;
- total source and target functions;
- one designated identity arrow for every object;
- one composition value for every and only every composable ordered pair, with the required source and target;
- two-sided unit laws and associativity.

These are the data and laws of a small category. A map preserving them is a functor. RCCD, FARA primitives, audit objectives, observations, failure rules, and preferred decompositions are absent from the premises.

## 3. Preserved exploratory path-classification argument

Let `G` be a finite directed graph with distinguished vertices `s` and `t`, and let `F(G)` be the free category on `G`. A presentation of `G` in a small category `C` is a graph map `x:G->U(C)`, equivalently its unique functorial extension `x_bar:F(G)->C`.

Suppose `alpha` assigns an arrow `alpha_C(x):x(s)->x(t)` to every presentation and is invariant under every functor `H:C->D`:

`H(alpha_C(x)) = alpha_D(H composed with x)`.

The preserved argument evaluates `alpha` on the identity presentation in `F(G)` and sets

`p = alpha_F(G)(eta_G)`.

It then uses naturality with respect to `x_bar` to obtain

`alpha_C(x) = x_bar(p)`.

This suggests that invariant operations in the declared scope are evaluations of fixed paths, with uniqueness tested by the identity presentation. The converse candidate direction is that fixed paths are invariant because functors preserve identities and composition.

This is a historical exploratory derivation. It was not executed under a prospectively registered deductive program, so repository governance does not permit it to be classified as proved or established.

## 4. Nontrivial witness and identity correction

Use the graph `A --a--> B --b--> C` with a second generator `c:A->C`. The free category adds the nonidentity arrow `b∘a:A->C`.

For the distinguished operation shape `A->C`, the two paths are `c` and `b∘a`. No identity arrow has type `A->C`. Identity paths are admissible only when the distinguished source and target coincide, and identities are trivial structural terms rather than nontrivial witnesses.

The bounded executable fixture therefore corroborates sequential composition as the nontrivial witness in this example; it does not establish the general theorem candidate.

## 5. RCCD consequence

The exploratory argument does not derive Construct, Differentiate, Restrict, Resolve, a four-part decomposition, an observation contract, an audit objective, a failure policy, or an Unknown policy. Relabeling category structure with RCCD terms would be post hoc interpretation, not derivation.

## 6. Public claim boundary

- No weakest invariant-supporting structure has been proved.
- No first invariant-supporting structure has been proved.
- No minimal invariant-supporting structure has been proved.
- No globally optimal invariant-supporting structure has been proved.
- Small categories are not claimed to be broader than bare sets under a common comparison order.
- No complete architecture of reasoning is established.
- RCCD is not derived.
- The empirical clean-room program has not been executed.
- Accepted Project FAR theory is unchanged.
- This derivation is exploratory and is not a registered theorem.

## 7. Governance disposition

No corresponding prospective deductive program was frozen before this derivation. Under the Central Research Program, theorem execution requires a new program identifier with independently frozen definitions, explicit terminal outcomes, a finite stopping rule, and a claim-impact policy before execution.

Accordingly, this note preserves the mathematical idea for later falsification and review but does not close the research question, does not establish an internal theorem, and cannot be retroactively promoted by satisfying a later release gate.

## 8. Assurance status

The Python verifier supplies bounded executable corroboration, drift detection, and claim-boundary enforcement. It is not a proof assistant and does not convert CI success into mathematical proof.
