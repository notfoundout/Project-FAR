from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from typing import Any
from s_core_w3_schema import AXES, DECISIONS, LIVE_STATUS, REVISION_KINDS, W3Error, _entity_registry, _unique, canonical_json, parse_weight

def validate_source(source: dict[str, Any]) -> None:
    if source.get("schema_version") != "1.0":
        raise W3Error("source.schema_version must equal 1.0")
    carriers = _unique(source.get("carriers", []), "carrier")
    entities = _entity_registry(source)
    axes = source.get("axes")
    if not isinstance(axes, dict) or set(axes) != set(AXES):
        raise W3Error(f"source.axes must contain exactly {list(AXES)}")

    role_uses: set[tuple[str, str]] = set()
    for axis in AXES:
        reduct = axes[axis]
        members = [str(x) for x in reduct.get("members", [])]
        if len(members) != len(set(members)):
            raise W3Error(f"duplicate {axis} member")
        if set(members) - set(carriers):
            raise W3Error(f"{axis} has undeclared carrier members")
        for relation in reduct.get("relations", []):
            relation_id = str(relation.get("id", ""))
            role = str(relation.get("role", ""))
            args = [str(x) for x in relation.get("args", [])]
            if not relation_id or not role or not args:
                raise W3Error(f"{axis} relation requires id, role, and nonempty args")
            if set(args) - set(members):
                raise W3Error(f"{axis} relation {relation_id} references nonmember")
            role_uses.add(("relation", role))
        for attribute in reduct.get("attributes", []):
            attribute_id = str(attribute.get("id", ""))
            role = str(attribute.get("role", ""))
            owner = str(attribute.get("owner", ""))
            if not attribute_id or not role or owner not in members or "value" not in attribute:
                raise W3Error(f"{axis} attribute requires id, role, member owner, and value")
            role_uses.add(("attribute", role))

    semantics = source.get("semantics", {})
    role_semantics = {
        (str(x.get("kind", "")), str(x.get("role", ""))): x
        for x in semantics.get("role_denotations", [])
    }
    missing_roles = role_uses - set(role_semantics)
    if missing_roles:
        raise W3Error(f"missing role denotations: {sorted(missing_roles)}")
    sort_semantics = {str(x.get("sort", "")): x for x in semantics.get("sort_denotations", [])}
    missing_sorts = set(entities.values()) - set(sort_semantics)
    if missing_sorts:
        raise W3Error(f"missing sort denotations: {sorted(missing_sorts)}")
    for carrier_id, carrier in carriers.items():
        if "denotation" not in carrier:
            raise W3Error(f"carrier {carrier_id} lacks denotation")

    dynamics = source.get("dynamics", {})
    states = _unique(dynamics.get("states", []), "state")
    transitions = _unique(dynamics.get("transitions", []), "transition")
    rules = _unique(dynamics.get("rules", []), "rule")
    versions = _unique(dynamics.get("rule_versions", []), "rule_version")
    events = _unique(dynamics.get("history", {}).get("events", []), "event")
    for version_id, version in versions.items():
        if str(version.get("rule", "")) not in rules:
            raise W3Error(f"rule version {version_id} references unknown rule")
    for state_id, state in states.items():
        active = {str(x) for x in state.get("active_rule_versions", [])}
        if active - set(versions):
            raise W3Error(f"state {state_id} has unknown active rule version")
        if not isinstance(state.get("commitments", {}), dict) or not isinstance(state.get("resources", {}), dict):
            raise W3Error(f"state {state_id} commitments/resources must be objects")
    kernels: dict[tuple[str, str], list[Fraction]] = defaultdict(list)
    for transition_id, transition in transitions.items():
        source_state = str(transition.get("from", ""))
        target_state = str(transition.get("to", ""))
        if source_state not in states or target_state not in states:
            raise W3Error(f"transition {transition_id} references unknown state")
        status = str(transition.get("status", ""))
        if not status or "label" not in transition:
            raise W3Error(f"transition {transition_id} requires status and label")
        version = transition.get("rule_version")
        if version is not None:
            version = str(version)
            if version not in versions:
                raise W3Error(f"transition {transition_id} references unknown rule version")
            if status == LIVE_STATUS and version not in states[source_state].get("active_rule_versions", []):
                raise W3Error(f"permitted transition {transition_id} uses inactive rule version")
        weight = parse_weight(transition.get("weight"))
        kernel = transition.get("kernel")
        if (kernel is None) != (weight is None):
            raise W3Error(f"transition {transition_id} kernel and weight must occur together")
        if weight is not None:
            if weight < 0:
                raise W3Error(f"transition {transition_id} has negative weight")
            if status == LIVE_STATUS:
                kernels[(source_state, canonical_json(kernel))].append(weight)
    for key, weights in kernels.items():
        if sum(weights, Fraction(0, 1)) != Fraction(1, 1):
            raise W3Error(f"live kernel {key} weights must sum to 1")

    history = dynamics.get("history", {})
    event_ids = set(events)
    for event_id, event in events.items():
        if str(event.get("state", "")) not in states:
            raise W3Error(f"event {event_id} references unknown state")
        transition = event.get("transition")
        if transition is not None and str(transition) not in transitions:
            raise W3Error(f"event {event_id} references unknown transition")
    for name in ("order", "causal", "dependency_ancestry"):
        for pair in history.get(name, []):
            if not isinstance(pair, list) or len(pair) != 2 or set(map(str, pair)) - event_ids:
                raise W3Error(f"history.{name} has unknown event pair")
    for item in history.get("provenance", []):
        if str(item.get("event", "")) not in event_ids:
            raise W3Error("history provenance references unknown event")
    for item in history.get("revisions", []):
        if str(item.get("kind", "")) not in REVISION_KINDS:
            raise W3Error("revision kind invalid")
        before_state = str(item.get("before_state", "")); after_state = str(item.get("after_state", ""))
        event = str(item.get("event", "")); subject = str(item.get("subject", ""))
        if before_state not in states or after_state not in states or event not in event_ids or not subject:
            raise W3Error("revision references unknown state/event or lacks subject")
        if states[before_state].get("commitments", {}).get(subject) != item.get("before"):
            raise W3Error("revision before value mismatches state")
        if states[after_state].get("commitments", {}).get(subject) != item.get("after"):
            raise W3Error("revision after value mismatches state")
    for item in history.get("modifications", []):
        decision = str(item.get("decision", ""))
        if decision not in DECISIONS:
            raise W3Error("modification decision invalid")
        before_state = str(item.get("before_state", "")); after_state = str(item.get("after_state", ""))
        event = str(item.get("event", ""))
        if before_state not in states or after_state not in states or event not in event_ids:
            raise W3Error("modification references unknown state/event")
        before_active = set(map(str, states[before_state].get("active_rule_versions", [])))
        after_active = set(map(str, states[after_state].get("active_rule_versions", [])))
        deactivates = set(map(str, item.get("deactivates", [])))
        activates = set(map(str, item.get("activates", [])))
        if not (deactivates | activates) <= set(versions):
            raise W3Error("modification references unknown rule version")
        if decision == "accepted" and after_active != (before_active - deactivates) | activates:
            raise W3Error("accepted modification has incorrect active versions")
        if decision == "rejected" and after_active != before_active:
            raise W3Error("rejected modification changes active versions")
    for item in history.get("path_conditions", []):
        path = [str(x) for x in item.get("path", [])]
        if not path or set(path) - event_ids:
            raise W3Error("path condition references unknown or empty path")

    decomposition = source.get("decomposition", {})
    components = _unique(decomposition.get("components", []), "component")
    interfaces = _unique(decomposition.get("interfaces", []), "interface")
    admissible_members = set(entities)
    for component_id, component in components.items():
        members = {str(x) for x in component.get("members", [])}
        if not members or members - admissible_members:
            raise W3Error(f"component {component_id} has empty or unknown membership")
    for interface_id, interface in interfaces.items():
        members = {str(x) for x in interface.get("members", [])}
        links = {str(x) for x in interface.get("components", [])}
        if not members or members - admissible_members or not links or links - set(components):
            raise W3Error(f"interface {interface_id} has invalid members/components")
    cross_roles: set[tuple[str, str]] = set()
    for item in decomposition.get("cross_component_relations", []):
        args = {str(x) for x in item.get("args", [])}
        role = str(item.get("role", ""))
        if not role or not args or args - admissible_members:
            raise W3Error("cross-component relation invalid")
        cross_roles.add(("cross", role))
    missing_cross = cross_roles - set(role_semantics)
    if missing_cross:
        raise W3Error(f"missing cross role denotations: {sorted(missing_cross)}")
