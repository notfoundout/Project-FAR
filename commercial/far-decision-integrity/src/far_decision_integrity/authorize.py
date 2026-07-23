from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .adjudicate import Adjudication, adjudicate
from .model import DecisionPackage, IntegrityStatus


class RuntimeDisposition(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    ESCALATE = "escalate"


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    disposition: RuntimeDisposition
    adjudication: Adjudication


def authorize(package: DecisionPackage) -> AuthorizationDecision:
    result = adjudicate(package)
    if result.status is IntegrityStatus.JUSTIFIED:
        disposition = RuntimeDisposition.ALLOW
    elif result.status is IntegrityStatus.UNSUPPORTED:
        disposition = RuntimeDisposition.BLOCK
    else:
        disposition = RuntimeDisposition.ESCALATE
    return AuthorizationDecision(disposition, result)
