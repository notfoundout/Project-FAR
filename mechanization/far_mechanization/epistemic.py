"""Typed, additive epistemic-learning records for Project FAR.

This module deliberately does not extend or reinterpret ``far-ir/1.0`` or the
``far-ir/2.1`` approximation/cost order.  Epistemic probabilities, utilities,
and decision costs live in the separate ``far-epistemic/1.0`` namespace.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping


FORMAT_VERSION = "far-epistemic/1.0"
LEGACY_VERSION = "far-epistemic/0.9"
RECORD_KINDS = {
    "belief", "prediction", "decision", "dialectic", "causal_model", "error"
}


class EpistemicValidationError(ValueError):
    """A deterministic collection of invalid epistemic record paths."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(sorted(set(errors)))
        super().__init__("; ".join(self.errors))


def _decimal(value: Any, path: str, errors: list[str]) -> Decimal | None:
    if isinstance(value, bool):
        errors.append(f"{path}: must be a number, not boolean")
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        errors.append(f"{path}: must be a finite number")
        return None
    if not result.is_finite():
        errors.append(f"{path}: must be finite")
        return None
    return result


def _prob(value: Any, path: str, errors: list[str], *, open_interval: bool = False) -> Decimal | None:
    result = _decimal(value, path, errors)
    if result is not None and not ((0 < result < 1) if open_interval else (0 <= result <= 1)):
        errors.append(f"{path}: probability must be {'strictly ' if open_interval else ''}between 0 and 1")
    return result


def _required_text(obj: Mapping[str, Any], name: str, path: str, errors: list[str]) -> None:
    if not isinstance(obj.get(name), str) or not obj[name].strip():
        errors.append(f"{path}.{name}: non-empty string required")


def _list(obj: Mapping[str, Any], name: str, path: str, errors: list[str], *, nonempty: bool = False) -> list[Any]:
    value = obj.get(name)
    if not isinstance(value, list) or (nonempty and not value):
        errors.append(f"{path}.{name}: {'non-empty ' if nonempty else ''}array required")
        return []
    return value


def _text_list(obj: Mapping[str, Any], name: str, path: str, errors: list[str], *, nonempty: bool = False) -> list[str]:
    value = _list(obj, name, path, errors, nonempty=nonempty)
    if not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{path}.{name}: every item must be a non-empty string")
    return value


def _timestamp(value: Any, path: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        errors.append(f"{path}: RFC 3339 timestamp required")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}: invalid RFC 3339 timestamp")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{path}: timestamp must include an offset")
        return None
    return parsed.astimezone(timezone.utc)


def _ids(items: list[Any], path: str, errors: list[str]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(items):
        p = f"{path}[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{p}: object required")
            continue
        _required_text(item, "id", p, errors)
        identifier = item.get("id")
        if isinstance(identifier, str):
            if identifier in result:
                errors.append(f"{p}.id: duplicate id {identifier}")
            result[identifier] = item
    return result


def _provenance(record: Mapping[str, Any], path: str, errors: list[str]) -> None:
    provenance = record.get("provenance")
    if not isinstance(provenance, Mapping):
        errors.append(f"{path}.provenance: object required")
        return
    _required_text(provenance, "source", f"{path}.provenance", errors)
    _required_text(provenance, "content_hash", f"{path}.provenance", errors)
    refs = provenance.get("far_refs", [])
    if not isinstance(refs, list) or not all(isinstance(x, str) and x for x in refs):
        errors.append(f"{path}.provenance.far_refs: string array required")


