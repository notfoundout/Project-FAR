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

## Research Contribution and Claim Boundary

Complete this section for research, theory, validation, mechanization used as evidence, or evidence-facing release work.

- Central claim tested: existence / bounded sufficiency / universality / necessity / minimality / nontriviality / none
- Evidential role: exploratory / internal robustness / confirmatory / independent replication / enabling engineering / maintenance / application
- Current uncertainty reduced:
- Result that could count against FAR:
- Frozen theory or semantics version:
- External observation contract:
- Negative controls:
- Full-cost accounting method:
- Independence level and conflicts:
- Strongest claim supported:
- Explicit nonclaims:

Confirm all that apply:

- [ ] The PR does not allow FAR to define the theory, source cases, competitors, mappings, verifier, and final adjudication for a confirmatory claim.
- [ ] Any theory change after exposure to a frozen case creates a new version and preserves the earlier result.
- [ ] Internal multi-implementation robustness is not described as external independence.
- [ ] Derived machinery, hidden state, ambiguity policies, and adjudication burden are counted where comparative economy is discussed.
- [ ] Tradeoffs are not reported as superiority.
- [ ] Failed, excluded, unresolved, and divergent outcomes remain visible.
- [ ] Scope was fixed before the challenged result or is identified as post hoc.
- [ ] The work is authorized by `theory/evaluation/research-gates.json`, or the reason for an exception is documented.

---

## Related Research

Reference any relevant documents.

- `docs/governance/central-research-program.md`
- `docs/governance/anti-self-validation-standard.md`
- `docs/governance/research-priority-reset.md`
- `docs/methodology/confirmatory-research-package.md`
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
- [ ] `python tools/check_research_gates.py` passes
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
