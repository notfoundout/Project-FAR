# Project FAR governed registries

Status: **Canonical for the named registry function; never theory authority**

These machine-readable registries prevent research opportunities, unresolved questions,
citations, tool boundaries, and known epistemic threats from disappearing into transient
conversation. They may route work and record provenance. They may not alter a theorem,
contract, proof, counterexample, or governance disposition.

`opportunities-v1.0.json` is the canonical planning inventory. Its `canonical` field means the
entry is a governed Project FAR planning record, not that the idea is part of canonical theory.
`SUPERSEDED` and `REJECTED` entries are permanent regression guards, not a backlog.

Generated human views are written under `docs/planning/` and `docs/research/`. Edit the JSON
source and run `python tools/far_research_registry.py --write`; do not hand-edit a generated
view.

Validation fails on duplicate identifiers, schema violations, unknown references, prohibited
ideas assigned an active priority, stale generated output, or a registry that attempts to
claim theory authority.
