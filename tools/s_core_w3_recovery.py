from __future__ import annotations
import copy
from collections import defaultdict
from typing import Any
from s_core_w3_schema import AXES, FIXED_RELATIONS, RECOVERED_SCHEMA, RECOVERY_SCHEMA, REQUIRED_A_FIELDS, REQUIRED_W_FIELDS, SCHEMA, W3Error, canonical_json
from s_core_w3_builder import _sort_records
from s_core_w3_machinery import validate_kappa

def _object_map(A: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {str(item.get("id", "")): item for item in A.get("U", [])}
    if "" in result or len(result) != len(A.get("U", [])):
        raise W3Error("target objects require unique ids")
    return result


def _property_maps(A: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
    literals: dict[str, Any] = {}
    positions: dict[str, int] = {}
    for item in A.get("Pi", []):
        object_id = str(item.get("object", "")); prop = str(item.get("property", ""))
        if prop == "literal":
            if object_id in literals and literals[object_id] != item.get("value"):
                raise W3Error("value object has conflicting literals")
            literals[object_id] = copy.deepcopy(item.get("value"))
        elif prop == "position":
            positions[object_id] = int(item.get("value"))
    return literals, positions


def validate_package(package: dict[str, Any]) -> None:
    if package.get("schema") != SCHEMA:
        raise W3Error("wrong package schema")
    A = package.get("A"); W = package.get("W")
    if not isinstance(A, dict) or not isinstance(W, dict):
        raise W3Error("package requires A and W")
    if any(field not in A for field in REQUIRED_A_FIELDS) or any(field not in W for field in REQUIRED_W_FIELDS):
        raise W3Error("package is missing required A or W field")
    if A.get("schema") != SCHEMA:
        raise W3Error("target schema mismatch")
    objects = _object_map(A)
    reps = {str(item.get("id", "")): item for item in A.get("Rep", [])}
    if len(reps) != len(A.get("Rep", [])) or len(reps) != len(objects):
        raise W3Error("representations must be unique and one-per-object")
    if set(objects) & set(reps):
        raise W3Error("object and representation namespaces must be disjoint")
    if set(A.get("R", {})) != set(FIXED_RELATIONS):
        raise W3Error("target relation schema changed")
    represented = {tuple(x) for x in A["R"]["represented_by"]}
    denoted = {tuple(x) for x in A["R"]["denotes"]}
    for object_id in objects:
        rep_id = f"rep:{object_id}"
        if rep_id not in reps or (object_id, rep_id) not in represented or (rep_id, object_id) not in denoted:
            raise W3Error("object/representation separation is incomplete")
    _property_maps(A)
    D = W.get("D", {})
    if D != {"schema": RECOVERY_SCHEMA, "algorithm": "recover_target", "target_only": True, "deterministic": True, "terminates_on_finite_target": True}:
        raise W3Error("recovery descriptor changed")
    validate_kappa(W.get("kappa", {}))
    E = W.get("E", {})
    if len(set(E.values())) != len(E):
        raise W3Error("source entity correspondence is not injective")
    if set(E.values()) - set(objects):
        raise W3Error("correspondence references unknown target objects")
    if W.get("iota", {}).get("component") != "A.I" or W.get("iota", {}).get("no_lexical_shortcuts") is not True:
        raise W3Error("interpretation descriptor changed")


def recover_target(A: dict[str, Any], D: dict[str, Any], kappa: dict[str, Any]) -> dict[str, Any]:
    """Recover the canonical target-indexed source contract without source access."""
    if D != {"schema": RECOVERY_SCHEMA, "algorithm": "recover_target", "target_only": True, "deterministic": True, "terminates_on_finite_target": True}:
        raise W3Error("inadmissible recovery descriptor")
    validate_kappa(kappa)
    if A.get("schema") != SCHEMA:
        raise W3Error("target schema mismatch")
    objects = _object_map(A)
    literals, positions = _property_maps(A)
    sorts: dict[str, str] = {}
    for object_id, sort_id in A.get("R", {}).get("has_sort", []):
        if object_id in sorts and sorts[object_id] != sort_id:
            raise W3Error("target object has conflicting sorts")
        if object_id not in objects or sort_id not in objects:
            raise W3Error("sort relation references unknown object")
        sorts[object_id] = sort_id

    axis_members: dict[str, set[str]] = {axis: set() for axis in AXES}
    axis_ids = {f"axis:{axis}": axis for axis in AXES}
    for axis_id, member in A["R"]["axis_member"]:
        if axis_id not in axis_ids or member not in objects:
            raise W3Error("axis_member references unknown axis/object")
        axis_members[axis_ids[axis_id]].add(member)
    in_axis: dict[str, str] = {}
    for occurrence, axis_id in A["R"]["in_axis"]:
        if occurrence not in objects or axis_id not in axis_ids or occurrence in in_axis:
            raise W3Error("in_axis malformed or duplicated")
        in_axis[occurrence] = axis_ids[axis_id]
    relation_roles = {str(a): str(b) for a, b in A["R"]["occurrence_role"]}
    attribute_roles = {str(a): str(b) for a, b in A["R"]["attribute_role"]}
    attribute_owners = {str(a): str(b) for a, b in A["R"]["attribute_owner"]}
    attribute_values = {str(a): str(b) for a, b in A["R"]["attribute_value"]}
    arguments: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for occurrence, position, arg in A["R"]["argument"]:
        if position not in positions or arg not in objects:
            raise W3Error("argument references unknown position/object")
        arguments[str(occurrence)].append((positions[position], str(arg)))

    axes: dict[str, Any] = {}
    for axis in AXES:
        relations = []
        attributes = []
        for occurrence, occurrence_axis in in_axis.items():
            if occurrence_axis != axis:
                continue
            kind = objects[occurrence]["kind"]
            if kind == "relation_occurrence":
                if occurrence not in relation_roles:
                    raise W3Error("relation occurrence lacks role")
                ordered = sorted(arguments.get(occurrence, []))
                if [x for x, _ in ordered] != list(range(1, len(ordered) + 1)) or not ordered:
                    raise W3Error("relation occurrence has invalid ordered arguments")
                relations.append({"id": occurrence, "role": relation_roles[occurrence], "args": [x for _, x in ordered]})
            elif kind == "attribute_occurrence":
                if occurrence not in attribute_roles or occurrence not in attribute_owners or occurrence not in attribute_values:
                    raise W3Error("attribute occurrence incomplete")
                attributes.append({"id": occurrence, "owner": attribute_owners[occurrence], "role": attribute_roles[occurrence], "value": attribute_values[occurrence]})
            else:
                raise W3Error("unexpected occurrence kind in direct axis")
        axes[axis] = {
            "members": sorted(axis_members[axis]),
            "relations": _sort_records(relations),
            "attributes": _sort_records(attributes),
        }

    recovered = {
        "schema": RECOVERED_SCHEMA,
        "carriers": _sort_records([{"id": object_id, "sort": sort_id} for object_id, sort_id in sorts.items() if objects[object_id]["kind"] not in {"relation_occurrence", "attribute_occurrence", "cross_relation_occurrence", "component", "interface"}]),
        "axes": axes,
        "dynamics": {
            "rules": copy.deepcopy(A.get("C", {}).get("rules", [])),
            "rule_versions": copy.deepcopy(A.get("C", {}).get("rule_versions", [])),
            "states": copy.deepcopy(A.get("Sigma", [])),
            "transitions": copy.deepcopy(A.get("Theta", [])),
            "history": copy.deepcopy(A.get("H", {})),
            "transition_statuses": copy.deepcopy(A.get("Omega", {}).get("transition_statuses", [])),
        },
        "semantics": {
            "interpretations": copy.deepcopy(A.get("I", [])),
            "value_literals": _sort_records([{"object": object_id, "literal": value} for object_id, value in literals.items()]),
            "equivalences": copy.deepcopy(A.get("R", {}).get("source_equivalent", [])),
        },
        "decomposition": copy.deepcopy(A.get("Res", {})),
        "provenance": copy.deepcopy(A.get("Prov", [])),
    }
    for key in ("rules", "rule_versions", "states", "transitions", "transition_statuses"):
        recovered["dynamics"][key] = _sort_records(recovered["dynamics"][key])
    for key in recovered["dynamics"]["history"]:
        recovered["dynamics"]["history"][key] = _sort_records(recovered["dynamics"]["history"][key])
    for key in recovered["decomposition"]:
        recovered["decomposition"][key] = _sort_records(recovered["decomposition"][key])
    recovered["semantics"]["interpretations"] = _sort_records(recovered["semantics"]["interpretations"])
    recovered["semantics"]["equivalences"] = _sort_records(recovered["semantics"]["equivalences"])
    recovered["provenance"] = _sort_records(recovered["provenance"])
    return recovered
