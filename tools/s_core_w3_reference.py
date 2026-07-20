#!/usr/bin/env python3
"""Finite executable reference facade for SCORE-W3-PROOF-001."""
from __future__ import annotations
import copy
import hashlib
from typing import Any
from s_core_w3_schema import AXES, SCHEMA, W3Error, canonical_json
from s_core_w3_validation import validate_source
from s_core_w3_construct import construct_witness
from s_core_w3_recovery import recover_target, validate_package
from s_core_w3_expected import expected_recovered
from s_core_w3_builder import _sort_records

def semantic_agreement(source: dict[str, Any], package: dict[str, Any]) -> bool:
    try:
        expected = expected_recovered(source, package["W"])["semantics"]
        recovered = recover_target(package["A"], package["W"]["D"], package["W"]["kappa"])["semantics"]
        return expected == recovered and package["W"]["iota"]["no_lexical_shortcuts"] is True
    except (KeyError, TypeError, W3Error):
        return False


def cross_axis_coherent(source: dict[str, Any], package: dict[str, Any]) -> bool:
    try:
        E = package["W"]["E"]; recovered = recover_target(package["A"], package["W"]["D"], package["W"]["kappa"])
        for source_id in {x for axis in AXES for x in source["axes"][axis].get("members", [])}:
            target_id = E[str(source_id)]
            for axis in AXES:
                present = str(source_id) in source["axes"][axis].get("members", [])
                if (target_id in recovered["axes"][axis]["members"]) != present:
                    return False
        object_ids = [x["id"] for x in package["A"]["U"]]
        return len(object_ids) == len(set(object_ids))
    except (KeyError, TypeError, W3Error):
        return False


def component_view(recovered: dict[str, Any], component_id: str) -> dict[str, Any]:
    decomposition = recovered["decomposition"]
    components = set(decomposition.get("components", []))
    if component_id not in components:
        raise W3Error("unknown component")
    allowed = {member for component, member in decomposition.get("component_members", []) if component == component_id}
    linked_interfaces = {interface for interface, component in decomposition.get("interface_links", []) if component == component_id}
    allowed |= {member for interface, member in decomposition.get("interface_members", []) if interface in linked_interfaces}
    axes = {}
    for axis, reduct in recovered["axes"].items():
        axes[axis] = {
            "members": sorted(set(reduct["members"]) & allowed),
            "relations": _sort_records([x for x in reduct["relations"] if set(x["args"]) <= allowed]),
            "attributes": _sort_records([x for x in reduct["attributes"] if x["owner"] in allowed]),
        }
    cross = _sort_records([x for x in decomposition.get("cross_component_relations", []) if set(x["args"]) & allowed])
    return {"component": component_id, "allowed": sorted(allowed), "axes": axes, "cross_component_relations": cross}


def compositional_accountability(source: dict[str, Any], package: dict[str, Any]) -> bool:
    try:
        recovered = recover_target(package["A"], package["W"]["D"], package["W"]["kappa"])
        E = package["W"]["E"]
        for component in source.get("decomposition", {}).get("components", []):
            view = component_view(recovered, E[str(component["id"])])
            member_targets = {E[str(x)] for x in component.get("members", [])}
            linked = [x for x in source["decomposition"].get("interfaces", []) if str(component["id"]) in x.get("components", [])]
            member_targets |= {E[str(m)] for x in linked for m in x.get("members", [])}
            if set(view["allowed"]) != member_targets:
                return False
            expected_cross = [x for x in expected_recovered(source, package["W"])["decomposition"]["cross_component_relations"] if set(x["args"]) & member_targets]
            if view["cross_component_relations"] != _sort_records(expected_cross):
                return False
        return True
    except (KeyError, TypeError, W3Error):
        return False


def verify_witness(source: dict[str, Any], package: dict[str, Any]) -> bool:
    try:
        validate_source(source); validate_package(package)
        recovered = recover_target(package["A"], package["W"]["D"], package["W"]["kappa"])
        expected = expected_recovered(source, package["W"])
        return recovered == expected and semantic_agreement(source, package) and cross_axis_coherent(source, package) and compositional_accountability(source, package)
    except (KeyError, TypeError, ValueError, W3Error):
        return False


def structural_digest(package: dict[str, Any]) -> str:
    structural = copy.deepcopy(package)
    structural["W"].pop("E", None)
    structural["W"].pop("M", None)
    return hashlib.sha256(canonical_json(structural).encode("utf-8")).hexdigest()


def deep_copy(value: Any) -> Any:
    return copy.deepcopy(value)


__all__ = ["W3Error", "canonical_json", "component_view", "construct_witness", "cross_axis_coherent", "deep_copy", "recover_target", "semantic_agreement", "structural_digest", "validate_package", "validate_source", "verify_witness"]
