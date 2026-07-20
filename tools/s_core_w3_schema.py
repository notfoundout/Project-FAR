#!/usr/bin/env python3
"""Finite executable reference for SCORE-W3-PROOF-001.

This module corroborates the W3 global-witness construction on finite fixtures.
It intentionally separates construction, target-only recovery, correspondence,
semantics, machinery accounting, decomposition, and verification. It is not a
proof assistant and does not establish the final S_core theorem.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict, deque
from fractions import Fraction
from typing import Any

SCHEMA = "FARA-WITNESS-1.0"
RECOVERY_SCHEMA = "RECOVER-FARA-1.0"
RECOVERED_SCHEMA = "RECOVERED-SCORE-1.0"
AXES = ("P1", "P2", "P3", "P4", "P6", "P8I")
LIVE_STATUS = "permitted"
REVISION_KINDS = {"revise", "retract", "supersede"}
DECISIONS = {"accepted", "rejected"}

FIXED_RELATIONS = (
    "represented_by", "denotes", "has_sort", "axis_member", "in_axis",
    "occurrence_role", "argument", "attribute_owner", "attribute_role",
    "attribute_value", "has_source_denotation", "source_equivalent",
    "component_member", "interface_member", "interface_for_component",
    "cross_occurrence_role", "cross_argument",
)

REQUIRED_A_FIELDS = (
    "U", "Pi", "R", "Rep", "S", "I", "Inv", "C", "Sigma", "Theta",
    "H", "Omega", "Res", "Prov",
)
REQUIRED_W_FIELDS = ("E", "D", "M", "iota", "kappa")


class W3Error(ValueError):
    """Malformed finite W3 source, target, recovery, or machinery package."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def token(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:20]
    return f"{prefix}:{digest}"


def parse_weight(value: Any) -> Fraction | None:
    if value is None:
        return None
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise W3Error(f"invalid exact weight: {value}") from exc
    if isinstance(value, list) and len(value) == 2:
        try:
            return Fraction(int(value[0]), int(value[1]))
        except (ValueError, ZeroDivisionError) as exc:
            raise W3Error(f"invalid exact weight: {value}") from exc
    raise W3Error(f"invalid exact weight: {value!r}")


def _unique(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        item_id = str(item.get("id", ""))
        if not item_id:
            raise W3Error(f"{label} requires id")
        if item_id in result:
            raise W3Error(f"duplicate {label}: {item_id}")
        result[item_id] = item
    return result


def _entity_registry(source: dict[str, Any]) -> dict[str, str]:
    entities: dict[str, str] = {}

    def add(item_id: str, sort: str) -> None:
        if not item_id or not sort:
            raise W3Error("entity id and sort are required")
        old = entities.setdefault(item_id, sort)
        if old != sort:
            raise W3Error(f"entity {item_id} changes sort: {old} -> {sort}")

    for item in source.get("carriers", []):
        add(str(item.get("id", "")), str(item.get("sort", "")))
    dynamics = source.get("dynamics", {})
    for item in dynamics.get("states", []):
        add(str(item.get("id", "")), "configuration")
    for item in dynamics.get("rules", []):
        add(str(item.get("id", "")), "rule")
    for item in dynamics.get("rule_versions", []):
        add(str(item.get("id", "")), "rule_version")
    for item in dynamics.get("transitions", []):
        add(str(item.get("id", "")), "transition")
    for item in dynamics.get("history", {}).get("events", []):
        add(str(item.get("id", "")), "event")
    decomposition = source.get("decomposition", {})
    for item in decomposition.get("components", []):
        add(str(item.get("id", "")), "component")
    for item in decomposition.get("interfaces", []):
        add(str(item.get("id", "")), "interface")
    for axis, reduct in source.get("axes", {}).items():
        for relation in reduct.get("relations", []):
            add(str(relation.get("id", "")), "relation_occurrence")
        for attribute in reduct.get("attributes", []):
            add(str(attribute.get("id", "")), "attribute_occurrence")
    for item in decomposition.get("cross_component_relations", []):
        add(str(item.get("id", "")), "cross_relation_occurrence")
    return entities
