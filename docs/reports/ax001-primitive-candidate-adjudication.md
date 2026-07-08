# AX-001 Primitive Candidate Adjudication

## Executive Summary

This foundational research adjudication evaluates the competing AX-001 primitive candidates identified by the prior circularity investigation. It does not validate L-001 through T-001, does not revise repository architecture, and does not introduce tooling or automation.

Final recommendation: **REVISE OPERATION**.

The adjudication does not establish that Operation should be replaced. Every serious replacement candidate avoids one pressure only by importing another unresolved primitive burden. Transition, Rule-Licensed Transition, and Admissible Transition are the strongest rivals because they offer greater structural precision and better explain why reasoning is not arbitrary manipulation. However, none can replace Operation without requiring prior independent accounts of reasoning state, admissibility, rule, licensing, ordering, and representation.

The current AX-001 characterization, `An operation is an executable act performed within a reasoning process.`, should not remain as the best available characterization. The terms `executable`, `act`, and `performed` are operation-adjacent and create avoidable circularity pressure. The superior supported formulation is not a replacement primitive, but a narrower characterization of Operation as a primitive whose role is to mark admissible reasoning-relevant transition, preservation, inspection, constraint, or transformation without reducing Operation to any one of those effects.

AX-001 is not changed in this PR because the user requested an adjudication report and directed that AX-001 be revised only if the adjudication clearly supports a superior formulation. This report supports revision as the final recommendation, but applying the canonical revision would require a separate AX-001 edit with exact wording and stability-gate review. Therefore AX-001 remains unchanged in this PR.

## Prior Evidence

This adjudication uses the following prior evidence:

- `docs/reports/foundation-validation-report.md`
- `docs/reports/ax001-circularity-investigation.md`
- `docs/reports/appendices/ax001-p1-raw.md`
- `docs/reports/appendices/ax001-c1-raw.md`

Evidence carried forward:

1. The foundation validation stopped at AX-001 and did not validate downstream artifacts.
2. The current AX-001 characterization is not syntactically self-referential, but it is definitionally unstable.
3. The strongest circularity pressures are `act`, `performed`, `execute`, `executable`, `act upon`, and `reasoning process` when reasoning process is construed as a sequence of operations.
4. P1 and C1 both found that no successful non-circular reduction of Operation was established.
5. P1 and C1 both found multiple live rivals, especially Transition, with limited viability for State Change, Event, Transformation, Rule-Licensed Transition, and Constraint Application.
6. Prior evidence already rejects simple reductions of Operation to state transition, representation modification, calculus application, and transformation because each loses cases or imports hidden assumptions.
7. Operation alone does not explain the difference between reasoning and arbitrary manipulation unless admissibility, rule, trace, representation, interpretation, or inferential constraint is supplied somewhere.

## Candidate Definitions

The following are strongest formulations for adjudication. They are not promoted as accepted definitions.

### Operation

A primitive marker for a reasoning-relevant doing, occurrence, or formal step that can transform, preserve, inspect, constrain, relate, or determine a reasoning condition under a non-arbitrary standard.

Strongest use: broadest explanatory coverage across transformation, preservation, inspection, validation, comparison, constraint, and trace participation.

Main risk: current wording uses `executable act performed`, which imports act/perform/execute circularity.

### Transition

A relation from one reasoning state to another reasoning state, including identity and meta-state transitions where preservation, inspection, or verification leaves the object-level representation unchanged but changes determinacy, warrant, availability, or trace status.

Strongest use: provides before/after structure and avoids act/perform vocabulary.

Main risk: depends on independently individuated reasoning states and on a non-operational successor relation.

### State Change

A change in a reasoning state, including changes in representation, warrant, constraint satisfaction, path availability, or trace status.

Strongest use: captures effect and distinguishes inert objects from reasoning episodes.

Main risk: narrower than transition because it struggles with identity, preservation, inspection, and no-op cases unless state is expanded until nearly every determination counts as a change.

### Event

A bounded occurrence within a reasoning process or trace.

Strongest use: avoids agency and execution vocabulary while supporting token individuation.

