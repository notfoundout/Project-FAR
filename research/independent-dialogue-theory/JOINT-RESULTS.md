# W-star, joint profiles, frames, common content, and prior art

This is the human-readable report for `W-STAR.json`. It belongs to
`E1-transparent-source-recovery`; no result here is retrofitted into frozen E0.

## 1. Cell matrix and budget movement

The matrix contains every one of the $11\times88=968$ target/item cells. An unreached
secondary cell is explicitly `OPEN`, never blank and never `NO`.

| Stratum | Population | B1 YES / NO / OPEN | B2 YES / NO / OPEN |
|---|---:|---:|---:|
| mandatory S1/S2 × U0 | 176 | 20 / 0 / 156 | 20 / 0 / 156 |
| secondary S3–S11 × U0 | 792 | 9 / 0 / 783 | 39 / 0 / 753 |
| **global** | **968** | **29 / 0 / 939** | **59 / 0 / 909** |

The first 100 secondary cells were reached at B1 and the first 400 at B2 under the E1 seed
recorded in `PROTOCOL-SUCCESSOR.md`. Movement was **30 OPEN→YES, 0 OPEN→NO**. All 30 were
literal own-source items first reached between ranks 101 and 400. No sampled secondary result
is used for a maximality claim.

Every YES record names a grammar, profile, uniform schema, $E$-factorization, $O$-respect, and
Ax check. No NO was asserted because no impossibility proof met the frozen burden. The OPEN
count is therefore a result, not an invitation to treat absence of a witness as failure.

## 2. Both frozen arms

| Arm | Fragments | JOINT-YES | JOINT-NO | JOINT-OPEN |
|---|---:|---:|---:|---:|
| dialogue-derived calibration: $c_0$ and $c_0+u$ | 89 | 3 | 0 | 86 |
| native-registry singleton: $\{u\}$ | 88 | 2 | 0 | 86 |

The only source-registry extensions certified on both S1 and S2 are:

- `u058`: Plotkin's configuration carrier, interpreted as the frozen native state carrier;
- `u059`: Plotkin's binary transition relation, interpreted as the frozen arrow.

They are retained as distinct source items even though their interpretations coincide with
parts of $c_0$ at this resolution. This is extensional coincidence, not an identity finding.

## 3. Joint profiles and $J^\ast$

`W-STAR.json` contains **all profiles actually certified**:

| Profile | Fragment(s) | Grammar | Interpretation |
|---|---|---|---|
| `J0` | $c_0$ | G1 | S1 frontier expansion / S2 non-stuttering propagator application |
| `J-u058` | $c_0+u058$, native `u058` | G2 | configuration = native state carrier |
| `J-u059` | $c_0+u059$, native `u059` | G2 | transition = frozen arrow |
| `J-star` | $c_0+u058+u059$ | G2 | both aliases simultaneously |

$J^\ast=$ `J-star` is the **maximal certified profile**, not a proof of mathematical
maximality. The protocol defines the full profile class as possibly infinite; no fragment is
JOINT-COMPLETE. Claiming to enumerate “all mathematical joint profiles” would violate the
protocol, so the exact result is: all *certified* profiles are listed, and completeness is
OPEN.

## 4. Maximal witnessed fragment and failure frontiers

At B2:

$$J^\ast\text{ witnesses }c^\ast=c_0+u058+u059.$$

For the frozen one-step extension family around $c_0$:

- proved failure frontier $\partial_1(c_0)=\varnothing$ (there are no JOINT-NO proofs);
- witness-extension frontier $=\{u058,u059\}$;
- OPEN frontier $\partial_1^{OPEN}(c_0)=U0\setminus\{u058,u059\}$, of size **86**.

Therefore $c^\ast$ is the **maximal witnessed fragment among established certificates**. It is
not a maximal jointly interpretable fragment, and no complete failure frontier exists. The
86-item OPEN frontier is the exact reason maximality remains UNRESOLVED.

## 5. Frames, generated before theory

`FRAMES.json` was sealed at SHA-256
`66b7810a51e476e5101be12bfcdde43f182e999f5d5e3107e3a524faa0467047` before the computations
below. Its six frames contain only translated constitutive definitions, forced typing, and host
equality/congruence. In particular, none contains irreflexivity, termination, acyclicity, or a
law inserted because it happens to hold in the targets.

For $c_0$, this reproduces the frozen nonlogical frame $\Gamma_{c_0}=\varnothing$. The alias
extensions add only sort/relation identifications and typing; they do not constrain the binary
relation.

## 6. Common theories and substantive content

Let $\varphi_{irr}=\forall x\,\neg(x\to x)$. The existing source-checked proof in
`PROOFS.md` establishes it for every S1 instance under `K1-LM-frontier-multiset`; the frozen S2
arrow explicitly omits $p(D)=D$. Hence:

| Fragment/profile | Certified theory result | Content beyond frame |
|---|---|---|
| $c_0$/`J0` | $Cn(\Gamma\cup\{\varphi_{irr}\})\subseteq\mathcal T$ | **YES** |
| $c_0+u058$/`J-u058` | same lower bound | **YES** |
| $c_0+u059$/`J-u059` | same lower bound, with relation alias | **YES** |
| $c^\ast$/`J-star` | same lower bound, with both aliases | **YES** |
| native `u058` | logical/typing consequences only established | **NO substantive sentence certified** |
| native `u059` | $Cn(\Gamma\cup\{\varphi_{irr}\})\subseteq\mathcal T$ | **YES** |

