#!/usr/bin/env python3
"""Finite executable reference for SCORE-W2-PROOF-001.

This module corroborates the W2 dynamics/history construction on finite fixtures.
It is not a proof assistant and does not establish a complete Faithful_split witness.
"""
from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction
from typing import Any

SCHEMA = "DYN-HISTORY-1.0"
LIVE_STATUS = "permitted"
REVISION_KINDS = {"revise", "retract", "supersede"}
DECISIONS = {"accepted", "rejected"}


class W2Error(ValueError):
    """Malformed finite W2 source or target package."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def token(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:20]
    return f"{prefix}:{digest}"


def element_token(source_id: str, sort: str) -> str:
    return token("element", {"id": source_id, "sort": sort})


def parse_weight(value: Any) -> Fraction | None:
    if value is None:
        return None
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise W2Error(f"invalid exact weight: {value}") from exc
    if isinstance(value, list) and len(value) == 2:
        try:
            return Fraction(int(value[0]), int(value[1]))
        except (ValueError, ZeroDivisionError) as exc:
            raise W2Error(f"invalid exact weight: {value}") from exc
    raise W2Error(f"invalid exact weight: {value!r}")


def _unique(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        item_id = str(item.get("id", ""))
        if not item_id:
            raise W2Error(f"{label} requires id")
        if item_id in result:
            raise W2Error(f"duplicate {label}: {item_id}")
        result[item_id] = item
    return result


def validate_source(source: dict[str, Any]) -> None:
    if source.get("schema_version") != "1.0":
        raise W2Error("source.schema_version must equal 1.0")
    states = _unique(source.get("states", []), "state")
    transitions = _unique(source.get("transitions", []), "transition")
    rules = _unique(source.get("rules", []), "rule")
    versions = _unique(source.get("rule_versions", []), "rule_version")
    events = _unique(source.get("history", {}).get("events", []), "event")

    for version_id, version in versions.items():
        rule_id = str(version.get("rule", ""))
        if rule_id not in rules:
            raise W2Error(f"rule version {version_id} references unknown rule: {rule_id}")

    for state_id, state in states.items():
        active = [str(x) for x in state.get("active_rule_versions", [])]
        missing = set(active) - set(versions)
        if missing:
            raise W2Error(f"state {state_id} has unknown active rule versions: {sorted(missing)}")
        commitments = state.get("commitments", {})
        if not isinstance(commitments, dict):
            raise W2Error(f"state {state_id} commitments must be an object")

    kernel_groups: dict[tuple[str, str], list[Fraction]] = {}
    for transition_id, transition in transitions.items():
        source_id = str(transition.get("from", ""))
        target_id = str(transition.get("to", ""))
        if source_id not in states or target_id not in states:
            raise W2Error(f"transition {transition_id} references unknown state")
        status = str(transition.get("status", ""))
        if not status:
            raise W2Error(f"transition {transition_id} requires status")
        label = str(transition.get("label", ""))
        if not label:
            raise W2Error(f"transition {transition_id} requires label")
        rule_version = transition.get("rule_version")
        if rule_version is not None:
            rule_version = str(rule_version)
            if rule_version not in versions:
                raise W2Error(f"transition {transition_id} references unknown rule version: {rule_version}")
            if status == LIVE_STATUS and rule_version not in states[source_id].get("active_rule_versions", []):
                raise W2Error(f"permitted transition {transition_id} uses inactive rule version at {source_id}")
        weight = parse_weight(transition.get("weight"))
        kernel = transition.get("kernel")
        if kernel is None and weight is not None:
            raise W2Error(f"weighted transition {transition_id} requires kernel")
        if kernel is not None:
            if weight is None:
                raise W2Error(f"kernel transition {transition_id} requires weight")
            if weight < 0:
                raise W2Error(f"transition {transition_id} has negative weight")
            if status == LIVE_STATUS:
                kernel_groups.setdefault((source_id, str(kernel)), []).append(weight)
    for key, weights in kernel_groups.items():
        if sum(weights, Fraction(0, 1)) != Fraction(1, 1):
            raise W2Error(f"live kernel {key} weights must sum to 1")

    history = source.get("history", {})
    event_ids = set(events)
    for relation_name in ("order", "causal", "dependency_ancestry"):
        for pair in history.get(relation_name, []):
            if not isinstance(pair, list) or len(pair) != 2 or set(map(str, pair)) - event_ids:
                raise W2Error(f"history.{relation_name} contains unknown event pair: {pair}")
    for provenance in history.get("provenance", []):
        if str(provenance.get("event", "")) not in event_ids:
            raise W2Error("history provenance references unknown event")
    for event_id, event in events.items():
        if str(event.get("state", "")) not in states:
            raise W2Error(f"event {event_id} references unknown state")
        transition_id = event.get("transition")
        if transition_id is not None and str(transition_id) not in transitions:
            raise W2Error(f"event {event_id} references unknown transition")

    for revision in history.get("revisions", []):
        if str(revision.get("kind", "")) not in REVISION_KINDS:
            raise W2Error("revision requires revise, retract, or supersede kind")
        before_state = str(revision.get("before_state", ""))
        after_state = str(revision.get("after_state", ""))
        event_id = str(revision.get("event", ""))
        subject = str(revision.get("subject", ""))
        if before_state not in states or after_state not in states or event_id not in event_ids or not subject:
            raise W2Error("revision references unknown state/event or missing subject")
        before = revision.get("before")
        after = revision.get("after")
        if states[before_state].get("commitments", {}).get(subject) != before:
            raise W2Error(f"revision before value does not match state {before_state}")
        if states[after_state].get("commitments", {}).get(subject) != after:
            raise W2Error(f"revision after value does not match state {after_state}")

    for modification in history.get("modifications", []):
        decision = str(modification.get("decision", ""))
        if decision not in DECISIONS:
            raise W2Error("modification decision must be accepted or rejected")
        before_state = str(modification.get("before_state", ""))
        after_state = str(modification.get("after_state", ""))
        event_id = str(modification.get("event", ""))
        if before_state not in states or after_state not in states or event_id not in event_ids:
            raise W2Error("modification references unknown state/event")
        before_active = set(map(str, states[before_state].get("active_rule_versions", [])))
        after_active = set(map(str, states[after_state].get("active_rule_versions", [])))
        deactivates = set(map(str, modification.get("deactivates", [])))
        activates = set(map(str, modification.get("activates", [])))
        if not (deactivates | activates) <= set(versions):
            raise W2Error("modification references unknown rule version")
        if decision == "accepted":
            expected = (before_active - deactivates) | activates
            if after_active != expected:
                raise W2Error("accepted modification does not produce declared active rule versions")
        elif after_active != before_active:
            raise W2Error("rejected modification changes active rule versions")

    for condition in history.get("path_conditions", []):
        path = [str(x) for x in condition.get("path", [])]
        if not path or set(path) - event_ids:
            raise W2Error("path condition references unknown or empty path")


def construct_target(source: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_source(source)
    states = {str(item["id"]): item for item in source["states"]}
    rules = {str(item["id"]): item for item in source.get("rules", [])}
    versions = {str(item["id"]): item for item in source.get("rule_versions", [])}
    history = source.get("history", {})

    state_map = {state_id: element_token(state_id, "configuration") for state_id in states}
    transition_map = {str(item["id"]): token("transition", str(item["id"])) for item in source.get("transitions", [])}
    event_map = {str(item["id"]): token("event", str(item["id"])) for item in history.get("events", [])}
    rule_map = {rule_id: element_token(rule_id, "rule") for rule_id in rules}
    version_map = {version_id: token("rule_version", version_id) for version_id in versions}

    target: dict[str, Any] = {
        "schema": SCHEMA,
        "U": [], "Pi": [], "R": {}, "Rep": [], "S": {"representations": [], "relations": []}, "I": [],
        "Inv": {"id": "inv:S_core:W2", "scope": "finite_dynamics_history_revision"},
        "C": {"rules": [], "rule_versions": [], "active_rule_versions": []},
        "Sigma": [], "Theta": [], "H": {}, "Omega": {"transition_statuses": []}, "Res": {"status": "typed_empty_at_W2"},
        "Prov": [],
        "kappa_W2": {
            "schema": SCHEMA,
            "constructor": "tools/s_core_w2_reference.py",
            "live_transition_definition": "status=permitted and required rule version active at source state",
            "probabilistic_kernel_definition": "finite exact weights grouped by source state and kernel",
            "history_definition": "exact copied material order, causal, provenance, revision, modification, ancestry, and path facts",
            "source_specific_content_is_data": True,
            "case_database": False,
            "external_interpreter": False,
        },
    }

    def add_object(object_id: str, kind: str, payload: Any) -> None:
        if any(item["id"] == object_id for item in target["U"]):
            return
        rep_id = f"rep:{object_id}"
        target["U"].append({"id": object_id, "kind": kind, "payload": copy.deepcopy(payload)})
        target["Pi"].append({"object": object_id, "property": "kind", "value": kind})
        target["Rep"].append({"id": rep_id, "kind": "representation", "represents": object_id})
        target["S"]["representations"].append(rep_id)
        target["S"]["relations"].append(["represents", rep_id, object_id])

    for state_id, state in sorted(states.items()):
        state_object = state_map[state_id]
        add_object(state_object, "configuration", {"source_key": state_id})
        active = [version_map[str(v)] for v in state.get("active_rule_versions", [])]
        target["Sigma"].append({
            "id": state_object,
            "source_key": state_id,
            "commitments": copy.deepcopy(state.get("commitments", {})),
            "active_rule_versions": sorted(active),
            "resources": copy.deepcopy(state.get("resources", {})),
        })
        for version in active:
            target["C"]["active_rule_versions"].append([state_object, version])

    for rule_id, rule in sorted(rules.items()):
        add_object(rule_map[rule_id], "rule", {"source_key": rule_id})
        target["C"]["rules"].append({"id": rule_map[rule_id], "source_key": rule_id, "payload": copy.deepcopy(rule)})
    for version_id, version in sorted(versions.items()):
        add_object(version_map[version_id], "rule_version", {"source_key": version_id})
        target["C"]["rule_versions"].append({
            "id": version_map[version_id],
            "source_key": version_id,
            "rule": rule_map[str(version["rule"])],
            "payload": copy.deepcopy(version),
        })

    for transition in sorted(source.get("transitions", []), key=lambda item: str(item["id"])):
        transition_id = str(transition["id"])
        object_id = transition_map[transition_id]
        add_object(object_id, "transition", {"source_key": transition_id})
        version = transition.get("rule_version")
        record = {
            "id": object_id,
            "source_key": transition_id,
            "from": state_map[str(transition["from"])],
            "to": state_map[str(transition["to"])],
            "label": copy.deepcopy(transition["label"]),
            "status": str(transition["status"]),
            "rule_version": version_map[str(version)] if version is not None else None,
            "kernel": copy.deepcopy(transition.get("kernel")),
            "weight": str(parse_weight(transition.get("weight"))) if transition.get("weight") is not None else None,
            "preconditions": copy.deepcopy(transition.get("preconditions", [])),
            "resource_conditions": copy.deepcopy(transition.get("resource_conditions", [])),
            "action_dependencies": copy.deepcopy(transition.get("action_dependencies", [])),
            "observation_dependencies": copy.deepcopy(transition.get("observation_dependencies", [])),
        }
        target["Theta"].append(record)
        target["Omega"]["transition_statuses"].append([object_id, record["status"]])

    target["H"] = {
        "events": [],
        "order": [[event_map[str(a)], event_map[str(b)]] for a, b in history.get("order", [])],
        "causal": [[event_map[str(a)], event_map[str(b)]] for a, b in history.get("causal", [])],
        "provenance": [],
        "revisions": [],
        "modifications": [],
        "dependency_ancestry": [[event_map[str(a)], event_map[str(b)]] for a, b in history.get("dependency_ancestry", [])],
        "path_conditions": [],
    }
    for event in sorted(history.get("events", []), key=lambda item: str(item["id"])):
        event_id = str(event["id"])
        object_id = event_map[event_id]
        add_object(object_id, "history_event", {"source_key": event_id})
        transition = event.get("transition")
        target["H"]["events"].append({
            "id": object_id,
            "source_key": event_id,
            "state": state_map[str(event["state"])],
            "transition": transition_map[str(transition)] if transition is not None else None,
            "kind": copy.deepcopy(event.get("kind")),
        })
    for item in history.get("provenance", []):
        record = copy.deepcopy(item)
        record["event"] = event_map[str(item["event"])]
        target["H"]["provenance"].append(record)
        target["Prov"].append(copy.deepcopy(record))
    for item in history.get("revisions", []):
        record = copy.deepcopy(item)
        record.update({
            "event": event_map[str(item["event"])],
            "before_state": state_map[str(item["before_state"])],
            "after_state": state_map[str(item["after_state"])],
        })
        target["H"]["revisions"].append(record)
    for item in history.get("modifications", []):
        record = copy.deepcopy(item)
        record.update({
            "event": event_map[str(item["event"])],
            "before_state": state_map[str(item["before_state"])],
            "after_state": state_map[str(item["after_state"])],
            "deactivates": [version_map[str(x)] for x in item.get("deactivates", [])],
            "activates": [version_map[str(x)] for x in item.get("activates", [])],
        })
        target["H"]["modifications"].append(record)
    for item in history.get("path_conditions", []):
        record = copy.deepcopy(item)
        record["path"] = [event_map[str(x)] for x in item.get("path", [])]
        target["H"]["path_conditions"].append(record)

    for key in ("U", "Pi", "Rep", "I", "Prov", "Sigma", "Theta"):
        target[key].sort(key=canonical_json)
    target["S"]["representations"].sort()
    target["S"]["relations"].sort(key=canonical_json)
    for key in target["H"]:
        target["H"][key].sort(key=canonical_json)
    for key in target["C"]:
        target["C"][key].sort(key=canonical_json)
    target["Omega"]["transition_statuses"].sort(key=canonical_json)

    witness = {
        "state_map": state_map,
        "transition_map": transition_map,
        "event_map": event_map,
        "rule_map": rule_map,
        "version_map": version_map,
    }
    return target, witness


def _target_state_by_id(target: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in target.get("Sigma", [])}


def live_target_transitions(target: dict[str, Any]) -> list[dict[str, Any]]:
    states = _target_state_by_id(target)
    result = []
    for transition in target.get("Theta", []):
        if transition.get("status") != LIVE_STATUS:
            continue
        version = transition.get("rule_version")
        if version is not None and version not in states[str(transition["from"])].get("active_rule_versions", []):
            continue
        result.append(transition)
    return result


def source_live_transitions(source: dict[str, Any]) -> list[dict[str, Any]]:
    states = {str(item["id"]): item for item in source.get("states", [])}
    result = []
    for transition in source.get("transitions", []):
        if transition.get("status") != LIVE_STATUS:
            continue
        version = transition.get("rule_version")
        if version is not None and str(version) not in states[str(transition["from"])].get("active_rule_versions", []):
            continue
        result.append(transition)
    return result


def _source_transition_signature(item: dict[str, Any]) -> tuple[Any, ...]:
    return (
        str(item["id"]), str(item["from"]), str(item["to"]), canonical_json(item["label"]),
        str(item["status"]), str(item.get("rule_version")), canonical_json(item.get("kernel")),
        str(parse_weight(item.get("weight"))) if item.get("weight") is not None else None,
        canonical_json(item.get("preconditions", [])), canonical_json(item.get("resource_conditions", [])),
        canonical_json(item.get("action_dependencies", [])), canonical_json(item.get("observation_dependencies", [])),
    )


def _target_transition_signature(item: dict[str, Any], witness: dict[str, Any]) -> tuple[Any, ...]:
    inv_state = {v: k for k, v in witness["state_map"].items()}
    inv_transition = {v: k for k, v in witness["transition_map"].items()}
    inv_version = {v: k for k, v in witness["version_map"].items()}
    version = item.get("rule_version")
    return (
        inv_transition[str(item["id"])], inv_state[str(item["from"])], inv_state[str(item["to"])],
        canonical_json(item["label"]), str(item["status"]), str(inv_version.get(version)) if version is not None else "None",
        canonical_json(item.get("kernel")), item.get("weight"), canonical_json(item.get("preconditions", [])),
        canonical_json(item.get("resource_conditions", [])), canonical_json(item.get("action_dependencies", [])),
        canonical_json(item.get("observation_dependencies", [])),
    )


def check_dynamics(source: dict[str, Any], target: dict[str, Any], witness: dict[str, Any]) -> bool:
    try:
        validate_source(source)
        source_all = {_source_transition_signature(item) for item in source.get("transitions", [])}
        target_all = {_target_transition_signature(item, witness) for item in target.get("Theta", [])}
        if source_all != target_all:
            return False
        source_live = {_source_transition_signature(item) for item in source_live_transitions(source)}
        target_live = {_target_transition_signature(item, witness) for item in live_target_transitions(target)}
        if source_live != target_live:
            return False
        source_states = {str(item["id"]): item for item in source.get("states", [])}
        target_states = _target_state_by_id(target)
        for source_id, target_id in witness["state_map"].items():
            source_state = source_states[source_id]
            target_state = target_states.get(target_id)
            if target_state is None:
                return False
            mapped_active = sorted(witness["version_map"][str(v)] for v in source_state.get("active_rule_versions", []))
            if target_state.get("active_rule_versions") != mapped_active:
                return False
            if target_state.get("commitments") != source_state.get("commitments", {}):
                return False
            if target_state.get("resources") != source_state.get("resources", {}):
                return False
        return True
    except (KeyError, TypeError, W2Error):
        return False


def _normalize_history_source(source: dict[str, Any]) -> dict[str, Any]:
    history = copy.deepcopy(source.get("history", {}))
    for key in history:
        if isinstance(history[key], list):
            history[key].sort(key=canonical_json)
    return history


def _normalize_history_target(target: dict[str, Any], witness: dict[str, Any]) -> dict[str, Any]:
    inv_state = {v: k for k, v in witness["state_map"].items()}
    inv_transition = {v: k for k, v in witness["transition_map"].items()}
    inv_event = {v: k for k, v in witness["event_map"].items()}
    inv_version = {v: k for k, v in witness["version_map"].items()}
    h = copy.deepcopy(target.get("H", {}))
    result: dict[str, Any] = {"events": [], "order": [], "causal": [], "provenance": [], "revisions": [], "modifications": [], "dependency_ancestry": [], "path_conditions": []}
    for item in h.get("events", []):
        result["events"].append({
            "id": inv_event[str(item["id"])], "state": inv_state[str(item["state"])],
            "transition": inv_transition[str(item["transition"])] if item.get("transition") is not None else None,
            "kind": item.get("kind"),
        })
    for key in ("order", "causal", "dependency_ancestry"):
        result[key] = [[inv_event[str(a)], inv_event[str(b)]] for a, b in h.get(key, [])]
    for item in h.get("provenance", []):
        record = copy.deepcopy(item); record["event"] = inv_event[str(item["event"])]; result["provenance"].append(record)
    for item in h.get("revisions", []):
        record = copy.deepcopy(item)
        record.update({"event": inv_event[str(item["event"])], "before_state": inv_state[str(item["before_state"])], "after_state": inv_state[str(item["after_state"])]})
        result["revisions"].append(record)
    for item in h.get("modifications", []):
        record = copy.deepcopy(item)
        record.update({
            "event": inv_event[str(item["event"])], "before_state": inv_state[str(item["before_state"])], "after_state": inv_state[str(item["after_state"])],
            "deactivates": [inv_version[str(x)] for x in item.get("deactivates", [])],
            "activates": [inv_version[str(x)] for x in item.get("activates", [])],
        })
        result["modifications"].append(record)
    for item in h.get("path_conditions", []):
        record = copy.deepcopy(item); record["path"] = [inv_event[str(x)] for x in item.get("path", [])]; result["path_conditions"].append(record)
    for key in result:
        result[key].sort(key=canonical_json)
    return result


def check_history(source: dict[str, Any], target: dict[str, Any], witness: dict[str, Any]) -> bool:
    try:
        validate_source(source)
        return _normalize_history_source(source) == _normalize_history_target(target, witness)
    except (KeyError, TypeError, W2Error):
        return False


def check_w2(source: dict[str, Any], target: dict[str, Any], witness: dict[str, Any]) -> bool:
    return target.get("schema") == SCHEMA and check_dynamics(source, target, witness) and check_history(source, target, witness)
