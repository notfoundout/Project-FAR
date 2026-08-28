# PCA-W1 Independent Review — Stage E Controlled Unblinding

Review program: `PCA-W1-INDEPENDENT-REVIEW`  
Immutable target: `14105775daf3c5713b134a728db2e1e53673af97`  
Target tree: `68f058199b7c94b707fd5fe978f1ef59d695ab00`  
Stage-D freeze commit: `c764a3af9b8f69efc6fd59eae0b2bb658ab40aeb`  
Frozen document SHA-256: `e27c99c7ff52f5f95e30e6f163b83cacbfa389d61d6f9408966bf983ce66902e`  
Controlled unblinding completed: 2026-08-28T17:22:39Z

## 1. Gate and preservation record

No internal historical material was opened until the Stage-D verdict file was
committed and its hash was anchored in the separate freeze manifest at commit
`6c142853ba8e2c37363987acc3e98d4476b196d2`.  The frozen document and manifest
were not edited after unblinding.

Stage E does not retroactively call an unblinded result “independent.”  It
instead records three categories:

1. independently reproduced before unblinding;
2. matched or resolved only after unblinding; and
3. not reproduced or irrelevant to the mathematical claims.

## 2. Exact internal access log

These are the substantive internal sources opened during controlled unblinding.
The commit/ref and Git blob identifiers make the reads reproducible.

| Source | Ref / blob | Reason allowed and used |
|---|---|---|
| `theory/theorems/Project-FAR-Theory-Closure-v1.0.md` | target commit / blob `327ac3290a07bf166895fcbdbd9b8ee1ed6e5166` | Recover incorporated definitions/proofs after the freeze; confirm exact image-decoder, Omega, and SSS scopes. |
| `docs/audits/project-far-core-theory-v1.1-correction-audit.md` | target / `0d2013f6b812636d75bb51de631bbca4e34ab644` | Compare independent findings to the prior hostile correction audit. |
| `docs/governance/project-far-theory-closure-acceptance-v1.1.md` | target / `9b20263d858d098e5602ee254fe6ede67bd9deca` | Check what governance accepted and what assurance it expressly did not claim. |
| `docs/research/project-far-core-v1.1-correction-replication-v1.0.md` | target / `4a72c9b60078b36bf781f1b6ed3b98655bd2cfcd` | Compare the independent reconstruction with internal replication. |
| `theory/evaluation/project-far-core-theory-v1.1-regressions.json` | target / `bd92b25c9a24a61aa09b7ea686f10c54fcfd5cc3` | Inspect permanent 004/010 consistency fixtures; not used as proof. |
| Pull request #457 metadata, discussion, changed-file list, and exact patches for the v1.1 monograph, ledger, audit, acceptance, replication, and fixture | merged as target commit `14105775daf3c5713b134a728db2e1e53673af97` | Inspect correction history and discussion only after freeze. |
| `frameworks/FARA/admissibility-structure.md` | target / `f26a77b75cc2e54d6f00a6d432d7fcc44cd6aad9` | Check canonical Omega's declared architectural role and semantic/operational boundary. |
| Pull request #453 metadata, discussion, and changed-file list | merged PR #453; exact theory artifacts read at `c54110490ec4d14b8a85162d020e2426867ab973` | Recover the classes explicitly locked by FAR-CORE-014. |
| `research/independent-dialogue-theory/TERMINAL-REPORT.md` | `c541104...` / `6d59e7541b5ffd1f6f744c6ba5d9b4221cf3b788` | Separate SSS mathematics from the source experiment's unrelated terminal status. |
| `research/independent-dialogue-theory/DIALOGUE-THEORY.md` | `c541104...` / `3331ddb3dd7b75765f284dad512a7717d1cddce2` | Read exact SSS-1/2/3 claims, classes, nonclaims, and falsifiers. |
| `research/independent-dialogue-theory/PROOFS.md` | `c541104...` / `8bb4cde696fbd778a0b6eed42a102d34d71f93e1` | Audit the complete four-decoder lemma, MLL witnesses, and positive factorization proofs. |

