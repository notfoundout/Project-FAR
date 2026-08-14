"""The adversarial relay loop.

This replaces exactly one manual activity: carrying messages between the Claude
lane and the GPT lane. It decides nothing that the manual process did not
already decide by rule.

    frozen target -> blind first passes -> raw preservation -> issue extraction
    -> controlled cross-audit -> typed actions -> terminal disposition
    -> next dependency-valid target

The orchestrator is the only writer. Lanes receive prompts and return text.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from . import protocol
from .evidence import EvidenceStore
from .ledger import (
    BLOCKING_ISSUE_STATES,
    GOVERNANCE_DECISION_REQUIRED,
    Ledger,
    RECONSTRUCTED_RESEARCH_STATE,
    SOURCE_REQUIRED,
    Target,
    UNDERDETERMINED,
)
from .providers import INVALID_PROVIDER_OUTPUT, Provider, ProviderResult

# Stop reasons that mean "this run stopped", not "this target is settled".
EXECUTION_STOP = "EXECUTION_STOP"
TARGET_TERMINAL = "TARGET_TERMINAL"
NO_ELIGIBLE_TARGET = "NO_ELIGIBLE_TARGET"
ROUND_LIMIT = "ROUND_LIMIT"


@dataclass
class LanePass:
    lane: str
    prompt: str
    result: ProviderResult
    parsed: dict[str, Any] | None
    invocation_id: str | None = None

    @property
    def failed(self) -> bool:
        return not self.result.ok or self.parsed is None

    @property
    def failure_code(self) -> str | None:
        if not self.result.ok:
            return self.result.failure
        if self.parsed is None:
            return INVALID_PROVIDER_OUTPUT
        return None


@dataclass
class RunReport:
    stop_reason: str
    detail: str = ""
    targets_closed: list[str] = field(default_factory=list)
    execution_failures: list[str] = field(default_factory=list)
    rounds: int = 0

    @property
    def is_epistemic_stop(self) -> bool:
        """A resource ceiling is never a theoretical stalemate."""
        return self.stop_reason in {TARGET_TERMINAL, NO_ELIGIBLE_TARGET}


class Orchestrator:
    def __init__(
        self,
        *,
        ledger: Ledger,
        store: EvidenceStore,
        claude: Provider,
        gpt: Provider,
        evidence_loader: Callable[[Target], dict[str, str]],
        source_freeze: str,
        max_rounds_per_target: int = 4,
        parallel: bool = True,
    ):
        self.ledger = ledger
        self.store = store
        self.claude = claude
        self.gpt = gpt
        self.evidence_loader = evidence_loader
        self.source_freeze = source_freeze
        self.max_rounds_per_target = max_rounds_per_target
        self.parallel = parallel
        self.lane_prompts: dict[str, list[str]] = {"claude": [], "gpt": []}

    # -- provider plumbing -------------------------------------------------

    def _invoke(self, provider: Provider, lane: str, target_id: str, prompt: str,
                parser: Callable[[str], Any], tags: list[str]) -> LanePass:
        self.lane_prompts.setdefault(lane, []).append(prompt)
        result = provider.complete(prompt)
        parsed = parser(result.raw) if result.ok else None
        invocation = self.store.record(
            provider=provider.name,
            model=provider.model,
            config=provider.config(),
            prompt_text=prompt,
            source_freeze=self.source_freeze,
            raw_response=result.raw,
            normalized_response=parsed,
            request_id=result.request_id,
            usage=result.usage or {},
            started_at=result.started_at or None,
            finished_at=result.finished_at or None,
            lane=lane,
            target_id=target_id,
            failure=result.failure or (INVALID_PROVIDER_OUTPUT if parsed is None else None),
            tags=tags,
        )
        return LanePass(lane=lane, prompt=prompt, result=result, parsed=parsed,
                        invocation_id=invocation.invocation_id)

    # -- blind first passes -------------------------------------------------

    def blind_first_passes(self, target: Target) -> dict[str, LanePass]:
        """Run both lanes over equivalent frozen evidence without cross-exposure.

        Both prompts are built before either provider is called, so neither can
        depend on the other's output even in principle. Raw output is preserved
        before any cross-exchange happens.
        """
        evidence = self.evidence_loader(target)
        claude_prompt = protocol.first_pass_prompt(
            role=protocol.CLAUDE_ROLE, target=target, evidence=evidence,
            source_freeze=self.source_freeze,
        )
        gpt_prompt = protocol.first_pass_prompt(
            role=protocol.GPT_ROLE, target=target, evidence=evidence,
            source_freeze=self.source_freeze,
        )
        jobs = {
            "claude": (self.claude, claude_prompt),
            "gpt": (self.gpt, gpt_prompt),
        }
        tags = ["first-pass", target.id]

        def run(item):
            lane, (provider, prompt) = item
            return lane, self._invoke(provider, lane, target.id, prompt,
                                      protocol.parse_first_pass, tags)

        if self.parallel:
            with ThreadPoolExecutor(max_workers=2) as pool:
                passes = dict(pool.map(run, jobs.items()))
        else:
            passes = dict(run(item) for item in jobs.items())
        return passes

    # -- issue extraction ---------------------------------------------------

    def extract_issues(self, target: Target, passes: dict[str, LanePass]) -> list[str]:
        """Register each lane's objections with stable, content-addressed ids.

        Objections are never merged by similarity. Two lanes that phrase the
        same worry differently produce two issues, and reconciling them
        requires an explicit recorded action from a lane.
        """
        registered: list[str] = []
        for lane in sorted(passes):
            lane_pass = passes[lane]
            if lane_pass.parsed is None:
                continue
            for objection in lane_pass.parsed["objections"]:
                issue = self.ledger.register_issue(
                    target_id=target.id,
                    claim=objection["claim"],
                    raised_by=lane,
                    provenance=f"first-pass:{lane}:{lane_pass.invocation_id}",
                    confidence_class=RECONSTRUCTED_RESEARCH_STATE,
                )
                if issue.id not in registered:
                    registered.append(issue.id)
            for request in lane_pass.parsed["source_requests"]:
                if request not in target.source_dependencies:
                    target.source_dependencies.append(request)
            for obligation in lane_pass.parsed["formal_obligations"]:
                if obligation not in target.formal_obligations:
                    target.formal_obligations.append(obligation)
        return registered

    # -- controlled cross audit ---------------------------------------------

    def cross_audit(self, target: Target, issue_ids: list[str]) -> list[LanePass]:
        """Audit live issues one by one, each lane answering the other's.

        Only live issues are sent. Nothing that has already been conceded,
        withdrawn, or rejected is resent, so a defeated argument cannot be
        recycled by transcript growth.
        """
        evidence = self.evidence_loader(target)
        known = {iid for iid in issue_ids if iid in self.ledger.issues}
        passes: list[LanePass] = []
        for lane, provider, role in (
            ("claude", self.claude, protocol.CLAUDE_ROLE),
            ("gpt", self.gpt, protocol.GPT_ROLE),
        ):
            # A lane answers the objections raised against it by the other lane.
            addressed = [
                self.ledger.issues[iid]
                for iid in sorted(known)
                if self.ledger.issues[iid].raised_by != lane
                and self.ledger.issues[iid].is_live()
            ]
            if not addressed:
                continue
            prompt = protocol.cross_audit_prompt(
                role=role, target=target, issues=addressed, evidence=evidence,
                source_freeze=self.source_freeze,
            )
            lane_pass = self._invoke(
                provider, lane, target.id, prompt,
                lambda raw: protocol.parse_cross_audit(raw, {i.id for i in addressed}),
                ["cross-audit", target.id],
            )
            passes.append(lane_pass)
            if lane_pass.parsed is None:
                continue
            for response in lane_pass.parsed:
                self.ledger.apply_action(
                    response["issue_id"],
                    actor=lane,
                    action=response["action"],
                    rationale=response["rationale"],
                    provenance=f"cross-audit:{lane}:{lane_pass.invocation_id}",
                    invocation_id=lane_pass.invocation_id,
                    revised_claim=response["revised_claim"],
                )
        return passes

    # -- target loop ---------------------------------------------------------

    def run_target(self, target: Target) -> RunReport:
        report = RunReport(stop_reason=ROUND_LIMIT)
        for round_index in range(self.max_rounds_per_target):
            report.rounds += 1
            if round_index == 0:
                passes = self.blind_first_passes(target)
                failures = [p.failure_code for p in passes.values() if p.failed]
                if failures:
                    report.stop_reason = EXECUTION_STOP
                    report.execution_failures = [f for f in failures if f]
                    report.detail = f"{target.id}: first pass failed: {', '.join(report.execution_failures)}"
                    return report
                issue_ids = self.extract_issues(target, passes)
            else:
                issue_ids = [i.id for i in self.ledger.live_issues_for(target.id)]
            live = [iid for iid in issue_ids if self.ledger.issues[iid].is_live()]
            if live:
                audit_passes = self.cross_audit(target, live)
                failures = [p.failure_code for p in audit_passes if p.failed]
                if failures:
                    report.stop_reason = EXECUTION_STOP
                    report.execution_failures = [f for f in failures if f]
                    report.detail = f"{target.id}: cross-audit failed: {', '.join(report.execution_failures)}"
                    return report
            disposition = self.ledger.evaluate_target(target.id)
            self._sync_target_lists(target)
            if disposition in {SOURCE_REQUIRED, GOVERNANCE_DECISION_REQUIRED,
                               UNDERDETERMINED} or self.ledger.targets[target.id].is_terminal():
                self.ledger.set_target_status(target.id, disposition,
                                              f"round {report.rounds}")
                report.stop_reason = TARGET_TERMINAL
                report.detail = f"{target.id}: {disposition}"
                report.targets_closed = [target.id]
                return report
            self.ledger.set_target_status(target.id, disposition, f"round {report.rounds}")
            if not self.ledger.live_issues_for(target.id):
                report.stop_reason = TARGET_TERMINAL
                report.detail = f"{target.id}: {disposition}"
                report.targets_closed = [target.id]
                return report
        # Round ceiling reached with objections still standing: the target is
        # not settled, and this is not a theoretical result.
        self.ledger.set_target_status(target.id, UNDERDETERMINED,
                                      "round ceiling reached with live objections")
        report.stop_reason = TARGET_TERMINAL
        report.detail = f"{target.id}: {UNDERDETERMINED} (round ceiling)"
        report.targets_closed = [target.id]
        return report

    def _sync_target_lists(self, target: Target) -> None:
        target.sustained_objections = []
        target.defeated_objections = []
        target.withdrawn_objections = []
        target.concessions = []
        for issue in self.ledger.issues_for(target.id):
            if issue.state == "WITHDRAWN":
                target.withdrawn_objections.append(issue.id)
            elif issue.state == "CONCEDED":
                target.concessions.append(issue.id)
                target.defeated_objections.append(issue.id)
            elif issue.state == "REJECTED":
                target.defeated_objections.append(issue.id)
            elif issue.is_live():
                target.sustained_objections.append(issue.id)

    def run(self, max_targets: int = 8) -> list[RunReport]:
        """Continue automatically from one terminal target to the next.

        No user turn is required between targets: the next step is selected by
        the recorded dependency order, not by a person copying messages.
        """
        reports: list[RunReport] = []
        for _ in range(max_targets):
            target = self.ledger.next_target()
            if target is None:
                reports.append(RunReport(stop_reason=NO_ELIGIBLE_TARGET,
                                         detail="no authorized dependency-valid target remains"))
                break
            report = self.run_target(target)
            reports.append(report)
            if self.ledger.path:
                self.ledger.save()
            if report.stop_reason == EXECUTION_STOP:
                break
        return reports


def replay_run(store: EvidenceStore) -> dict[str, Any]:
    """Reproduce a recorded run from stored raw evidence, without providers."""
    invocations = store.all_invocations()
    problems = store.verify_integrity()
    return {
        "invocations": len(invocations),
        "integrity_problems": problems,
        "replayable": not problems,
        "keys": sorted({inv.key() for inv in invocations if inv.failure is None}),
    }
