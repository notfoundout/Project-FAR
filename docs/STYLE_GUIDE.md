# Style Guide

## Purpose

This document defines the documentation standards used throughout Project FAR.

Its purpose is to promote clarity, consistency, precision, and maintainability across the repository.

The style guide governs presentation rather than theory.

---

## General Principles

Documentation should be:

- Precise
- Explicit
- Consistent
- Concise
- Auditable

Clarity should always take precedence over stylistic preference.

---

## Terminology

Technical terms shall be used consistently throughout the repository.

Unless explicitly stated otherwise, every technical term refers to its canonical definition in:

`theory/definitions/definitions.md`

New terminology should not be introduced if an existing defined term is sufficient.

---

## Canonical Sources

Every concept should possess exactly one canonical location.

Other documents should reference that location rather than restating the concept.

Redundant definitions should be avoided.

---

## Document Structure

Documents should generally follow this structure:

1. Purpose
2. Definition (when applicable)
3. Objective
4. Core Content
5. Relationships
6. Research Status (when applicable)

Not every document requires every section.

Sections should be included only when they contribute meaningful information.

---

## Language

Documentation should:

- use precise language,
- avoid unnecessary ambiguity,
- distinguish clearly between established results and ongoing research,
- avoid rhetorical or persuasive language.

Normative language should be used only when specifying framework requirements.

---

## Definitions

Formal definitions belong exclusively in:

`theory/definitions/definitions.md`

Other documents should reference canonical definitions rather than redefining terms.

---

## Cross References

Whenever another document provides the canonical treatment of a concept, reference that document instead of duplicating its content.

---

## Repository Organization

Every file should have a single primary responsibility.

If removing a file does not reduce the expressive power of the repository, that file should be merged with another document or removed.

Similarly, if two files substantially overlap in purpose, they should be consolidated.

---

## Revision Policy

Changes to canonical definitions should be made only after considering their effects throughout the repository.

Whenever a canonical definition changes, all dependent documents should be updated to maintain consistency.