The PR #457 discussion contained automated software/repository-consistency
findings about checker phrases, manifest schemas, authority consumers, and status
parsing.  Those were treated only as software consistency history.  They neither
prove nor refute any FAR-CORE claim.  Likewise, no CI result was used as
mathematical evidence.

## 3. Comparison to pre-unblinding findings

| Matter | Frozen independent result | What the internal record disclosed | Classification |
|---|---|---|---|
| Reachable-image decoder for 001/002 | Explicit normalization; whole-codomain edge preserved as an objection | v1.0 defines `d:rho[X]->V^T` and says only the image matters | Independently reconstructed and then textually confirmed |
| FAR-CORE-004 | Constant/injective proof; identity is universally sufficient but not universally minimal | Correction audit, replication, fixture, and PR #457 record the same distinction | Independently reproduced before unblinding |
| FAR-CORE-010 | `T` fixed under Gamma-only change; residue can change; exact witness supplied | Audit, replication, fixture, and PR #457 record the same dependency defect and witness | Independently reproduced before unblinding |
| Blackwell boundary | Primary Blackwell source found from a claim-derived query; uniform decision-problem comparison recognized | Correction audit says v1.0 understated the classical order and disclaims novelty | Independently reproduced, with the name unavoidably disclosed in Stage A |
| FAR-CORE-013 | Generic graph/composition theorem proved; application equation unavailable, so frozen `UNDERDETERMINED` | v1.0 supplies `Omega(z)=Rep(Class_kappa(z))`; FARA spec calls Omega the classification representation/derived view | Missing application premise resolved only after unblinding |
| FAR-CORE-014 | Exact PR-#453 classes locked but unread; proof obligation and hostile out-of-class extension stated; frozen `UNDERDETERMINED` | PR #453 supplies the exact state/transition/decoder classes and explicit proofs/countermodels | Missing application specification resolved only after unblinding |
| Overbroad binary-relation impossibility | Frozen review warned that adding representations/decoders outside the locked class defeats universal promotion | PR #453 history shows an earlier unrestricted binary-relation claim was false and was narrowed after review | Boundary independently anticipated; exact historical countermodel seen only after unblinding |
| Closure necessity | Frozen review proved context closure sufficient but supplied an accidental stable quotient without syntactic closure | v1.0 states only the sufficient direction | Independent strengthening; no conflict |
| Syntactic omission | Frozen review gave a recoverable-omitted-field countermodel and required an attainable fiber collision | v1.0 Theorem 11 uses exactly two same-`x`, different-`c` cases with different outcomes | Independently reconstructed and then confirmed |

The prior internal correction record's substantive 004/010/Blackwell findings
were all independently reproduced.  No correction-audit conclusion had to be
accepted on authority.  The correction audit did not supply the definitions
needed to close 013/014; those were audited directly from their canonical
application sources only after the freeze.

## 4. FAR-CORE-013 after unblinding

The incorporated v1.0 definition states, for complete investigation/calculus
input `z`, calculus `kappa`, and representation map `Rep`,

`Omega(z) = Rep(Class_kappa(z))`.

For every declared resolution rule `r`, therefore,

`r(Omega(z)) = (r o Rep o Class_kappa)(z)`.

This is a direct composition proof: the semantic consequence can be computed
from `z` without treating Omega as an independent semantic primitive.  The
canonical FARA document independently describes Omega as the representation and
record of classifications, not their cause or determinant.

The hostile countermodels from Stage D remain important scope guards:

- the result would fail if equal complete `z` values lawfully admitted different
  consequence-relevant Omega values;
- a stale or corrupted cache is not a canonical derived view;
- a hidden calculus, execution, context, or provenance parameter must be included
  in the complete input when a declared contract observes it; and
- operational usefulness as a cache, audit table, interface, or provenance view
  is not semantic irreducibility.

Within the exact canonical consequence semantics, the missing application
premise is now present and the conditional proof closes.  FAR-CORE-013 changes
from frozen `UNDERDETERMINED` to final `PROVED`.