def _validate_belief(record: Mapping[str, Any], path: str, errors: list[str]) -> None:
    hypotheses = _list(record, "hypotheses", path, errors, nonempty=True)
    if len(hypotheses) < 2: errors.append(f"{path}.hypotheses: at least two competing hypotheses required")
    by_id = _ids(hypotheses, f"{path}.hypotheses", errors)
    total = Decimal(0)
    prior_total = Decimal(0)
    for hid, item in by_id.items():
        hp = f"{path}.hypotheses[{hid}]"
        _required_text(item, "statement", hp, errors)
        prior = _prob(item.get("prior_probability"), f"{hp}.prior_probability", errors)
        if prior is not None: prior_total += prior
        p = _prob(item.get("confidence"), f"{hp}.confidence", errors)
        if p is not None:
            total += p
        _text_list(item, "falsifiers", hp, errors, nonempty=True)
        _text_list(item, "base_reference_classes", hp, errors, nonempty=True)
        uncertainty = item.get("uncertainty")
        if not isinstance(uncertainty, Mapping):
            errors.append(f"{hp}.uncertainty: object required")
        else:
            _required_text(uncertainty, "kind", f"{hp}.uncertainty", errors)
            _required_text(uncertainty, "description", f"{hp}.uncertainty", errors)
    if by_id and total != Decimal(1):
        errors.append(f"{path}.hypotheses: confidences must sum exactly to 1 (got {total})")
    if by_id and prior_total != Decimal(1):
        errors.append(f"{path}.hypotheses: priors must sum exactly to 1 (got {prior_total})")
    updates = _list(record, "evidence_updates", path, errors)
    previous: dict[str, Decimal] | None = None
    for index, update in enumerate(updates):
        up = f"{path}.evidence_updates[{index}]"
        if not isinstance(update, Mapping):
            errors.append(f"{up}: object required"); continue
        _timestamp(update.get("timestamp"), f"{up}.timestamp", errors)
        _required_text(update, "evidence_ref", up, errors)
        posterior = update.get("posterior")
        if not isinstance(posterior, Mapping) or set(posterior) != set(by_id):
            errors.append(f"{up}.posterior: must contain exactly all hypothesis ids")
        else:
            vals = {k: _prob(v, f"{up}.posterior.{k}", errors) for k, v in posterior.items()}
            if all(v is not None for v in vals.values()) and sum(vals.values(), Decimal(0)) != Decimal(1):
                errors.append(f"{up}.posterior: probabilities must sum exactly to 1")
            previous = {k: v for k, v in vals.items() if v is not None}
    if previous is not None:
        current = {k: Decimal(str(v["confidence"])) for k, v in by_id.items() if "confidence" in v}
        if current != previous:
            errors.append(f"{path}.hypotheses: current confidence must equal final evidence posterior")
    revisions = _list(record, "revision_history", path, errors, nonempty=True)
    last_revision: datetime | None = None
    for index, revision in enumerate(revisions):
        rp = f"{path}.revision_history[{index}]"
        if not isinstance(revision, Mapping): errors.append(f"{rp}: object required"); continue
        timestamp = _timestamp(revision.get("timestamp"), f"{rp}.timestamp", errors)
        if timestamp and last_revision and timestamp < last_revision:
            errors.append(f"{rp}.timestamp: revision history must be chronological")
        if timestamp: last_revision = timestamp
        _required_text(revision, "reason", rp, errors)


def _validate_prediction(record: Mapping[str, Any], path: str, errors: list[str]) -> None:
    made = _timestamp(record.get("made_at"), f"{path}.made_at", errors)
    start = _timestamp(record.get("resolution_window_start"), f"{path}.resolution_window_start", errors)
    end = _timestamp(record.get("resolution_window_end"), f"{path}.resolution_window_end", errors)
    if made and start and made > start: errors.append(f"{path}: prediction must precede resolution window")
    if start and end and start > end: errors.append(f"{path}: resolution window start must not exceed end")
    _prob(record.get("probability"), f"{path}.probability", errors, open_interval=True)
    _required_text(record, "proposition", path, errors)
    _required_text(record, "objective_resolution_criteria", path, errors)
    _required_text(record, "evidence_snapshot_hash", path, errors)
    provenance = record.get("provenance", {})
    if isinstance(provenance, Mapping) and provenance.get("content_hash") != record.get("evidence_snapshot_hash"):
        errors.append(f"{path}.evidence_snapshot_hash: must equal provenance content_hash")
    outcome = record.get("outcome")
    scores = record.get("scores")
    if outcome is None:
        if scores is not None: errors.append(f"{path}.scores: unresolved prediction cannot have scores")
    elif outcome not in (0, 1, False, True):
        errors.append(f"{path}.outcome: binary 0 or 1 required")
    else:
        resolved = _timestamp(record.get("resolved_at"), f"{path}.resolved_at", errors)
        if resolved and end and resolved < start: errors.append(f"{path}.resolved_at: cannot precede resolution window")
        if not isinstance(scores, Mapping): errors.append(f"{path}.scores: resolved prediction requires scores")
        else:
            expected = score_binary(record["probability"], int(outcome))
            for key in ("brier", "log"):
                value = _decimal(scores.get(key), f"{path}.scores.{key}", errors)
                if value is not None and abs(value - expected[key]) > Decimal("0.000000000001"):
                    errors.append(f"{path}.scores.{key}: does not match computed score")


