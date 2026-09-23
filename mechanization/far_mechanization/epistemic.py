"""Executable far-epistemic/1.0 learning contract.

The namespace is additive.  Probabilities and utilities are fixed-scale decimal
strings and never reuse FAR approximation, provenance, or construction costs.
Interactive dialectic is represented only by the canonical FAR-ELENCHUS-1.0
contract and is embedded here by reference to its exact validated document.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator
from .socratic_epistemic import validate_socratic_record

FORMAT_VERSION = "far-epistemic/1.0"
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "far-epistemic-v1.schema.json"
PROB_SCALE = Decimal("0.000001")
SCORE_SCALE = Decimal("0.000000000001")
RECORD_KINDS = frozenset({"belief", "prediction", "decision", "outcome", "error", "retest", "causal_model"})
REFERENCE_KINDS = {
    "belief_ref": "belief", "prediction_ref": "prediction", "decision_ref": "decision",
    "outcome_ref": "outcome", "error_ref": "error", "causal_model_ref": "causal_model",
}


class EpistemicValidationError(ValueError):
    """Stable, sorted path-addressed contract violations."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(sorted(set(errors)))
        super().__init__("; ".join(self.errors))


def _path(parts: Iterable[object]) -> str:
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def _reject_non_json(value: Any, path: str, errors: list[str]) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        errors.append(f"{path}: binary floating-point and non-finite values are forbidden; use fixed-scale decimal strings")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _reject_non_json(item, f"{path}[{index}]", errors)
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                errors.append(f"{path}: object keys must be strings")
            else:
                _reject_non_json(item, f"{path}.{key}", errors)
        return
    errors.append(f"{path}: value is not JSON-compatible")


def _load_schema() -> Mapping[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"), parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))


def _schema_errors(data: object) -> list[str]:
    schema = _load_schema()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [f"{_path(error.path)}: {error.message}" for error in sorted(
        validator.iter_errors(data), key=lambda error: (tuple(str(x) for x in error.path), error.message)
    )]


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)


def _decimal(value: str) -> Decimal:
    result = Decimal(value)
    if result == 0 and value.startswith("-"):
        raise ValueError("negative zero is not canonical")
    return result


def canonical_bytes(value: object) -> bytes:
    """FAR-CJ/1: UTF-8, NFC-free exact strings, code-point key order, no whitespace.

    The schema excludes JSON numbers for semantic numeric fields; validation also
    rejects every binary float.  This leaves integers only for discrete versions.
    Surrogates are rejected by ``encode`` rather than normalized or replaced.
    """
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8", "strict")