## 5. FAR-CORE-014 after unblinding

### 5.1 Immutable exact scope

The final evaluation preserves precisely the PR-#453 classes.  It does not
replace them with a looser statement.

| SSS item | State type | Transition representation | Decoder/test class | Exact conclusion |
|---|---|---|---|---|
| SSS-1 | frontier multiset of sequents | binary one-rule expansion relation on frontiers | disjunctive closability recursion | sufficient for any rule system whose derivations use finitary rules |
| SSS-2 | individual sequent | one labelled hyperedge per rule instance, retaining the joint premise family/resource partition | standard AND/OR derivability recursion | sufficient |
| SSS-3 | individual MLL sequent | the unique rule-induced projected binary relation, forgetting rule-instance premise grouping | exactly the uniform monotone successor-truth-set class `D_succ` | insufficient; all four decoders fail |

This is a small representation/decoder taxonomy.  It is not an iff
characterization, not an impossibility for arbitrary binary relations, not a
statement about a state-inspecting decoder, not a primitive operator basis, and
not a universal architecture.

### 5.2 Positive proofs

For SSS-1, a frontier is closable exactly when it is empty or one can choose a
sequent, replace it by the finitely many premises of the last rule in one of its
derivations, and obtain a closable frontier.  The reverse implication applies
that same rule after deriving every premise.  Conjunction is held in the
frontier state rather than discarded by an edge projection.

For SSS-2, a labelled hyperedge is definitionally one complete rule instance.
A conclusion is derivable exactly when some outgoing rule-instance hyperedge has
all premises derivable.  The joint premise family required by AND/OR decoding is
therefore preserved.

Both are exact factorization/descent constructions on the stated state and
transition types.

### 5.3 Negative bounded proof

For SSS-3, the projected representation is fixed to

`S ->_pi P` iff `P` is a premise of some backward MLL rule instance concluding
`S`.

A uniform decoder sees only the set of successor truth values and is monotone,
with the empty set mapped to false.  Its three remaining values must be a
nondecreasing Boolean triple along

`{0} -> {0,1} -> {1}`.

There are exactly four: `TERM=(0,0,0)`, `AND=(0,0,1)`,
`OR=(0,1,1)`, and `NONEMPTY=(1,1,1)`.

The two explicit MLL sequents have the same projected successor truth set
`{0,1}` but different provability:

- `S_or = |- a_perp, a_perp, a tensor b` is unprovable by atom balance, yet
  has a provable successor;
- `S_and = |- a_perp, b_perp, a tensor b` is provable under the matching
  resource split, yet has an unprovable successor under another split.

`TERM` and `AND` fail on `S_and`; `OR` and `NONEMPTY` fail on `S_or`.
Therefore no member of the complete locked decoder class computes MLL
provability from the locked projected relation.

### 5.4 Independent post-unblind computation

The review's own Python reconstruction did not invoke repository tests.  It:

- implemented cut-free unit-free MLL proof search for the witness fragment;
- enumerated all monotone Boolean triples and found exactly the stated four;
- generated every projected tensor-premise successor;
- confirmed `S_or` unprovable and `S_and` provable;
- confirmed both projected successor truth sets are `{0,1}`; and
- assigned a refuting witness to each of the four decoders.

The captured run is `PASS`.  This finite computation is consistency evidence;
the complete class enumeration and displayed proofs carry the mathematical
burden.

Within the immutable PR-#453-bounded scope, FAR-CORE-014 changes from frozen
`UNDERDETERMINED` to final `PROVED`.

## 6. Stage-D-to-final verdict transition

All claim rows use only the required five-term vocabulary.