def _validate_decision(record: Mapping[str, Any], path: str, errors: list[str]) -> None:
    actions = _list(record, "actions", path, errors, nonempty=True)
    if len(actions) < 2: errors.append(f"{path}.actions: at least two available actions required")
    states = _list(record, "states", path, errors, nonempty=True)
    action_ids = _ids(actions, f"{path}.actions", errors)
    state_ids = _ids(states, f"{path}.states", errors)
    state_total = Decimal(0)
    for sid, state in state_ids.items():
        p = _prob(state.get("probability"), f"{path}.states[{sid}].probability", errors)
        if p is not None: state_total += p
    if state_ids and state_total != Decimal(1): errors.append(f"{path}.states: probabilities must sum exactly to 1")
    computed: dict[str, Decimal] = {}
    for aid, action in action_ids.items():
        utilities = action.get("utilities")
        if not isinstance(utilities, Mapping) or set(utilities) != set(state_ids):
            errors.append(f"{path}.actions[{aid}].utilities: must contain exactly all state ids"); continue
        ev = Decimal(0)
        for sid, state in state_ids.items():
            utility = _decimal(utilities[sid], f"{path}.actions[{aid}].utilities.{sid}", errors)
            if utility is not None: ev += Decimal(str(state["probability"])) * utility
        declared = _decimal(action.get("expected_utility"), f"{path}.actions[{aid}].expected_utility", errors)
        if declared is not None and declared != ev: errors.append(f"{path}.actions[{aid}].expected_utility: expected {ev}")
        _required_text(action, "tail_risk", f"{path}.actions[{aid}]", errors)
        downside = _decimal(action.get("downside_utility"), f"{path}.actions[{aid}].downside_utility", errors)
        if downside is not None and utilities and downside != min(Decimal(str(x)) for x in utilities.values()):
            errors.append(f"{path}.actions[{aid}].downside_utility: must equal worst utility")
        computed[aid] = ev
    chosen = record.get("chosen_action")
    if chosen not in action_ids: errors.append(f"{path}.chosen_action: must reference an action")
    _required_text(record, "rationale", path, errors)
    if computed and chosen in computed:
        opportunity = max(computed.values()) - computed[chosen]
        declared = _decimal(record.get("opportunity_cost"), f"{path}.opportunity_cost", errors)
        if declared is not None and declared != opportunity: errors.append(f"{path}.opportunity_cost: expected {opportunity}")
    voi = _decimal(record.get("value_of_information"), f"{path}.value_of_information", errors)
    if voi is not None and voi < 0: errors.append(f"{path}.value_of_information: must be non-negative")
    if len(computed) == len(action_ids) and state_ids and voi is not None:
        perfect = sum((Decimal(str(state["probability"])) * max(Decimal(str(action["utilities"][sid])) for action in action_ids.values()) for sid, state in state_ids.items()), Decimal(0))
        expected_voi = perfect - max(computed.values())
        if voi != expected_voi: errors.append(f"{path}.value_of_information: expected {expected_voi}")
    if record.get("actual_state") is not None:
        actual = record.get("actual_state")
        if actual not in state_ids: errors.append(f"{path}.actual_state: must reference a state")
        if actual in state_ids and chosen in action_ids:
            achieved = Decimal(str(action_ids[chosen]["utilities"][actual]))
            regret = max(Decimal(str(a["utilities"][actual])) for a in action_ids.values()) - achieved
            declared = _decimal(record.get("regret"), f"{path}.regret", errors)
            if declared is not None and declared != regret: errors.append(f"{path}.regret: expected {regret}")