The content test is strict: a one-element structure with a reflexive self-loop satisfies each
relevant interface frame but falsifies $\varphi_{irr}$. Thus $\varphi_{irr}\notin Cn(\Gamma)$.
This falsifies preregistered A2 at `J0`, as already recorded.

These are **lower bounds**, not exact common theories. Exact $\mathcal T$, robust
$\mathcal T^{rob}$, and profile independence remain UNRESOLVED because no JOINT-COMPLETE proof
exists and the list-with-exchange S1 profile remains open. No finite-panel result is promoted
to a class theorem.

## 7. Conditional rank, irreducibility, minimality, and bases

Substantive content survives, so the conditional gate opens—but only for the certified kernel

$$\mathcal K_{irr}=Cn_\Gamma(\{\varphi_{irr}\}).$$

| Question | Exact answer for $\mathcal K_{irr}$ | Scope limit |
|---|---|---|
| rank | **1** over $\Gamma$ | rank of the full unknown common theory is UNRESOLVED |
| irreducibility | **YES** | semantic, modulo $\Gamma$ |
| inclusion minimality | **YES** | removing the sole generator leaves the frame |
| independence witness | one-state reflexive frame model | satisfies $\Gamma$, falsifies $\varphi_{irr}$ |
| alternative bases | every singleton $\{\psi\}$ with $\Gamma\vdash\psi\leftrightarrow\varphi_{irr}$ | infinitely many syntactic variants; one semantic equivalence class |

No uniqueness of presentation is claimed. Adding tautological conjuncts produces infinitely
many syntactic bases; none supplies a second independent semantic generator. Nothing in this
table answers rank or minimality for the exact, still-unknown common theory.

## 8. PI0-BIB-v1 translation and subsumption tests

The eleven newly recovered documents plus the two held documents cover all twelve labels
(thirteen document bodies). Each body was identity-checked, hashed, and inspected. The test
object is only the surviving kernel $\varphi_{irr}$.

| Label / bodies | Result for $\varphi_{irr}$ |
|---|---|
| 1 Goguen–Burstall institutions | OPEN: no outcome-independent canonical directed-step translation certified |
| 2 Rabe–Kohlhase MMT | OPEN: theory morphisms do not fix the required state/step interpretation |
| 3 Wille FCA; Gupta Chu spaces | OPEN for the label; order/transform candidates are non-unique |
| 4 Lawvere adjointness | OPEN: no canonical arrow-as-step profile |
| 5 Fritz Markov categories | OPEN overall; categorical identity arrows make the obvious reachability candidate reflexive, so that candidate does not subsume irreflexivity |
| 6 Effectus theory | OPEN overall for the same translation non-uniqueness |
| 7 Cockett–Lack restriction categories | OPEN overall; identity/restriction structure does not entail irreflexive step |
| 8 Cousot–Cousot abstract interpretation | the canonical approximation relation is a preorder and hence reflexive; that direct candidate **fails to subsume** $\varphi_{irr}$ |
| 9 Pearl causal hierarchy | OPEN: no single canonical binary step language is fixed |
| 10 Coecke–Fritz–Spekkens resource theory | convertibility is reflexive under identity processes; that direct candidate **fails to subsume** $\varphi_{irr}$ |
| 11 Jacobs–Rutten (co)algebras | OPEN: coalgebraic transition/bisimulation choices are not unique |
| 12 Meseguer rewriting logic | reflexive-transitive reachability fails to subsume; a one-step rewrite translation remains OPEN |

At least one PI0 translation is OPEN. By the frozen rule, the exact prior-art verdict is

$$\boxed{\textbf{NOVELTY UNRESOLVED — NEVER POSITIVE}}.$$

The narrower statement “no inspected canonical candidate certified subsumption” is only a
bounded search result, not a novelty claim.

## 9. C1–C12 content tests

The sole substantive candidate was run through the fixed registry:

| Test | Disposition |
|---|---|
| C1 Galois antitonicity | fails to defeat; no antitone operator occurs in the kernel |
| C2 van Glabbeek spectrum | **narrows**: transition semantics is profile-indexed; no spectrum-invariant claim |
| C3 dense factorization | fails to defeat; no factorization claim |
| C4 idempotent monoid | fails to defeat; no monoid operation |
| C5 NAND vs. $\{\neg,\wedge\}$ | **exposes presentation dependence**; alternative bases are reported modulo equivalence |
| C6 Janov–Mučnik | **narrows**: no finite-basis claim for the full common theory |
| C7 Markov non-naturality of $\Delta$ | fails to defeat; no copying/naturality claim |
| C8 $R_P$ nonconstant | fails to defeat; no $R_P$ claim |
| C9 $d_P$ not from $\Delta$ | fails to defeat; no $d_P$ claim |
| C10 $P(y\mid x)\ne P(y\mid do(x))$ | fails to defeat; no observational/interventional identification |
| C11 Boolean $d_P$ | fails to defeat; no Boolean decomposition claim |
| C12 $\sqsubseteq$ failure | fails to defeat; no universal approximation-order claim |

No registry test refutes irreflexivity at the certified profile. C2, C5, and C6 materially
limit what may be inferred from it.

## 10. Result in one line

E1 reaches a small, profile-relative, substantive kernel and two source-registry aliases, but
not an exact robust theory, a proved maximal language, a failure frontier containing any NO,
or a positive prior-art result. The mathematically honest successor classification is
**FRAGMENTED**; the dialogue-built theory as a whole remains **THEORY UNRESOLVED**.

