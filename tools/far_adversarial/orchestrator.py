"""The adversarial relay loop.

This replaces exactly one manual activity: carrying messages between the Claude
lane and the GPT lane. It decides nothing that the manual process did not
already decide by rule.

    frozen target -> blind first passes -> raw preservation -> issue extraction
    -> rebuttal by the challenged lane -> owner review by the raising lane
    -> terminal disposition -> next dependency-valid target

Two invariants are enforced here rather than assumed:

- A round, call, token, or time ceiling produces an execution stop. It never
  writes a disposition, never clears a live issue, and never makes a
  dependency look satisfied. The target stays exactly where it was and the run
  is resumable.
- No lane adjudicates. A challenged lane rebuts; the owner decides.
"""

from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable

from . import protocol
from .evidence import EvidenceStore, RunRecord
from .ledger import (
    CHALLENGED_ACTIONS,
    LEDGER_SCHEMA,
    Ledger,
    OBLIGATION_FORMAL,
    OBLIGATION_SOURCE,
    OWNER_ACTIONS,
    RECONSTRUCTED_RESEARCH_STATE,
    REDUCER_VERSION,
    TERMINAL_TARGET_STATUSES,
    Target,
)
from .providers import INVALID_PROVIDER_OUTPUT, Provider, ProviderResult

# Epistemic stops: the target reached a research disposition.
TARGET_TERMINAL = "TARGET_TERMINAL"
NO_ELIGIBLE_TARGET = "NO_ELIGIBLE_TARGET"
EPISTEMIC_STOPS = frozenset({TARGET_TERMINAL, NO_ELIGIBLE_TARGET})

# Execution stops: the run stopped. The research state is unchanged and
# resumable. None of these is a finding.
EXECUTION_STOP = "EXECUTION_STOP"
ROUND_LIMIT = "ROUND_LIMIT"
EXECUTION_STOPS = frozenset({EXECUTION_STOP, ROUND_LIMIT})