def _validate_dialectic(record: Mapping[str, Any], path: str, errors: list[str]) -> None:
    for field in ("claim", "clarification", "steelman", "burden_of_proof", "revision_result"):
        _required_text(record, field, path, errors)
    for field in ("definitions", "commitments", "assumptions", "counterexamples", "contradictions", "cruxes", "falsifiers", "change_evidence"):
        _text_list(record, field, path, errors, nonempty=True)


def _validate_causal(record: Mapping[str, Any], path: str, errors: list[str]) -> None:
    nodes = _list(record, "nodes", path, errors, nonempty=True)
    node_ids = set(x for x in nodes if isinstance(x, str) and x)
    if len(node_ids) != len(nodes): errors.append(f"{path}.nodes: unique non-empty strings required")
    edges = _list(record, "edges", path, errors)
    adjacency = {x: [] for x in node_ids}
    for i, edge in enumerate(edges):
        if not isinstance(edge, Mapping) or edge.get("cause") not in node_ids or edge.get("effect") not in node_ids:
            errors.append(f"{path}.edges[{i}]: cause and effect must reference nodes"); continue
        adjacency[edge["cause"]].append(edge["effect"])
    visiting: set[str] = set(); visited: set[str] = set()
    def visit(node: str) -> bool:
        if node in visiting: return True
        if node in visited: return False
        visiting.add(node)
        if any(visit(n) for n in adjacency[node]): return True
        visiting.remove(node); visited.add(node); return False
    if any(visit(n) for n in node_ids): errors.append(f"{path}.edges: causal graph must be acyclic")
    for field in ("interventions", "confounders", "counterfactuals", "assumptions", "identification_limits"):
        _text_list(record, field, path, errors, nonempty=True)


def _validate_error(record: Mapping[str, Any], path: str, errors: list[str]) -> None:
    for field in ("root_cause", "corrective_rule", "retest_criterion"):
        _required_text(record, field, path, errors)
    _text_list(record, "linked_record_ids", path, errors, nonempty=True)
    _text_list(record, "classifications", path, errors, nonempty=True)
    recurrences = record.get("recurring_failure_ids")
    if not isinstance(recurrences, list): errors.append(f"{path}.recurring_failure_ids: array required")
    result = record.get("retest_result")
    if result is not None and result not in {"improved", "unchanged", "worse", "inconclusive"}:
        errors.append(f"{path}.retest_result: invalid result")


VALIDATORS = {
    "belief": _validate_belief, "prediction": _validate_prediction,
    "decision": _validate_decision, "dialectic": _validate_dialectic,
    "causal_model": _validate_causal, "error": _validate_error,
}

COMMON_FIELDS = {"id", "kind", "provenance", "belief_ref", "prediction_ref", "decision_ref", "dialectic_ref", "causal_model_ref", "error_ref"}
KIND_FIELDS = {
    "belief": {"hypotheses", "evidence_updates", "revision_history"},
    "prediction": {"proposition", "probability", "made_at", "resolution_window_start", "resolution_window_end", "objective_resolution_criteria", "evidence_snapshot_hash", "outcome", "resolved_at", "scores"},
    "decision": {"actions", "states", "chosen_action", "rationale", "opportunity_cost", "value_of_information", "actual_state", "eventual_outcome", "regret"},
    "dialectic": {"claim", "clarification", "definitions", "commitments", "assumptions", "steelman", "burden_of_proof", "counterexamples", "contradictions", "cruxes", "falsifiers", "change_evidence", "revision_result"},
    "causal_model": {"nodes", "edges", "interventions", "confounders", "counterfactuals", "assumptions", "identification_limits"},
    "error": {"linked_record_ids", "classifications", "root_cause", "corrective_rule", "recurring_failure_ids", "retest_criterion", "retest_result"},
}