def sha256_commitment(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key {key}")
        result[key] = value
    return result


def snapshot_payload(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in snapshot.items() if key != "sha256"}


def _validate_elenchus(data: Mapping[str, Any], errors: list[str]) -> dict[str, Mapping[str, Any]]:
    sessions: dict[str, Mapping[str, Any]] = {}
    for index, document in enumerate(data["elenchus_sessions"]):
        result = validate_socratic_record(document)
        prefix = f"$.elenchus_sessions[{index}]"
        for diagnostic in result.diagnostics:
            errors.append(f"{prefix}{_path(diagnostic.path)[1:]}: {diagnostic.code}: {diagnostic.message}")
        if document.get("record_type") != "ELENCHUS_SESSION":
            errors.append(f"{prefix}.record_type: only canonical FAR-ELENCHUS-1.0 sessions are permitted")
            continue
        record = document.get("record", {})
        session_id = record.get("session_id")
        if isinstance(session_id, str):
            if session_id in sessions:
                errors.append(f"{prefix}.record.session_id: duplicate id {session_id}")
            sessions[session_id] = document
    return sessions


def _index(items: Sequence[Mapping[str, Any]], path: str, errors: list[str]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(items):
        identifier = item["id"]
        if identifier in result:
            errors.append(f"{path}[{index}].id: duplicate id {identifier}")
        result[identifier] = item
    return result


def _validate_semantics(data: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    evidence = _index(data["evidence"], "$.evidence", errors)
    snapshots = _index(data["snapshots"], "$.snapshots", errors)
    records = _index(data["records"], "$.records", errors)
    sessions = _validate_elenchus(data, errors)

    for eid, item in evidence.items():
        if item["provenance"]["evidence_id"] != eid:
            errors.append(f"$.evidence[{eid}].provenance.evidence_id: must equal evidence id")
        expected_evidence_hash = "sha256:" + hashlib.sha256(item["statement"].encode("utf-8", "strict")).hexdigest()
        if item["provenance"]["byte_target"] != "UTF-8 bytes of statement" or item["provenance"]["artifact_sha256"] != expected_evidence_hash:
            errors.append(f"$.evidence[{eid}].provenance: artifact_sha256 must commit to UTF-8 statement bytes")

    for rid, record in records.items():
        if record["kind"] not in RECORD_KINDS:
            errors.append(f"$.records[{rid}].kind: unsupported kind")
        for field, expected_kind in REFERENCE_KINDS.items():
            if field in record:
                target = records.get(record[field])
                if target is None:
                    errors.append(f"$.records[{rid}].{field}: unknown record id {record[field]}")
                elif target["kind"] != expected_kind:
                    errors.append(f"$.records[{rid}].{field}: expected {expected_kind}, got {target['kind']}")
        provenance = record["provenance"]
        for evidence_ref in provenance["evidence_refs"]:
            if evidence_ref not in evidence:
                errors.append(f"$.records[{rid}].provenance.evidence_refs: unknown evidence id {evidence_ref}")
        for session_ref in provenance["elenchus_session_refs"]:
            if session_ref not in sessions:
                errors.append(f"$.records[{rid}].provenance.elenchus_session_refs: unknown FAR-ELENCHUS-1.0 session {session_ref}")

    beliefs = {rid: r for rid, r in records.items() if r["kind"] == "belief"}
    for rid, belief in beliefs.items():
        hypotheses = _index(belief["hypotheses"], f"$.records[{rid}].hypotheses", errors)
        revisions = belief["revisions"]
        revision_ids: set[str] = set()
        last_time: datetime | None = None
        previous: Mapping[str, Any] | None = None
        for index, revision in enumerate(revisions):
            path = f"$.records[{rid}].revisions[{index}]"
            if revision["id"] in revision_ids:
                errors.append(f"{path}.id: duplicate revision id {revision['id']}")
            revision_ids.add(revision["id"])
            timestamp = _parse_time(revision["timestamp"])
            if last_time is not None and timestamp <= last_time:
                errors.append(f"{path}.timestamp: revisions must be strictly chronological")
            last_time = timestamp
            if set(revision["probabilities"]) != set(hypotheses):
                errors.append(f"{path}.probabilities: must contain exactly all hypothesis ids")
            elif sum((_decimal(x) for x in revision["probabilities"].values()), Decimal(0)) != Decimal(1):
                errors.append(f"{path}.probabilities: must sum exactly to 1.000000")
            for evidence_ref in revision["evidence_refs"]:
                if evidence_ref not in evidence:
                    errors.append(f"{path}.evidence_refs: unknown evidence id {evidence_ref}")
                if evidence_ref not in belief["provenance"]["evidence_refs"]:
                    errors.append(f"{path}.evidence_refs: evidence {evidence_ref} is absent from belief provenance")
                if evidence_ref in evidence and _parse_time(evidence[evidence_ref]["observed_at"]) > timestamp:
                    errors.append(f"{path}.evidence_refs: evidence {evidence_ref} was observed after the revision")
            if index == 0:
                priors = {hid: hypothesis["prior_probability"] for hid, hypothesis in hypotheses.items()}
                if revision["probabilities"] != priors or revision["supersedes"] is not None:
                    errors.append(f"{path}: initial revision must equal priors and supersede null")
                if revision["trigger_outcome_ref"] is not None:
                    errors.append(f"{path}.trigger_outcome_ref: initial revision cannot be outcome-triggered")
            else:
                assert previous is not None
                if revision["supersedes"] != previous["id"]:
                    errors.append(f"{path}.supersedes: must reference immediately preceding revision {previous['id']}")
                if not revision["evidence_refs"]:
                    errors.append(f"{path}.evidence_refs: a belief change requires evidence")
            previous = revision
        if belief["current_revision_ref"] != revisions[-1]["id"]:
            errors.append(f"$.records[{rid}].current_revision_ref: must reference final revision")

    for sid, snapshot in snapshots.items():
        if snapshot["sha256"] != sha256_commitment(snapshot_payload(snapshot)):
            errors.append(f"$.snapshots[{sid}].sha256: digest does not match FAR-CJ/1 snapshot payload")
        belief = records.get(snapshot["belief_ref"])
        if belief is None or belief["kind"] != "belief":
            errors.append(f"$.snapshots[{sid}].belief_ref: must reference a belief")
            continue
        revisions = {x["id"]: x for x in belief["revisions"]}
        revision = revisions.get(snapshot["belief_revision_ref"])
        if revision is None:
            errors.append(f"$.snapshots[{sid}].belief_revision_ref: unknown revision")
            continue
        if snapshot["hypothesis_probabilities"] != revision["probabilities"]:
            errors.append(f"$.snapshots[{sid}].hypothesis_probabilities: must equal referenced belief revision")
        if snapshot["evidence_refs"] != revision["evidence_refs"]:
            errors.append(f"$.snapshots[{sid}].evidence_refs: must equal referenced belief revision")
        if _parse_time(snapshot["captured_at"]) < _parse_time(revision["timestamp"]):
            errors.append(f"$.snapshots[{sid}].captured_at: cannot predate belief revision")
        for evidence_ref in snapshot["evidence_refs"]:
            if evidence_ref not in evidence:
                errors.append(f"$.snapshots[{sid}].evidence_refs: unknown evidence id {evidence_ref}")

    predictions = {rid: r for rid, r in records.items() if r["kind"] == "prediction"}
    for rid, prediction in predictions.items():
        snapshot = snapshots.get(prediction["belief_snapshot_ref"])
        if snapshot is None:
            errors.append(f"$.records[{rid}].belief_snapshot_ref: unknown snapshot")
            continue
        if prediction["belief_ref"] != snapshot["belief_ref"]:
            errors.append(f"$.records[{rid}].belief_ref: must equal snapshot belief_ref")
        if prediction["provenance"]["evidence_refs"] != snapshot["evidence_refs"]:
            errors.append(f"$.records[{rid}].provenance.evidence_refs: must equal snapshot evidence_refs")
        expected = snapshot["hypothesis_probabilities"].get(prediction["hypothesis_ref"])
        if expected is None:
            errors.append(f"$.records[{rid}].hypothesis_ref: absent from snapshot")
        elif prediction["probability"] != expected:
            errors.append(f"$.records[{rid}].probability: must equal snapshot hypothesis probability {expected}")
        made = _parse_time(prediction["made_at"])
        if made < _parse_time(snapshot["captured_at"]):
            errors.append(f"$.records[{rid}].made_at: cannot predate snapshot")
        if made > _parse_time(prediction["resolution_window_start"]):
            errors.append(f"$.records[{rid}].made_at: must precede resolution window")
        if _parse_time(prediction["resolution_window_start"]) > _parse_time(prediction["resolution_window_end"]):
            errors.append(f"$.records[{rid}]: invalid resolution window")

    decisions = {rid: r for rid, r in records.items() if r["kind"] == "decision"}
    for rid, decision in decisions.items():
        prediction = records.get(decision["prediction_ref"])
        snapshot = snapshots.get(decision["belief_snapshot_ref"])
        if prediction is None or prediction["kind"] != "prediction" or snapshot is None:
            continue
        if decision["belief_snapshot_ref"] != prediction["belief_snapshot_ref"] or decision["belief_ref"] != prediction["belief_ref"]:
            errors.append(f"$.records[{rid}]: decision must use prediction's frozen belief snapshot")
        if decision["provenance"]["evidence_refs"] != snapshot["evidence_refs"]:
            errors.append(f"$.records[{rid}].provenance.evidence_refs: must equal snapshot evidence_refs")
        decided = _parse_time(decision["decided_at"])
        if decided < _parse_time(prediction["made_at"]) or decided > _parse_time(prediction["resolution_window_start"]):
            errors.append(f"$.records[{rid}].decided_at: must follow prediction and precede resolution window")
        states = _index(decision["states"], f"$.records[{rid}].states", errors)
        if sum((_decimal(x["probability"]) for x in states.values()), Decimal(0)) != Decimal(1):
            errors.append(f"$.records[{rid}].states: probabilities must sum exactly to 1.000000")
        for state_id, state in states.items():
            expected = snapshot["hypothesis_probabilities"].get(state["hypothesis_ref"])
            if expected != state["probability"]:
                errors.append(f"$.records[{rid}].states[{state_id}].probability: must equal snapshot probability")
        if {state["hypothesis_ref"] for state in states.values()} != set(snapshot["hypothesis_probabilities"]):
            errors.append(f"$.records[{rid}].states: must map exactly once to every snapshot hypothesis")
        actions = _index(decision["actions"], f"$.records[{rid}].actions", errors)
        evs: dict[str, Decimal] = {}
        for aid, action in actions.items():
            if set(action["utilities"]) != set(states):
                errors.append(f"$.records[{rid}].actions[{aid}].utilities: must contain exactly all state ids")
                continue
            ev = sum((_decimal(states[s]["probability"]) * _decimal(action["utilities"][s]) for s in states), Decimal(0))
            ev = ev.quantize(PROB_SCALE, rounding=ROUND_HALF_EVEN)
            evs[aid] = ev
            if _decimal(action["expected_utility"]) != ev:
                errors.append(f"$.records[{rid}].actions[{aid}].expected_utility: expected {ev:.6f}")
            if _decimal(action["downside_utility"]) != min(_decimal(x) for x in action["utilities"].values()):
                errors.append(f"$.records[{rid}].actions[{aid}].downside_utility: must equal worst utility")
            threshold = _decimal(action["tail_risk"]["threshold_utility"])
            tail_probability = sum((_decimal(states[s]["probability"]) for s, value in action["utilities"].items() if _decimal(value) <= threshold), Decimal(0))
            if _decimal(action["tail_risk"]["probability_at_or_below"]) != tail_probability:
                errors.append(f"$.records[{rid}].actions[{aid}].tail_risk.probability_at_or_below: expected {tail_probability:.6f}")
        if decision["chosen_action"] not in actions:
            errors.append(f"$.records[{rid}].chosen_action: unknown action")
        elif decision["chosen_action"] in evs:
            opportunity = max(evs.values()) - evs[decision["chosen_action"]]
            if _decimal(decision["opportunity_cost"]) != opportunity:
                errors.append(f"$.records[{rid}].opportunity_cost: expected {opportunity:.6f}")
        if len(evs) == len(actions):
            perfect = sum((_decimal(state["probability"]) * max(_decimal(action["utilities"][sid]) for action in actions.values()) for sid, state in states.items()), Decimal(0))
            evpi = (perfect - max(evs.values())).quantize(PROB_SCALE, rounding=ROUND_HALF_EVEN)
            if _decimal(decision["expected_value_of_perfect_information"]) != evpi:
                errors.append(f"$.records[{rid}].expected_value_of_perfect_information: expected {evpi:.6f}")

    outcomes = {rid: r for rid, r in records.items() if r["kind"] == "outcome"}
    for rid, outcome in outcomes.items():
        prediction = records.get(outcome["prediction_ref"])
        decision = records.get(outcome["decision_ref"])
        if prediction is None or prediction["kind"] != "prediction" or decision is None or decision["kind"] != "decision":
            continue
        if decision["prediction_ref"] != prediction["id"]:
            errors.append(f"$.records[{rid}]: outcome prediction and decision are not linked")
        if outcome["evidence_ref"] not in evidence or outcome["evidence_ref"] not in outcome["provenance"]["evidence_refs"]:
            errors.append(f"$.records[{rid}].evidence_ref: must exist and be bound by outcome provenance")
        resolved = _parse_time(outcome["resolved_at"])
        if resolved < _parse_time(prediction["resolution_window_start"]):
            errors.append(f"$.records[{rid}].resolved_at: cannot precede resolution window")
        states = {x["id"]: x for x in decision["states"]}; actions = {x["id"]: x for x in decision["actions"]}
        if outcome["realized_state"] not in states:
            errors.append(f"$.records[{rid}].realized_state: unknown decision state")
        else:
            achieved = _decimal(actions[decision["chosen_action"]]["utilities"][outcome["realized_state"]])
            regret = max(_decimal(a["utilities"][outcome["realized_state"]]) for a in actions.values()) - achieved
            if _decimal(outcome["regret"]) != regret:
                errors.append(f"$.records[{rid}].regret: expected {regret:.6f}")
        expected_scores = score_binary(prediction["probability"], outcome["binary_outcome"])
        if outcome["scores"] != expected_scores:
            errors.append(f"$.records[{rid}].scores: must equal deterministic prediction scores {expected_scores}")

    for belief_id, belief in beliefs.items():
        for revision in belief["revisions"]:
            trigger = revision["trigger_outcome_ref"]
            if trigger is None:
                continue
            outcome = outcomes.get(trigger)
            path = f"$.records[{belief_id}].revisions[{revision['id']}].trigger_outcome_ref"
            if outcome is None:
                errors.append(f"{path}: must reference an outcome")
            else:
                if outcome["evidence_ref"] not in revision["evidence_refs"]:
                    errors.append(f"{path}: triggering outcome evidence must be included in revision")
                if _parse_time(revision["timestamp"]) <= _parse_time(outcome["resolved_at"]):
                    errors.append(f"{path}: belief revision must occur after outcome resolution")

    for rid, error in ((rid, r) for rid, r in records.items() if r["kind"] == "error"):
        outcome = records.get(error["outcome_ref"])
        if outcome is not None and outcome["kind"] == "outcome":
            if error["prediction_ref"] != outcome["prediction_ref"] or error["decision_ref"] != outcome["decision_ref"]:
                errors.append(f"$.records[{rid}]: error must preserve outcome lifecycle references")
        belief = records.get(error["belief_ref"])
        if belief is None or belief["kind"] != "belief" or error["belief_revision_ref"] not in {x["id"] for x in belief.get("revisions", [])}:
            errors.append(f"$.records[{rid}].belief_revision_ref: must reference a revision of belief_ref")
        else:
            revision = next(x for x in belief["revisions"] if x["id"] == error["belief_revision_ref"])
            if revision["trigger_outcome_ref"] != error["outcome_ref"]:
                errors.append(f"$.records[{rid}].belief_revision_ref: revision must be triggered by error outcome")
        if error["retest_ref"] is not None:
            retest = records.get(error["retest_ref"])
            if retest is None or retest["kind"] != "retest" or retest["error_ref"] != rid:
                errors.append(f"$.records[{rid}].retest_ref: must reference its retest record")
        if error["failure_mode_code"] not in error["corrective_rule"]["applies_to_failure_mode_codes"]:
            errors.append(f"$.records[{rid}].corrective_rule: must apply to recorded failure_mode_code")

    for rid, retest in ((rid, r) for rid, r in records.items() if r["kind"] == "retest"):
        error = records.get(retest["error_ref"])
        if error is None or error["kind"] != "error":
            continue
        baseline_outcome = records.get(error["outcome_ref"])
        if baseline_outcome is None or baseline_outcome["kind"] != "outcome":
            errors.append(f"$.records[{rid}]: linked error must reference a valid baseline outcome")
            continue
        comparison_outcomes = [records.get(x) for x in retest["comparison_outcome_refs"]]
        if any(x is None or x["kind"] != "outcome" for x in comparison_outcomes):
            errors.append(f"$.records[{rid}].comparison_outcome_refs: every reference must target an outcome")
            continue
        if _parse_time(retest["evaluated_at"]) <= _parse_time(baseline_outcome["resolved_at"]):
            errors.append(f"$.records[{rid}].evaluated_at: retest must follow baseline outcome")
        if any(_parse_time(x["resolved_at"]) <= _parse_time(baseline_outcome["resolved_at"]) for x in comparison_outcomes):
            errors.append(f"$.records[{rid}].comparison_outcome_refs: comparisons must be later outcomes")
        baseline = _decimal(retest["baseline_mean_brier"])
        actual_baseline = _decimal(baseline_outcome["scores"]["brier"])
        if baseline != actual_baseline:
            errors.append(f"$.records[{rid}].baseline_mean_brier: must equal linked baseline outcome score")
        baseline_prediction = records[baseline_outcome["prediction_ref"]]
        comparison_predictions = [records[x["prediction_ref"]] for x in comparison_outcomes]
        if baseline_prediction["reference_class"] != retest["reference_class"] or any(x["reference_class"] != retest["reference_class"] for x in comparison_predictions):
            errors.append(f"$.records[{rid}].reference_class: must equal every compared prediction reference class")
        comparison = sum((_decimal(x["scores"]["brier"]) for x in comparison_outcomes), Decimal(0)) / Decimal(len(comparison_outcomes))
        comparison = comparison.quantize(SCORE_SCALE, rounding=ROUND_HALF_EVEN)
        if _decimal(retest["comparison_mean_brier"]) != comparison:
            errors.append(f"$.records[{rid}].comparison_mean_brier: expected {comparison:.12f}")
        derived = "IMPROVED" if comparison < baseline else "WORSE" if comparison > baseline else "UNCHANGED"
        if retest["result"] != derived:
            errors.append(f"$.records[{rid}].result: expected {derived}")

    for rid, causal in ((rid, r) for rid, r in records.items() if r["kind"] == "causal_model"):
        variables = _index(causal["variables"], f"$.records[{rid}].variables", errors)
        assumptions = _index(causal["assumptions"], f"$.records[{rid}].assumptions", errors)
        interventions = _index(causal["interventions"], f"$.records[{rid}].interventions", errors)
        for assumption_id, assumption in assumptions.items():
            for evidence_ref in assumption["evidence_refs"]:
                if evidence_ref not in evidence or evidence_ref not in causal["provenance"]["evidence_refs"]:
                    errors.append(f"$.records[{rid}].assumptions[{assumption_id}].evidence_refs: evidence must exist and be provenance-bound")
        adjacency = {x: [] for x in variables}
        for index, edge in enumerate(causal["edges"]):
            if edge["cause"] not in variables or edge["effect"] not in variables:
                errors.append(f"$.records[{rid}].edges[{index}]: endpoints must reference variables")
            else: adjacency[edge["cause"]].append(edge["effect"])
            for ref in edge["assumption_refs"]:
                if ref not in assumptions: errors.append(f"$.records[{rid}].edges[{index}].assumption_refs: unknown assumption")
        visiting: set[str] = set(); visited: set[str] = set()
        def visit(node: str) -> bool:
            if node in visiting: return True
            if node in visited: return False
            visiting.add(node)
            if any(visit(child) for child in adjacency[node]): return True
            visiting.remove(node); visited.add(node); return False
        if any(visit(node) for node in variables): errors.append(f"$.records[{rid}].edges: causal graph must be acyclic")
        for collection in ("interventions", "confounders", "counterfactuals"):
            for index, item in enumerate(causal[collection]):
                for field in ("variable_ref", "target_ref", "cause_ref", "effect_ref", "outcome_variable_ref"):
                    if field in item and item[field] not in variables:
                        errors.append(f"$.records[{rid}].{collection}[{index}].{field}: unknown variable")
                if collection == "counterfactuals":
                    for ref in item["intervention_refs"]:
                        if ref not in interventions: errors.append(f"$.records[{rid}].counterfactuals[{index}].intervention_refs: unknown intervention")
        for ref in causal["identification"]["assumption_refs"]:
            if ref not in assumptions: errors.append(f"$.records[{rid}].identification.assumption_refs: unknown assumption")
        for ref in causal["identification"]["adjustment_set"]:
            if ref not in variables: errors.append(f"$.records[{rid}].identification.adjustment_set: unknown variable")

    return errors


def validate_document(data: object) -> tuple[str, ...]:
    errors: list[str] = []
    _reject_non_json(data, "$", errors)
    if errors: return tuple(sorted(set(errors)))
    try:
        errors.extend(_schema_errors(data))
    except (OSError, ValueError, TypeError, UnicodeError) as exc:
        return (f"$: schema validation failed: {exc}",)
    if errors or not isinstance(data, Mapping): return tuple(sorted(set(errors)))
    try:
        errors.extend(_validate_semantics(data))
    except (KeyError, TypeError, ValueError, ArithmeticError, UnicodeError) as exc:
        errors.append(f"$: semantic validation failed closed: {type(exc).__name__}: {exc}")
    return tuple(sorted(set(errors)))


@dataclass(frozen=True, slots=True)
class EpistemicDocument:
    _canonical: bytes

    @classmethod
    def from_dict(cls, data: object) -> "EpistemicDocument":
        errors = validate_document(data)
        if errors: raise EpistemicValidationError(errors)
        try:
            return cls(canonical_bytes(data))
        except (TypeError, ValueError, UnicodeError) as exc:
            raise EpistemicValidationError((f"$: canonicalization failed: {exc}",)) from exc

    @classmethod
    def loads(cls, text: str) -> "EpistemicDocument":
        try:
            data = json.loads(text, object_pairs_hook=_unique_object,
                              parse_constant=lambda token: (_ for _ in ()).throw(ValueError(f"non-finite {token}")))
        except (json.JSONDecodeError, ValueError, UnicodeError) as exc:
            raise EpistemicValidationError((f"$: invalid strict JSON: {exc}",)) from exc
        return cls.from_dict(data)

    @classmethod
    def load(cls, path: str | Path) -> "EpistemicDocument":
        try: return cls.loads(Path(path).read_text(encoding="utf-8"))
        except OSError as exc: raise EpistemicValidationError((f"$: unreadable document: {exc}",)) from exc

    def to_dict(self) -> dict[str, Any]: return json.loads(self._canonical)
    def dumps(self) -> str: return self._canonical.decode("utf-8") + "\n"
    @property
    def digest(self) -> str: return "sha256:" + hashlib.sha256(self._canonical).hexdigest()
    def audit_event(self) -> dict[str, Any]:
        data = self.to_dict()
        return {"event": "far_epistemic_validation", "format_version": FORMAT_VERSION,
                "document_id": data["id"], "content_hash": self.digest,
                "record_ids": [x["id"] for x in data["records"]], "valid": True}


def score_binary(probability: str, outcome: int) -> dict[str, str]:
    if not isinstance(probability, str) or not isinstance(outcome, int) or isinstance(outcome, bool) or outcome not in (0, 1):
        raise EpistemicValidationError(("$: fixed-scale probability string and binary integer outcome required",))
    try: p = Decimal(probability)
    except Exception as exc: raise EpistemicValidationError(("$.probability: invalid decimal",)) from exc
    if not p.is_finite() or not (Decimal(0) < p < Decimal(1)) or p.as_tuple().exponent != -6:
        raise EpistemicValidationError(("$.probability: strict interior probability with exactly six decimals required",))
    with localcontext() as context:
        context.prec = 50
        context.rounding = ROUND_HALF_EVEN
        brier = ((p - Decimal(outcome)) ** 2).quantize(SCORE_SCALE)
        likelihood = p if outcome else Decimal(1) - p
        log_loss = (-likelihood.ln()).quantize(SCORE_SCALE)
    return {"brier": f"{brier:.12f}", "log": f"{log_loss:.12f}"}


def calibration(outcomes: Iterable[Mapping[str, Any]], *, bin_edges: Sequence[str]) -> dict[str, Any]:
    """Aggregate explicitly selected comparable outcomes under declared fixed bins."""
    try: edges = [Decimal(x) for x in bin_edges]
    except Exception as exc: raise EpistemicValidationError(("$.bin_edges: decimal strings required",)) from exc
    if len(edges) < 2 or edges[0] != 0 or edges[-1] != 1 or any(a >= b for a, b in zip(edges, edges[1:])):
        raise EpistemicValidationError(("$.bin_edges: strictly increasing edges from 0 to 1 required",))
    rows = list(outcomes)
    if not rows: raise EpistemicValidationError(("$.outcomes: at least one resolved comparable outcome required",))
    reference_classes = {row.get("reference_class") for row in rows}
    if len(reference_classes) != 1 or None in reference_classes:
        raise EpistemicValidationError(("$.outcomes: one explicit comparable reference_class required",))
    buckets: list[list[tuple[Decimal, int]]] = [[] for _ in range(len(edges) - 1)]
    for index, row in enumerate(rows):
        try: p = Decimal(row["probability"]); outcome = row["binary_outcome"]
        except Exception as exc: raise EpistemicValidationError((f"$.outcomes[{index}]: probability and outcome required",)) from exc
        if outcome not in (0, 1) or isinstance(outcome, bool) or not (0 < p < 1):
            raise EpistemicValidationError((f"$.outcomes[{index}]: strict probability and binary integer outcome required",))
        bucket = next((i for i, (a, b) in enumerate(zip(edges, edges[1:])) if a <= p < b or (i == len(edges)-2 and p == b)), None)
        if bucket is None: raise EpistemicValidationError((f"$.outcomes[{index}]: probability outside bins",))
        buckets[bucket].append((p, outcome))
    result = []
    all_rows = [x for bucket in buckets for x in bucket]
    for index, bucket in enumerate(buckets):
        if bucket:
            count = Decimal(len(bucket))
            mean = (sum((p for p, _ in bucket), Decimal(0))/count).quantize(PROB_SCALE, rounding=ROUND_HALF_EVEN)
            observed = (sum((Decimal(o) for _, o in bucket), Decimal(0))/count).quantize(PROB_SCALE, rounding=ROUND_HALF_EVEN)
            result.append({"lower": str(bin_edges[index]), "upper": str(bin_edges[index+1]), "count": len(bucket), "mean_probability": f"{mean:.6f}", "observed_frequency": f"{observed:.6f}"})
    brier = (sum(((p-Decimal(o))**2 for p,o in all_rows),Decimal(0))/Decimal(len(all_rows))).quantize(SCORE_SCALE,rounding=ROUND_HALF_EVEN)
    return {"reference_class": next(iter(reference_classes)), "bin_edges": list(bin_edges), "resolved_count": len(all_rows), "bins": result, "mean_brier": f"{brier:.12f}"}


def recurring_failure_modes(error_records: Iterable[Mapping[str, Any]], *, minimum: int = 2) -> list[dict[str, Any]]:
    if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 2:
        raise EpistemicValidationError(("$.minimum: integer at least 2 required",))
    groups: dict[tuple[str, str], list[str]] = {}
    for index, record in enumerate(error_records):
        if record.get("kind") != "error" or not all(isinstance(record.get(x), str) for x in ("id", "failure_mode_code")) or not isinstance(record.get("corrective_rule"), Mapping):
            raise EpistemicValidationError((f"$.error_records[{index}]: normalized ErrorRecord required",))
        rule_id = record["corrective_rule"].get("id")
        if not isinstance(rule_id, str): raise EpistemicValidationError((f"$.error_records[{index}].corrective_rule.id: required",))
        groups.setdefault((record["failure_mode_code"], rule_id), []).append(record["id"])
    return [{"failure_mode_code": key[0], "corrective_rule_id": key[1], "count": len(ids), "record_ids": sorted(ids)} for key, ids in sorted(groups.items()) if len(ids) >= minimum]
