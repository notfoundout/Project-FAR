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
    Dependency,
    EXACT_TRANSCRIPT_EVIDENCE,
    GOVERNANCE_DECISION_REQUIRED,
    Ledger,
    MISSING_TRANSCRIPT_EVIDENCE,
    OBLIGATION_FORMAL,
    OBLIGATION_SOURCE,
    OPEN,
    READY_UNDER_INTERNAL_PROTOCOL,
    REBUT,
    RECONSTRUCTED_RESEARCH_STATE,
    REFUTED,
    SOURCE_REQUIRED,
    STATUS_DERIVED,
    STATUS_RECORDED,
    Target,
    UNDERDETERMINED,
    WITHDRAW,
)

TRANSCRIPT = ".far/inbox/presenting-project-far.md"
ADDENDUM = ".far/inbox/presenting-project-far-recovery-addendum-2026-08-14.md"
STATE_ROOT = ROOT / ".far" / "research" / "presenting-far"
LEDGER_PATH = STATE_ROOT / "live-theory-state.json"

RESEARCH_STATE_VERSION = "v3"

# Corrected scope. The v1 ledger asserted that no Presenting FAR protocol
# identifier occurred anywhere; the addendum shows that was true only of
# repository and local-file search, not of recoverable conversation state.
NOT_RECOVERED_NOTE = (
    "NOT_RECOVERED_IN_REPOSITORY: no occurrence in the repository working tree, "
    "in any reachable object across all branches of notfoundout/Project-FAR, or "
    "in local session state (searched 2026-08-14). This is a statement about "
    "file-based search only; retained conversation state is a separate evidence "
    "channel and did yield further content, per the recovery addendum."
)


