# Statement Schema

## Status

Proposed canonical schema for machine-readable Project FAR statements.

---

## Purpose

Project FAR currently stores many claims as prose strings. Prose is readable but weak for automated comparison.

The statement schema defines a minimal structured form that can be compared by tools while preserving human-readable text.

The schema is intentionally small. It is not yet a complete formal language or proof-assistant encoding.

---

## Canonical Statement Object

A statement object should use this shape when possible:

```yaml
statement:
  kind: universal | existential | definitional | conditional | equivalence | preservation | construction | validation | classification | meta
  subject: <main object or domain>
  predicate: <claim made about the subject>
  scope: <where the claim applies>
  claim: <human-readable canonical claim>
```

Only `kind` and `claim` are mandatory during the transition period.

`subject`, `predicate`, and `scope` should be supplied whenever they are clear.

---

## Field Semantics

### `kind`

The logical shape of the statement.

Allowed initial values:

- `universal`: claims all objects in a scope satisfy a predicate;
- `existential`: claims at least one object exists;
- `definitional`: gives or unfolds a definition;
- `conditional`: claims that one condition implies another;
- `equivalence`: claims two objects, models, or statements are equivalent under a condition;
- `preservation`: claims some property is preserved across a mapping or transformation;
- `construction`: claims something can be constructed from prior objects;
- `validation`: claims a checker, rule, or process validates something;
- `classification`: assigns an object to a class or status;
- `meta`: claims something about the theory, repository, proof system, or verification process.

### `subject`

The main object, process, representation, model, theorem, rule, or concept being discussed.

### `predicate`

The main property or relation asserted of the subject.

### `scope`

The boundary under which the claim is valid.

Examples:

- `Project FAR scoped reasoning processes`
- `finite FAR representations`
- `registered derived concepts`
- `proof objects T-001 through T-015`

### `claim`

A canonical human-readable rendering of the statement.

This field remains necessary because the schema is transitional. Tools should compare structured fields first and fall back to `claim` when necessary.

---

## Matching Rules

Two statement objects are an exact structured match when:

1. `kind` matches;
2. `subject` matches, if both are present;
3. `predicate` matches, if both are present;
4. `scope` matches, if both are present;
5. `claim` matches or is sufficiently similar under the checker fallback.

A statement object is a weak structured match when:

1. `kind` matches; and
2. at least one of `subject`, `predicate`, or `scope` overlaps; and
3. the `claim` fallback is compatible.

---

## Transitional Rule

During migration, metadata and proof objects may still contain prose statement strings.

Tools should support both forms:

```yaml
statement: "Every scoped reasoning process admits a FAR representation."
```

and:

```yaml
statement:
  kind: universal
  subject: scoped reasoning process
  predicate: admits FAR representation
  scope: Project FAR
  claim: Every scoped reasoning process admits a FAR representation.
```

Structured objects should be preferred for new artifacts.

---

## Relationship to FIR

FIR uses statement objects as the bridge between repository metadata, proof objects, parsers, reasoning engine output, and future proof-assistant encodings.

The current schema is the first machine-comparable statement layer. Later versions may replace strings with fully formal terms, quantifiers, variables, and typed expressions.

---

## Failure Conditions

A structured statement is invalid if:

- it lacks `kind`;
- it lacks `claim`;
- `kind` is not one of the allowed values;
- it contradicts the human-readable source file;
- it claims a broader scope than the source artifact supports.