Main risk: too broad; arbitrary noise, errors, elapsed time, or irrelevant system events are events unless additional admissibility or reasoning-relevance constraints are imported.

### Transformation

A mapping or episode that converts an input reasoning representation, state, or condition into an output representation, state, or condition.

Strongest use: strong coverage for constructive and modifying operations.

Main risk: too narrow for inspection, preservation, validation, comparison, rejection, and identity cases unless transformation is broadened into an operation-like synonym.

### Rule-Licensed Transition

An ordered pair of reasoning states or conditions whose successor relation is licensed by a rule.

Strongest use: explains non-arbitrariness better than bare Operation or bare Transition.

Main risk: assumes all reasoning steps are rule-licensed and imports rule, licensing, state, and transition as prior burdens.

### Admissible Transition

A transition between reasoning states that satisfies the constraints required for participation in reasoning.

Strongest use: captures normativity without requiring a specific rule syntax.

Main risk: shifts primitive burden to admissibility, constraint satisfaction, reasoning state, and transition.

### Act

An occurrence of doing within reasoning, construed minimally as an event-token rather than as agency or intentional action.

Strongest use: close to ordinary operational language and can cover non-transformative cases.

Main risk: if act means operation-like doing, it is not reductive; if act means event-token, Event is simpler.

### Constraint Application

The imposition, satisfaction, checking, or use of a constraint over a reasoning state or transition.

Strongest use: explains filtering, rejection, admissibility, and non-arbitrariness.

Main risk: `application` reintroduces perform/execute language, and constraint use is too narrow to cover all constructive, representational, or trace-producing steps.

## Candidate Evaluation Matrix

| Candidate | Non-circularity | Necessity | Sufficiency | Independence | Replaceability | Explanatory economy | Distinguishes reasoning from arbitrary manipulation | Compatibility with representation, structure, interpretation, investigation, calculus, trace | Hidden assumptions | Downstream concepts required | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Operation | Medium if revised; low in current wording | High | Medium | Medium-low | Not replaced by evidence | High coverage, weak current wording | Weak alone; stronger when paired with admissibility | Broad compatibility | act, execution, performance, process | admissibility, representation, trace, calculus or constraints | Dominant if revised |
| Transition | Medium-high | High | Medium-high | Medium | Strong rival | Good | Medium; needs admissibility | Strong with structure and trace | state individuation, ordering | reasoning state, relation, admissibility | Viable |
| State Change | Medium | Medium-high | Medium-low | Medium | Partial rival | Moderate | Low-medium | Good for dynamic structure, weak for preservation | expanded state, effect | state, change criterion | Eliminated as replacement |
| Event | High | Medium | Low | High | Weak replacement | Simple but overbroad | Low | Good for trace, weak for calculus and interpretation | bounded occurrence, relevance | reasoning relevance, admissibility | Eliminated as replacement |
| Transformation | Medium | Medium | Medium-low | Medium | Partial rival | Moderate-low after broadening | Low-medium | Good for representation, weak for preservation/inspection | input-output, effect | representation/state mapping | Eliminated as replacement |
| Rule-Licensed Transition | Medium | Medium-high in formal reasoning | Medium-high | Low-medium | Strong rival | Lower; imports rule apparatus | High | Strong with calculus and trace | rule-governance, licensing | rule, state, transition, licensing | Viable |
| Admissible Transition | Medium-high | High | Medium-high | Medium-low | Strongest rival | Good but abstract | High | Strong across structure, calculus, trace | admissibility primitive | admissibility, state, transition | Viable |
| Act | Low-medium | Medium | Medium-low | Low | Weak | Poor; synonymic pressure | Low | Weak unless supplemented | agency/doing | event or agency, reasoning relevance | Eliminated |
| Constraint Application | Low-medium | Medium | Medium | Low-medium | Partial rival | Moderate-low | High for filtering | Strong for calculus, weak for constructive steps | application, constraint priority | constraints, state, admissibility | Eliminated as replacement |

## Elimination Test

### Operation — dominant if revised

Operation is retained as the dominant candidate only under revision. It has the broadest coverage and best preserves the ability to describe transformation, preservation, inspection, constraint, relation, validation, and trace participation. Current wording is not dominant because `executable act performed` carries avoidable circularity pressure.

