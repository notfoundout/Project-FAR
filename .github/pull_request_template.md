# Pull Request

## Summary

Provide a concise description of the proposed changes.

---

## Motivation

Why are these changes necessary?

---

## Type of Change

Select all that apply.

- [ ] Documentation
- [ ] Theory
- [ ] FARA
- [ ] FAR
- [ ] FARO
- [ ] Validation
- [ ] Examples
- [ ] Research
- [ ] Repository Infrastructure

---

## Files Modified

List the primary files affected.

---

## Dependencies

Does this change introduce any new dependencies?

If yes, describe them.

---

## Architectural Impact

Does this change:

- introduce a new concept?
- modify an existing concept?
- change a definition?
- affect the dependency structure?

Explain.

---

## Related Research

Reference any relevant documents.

- `research/open-problems/open-questions.md`
- `docs/DECISION_LOG.md`
- `research/notes/backburner.md`
- `research/notes/failed-approaches.md`

---

## Checklist

- [ ] Definitions remain consistent.
- [ ] No circular dependencies introduced.
- [ ] Documentation updated.
- [ ] Examples updated (if necessary).
- [ ] Validation updated (if necessary).

---

## Validation

- [ ] `python tools/repo_health_check.py --fast` passes
- [ ] Internal links pass
- [ ] Math displays render
- [ ] Release docs are consistent if release-facing files changed
- [ ] No broken image or math-display links were introduced
- [ ] No orphaned documentation was introduced unless intentional
- [ ] No theory meaning changed unless explicitly intended
- [ ] No primitives, axioms, theorem statements, proof objects, parser behavior, reasoning-engine behavior, or metadata schemas changed unless explicitly intended

## Scope

Describe whether this PR is:
- theory
- tooling
- docs
- evaluation
- release
- cleanup
