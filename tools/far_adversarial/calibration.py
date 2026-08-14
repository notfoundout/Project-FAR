"""Blind historical calibration against already-resolved Presenting FAR history.

Calibration validates the WORKFLOW, not the theory. A case passes when a fresh
lane, shown only what the historical lane was shown, recovers the correction
the historical exchange actually reached.

The acceptance criteria below are preregistered: they are fixed in this file
before any case is executed, and a miss is recorded as a miss. Revising a
criterion after seeing a result produces a new calibration run with a new
identity; it never retroactively becomes the original calibration.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from .safety import sha256_hex

CALIBRATION_VERSION = "far-adversarial-calibration/1"


@dataclass
class CalibrationCase:
    id: str
    description: str
    # Everything the historical lane had, with the historical answer removed.
    stimulus: str
    # Preregistered discriminating markers. All groups must fire for a pass;
    # within a group, any alternative counts.
    required_markers: list[list[str]]
    # Markers whose presence means the lane reproduced the defeated position.
    failure_markers: list[str] = field(default_factory=list)
    known_answer: str = ""
    provenance: str = ""


@dataclass
class CaseResult:
    case_id: str
    passed: bool
    missed_groups: list[int]
    fired_failure_markers: list[str]
    execution_failure: str | None = None
    invocation_id: str | None = None


def _matches(text: str, marker: str) -> bool:
    return re.search(marker, text, re.IGNORECASE | re.DOTALL) is not None


def grade(case: CalibrationCase, response_text: str) -> CaseResult:
    """Deterministic grading against the preregistered markers."""
    missed = [
        index
        for index, group in enumerate(case.required_markers)
        if not any(_matches(response_text, marker) for marker in group)
    ]
    fired = [m for m in case.failure_markers if _matches(response_text, m)]
    return CaseResult(
        case_id=case.id,
        passed=not missed and not fired,
        missed_groups=missed,
        fired_failure_markers=fired,
    )


# --- preregistered cases -------------------------------------------------

DI3_STIMULUS = """A frozen research target (call it S1) requires, among other things, that a
source determine a *completely determined transition relation* for a proof
calculus, at the level of the proof frontier.

An analyst has argued as follows against S1, and has run this argument across
four separate turns:

    Miller's treatment of sequent calculus establishes that at any point in LK
    proof search there are on the order of "1000 choices", and that "proofs are
    formless". Therefore LK has no canonical deterministic search strategy.
    Therefore the calculus does not determine search structure. Therefore no
    eligible source determines the structure S1 requires, and S1 must stay OPEN.

The same analyst also treats variation in how formulas are collected inside a
single sequent (lists vs sets vs multisets) as evidence of the same
indeterminacy.

Audit this argument against the frozen target as stated. Is it valid? If it is
not, state exactly what it conflates, and state the strongest negative claim
about the sources that actually survives your audit."""

DI3_CASE = CalibrationCase(
    id="CAL-DI3-S1",
    description=(
        "Can a fresh blind lane recover the Turn 33 correction: that absence of a "
        "canonical deterministic LK search strategy does not entail absence of a "
        "completely determined transition relation, and that intra-sequent and "
        "frontier representation are distinct levels?"
    ),
    stimulus=DI3_STIMULUS,
    required_markers=[
        # Group 0: nondeterminism is compatible with full determination.
        [
            r"nondetermin\w*[^.]{0,200}(compatible|consistent|still)[^.]{0,200}determin",
            r"(fully|completely)\s+determined\s+transition\s+relation",
            r"(does|do)\s+not\s+(entail|imply|follow)[^.]{0,200}(determined|determination)",
            r"conflat\w+[^.]{0,240}(search\s+strateg|determin)",
        ],
        # Group 1: the two representational levels are distinct.
        [
            r"intra[- ]sequent[^.]{0,200}(frontier|distinct|different)",
            r"frontier[^.]{0,200}(intra[- ]sequent|different level|distinct level)",
            r"(list|set|multiset)[^.]{0,240}(different|distinct|separate)\s+(level|question|issue)",
        ],
        # Group 2: the argument is judged invalid rather than sustained.
        [
            r"\b(invalid|does not hold|fails|unsound|not valid|defeated|rejected)\b",
            r"argument\s+(is|does)\s+not\s+(valid|succeed|work)",
        ],
    ],
    failure_markers=[
        r"the\s+argument\s+is\s+(valid|sound|correct)\s+and\s+S1\s+must\s+(stay|remain)\s+OPEN",
        r"\bI\s+sustain\s+the\s+objection\b",
    ],
    known_answer=(
        "DI3 was withdrawn in Claude Turn 33. Nondeterministic search is compatible "
        "with a completely determined transition relation; intra-sequent and "
        "frontier representation are distinct levels; the surviving negative claim "
        "weakened to 'no eligible source encountered so far has been certified to "
        "determine the frozen frontier-level search structure'."
    ),
    provenance=".far/inbox/presenting-project-far.md CLAUDE TURN 33 (VERBATIM-RECOVERED)",
)

CASES = {DI3_CASE.id: DI3_CASE}


def preregistration_digest(case_ids: list[str]) -> str:
    """Content hash of the exact criteria a run was graded against."""
    payload = [asdict(CASES[cid]) for cid in sorted(case_ids)]
    return sha256_hex(json.dumps(payload, sort_keys=True, ensure_ascii=False))


def run_case(case: CalibrationCase, provider, store, source_freeze: str) -> CaseResult:
    """Execute one blind case.

    The known answer is never placed in the prompt; only the stimulus is sent.
    """
    from .protocol import CLAUDE_ROLE

    prompt = f"{CLAUDE_ROLE}\n\nCalibration case {case.id}.\n\n{case.stimulus}"
    assert case.known_answer not in prompt, "calibration stimulus leaked the known answer"
    result = provider.complete(prompt)
    invocation = store.record(
        provider=provider.name,
        model=provider.model,
        config=provider.config(),
        prompt_text=prompt,
        source_freeze=source_freeze,
        raw_response=result.raw,
        normalized_response=None,
        request_id=result.request_id,
        usage=result.usage or {},
        lane="calibration",
        target_id=case.id,
        failure=result.failure,
        tags=["calibration", case.id],
    )
    if not result.ok:
        return CaseResult(case_id=case.id, passed=False, missed_groups=[],
                          fired_failure_markers=[], execution_failure=result.failure,
                          invocation_id=invocation.invocation_id)
    graded = grade(case, result.raw)
    graded.invocation_id = invocation.invocation_id
    return graded


def write_report(path: Path, *, results: list[CaseResult], digest: str,
                 notes: list[str]) -> Path:
    payload = {
        "version": CALIBRATION_VERSION,
        "preregistration_digest": digest,
        "results": [asdict(r) for r in results],
        "notes": notes,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
