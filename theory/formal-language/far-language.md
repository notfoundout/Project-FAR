# FAR Formal Language

## Status

Initial formal syntax specification.

---

## Purpose

This document defines the first formal language for Project FAR representations.

The goal is to separate:

- syntax: what can be written;
- well-formedness: what counts as a valid FAR object;
- semantics: what those objects mean under an interpretation;
- proof: which transformations are justified.

---

# 1. Primitive Sorts

The FAR language has five primitive sorts:

```text
Investigation
Representation
Structure
Interpretation
Calculus
```

A FAR reasoning object also uses the derived sort:

```text
Trace
```

---

# 2. Core Tuple Syntax

A FAR object has the syntactic form:

```text
FAR(R) = <I, Rep, S, Int, C, T>
```

where:

- `I : Investigation`
- `Rep : List[Representation]`
- `S : Structure`
- `Int : Interpretation`
- `C : Calculus`
- `T : Trace`

---

# 3. Representation Syntax

A representation has the form:

```text
representation <id>:
  kind: <kind>
  content: <content>
```

Required fields:

- `id`: stable identifier;
- `kind`: claim, premise, conclusion, rule, observation, hypothesis, objection, model, or definition;
- `content`: uninterpreted syntactic payload.

---

# 4. Structure Syntax

A structural relation has the form:

```text
relation <id>:
  type: <relation-type>
  source: <representation-id>
  target: <representation-id>
```

Permitted relation types include:

- supports;
- depends_on;
- contradicts;
- rebuts;
- undercuts;
- instantiates;
- generalizes;
- precedes;
- equivalent_to.

---

# 5. Interpretation Syntax

An interpretation assignment has the form:

```text
interpretation <representation-id>:
  meaning: <semantic-content>
```

The semantic content may be informal text, formal notation, or a reference into a semantic model.

---

# 6. Calculus Syntax

A calculus rule has the form:

```text
rule <id>:
  name: <rule-name>
  inputs: [<representation-id>]
  output: <representation-id>
  condition: <admissibility-condition>
```

Rules do not have to be deductive. A calculus may be deductive, probabilistic, defeasible, abductive, analogical, legal, empirical, or hybrid.

---

# 7. Trace Syntax

A transition signature has the form:

```text
transition <id>:
  source: <state-id>
  rule: <rule-id>
  target: <state-id>
  status: <status>
  order: <integer>
```

Permitted statuses:

- admissible;
- inadmissible;
- unresolved.

---

# 8. Well-Formed FAR Object

A FAR object is well-formed if:

1. every representation has a unique id;
2. every structural relation references existing representations;
3. every interpretation assignment references an existing representation;
4. every calculus rule references existing representations;
5. every transition references an existing rule;
6. transition order is total within the trace;
7. the investigation is nonempty;
8. every conclusion has at least one structural or trace role unless explicitly marked isolated.

---

# 9. Syntax/Semantics Separation

A representation's `content` field is syntax.

An interpretation assignment supplies semantic content.

Therefore two representations may have identical syntax and different meanings under different interpretations.

---

# 10. Machine Format

The first machine-readable format for FAR objects is YAML.

The parser in `tools/parse_far.py` reads YAML into internal FAR data structures.
