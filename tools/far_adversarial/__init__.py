"""Minimum automation for the Presenting Project FAR adversarial relay.

Scope: it removes the manual Claude<->GPT message relay and preserves the
evidence that relay used to leave only in a chat window. It is not a research
platform, it does not adjudicate theory, and nothing it produces is canonical.

Governance boundaries enforced here:

- ``READY_UNDER_INTERNAL_PROTOCOL`` is an internal disposition, never Acceptance.
- Model agreement is recorded as metadata and is never an input to a disposition.
- Execution failures are typed separately from research dispositions.
- Analytical lanes are read-only; the orchestrator owns every runtime write.
"""

from .ledger import Ledger, Target, Issue  # noqa: F401
from .evidence import EvidenceStore  # noqa: F401
from .orchestrator import Orchestrator  # noqa: F401

__all__ = ["Ledger", "Target", "Issue", "EvidenceStore", "Orchestrator"]
