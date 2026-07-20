#!/usr/bin/env python3
"""Finite executable reference for SCORE-W1-PROOF-001.

The code checks the fixed direct-axis incidence construction on finite fixtures.
It is bounded corroboration, not a proof assistant or a full Faithful_split witness.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from typing import Any

DIRECT_AXES = ("P1", "P2", "P3", "P4", "P6", "P8I")
FIXED_RELATIONS = (
    "represented_by", "denotes", "has_sort", "in_axis", "occurrence_role",
    "argument", "attribute_owner", "attribute_role", "attribute_value",
    "has_provenance", "has_evidence_status", "has_source_denotation",
    "source_equivalent",
)


class W1Error(ValueError):
    """Malformed finite W1 source or target."""


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
            old = global_sorts.setdefault(element_id, sort)
            if old != sort:
                raise W1Error(f"shared element {element_id} changes sort: {old} -> {sort}")
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
        return cls({
            "schema": "DIR-INCIDENCE-1.0",
            "U": [], "Pi": [], "R": {name: [] for name in FIXED_RELATIONS},
            "Rep": [], "S": {"representations": [], "relations": []}, "I": [],
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
        })

    def add_object(self, object_id: str, kind: str, payload: Any | None = None) -> str:
        if any(item["id"] == object_id for item in self.target["U"]):
            return object_id
        rep_id = f"rep:{object_id}"
        self.target["U"].append({"id": object_id, "kind": kind, "payload": payload})
        self.target["Pi"].append({"object": object_id, "property": "kind", "value": kind})
        self.target["Rep"].append({"id": rep_id, "kind": "representation", "represents": object_id})
        self.target["S"]["representations"].append(rep_id)
        self.target["S"]["relations"].append(["represents", rep_id, object_id])
        self.add_relation("represented_by", object_id, rep_id)
        self.add_relation("denotes", rep_id, object_id)
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
    correspondence = {
        axis: {"phi": {}, "psi": {}, "rho": {}, "alpha": {}}
        for axis in DIRECT_AXES
    }
    axis_objects: dict[str, str] = {}
    sort_objects: dict[str, str] = {}
    role_objects: dict[tuple[str, str], str] = {}
    value_objects: dict[str, str] = {}
    element_objects: dict[str, str] = {}

    def axis_object(axis: str) -> str:
        if axis not in axis_objects:
            axis_objects[axis] = builder.add_object(f"axis:{axis}", "axis_code", axis)
        return axis_objects[axis]

    def sort_object(sort: str) -> str:
        if sort not in sort_objects:
            sort_objects[sort] = builder.add_object(token("sort", sort), "sort_code", sort)
        return sort_objects[sort]

    def role_object(kind: str, role: str) -> str:
        key = (kind, role)
        if key not in role_objects:
            role_objects[key] = builder.add_object(
                token(f"role:{kind}", role), "role_code", {"kind": kind, "role": role}
            )
        return role_objects[key]

    def value_object(value: Any) -> str:
        key = canonical_json(value)
        if key not in value_objects:
            value_objects[key] = builder.add_object(token("value", value), "encoded_value", copy.deepcopy(value))
        return value_objects[key]

    for equivalence in source.get("value_equivalences", []):
        left = value_object(equivalence["left"])
        right = value_object(equivalence["right"])
        rule = value_object({"equivalence": equivalence.get("rule", "exact")})
        builder.add_relation("source_equivalent", left, right, rule)

    for axis in DIRECT_AXES:
        reduct = source.get("axes", {}).get(axis, {"elements": [], "relations": [], "attributes": []})
        axis_id = axis_object(axis)
        for element in sorted(reduct.get("elements", []), key=lambda x: str(x["id"])):
            source_id, sort = str(element["id"]), str(element["sort"])
            if source_id not in element_objects:
                object_id = builder.add_object(
                    token("element", {"id": source_id, "sort": sort}),
                    "encoded_element", {"source_key": source_id},
                )
                element_objects[source_id] = object_id
                builder.add_relation("has_sort", object_id, sort_object(sort))
                denotation = element.get("denotation", {"source_key": source_id})
                den_id = value_object({"denotation": denotation})
                builder.add_relation("has_source_denotation", object_id, den_id)
                builder.target["I"].append({"representation": f"rep:{object_id}", "denotation": denotation})
            object_id = element_objects[source_id]
            builder.add_relation("in_axis", object_id, axis_id)
            correspondence[axis]["phi"][source_id] = object_id

        for index, relation in enumerate(sorted(reduct.get("relations", []), key=_relation_key)):
            role = str(relation["role"])
            args = [str(x) for x in relation["args"]]
            role_id = role_object("relation", role)
            occurrence_id = builder.add_object(
                token("relation_occurrence", {"axis": axis, "index": index, "role": role, "args": args}),
                "relation_occurrence", {"axis": axis},
            )
            builder.add_relation("in_axis", occurrence_id, axis_id)
            builder.add_relation("occurrence_role", occurrence_id, role_id)
            for position, source_id in enumerate(args, start=1):
                pos_id = builder.add_object(token("position", position), "position_code", position)
                builder.add_relation("argument", occurrence_id, pos_id, element_objects[source_id])
            correspondence[axis]["rho"][role] = {"schema": "DR", "role_object": role_id, "arity": len(args)}

        for index, attribute in enumerate(sorted(reduct.get("attributes", []), key=_attribute_key)):
            owner, role = str(attribute["owner"]), str(attribute["role"])
            value = copy.deepcopy(attribute["value"])
            role_id, value_id = role_object("attribute", role), value_object(value)
            occurrence_id = builder.add_object(
                token("attribute_occurrence", {"axis": axis, "index": index, "owner": owner, "role": role, "value": value}),
                "evidence_status_record" if axis == "P8I" and "evidence" in role else "attribute_occurrence",
                {"axis": axis},
            )
            builder.add_relation("in_axis", occurrence_id, axis_id)
            builder.add_relation("attribute_owner", occurrence_id, element_objects[owner])
            builder.add_relation("attribute_role", occurrence_id, role_id)
            builder.add_relation("attribute_value", occurrence_id, value_id)
            correspondence[axis]["psi"][canonical_json(value)] = value_id
            correspondence[axis]["alpha"][role] = {"schema": "DA", "role_object": role_id, "arity": 1}
            if axis == "P8I":
                builder.add_relation("has_evidence_status", element_objects[owner], occurrence_id)
                builder.target["Prov"].append({"owner": element_objects[owner], "role": role_id, "value": value_id})
            if "provenance" in role:
                builder.add_relation("has_provenance", element_objects[owner], occurrence_id)
                builder.target["Prov"].append({"owner": element_objects[owner], "role": role_id, "value": value_id})

    for name in builder.target["R"]:
        builder.target["R"][name].sort(key=canonical_json)
    for key in ("U", "Pi", "Rep", "I", "Prov"):
        builder.target[key].sort(key=canonical_json)
    builder.target["S"]["representations"].sort()
    builder.target["S"]["relations"].sort(key=canonical_json)
    return builder.target, correspondence


def _position_payload(target: dict[str, Any]) -> dict[str, int]:
    return {item["id"]: int(item["payload"]) for item in target["U"] if item["kind"] == "position_code"}


def derived_relation(target: dict[str, Any], role_object: str, arity: int, axis: str) -> set[tuple[str, ...]]:
    axis_id = f"axis:{axis}"
    in_axis = {tuple(x) for x in target["R"]["in_axis"]}
    roles = {tuple(x) for x in target["R"]["occurrence_role"]}
    positions = _position_payload(target)
    arguments: dict[str, list[tuple[int, str]]] = {}
    for occurrence, position, value in target["R"]["argument"]:
        if position not in positions:
            raise W1Error(f"unknown argument position: {position}")
        arguments.setdefault(occurrence, []).append((positions[position], value))
    result: set[tuple[str, ...]] = set()
    for occurrence, role in roles:
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
    return {
        (owners[occurrence], values[occurrence])
        for occurrence, role in roles.items()
        if role == role_object and (occurrence, axis_id) in in_axis
        and occurrence in owners and occurrence in values
    }


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

        expected_relations: dict[str, set[tuple[str, ...]]] = {}
        for relation in reduct.get("relations", []):
            role = str(relation["role"])
            expected_relations.setdefault(role, set()).add(tuple(phi[str(x)] for x in relation["args"]))
        if set(expected_relations) != set(corr["rho"]):
            return False
        for role, expected in expected_relations.items():
            descriptor = corr["rho"].get(role)
            if not descriptor or descriptor.get("schema") != "DR":
                return False
            if derived_relation(target, descriptor["role_object"], int(descriptor["arity"]), axis) != expected:
                return False

        expected_attributes: dict[str, set[tuple[str, str]]] = {}
        for attribute in reduct.get("attributes", []):
            role = str(attribute["role"])
            value_id = corr["psi"].get(canonical_json(attribute["value"]))
            if value_id is None:
                return False
            expected_attributes.setdefault(role, set()).add((phi[str(attribute["owner"])], value_id))
        if set(expected_attributes) != set(corr["alpha"]):
            return False
        for role, expected in expected_attributes.items():
            descriptor = corr["alpha"].get(role)
            if not descriptor or descriptor.get("schema") != "DA":
                return False
            if derived_attribute(target, descriptor["role_object"], axis) != expected:
                return False

        expected_role_objects = {
            descriptor["role_object"]
            for family in (corr["rho"], corr["alpha"])
            for descriptor in family.values()
        }
        axis_id = f"axis:{axis}"
        in_axis = {tuple(x) for x in target["R"]["in_axis"]}
        for relation_name in ("occurrence_role", "attribute_role"):
            for occurrence, role_object in target["R"][relation_name]:
                if (occurrence, axis_id) in in_axis and role_object not in expected_role_objects:
                    return False
        return True
    except (KeyError, TypeError, ValueError, W1Error):
        return False


def verify_all(source: dict[str, Any], target: dict[str, Any], correspondence: dict[str, Any]) -> bool:
    return all(verify_axis(source, target, correspondence, axis) for axis in DIRECT_AXES)


def structural_digest(target: dict[str, Any]) -> str:
    structural = {
        "schema": target["schema"], "U": target["U"], "Pi": target["Pi"],
        "R": target["R"], "Rep": target["Rep"], "S": target["S"],
        "kappa_W1": target["kappa_W1"],
    }
    return hashlib.sha256(canonical_json(structural).encode("utf-8")).hexdigest()


def deep_copy(value: Any) -> Any:
    return copy.deepcopy(value)


__all__ = [
    "DIRECT_AXES", "W1Error", "canonical_json", "construct_target", "deep_copy",
    "derived_attribute", "derived_relation", "structural_digest", "validate_source",
    "verify_all", "verify_axis",
]
