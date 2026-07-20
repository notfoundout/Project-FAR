from __future__ import annotations
import json
from typing import Any
from s_core_w3_schema import AXES, RECOVERED_SCHEMA, _entity_registry, canonical_json, parse_weight
from s_core_w3_builder import _sort_records

def expected_recovered(source: dict[str, Any], W: dict[str, Any]) -> dict[str, Any]:
    E = W["E"]; M = W["M"]
    value = lambda x: M["values"][canonical_json(x)]
    role = lambda kind, name: M["roles"][f"{kind}:{name}"]
    sort = lambda name: M["sorts"][name]
    entities = _entity_registry(source)
    expected: dict[str, Any] = {
        "schema": RECOVERED_SCHEMA,
        "carriers": _sort_records([{"id": E[item_id], "sort": sort(item_sort)} for item_id, item_sort in entities.items() if item_sort not in {"relation_occurrence", "attribute_occurrence", "cross_relation_occurrence", "component", "interface"}]),
        "axes": {}, "dynamics": {}, "semantics": {}, "decomposition": {}, "provenance": [],
    }
    for axis in AXES:
        reduct = source["axes"][axis]
        expected["axes"][axis] = {
            "members": sorted(E[str(x)] for x in reduct.get("members", [])),
            "relations": _sort_records([{"id": E[str(x["id"])], "role": role("relation", str(x["role"])), "args": [E[str(a)] for a in x.get("args", [])]} for x in reduct.get("relations", [])]),
            "attributes": _sort_records([{"id": E[str(x["id"])], "owner": E[str(x["owner"])], "role": role("attribute", str(x["role"])), "value": value(x["value"])} for x in reduct.get("attributes", [])]),
        }
    dynamics = source.get("dynamics", {}); history = dynamics.get("history", {})
    rules = _sort_records([{"id": E[str(x["id"])], "kind": value(x.get("kind"))} for x in dynamics.get("rules", [])])
    versions = _sort_records([{"id": E[str(x["id"])], "rule": E[str(x["rule"])], "version": value(x.get("version"))} for x in dynamics.get("rule_versions", [])])
    states = _sort_records([{
        "id": E[str(x["id"])],
        "commitments": _sort_records([{"subject": E[str(k)] if str(k) in E else value(k), "value": value(v)} for k, v in x.get("commitments", {}).items()]),
        "active_rule_versions": sorted(E[str(v)] for v in x.get("active_rule_versions", [])),
        "resources": _sort_records([{"resource": value(k), "value": value(v)} for k, v in x.get("resources", {}).items()]),
    } for x in dynamics.get("states", [])])
    transitions = _sort_records([{
        "id": E[str(x["id"])], "from": E[str(x["from"])], "to": E[str(x["to"])], "label": value(x["label"]),
        "status": value(str(x["status"])), "rule_version": E[str(x["rule_version"])] if x.get("rule_version") is not None else None,
        "kernel": value(x["kernel"]) if x.get("kernel") is not None else None,
        "weight": str(parse_weight(x.get("weight"))) if x.get("weight") is not None else None,
        "preconditions": sorted(value(v) for v in x.get("preconditions", [])), "resource_conditions": sorted(value(v) for v in x.get("resource_conditions", [])),
        "action_dependencies": sorted(value(v) for v in x.get("action_dependencies", [])), "observation_dependencies": sorted(value(v) for v in x.get("observation_dependencies", [])),
    } for x in dynamics.get("transitions", [])])
    events = _sort_records([{"id": E[str(x["id"])], "state": E[str(x["state"])], "transition": E[str(x["transition"])] if x.get("transition") is not None else None, "kind": value(x.get("kind"))} for x in history.get("events", [])])
    hist = {
        "events": events,
        "order": _sort_records([[E[str(a)], E[str(b)]] for a, b in history.get("order", [])]),
        "causal": _sort_records([[E[str(a)], E[str(b)]] for a, b in history.get("causal", [])]),
        "provenance": _sort_records([{"event": E[str(x["event"])], "source": value(x.get("source")), "grade": value(x.get("grade"))} for x in history.get("provenance", [])]),
        "revisions": _sort_records([{"id": value(x.get("id")), "event": E[str(x["event"])], "before_state": E[str(x["before_state"])], "after_state": E[str(x["after_state"])], "subject": E[str(x.get("subject"))] if str(x.get("subject")) in E else value(x.get("subject")), "kind": value(x.get("kind")), "before": value(x.get("before")), "after": value(x.get("after")), "basis": value(x.get("basis"))} for x in history.get("revisions", [])]),
        "modifications": _sort_records([{"id": value(x.get("id")), "event": E[str(x["event"])], "before_state": E[str(x["before_state"])], "after_state": E[str(x["after_state"])], "proposal": value(x.get("proposal")), "decision": value(x.get("decision")), "deactivates": sorted(E[str(v)] for v in x.get("deactivates", [])), "activates": sorted(E[str(v)] for v in x.get("activates", []))} for x in history.get("modifications", [])]),
        "dependency_ancestry": _sort_records([[E[str(a)], E[str(b)]] for a, b in history.get("dependency_ancestry", [])]),
        "path_conditions": _sort_records([{"id": value(x.get("id")), "path": [E[str(v)] for v in x.get("path", [])], "effect": value(x.get("effect"))} for x in history.get("path_conditions", [])]),
    }
    statuses = _sort_records([[E[str(x["id"])], value(str(x["status"]))] for x in dynamics.get("transitions", [])])
    expected["dynamics"] = {"rules": rules, "rule_versions": versions, "states": states, "transitions": transitions, "history": hist, "transition_statuses": statuses}

    interpretations = []
    for item in source.get("carriers", []):
        interpretations.append({"subject": E[str(item["id"])], "denotation": value(item["denotation"]), "kind": "carrier"})
    for item in source.get("semantics", {}).get("sort_denotations", []):
        interpretations.append({"subject": sort(str(item["sort"])), "denotation": value(item["denotation"]), "kind": "sort"})
    for item in source.get("semantics", {}).get("role_denotations", []):
        interpretations.append({"subject": role(str(item["kind"]), str(item["role"])), "denotation": value(item["denotation"]), "kind": f"role:{item['kind']}"})
    equivalences = _sort_records([[value(x["left"]), value(x["right"]), value(x.get("rule", "exact"))] for x in source.get("semantics", {}).get("value_equivalences", [])])
    expected["semantics"] = {
        "interpretations": _sort_records(interpretations),
        "value_literals": _sort_records([{"object": object_id, "literal": json.loads(key)} for key, object_id in M["values"].items()]),
        "equivalences": equivalences,
    }
    decomposition = source.get("decomposition", {})
    expected["decomposition"] = {
        "components": sorted(E[str(x["id"])] for x in decomposition.get("components", [])),
        "interfaces": sorted(E[str(x["id"])] for x in decomposition.get("interfaces", [])),
        "component_members": _sort_records([[E[str(x["id"])], E[str(m)]] for x in decomposition.get("components", []) for m in x.get("members", [])]),
        "interface_members": _sort_records([[E[str(x["id"])], E[str(m)]] for x in decomposition.get("interfaces", []) for m in x.get("members", [])]),
        "interface_links": _sort_records([[E[str(x["id"])], E[str(c)]] for x in decomposition.get("interfaces", []) for c in x.get("components", [])]),
        "cross_component_relations": _sort_records([{"id": E[str(x["id"])], "role": role("cross", str(x["role"])), "args": [E[str(a)] for a in x.get("args", [])]} for x in decomposition.get("cross_component_relations", [])]),
    }
    expected["provenance"] = hist["provenance"] + _sort_records([{"owner": E[str(x["owner"])], "role": role("attribute", str(x["role"])), "value": value(x["value"])} for x in source["axes"]["P8I"].get("attributes", [])])
    expected["provenance"] = _sort_records(expected["provenance"])
    return expected
