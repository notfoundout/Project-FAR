from __future__ import annotations

import copy
from typing import Any

from s_core_w3_schema import canonical_json
from w3_5_factor_source import FactorizationError, _record_id

GREL_SCHEMA = "GREL-INSTANCE-1.0"

def _value_id(value: Any) -> str:
    return _record_id("value", value)

def encode_grel(value: Any) -> dict[str, Any]:
    entities: list[dict[str, Any]] = []
    exact_values: dict[str, dict[str, Any]] = {}
    attributes: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []

    def visit(item: Any, path: tuple[Any, ...]) -> str:
        node_id = _record_id("node", list(path))
        sort = "object" if isinstance(item, dict) else "array" if isinstance(item, list) else "scalar"
        entities.append({"id": node_id, "sort": sort})
        if sort == "scalar":
            value_id = _value_id(item)
            exact_values[value_id] = {"id": value_id, "value": copy.deepcopy(item)}
            attributes.append({"id": _record_id("attribute", [list(path), "literal"]), "owner": node_id, "role": "literal", "value": value_id})
        elif sort == "object":
            for key in sorted(item):
                child_id = visit(item[key], path + (key,))
                relations.append({"id": _record_id("relation", [list(path), "field", key]), "role": "field", "args": [node_id, key, child_id]})
        else:
            for index, child in enumerate(item):
                child_id = visit(child, path + (index,))
                relations.append({"id": _record_id("relation", [list(path), "item", index]), "role": "item", "args": [node_id, index, child_id]})
        return node_id

    root_id = visit(copy.deepcopy(value), ("$",))
    package = {
        "schema": GREL_SCHEMA,
        "sorts": ["array", "object", "scalar"],
        "entities": sorted(entities, key=lambda item: item["id"]),
        "exact_values": sorted(exact_values.values(), key=lambda item: item["id"]),
        "typed_attributes": sorted(attributes, key=canonical_json),
        "typed_nary_relation_occurrences": sorted(relations, key=canonical_json),
        "schema_descriptor": {
            "root_entity": root_id,
            "relation_roles": {"field": ["parent_entity", "field_name", "child_entity"], "item": ["parent_entity", "index", "child_entity"]},
            "attribute_roles": {"literal": ["owner_entity", "exact_value"]},
        },
        "canonical_encoder": {"algorithm": "encode_grel", "fixed_schema": True, "case_identifier_branching": False, "case_database": False, "source_isomorphism_equivariant": True},
        "target_only_decoder": {"algorithm": "decode_grel", "target_only": True, "deterministic": True, "terminates_on_finite_target": True},
        "machinery_ledger": {
            "schema": "GREL-MACHINERY-1.0",
            "algorithms": ["validate_grel", "encode_grel", "decode_grel"],
            "external_dependencies": [],
            "forbidden": {"source_oracle": False, "case_database": False, "hidden_interpreter": False, "network": False, "evaluator_repair": False},
        },
    }
    validate_grel(package)
    return package