def validate_document(data: Mapping[str, Any]) -> tuple[str, ...]:
    """Return stable path-addressed validation errors without mutating input."""
    errors: list[str] = []
    unknown_document_fields = set(data) - {"format_version", "id", "far_ir_version", "records", "metadata"}
    for field in unknown_document_fields: errors.append(f"$.{field}: unknown field")
    if data.get("format_version") != FORMAT_VERSION:
        errors.append(f"format_version: expected {FORMAT_VERSION}")
    _required_text(data, "id", "$", errors)
    _required_text(data, "far_ir_version", "$", errors)
    if data.get("far_ir_version") not in {"far-ir/1.0", "far-ir/2.0", "far-ir/2.1"}:
        errors.append("$.far_ir_version: unsupported FAR IR version")
    records = _list(data, "records", "$", errors, nonempty=True)
    by_id = _ids(records, "$.records", errors)
    for index, record in enumerate(records):
        if not isinstance(record, Mapping): continue
        path = f"$.records[{index}]"
        kind = record.get("kind")
        if kind not in RECORD_KINDS:
            errors.append(f"{path}.kind: unsupported record kind")
        else:
            for field in set(record) - COMMON_FIELDS - KIND_FIELDS[kind]:
                errors.append(f"{path}.{field}: field is not valid for {kind} records")
            _provenance(record, path, errors)
            VALIDATORS[kind](record, path, errors)
    for rid, record in by_id.items():
        for field in ("belief_ref", "prediction_ref", "decision_ref", "dialectic_ref", "causal_model_ref", "error_ref"):
            if field in record and record[field] not in by_id:
                errors.append(f"$.records[{rid}].{field}: unknown record id")
        for field in ("linked_record_ids", "recurring_failure_ids"):
            for target in record.get(field, []):
                if target not in by_id:
                    errors.append(f"$.records[{rid}].{field}: unknown record id {target}")
    return tuple(sorted(set(errors)))


@dataclass(frozen=True, slots=True)
class EpistemicDocument:
    """Validated immutable facade; ``to_dict`` returns a defensive copy."""
    _canonical_json: str

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EpistemicDocument":
        if not isinstance(data, Mapping): raise EpistemicValidationError(("$: object required",))
        errors = validate_document(data)
        if errors: raise EpistemicValidationError(errors)
        return cls(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False))

    @classmethod
    def loads(cls, text: str) -> "EpistemicDocument":
        try: data = json.loads(text)
        except json.JSONDecodeError as exc: raise EpistemicValidationError((f"$: invalid JSON: {exc.msg}",)) from exc
        return cls.from_dict(data)

    @classmethod
    def load(cls, path: str | Path) -> "EpistemicDocument":
        return cls.loads(Path(path).read_text(encoding="utf-8"))

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self._canonical_json)

    def dumps(self, *, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, indent=indent, ensure_ascii=False) + ("\n" if indent else "")

    @property
    def digest(self) -> str:
        return "sha256:" + hashlib.sha256(self._canonical_json.encode()).hexdigest()

    def audit_event(self) -> dict[str, Any]:
        """Replay/certificate-compatible deterministic content commitment."""
        data = self.to_dict()
        return {"event": "far_epistemic_validation", "format_version": FORMAT_VERSION,
                "document_id": data["id"], "content_hash": self.digest,
                "record_ids": [r["id"] for r in data["records"]], "valid": True}