### Transition — retained as viable

Transition is not eliminated. It is the strongest pure replacement candidate. It avoids act/perform/execute vocabulary and gives a useful structure for trace and reasoning-state succession. It is not dominant because it requires independently accepted reasoning states and admissibility to avoid arbitrary manipulation.

### State Change — eliminated as replacement

State Change is eliminated as a replacement for Operation. It either excludes preservation, inspection, identity, verification, and no-op cases, or it expands `state` and `change` until any determination counts as change. That expansion shifts the burden to state individuation and meta-state change rather than reducing Operation.

### Event — eliminated as replacement

Event is eliminated as a replacement. It has low circularity and useful tokenhood, but it is too broad. It cannot distinguish reasoning from arbitrary occurrences without importing admissibility, reasoning relevance, representation, or trace conditions.

### Transformation — eliminated as replacement

Transformation is eliminated as a replacement. It explains constructive changes but fails for preservation, inspection, comparison, validation, rejection, and identity cases unless broadened into a synonym for operation.

### Rule-Licensed Transition — retained as viable

Rule-Licensed Transition is retained as viable. It gives the strongest account of non-arbitrary reasoning when calculus-like rules are present. It is not dominant because it assumes rule-governance and imports rule/licensing burdens.

### Admissible Transition — retained as viable

Admissible Transition is retained as viable and is the strongest rival to revised Operation. It explains non-arbitrariness without requiring the narrower term `rule`. It is not dominant because admissibility remains an unresolved primitive burden.

### Act — eliminated

Act is eliminated. If construed as ordinary doing, it is too close to Operation. If construed as event-token, Event is cleaner. If construed through agency, it is too narrow and imports unnecessary intentionality.

### Constraint Application — eliminated as replacement

Constraint Application is eliminated as a replacement. It is important for admissibility and arbitrary-manipulation tests, but not every operation is merely constraint application. The word `application` also reintroduces execution/performance pressure.

## Pairwise Comparisons

### Operation vs Transition

Transition improves structural clarity and reduces act/perform circularity. Operation has better coverage because it can include inspection, preservation, validation, comparison, and constraint cases without forcing each into a state-successor model. Transition beats unrevised Operation on clarity; revised Operation beats Transition on coverage and primitive economy because Transition still needs reasoning state and admissibility.

### Operation vs Rule-Licensed Transition

Rule-Licensed Transition best distinguishes reasoning from arbitrary manipulation where formal rules are already available. It loses economy by requiring rule, licensing, state, and transition, and it may exclude non-rule-formal but still admissible reasoning. Revised Operation can treat rule-licensed transitions as a major species without making rule-licensing the primitive.

### Operation vs Admissible Transition

Admissible Transition is the strongest replacement candidate. It avoids agency and execution vocabulary and directly addresses arbitrary manipulation. Its weakness is burden shifting: admissibility must be explained without Operation, and reasoning states must be individuated independently. Revised Operation should absorb the lesson that admissibility is required for reasoning relevance while not reducing Operation to transition.

## Burden Shift Analysis

| Candidate | Circularity avoided | Burden shifted |
|---|---|---|
| Transition | Avoids act/perform/execute | reasoning state, successor relation, ordering, identity transition, admissibility |
| State Change | Avoids act language | state individuation, change criterion, meta-state expansion |
| Event | Avoids agency/execution | reasoning relevance, admissibility, trace membership, boundedness |
| Transformation | Avoids performance vocabulary | input/output mapping, effect, representation/state ontology, preservation handling |
| Rule-Licensed Transition | Avoids arbitrary transition | rule, licensing, rule validity, state, transition, applicability |
| Admissible Transition | Avoids rule narrowness and act vocabulary | admissibility, constraint satisfaction, reasoning-state identity, non-arbitrary standard |
| Act | Avoids formal state apparatus | agency, doing, performance, event-token identity |
| Constraint Application | Avoids arbitrary manipulation | constraint ontology, application, priority, scope, constructive coverage |

