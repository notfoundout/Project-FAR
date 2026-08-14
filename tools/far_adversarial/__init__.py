"""Minimum automation for the Presenting Project FAR adversarial relay.

Scope: it removes the manual Claude<->GPT message relay and preserves the
evidence that relay used to leave only in a chat window. It is not a research
platform, it does not adjudicate theory, and nothing it produces is canonical.

Governance boundaries enforced here:

- ``READY_UNDER_INTERNAL_PROTOCOL`` is an internal disposition, never Acceptance.
- Model agreement is recorded as metadata and is never an input to a disposition.
- No lane adjudicates: a challenged lane rebuts, only an owner withdraws, and
  only non-model evidence settles.
- Execution stops (round, token, rate, time ceilings) never write a research
  disposition and never satisfy a dependency.
- Unresolved source and formal obligations block readiness.
- Both lanes read the same frozen bytes from a registered source; neither reads
  the working tree.
- Analytical lanes are read-only; the orchestrator owns every runtime write.
"""

from .evidence import EvidenceStore, RunRecord  # noqa: F401
from .frozen_source import GitFrozenSource, ManifestFrozenSource  # noqa: F401
from .ledger import Candidate, Dependency, Issue, Ledger, Obligation, Target  # noqa: F401
from .orchestrator import Orchestrator  # noqa: F401
from .replay import replay  # noqa: F401

__all__ = [
    "Candidate",
    "Dependency",
    "EvidenceStore",
    "GitFrozenSource",
    "Issue",
    "Ledger",
    "ManifestFrozenSource",
    "Obligation",
    "Orchestrator",
    "RunRecord",
    "Target",
    "replay",
]
