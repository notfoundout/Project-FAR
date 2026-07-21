from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from s_core_w3_schema import canonical_json

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DECISIONS = {"positive", "contrast", "disputed"}

AXIS_ROLES: dict[str, tuple[tuple[str, str, str], ...]] = {'P1': (('relation', 'P1.system_state', 'source-declared system to observable-state incidence'), ('relation', 'P1.system_payload', 'source-declared authoritative-payload incidence'), ('relation', 'P1.task_of', 'source-declared task incidence'), ('attribute', 'P1.state_label', 'source-declared observable-state label'), ('attribute', 'P1.formalization_boundary', 'source-declared formalization boundary')), 'P2': (('relation', 'P2.source_commitment', 'source-declared commitment-or-alternative statement'), ('attribute', 'P2.commitment_statement', 'verbatim source commitment-or-alternative statement')), 'P3': (('relation', 'P3.task_context', 'task, commitment statement, and system context'), ('attribute', 'P3.task_statement', 'verbatim source objective or task')), 'P4': (('relation', 'P4.source_ground', 'source-declared ground or dependency'), ('attribute', 'P4.ground_statement', 'verbatim source ground or dependency statement')), 'P6': (('relation', 'P6.source_result', 'source-declared result incidence'), ('attribute', 'P6.result_value', 'source-declared result value')), 'P8I': (('relation', 'P8I.uncertainty_for', 'source-declared uncertainty or revision status'), ('relation', 'P8I.provenance_for', 'source-declared provenance and correspondence limit'), ('attribute', 'P8I.uncertainty_statement', 'verbatim uncertainty or revision statement'), ('attribute', 'P8I.provenance_statement', 'verbatim provenance and correspondence limit'), ('attribute', 'P8I.evidence_status', 'internal status of the encoded source declaration'))}

class FactorizationError(ValueError):
    """Invalid corpus source, GREL package, or factorization witness."""

def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def _short(value: Any) -> str:
    return sha256_json(value)[:20]

def _record_id(prefix: str, value: Any) -> str:
    return f"{prefix}:{_short(value)}"

def load_records(root: Path = ROOT) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index in range(1, 7):
        path = root / "theory" / "evaluation" / "rcs-corpus-sources" / f"rcs-source-bundle-{index:02d}.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("status") != "frozen":
            raise FactorizationError(f"{path}: source bundle is not frozen")
        for record in payload.get("records", []):
            instance_id = str(record.get("instance_id", ""))
            if not instance_id or instance_id in seen:
                raise FactorizationError(f"duplicate or missing instance id: {instance_id!r}")
            if record.get("admission_decision") not in ALLOWED_DECISIONS:
                raise FactorizationError(f"{instance_id}: invalid admission decision")
            seen.add(instance_id)
            item = copy.deepcopy(record)
            item["_source_bundle"] = path.relative_to(root).as_posix()
            records.append(item)
    records.sort(key=lambda item: item["instance_id"])
    if len(records) != 18:
        raise FactorizationError(f"expected 18 frozen corpus records, found {len(records)}")
    return records

def authoritative_projection(record: dict[str, Any]) -> dict[str, Any]:
    """Return only candidate-neutral, source-authoritative fields.

    Admission class, family, title, rationale, and candidate exposure metadata
    are deliberately excluded so they cannot steer construction.
    """
    return {
        "formal_system": copy.deepcopy(record["formal_system"]),
        "candidate_neutral_observations": copy.deepcopy(record["candidate_neutral_observations"]),
        "formalization_boundary": record["formalization_boundary"],
    }

def _result_value(formal_system: dict[str, Any]) -> Any:
    for key in ("result", "decision", "selected"):
        if key in formal_system:
            return copy.deepcopy(formal_system[key])
    for key in ("event_trace", "trace"):
        sequence = formal_system.get(key)
        if isinstance(sequence, list) and sequence:
            return copy.deepcopy(sequence[-1])
    return copy.deepcopy(formal_system)