@dataclass
class LanePass:
    lane: str
    prompt: str
    result: ProviderResult
    parsed: Any
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
    resumable: bool = False

    @property
    def is_epistemic_stop(self) -> bool:
        """A resource ceiling is never a theoretical stalemate."""
        return self.stop_reason in EPISTEMIC_STOPS

    @property
    def is_execution_stop(self) -> bool:
        return self.stop_reason in EXECUTION_STOPS


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
        self.invocation_ids: list[str] = []
        self.resolved_models: dict[str, str] = {}

    def _provider(self, lane: str) -> Provider:
        return self.claude if lane == "claude" else self.gpt

    # -- provider plumbing -------------------------------------------------

    def _record(self, provider: Provider, lane: str, target_id: str, prompt: str,
                result: ProviderResult, parser: Callable[[str], Any], tags: list[str]) -> LanePass:
        """Persist one provider exchange.

        Recording is always sequential and in a deterministic lane order, even
        when the calls themselves ran concurrently. Invocation identity ends up
        in issue provenance, so a nondeterministic recording order would make
        an otherwise identical replay diverge.
        """
        self.lane_prompts.setdefault(lane, []).append(prompt)
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
            resolved_model=result.resolved_model,
        )
        self.invocation_ids.append(invocation.invocation_id)
        if result.resolved_model:
            self.resolved_models[lane] = result.resolved_model
        return LanePass(lane=lane, prompt=prompt, result=result, parsed=parsed,
                        invocation_id=invocation.invocation_id)

    def _invoke(self, provider: Provider, lane: str, target_id: str, prompt: str,
                parser: Callable[[str], Any], tags: list[str],
                schema: dict[str, Any] | None) -> LanePass:
        result = provider.complete(prompt, schema=schema)
        return self._record(provider, lane, target_id, prompt, result, parser, tags)

    # -- blind first passes -------------------------------------------------

    def blind_first_passes(self, target: Target) -> dict[str, LanePass]:
        """Run both lanes over identical frozen evidence without cross-exposure.

        Both prompts are built before either provider is called, so neither can
        depend on the other's output even in principle. Raw output is preserved
        before any cross-exchange happens.
        """
        evidence = self.evidence_loader(target)
        prompts = {
            "claude": protocol.first_pass_prompt(
                role=protocol.CLAUDE_ROLE, target=target, evidence=evidence,
                source_freeze=self.source_freeze),
            "gpt": protocol.first_pass_prompt(
                role=protocol.GPT_ROLE, target=target, evidence=evidence,
                source_freeze=self.source_freeze),
        }
        tags = ["first-pass", target.id]
        lanes = sorted(prompts)

        def call(lane: str) -> ProviderResult:
            return self._provider(lane).complete(prompts[lane],
                                                 schema=protocol.FIRST_PASS_SCHEMA)

        # The two calls are independent, so they run concurrently. Recording is
        # then replayed sequentially in lane order so the run is reproducible.
        if self.parallel:
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(call, lanes))
        else:
            results = [call(lane) for lane in lanes]
        return {
            lane: self._record(self._provider(lane), lane, target.id, prompts[lane],
                               result, protocol.parse_first_pass, tags)
            for lane, result in zip(lanes, results)
        }

    # -- issue and obligation extraction ------------------------------------

    def extract_issues(self, target: Target, passes: dict[str, LanePass]) -> list[str]:
        """Register objections and obligations from both first passes.

        Objections are never merged by similarity. Source requests and formal
        obligations become first-class ledger objects that block readiness
        until discharged with provenance — they are not appended to the
        target's declared frozen-evidence paths, which are an input contract.
        """
        registered: list[str] = []
        for lane in sorted(passes):
            lane_pass = passes[lane]
            if lane_pass.parsed is None:
                continue
            provenance = f"first-pass:{lane}:{lane_pass.invocation_id}"
            for objection in lane_pass.parsed["objections"]:
                issue = self.ledger.register_issue(
                    target_id=target.id, claim=objection["claim"], raised_by=lane,
                    provenance=provenance,
                    confidence_class=RECONSTRUCTED_RESEARCH_STATE,
                )
                if issue.id not in registered:
                    registered.append(issue.id)
            for request in lane_pass.parsed["source_requests"]:
                self.ledger.register_obligation(
                    target_id=target.id, kind=OBLIGATION_SOURCE, statement=request,
                    raised_by=lane, provenance=provenance,
                )
            for obligation in lane_pass.parsed["formal_obligations"]:
                self.ledger.register_obligation(
                    target_id=target.id, kind=OBLIGATION_FORMAL, statement=obligation,
                    raised_by=lane, provenance=provenance,
                )
        return registered

    # -- controlled cross audit ---------------------------------------------

    def _audit_side(self, target: Target, lane: str, issues: list[Any],
                    audit_role: str, evidence: dict[str, str]) -> LanePass | None:
        if not issues:
            return None
        permitted = OWNER_ACTIONS if audit_role == protocol.ROLE_OWNER else CHALLENGED_ACTIONS
        role_prompt = protocol.CLAUDE_ROLE if lane == "claude" else protocol.GPT_ROLE
        prompt = protocol.cross_audit_prompt(
            role=role_prompt, audit_role=audit_role, target=target, issues=issues,
            evidence=evidence, source_freeze=self.source_freeze,
        )
        known = {issue.id for issue in issues}
        lane_pass = self._invoke(
            self._provider(lane), lane, target.id, prompt,
            lambda raw: protocol.parse_cross_audit(raw, known, permitted),
            [audit_role, target.id],
            protocol.cross_audit_schema(sorted(permitted)),
        )
        if lane_pass.parsed is None:
            return lane_pass
        for response in lane_pass.parsed:
            self.ledger.apply_action(
                response["issue_id"], actor=lane, action=response["action"],
                rationale=response["rationale"],
                provenance=f"{audit_role}:{lane}:{lane_pass.invocation_id}",
                invocation_id=lane_pass.invocation_id,
                revised_claim=response["revised_claim"],
            )
        return lane_pass

    def rebuttal_round(self, target: Target, issue_ids: list[str]) -> list[LanePass]:
        """Each lane answers the objections raised against it.

        The strongest move available here is REBUT. A challenged lane cannot
        end an objection it does not own, so this round never defeats anything.
        """
        evidence = self.evidence_loader(target)
        passes: list[LanePass] = []
        for lane in ("claude", "gpt"):
            issues = [
                self.ledger.issues[iid] for iid in sorted(issue_ids)
                if iid in self.ledger.issues
                and self.ledger.issues[iid].raised_by != lane
                and self.ledger.issues[iid].state == "OPEN"
            ]
            lane_pass = self._audit_side(target, lane, issues,
                                         protocol.ROLE_CHALLENGED, evidence)
            if lane_pass is not None:
                passes.append(lane_pass)
        return passes

    def owner_review_round(self, target: Target, issue_ids: list[str]) -> list[LanePass]:
        """Each lane reviews the rebuttals to the objections it owns.

        Withdrawal happens only here, and only from the owner. This is the only
        route by which an objection becomes defeated by argument.
        """
        evidence = self.evidence_loader(target)
        passes: list[LanePass] = []
        for lane in ("claude", "gpt"):
            issues = [
                self.ledger.issues[iid] for iid in sorted(issue_ids)
                if iid in self.ledger.issues
                and self.ledger.issues[iid].raised_by == lane
                and self.ledger.issues[iid].state == "REBUTTED"
            ]
            lane_pass = self._audit_side(target, lane, issues,
                                         protocol.ROLE_OWNER, evidence)
            if lane_pass is not None:
                passes.append(lane_pass)
        return passes

    # -- target loop ---------------------------------------------------------

    def _execution_stop(self, report: RunReport, target: Target, stage: str,
                        failures: list[str]) -> RunReport:
        """Stop the run without touching the epistemic state."""
        report.stop_reason = EXECUTION_STOP
        report.execution_failures = [f for f in failures if f]
        report.detail = (f"{target.id}: {stage} failed: "
                         f"{', '.join(report.execution_failures)}")
        report.resumable = True
        return report

    def run_target(self, target: Target) -> RunReport:
        report = RunReport(stop_reason=ROUND_LIMIT)
        for round_index in range(self.max_rounds_per_target):
            report.rounds += 1
            if round_index == 0:
                passes = self.blind_first_passes(target)
                failures = [p.failure_code for p in passes.values() if p.failed]
                if failures:
                    return self._execution_stop(report, target, "first pass", failures)
                issue_ids = self.extract_issues(target, passes)
            else:
                issue_ids = [i.id for i in self.ledger.live_issues_for(target.id)]

            rebuttals = self.rebuttal_round(target, issue_ids)
            failures = [p.failure_code for p in rebuttals if p.failed]
            if failures:
                return self._execution_stop(report, target, "rebuttal", failures)

            reviews = self.owner_review_round(target, issue_ids)
            failures = [p.failure_code for p in reviews if p.failed]
            if failures:
                return self._execution_stop(report, target, "owner review", failures)

            self._sync_target_lists(target)
            disposition = self.ledger.evaluate_target(target.id)
            if disposition in TERMINAL_TARGET_STATUSES:
                self.ledger.set_target_status(target.id, disposition,
                                              f"round {report.rounds}")
                report.stop_reason = TARGET_TERMINAL
                report.detail = f"{target.id}: {disposition}"
                report.targets_closed = [target.id]
                return report
            # Non-terminal: record progress and keep going.
            self.ledger.set_target_status(target.id, disposition, f"round {report.rounds}")

        # Round ceiling. This is a resource stop: the disposition stays
        # non-terminal, every live issue survives, and the target is resumable.
        # It must never look like a settled research outcome to a dependency.
        report.stop_reason = ROUND_LIMIT
        report.execution_failures = [ROUND_LIMIT]
        report.resumable = True
        report.targets_closed = []
        live = len(self.ledger.live_issues_for(target.id))
        report.detail = (
            f"{target.id}: round ceiling ({self.max_rounds_per_target}) reached with "
            f"{live} live objection(s); disposition left at {target.status}"
        )
        return report

    def _sync_target_lists(self, target: Target) -> None:
        target.sustained_objections = []
        target.upheld_objections = []
        target.defeated_objections = []
        target.withdrawn_objections = []
        target.concessions = []
        for issue in self.ledger.issues_for(target.id):
            if issue.state == "WITHDRAWN":
                target.withdrawn_objections.append(issue.id)
                target.defeated_objections.append(issue.id)
            elif issue.state == "SETTLED_DEFEATED":
                target.defeated_objections.append(issue.id)
            elif issue.state == "CONCEDED":
                target.concessions.append(issue.id)
                target.upheld_objections.append(issue.id)
            elif issue.state == "SETTLED_UPHELD":
                target.upheld_objections.append(issue.id)
            elif issue.is_live():
                target.sustained_objections.append(issue.id)

    def run(self, max_targets: int = 8) -> list[RunReport]:
        """Continue automatically from one terminal target to the next.

        No user turn is required between targets: the next step is selected by
        the recorded dependency predicates, not by a person copying messages.
        """
        reports: list[RunReport] = []
        for _ in range(max_targets):
            target = self.ledger.next_target()
            if target is None:
                reports.append(RunReport(
                    stop_reason=NO_ELIGIBLE_TARGET,
                    detail="no authorized target has its dependency conditions satisfied"))
                break
            report = self.run_target(target)
            reports.append(report)
            if self.ledger.path:
                self.ledger.save()
            if report.is_execution_stop:
                break
        return reports

    def run_record(self, run_id: str, baseline_digest: str,
                   reports: list[RunReport]) -> RunRecord:
        return RunRecord(
            run_id=run_id,
            source_identity=self.source_freeze,
            baseline_ledger_digest=baseline_digest,
            final_ledger_digest=self.ledger.digest(),
            invocation_ids=list(self.invocation_ids),
            reducer_version=REDUCER_VERSION,
            ledger_schema=LEDGER_SCHEMA,
            protocol_version=protocol.PROTOCOL_VERSION,
            lane_models={"claude": self.claude.model, "gpt": self.gpt.model},
            resolved_models=dict(self.resolved_models),
            stop_reasons=[r.stop_reason for r in reports],
        )


def new_run_id() -> str:
    return uuid.uuid4().hex
