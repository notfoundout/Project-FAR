from __future__ import annotations
import copy
from typing import Any
from s_core_w3_schema import AXES, RECOVERY_SCHEMA, SCHEMA, _entity_registry, canonical_json, parse_weight, token
from s_core_w3_validation import validate_source
from s_core_w3_builder import Builder, _sort_records
from s_core_w3_machinery import machinery_ledger

def construct_witness(source: dict[str, Any]) -> dict[str, Any]:
    validate_source(source)
    entities = _entity_registry(source)
    builder = Builder()
    for source_id, sort in sorted(entities.items()):
        builder.entity(source_id, sort)

    carriers = {str(item["id"]): item for item in source.get("carriers", [])}
    for source_id, carrier in sorted(carriers.items()):
        builder.semantic(builder.E[source_id], carrier["denotation"], "carrier")
    semantics = source.get("semantics", {})
    for item in semantics.get("sort_denotations", []):
        builder.semantic(builder.sort(str(item["sort"])), item["denotation"], "sort")
    for item in semantics.get("role_denotations", []):
        builder.semantic(builder.role(str(item["kind"]), str(item["role"])), item["denotation"], f"role:{item['kind']}")
    for item in semantics.get("value_equivalences", []):
        left = builder.value(item["left"]); right = builder.value(item["right"]); rule = builder.value(item.get("rule", "exact"))
        builder.add_relation("source_equivalent", left, right, rule)

    for axis in AXES:
        axis_id = builder.add_object(f"axis:{axis}", "axis_code")
        reduct = source["axes"][axis]
        for source_id in reduct.get("members", []):
            builder.add_relation("axis_member", axis_id, builder.E[str(source_id)])
        for relation in sorted(reduct.get("relations", []), key=lambda x: str(x["id"])):
            occurrence = builder.E[str(relation["id"])]
            role = builder.role("relation", str(relation["role"]))
            builder.add_relation("in_axis", occurrence, axis_id)
            builder.add_relation("occurrence_role", occurrence, role)
            for position, source_id in enumerate(relation.get("args", []), start=1):
                builder.add_relation("argument", occurrence, builder.position(position), builder.E[str(source_id)])
        for attribute in sorted(reduct.get("attributes", []), key=lambda x: str(x["id"])):
            occurrence = builder.E[str(attribute["id"])]
            role = builder.role("attribute", str(attribute["role"]))
            value = builder.value(attribute["value"])
            builder.add_relation("in_axis", occurrence, axis_id)
            builder.add_relation("attribute_owner", occurrence, builder.E[str(attribute["owner"])])
            builder.add_relation("attribute_role", occurrence, role)
            builder.add_relation("attribute_value", occurrence, value)
            if axis == "P8I":
                builder.A["Prov"].append({"owner": builder.E[str(attribute["owner"])], "role": role, "value": value})

    dynamics = source.get("dynamics", {})
    states = {str(x["id"]): x for x in dynamics.get("states", [])}
    rules = {str(x["id"]): x for x in dynamics.get("rules", [])}
    versions = {str(x["id"]): x for x in dynamics.get("rule_versions", [])}
    transitions = {str(x["id"]): x for x in dynamics.get("transitions", [])}
    history = dynamics.get("history", {})
    events = {str(x["id"]): x for x in history.get("events", [])}

    for state_id, state in sorted(states.items()):
        builder.A["Sigma"].append({
            "id": builder.E[state_id],
            "commitments": _sort_records([{"subject": builder.E[key] if key in builder.E else builder.value(key), "value": builder.value(value)} for key, value in state.get("commitments", {}).items()]),
            "active_rule_versions": sorted(builder.E[str(x)] for x in state.get("active_rule_versions", [])),
            "resources": _sort_records([{"resource": builder.value(key), "value": builder.value(value)} for key, value in state.get("resources", {}).items()]),
        })
        for version in state.get("active_rule_versions", []):
            builder.A["C"]["active_rule_versions"].append([builder.E[state_id], builder.E[str(version)]])
    for rule_id, rule in sorted(rules.items()):
        builder.A["C"]["rules"].append({"id": builder.E[rule_id], "kind": builder.value(rule.get("kind"))})
    for version_id, version in sorted(versions.items()):
        builder.A["C"]["rule_versions"].append({
            "id": builder.E[version_id], "rule": builder.E[str(version["rule"])], "version": builder.value(version.get("version")),
        })
    for transition_id, transition in sorted(transitions.items()):
        version = transition.get("rule_version")
        record = {
            "id": builder.E[transition_id], "from": builder.E[str(transition["from"])], "to": builder.E[str(transition["to"])],
            "label": builder.value(transition["label"]), "status": builder.value(str(transition["status"])),
            "rule_version": builder.E[str(version)] if version is not None else None,
            "kernel": builder.value(transition["kernel"]) if transition.get("kernel") is not None else None,
            "weight": str(parse_weight(transition.get("weight"))) if transition.get("weight") is not None else None,
            "preconditions": sorted(builder.value(x) for x in transition.get("preconditions", [])),
            "resource_conditions": sorted(builder.value(x) for x in transition.get("resource_conditions", [])),
            "action_dependencies": sorted(builder.value(x) for x in transition.get("action_dependencies", [])),
            "observation_dependencies": sorted(builder.value(x) for x in transition.get("observation_dependencies", [])),
        }
        builder.A["Theta"].append(record)
        builder.A["Omega"]["transition_statuses"].append([builder.E[transition_id], record["status"]])
    for event_id, event in sorted(events.items()):
        transition = event.get("transition")
        builder.A["H"]["events"].append({
            "id": builder.E[event_id], "state": builder.E[str(event["state"])],
            "transition": builder.E[str(transition)] if transition is not None else None,
            "kind": builder.value(event.get("kind")),
        })
    for key in ("order", "causal", "dependency_ancestry"):
        builder.A["H"][key] = [[builder.E[str(a)], builder.E[str(b)]] for a, b in history.get(key, [])]
    for item in history.get("provenance", []):
        record = {"event": builder.E[str(item["event"])], "source": builder.value(item.get("source")), "grade": builder.value(item.get("grade"))}
        builder.A["H"]["provenance"].append(record); builder.A["Prov"].append(copy.deepcopy(record))
    for item in history.get("revisions", []):
        builder.A["H"]["revisions"].append({
            "id": builder.value(item.get("id")), "event": builder.E[str(item["event"])],
            "before_state": builder.E[str(item["before_state"])], "after_state": builder.E[str(item["after_state"])],
            "subject": builder.E[str(item.get("subject"))] if str(item.get("subject")) in builder.E else builder.value(item.get("subject")), "kind": builder.value(item.get("kind")),
            "before": builder.value(item.get("before")), "after": builder.value(item.get("after")),
            "basis": builder.value(item.get("basis")),
        })
    for item in history.get("modifications", []):
        builder.A["H"]["modifications"].append({
            "id": builder.value(item.get("id")), "event": builder.E[str(item["event"])],
            "before_state": builder.E[str(item["before_state"])], "after_state": builder.E[str(item["after_state"])],
            "proposal": builder.value(item.get("proposal")), "decision": builder.value(item.get("decision")),
            "deactivates": sorted(builder.E[str(x)] for x in item.get("deactivates", [])),
            "activates": sorted(builder.E[str(x)] for x in item.get("activates", [])),
        })
    for item in history.get("path_conditions", []):
        builder.A["H"]["path_conditions"].append({
            "id": builder.value(item.get("id")), "path": [builder.E[str(x)] for x in item.get("path", [])],
            "effect": builder.value(item.get("effect")),
        })

    decomposition = source.get("decomposition", {})
    for component in sorted(decomposition.get("components", []), key=lambda x: str(x["id"])):
        component_id = builder.E[str(component["id"])]
        builder.A["Res"]["components"].append(component_id)
        for member in component.get("members", []):
            pair = [component_id, builder.E[str(member)]]
            builder.A["Res"]["component_members"].append(pair)
            builder.add_relation("component_member", *pair)
    for interface in sorted(decomposition.get("interfaces", []), key=lambda x: str(x["id"])):
        interface_id = builder.E[str(interface["id"])]
        builder.A["Res"]["interfaces"].append(interface_id)
        for member in interface.get("members", []):
            pair = [interface_id, builder.E[str(member)]]
            builder.A["Res"]["interface_members"].append(pair)
            builder.add_relation("interface_member", *pair)
        for component in interface.get("components", []):
            pair = [interface_id, builder.E[str(component)]]
            builder.A["Res"]["interface_links"].append(pair)
            builder.add_relation("interface_for_component", *pair)
    for item in sorted(decomposition.get("cross_component_relations", []), key=lambda x: str(x["id"])):
        occurrence = builder.E[str(item["id"])]
        role = builder.role("cross", str(item["role"]))
        args = [builder.E[str(x)] for x in item.get("args", [])]
        builder.A["Res"]["cross_component_relations"].append({"id": occurrence, "role": role, "args": args})
        builder.add_relation("cross_occurrence_role", occurrence, role)
        for position, arg in enumerate(args, start=1):
            builder.add_relation("cross_argument", occurrence, builder.position(position), arg)

    builder.finish()
    kappa = machinery_ledger()
    return {
        "schema": SCHEMA,
        "A": builder.A,
        "W": {
            "E": builder.E,
            "D": {"schema": RECOVERY_SCHEMA, "algorithm": "recover_target", "target_only": True, "deterministic": True, "terminates_on_finite_target": True},
            "M": builder.M,
            "iota": {"component": "A.I", "semantic_equivalence": "A.R.source_equivalent", "no_lexical_shortcuts": True},
            "kappa": kappa,
        },
    }
