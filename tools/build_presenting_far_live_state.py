#!/usr/bin/env python3
"""Rebuild the noncanonical Presenting FAR live-research ledger.

Deterministic: every entry traces to a labelled span of
``.far/inbox/presenting-project-far.md`` or to a recorded NOT_RECOVERED search
result. Nothing here is canonical, and nothing here is Acceptance.

Run:  python tools/build_presenting_far_live_state.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial.ledger import (  # noqa: E402
    CONCEDE,
    EXACT_TRANSCRIPT_EVIDENCE,
    Ledger,
    MISSING_TRANSCRIPT_EVIDENCE,
    OPEN,
    READY_UNDER_INTERNAL_PROTOCOL,
    RECONSTRUCTED_RESEARCH_STATE,
    REFUTED,
    SOURCE_REQUIRED,
    SUSTAIN,
    Target,
    UNDERDETERMINED,
    WITHDRAW,
)

TRANSCRIPT = ".far/inbox/presenting-project-far.md"
STATE_ROOT = ROOT / ".far" / "research" / "presenting-far"
LEDGER_PATH = STATE_ROOT / "live-theory-state.json"

NOT_RECOVERED_NOTE = (
    "NOT_RECOVERED: no occurrence anywhere in the repository working tree or in "
    "any reachable object across all 400+ branches of notfoundout/Project-FAR, "
    "nor in local session state. Searched 2026-08-14."
)


def build() -> Ledger:
    ledger = Ledger(LEDGER_PATH)
    ledger.meta = {
        "schema": "far-adversarial-ledger/1",
        "status": "NONCANONICAL LIVE RESEARCH STATE",
        "not_acceptance": (
            "READY_UNDER_INTERNAL_PROTOCOL is an internal research disposition under "
            "a frozen protocol. It is not Project FAR Acceptance or Promotion, and it "
            "confers no canonical authority."
        ),
        "primary_source": TRANSCRIPT,
        "source_class": "NONCANONICAL / INCOMPLETE RECONSTRUCTION",
        "investigation": "Presenting Project FAR (Claude<->GPT adversarial), 2026-08-14",
        "research_question": (
            "Discover the minimal architecture of reasoning without inserting "
            "Project FAR / RCCD into the premises."
        ),
    }

    # -- S1 ---------------------------------------------------------------
    s1 = ledger.add_target(
        Target(
            id="PFAR-S1",
            original_formulation=(
                "NOT_RECOVERED. The exact frozen S1 statement is absent from every "
                "searched artifact. Recovered constraints only: S1 specifies a "
                "relation whose transitions are all one-rule backward applications, "
                "and it requires a completely determined transition relation at the "
                "frontier level. It never required a canonical deterministic search "
                "strategy."
            ),
            current_formulation=(
                "NOT_RECOVERED (same as original; no revision to the S1 text itself "
                "is recorded in the reconstruction). The adjudication record moved, "
                "the target text did not."
            ),
            frozen_scope="SR-B2 v2 (executable), CDE-v1 / FDI1-FDI5 determination structure",
            status=READY_UNDER_INTERNAL_PROTOCOL,
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
            provenance=f"{TRANSCRIPT}: TURN 25, CLAUDE TURN 33, GPT TURN 34",
            repository_relationship=(
                "TRANSCRIPT_AHEAD. No S1, SR-B2, CDE-v1, or FDI record exists in the "
                "canonical repository. This target has no canonical counterpart."
            ),
            authorized=False,
            supporting_arguments=[
                "Turn 33 (VERBATIM): a highly nondeterministic transition relation is "
                "still a completely determined transition relation, so LK search "
                "nondeterminism does not bear on what S1 requires.",
                "Turn 33 (VERBATIM): intra-sequent representation (lists/sets/multisets) "
                "and frontier representation are distinct analytical levels.",
            ],
            counterexamples=[],
            source_dependencies=[
                "Miller, sequent calculus / LK proof search ('1000 choices', "
                "'proofs are formless') - cited in Turn 33, artifact NOT_RECOVERED",
            ],
            formal_obligations=[],
            missing_evidence=[
                "Exact frozen S1 statement (NOT_RECOVERED)",
                "CDE-v1 definition (NOT_RECOVERED)",
                "FDI1-FDI5 determination criteria (NOT_RECOVERED)",
                "FDI-v1 definition (NOT_RECOVERED)",
                "SR-B2 v2 executable protocol text (NOT_RECOVERED)",
                "GPT Turn 34 full wording (GAP)",
                "Turn 33 final sentence (source truncates mid-sentence)",
            ],
            notes=[
                "DO NOT RESTART. S1 is internally closed under the then-current frozen "
                "protocol per GPT Turn 34. Re-running it would recycle settled work.",
                "READY here is the internal protocol disposition only. It is not "
                "Acceptance and has no canonical standing.",
            ],
        )
    )

    di3 = ledger.register_issue(
        target_id="PFAR-S1",
        claim=(
            "DI3: LK has no canonical deterministic search strategy (Miller: '1000 "
            "choices', 'proofs are formless'), therefore the calculus does not "
            "determine search structure, therefore S1 must stay OPEN."
        ),
        raised_by="claude",
        provenance=f"{TRANSCRIPT}: TURNS 25, 28, 31, 32; withdrawn in CLAUDE TURN 33",
        confidence_class=EXACT_TRANSCRIPT_EVIDENCE,
    )
    ledger.apply_action(
        di3.id,
        actor="gpt",
        action=SUSTAIN,
        rationale=(
            "GPT ran the counter-argument in its Turn 33 §3 correction: the frozen "
            "target never required a canonical deterministic strategy."
        ),
        provenance=f"{TRANSCRIPT}: CLAUDE TURN 33 reporting GPT §3",
    )
    ledger.apply_action(
        di3.id,
        actor="claude",
        action=WITHDRAW,
        rationale=(
            "VERBATIM (Turn 33): 'A highly nondeterministic transition relation is "
            "still a completely determined transition relation. My DI3 argument, run "
            "across Turns 25, 28, 31, and 32, conflated the two.' DI3 is withdrawn as "
            "a valid reason to keep S1 open and must never be re-run."
        ),
        provenance=f"{TRANSCRIPT}: CLAUDE TURN 33 (VERBATIM-RECOVERED)",
        agreement={"claude": "concede", "gpt": "sustain",
                   "note": "agreement is metadata; the argument decided this"},
    )

    conflation = ledger.register_issue(
        target_id="PFAR-S1",
        claim=(
            "Variation in intra-sequent representation (lists/sets/multisets of "
            "formulas) was merged with frontier-level representation; they are "
            "distinct analytical levels."
        ),
        raised_by="gpt",
        provenance=f"{TRANSCRIPT}: CLAUDE TURN 33 §4 (VERBATIM-RECOVERED)",
        confidence_class=EXACT_TRANSCRIPT_EVIDENCE,
    )
    ledger.apply_action(
        conflation.id,
        actor="claude",
        action=CONCEDE,
        rationale="VERBATIM (Turn 33): 'Also accepted: §4 ... and I merged them.'",
        provenance=f"{TRANSCRIPT}: CLAUDE TURN 33 (VERBATIM-RECOVERED)",
    )

    df02b = ledger.register_issue(
        target_id="PFAR-S1",
        claim=(
            "DF-02b as originally worded ('the calculus does not determine search "
            "structure') overstates the negative source finding."
        ),
        raised_by="gpt",
        provenance=f"{TRANSCRIPT}: CLAUDE TURN 33 (VERBATIM-RECOVERED)",
        confidence_class=EXACT_TRANSCRIPT_EVIDENCE,
    )
    ledger.apply_action(
        df02b.id,
        actor="claude",
        action=CONCEDE,
        rationale=(
            "VERBATIM (Turn 33) revised record: 'No eligible source encountered so "
            "far has been certified to determine the frozen frontier-level search "
            "structure.' Not 'the calculus does not determine search structure.'"
        ),
        provenance=f"{TRANSCRIPT}: CLAUDE TURN 33 (VERBATIM-RECOVERED)",
    )
    s1.concessions.append(conflation.id)
    s1.withdrawn_objections.append(di3.id)
    s1.defeated_objections.append(di3.id)

    # -- frozen target/protocol block T1-T8 --------------------------------
    ledger.add_target(
        Target(
            id="PFAR-T1-T8",
            original_formulation=(
                "NOT_RECOVERED. GPT Turn 4 froze targets/protocol items T1-T8 after "
                "replacing 'irredundant size' with intrinsic minimum generating rank "
                "and introducing a translation-rank spectrum."
            ),
            current_formulation="NOT_RECOVERED.",
            frozen_scope="NOT_RECOVERED",
            status=SOURCE_REQUIRED,
            confidence_class=MISSING_TRANSCRIPT_EVIDENCE,
            provenance=f"{TRANSCRIPT}: GPT TURN 4 (RECONSTRUCTED-HIGH)",
            repository_relationship="TRANSCRIPT_AHEAD; no canonical counterpart.",
            authorized=False,
            missing_evidence=[
                f"T1-T8 definitions. {NOT_RECOVERED_NOTE}",
                "Turns 6-11 (GAP), 14 (GAP), 18-22 (GAP), 24 (GAP)",
            ],
            notes=[
                "The successor target queue after S1 lives inside T1-T8. Without these "
                "definitions the next dependency-valid Presenting FAR target cannot be "
                "identified, let alone executed."
            ],
        )
    )

    # -- source freeze -----------------------------------------------------
    ledger.add_target(
        Target(
            id="PFAR-E0",
            original_formulation=(
                "NOT_RECOVERED. Turn 13 fixed the immediate sequence: freeze E0, "
                "native extraction, witnesses, joint profiles, common theory, "
                "frame/prior-art comparison, and only then minimality."
            ),
            current_formulation="NOT_RECOVERED.",
            frozen_scope="NOT_RECOVERED",
            status=SOURCE_REQUIRED,
            confidence_class=MISSING_TRANSCRIPT_EVIDENCE,
            provenance=f"{TRANSCRIPT}: GPT TURN 13 (RECONSTRUCTED-HIGH)",
            repository_relationship="TRANSCRIPT_AHEAD; no canonical counterpart.",
            authorized=False,
            missing_evidence=[f"E0 source-corpus freeze contents. {NOT_RECOVERED_NOTE}"],
            notes=[
                "E0 is the eligible-evidence set for every Presenting FAR target. "
                "Without it no lane can be given equivalent frozen evidence, so blind "
                "first passes cannot be executed at all for this line of work."
            ],
        )
    )

    # -- RC1 / RC2 ---------------------------------------------------------
    ledger.add_target(
        Target(
            id="PFAR-RC1",
            original_formulation="NOT_RECOVERED (RC1 research contract text).",
            current_formulation="Superseded by RC2; not re-freezable as written.",
            frozen_scope="NOT_RECOVERED",
            status=REFUTED,
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
            provenance=f"{TRANSCRIPT}: GPT TURN 15 (RECONSTRUCTED-HIGH)",
            repository_relationship="TRANSCRIPT_AHEAD; no canonical counterpart.",
            authorized=False,
            missing_evidence=[f"RC1 contract text. {NOT_RECOVERED_NOTE}"],
            notes=["Verdict: RC1 was not safe to hash/freeze."],
        )
    )
    for blocker in [
        "RC1 instance-class quantification is unspecified.",
        "RC1 interpretation grammar is undefined.",
        "RC1 lexical exclusion is RCCD-driven.",
        "RC1 c0 calibration status is dialogue-derived.",
        "RC1 S11 discrete-gradient conflicts with C3.",
        "RC1 leaks its frame.",
    ]:
        issue = ledger.register_issue(
            target_id="PFAR-RC1",
            claim=blocker,
            raised_by="gpt",
            provenance=f"{TRANSCRIPT}: GPT TURN 15 (RECONSTRUCTED-HIGH)",
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
        )
        ledger.apply_action(
            issue.id,
            actor="claude",
            action=CONCEDE,
            rationale="Claude Turn 16 produced RC2 instead of freezing RC1.",
            provenance=f"{TRANSCRIPT}: CLAUDE TURN 16 (GAP for exact wording)",
        )

    ledger.add_target(
        Target(
            id="PFAR-RC2",
            original_formulation="NOT_RECOVERED (RC2 research contract text; Turn 16 GAP).",
            current_formulation=(
                "NOT_RECOVERED. Turn 17 verdict: still not safe to hash, pending five "
                "repairs."
            ),
            frozen_scope="NOT_RECOVERED",
            status=UNDERDETERMINED,
            confidence_class=MISSING_TRANSCRIPT_EVIDENCE,
            provenance=f"{TRANSCRIPT}: GPT TURN 17 (RECONSTRUCTED-HIGH); TURNS 18-22 GAP",
            repository_relationship="TRANSCRIPT_AHEAD; no canonical counterpart.",
            authorized=False,
            missing_evidence=[
                f"RC2 contract text. {NOT_RECOVERED_NOTE}",
                "Turns 18-22 (GAP): whether the five Turn 17 repairs were discharged "
                "is not recoverable. Absence of a recorded resolution is not evidence "
                "that the turns did not occur.",
            ],
            notes=[
                "Do not infer from the GAP that RC2 remained unrepaired; equally, do "
                "not infer that it was repaired.",
            ],
        )
    )
    for repair in [
        "S2 requires an explicit constraint/propagator association.",
        "S7 requires paired concrete/abstract transfer maps and correctly typed "
        "native structure.",
        "S7 requires an outcome-independent rationale.",
        "G2/G3 must be standard finite-tuple first-order with no parameters.",
        "An explicit determination invariant is required: a = a' implies "
        "S_{i,a} = S_{i,a'}.",
    ]:
        ledger.register_issue(
            target_id="PFAR-RC2",
            claim=repair,
            raised_by="gpt",
            provenance=f"{TRANSCRIPT}: GPT TURN 17 (RECONSTRUCTED-HIGH)",
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
        )

    # -- retrieval / eligibility protocol ---------------------------------
    ledger.add_target(
        Target(
            id="PFAR-SRB2",
            original_formulation=(
                "SR-B2 v1: judged infeasible and retired (Turn 26). SR-B2 v2: frozen "
                "as executable. Exact text of neither version is recovered."
            ),
            current_formulation="SR-B2 v2 (executable). NOT_RECOVERED.",
            frozen_scope="NOT_RECOVERED",
            status=SOURCE_REQUIRED,
            confidence_class=MISSING_TRANSCRIPT_EVIDENCE,
            provenance=f"{TRANSCRIPT}: TURNS 23, 26, 27, 28, 32 (RECONSTRUCTED-HIGH)",
            repository_relationship="TRANSCRIPT_AHEAD; no canonical counterpart.",
            authorized=False,
            missing_evidence=[
                f"SR-B2 v1 and v2 text. {NOT_RECOVERED_NOTE}",
                f"NM-v1 retrieval definition. {NOT_RECOVERED_NOTE}",
                f"K-P1 strictness criterion. {NOT_RECOVERED_NOTE}",
                f"FDI-v1 definition. {NOT_RECOVERED_NOTE}",
            ],
            notes=[
                "Recovered protocol facts, definitions absent: broad NM-v1 retrieval "
                "retained while K-P1 made strict (Turn 27); all six queries mandatory "
                "so selective retrieval cannot silently decide an outcome (Turn 28); "
                "'direct instantiation' means specialization plus source-internal "
                "definitional expansion, excluding new primitive structure and "
                "cross-source assembly (Turn 23).",
            ],
        )
    )

    # -- repository-side successor programme ------------------------------
    ledger.add_target(
        Target(
            id="REPO-UPP-SR-001-W1",
            original_formulation=(
                "SR-W1-ABSENCE-REPRESENTATION: adjudicate the determinate-absence "
                "representation for the bounded-v1 successor repair (H1 local/typed "
                "degenerate vs H2 applicability-indexed vs H4 new global status), "
                "with falsification attempts recorded and H4 requiring proof of "
                "necessity."
            ),
            current_formulation=(
                "Unchanged from its registration in "
                "docs/research/upp-successor-repair-program-v1.0.md."
            ),
            frozen_scope=(
                "Frozen bounded-v1 source f6645a77f3b0af0b12897fa9bc2c329cdb345261; "
                "defects XA-001 to XA-005; forbidden-repair list."
            ),
            status=OPEN,
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
            provenance=(
                "docs/research/upp-successor-repair-program-v1.0.md; "
                "docs/governance/open-problems-register.md OP-22; "
                "docs/project-status.md (canonical repository state)"
            ),
            repository_relationship=(
                "REPO_AHEAD. Fully specified canonically and untouched by the "
                "Presenting FAR investigation, which never reached the bounded-v1 "
                "successor line."
            ),
            authorized=True,
            source_dependencies=[
                "docs/research/upp-successor-repair-program-v1.0.md",
                "docs/audits/bounded-v1-three-lane-cross-audit-adjudication-v1.0.md",
                "docs/governance/bounded-v1-closure-source-freeze-f6645a77.md",
                "docs/governance/limitations-register.md",
            ],
            formal_obligations=[
                "Determinate absence must be representable distinctly from epistemic "
                "Unknown wherever the repaired theorem requires it (XA-005).",
            ],
            notes=[
                "This is the only fully specified, canonically authorized, "
                "dependency-valid live target found in this run. Execution still "
                "requires both adversarial lanes.",
            ],
        )
    )
    ledger.add_target(
        Target(
            id="REPO-UPP-SR-001-W2",
            original_formulation=(
                "SR-W2-W9-REPAIR: settle the exact weakest true W9 successor theorem "
                "over the frozen C*/E*/P*/closure/equivalence domain, testing "
                "questions A-D without assuming them."
            ),
            current_formulation="Unchanged from registration.",
            frozen_scope="As SR-W1; K-matrix corners must be derivable.",
            status=OPEN,
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
            provenance="docs/research/upp-successor-repair-program-v1.0.md",
            repository_relationship="REPO_AHEAD.",
            authorized=True,
            depends_on=["REPO-UPP-SR-001-W1"],
            source_dependencies=[
                "docs/research/upp-successor-repair-program-v1.0.md",
                "docs/audits/bounded-v1-three-lane-cross-audit-adjudication-v1.0.md",
            ],
            notes=["Blocked behind SR-W1 by the program's own declared sequencing."],
        )
    )
    return ledger


def main() -> int:
    ledger = build()
    path = ledger.save()
    print(f"wrote {path}")
    print(f"digest {ledger.digest()}")
    print(f"targets {len(ledger.targets)} issues {len(ledger.issues)}")
    nxt = ledger.next_target()
    print(f"next dependency-valid authorized target: {nxt.id if nxt else 'NONE'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