def build() -> Ledger:
    ledger = Ledger(LEDGER_PATH)
    ledger.meta = {
        "schema": "far-adversarial-ledger/2",
        "reducer": "far-adversarial-reducer/2",
        "status": "NONCANONICAL LIVE RESEARCH STATE",
        "not_acceptance": (
            "READY_UNDER_INTERNAL_PROTOCOL is an internal research disposition under "
            "a frozen protocol. It is not Project FAR Acceptance or Promotion, and it "
            "confers no canonical authority."
        ),
        "status_basis_note": (
            "Targets carrying RECORDED_TRANSCRIPT_DISPOSITION hold a status this "
            "executor read out of the reconstruction, not one it derived. Recorded "
            "dispositions do not satisfy downstream dependency edges by default."
        ),
        "research_state_version": RESEARCH_STATE_VERSION,
        "successor_of": (
            "v1 (continuation-freeze-v1.md, original reconstruction); "
            "v2 (continuation-freeze-v2.md, executor audit repair). Both are "
            "preserved unamended. v3 ingests the recovery addendum."
        ),
        "primary_source": TRANSCRIPT,
        "supplementary_source": ADDENDUM,
        "supplementary_source_class": (
            "NONCANONICAL / RECOVERED CONVERSATION-STATE EVIDENCE. Not a verbatim "
            "scrape of the shared conversation URL: the public fetch did not expose "
            "the conversation body. Items are RECONSTRUCTED-HIGH unless labelled "
            "otherwise and must not be upgraded to verbatim transcript."
        ),
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
            status_basis=STATUS_RECORDED,
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
            provenance=(
                f"{TRANSCRIPT}: TURN 25, CLAUDE TURN 33, GPT TURN 34; "
                f"{ADDENDUM}: TURNS 25, 32, 34 (RECONSTRUCTED-HIGH)"
            ),
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
                "and frontier representation are distinct analytical levels; the earlier "
                "argument merged them.",
                "Turn 33 (VERBATIM) revised record, replacing the earlier DF-02b wording: "
                "'No eligible source encountered so far has been certified to determine "
                "the frozen frontier-level search structure.' Not 'the calculus does not "
                "determine search structure.'",
                "FDI-v1 (addendum Turn 32): a five-condition frontier-DI certificate "
                "for frozen S1, requiring source-defined partial derivations, an "
                "open-leaf frontier with its multiplicity/structure, one-step "
                "source-induced evolution, and frontier-quotient well-definedness. "
                "Partial derivations alone were explicitly insufficient.",
                "CDE-v1 (addendum Turn 34): canonical definitional expansions from "
                "source-defined structure with no free methodological parameters.",
                "Adjudication route (addendum Turn 34): FDI4 satisfied by DI2; CDE-v1 "
                "fixed; Liang-Miller member 2 classified DIRECT under DI1 plus the "
                "FDI1-FDI5 structure; c0 survived; S1 adjudicated READY.",
            ],
            concessions=[
                "Turn 33 §4: Claude accepted that intra-sequent and frontier "
                "representation had been conflated.",
                "Turn 33: Claude weakened the DF-02b negative source claim.",
            ],
            source_dependencies=[
                "Miller, 'A Survey of the Proof-Theoretic Foundations of Logic "
                "Programming', arXiv:2109.01483 (2021). SOURCE-IDENTIFICATION-HIGH "
                "candidate for the Turn 33 '1000 choices' / 'proofs are formless' "
                "reference. An identification, not transcript wording.",
                "Liang and Miller, 'Focusing and Polarization in Intuitionistic "
                "Logic', arXiv:0708.2252 (2007). SOURCE-IDENTIFICATION-HIGH candidate "
                "for 'Liang-Miller member 2' in the retained Turn 34 state. Do not "
                "collapse the two without the original candidate ledger: the dialogue "
                "may have used them as distinct members of the source set.",
            ],
            missing_evidence=[
                "Exact frozen S1 statement (still NOT_RECOVERED)",
                "Exact full CDE-v1 definition (rule partially recovered in v3)",
                "Exact FDI1-FDI5 clause text; the addendum recovers the five "
                "conditions' content but explicitly warns against inventing the "
                "phrase-to-label mapping",
                "Exact SR-B2 v2 protocol text (procedure recovered in v3)",
                "GPT Turn 34 full wording (adjudication route partially recovered)",
                "Turn 33 final sentence (source truncates mid-sentence; the addendum "
                "recovered no completion)",
            ],
            notes=[
                "DO NOT RESTART. S1 is internally closed under the then-current frozen "
                "protocol per GPT Turn 34. Re-running it would recycle settled work.",
                "READY here is the internal protocol disposition only. It is not "
                "Acceptance and has no canonical standing.",
                "status_basis is RECORDED_TRANSCRIPT_DISPOSITION: this executor did not "
                "derive READY and could not, since the frozen protocol is unrecovered.",
            ],
        )
    )

    # The one registered objection against S1, and its actual lifecycle: Claude
    # raised it, GPT rebutted it, Claude withdrew it. GPT never had standing to
    # end it, and did not.
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
        action=REBUT,
        rationale=(
            "GPT's Turn 33 §3 correction: the frozen target never required a canonical "
            "deterministic strategy, only a completely determined transition relation. "
            "This is a rebuttal; GPT could not and did not end the objection."
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
            "across Turns 25, 28, 31, and 32, conflated the two.' The owner withdrew; "
            "that is what defeated it."
        ),
        provenance=f"{TRANSCRIPT}: CLAUDE TURN 33 (VERBATIM-RECOVERED)",
        agreement={"claude": "withdraw", "gpt": "rebut",
                   "note": "agreement is metadata; the owner's withdrawal decided this"},
    )

    for statement in (
        "Exact frozen S1 statement",
        "CDE-v1 and FDI1-FDI5 determination criteria",
        "SR-B2 v2 executable protocol text",
    ):
        ledger.register_obligation(
            target_id="PFAR-S1", kind=OBLIGATION_SOURCE, statement=statement,
            raised_by="reconstruction",
            provenance=f"{TRANSCRIPT}; {NOT_RECOVERED_NOTE}",
        )

    # -- S2, revealed by the Turn 24 precondition stop ---------------------
    ledger.add_target(
        Target(
            id="PFAR-S2",
            original_formulation=(
                "NOT_RECOVERED. S2 is known only as the second gating S-target named "
                "alongside S1 in the addendum's Turn 24 precondition stop."
            ),
            current_formulation="NOT_RECOVERED.",
            frozen_scope="SR-B2 v2; same determination machinery as S1 (unrecovered).",
            status=UNDERDETERMINED,
            status_basis=STATUS_RECORDED,
            confidence_class=MISSING_TRANSCRIPT_EVIDENCE,
            provenance=f"{ADDENDUM}: GPT TURN 24 (RECONSTRUCTED-HIGH)",
            repository_relationship="TRANSCRIPT_AHEAD; no canonical counterpart.",
            authorized=False,
            missing_evidence=[
                "Exact S2 statement.",
                "S2's disposition. The reconstruction records that S1 reached READY "
                "and says nothing about S2. Do not infer S2's status from S1's.",
            ],
            notes=[
                "Turn 24 (addendum): if S1 or S2 were non-READY, the E0 shared-content "
                "fragments became UNTESTABLE, no substitute domain or fragment was "
                "permitted, and the correct outcome was a PRECONDITION STOP / "
                "domain-instantiation failure rather than an invented replacement.",
                "S2's disposition therefore gates the E0 fragments independently of S1.",
            ],
        )
    )
    ledger.register_obligation(
        target_id="PFAR-S2", kind=OBLIGATION_SOURCE,
        statement="Exact S2 statement and its recorded disposition",
        raised_by="reconstruction", provenance=f"{ADDENDUM}: GPT TURN 24",
    )

    # -- the recorded next Presenting FAR action ---------------------------
    ledger.add_target(
        Target(
            id="PFAR-S6-S7",
            original_formulation=(
                "NOT_RECOVERED. Recorded only as the remaining action after the Turn "
                "34 S1 adjudication: 'S6 -> S7'."
            ),
            current_formulation="NOT_RECOVERED.",
            frozen_scope="NOT_RECOVERED.",
            status=SOURCE_REQUIRED,
            status_basis=STATUS_RECORDED,
            confidence_class=MISSING_TRANSCRIPT_EVIDENCE,
            provenance=f"{ADDENDUM}: GPT TURN 34 (RECONSTRUCTED-HIGH)",
            repository_relationship="TRANSCRIPT_AHEAD; no canonical counterpart.",
            authorized=False,
            missing_evidence=[
                "Exact S6 and S7 statements.",
                "What the S6 -> S7 transition requires.",
                "Whether S3, S4, and S5 exist and what their dispositions were.",
            ],
            notes=[
                "This is the successor step the Presenting FAR investigation actually "
                "recorded as next. It is the first time the reconstruction names one: "
                "v1 and v2 could only say the successor queue lived inside T1-T8.",
                "It remains unexecutable. Naming the next action is not the same as "
                "recovering its content, and inventing S6 or S7 is forbidden.",
            ],
        )
    )
    ledger.register_obligation(
        target_id="PFAR-S6-S7", kind=OBLIGATION_SOURCE,
        statement="Exact S6 and S7 statements and the S6 -> S7 transition requirement",
        raised_by="reconstruction", provenance=f"{ADDENDUM}: GPT TURN 34",
    )

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
            status_basis=STATUS_RECORDED,
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
    ledger.register_obligation(
        target_id="PFAR-T1-T8", kind=OBLIGATION_SOURCE,
        statement="T1-T8 frozen target and protocol definitions",
        raised_by="reconstruction", provenance=NOT_RECOVERED_NOTE,
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
            status_basis=STATUS_RECORDED,
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
    ledger.register_obligation(
        target_id="PFAR-E0", kind=OBLIGATION_SOURCE,
        statement="E0 frozen source-corpus contents",
        raised_by="reconstruction", provenance=NOT_RECOVERED_NOTE,
    )

    # -- RC1 / RC2 ---------------------------------------------------------
    ledger.add_target(
        Target(
            id="PFAR-RC1",
            original_formulation="NOT_RECOVERED (RC1 research contract text).",
            current_formulation="Superseded by RC2; not re-freezable as written.",
            frozen_scope="NOT_RECOVERED",
            status=REFUTED,
            status_basis=STATUS_RECORDED,
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
            target_id="PFAR-RC1", claim=blocker, raised_by="gpt",
            provenance=f"{TRANSCRIPT}: GPT TURN 15 (RECONSTRUCTED-HIGH)",
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
        )
        # Claude was the challenged party and conceded: the objection stands
        # against RC1, which is why RC1 is REFUTED rather than resolved.
        ledger.apply_action(
            issue.id, actor="claude", action=CONCEDE,
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
            status_basis=STATUS_RECORDED,
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
            target_id="PFAR-RC2", claim=repair, raised_by="gpt",
            provenance=f"{TRANSCRIPT}: GPT TURN 17 (RECONSTRUCTED-HIGH)",
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
        )

    # -- retrieval / eligibility protocol ---------------------------------
    ledger.add_target(
        Target(
            id="PFAR-SRB2",
            original_formulation=(
                "SR-B2 v1: retired as capability-infeasible (Turn 26). Under v1, S1 "
                "remained OPEN until a finite retrieval procedure was exhausted; "
                "strong negative-looking evidence could not by itself produce "
                "SOURCE-FAIL before the registered search completed (Turn 25)."
            ),
            current_formulation=(
                "SR-B2 v2, executable finite search procedure (RECOVERED_PARTIALLY, "
                "addendum Turn 26): six fixed queries per OPEN target; ten results "
                "per query; up to five NM-v1 near-matches eligible for follow-up; two "
                "title/author follow-up queries per near-match; an EXACT/DIRECT "
                "positive permits an early positive stop; a negative SOURCE-FAIL "
                "requires exhaustion of all prescribed invocations; S1 reruns from "
                "query 1 under the repaired protocol. Exact protocol text still "
                "unrecovered."
            ),
            frozen_scope=(
                "Two-stage design (addendum Turn 27): broad NM-v1 recall at "
                "retrieval, strict K-P1 precision at admissibility."
            ),
            status=SOURCE_REQUIRED,
            status_basis=STATUS_RECORDED,
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
            provenance=(
                f"{TRANSCRIPT}: TURNS 23, 26, 27, 28, 32 (RECONSTRUCTED-HIGH); "
                f"{ADDENDUM}: TURNS 23, 25, 26, 27, 28, 32 (RECONSTRUCTED-HIGH)"
            ),
            repository_relationship="TRANSCRIPT_AHEAD; no canonical counterpart.",
            authorized=False,
            supporting_arguments=[
                "NM-v1 (addendum Turn 27): deliberately broad at retrieval — same "
                "formal family, structural role, or provenance qualifies a near-match "
                "for inspection.",
                "K-P1 (addendum Turn 27): strict at final eligibility. A focused-LK "
                "paper may enter the N1/near-match pool and still fail admissibility.",
                "Direct instantiation (addendum Turn 23): specialization plus "
                "source-internal definitional expansion, bounded by an explicit "
                "DI1-DI6 boundary; analyst-supplied primitive structure and "
                "cross-source assembly both excluded.",
                "Exhaustion rule (Turns 26/28): all six queries are mandatory, so "
                "selective query execution cannot manufacture a negative source "
                "result.",
            ],
            missing_evidence=[
                "Exact SR-B2 v1 and v2 protocol text (procedure recovered, wording not).",
                "Exact NM-v1 criterion wording (criterion recovered, wording not).",
                "Exact K-P1 test wording (role recovered, wording not).",
                "Exact DI1-DI6 clause text.",
                "The six fixed queries themselves.",
            ],
            notes=[
                "Upgraded in v3 from 'an executable v2 was frozen' to a recoverable "
                "finite search procedure, per the recovery addendum.",
            ],
        )
    )
    for statement in (
        "Exact SR-B2 v2 protocol text and the six fixed queries",
        "Exact DI1-DI6 direct-instantiation boundary text",
    ):
        ledger.register_obligation(
            target_id="PFAR-SRB2", kind=OBLIGATION_SOURCE, statement=statement,
            raised_by="reconstruction", provenance=f"{ADDENDUM}: TURNS 23, 26",
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
            status_basis=STATUS_DERIVED,
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
            frozen_evidence_paths=[
                "docs/research/upp-successor-repair-program-v1.0.md",
                "docs/audits/bounded-v1-three-lane-cross-audit-adjudication-v1.0.md",
                "docs/governance/bounded-v1-closure-source-freeze-f6645a77.md",
                "docs/governance/limitations-register.md",
            ],
            notes=[
                "The next fully specified, authorized executable research path while "
                "Presenting FAR is source-blocked. Not a proven global critical path.",
                "Execution still requires both adversarial lanes.",
            ],
        )
    )
    ledger.register_obligation(
        target_id="REPO-UPP-SR-001-W1", kind=OBLIGATION_FORMAL,
        statement=(
            "Determinate absence must be representable distinctly from epistemic "
            "Unknown wherever the repaired theorem requires it (XA-005)."
        ),
        raised_by="registration",
        provenance="docs/research/upp-successor-repair-program-v1.0.md",
    )

    # -- registered governance conflict -----------------------------------
    # Recorded, not resolved. Repairing the higher-ranked surface would be a
    # canonical documentation change this noncanonical work cannot authorize,
    # and the charter forbids choosing between conflicting authorities.
    ledger.add_target(
        Target(
            id="REPO-AUTHORITY-CONFLICT-001",
            original_formulation=(
                "README.md:14-16 and docs/governance/central-research-program.md:19-21 "
                "present POST-TUE-UPP-001's terminal adjudication as a theorem proved "
                "with a complete dependency audit, with no mention of the 2026-08-13 "
                "bounded-v1 finding. docs/project-status.md:31-37 records that same "
                "derivation as FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED and defective "
                "over part of its stated domain (XA-001-XA-005), and registers "
                "UPP-SR-001/OP-22 as the successor repair. All three are current "
                "authority surfaces; README.md outranks project-status.md in the "
                "navigation order project-status.md itself declares."
            ),
            current_formulation=(
                "Unresolved. The affected inference — that the current-authority "
                "surfaces agree on the standing of POST-TUE-UPP-001 — is stopped."
            ),
            frozen_scope=(
                "Presentation of current standing, not the frozen historical record. "
                "project-status.md is explicit that the terminal adjudication string "
                "is not silently rewritten."
            ),
            status=GOVERNANCE_DECISION_REQUIRED,
            status_basis=STATUS_DERIVED,
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
            provenance=(
                "README.md:14-16; docs/governance/central-research-program.md:19-21; "
                "docs/project-status.md:31-37. Surfaced by an independent parallel "
                "reconstruction and verified directly against the files."
            ),
            repository_relationship="CONFLICT",
            authorized=False,
            notes=[
                "Charter action is to surface, not to choose: AGENTS.md section 4 and "
                "CLAUDE.md Authority both forbid silently resolving a conflict between "
                "current-authority surfaces.",
                "Repair requires separate governance authorization. It is a canonical "
                "documentation change and is out of scope for noncanonical research "
                "state.",
                "This executor's own earlier delta asserted no authority conflict "
                "existed. That assertion was the defect and is withdrawn.",
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
            status_basis=STATUS_DERIVED,
            confidence_class=RECONSTRUCTED_RESEARCH_STATE,
            provenance="docs/research/upp-successor-repair-program-v1.0.md",
            repository_relationship="REPO_AHEAD.",
            authorized=True,
            # SR-W2 needs SR-W1 to have established a representation. A refuted,
            # source-blocked, or governance-blocked SR-W1 redirects the program;
            # it does not unlock this.
            depends_on=[Dependency(target_id="REPO-UPP-SR-001-W1",
                                   requires=[READY_UNDER_INTERNAL_PROTOCOL])],
            frozen_evidence_paths=[
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
    print(f"targets {len(ledger.targets)} issues {len(ledger.issues)} "
          f"obligations {len(ledger.obligations)}")
    nxt = ledger.next_target()
    print(f"next dependency-valid authorized target: {nxt.id if nxt else 'NONE'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