def compile_projection(projection: dict[str, Any]) -> dict[str, Any]:
    """Compile one candidate-neutral authoritative projection into S_core.

    This adapter is fixed across the corpus, but it is FARA-oriented machinery:
    it projects source fields into the six registered preservation axes. It is
    therefore declared in the factorization witness and may not be treated as
    part of the neutral GREL baseline or as a primitive reduction.
    """
    obs = projection["candidate_neutral_observations"]
    formal = projection["formal_system"]
    digest = _short(projection)

    states = list(obs.get("observable_or_formal_states", []))
    constraints = list(obs.get("transitions_and_constraints", []))
    distinctions = list(obs.get("represented_distinctions", []))
    grounds = list(obs.get("grounds_or_dependencies", []))
    if not states or not constraints or not distinctions or not grounds:
        raise FactorizationError("authoritative observation fields must be nonempty")

    carriers: list[dict[str, Any]] = []
    seen_carriers: set[str] = set()

    def carrier(prefix: str, sort: str, denotation: Any) -> str:
        item_id = _record_id(prefix, {"digest": digest, "denotation": denotation})
        if item_id not in seen_carriers:
            seen_carriers.add(item_id)
            carriers.append({"id": item_id, "sort": sort, "display_label": prefix, "denotation": copy.deepcopy(denotation)})
        return item_id

    system_id = carrier("system", "system", "the frozen candidate-neutral formal episode")
    payload_id = carrier("payload", "field_value", projection)
    task_text = obs.get("objectives_or_tasks")
    commitment_text = obs.get("commitment_or_alternative_structure")
    uncertainty_text = obs.get("uncertainty_and_revision")
    provenance_text = obs.get("provenance_and_correspondence_limits")
    task_id = carrier("task", "field_value", task_text)
    commitment_id = carrier("commitment_statement", "field_value", commitment_text)
    uncertainty_id = carrier("uncertainty_statement", "field_value", uncertainty_text)
    provenance_id = carrier("provenance_statement", "field_value", provenance_text)
    result_value = _result_value(formal)
    result_id = carrier("result", "field_value", result_value)
    state_ids = [carrier(f"state_{index}", "configuration", value) for index, value in enumerate(states)]
    ground_ids = [carrier(f"ground_{index}", "ground", value) for index, value in enumerate(grounds)]
    distinction_ids = [carrier(f"distinction_{index}", "content", value) for index, value in enumerate(distinctions)]

    occurrence_counter = 0
    def occurrence(prefix: str) -> str:
        nonlocal occurrence_counter
        occurrence_counter += 1
        return f"occ:{digest}:{prefix}:{occurrence_counter:04d}"
    def attribute(prefix: str) -> str:
        nonlocal occurrence_counter
        occurrence_counter += 1
        return f"attr:{digest}:{prefix}:{occurrence_counter:04d}"

    axes: dict[str, dict[str, Any]] = {axis: {"members": [], "relations": [], "attributes": []} for axis in ("P1", "P2", "P3", "P4", "P6", "P8I")}
    def members(axis: str, *ids: str) -> None:
        axes[axis]["members"] = sorted(set(axes[axis]["members"]) | set(ids))

    members("P1", system_id, payload_id, task_id, *state_ids, *distinction_ids)
    for state_id in state_ids:
        axes["P1"]["relations"].append({"id": occurrence("p1-state"), "role": "P1.system_state", "args": [system_id, state_id]})
    axes["P1"]["relations"].append({"id": occurrence("p1-payload"), "role": "P1.system_payload", "args": [system_id, payload_id]})
    axes["P1"]["relations"].append({"id": occurrence("p1-task"), "role": "P1.task_of", "args": [task_id, system_id]})
    for state_id, state_value in zip(state_ids, states):
        axes["P1"]["attributes"].append({"id": attribute("p1-state-label"), "owner": state_id, "role": "P1.state_label", "value": state_value})
    axes["P1"]["attributes"].append({"id": attribute("p1-boundary"), "owner": system_id, "role": "P1.formalization_boundary", "value": projection["formalization_boundary"]})

    members("P2", system_id, commitment_id)
    axes["P2"]["relations"].append({"id": occurrence("p2-commitment"), "role": "P2.source_commitment", "args": [commitment_id, system_id]})
    axes["P2"]["attributes"].append({"id": attribute("p2-statement"), "owner": commitment_id, "role": "P2.commitment_statement", "value": commitment_text})

    members("P3", system_id, task_id, commitment_id)
    axes["P3"]["relations"].append({"id": occurrence("p3-context"), "role": "P3.task_context", "args": [task_id, commitment_id, system_id]})
    axes["P3"]["attributes"].append({"id": attribute("p3-task"), "owner": task_id, "role": "P3.task_statement", "value": task_text})

    members("P4", system_id, *ground_ids)
    for ground_id, ground_value in zip(ground_ids, grounds):
        axes["P4"]["relations"].append({"id": occurrence("p4-ground"), "role": "P4.source_ground", "args": [ground_id, system_id]})
        axes["P4"]["attributes"].append({"id": attribute("p4-ground-statement"), "owner": ground_id, "role": "P4.ground_statement", "value": ground_value})

    members("P6", system_id, result_id)
    axes["P6"]["relations"].append({"id": occurrence("p6-result"), "role": "P6.source_result", "args": [result_id, system_id]})
    axes["P6"]["attributes"].append({"id": attribute("p6-result-value"), "owner": result_id, "role": "P6.result_value", "value": result_value})

    members("P8I", system_id, uncertainty_id, provenance_id)
    axes["P8I"]["relations"].extend([
        {"id": occurrence("p8-uncertainty"), "role": "P8I.uncertainty_for", "args": [uncertainty_id, system_id]},
        {"id": occurrence("p8-provenance"), "role": "P8I.provenance_for", "args": [provenance_id, system_id]},
    ])
    axes["P8I"]["attributes"].extend([
        {"id": attribute("p8-uncertainty"), "owner": uncertainty_id, "role": "P8I.uncertainty_statement", "value": uncertainty_text},
        {"id": attribute("p8-provenance"), "owner": provenance_id, "role": "P8I.provenance_statement", "value": provenance_text},
        {"id": attribute("p8-status"), "owner": system_id, "role": "P8I.evidence_status", "value": "source_declared"},
    ])

    rule_ids = [f"rule:{digest}:{index:03d}" for index in range(len(constraints))]
    version_ids = [f"rule_version:{digest}:{index:03d}" for index in range(len(constraints))]
    rules = [{"id": rule_id, "kind": "source_constraint"} for rule_id in rule_ids]
    versions = [{"id": version_id, "rule": rule_id, "version": 1} for rule_id, version_id in zip(rule_ids, version_ids)]
    state_records = []
    for index, state_id in enumerate(state_ids):
        status = "recorded" if index == len(state_ids) - 1 else ("open" if index else "initialized")
        state_records.append({"id": state_id, "commitments": {commitment_id: status}, "active_rule_versions": list(version_ids), "resources": {"observation_index": index}})
    transitions = []
    transition_ids = []
    for index in range(max(0, len(state_ids) - 1)):
        transition_id = f"transition:{digest}:{index:03d}"
        transition_ids.append(transition_id)
        transitions.append({"id": transition_id, "from": state_ids[index], "to": state_ids[index + 1], "label": constraints[index % len(constraints)], "status": "permitted", "rule_version": version_ids[index % len(version_ids)], "preconditions": [], "resource_conditions": [], "action_dependencies": [], "observation_dependencies": []})
    event_ids = [f"event:{digest}:{index:03d}" for index in range(len(state_ids))]
    events = [{"id": event_id, "state": state_id, "transition": None if index == 0 else transition_ids[index - 1], "kind": "initial" if index == 0 else "source_transition"} for index, (event_id, state_id) in enumerate(zip(event_ids, state_ids))]
    order = [[event_ids[i], event_ids[j]] for i in range(len(event_ids)) for j in range(i, len(event_ids))]
    causal = [[event_ids[i], event_ids[i + 1]] for i in range(len(event_ids) - 1)]
    ancestry = [[event_ids[i], event_ids[j]] for i in range(len(event_ids)) for j in range(i + 1, len(event_ids))]
    history = {"events": events, "order": order, "causal": causal, "provenance": [{"event": event_ids[-1], "source": provenance_text, "grade": "source_declared"}], "revisions": [], "modifications": [], "dependency_ancestry": ancestry, "path_conditions": []}

    sort_names = sorted({item["sort"] for item in carriers} | {"rule", "rule_version", "transition", "event", "relation_occurrence", "attribute_occurrence"})
    role_denotations = [{"kind": kind, "role": role, "denotation": denotation} for axis in sorted(AXIS_ROLES) for kind, role, denotation in AXIS_ROLES[axis]]

    return {
        "schema_version": "1.0",
        "carriers": sorted(carriers, key=lambda item: item["id"]),
        "axes": {axis: {"members": sorted(data["members"]), "relations": sorted(data["relations"], key=canonical_json), "attributes": sorted(data["attributes"], key=canonical_json)} for axis, data in axes.items()},
        "dynamics": {"rules": rules, "rule_versions": versions, "states": state_records, "transitions": transitions, "history": history},
        "semantics": {"sort_denotations": [{"sort": sort_name, "denotation": f"the source-declared sort {sort_name}"} for sort_name in sort_names], "role_denotations": role_denotations, "value_equivalences": []},
        "decomposition": {"components": [], "interfaces": [], "cross_component_relations": []},
    }

def compile_record(record: dict[str, Any]) -> dict[str, Any]:
    return compile_projection(authoritative_projection(record))