No candidate eliminates primitive burden. The strongest rivals shift the burden from Operation to state/transition/admissibility/rule. The weaker rivals shift it to event/relevance, transformation/effect, or act/agency.

## Reasoning vs Arbitrary Manipulation

The best explanation of why reasoning is not arbitrary manipulation is not bare Operation, bare Transition, bare Event, or bare State Change. Arbitrary manipulation can be an operation-like act, a transition, an event, or a state change.

The differentiating feature is admissibility under reasoning-relevant constraints. Rule-Licensed Transition explains this most concretely in formal systems. Admissible Transition explains it more generally. Revised Operation should therefore be characterized so that operation is not mere doing but a primitive reasoning-relevant unit whose admissibility is assessed by downstream calculus, representation, interpretation, structure, investigation, and trace constraints.

This does not mean Operation reduces to admissibility. It means Operation alone is insufficient to reconstruct reasoning; its primitive role must be paired with later constraints that determine whether an operation participates in reasoning rather than arbitrary manipulation.

## Replacement Analysis

Operation cannot currently be replaced without loss.

- Replacing Operation with Transition loses or distorts preservation, inspection, identity, and non-effect cases unless transition is broadened with meta-state machinery.
- Replacing Operation with Admissible Transition improves non-arbitrariness but imports admissibility as an unexplained primitive burden.
- Replacing Operation with Rule-Licensed Transition overfits formal rule-governed reasoning and imports rule/licensing machinery.
- Replacing Operation with Event is too broad.
- Replacing Operation with Transformation is too narrow.
- Replacing Operation with State Change is too narrow unless state is expanded beyond demonstrated need.
- Replacing Operation with Act does not reduce circularity.
- Replacing Operation with Constraint Application covers filtering and checking but not the full range of reasoning steps.

Therefore replacement is not justified by the available evidence.

## Revision Analysis

Revision is justified. The current characterization should not continue to rely on `executable act performed` as if those terms were independent reducers. A better characterization would avoid presenting act, performance, or execution as reductive vocabulary.

Supported revision direction:

```text
Operation is the primitive unit of reasoning-relevant occurrence or step by which a reasoning process transforms, preserves, inspects, relates, constrains, or determines reasoning conditions under standards of admissibility supplied by the surrounding theory.
```

This wording is not adopted here as canonical AX-001 text. It is recorded as the supported direction because it:

1. avoids treating `act`, `performed`, or `executable` as reducers;
2. preserves coverage for transformation and non-transformation cases;
3. acknowledges that non-arbitrariness depends on admissibility standards;
4. does not reduce Operation to Transition, State Change, Event, Rule, or Constraint;
5. keeps Operation primitive while clarifying its role.

## Final Adjudication

**REVISE OPERATION**

Operation remains the dominant candidate only if revised. No replacement candidate satisfies Project FAR primitive doctrine with less circularity and equal or greater explanatory coverage. However, unrevised Operation is too circularity-prone and insufficiently clear to remain stable.

AX-001 changed in this PR: **No**.

Reason: this PR creates the requested adjudication report only. The adjudication supports later AX-001 revision, but no canonical AX-001 edit is made without a separate stability review of exact wording.

Candidates eliminated as replacements:

- State Change
- Event
- Transformation
- Act
- Constraint Application

Candidates still viable:

- Operation, if revised
- Transition
- Rule-Licensed Transition
- Admissible Transition

Dominant candidate:

- Revised Operation

## Remaining Open Questions

1. What exact AX-001 wording should replace `An operation is an executable act performed within a reasoning process`?
2. Can admissibility be characterized without reducing it to Operation, rule application, or downstream calculus?
3. Can reasoning states be individuated independently enough to support Transition or Admissible Transition as future competitors?
4. Should AX-001 distinguish operation-types from operation-tokens?
5. Should AX-001 distinguish temporal containment in a reasoning process from functional participation in reasoning?
6. What minimal downstream concepts are required to distinguish reasoning from arbitrary manipulation without making AX-001 depend circularly on L-001 through T-001?
7. Should a future AX-001 revision include an explicit note that Operation alone does not supply normativity, semantics, or validity?