def score_binary(probability: Any, outcome: int) -> dict[str, Decimal]:
    """Compute negatively oriented Brier and natural-log loss (lower is better)."""
    errors: list[str] = []
    p = _prob(probability, "probability", errors, open_interval=True)
    if outcome not in (0, 1): errors.append("outcome: binary 0 or 1 required")
    if errors: raise EpistemicValidationError(errors)
    assert p is not None
    actual = Decimal(outcome)
    brier = (p - actual) ** 2
    log_loss = Decimal(str(-math.log(float(p if outcome else Decimal(1) - p))))
    return {"brier": brier, "log": log_loss}


def calibration(predictions: Iterable[Mapping[str, Any]], *, bins: int = 10) -> dict[str, Any]:
    """Return deterministic equal-width longitudinal calibration aggregates."""
    if not isinstance(bins, int) or isinstance(bins, bool) or bins < 1:
        raise EpistemicValidationError(("bins: positive integer required",))
    grouped: list[list[tuple[Decimal, int]]] = [[] for _ in range(bins)]
    for index, record in enumerate(predictions):
        errors: list[str] = []
        p = _prob(record.get("probability"), f"predictions[{index}].probability", errors)
        outcome = record.get("outcome")
        if outcome not in (0, 1, False, True): errors.append(f"predictions[{index}].outcome: resolved binary outcome required")
        if errors: raise EpistemicValidationError(errors)
        assert p is not None
        bucket = min(int(p * bins), bins - 1)
        grouped[bucket].append((p, int(outcome)))
    output = []
    all_items = [x for group in grouped for x in group]
    for index, group in enumerate(grouped):
        if group:
            count = Decimal(len(group))
            output.append({"bin": index, "count": len(group),
                           "mean_probability": str(sum((p for p, _ in group), Decimal(0)) / count),
                           "observed_frequency": str(sum((Decimal(o) for _, o in group), Decimal(0)) / count)})
    mean_brier = sum(((p - Decimal(o)) ** 2 for p, o in all_items), Decimal(0)) / Decimal(len(all_items)) if all_items else None
    return {"bins": output, "resolved_count": len(all_items), "mean_brier": None if mean_brier is None else str(mean_brier)}


def recurring_failure_modes(error_records: Iterable[Mapping[str, Any]], *, minimum: int = 2) -> list[dict[str, Any]]:
    """Detect repeated root-cause/classification signatures without semantic guessing."""
    if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 2:
        raise EpistemicValidationError(("minimum: integer of at least 2 required",))
    groups: dict[tuple[str, tuple[str, ...]], list[str]] = {}
    for index, record in enumerate(error_records):
        if record.get("kind") != "error" or not isinstance(record.get("id"), str):
            raise EpistemicValidationError((f"error_records[{index}]: ErrorRecord required",))
        root = record.get("root_cause")
        classifications = record.get("classifications")
        if not isinstance(root, str) or not root or not isinstance(classifications, list) or not all(isinstance(x, str) and x for x in classifications):
            raise EpistemicValidationError((f"error_records[{index}]: root cause and classifications required",))
        key = (root, tuple(sorted(set(classifications))))
        groups.setdefault(key, []).append(record["id"])
    return [{"root_cause": key[0], "classifications": list(key[1]), "count": len(ids), "record_ids": sorted(ids)}
            for key, ids in sorted(groups.items()) if len(ids) >= minimum]


def migrate(data: Mapping[str, Any]) -> dict[str, Any]:
    """Migrate the only predecessor format without guessing missing semantics."""
    if data.get("format_version") == FORMAT_VERSION:
        return json.loads(json.dumps(data))
    if data.get("format_version") != LEGACY_VERSION:
        raise EpistemicValidationError(("format_version: unsupported migration source",))
    result = json.loads(json.dumps(data))
    result["format_version"] = FORMAT_VERSION
    result.setdefault("far_ir_version", "far-ir/1.0")
    for record in result.get("records", []):
        if record.get("kind") == "prediction" and "resolution_date" in record:
            date = record.pop("resolution_date")
            record.setdefault("resolution_window_start", date)
            record.setdefault("resolution_window_end", date)
    # Validation is intentional: migration never fabricates provenance, uncertainty, or utilities.
    return EpistemicDocument.from_dict(result).to_dict()
