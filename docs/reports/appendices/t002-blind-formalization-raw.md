# T-002 Blind Formalization Raw Appendix

## Execution Metadata

- Artifact: T-002 — Conditional Primitive Independence
- Execution date: 2026-07-09
- Executor: Codex research executor
- Isolation classification: I1 — Claimed Isolation
- Repository access during blind step: Prohibited by prompt; not technically enforced by environment
- Technical limitation: The environment cannot independently verify that repository artifacts were inaccessible.

## Prompt

Formalize T-002 using only the supplied inputs. Do not inspect repository files. Determine whether the result follows, identify the proof standard required, identify logical dependencies, and state any limitations or required revisions.

## Supplied Inputs

Accepted foundation:

- Current AX-001.
- Accepted L-001 through L-007.
- Accepted P-001.
- Accepted T-001 in revised form: for each primitive in the current primitive architecture, removing that primitive without supplying an accepted replacement reduces expressive power relative to representing reasoning processes within current Project FAR scope; therefore the architecture is minimal relative to current scope, definitions, axioms, and deletion-only compression standard.
- Foundation validation consolidation report.
- Isolation Classification doctrine.

Candidate T-002 statement:

No current primitive is derivable from the other four without loss of expressive power under the current Project FAR reduction standard. Therefore the current primitive architecture is mutually independent relative to the present reduction standard.

Candidate primitive list:

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

Declared candidate dependencies:

- Canonical definitions
- Canonical axioms
- T-001
- L-001 through L-005

## Complete Raw Output

Formalization attempt:

Let P = {I, R, S, M, C}, where I is Investigation, R is Representation, S is Representational Structure, M is Interpretation, and C is Reasoning Calculus.

The accepted T-001 result gives a deletion-only minimality claim: for every p in P, deleting p from P without supplying an accepted replacement reduces expressive power relative to the Project FAR objective.

To derive T-002 as stated, one must show more than deletion-only minimality if the phrase “derivable from the other four” is read literally. Underivability normally means no definition, construction, or theorem using the other four can recover p. The supplied foundation does not establish that absolute underivability claim. It establishes that simply retaining the other four while deleting p does not preserve the expressive role required by the current axioms and lemmas.

A valid theorem is available in a narrower form:

For every p in P, p is not eliminable in favor of P \ {p} by deletion-only reduction without loss of expressive power, unless an accepted replacement for p is supplied. Equivalently, P is deletion-independent relative to the current Project FAR reduction standard.

Proof sketch under the narrower formulation:

1. Representation case. By L-001 and P-001, scoped FAR reasoning satisfying the representation condition requires explicit representations. A system retaining investigation, structure, interpretation, and calculus but deleting representation lacks the explicit objects to be structured, interpreted, or transformed. Repair requires reintroducing representations or an accepted replacement. Therefore representation is not deletion-eliminable in favor of the other four.

2. Representational Structure case. By L-002, a participating collection of representations satisfying the structure condition requires structure. A system retaining investigation, representation, interpretation, and calculus but deleting structure lacks explicit relations needed for ordering, dependency, support, contradiction, transition organization, or role connection. Repair requires reintroducing structure or an accepted replacement. Therefore representational structure is not deletion-eliminable in favor of the other four.

3. Interpretation case. By L-003, participating representations satisfying the interpretation condition require interpretation. A system retaining investigation, representation, structure, and calculus but deleting interpretation has formal marks and relations without assigned meaning or semantic role. Repair requires reintroducing interpretation or an accepted replacement. Therefore interpretation is not deletion-eliminable in favor of the other four.

4. Investigation case. By L-004, scoped reasoning processes satisfying the investigation condition require an investigation. A system retaining representation, structure, interpretation, and calculus but deleting investigation lacks objective, scope, governing question, or resolution conditions. Repair requires reintroducing investigation or an accepted replacement. Therefore investigation is not deletion-eliminable in favor of the other four.

5. Reasoning Calculus case. By L-005, scoped reasoning processes satisfying the calculus condition require admissible reasoning transitions. A system retaining investigation, representation, structure, and interpretation but deleting calculus cannot distinguish admissible from inadmissible transitions. Repair requires reintroducing reasoning calculus or an accepted replacement. Therefore reasoning calculus is not deletion-eliminable in favor of the other four.

Combining the five cases yields deletion-independence of the five primitive roles relative to the current reduction standard.

Logical dependencies actually required:

- Current primitive architecture P.
- Current reduction standard, specifically deletion-only compression without accepted replacement.
- T-001 revised deletion-only minimality.
- L-001 and P-001 for the representation case.
- L-002 for the representational-structure case.
- L-003 for the interpretation case.
- L-004 for the investigation case.
- L-005 for the reasoning-calculus case.
- Canonical definitions and axioms as background for the lemmas.

Informative but not logically required:

- L-006, because canonical role pairing is not needed for deletion-independence.
- L-007, because finite normalization termination is not needed for deletion-independence.
- Foundation consolidation report, because it authorizes the sequence but does not supply a direct premise beyond accepted T-001 and lemmas.

Historical only:

- Prior validation reports, except insofar as they establish accepted status of the consumed foundation.

Conclusion:

T-002 can be accepted only if formulated as deletion-independence under the current reduction standard. The stronger wording “not derivable from the other four” overstates the supplied evidence if read as absolute underivability. Revision to deletion-eliminability is required for precision, but the theorem’s intended result survives in that form.
