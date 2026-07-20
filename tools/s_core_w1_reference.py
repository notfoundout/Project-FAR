#!/usr/bin/env python3
"""Finite executable reference for the S_core W1 direct-axis constructor.

This module corroborates SCORE-W1-PROOF-001 on finite fixtures.  It is not a
proof assistant and does not establish the full Faithful_split witness.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable

DIRECT_AXES = ("P1", "P2", "P3", "P4", "P6", "P8I")
FIXED_RELATIONS = (
    "represented_by",
    "denotes",
    "has_sort",
    "in_axis",
    "occurrence_role",
    "argument",
    "attribute_owner",
    "attribute_role",
    "attribute_value",
    "has_provenance",
    "has_evidence_status",
    "has_source_denotation",
    "source_equivalent",
)


class W1Error(ValueError):
    """Raised for malformed finite W1 fixtures or target packages."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def token(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:20]
    return f"{prefix}:{digest}"


def _relation_key(item: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    return str(item["role"]), tuple(str(x) for x in item.get("args", []))


def _attribute_key(item: dict[str, Any]) -> tuple[str, str, str]:
    return str(item["owner"]), str(item["role"]), canonical_json(item.get("value"))


def validate_source(source: dict[str, Any]) -> None:
    axes = source.get("axes")
    if not isinstance(axes, dict):
        raise W1Error("source.axes must be an object")
    unexpected = set(axes) - set(DIRECT_AXES)
    if unexpected:
        raise W1Error(f"unsupported direct axes: {sorted(unexpected)}")

    global_sorts: dict[str, str] = {}
    for axis, reduct in axes.items():
        if not isinstance(reduct, dict):
            raise W1Error(f"{axis} reduct must be an object")
        elements = reduct.get("elements", [])
        relations = reduct.get("relations", [])
        attributes = reduct.get("attributes", [])
        if not all(isinstance(x, list) for x in (elements, relations, attributes)):
            raise W1Error(f"{axis} elements/relations/attributes must be lists")
        local_ids: set[str] = set()
        for element in elements:
            element_id = str(element.get("id", ""))
            sort = str(element.get("sort", ""))
            if not element_id or not sort:
                raise W1Error(f"{axis} element requires id and sort")
            if element_id in local_ids:
                raise W1Error(f"duplicate {axis} element: {element_id}")
            local_ids.add(element_id)
            previous = global_sorts.setdefault(element_id, sort)
            if previous != sort:
                raise W1Error(f"shared element {element_id} changes sort: {previous} -> {sort}")
        for relation in relations:
            role = str(relation.get("role", ""))
            args = [str(x) for x in relation.get("args", [])]
            if not role or not args:
                raise W1Error(f"{axis} relation requires role and nonempty args")
            missing = set(args) - local_ids
            if missing:
                raise W1Error(f"{axis} relation {role} references undeclared elements: {sorted(missing)}")
        for attribute in attributes:
            owner = str(attribute.get("owner", ""))
            role = str(attribute.get("role", ""))
            if not owner or not role or "value" not in attribute:
                raise W1Error(f"{axis} attribute requires owner, role, and value")
            if owner not in local_ids:
                raise W1Error(f"{axis} attribute {role} references undeclared owner: {owner}")


@dataclass
class TargetBuilder:
    target: dict[str, Any]

    @classmethod
    def new(cls) -> "TargetBuilder":
        return cls(
            {
                "schema": "DIR-INCIDENCE-1.0",
                "U": [],
                "Pi": [],
                "R": {name: [] for name in FIXED_RELATIONS},
                "Rep": [],
                "S": {"representations": [], "relations": []},
                "I": [],
                "Inv": {"id": "inv:S_core:W1", "scope": "finite_direct_axes"},
                "C": {"status": "typed_empty_at_W1"},
                "Sigma": {"status": "typed_empty_at_W1"},
                "Theta": {"status": "typed_empty_at_W1"},
                "H": {"status": "typed_empty_at_W1"},
                "Omega": {"status": "typed_empty_at_W1"},
                "Res": {"status": "typed_empty_at_W1"},
                "Prov": [],
                "kappa_W1": {
                    "schema": "DIR-INCIDENCE-1.0",
                    "constructor": "tools/s_core_w1_reference.py",
                    "derived_relation": "occurrence_role + ordered argument positions",
                    "derived_attribute": "attribute_owner + attribute_role + attribute_value",
                    "source_specific_content_is_data": True,
                    "case_database": False,
                    "external_interpreter": False,
                },
            }
        )

    def add_object(self, object_id: str, kind: str, payload: Any | None = None) -> str:
        if any(item["id"] == object_id for item in self.target["U"]):
            return object_id
        rep_id = f"rep:{object_id}"
        self.target["U"].append({"id": object_id, "kind": kind, "payload": payload})
        self.target["Rep"].append({"id": rep_id, "kind": "representation", "represents": object_id})
        self.target["S"]["representations"].append(rep_id)
        self.target["R"]["represented_by"].append([object_id, rep_id])
        self.target["R"]["denotes"].append([rep_id, object_id])
        return object_id

    def add_relation(self, name: str, *args: str) -> None:
        if name not in self.target["R"]:
            raise W1Error(f"unknown fixed target relation: {name}")
        fact = list(args)
        if fact not in self.target["R"][name]:
            self.target["R"][name].append(fact)


def construct_target(source: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_source(source)
    builder = TargetBuilder.new()
    correspondence: dict[str, Any] = {axis: {"phi": {}, "psi": {}, "rho": {}} for axis in DIRECT_AXES}

    axis_objects: dict[str, str] = {}
    sort_objects: dict[str, str] = {}
    role_objects: dict[tuple[str, str], str] = {}
    value_objects: dict[str, str] = {}

    def axis_object(axis: str) -> str:
        if axis not in axis_objects:
            object_id = f"axis:{axis}"
            builder.add_object(object_id, "axis_code", axis)
            axis_objects[axis] = object_id
        return axis_objects[axis]

    def sort_object(sort: str) -> str:
        if sort not in sort_objects:
            object_id = token("sort", sort)
            builder.add_object(object_id, "sort_code", sort)
            sort_objects[sort] = object_id
        return sort_objects[sort]

    def role_object(kind: str, role: str) -> str:
        key = (kind, role)
        if key not in role_objects:
            object_id = token(f"role:{kind}", role)
            builder.add_object(object_id, "role_code", {"kind": kind, "role": role})
            role_objects[key] = object_id
        return role_objects[key]

    def value_object(value: Any) -> str:
        key = canonical_json(value)
        if key not in value_objects:
            object_id = token("value", value)
            builder.add_object(object_id, "encoded_value", copy.deepcopy(value))
            value_objects[key] = object_id
        return value_objects[key]

    element_objects: dict[str, str] = {}
    for axis in DIRECT_AXES:
        reduct = source.get("axes", {}).get(axis, {"elements": [], "relations": [], "attributes": []})
        axis_id = axis_object(axis)
        for element in sorted(reduct.get("elements", []), key=lambda x: str(x["id"])):
            source_id = str(element["id"])
            sort = str(element["sort"])
            object_id = element_objects.get(source_id)
            if object_id is None:
                object_id = token("element", {"id": source_id, "sort": sort})
                builder.add_object(object_id, "encoded_element", {"source_key": source_id})
                element_objects[source_id] = object_id
                builder.add_relation("has_sort", object_id, sort_object(sort))
                denotation = element.get("denotation", {"source_key": source_id})
                den_id = value_object({"denotation": denotation})
                builder.add_relation("has_source_denotation", object_id, den_id)
                builder.target["I"].append({"representation": f"rep:{object_id}", "denotation": denotation})
            builder.add_relation("in_axis", object_id, axis_id)
            correspondence[axis]["phi"][source_id] = object_id

        for index, relation in enumerate(sorted(reduct.get("relations", []), key=_relation_key)):
            role = str(relation["role"])
            args = [str(x) for x in relation["args"]]
            role_id = role_object("relation", role)
            occurrence_id = token("relation_occurrence", {"axis": axis, "index": index, "role": role, "args": args})
            builder.add_object(occurrence_id, "relation_occurrence", {"axis": axis})
            builder.add_relation("in_axis", occurrence_id, axis_id)
            builder.add_relation("occurrence_role", occurrence_id, role_id)
            for position, source_id in enumerate(args, start=1):
                pos_id = token("position", position)
                builder.add_object(pos_id, "position_code", position)
                builder.add_relation("argument", occurrence_id, pos_id, element_objects[source_id])
            correspondence[axis]["rho"][role] = {
                "schema": "DR",
                "role_object": role_id,
                "arity": len(args),
            }

        for index, attribute in enumerate(sorted(reduct.get("attributes", []), key=_attribute_key)):
            owner = str(attribute["owner"])
            role = str(attribute["role"])
            value = copy.deepcopy(attribute["value"])
            role_id = role_object("attribute", role)
            value_id = value_object(value)
            occurrence_id = token(
                "attribute_occurrence",
                {"axis": axis, "index": index, "owner": owner, "role": role, "value": value},
            )
            kind = "evidence_status_record" if axis == "P8I" and "evidence" in role else "attribute_occurrence"
            builder.add_object(occurrence_id, kind, {"axis": axis})
            builder.add_relation("in_axis", occurrence_id, axis_id)
            builder.add_relation("attribute_owner", occurrence_id, element_objects[owner])
            builder.add_relation("attribute_role", occurrence_id, role_id)
            builder.add_relation("attribute_value", occurrence_id, value_id)
            correspondence[axis]["psi"][canonical_json(value)] = value_id
            correspondence[axis]["rho"].setdefault(
                role,
                {"schema": "DA", "role_object": role_id, "arity": 1},
            )
            if axis == "P8I":
                builder.add_relation("has_evidence_status", element_objects[owner], occurrence_id)
                builder.target["Prov"].append(
                    {"owner": element_objects[owner], "role": role_id, "value": value_id}
                )
            if "provenance" in role:
                builder.add_relation("has_provenance", element_objects[owner], occurrence_id)
                builder.target["Prov"].append(
                    {"owner": element_objects[owner], "role": role_id, "value": value_id}
                )

    for relation_name in builder.target["R"]:
        builder.target["R"][relation_name].sort(key=canonical_json)
    builder.target["U"].sort(key=lambda x: x["id"])
    builder.target["Rep"].sort(key=lambda x: x["id"])
    builder.target["S"]["representations"].sort()
    builder.target["I"].sort(key=canonical_json)
    builder.target["Prov"].sort(key=canonical_json)
    return builder.target, correspondence


def _position_payload(target: dict[str, Any]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in target["U"]:
        if item["kind"] == "position_code":
            result[item["id"]] = int(item["payload"])
    return result


def derived_relation(target: dict[str, Any], role_object: str, arity: int, axis: str) -> set[tuple[str, ...]]:
    axis_id = f"axis:{axis}"
    in_axis = {tuple(x) for x in target["R"]["in_axis"]}
    role_facts = {tuple(x) for x in target["R"]["occurrence_role"]}
    arguments: dict[str, list[tuple[int, str]]] = {}
    positions = _position_payload(target)
    for occurrence, position, value in target["R"]["argument"]:
        arguments.setdefault(occurrence, []).append((positions[position], value))
    result: set[tuple[str, ...]] = set()
    for occurrence, role in role_facts:
        if role != role_object or (occurrence, axis_id) not in in_axis:
            continue
        ordered = sorted(arguments.get(occurrence, []))
        if len(ordered) == arity and [p for p, _ in ordered] == list(range(1, arity + 1)):
            result.add(tuple(value for _, value in ordered))
    return result


def derived_attribute(target: dict[str, Any], role_object: str, axis: str) -> set[tuple[str, str]]:
    axis_id = f"axis:{axis}"
    in_axis = {tuple(x) for x in target["R"]["in_axis"]}
    roles = {occ: role for occ, role in target["R"]["attribute_role"]}
    owners = {occ: owner for occ, owner in target["R"]["attribute_owner"]}
    values = {occ: value for occ, value in target["R"]["attribute_value"]}
    result: set[tuple[str, str]] = set()
    for occurrence, role in roles.items():
        if role == role_object and (occurrence, axis_id) in in_axis:
            if occurrence in owners and occurrence in values:
                result.add((owners[occurrence], values[occurrence]))
    return result


def verify_axis(source: dict[str, Any], target: dict[str, Any], correspondence: dict[str, Any], axis: str) -> bool:
    try:
        validate_source(source)
        reduct = source.get("axes", {}).get(axis, {"elements": [], "relations": [], "attributes": []})
        corr = correspondence[axis]
        elements = {str(x["id"]): str(x["sort"]) for x in reduct.get("elements", [])}
        phi = corr["phi"]
        if set(phi) != set(elements) or len(set(phi.values())) != len(phi):
            return False
        target_objects = {item["id"]: item for item in target["U"]}
        if any(value not in target_objects for value in phi.values()):
            return False
        sort_payload = {item["id"]: item["payload"] for item in target["U"] if item["kind"] == "sort_code"}
        sort_facts = {tuple(x) for x in target["R"]["has_sort"]}
        for source_id, sort in elements.items():
            if not any(obj == phi[source_id] and sort_payload.get(sort_id) == sort for obj, sort_id in sort_facts):
                return False

        roles = corr["rho"]
        expected_relations: dict[str, set[tuple[str, ...]]] = {}
        for relation in reduct.get("relations", []):
            role = str(relation["role"])
            expected_relations.setdefault(role, set()).add(tuple(phi[str(x)] for x in relation["args"]))
        for role, expected in expected_relations.items():
            descriptor = roles.get(role)
            if not descriptor or descriptor.get("schema") != "DR":
                return False
            actual = derived_relation(target, descriptor["role_object"], int(descriptor["arity"]), axis)
            if actual != expected:
                return False

        expected_attributes: dict[str, set[tuple[str, str]]] = {}
        for attribute in reduct.get("attributes", []):
            role = str(attribute["role"])
            value_key = canonical_json(attribute["value"])
            value_id = corr["psi"].get(value_key)
            if value_id is None:
                return False
            expected_attributes.setdefault(role, set()).add((phi[str(attribute["owner"])], value_id))
        for role, expected in expected_attributes.items():
            descriptor = roles.get(role)
            if not descriptor or descriptor.get("schema") != "DA":
                return False
            actual = derived_attribute(target, descriptor["role_object"], axis)
            if actual != expected:
                return False

        # Reflection also requires no target role represented in this axis to be omitted from the source comparison.
        expected_role_objects = {
            descriptor["role_object"]
            for descriptor in roles.values()
            if isinstance(descriptor, dict) and "role_object" in descriptor
        }
        axis_id = f"axis:{axis}"
        in_axis = {tuple(x) for x in target["R"]["in_axis"]}
        for occurrence, role_object in target["R"]["occurrence_role"]:
            if (occurrence, axis_id) in in_axis and role_object not in expected_role_objects:
                return False
        for occurrence, role_object in target["R"]["attribute_role"]:
            if (occurrence, axis_id) in in_axis and role_object not in expected_role_objects:
                return False
        return True
    except (KeyError, TypeError, ValueError, W1Error):
        return False


def verify_all(source: dict[str, Any], target: dict[str, Any], correspondence: dict[str, Any]) -> bool:
    return all(verify_axis(source, target, correspondence, axis) for axis in DIRECT_AXES)


def structural_digest(target: dict[str, Any]) -> str:
    """Return a display-label-independent digest of the W1 target structure."""
    structural = {
        "schema": target["schema"],
        "U": [{"id": x["id"], "kind": x["kind"], "payload": x["payload"]} for x in target["U"]],
        "R": target["R"],
        "Rep": target["Rep"],
        "kappa_W1": target["kappa_W1"],
    }
    return hashlib.sha256(canonical_json(structural).encode("utf-8")).hexdigest()


def deep_copy(value: Any) -> Any:
    return copy.deepcopy(value)


__all__ = [
    "DIRECT_AXES",
    "W1Error",
    "canonical_json",
    "construct_target",
    "deep_copy",
    "derived_attribute",
    "derived_relation",
    "structural_digest",
    "validate_source",
    "verify_all",
    "verify_axis",
]
