# Vocabulary Semantics Baseline 1.1

## Status and chronology

Vocabulary Semantics Baseline 1.1 is a prospective semantic extension created after the official CRE-002 semantic-licensing result. It does not modify Baseline 1.0, does not alter any CRE-002 artifact, and cannot reclassify the three recorded CRE-002 outcomes.

Its first eligible use is a separately preregistered experiment labeled `CRE-002-EXT-001`, after checksum locking, independent review, and an explicit execution unlock.

The claim subject is not the primitives alone. It is each official vocabulary together with the explicitly declared, bounded derived constructs below.

## Added bounded derived constructs

### D_nondeterminism

A finite, explicitly enumerated set of alternative outcomes at one transition point. One listed alternative is selected per firing. The construct does not license probabilities, fairness, hidden choice rules, or unlisted outcomes.

Example: a sensor-record transition with exactly two declared outcomes, `positive` and `negative`, each with explicit state and evidence updates.

Non-example: an instruction to choose any value, sample from an unstated distribution, or continue generating alternatives indefinitely.

### D_concurrency

A bounded interleaving semantics over a finite set of atomic transitions. More than one transition may be eligible, but one complete atomic transition executes per step and the ordered history records the interleaving.

Example: two sensor-record transitions can occur in either order, with each transition applied atomically.

Non-example: true simultaneous writes, an unbounded process population, continuous time, or implicit race resolution.

### D_priority

A finite defeasible ordering between identified applicable rules. A higher-priority rule defeats a lower-priority conflicting rule only in the current state and only when the explicit conflict predicate holds.

Example: an operator override defeats an automatic dispatch rule for the current state while leaving unrelated rules eligible.

Non-example: an unstated preference, a universal moral ranking, or an unlimited priority hierarchy.

### D_provenance

A finite evidence tuple containing a claim, value, source identifier, reliability label, and ordered record position. Guards match exact recorded tuples. The construct does not infer truth, source credibility, probability, or causation.

Example: `sensor_a_positive=true`, source `sensor_a`, reliability `high`, recorded at evidence position 1.

Non-example: treating an unrecorded source as trustworthy or inferring a probability from the word `high`.

### D_rule_modification

A bounded transition that changes an identified rule's registered status or parameter. The authorizing rule, target, before-state requirement, after-state value, firing bound, history effect, and later eligibility effect must be explicit.

Example: one authorized transition changes `R_dispatch_beta` from active to inactive and may fire at most once.

Non-example: arbitrary code execution, unrestricted rule creation, self-modifying compiler logic, or modification of an unregistered target.

## Vocabulary-specific licensing

### Vocabulary A: Object, Relation, Transformation

Objects identify states, rules, alternatives, and evidence records. Relations encode finite guards, provenance tuples, priority and conflict relations, and ordering. Transformations encode atomic state changes and bounded rule-status modifications.

### Vocabulary B: State, Transition, Label

States hold bounded assignments. Transitions encode atomic moves and rule modifications. Labels use registered finite schemas for alternatives, evidence, priority, conflict, and history. A Label is not an unrestricted payload container.

### Vocabulary C: Representation, Representational Structure, Interpretation, Investigation, Calculus

Representations identify values, rules, and evidence. Representational Structures record finite organization and ordering. Interpretations assign registered meanings. Investigation fixes the bounded objective and scope. Calculus records atomic eligibility, updates, priority defeat, and bounded modification. Calculus is not a general-purpose programming language.

## Freeze boundary

Baseline 1.1 becomes usable only after this package is merged and checksum locked. It cannot be cited as evidence that CRE-002 should have passed. CRE-002 remains an official prospective result showing that Baseline 1.0 did not explicitly license five required commitments.

## Unsupported conclusions

This baseline does not establish universal sufficiency, primitive-only sufficiency, necessity, minimality, independence, superiority, a FAR proof, a universal structure of reasoning, retrospective validation of CRE-002, or behavioral success in any future extension.
