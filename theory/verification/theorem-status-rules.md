# Theorem Status Rules

## Purpose

This document defines theorem lifecycle statuses for Project FAR.

No theorem may be marked Established merely because it has been written. Establishment requires verification.

---

# Statuses

## Draft

A theorem is Draft when its statement, scope, dependencies, or proof are incomplete.

Draft theorems may be speculative.

Draft theorems must not be used as dependencies.

---

## Proposed

A theorem is Proposed when it has:

- a clear statement;
- declared scope;
- listed dependencies;
- a candidate proof;
- stated limitations.

Proposed theorems may be discussed but must not be used as established dependencies.

---

## Verified

A theorem is Verified when it passes the proof verification checklist but has not yet been accepted into the canonical theorem catalog as established.

Verified theorems may be referenced as pending dependencies, but downstream proofs must mark the dependency as provisional.

---

## Established

A theorem is Established when it:

- passes the proof verification checklist;
- passes circularity audit;
- satisfies registry requirements;
- uses canonical notation;
- states scope and limitations;
- appears in the theorem catalog.

Established theorems may be used as dependencies.

---

## Deprecated

A theorem is Deprecated when it is no longer accepted as part of the current canonical theory.

Reasons include:

- circular dependency discovered;
- scope overclaim discovered;
- contradiction with stronger later result;
- dependency invalidated;
- primitive or definition revision invalidates the proof;
- replacement by a cleaner theorem.

Deprecated theorems must remain historically visible unless removal is explicitly justified.

---

# Status Transitions

```text
Draft -> Proposed -> Verified -> Established
```

A theorem may also move backward:

```text
Established -> Verified -> Proposed -> Draft
```

or:

```text
Established -> Deprecated
```

---

# Downgrade Rule

If a theorem fails any required verification gate after being marked Established, it must be downgraded immediately.

The downgrade must identify:

- failed gate;
- affected theorem;
- reason for failure;
- required repair;
- temporary replacement status.

---

# Dependency Rule

Only Established theorems may serve as stable dependencies for later Established theorems.

Verified but not Established theorems may be used only with explicit provisional marking.

Draft and Proposed theorems may not serve as canonical dependencies.
