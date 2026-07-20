from __future__ import annotations
import copy
from typing import Any
from s_core_w3_schema import AXES, FIXED_RELATIONS, SCHEMA, W3Error, canonical_json, token

def _sort_records(records: list[Any]) -> list[Any]:
    return sorted(records, key=canonical_json)


class Builder:
    def __init__(self) -> None:
        self.A: dict[str, Any] = {
            "schema": SCHEMA,
            "U": [], "Pi": [], "R": {name: [] for name in FIXED_RELATIONS},
            "Rep": [], "S": {"representations": [], "relations": []}, "I": [],
            "Inv": {"id": "inv:S_core:W3", "scope": "finite_global_witness"},
            "C": {"rules": [], "rule_versions": [], "active_rule_versions": []},
            "Sigma": [], "Theta": [],
            "H": {"events": [], "order": [], "causal": [], "provenance": [], "revisions": [], "modifications": [], "dependency_ancestry": [], "path_conditions": []},
            "Omega": {"transition_statuses": []},
            "Res": {"components": [], "interfaces": [], "component_members": [], "interface_members": [], "interface_links": [], "cross_component_relations": []},
            "Prov": [],
        }
        self.E: dict[str, str] = {}
        self.M: dict[str, Any] = {"sorts": {}, "roles": {}, "values": {}, "axes": {axis: f"axis:{axis}" for axis in AXES}}
        self._values: dict[str, str] = {}
        self._sorts: dict[str, str] = {}
        self._roles: dict[tuple[str, str], str] = {}
        self._positions: dict[int, str] = {}

    def add_object(self, object_id: str, kind: str) -> str:
        if any(item["id"] == object_id for item in self.A["U"]):
            return object_id
        rep_id = f"rep:{object_id}"
        self.A["U"].append({"id": object_id, "kind": kind})
        self.A["Pi"].append({"object": object_id, "property": "kind", "value": kind})
        self.A["Rep"].append({"id": rep_id, "kind": "representation", "represents": object_id})
        self.A["S"]["representations"].append(rep_id)
        self.A["S"]["relations"].append(["represents", rep_id, object_id])
        self.add_relation("represented_by", object_id, rep_id)
        self.add_relation("denotes", rep_id, object_id)
        return object_id

    def add_relation(self, name: str, *args: str) -> None:
        if name not in self.A["R"]:
            raise W3Error(f"unknown fixed relation: {name}")
        fact = list(args)
        if fact not in self.A["R"][name]:
            self.A["R"][name].append(fact)

    def entity(self, source_id: str, sort: str) -> str:
        if source_id in self.E:
            object_id = self.E[source_id]
            existing = next(item for item in self.A["U"] if item["id"] == object_id)
            if existing["kind"] != sort:
                raise W3Error(f"shared entity {source_id} changes target kind")
            return object_id
        object_id = self.add_object(token("entity", {"id": source_id, "sort": sort}), sort)
        self.E[source_id] = object_id
        self.add_relation("has_sort", object_id, self.sort(sort))
        return object_id

    def sort(self, sort: str) -> str:
        if sort not in self._sorts:
            object_id = self.add_object(token("sort", sort), "sort_code")
            self._sorts[sort] = object_id
            self.M["sorts"][sort] = object_id
        return self._sorts[sort]

    def role(self, kind: str, role: str) -> str:
        key = (kind, role)
        if key not in self._roles:
            object_id = self.add_object(token(f"role:{kind}", role), "role_code")
            self._roles[key] = object_id
            self.M["roles"][f"{kind}:{role}"] = object_id
        return self._roles[key]

    def value(self, value: Any) -> str:
        key = canonical_json(value)
        if key not in self._values:
            object_id = self.add_object(token("value", value), "encoded_value")
            self._values[key] = object_id
            self.M["values"][key] = object_id
            self.A["Pi"].append({"object": object_id, "property": "literal", "value": copy.deepcopy(value)})
        return self._values[key]

    def position(self, position: int) -> str:
        if position not in self._positions:
            object_id = self.add_object(token("position", position), "position_code")
            self._positions[position] = object_id
            self.A["Pi"].append({"object": object_id, "property": "position", "value": position})
        return self._positions[position]

    def semantic(self, subject: str, denotation: Any, semantic_kind: str) -> None:
        denotation_object = self.value(denotation)
        entry = {"subject": subject, "denotation": denotation_object, "kind": semantic_kind}
        if entry not in self.A["I"]:
            self.A["I"].append(entry)
        self.add_relation("has_source_denotation", subject, denotation_object)

    def finish(self) -> None:
        for key in ("U", "Pi", "Rep", "I", "Prov", "Sigma", "Theta"):
            self.A[key] = _sort_records(self.A[key])
        self.A["S"]["representations"].sort()
        self.A["S"]["relations"] = _sort_records(self.A["S"]["relations"])
        for name in self.A["R"]:
            self.A["R"][name] = _sort_records(self.A["R"][name])
        for key in self.A["C"]:
            self.A["C"][key] = _sort_records(self.A["C"][key])
        for key in self.A["H"]:
            self.A["H"][key] = _sort_records(self.A["H"][key])
        for key in self.A["Res"]:
            self.A["Res"][key] = _sort_records(self.A["Res"][key])
        self.A["Omega"]["transition_statuses"] = _sort_records(self.A["Omega"]["transition_statuses"])