| Claim(s) | Frozen Stage D | Final after controlled unblinding | Reason for any change |
|---|---|---|---|
| FAR-CORE-001–012 | PROVED | PROVED | Incorporated v1.0 definitions confirm the reconstructed scopes; no in-scope countermodel appeared. |
| FAR-CORE-013 | UNDERDETERMINED | PROVED | Canonical Omega composition equation and exact semantic scope became available. |
| FAR-CORE-014 | UNDERDETERMINED | PROVED | Exact locked classes, exhaustive four-decoder proof, positive constructions, and falsifiers became available and survived independent checking. |
| Full 14-claim bundle | UNDERDETERMINED | PROVED | Both missing application premises were resolved without changing any frozen mathematical judgment. |

The repository's `SUPPORTED/DERIVED` label for FAR-CORE-014 remains a
governance/evidence-provenance label in the historical machine ledger.  It is not
a sixth truth verdict and is not rewritten by this review.  Under the user's
truth-verdict vocabulary, the exact bounded proposition is `PROVED`.

PR #453's source experiment also used historical statuses such as `BLOCKED`,
`FRAGMENTED`, and `THEORY UNRESOLVED` for its separate retrieval/common-theory
experiment.  Those labels are not about SSS's three displayed mathematical
results and are not imported into any FAR-CORE claim row.

## 7. Final objections and scope guards

The following objections survive the positive verdict and are mandatory when
the theory is cited or implemented:

1. FAR-CORE-001/002 are extensional image-level theorems.  No arbitrary behavior
   on unreachable representation labels, computability, measurability, or
   efficiency follows.
2. FAR-CORE-003's closure construction is sufficient, not syntactically
   necessary in every accidental action-stable system.
3. FAR-CORE-004 concerns simultaneous least-informativeness over varying
   contracts.  Identity remains universally sufficient on fixed `X`.
4. FAR-CORE-006 proves non-entailment from underlying-set codes.  Stronger
   homomorphism/interpretation premises can establish genuine common structure.
5. FAR-CORE-007/008 depend on admitting reification, tags, tuple domains, and
   decoders; fixed languages and cost/complexity constraints can restore useful
   counts.
6. FAR-CORE-009 denies bare logical entailment from a proper finite panel, not
   probabilistic or deductive generalization under extra assumptions.
7. FAR-CORE-010's residue is not necessarily deductively closed, and empty-index
   and cross-language comparisons need explicit conventions/translations.
8. FAR-CORE-011 requires an attainable behavior collision inside a retained
   representation fiber, not mere syntactic omission.
9. FAR-CORE-012 is conditional on a distinguishing contract and reachable
   absence/Unknown states.
10. FAR-CORE-013 is semantic eliminability under the canonical complete-input
    definition, not a claim that materialization/provenance has no operational
    value.
11. FAR-CORE-014 remains exactly the three PR-#453 indexed results above.  It is
    not an unrestricted binary-relation impossibility, not a universal proof
    search architecture, and not a novelty claim.

## 8. Prior-art disposition after unblinding

The internal v1.0 bibliography contains several sources also found or paralleled
by the independent search, but it was not seen until after the corpus and
verdict freeze.  The independent corpus establishes that the core mathematical
patterns have extensive predecessors in quotient/coalgebra theory, statistical
sufficiency and Blackwell comparison, transformation-group invariants,
structure-preserving morphisms, definitional/Morita equivalence, learning
theory, abstract interpretation, view determinacy, database null semantics, MDP
homomorphisms, and predictive-state representations.

Accordingly:

- no novelty or priority claim is certified for FAR-CORE-001–014;
- the exact phrase search for “Search-State Sufficiency” finding no relevant
  scholarly result is only a negative search result, not novelty proof;
- the Project FAR synthesis/governance/application framing was not subjected to
  a legal-patent novelty analysis; and
- literature agreement is neither proof nor a substitute for the explicit
  arguments audited here.

## 9. Stage-E terminal result

Every FAR-CORE-001–014 proposition is `PROVED` under its exact declared scope.
No claim is `REFUTED`, `OPEN`, `UNDERDETERMINED`, or `NOT APPLICABLE` after
controlled unblinding.  The full reviewed bundle's final truth verdict is
`PROVED`, subject to every scope guard above and without a novelty claim.