def validate_grel(package: dict[str, Any]) -> None:
    if package.get("schema") != GREL_SCHEMA or package.get("sorts") != ["array", "object", "scalar"]:
        raise FactorizationError("GREL schema or sorts changed")
    entities = package.get("entities")
    values = package.get("exact_values")
    attributes = package.get("typed_attributes")
    relations = package.get("typed_nary_relation_occurrences")
    if not all(isinstance(item, list) for item in (entities, values, attributes, relations)):
        raise FactorizationError("GREL carriers must be lists")
    entity_map = {str(item.get("id", "")): item for item in entities}
    value_map = {str(item.get("id", "")): item for item in values}
    if "" in entity_map or len(entity_map) != len(entities):
        raise FactorizationError("GREL entities require unique ids")
    if "" in value_map or len(value_map) != len(values):
        raise FactorizationError("GREL exact values require unique ids")
    if package.get("schema_descriptor", {}).get("root_entity") not in entity_map:
        raise FactorizationError("GREL root entity is missing")
    literal_owner: set[str] = set()
    for item in attributes:
        owner, value = str(item.get("owner", "")), str(item.get("value", ""))
        if item.get("role") != "literal" or owner not in entity_map or value not in value_map or owner in literal_owner:
            raise FactorizationError("malformed or duplicate GREL literal")
        literal_owner.add(owner)
    relation_ids: set[str] = set()
    for item in relations:
        relation_id, role, args = str(item.get("id", "")), item.get("role"), item.get("args")
        if not relation_id or relation_id in relation_ids or role not in {"field", "item"}:
            raise FactorizationError("malformed GREL relation")
        relation_ids.add(relation_id)
        if not isinstance(args, list) or len(args) != 3 or str(args[0]) not in entity_map or str(args[2]) not in entity_map:
            raise FactorizationError("GREL relation arity or entity reference changed")
        if role == "field" and not isinstance(args[1], str):
            raise FactorizationError("GREL field name must be a string")
        if role == "item" and not isinstance(args[1], int):
            raise FactorizationError("GREL item index must be an integer")
    for entity_id, entity in entity_map.items():
        sort = entity.get("sort")
        if sort not in {"object", "array", "scalar"}:
            raise FactorizationError("unknown GREL entity sort")
        if sort == "scalar" and entity_id not in literal_owner:
            raise FactorizationError("scalar GREL entity lacks literal")
        if sort != "scalar" and entity_id in literal_owner:
            raise FactorizationError("non-scalar GREL entity has literal")
    if package.get("canonical_encoder") != {"algorithm": "encode_grel", "fixed_schema": True, "case_identifier_branching": False, "case_database": False, "source_isomorphism_equivariant": True}:
        raise FactorizationError("GREL encoder descriptor changed")
    if package.get("target_only_decoder") != {"algorithm": "decode_grel", "target_only": True, "deterministic": True, "terminates_on_finite_target": True}:
        raise FactorizationError("GREL decoder descriptor changed")
    ledger = package.get("machinery_ledger", {})
    if ledger.get("external_dependencies") != []:
        raise FactorizationError("GREL external dependencies are prohibited")
    forbidden = ledger.get("forbidden", {})
    if any(forbidden.get(key) is not False for key in ("source_oracle", "case_database", "hidden_interpreter", "network", "evaluator_repair")):
        raise FactorizationError("GREL forbidden machinery flag changed")

def decode_grel(package: dict[str, Any]) -> Any:
    validate_grel(package)
    entity_map = {item["id"]: item for item in package["entities"]}
    value_map = {item["id"]: copy.deepcopy(item["value"]) for item in package["exact_values"]}
    literals = {item["owner"]: value_map[item["value"]] for item in package["typed_attributes"]}
    outgoing: dict[str, list[dict[str, Any]]] = {}
    for relation in package["typed_nary_relation_occurrences"]:
        outgoing.setdefault(str(relation["args"][0]), []).append(relation)
    active: set[str] = set()

    def build(entity_id: str) -> Any:
        if entity_id in active:
            raise FactorizationError("GREL target contains a cycle")
        active.add(entity_id)
        try:
            sort = entity_map[entity_id]["sort"]
            if sort == "scalar":
                return copy.deepcopy(literals[entity_id])
            records = outgoing.get(entity_id, [])
            if sort == "object":
                result: dict[str, Any] = {}
                for relation in sorted(records, key=lambda item: str(item["args"][1])):
                    if relation["role"] != "field":
                        raise FactorizationError("object has non-field relation")
                    key = str(relation["args"][1])
                    if key in result:
                        raise FactorizationError("duplicate GREL object field")
                    result[key] = build(str(relation["args"][2]))
                return result
            indexed: dict[int, Any] = {}
            for relation in records:
                if relation["role"] != "item":
                    raise FactorizationError("array has non-item relation")
                index = int(relation["args"][1])
                if index in indexed:
                    raise FactorizationError("duplicate GREL array index")
                indexed[index] = build(str(relation["args"][2]))
            if sorted(indexed) != list(range(len(indexed))):
                raise FactorizationError("GREL array indices are not contiguous")
            return [indexed[index] for index in range(len(indexed))]
        finally:
            active.remove(entity_id)

    return build(str(package["schema_descriptor"]["root_entity"]))

def grel_metrics(package: dict[str, Any]) -> dict[str, int]:
    return {
        "schema_components": 10,
        "entities": len(package["entities"]),
        "exact_values": len(package["exact_values"]),
        "attributes": len(package["typed_attributes"]),
        "relation_occurrences": len(package["typed_nary_relation_occurrences"]),
        "serialized_bytes": len(canonical_json(package).encode("utf-8")),
        "semantic_axis_access_operations": len(package["typed_attributes"]) + len(package["typed_nary_relation_occurrences"]),
    }
