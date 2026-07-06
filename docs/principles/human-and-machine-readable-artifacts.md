# Human-Readable and Machine-Readable Artifact Principle

## Status

Accepted design principle.

---

## Principle

Every canonical Project FAR theoretical artifact should have both a human-readable representation and a machine-readable representation.

Neither representation is authoritative in isolation. Together they constitute the canonical artifact.

---

## Purpose

Project FAR is intended to be understandable by humans and usable by verification tools.

Human readers need explanations, motivation, examples, argumentation, and context.

Software tools need stable identifiers, statuses, dependencies, scopes, sources, and structured proof objects.

The repository therefore maintains parallel representations of the same theory.

---

## Human-Readable Layer

The human-readable layer is written primarily in Markdown.

It answers:

- What does this concept mean?
- Why does this theorem matter?
- What is the proof idea?
- What examples illustrate the point?
- What limitations should a reader understand?

Examples:

- `theory/definitions/`
- `theory/proofs/`
- `theory/lemmas/`
- `docs/releases/`
- `examples/`

---

## Machine-Readable Layer

The machine-readable layer is written primarily in YAML and eventually proof-assistant files.

It answers:

- What is the artifact ID?
- What is its status?
- What dependencies does it use?
- What source file explains it?
- What scope does it claim?
- Can software validate its references?
- Can software build its dependency graph?

Examples:

- `theory/metadata/theorems.yaml`
- `theory/metadata/propositions.yaml`
- `theory/metadata/lemmas.yaml`
- future `theory/metadata/definitions.yaml`
- future `theory/metadata/axioms.yaml`
- future `*.proof.yaml` proof objects
- future Lean or Coq files

---

## Synchronization Requirement

The human-readable and machine-readable representations must describe the same artifact.

If a theorem, definition, axiom, proposition, or lemma changes in one layer, the corresponding layer must be checked and updated if necessary.

A verifier should eventually reject changes that create inconsistency between the layers.

---

## Canonical Pattern

A mature FAR artifact may have this structure:

```text
theory/proofs/T-003-representation-theorem.md        # human-readable proof
theory/proof-objects/T-003.proof.yaml                # machine-readable proof object
theory/metadata/theorems.yaml                        # machine-readable catalog entry
mechanization/lean/FARCore.lean                      # proof-assistant representation
```

These are not four separate theorems. They are four representations of the same canonical theorem.

---

## Rationale

Markdown alone is readable but difficult to validate automatically.

YAML alone is structured but poor for explanation.

Proof-assistant code is precise but often difficult for ordinary readers.

Project FAR requires all three layers over time:

1. Markdown for human understanding;
2. YAML for repository verification and tooling;
3. proof-assistant files for independent logical checking.

---

## Enforcement Direction

The current verifier already validates theorem, proposition, and lemma metadata.

Future verifier work should add:

- definition metadata validation;
- axiom metadata validation;
- human/machine synchronization checks;
- proof-object checks;
- generated indexes;
- dependency impact analysis.

---

## Failure Condition

A canonical artifact is incomplete if it exists only as informal prose when the current project phase requires machine-readable metadata.

A machine-readable entry is incomplete if it points to no human-readable explanation.
