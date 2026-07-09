# T-004 Blind Formalization Raw Appendix

## Execution Metadata

- Artifact: T-004 — Semantic Preservation Theorem
- Execution date: 2026-07-09 UTC
- Executor: Codex CLI, GPT-5.5
- Method: blind formalization from supplied inputs before repository comparison
- Repository access during formalization: prohibited by prompt; repository comparison performed only after this raw output was fixed
- Internet access: not used
- Isolation classification: I1

## Prompt

Formalize T-004 using only the supplied inputs. Do not inspect the repository, Git history, internet, prior reports, downstream theorems, or any material not included below. Treat the listed foundation as accepted. Identify the minimal premises needed to prove or fail the theorem. Return the formalization, proof attempt, dependency assessment, and recommendation. Do not validate T-005 or any downstream theorem.

## Supplied Inputs

Accepted foundation:

- AX-001
- L-001 through L-007
- P-001 through P-005
- T-001
- T-002
- T-003
- Isolation Classification doctrine
- Foundation Validation Consolidation

Candidate theorem:

T-004 — Semantic Preservation Theorem

Statement:

Every interpretation-preserving representation mapping preserves semantic content.

Expanded statement:

Let M be a representation mapping from a source representational structure S1 to a target representational structure S2. If M preserves interpretation for every mapped representation, then M preserves semantic content.

Formal condition:

For every representation r in the domain of M:

Int1(r) = Int2(M(r))

Then:

SemanticContent(Int1, r) = SemanticContent(Int2, M(r))

Available definitions supplied for this exercise:

- Interpretation: a mapping that assigns semantic meaning to representations.
- Semantic content: the meaning assigned to a representation under a specified interpretation.
- Semantic equivalence: representations are semantically equivalent under specified interpretations when they possess the same semantic content under those interpretations.
- Representation mapping: an explicitly specified correspondence between one representational structure and another.

Task restrictions:

- Use Isolation Class I1 unless verified isolation is actually available.
- Do not validate T-005 or any downstream theorem.
- Do not create new axioms, primitives, propositions, or theorems.
- Recommend ACCEPT, REVISE, or REJECT.

## Complete Raw Output

### Formalization

Let S1 and S2 be representational structures. Let M be a representation mapping with domain Dom(M) contained in the representations of S1 and range contained in the representations of S2. Let Int1 be the interpretation applicable to source representations and Int2 be the interpretation applicable to target representations.

Define semantic content extensionally from the supplied definition:

SemanticContent(Int, x) is the meaning assigned to representation x by interpretation Int.

Define interpretation preservation for M relative to Int1 and Int2:

For every r in Dom(M), Int1(r) = Int2(M(r)).

T-004 target conclusion:

For every r in Dom(M), SemanticContent(Int1, r) = SemanticContent(Int2, M(r)).

Equivalently, M preserves semantic content over its mapped domain.

### Proof Attempt

1. Assume r is an arbitrary representation in Dom(M).
2. By interpretation preservation, Int1(r) = Int2(M(r)).
3. By the supplied definition of semantic content, SemanticContent(Int1, r) is the meaning assigned to r by Int1.
4. By the supplied definition of semantic content, SemanticContent(Int2, M(r)) is the meaning assigned to M(r) by Int2.
5. Step 2 states that these assigned meanings are identical for the mapped pair r and M(r).
6. Therefore SemanticContent(Int1, r) = SemanticContent(Int2, M(r)).
7. Because r was arbitrary in Dom(M), the equality holds for every mapped representation.
8. Therefore M preserves semantic content.

### Minimal Dependency Assessment

Logically required:

- Representation mapping: required to supply M and the mapped-domain relation between source and target representations.
- Interpretation: required because the hypothesis is interpretation preservation and because semantic content is assigned under interpretations.
- Semantic content: required because the conclusion is semantic-content preservation.

Informative:

- Semantic equivalence: useful for the corollary that mapped representations are semantically equivalent, but not required to prove semantic-content preservation itself.
- T-003: background assurance that scoped reasoning processes admit FAR representations, but T-004's conditional proof does not require proving that any particular reasoning process has a FAR representation.
- AX-001, L-001 through L-007, P-001 through P-005, T-001, and T-002: accepted foundation background, not direct logical premises for this conditional result.

Historical:

- None identified from supplied inputs.

### Vulnerabilities Noted During Formalization

The theorem is valid only if semantic content is understood extensionally as the meaning assigned by the interpretation. If semantic content included additional context, provenance, pragmatic force, or structural information beyond the interpretation-assigned meaning, the supplied condition might be insufficient. The supplied definitions do not add those extra elements, so this vulnerability does not defeat the theorem under the supplied foundation.

The statement should remain explicitly conditional on mapped representations in the domain of M. It should not imply that unmapped source representations or discarded representations preserve semantic content.

### Recommendation

ACCEPT.

No wording revision is required if the theorem is read with its existing domain restriction and sufficient-condition limitation. A dependency correction may be warranted if repository metadata lists dependencies beyond representation mapping, interpretation, and semantic content as logically required.
